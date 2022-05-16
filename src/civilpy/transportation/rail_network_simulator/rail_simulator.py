"""
CivilPy
Copyright (C) 2019 - Dane Parks

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
Modified Version of UXSim code by toruseo on github:
https://github.com/toruseo/UXsim

UXsim: Macroscopic/mesoscopic traffic flow simulator in a network.
This `uxsim.py` is the core of UXsim. It summarizes the classes and methods that are essential for the simulation.
"""

import random, csv, time, math, string, warnings
from collections import deque, OrderedDict
from collections import defaultdict as ddict

import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse.csgraph import floyd_warshall
import dill as pickle

from src.rail_network_simulator.analyzer import *
from src.rail_network_simulator.utils import *

from matplotlib.offsetbox import OffsetImage, AnnotationBbox


class Node:
    def __init__(
        self,
        W,
        name,
        x,
        y,
        signal=[0],
        signal_offset=0,
        number_of_lanes=1,
        block_control=0,
        flow_capacity=None,
        auto_rename=False,
        label_color="black",
        voffset=0,
        hoffset=0,
    ):

        self.W = W

        self.x = x
        self.y = y
        self.color = "green"
        self.label_color = label_color
        self.voffset = voffset
        self.hoffset = hoffset

        self.inbound_traffic = {}
        self.outbound_traffic = {}

        self.inbound_vehicles = []

        # Inbound Vehicle Queue
        self.generation_queue = deque()

        # Part of a Signalized Interlocking
        self.signal = signal
        self.signal_phase = 0
        self.signal_t = 0
        self.signal_offset = signal_offset
        offset = self.signal_offset
        if self.signal != [0]:
            i = 0
            while 1:
                if offset < self.signal[i]:
                    self.signal_phase = i
                    self.signal_t = offset
                    break
                offset -= self.signal[i]

                i += 1
                if i >= len(self.signal):
                    i = 0

        self.signal_log = []

        # flowRestrictionMacroSignal
        self.flag_lanes_automatically_determined = False
        if flow_capacity != None:
            self.flow_capacity = flow_capacity
            self.flow_capacity_remain = flow_capacity * self.W.DELTAT
            if number_of_lanes != None:
                self.lanes = number_of_lanes
            else:
                self.lanes = math.ceil(
                    flow_capacity / 0.8
                )  # TODO: Adjustment required. Currently, the number of lanes is determined based on the assumption that one lane is 0.8 veh/s.
                self.flag_lanes_automatically_determined = True
        else:
            self.flow_capacity = None
            self.flow_capacity_remain = 10e10
            self.lanes = None

        self.id = len(self.W.NODES)
        self.name = name
        if self.name in [n.name for n in self.W.NODES]:
            if auto_rename:
                self.name = (
                    self.name
                    + "_renamed"
                    + "".join(random.choices(string.ascii_letters + string.digits, k=8))
                )
            else:
                raise ValueError(
                    f"Node name {self.name} already used by another node. Please specify a unique name."
                )
        self.W.NODES.append(self)

    def __repr__(self):
        return f"<Node {self.name}>"

    def generate(self):
        """
        Departs vehicles from the waiting queue.

        Notes
        -----
        If there are vehicles in the generation queue of the node, this method attempts to depart a vehicle to one of the outgoing links.
        The choice of the outgoing link is based on the vehicle's route preference for each link. Once a vehicle is departed, it is removed from the generation queue, added to the list of vehicles on the chosen link, and its state is set to "run".
        """
        outbound_traffic0 = list(self.outbound_traffic.values())
        if len(outbound_traffic0):
            for i in range(sum([l.lanes for l in outbound_traffic0])):
                if len(self.generation_queue) > 0:
                    veh = self.generation_queue[0]

                    # consider the link preferences
                    outbound_traffic = list(self.outbound_traffic.values())
                    if set(outbound_traffic) & set(veh.links_prefer):
                        outbound_traffic = list(
                            set(outbound_traffic) & set(veh.links_prefer)
                        )
                    if set(outbound_traffic) & set(veh.links_avoid):
                        outbound_traffic = list(
                            set(outbound_traffic) - set(veh.links_avoid)
                        )

                    preference = [veh.route_pref[l] for l in outbound_traffic]
                    if sum(preference) > 0:
                        outlink = random.choices(outbound_traffic, preference)[0]
                    else:
                        outlink = random.choices(outbound_traffic)[0]

                    if (
                        len(outlink.vehicles) < outlink.lanes
                        or outlink.vehicles[-outlink.lanes].x
                        > outlink.delta_per_lane * self.W.DELTAN
                    ) and outlink.capacity_in_remain >= self.W.DELTAN:
                        # ifAcceptableSelectAccordingToLinkPriority
                        veh = self.generation_queue.popleft()

                        veh.state = "run"
                        veh.link = outlink
                        veh.x = 0
                        veh.v = outlink.u  # improvedEdgeBehavior
                        self.W.VEHICLES_RUNNING[veh.name] = veh

                        if len(outlink.vehicles) > 0:
                            veh.lane = (outlink.vehicles[-1].lane + 1) % outlink.lanes
                        else:
                            veh.lane = 0

                        veh.leader = None
                        if len(outlink.vehicles) >= outlink.lanes:
                            veh.leader = outlink.vehicles[-outlink.lanes]
                            veh.leader.follower = veh
                            assert veh.leader.lane == veh.lane

                        outlink.vehicles.append(veh)

                        outlink.cum_arrival[-1] += self.W.DELTAN
                        veh.link_arrival_time = self.W.T * self.W.DELTAT

                        outlink.capacity_in_remain -= self.W.DELTAN
                    else:
                        # If it is not acceptable, no inflow will occur from this node.
                        break
                else:
                    break

    def transfer(self):
        """
        Transfers vehicles between links at the node.

        Notes
        -----
        This method handles the transfer of vehicles from one link to another at the node.
        A vehicle is eligible for transfer if:
        - The next link it intends to move to has space.
        - The vehicle has the right signal phase to proceed.
        - The current link has enough capacity to allow the vehicle to exit.
        - The node capacity is not exceeded.
        """
        outbound_traffic = []
        for outlink in {
            veh.route_next_link
            for veh in self.inbound_vehicles
            if veh.route_next_link != None
        }:
            for i in range(
                outlink.lanes
            ):  # There are as many acceptance trials as there are lanes.
                outbound_traffic.append(outlink)
        random.shuffle(outbound_traffic)

        for outlink in outbound_traffic:
            if (
                (
                    len(outlink.vehicles) < outlink.lanes
                    or outlink.vehicles[-outlink.lanes].x
                    > outlink.delta_per_lane * self.W.DELTAN
                )
                and outlink.capacity_in_remain >= self.W.DELTAN
                and self.flow_capacity_remain >= self.W.DELTAN
            ):
                # If acceptable and leakable, select according to link priority
                vehs = [
                    veh
                    for veh in self.inbound_vehicles
                    if veh
                    == veh.link.vehicles[0]  # vehicleInTheLeadLaneOnTheSendingLink
                    and veh.route_next_link
                    == outlink  # destinationLinkIsAnAcceptedLink
                    and (
                        self.signal_phase in veh.link.signal_group
                        or len(self.signal) <= 1
                    )  # signalMatches
                    and veh.link.capacity_out_remain >= self.W.DELTAN
                ]
                if len(vehs) == 0:
                    continue
                veh = random.choices(vehs, [veh.link.merge_priority for veh in vehs])[
                    0
                ]  # Links with few lanes benefit from the number of trials of links with many lanes, giving them a slight advantage. There is no big difference, so I accept it.

                inlink = veh.link

                # cumulativeNumberRelatedUpdate
                inlink.cum_departure[-1] += self.W.DELTAN
                outlink.cum_arrival[-1] += self.W.DELTAN
                inlink.traveltime_actual[
                    int(veh.link_arrival_time / self.W.DELTAT) :
                ] = (
                    self.W.T * self.W.DELTAT - veh.link_arrival_time
                )  # The actual travel time after your inflow time is also tentatively determined using the current actual travel time. The assumption is that a later leaked vehicle will overwrite the information.

                veh.link_arrival_time = self.W.T * self.W.DELTAT

                inlink.capacity_out_remain -= self.W.DELTAN
                outlink.capacity_in_remain -= self.W.DELTAN
                if self.flow_capacity != None:
                    self.flow_capacity_remain -= self.W.DELTAN

                # linkTransitionExecution
                inlink.vehicles.popleft()
                veh.link = outlink
                veh.x = 0

                if veh.follower != None:
                    veh.follower.leader = None
                    veh.follower = None

                if len(outlink.vehicles) > 0:
                    veh.lane = (outlink.vehicles[-1].lane + 1) % outlink.lanes
                else:
                    veh.lane = 0

                veh.leader = None
                if len(outlink.vehicles) >= outlink.lanes:
                    veh.leader = outlink.vehicles[-outlink.lanes]
                    veh.leader.follower = veh
                    assert veh.leader.lane == veh.lane

                # remainingRunProcessing
                x_next = veh.move_remain * outlink.u / inlink.u
                if veh.leader != None:
                    x_cong = veh.leader.x_old - veh.link.delta_per_lane * veh.W.DELTAN
                    if x_cong < veh.x:
                        x_cong = veh.x
                    if x_next > x_cong:
                        x_next = x_cong
                    if x_next >= outlink.length:
                        x_next = outlink.length
                veh.x = x_next

                # If the vehicle following the vehicle that just moved is waiting for the trip to end, the trip will end.
                if (
                    len(inlink.vehicles)
                    and inlink.vehicles[0].flag_waiting_for_trip_end
                ):
                    inlink.vehicles[0].end_trip()

                outlink.vehicles.append(veh)
                self.inbound_vehicles.remove(veh)

        # Finish the trip of the vehicle waiting for the trip to end at the beginning of each link.
        for link in self.inbound_traffic.values():
            for lane in range(link.lanes):
                if len(link.vehicles) and link.vehicles[0].flag_waiting_for_trip_end:
                    link.vehicles[0].end_trip()
                else:
                    break

        self.inbound_vehicles = []


class Link:
    """
    Link in a network.
    """

    def __init__(
        self,
        W,
        name,
        start_node,
        end_node,
        length,
        free_flow_speed=20,
        jam_density=0.2,
        jam_density_per_lane=None,
        number_of_lanes=1,
        merge_priority=1,
        signal_group=0,
        capacity_out=None,
        capacity_in=None,
        eular_dx=None,
        attribute=None,
        auto_rename=False,
    ):
        """
        Create a link

        Parameters
        ----------
        W : object
            The world to which the link belongs.
        name : str
            The name of the link.
        start_node : str | Node
            The name of the start node of the link.
        end_node : str | Node
            The name of the end node of the link.
        length : float
            The length of the link.
        free_flow_speed : float, optional
            The free flow speed on the link, default is 20.
        jam_density : float, optional
            The jam density on the link, default is 0.2. If jam_density_per_lane is specified, this value is ignored.
        jam_density_per_lane : float, optional
            The jam density per lane on the link. If specified, it overrides the jam_density value.
        number_of_lanes : int, optional
            The number of lanes on the link, default is 1.
        merge_priority : float, optional
            The priority of the link when merging at the downstream node, default is 1.
        signal_group : int or list, optional
            The signal group(s) to which the link belongs, default is 0. If `signal_group` is int, say 0, it becomes green if `end_node.signal_phase` is 0. If `signal_group` is list, say [0,1], it becomes green if the `end_node.signal_phase` is 0 or 1.
        capacity_out : float, optional
            The capacity out of the link, default is calculated based on other parameters.
        capacity_in : float, optional
            The capacity into the link, default is calculated based on other parameters.
        eular_dx : float, optional
            The space aggregation size for link traffic state computation, default is 1/10 of link length or free flow distance per simulation step, whichever is larger.
        attribute : any, optional
            Additional (meta) attributes defined by users.
        auto_rename : bool, optional
            Whether to automatically rename the link if the name is already used. Default is False (raise an exception).

        Attributes
        ----------
        speed : float
            Average speed of traffic on the link.
        density : float
            Density of traffic on the link.
        flow : float
            Flow of traffic on the link.
        num_vehicles : float
            Number of vehicles on the link.
        num_vehicles_queue : float
            Number of slow vehicles (due to congestion) on the link.
        free_flow_speed : float
            Free flow speed of the link.
        jam_density : float
            Jam density of the link.
        capacity_out : float
            Capacity for outflow from the link.
        capacity_in : float
            Capacity for inflow to the link.
        merge_priority : float
            The priority of the link when merging at the downstream node.

        Notes
        -----
        Traffic Flow Model:

        - The link model follows a multi-lane, single-pipe approach where FIFO is guaranteed per link and no lane changing occurs.
        - Fundamental diagram parameters such as free_flow_speed, jam_density (or jam_density_per_lane), and number_of_lanes determine the link's flow characteristics. Reaction time of drivers `REACTION_TIME` is a grobal parameter.
        - Real-time link status for external reference is maintained with attributes `speed`, `density`, `flow`, `num_vehicles`, and `num_vehicles_queue`.

        Traffic Flow Model Parameters:

        - Their definition is illustrated as https://toruseo.jp/UXsim/docs/_images/fundamental_diagram.png
        - If you are not familiar to the traffic flow theory, it is recommended that you adjust only `free_flow_speed` and `number_of_lanes` for the traffic flow model parameters, leaving the other parameters at their default values.

        Capacity and Bottlenecks:

        - The `capacity_out` and `capacity_in` parameters set the outflow and inflow capacities of the link. If not provided, the capacities are unlimited.
        - These capacities can represent bottlenecks at the beginning or end of the link.

        Connection to Node Model:

        - At the downstream end of a sending link, vehicles in all lanes have the right to be sent out, but FIFO order is maintained.
        - At the upstream end of a receiving link, all lanes can accept vehicles.

        Parameter Adjustments:

        - Some traffic flow model parameters like `free_flow_speed`, `jam_density`, `capacity_out`, `capacity_in`, and `merge_priority` can be altered during simulation to reflect changing conditions.

        Details on Multi-lane model:

        - Link model:
            - Multiple lanes with single-pipe model. FIFO is guaranteed per link. No lane changing.
            - Links have a `lanes` attribute representing the number of lanes.
            - Each vehicle has a `lane` attribute.
            - Each vehicle follows the leader vehicle in the same lane, i.e., the vehicle `lanes` steps ahead on the link.
        - Node model:
            - Sending links:
                - Vehicles in all lanes at the downstream end of the link have the right to be sent out.
                - However, to ensure link FIFO, vehicles are tried to be sent out in the order they entered the link. If a vehicle cannot be accepted, the outflow from that link stops.
            - Receiving links:
                - All lanes at the upstream end of the link can accept vehicles.

        Details on Fundamental diagram parameters (+: input, ++: alternative input):

        - free_flow_speed (m/s)+
        - jam_density (veh/m/LINK)+
        - jam_density_per_lane (veh/m/lane)++
        - lanes, number_of_lane (lane)+
        - tau: y-intercept of link FD (s/veh*LINK)
        - REACTION_TIME, World.reaction_time (s/veh*lane)
        - w (m/s)
        - capacity (veh/s/LINK)
        - capacity_per_lane (veh/s/lane)
        - delta: minimum spacing (m/veh*LINK)
        - delta_per_lane: minimum spacing in lane (m/veh*lane)
        - q_star: capacity (veh/s/LINK)
        - k_star: critical density (veh/s/LINK)
        - capacity_in, capacity_out: bottleneck capacity at beginning/end of link (veh/s/LINK)+
        - Node.flow_capacity: node flow capacity (veh/s/LINK-LIKE)+
        """

        self.W = W
        # originDestinationNode
        self.start_node = self.W.get_node(start_node)
        self.end_node = self.W.get_node(end_node)
        self.color = "green"
        # linkLength
        self.length = length

        # NumberOfLanes
        self.lanes = int(number_of_lanes)
        if self.lanes != number_of_lanes:
            raise ValueError(
                f"number_of_lanes must be an integer. Got {number_of_lanes} at {self}."
            )

        # flowModelParameters:per link
        self.u = free_flow_speed
        self.kappa = jam_density
        if jam_density == 0.2 and jam_density_per_lane != None:
            self.kappa = jam_density_per_lane * number_of_lanes
        if jam_density != 0.2 and jam_density_per_lane != None:
            self.kappa = jam_density_per_lane * number_of_lanes
            warnings.warn(
                f"{self}: jam_density is ignored because jam_density_per_lane is set.",
                UserWarning,
            )
        self.tau = self.W.REACTION_TIME / self.lanes
        self.w = 1 / self.tau / self.kappa
        self.capacity = self.u * self.w * self.kappa / (self.u + self.w)
        self.delta = 1 / self.kappa
        self.delta_per_lane = (
            self.delta * self.lanes
        )  # m/veh for each lane. used for car-following model per lane
        self.q_star = self.capacity  # flow capacity
        self.k_star = self.capacity / self.u  # critical density

        # PriorityWhenMerging
        self.merge_priority = merge_priority

        # listOfVehiclesInTheLink
        self.vehicles = deque()

        # TravelTime
        self.traveltime_instant = []

        # RouteSelectionCorrection
        self.route_choice_penalty = 0

        # CumulativeFigureRelationship
        self.cum_arrival = []
        self.cum_departure = []
        self.traveltime_actual = []

        # signalRelated
        self.signal_group = signal_group
        if type(self.signal_group) == int:
            self.signal_group = [self.signal_group]

        # outflowCapacity
        self.capacity_out = capacity_out
        if capacity_out == None:
            self.capacity_out = self.capacity * 2
            # todo_later: capacity_out It seems that there is a slight bug (multi-discrete discretization error). At least when it is not set, it is doubled so that the bug does not become apparent.
        self.capacity_out_remain = self.capacity_out * self.W.DELTAT

        # inflowCapacity
        self.capacity_in = capacity_in
        if capacity_in == None:
            self.capacity_in = 10e10
            self.capacity_in_remain = 10e10
        else:
            self.capacity_in_remain = self.capacity_in * self.W.DELTAT

        self.id = len(self.W.LINKS)
        self.name = name
        if self.name in [l.name for l in self.W.LINKS]:
            if auto_rename:
                self.name = (
                    self.name
                    + "_renamed"
                    + "".join(random.choices(string.ascii_letters + string.digits, k=8))
                )
            else:
                raise ValueError(
                    f"Link name {self.name} already used by another link. Please specify a unique name."
                )
        self.W.LINKS.append(self)
        self.start_node.outbound_traffic[self.name] = self
        self.end_node.inbound_traffic[self.name] = self

        self.attribute = attribute

        # realTimeLinkStatusForExternalReference
        self._speed = -1  # averageSpeedAcrossLinks
        self._density = -1
        self._flow = -1
        self._num_vehicles = -1  # NumberOfVehicles
        self._num_vehicles_queue = -1  # NumberOfVehiclesBelowFreeStreamSpeed

        # MoreAccurateVehicleTrajectory
        self.tss = []
        self.xss = []
        self.cs = []
        self.ls = []
        self.names = []

        if eular_dx == None:
            self.eular_dx = self.length / 10
            if self.eular_dx < self.u * self.W.DELTAT:
                self.eular_dx = self.u * self.W.DELTAT

    def __repr__(self):
        return f"<Link {self.name}>"

    def init_after_tmax_fix(self):
        """
        Initalization before simulation execution.
        """

        # EulertypeTrafficCondition
        self.edie_dt = self.W.EULAR_DT
        self.edie_dx = self.eular_dx
        self.k_mat = np.zeros(
            [int(self.W.TMAX / self.edie_dt) + 1, int(self.length / self.edie_dx)]
        )
        self.q_mat = np.zeros(self.k_mat.shape)
        self.v_mat = np.zeros(self.k_mat.shape)
        self.tn_mat = np.zeros(self.k_mat.shape)
        self.dn_mat = np.zeros(self.k_mat.shape)
        self.an = self.edie_dt * self.edie_dx

        # accumulation
        self.traveltime_actual = np.array(
            [self.length / self.u for t in range(self.W.TSIZE)]
        )

    def update(self):
        """
        Make necessary updates when the timestep is incremented.
        """
        self.in_out_flow_constraint()

        self.set_traveltime_instant()
        self.cum_arrival.append(0)
        self.cum_departure.append(0)
        if len(self.cum_arrival) > 1:
            self.cum_arrival[-1] = self.cum_arrival[-2]
            self.cum_departure[-1] = self.cum_departure[-2]

        # RealTimeStateReset
        self._speed = -1
        self._density = -1
        self._flow = -1
        self._num_vehicles = -1
        self._num_vehicles_queue = -1

    def in_out_flow_constraint(self):
        """
        Link capacity updates.
        """
        # Processing to keep the link inflow/outflow rate below the outflow capacity. Ensure maximum number of passes per time step
        if self.capacity_in != None:
            if self.capacity_out_remain < self.W.DELTAN * self.lanes:
                self.capacity_out_remain += self.capacity_out * self.W.DELTAT
            if self.capacity_in_remain < self.W.DELTAN * self.lanes:
                self.capacity_in_remain += self.capacity_in * self.W.DELTAT
        else:
            self.capacity_out_remain = 10e10
            self.capacity_in_remain = 10e10

    def set_traveltime_instant(self):
        """
        Compute instantanious travel time.
        """
        if self.speed > 0:
            self.traveltime_instant.append(self.length / self.speed)
        else:
            self.traveltime_instant.append(self.length / (self.u / 100))

    def arrival_count(self, t):
        """
        Get cumulative vehicle count of arrival to this link on time t

        Parameters
        ----------
        t : float
            Time in seconds.

        Returns
        -------
        float
            The cumulative arrival vehicle count.
        """
        tt = int(t // self.W.DELTAT)
        if tt >= len(self.cum_arrival):
            return self.cum_arrival[-1]
        if tt < 0:
            return self.cum_arrival[0]
        return self.cum_arrival[tt]

    def departure_count(self, t):
        """
        Get cumulative vehicle count of departure from this link on time t

        Parameters
        ----------
        t : float
            Time in seconds.

        Returns
        -------
        float
            The cumulative departure vehicle count.
        """
        tt = int(t // self.W.DELTAT)
        if tt >= len(self.cum_departure):
            return self.cum_departure[-1]
        if tt < 0:
            return self.cum_departure[0]
        return self.cum_departure[tt]

    def instant_travel_time(self, t):
        """
        Get instantanious travel time of this link on time t

        Parameters
        ----------
        t : float
            Time in seconds.

        Returns
        -------
        float
            The instantanious travel time.
        """
        tt = int(t // self.W.DELTAT)
        if tt >= len(self.traveltime_instant):
            return self.traveltime_instant[-1]
        if tt < 0:
            return self.traveltime_instant[0]
        return self.traveltime_instant[tt]

    def actual_travel_time(self, t):
        """
        Get actual travel time of vehicle who enters this link on time t. Note that small error may occur due to fractional processing.

        Parameters
        ----------
        t : float
            Time in seconds.

        Returns
        -------
        float
            The actual travel time.
        """
        tt = int(t // self.W.DELTAT)
        if tt >= len(self.traveltime_actual):
            return self.traveltime_actual[-1]
        if tt < 0:
            return self.traveltime_actual[0]
        return self.traveltime_actual[tt]

    # getter/setter
    @property
    def speed(self):
        if self._speed == -1:
            if len(self.vehicles):
                self._speed = np.average([veh.v for veh in self.vehicles])
            else:
                self._speed = self.u
        return self._speed

    @property
    def density(self):
        if self._density == -1:
            self._density = self.num_vehicles / self.length
        return self._density

    @property
    def flow(self):
        if self._flow == -1:
            self._flow = self.density * self.speed
        return self._flow

    @property
    def num_vehicles(self):
        if self._num_vehicles == -1:
            self._num_vehicles = len(self.vehicles) * self.W.DELTAN
        return self._num_vehicles

    @property
    def num_vehicles_queue(self):
        if self._num_vehicles_queue == -1:
            self._num_vehicles_queue = (
                sum([veh.v < self.u for veh in self.vehicles]) * self.W.DELTAN
            )
        return self._num_vehicles_queue

    @property
    def free_flow_speed(self):
        return self.u

    @free_flow_speed.setter
    def free_flow_speed(self, new_value):
        if new_value >= 0:
            self.u = new_value
            self.w = 1 / self.tau / self.kappa
            self.capacity = self.u * self.w * self.kappa / (self.u + self.w)
            self.delta = 1 / self.kappa
        else:
            warnings.warn(f"ignored negative free_flow_speed at {self}", UserWarning)

    @property
    def jam_density(self):
        return self.kappa

    @jam_density.setter
    def jam_density(self, new_value):
        if new_value >= 0:
            self.kappa = new_value
            self.w = 1 / self.tau / self.kappa
            self.capacity = self.u * self.w * self.kappa / (self.u + self.w)
            self.delta = 1 / self.kappa
        else:
            warnings.warn(f"ignored negative jam_density at {self}", UserWarning)


class Vehicle:
    """
    Vehicle or platoon in a network.
    """

    def __init__(
        self,
        W,
        orig,
        dest,
        departure_time,
        name=None,
        route_pref=None,
        route_choice_principle=None,
        mode="single_trip",
        links_prefer=[],
        links_avoid=[],
        trip_abort=1,
        departure_time_is_time_step=0,
        attribute=None,
        auto_rename=False,
    ):
        """
        Create a vehicle (more precisely, platoon)

        Parameters
        ----------
        W : object
            The world to which the vehicle belongs.
        orig : str | Node
            The origin node.
        dest : str | Node
            The destination node.
        departure_time : int
            The departure time step of the vehicle.
        name : str, optional
            The name of the vehicle, default is the id of the vehicle.
        route_pref : dict, optional
            The preference weights for links, default is 0 for all links.
        route_choice_principle : str, optional
            The route choice principle of the vehicle, default is the network's route choice principle.
        mode : str, optional
            The mode of the vehicle. Available options are "single_trip" and "taxi", default is "single_trip".
            "single_trip": The vehicle makes a single trip from the origin to the destination.
            "taxi": The vehicle serves multiple trips by specifying sequence of destinations. The destination list `Vehicle.dest_list` can be dynamically updated externaly. (TODO: to be implemented next)
        links_prefer : list of str, optional
            The names of the links the vehicle prefers, default is empty list.
        links_avoid : list of str, optional
            The names of the links the vehicle avoids, default is empty list.
        trip_abort : int, optional
            Whether to abort the trip if a dead end is reached, default is 1.
        attribute : any, optinonal
            Additional (meta) attributes defined by users.
        auto_rename : bool, optional
            Whether to automatically rename the vehicle if the name is already used. Default is False.
        """

        self.W = W
        # DepartureDestinationNode
        self.orig = self.W.get_node(orig)
        self.dest = self.W.get_node(dest)

        # DepartureArrivalTime
        if (
            departure_time_is_time_step
        ):  # For compatibility, departure_time is always expressed in timestep notation. -> TODO: needToBeRevised
            self.departure_time = departure_time
        else:
            self.departure_time = int(departure_time / self.W.DELTAT)
        self.arrival_time = -1
        self.link_arrival_time = -1
        self.travel_time = -1

        # state：home, wait, run，end
        self.state = "home"

        # positionInLink
        self.link = None
        self.x = 0
        self.x_next = 0
        self.x_old = 0
        self.v = 0

        # DrivingLane
        self.lane = 0

        # GoFirstAndDriveLast
        self.leader = None
        self.follower = None

        # tripEndPreparationFlag
        self.flag_waiting_for_trip_end = 0

        # treatmentOfRemainingRunAtTheEndOfTheLink
        self.move_remain = 0

        # routeSelection
        if route_choice_principle == None:
            self.route_choice_principle = self.W.route_choice_principle
        else:
            self.route_choice_principle = route_choice_principle

        # private vehicle or taxi
        self.mode = mode
        self.dest_list = []

        # dict of events that are triggered when this vehicle reaches a certain node {Node: func}
        self.node_event = {}

        # DesiredLinkWeightLinkWeight
        self.route_pref = route_pref
        if self.route_pref == None:
            self.route_pref = {l: 0 for l in self.W.LINKS}

        # LinksToLikeAndAvoidMyopic
        self.links_prefer = [self.W.get_link(l) for l in links_prefer]
        self.links_avoid = [self.W.get_link(l) for l in links_avoid]

        # StopTheTripWhenItReachesADeadEnd
        self.trip_abort = trip_abort
        self.flag_trip_aborted = 0

        # LogEtc
        self.log_t = []  # always
        self.log_state = []  # state
        self.log_link = []  # link
        self.log_x = []  # position
        self.log_s = []  # headingDistance
        self.log_v = []  # currentSpeed
        self.log_lane = []  # lane
        self.color = (random.random(), random.random(), random.random())

        self.log_t_link = [
            [int(self.departure_time * self.W.DELTAT), "home"]
        ]  # When entering a new link, only the time and link are saved. For route analysis

        self.attribute = attribute

        self.id = len(self.W.VEHICLES)
        if name != None:
            self.name = name
        else:
            self.name = str(self.id)
        if self.name in [veh.name for veh in self.W.VEHICLES.values()]:
            if auto_rename:
                self.name = (
                    self.name
                    + "_renamed"
                    + "".join(random.choices(string.ascii_letters + string.digits, k=8))
                )
            else:
                raise ValueError(
                    f"Vehicle name {self.name} already used by another vehicle. Please specify a unique name."
                )
        self.W.VEHICLES[self.name] = self
        self.W.VEHICLES_LIVING[self.name] = self

    def __repr__(self):
        return f"<Vehicle {self.name}: {self.state}, x={self.x}, link={self.link}>"

    def update(self):
        """
        Updates the vehicle's state and position.

        Notes
        -----
        This method updates the state and position of the vehicle based on its current situation.

        - If the vehicle is at "home", it checks if the current time matches its departure time. If so, the vehicle's state is set to "wait" and it is added to the generation queue of its origin node.
        - If the vehicle is in the "wait" state, it remains waiting at its departure node.
        - If the vehicle is in the "run" state, it updates its speed and position. If the vehicle reaches the end of its current link, it either ends its trip if it has reached its destination, or requests a transfer to the next link.
        - If the vehicle's state is "end" or "abort", no further actions are taken.
        """
        self.record_log()

        if self.state == "home":
            # depart
            if self.W.T >= self.departure_time:
                self.state = "wait"
                self.orig.generation_queue.append(self)
        if self.state == "wait":
            # wait at the vertical queue at the origin node
            pass
        if self.state == "run":
            # drive within the link
            self.v = (self.x_next - self.x) / self.W.DELTAT
            self.x_old = self.x
            self.x = self.x_next

            # at the end of the link
            if self.x == self.link.length:
                if self.link.end_node in self.node_event.keys():
                    self.node_event[self.link.end_node]()

                if self.link.end_node == self.dest:
                    if self.mode == "single_trip":
                        # prepare for trip end
                        self.flag_waiting_for_trip_end = 1
                        if self.link.vehicles[0] == self:
                            self.end_trip()
                    elif self.mode == "taxi":
                        # proceed to next destination
                        if len(self.dest_list) > 0:
                            self.dest = self.dest_list.pop(0)
                        else:
                            self.dest = None
                            self.dest_list = []
                        self.route_pref_update(weight=1)
                        self.route_next_link_choice()
                        self.link.end_node.inbound_vehicles.append(self)

                elif (
                    len(self.link.end_node.outbound_traffic.values()) == 0
                    and self.trip_abort == 1
                ):
                    # prepare for trip abort due to dead end
                    self.flag_trip_aborted = 1
                    self.route_next_link = None
                    self.flag_waiting_for_trip_end = 1
                    if self.link.vehicles[0] == self:
                        self.end_trip()

                else:
                    # request link transfer
                    self.route_next_link_choice()
                    self.link.end_node.inbound_vehicles.append(self)

        if self.state in ["end", "abort"]:
            # ended the trip
            pass

    def end_trip(self):
        """
        Procedure when the vehicle finishes its trip.
        """
        self.state = "end"

        self.link.cum_departure[-1] += self.W.DELTAN
        self.link.traveltime_actual[int(self.link_arrival_time / self.W.DELTAT) :] = (
            self.W.T + 1
        ) * self.W.DELTAT - self.link_arrival_time  # improvedEdgeBehavior todo: carefulExamination

        if self.follower != None:
            self.follower.leader = None

        self.link.vehicles.popleft()
        self.link = None
        self.x = 0
        self.arrival_time = (
            self.W.T
        )  # TODO: arrival_time IsAlsoExpressedAsATimeStepNeedsCorrection
        self.travel_time = (self.arrival_time - self.departure_time) * self.W.DELTAT
        self.W.VEHICLES_RUNNING.pop(self.name)
        self.W.VEHICLES_LIVING.pop(self.name)

        if self.flag_trip_aborted:
            self.state = "abort"
            self.arrival_time = -1
            self.travel_time = -1

        self.record_log(enforce_log=1)

    def carfollow(self):
        """
        Drive withing a link.
        """
        self.x_next = self.x + self.link.u * self.W.DELTAT
        if self.leader != None:
            x_cong = self.leader.x - self.link.delta_per_lane * self.W.DELTAN
            if x_cong < self.x:
                x_cong = self.x
            if self.x_next > x_cong:
                self.x_next = x_cong

        if self.x_next > self.link.length:
            self.move_remain = self.x_next - self.link.length
            self.x_next = self.link.length

    def route_pref_update(self, weight):
        """
        Updates the vehicle's link preferences for route choice.

        Parameters
        ----------
        weight : float
            The weight for updating the link preferences based on the recent travel time.
            Should be in the range [0, 1], where 0 means the old preferences are fully retained and 1 means the preferences are completely updated.

        Notes
        -----
        This method updates the link preferences used by the vehicle to select its route based on its current understanding of the system.

        - If the vehicle's route choice principle is "homogeneous_DUO", it will update its preferences based on a global, homogenous dynamic user optimization (DUO) model.
        - If the route choice principle is "heterogeneous_DUO", it will update its preferences based on a heterogeneous DUO model, considering both its past preferences and the system's current state. This is imcomplete feature. Not recommended.

        The updated preferences guide the vehicle's decisions in subsequent route choices.
        """
        if self.route_choice_principle == "homogeneous_DUO":
            if self.dest != None:
                self.route_pref = self.W.ROUTECHOICE.route_pref[self.dest.id]
            else:
                self.route_pref = {l: 0 for l in self.W.LINKS}
        elif self.route_choice_principle == "heterogeneous_DUO":
            route_pref_new = {l: 0 for l in self.W.LINKS}
            k = self.dest.id
            for l in self.W.LINKS:
                i = l.start_node.id
                j = l.end_node.id
                if j == self.W.ROUTECHOICE.next[i, k]:
                    route_pref_new[l] = 1

            if sum(list(self.route_pref.values())) == 0:
                # If preference is initially empty, initialize it deterministically
                weight = 1
            for l in self.route_pref.keys():
                self.route_pref[l] = (1 - weight) * self.route_pref[
                    l
                ] + weight * route_pref_new[l]

    def route_next_link_choice(self):
        """
        Select a next link from the current link.
        """
        if self.dest != self.link.end_node:
            outbound_traffic = list(self.link.end_node.outbound_traffic.values())

            if len(outbound_traffic):

                # if links_prefer is given and available at the node, select only from the links in the list. if links_avoid is given, select links not in the list.
                if set(outbound_traffic) & set(self.links_prefer):
                    outbound_traffic = list(
                        set(outbound_traffic) & set(self.links_prefer)
                    )
                if set(outbound_traffic) & set(self.links_avoid):
                    outbound_traffic = list(
                        set(outbound_traffic) - set(self.links_avoid)
                    )

                preference = [self.route_pref[l] for l in outbound_traffic]

                if sum(preference) > 0:
                    self.route_next_link = random.choices(outbound_traffic, preference)[
                        0
                    ]
                else:
                    self.route_next_link = random.choices(outbound_traffic)[0]
            else:
                self.route_next_link = None

    def add_dest(self, dest, order=-1):
        """
        Add a destination to the vehicle's destination list.

        Parameters
        ----------
        dest : str | Node
            The destination node to be added.
        order : int, optional
            The order of the destination in the list. Default is -1, which appends the destination to the end of the list.
        """
        if self.mode == "taxi":
            if self.dest == None:
                self.dest = dest
                self.route_pref_update(weight=1)
            else:
                if order == -1:
                    self.dest_list.append(self.W.get_node(dest))
                else:
                    self.dest_list.insert(order, self.W.get_node(dest))
        else:
            raise ValueError(
                f"Vehicle {self.name} is not in taxi mode. Cannot add destination."
            )

    def set_links_prefer(self, links):
        """
        Set the links the vehicle prefers.

        Parameters
        ----------
        links : list of str
            The list of link names the vehicle prefers.
        """
        self.links_prefer = [self.W.get_link(l) for l in links]

    def set_links_avoid(self, links):
        """
        Set the links the vehicle avoids.

        Parameters
        ----------
        links : list of str
            The list of link names the vehicle avoids.
        """
        self.links_avoid = [self.W.get_link(l) for l in links]

    def add_dests(self, dests):
        """
        Add multiple destinations to the vehicle's destination list.

        Parameters
        ----------
        dests : list of str | Node
            The list of destinations to be added.
        """
        for dest in dests:
            self.add_dest(dest)

    def traveled_route(self):
        """
        Returns the route this vehicle traveled.
        """
        link_old = -1
        t = -1
        route = []
        ts = []
        for i, link in enumerate(self.log_link):
            if link_old != link:
                route.append(link)
                ts.append(self.log_t[i])
                link_old = link

        return Route(self.W, route[:-1]), ts

    def get_xy_coords(self, t=-1):
        """
        Get the x-y coordinates of the vehicle. If t is given, the position at time t is returned based on the logs.

        Parameters
        ----------
        t : int | float, optional
            Time in seconds. If it is -1, the latest position is returned.
        """
        if t != -1:
            link = self.log_link[
                int(t / self.W.DELTAT / self.W.logging_timestep_interval)
            ]
            xx = self.log_x[int(t / self.W.DELTAT / self.W.logging_timestep_interval)]
        else:
            link = self.link
            xx = self.x
        x0 = link.start_node.x
        y0 = link.start_node.y
        x1 = link.end_node.x
        y1 = link.end_node.y
        x = x0 + (x1 - x0) * xx / link.length
        y = y0 + (y1 - y0) * xx / link.length
        return (x, y)

    def record_log(self, enforce_log=0):
        """
        Record travel logs.

        Parameters
        ----------
        enforce_log : bool, optional
            Record log regardless of the logging interval, default is 0.
        """
        if self.W.vehicle_logging_timestep_interval != -1:
            if self.W.T % self.W.vehicle_logging_timestep_interval == 0 or enforce_log:
                if self.state != "run":
                    if self.state == "end" and self.log_t_link[-1][1] != "end":
                        self.log_t_link.append([self.W.T * self.W.DELTAT, "end"])

                    self.log_t.append(self.W.T * self.W.DELTAT)
                    self.log_state.append(self.state)
                    self.log_link.append(-1)
                    self.log_x.append(-1)
                    self.log_s.append(-1)
                    self.log_v.append(-1)
                    self.log_lane.append(-1)

                    if self.state == "wait":
                        self.W.analyzer.average_speed_count += 1
                        self.W.analyzer.average_speed += 0
                else:
                    if len(self.log_link) == 0 or self.log_link[-1] != self.link:
                        self.log_t_link.append([self.W.T * self.W.DELTAT, self.link])

                    self.log_t.append(self.W.T * self.W.DELTAT)
                    self.log_state.append(self.state)
                    self.log_link.append(self.link)
                    self.log_x.append(self.x)
                    self.log_v.append(self.v)
                    self.log_lane.append(self.lane)
                    if self.leader != None and self.link == self.leader.link:
                        self.log_s.append(self.leader.x - self.x)
                    else:
                        self.log_s.append(-1)

                    self.W.analyzer.average_speed_count += 1
                    self.W.analyzer.average_speed += (
                        self.v - self.W.analyzer.average_speed
                    ) / self.W.analyzer.average_speed_count


class RouteChoice:
    """
    Class for computing shortest path for all vehicles.
    """

    def __init__(self, W):
        """
        Create route choice computation object.

        Parameters
        ----------
        W : object
            The world to which this belongs.
        """
        self.W = W
        # LinkTravelTimeMatrix
        self.adj_mat_time = np.zeros([len(self.W.NODES), len(self.W.NODES)])
        # TheShortestDistanceBetweenIj
        self.dist = np.zeros([len(self.W.NODES), len(self.W.NODES)])
        # theNextNodeToGoToToGoFromIToJ
        self.next = np.zeros([len(self.W.NODES), len(self.W.NODES)])
        # theNodeThatCameToGoFromIToJ
        self.pred = np.zeros([len(self.W.NODES), len(self.W.NODES)])

        # homogeneous DUO use_1IfItIsOnTheShortestPathToGoToK
        self.route_pref = {k.id: {l: 0 for l in self.W.LINKS} for k in self.W.NODES}

    def route_search_all(self, infty=np.inf, noise=0):
        """
        Compute the current shortest path based on instantanious travel time.

        Parameters
        ----------
        infty : float
            value representing infinity.
        noise : float
            very small noise to slightly randomize route choice. useful to eliminate strange results at an initial stage of simulation where many routes has identical travel time.
        """
        self.adj_mat_time = np.zeros([len(self.W.NODES), len(self.W.NODES)])
        adj_mat_link_count = np.zeros([len(self.W.NODES), len(self.W.NODES)])

        for link in self.W.LINKS:
            i = link.start_node.id
            j = link.end_node.id
            if self.W.ADJ_MAT[i, j]:
                new_link_tt = (
                    link.traveltime_instant[-1] * random.uniform(1, 1 + noise)
                    + link.route_choice_penalty
                )
                n = adj_mat_link_count[i, j]
                self.adj_mat_time[i, j] = self.adj_mat_time[i, j] * n / (
                    n + 1
                ) + new_link_tt / (
                    n + 1
                )  # if there are multiple links between the same nodes, average the travel time
                # self.adj_mat_time[i,j] = new_link_tt #if there is only one link between the nodes, this line is fine, but for generality we use the above line
                adj_mat_link_count[i, j] += 1
                if (
                    link.capacity_in == 0
                ):  # if the inflow is profibited, travel time is assumed to be infinite
                    self.adj_mat_time[i, j] = np.inf
            else:
                self.adj_mat_time[i, j] = np.inf

        self.dist, self.pred = floyd_warshall(
            self.adj_mat_time, return_predecessors=True
        )

        n_vertices = self.pred.shape[0]
        self.next = -np.ones((n_vertices, n_vertices), dtype=int)
        for i in range(n_vertices):
            for j in range(n_vertices):
                # followTheShortestPathFromIToJInReverse．．． -> todo: You can search for the shortest route by reversing the starting and ending points.
                if i != j:
                    prev = j
                    while self.pred[i, prev] != i and self.pred[i, prev] != -9999:
                        prev = self.pred[i, prev]
                    self.next[i, j] = prev

    def homogeneous_DUO_update(self):
        """
        Update link preference of all homogeneous travelers based on DUO principle.
        """
        for dest in self.W.NODES:
            k = dest.id
            weight = self.W.DUO_UPDATE_WEIGHT
            if sum(list(self.route_pref[k].values())) == 0:
                # AtFirst preference ifIsEmptyInitializeDeterministically
                weight = 1
            for l in self.W.LINKS:
                i = l.start_node.id
                j = l.end_node.id
                if j == self.W.ROUTECHOICE.next[i, k]:
                    self.route_pref[k][l] = (1 - weight) * self.route_pref[k][
                        l
                    ] + weight
                else:
                    self.route_pref[k][l] = (1 - weight) * self.route_pref[k][l]


class World:
    """
    World (i.e., simulation environment). A World object is consistently referred to as `W` in this code.
    """

    def __init__(
        self,
        name="",
        deltan=5,
        reaction_time=1,
        duo_update_time=600,
        duo_update_weight=0.5,
        duo_noise=0.01,
        eular_dt=120,
        eular_dx=100,
        random_seed=None,
        print_mode=1,
        save_mode=1,
        show_mode=0,
        route_choice_principle="homogeneous_DUO",
        show_progress=1,
        show_progress_deltat=600,
        tmax=None,
        vehicle_logging_timestep_interval=1,
    ):
        """
        Create a World.

        Parameters
        ----------
        name : str, optional
            The name of the world, default is an empty string.
        deltan : int, optional
            The platoon size, default is 5 vehicles.
        reaction_time : float, optional
            The reaction time, default is 1 second. This is also related to simulation time step width.
        duo_update_time : float, optional
            The time interval for route choice update, default is 600 seconds.
        duo_update_weight : float, optional
            The update weight for route choice, default is 0.5.
        duo_noise : float, optional
            The noise in route choice, default is 0.01.
        eular_dt : float, optional
            The time aggregation size for eularian traffic state computation, default is 120.
        random_seed : int or None, optional
            The random seed, default is None.
        print_mode : int, optional
            The print mode, whether print the simulation progress or not. Default is 1 (enabled).
        save_mode : int, optional
            The save mode,. whether save the simulation results or not.  Default is 1 (enabled).
        show_mode : int, optional
            The show mode, whether show the matplotlib visualization results or not. Default is 0 (disabled).
        route_choice_principle : str, optional
            The route choice principle, default is "homogeneous_DUO".
        show_progress : int, optional
            Whether show network progress, default is 1 (enabled).
        show_progress_deltat : float, optional
            The time interval for showing network progress, default is 600 seconds.
        tmax : float or None, optional
            The simulation duration, default is None (automatically determined).
        vehicle_logging_timestep_interval : int, optional
            The interval for logging vehicle data, default is 1. Logging is off if set to -1.
            Setting large intervel (2 or more) or turn off the logging makes the simulation significantly faster in large-scale scenarios without loosing simulation internal accuracy, but outputed vehicle trajecotry and other related data will become inaccurate.

        Notes
        -----
        A World object must be defined firstly to initiate simulation.
        """

        # parameterSettings
        random.seed(random_seed)
        np.random.seed(random_seed)
        self.random_seed = random_seed

        # Create a holder attribute for the signal attributes
        self.signal_attributes_low = {}
        self.signal_attributes_high = {}
        self.title = ""

        self.TMAX = tmax  # SimulationTime（s）

        self.DELTAN = deltan  # vehicleFleetSize（veh）
        self.REACTION_TIME = reaction_time  # ReactionTime（s）

        self.DUO_UPDATE_TIME = duo_update_time  # RouteSelectionTimeInterval（s）
        self.DUO_UPDATE_WEIGHT = duo_update_weight  # RouteSelectionUpdateWeight
        self.DUO_NOISE = duo_noise  # NoiseDuringRouteSelection（Preventing extreme routing choices in a fully symmetric network）
        self.EULAR_DT = eular_dt  # Eular DefaultTimeDiscretizationWidthForTypeData

        self.DELTAT = self.REACTION_TIME * self.DELTAN
        self.DELTAT_ROUTE = int(self.DUO_UPDATE_TIME / self.DELTAT)

        # dataStorageDestinationDefinition
        self.VEHICLES = OrderedDict()  # home, wait, run, end
        self.VEHICLES_LIVING = OrderedDict()  # home, wait, run
        self.VEHICLES_RUNNING = OrderedDict()  # run
        self.NODES = []
        self.LINKS = []

        self.vehicle_logging_timestep_interval = vehicle_logging_timestep_interval

        self.route_choice_principle = route_choice_principle

        # realTimeProgressDisplay
        self.show_progress = show_progress
        self.show_progress_deltat_timestep = int(show_progress_deltat / self.DELTAT)

        # systemSetting
        self.name = name

        self.finalized = 0
        self.world_start_time = time.time()

        self.print_mode = print_mode
        if print_mode:
            self.print = print
        else:

            def noprint(*args, **kwargs):
                pass

            self.print = noprint
        self.save_mode = save_mode
        self.show_mode = show_mode

    def addNode(self, *args, **kwargs):
        """
        add a node to world

        Parameters
        ----------
        name : str
            The name of the node.
        x : float
            The x-coordinate of the node (for visualization purposes).
        y : float
            The y-coordinate of the node (for visualization purposes).
        signal : list of int, optional
            A list representing the signal at the node. Default is [0], representing no signal.
            If a signal is present, the list contains the green times for each group.
            For example, `signal`=[60, 10, 50, 5] means that this signal has 4 phases, and green time for the 1st group is 60s.
        signal_offset : float, optional
            The offset of the signal. Default is 0.
        flow_capacity : float, optional
            The maximum flow capacity of the node. Default is None, meaning infinite capacity.
        auto_rename : bool, optional
            Whether to automatically rename the node if the name is already used. Default is False.

        Returns
        -------
        object
            the added Node object.

        Notes
        -----
        This function acts as a wrapper for creating a Node object and adding it to the network.
        It passes all given arguments and keyword arguments to the Node class initialization.
        """
        return Node(self, *args, **kwargs)

    def addLink(self, *args, **kwargs):
        """
        add a link to world

        Parameters
        ----------
        name : str
            The name of the link.
        start_node : str | Node
            The name or object of the start node of the link.
        end_node : str | Node
            The name or object of the end node of the link.
        length : float
            The length of the link.
        free_flow_speed : float
            The free flow speed on the link.
        jam_density : float
            The jam density on the link.
        merge_priority : float, optional
            The priority of the link when merging at the downstream node, default is 1.
        signal_group : int or list, optional
            The signal group to which the link belongs, default is 0. If `signal_group` is int, say 0, it becomes green if `end_node.signal_phase` is 0.  the If `signal_group` is list, say [0,1], it becomes green if the `end_node.signal_phase` is 0 or 1.
        capacity_out : float, optional
            The capacity out of the link, default is calculated based on other parameters.
        capacity_in : float, optional
            The capacity into the link, default is calculated based on other parameters.
        eular_dx : float, optional
            The default space aggregation size for link traffic state computation, default is None. If None, the global eular_dx value is used.
        attribute : any, optinonal
            Additional (meta) attributes defined by users.
        auto_rename : bool, optional
            Whether to automatically rename the link if the name is already used. Default is False.

        Returns
        -------
        object
            the added Link object.

        Notes
        -----
        This function acts as a wrapper for creating a Link object and adding it to the network.
        It passes all given arguments and keyword arguments to the Link class initialization.
        """
        return Link(self, *args, **kwargs)

    def addVehicle(self, *args, **kwargs):
        """
        add a vehicle to world

        Parameters
        ----------
        orig : str | Node
            The origin node.
        dest : str | Node
            The destination node.
        departure_time : int
            The departure time of the vehicle.
        name : str, optional
            The name of the vehicle, default is the id of the vehicle.
        route_pref : dict, optional
            The preference weights for links, default is 0 for all links.
        route_choice_principle : str, optional
            The route choice principle of the vehicle, default is the network's route choice principle.
        links_prefer : list of str, optional
            The names of the links the vehicle prefers, default is empty list.
        links_avoid : list of str, optional
            The names of the links the vehicle avoids, default is empty list.
        trip_abort : int, optional
            Whether to abort the trip if a dead end is reached, default is 1.
        attribute : any, optinonal
            Additional (meta) attributes defined by users.
        auto_rename : bool, optional
            Whether to automatically rename the vehicle if the name is already used. Default is False.

        Returns
        -------
        object
            the added Vehicle object.

        Notes
        -----
        This function acts as a wrapper for creating a Vehicle object and adding it to the network.
        It passes all given arguments and keyword arguments to the Vehicle class initialization.
        """
        return Vehicle(self, *args, **kwargs)

    def adddemand(self, orig, dest, t_start, t_end, flow=-1, volume=-1, attribute=None):
        """
        Generate vehicles by specifying time-dependent origin-destination demand.

        Parameters
        ----------
        orig : str | Node
            The name or object of the origin node.
        dest : str | Node
            The name or object of the destination node.
        t_start : float
            The start time for the demand in seconds.
        t_end : float
            The end time for the demand in seconds.
        flow : float, optional
            The flow rate from the origin to the destination in vehicles per second.
        volume: float, optional
            The demand volume from the origin to the destination. If volume is specified, the flow is ignored.
        attribute : any, optinonal
            Additional (meta) attributes defined by users.
        """
        if volume > 0:
            flow = volume / (t_end - t_start)

        f = 0
        for t in range(int(t_start / self.DELTAT), int(t_end / self.DELTAT)):
            f += flow * self.DELTAT
            while f >= self.DELTAN:
                self.addVehicle(
                    orig, dest, t, departure_time_is_time_step=1, attribute=attribute
                )
                f -= self.DELTAN

    def adddemand_point2point(
        self,
        x_orig,
        y_orig,
        x_dest,
        y_dest,
        t_start,
        t_end,
        flow=-1,
        volume=-1,
        attribute=None,
    ):
        """
        Generate vehicles by specifying time-dependent origin-destination demand using coordinates.

        Parameters
        ----------
        x_orig : float
            The x-coordinate of the origin.
        y_orig : float
            The y-coordinate of the origin.
        x_dest : float
            The x-coordinate of the destination.
        y_dest : float
            The y-coordinate of the destination.
        t_start : float
            The start time for the demand in seconds.
        t_end : float
            The end time for the demand in seconds.
        flow : float, optional
            The flow rate from the origin to the destination in vehicles per second.
        volume: float, optional
            The demand volume from the origin to the destination. If volume is specified, the flow is ignored.
        attribute : any, optinonal
            Additional (meta) attributes defined by users.
        """
        orig = self.get_nearest_node(x_orig, y_orig)
        dest = self.get_nearest_node(x_dest, y_dest)
        self.adddemand(orig, dest, t_start, t_end, flow, volume, attribute)

    def adddemand_area2area(
        self,
        x_orig,
        y_orig,
        radious_orig,
        x_dest,
        y_dest,
        radious_dest,
        t_start,
        t_end,
        flow=-1,
        volume=-1,
        attribute=None,
    ):
        """
        Generate vehicles by specifying time-dependent origin-destination demand by specifying circular areas.

        Parameters
        ----------
        x_orig : float
            The x-coordinate of the center of the origin area.
        y_orig : float
            The y-coordinate of the center of the origin area.
        radious_orig : float
            The radious of the origin area. Note that too large radious may generate too sparse demand that is rounded to zero.
        x_dest : float
            The x-coordinate of the center of the destination area.
        y_dest : float
            The y-coordinate of the center of the destination area.
        radious_dest : float
            The radious of the destination area.
        t_start : float
            The start time for the demand in seconds.
        t_end : float
            The end time for the demand in seconds.
        flow : float, optional
            The flow rate from the origin to the destination in vehicles per second.
        volume: float, optional
            The demand volume from the origin to the destination. If volume is specified, the flow is ignored.
        attribute : any, optinonal
            Additional (meta) attributes defined by users.
        """
        origs = self.get_nodes_in_area(x_orig, y_orig, radious_orig)
        dests = self.get_nodes_in_area(x_dest, y_dest, radious_dest)

        origs_new = []
        dests_new = []
        for o in origs:
            if len(o.outbound_traffic) != 0:
                origs_new.append(o)
        for d in dests:
            if len(d.inbound_traffic) != 0:
                dests_new.append(d)
        origs = origs_new
        dests = dests_new
        if len(origs) == 0:
            origs.append(self.get_nearest_node(x_orig, y_orig))
        if len(dests) == 0:
            dests.append(self.get_nearest_node(x_dest, y_dest))

        if flow != -1:
            flow = flow / (len(origs) * len(dests))
        if volume != -1:
            volume = volume / (len(origs) * len(dests))
        for o in origs:
            for d in dests:
                self.adddemand(o, d, t_start, t_end, flow, volume, attribute)

    def finalize_scenario(self, tmax=None):
        """
        Finalizes the settings and preparations for the simulation scenario execution.

        Parameters
        ----------
        tmax : float, optional
            The maximum simulation time. If not provided, it will be determined based on the departure times of the vehicles.

        Notes
        -----
        This function automatically called by `exec_simulation()` if it has not been called manually.
        """
        if self.TMAX == None:
            if tmax == None:
                tmax = 0
                for veh in self.VEHICLES.values():
                    if veh.departure_time * self.DELTAT > tmax:
                        tmax = veh.departure_time * self.DELTAT
                self.TMAX = (tmax // 1800 + 2) * 1800
            else:
                self.TMAX = tmax  # s

        self.T = 0  # timestep
        self.TIME = 0  # s

        self.TSIZE = int(self.TMAX / self.DELTAT)
        self.Q_AREA = ddict(lambda: np.zeros(int(self.TMAX / self.EULAR_DT)))
        self.K_AREA = ddict(lambda: np.zeros(int(self.TMAX / self.EULAR_DT)))
        for l in self.LINKS:
            l.init_after_tmax_fix()

        # GeneratingAdjacencyMatrix
        self.ROUTECHOICE = RouteChoice(self)
        self.ADJ_MAT = np.zeros([len(self.NODES), len(self.NODES)])
        self.ADJ_MAT_LINKS = {}  # Adjacency matrix (dictionary) containing link objects
        for link in self.LINKS:
            for i, node in enumerate(self.NODES):
                if node == link.start_node:
                    break
            for j, node in enumerate(self.NODES):
                if node == link.end_node:
                    break
            self.ADJ_MAT[i, j] = 1
            self.ADJ_MAT_LINKS[i, j] = link

        self.analyzer = Analyzer(self)

        self.finalized = 1

        # problemSizeRepresentation
        self.print("simulation setting:")
        self.print(" scenario name:", self.name)
        self.print(" simulation duration:\t", self.TMAX, "s")
        self.print(" number of vehicles:\t", len(self.VEHICLES) * self.DELTAN, "veh")
        self.print(" total road length:\t", sum([l.length for l in self.LINKS]), "m")
        self.print(" time discret. width:\t", self.DELTAT, "s")
        self.print(" platoon size:\t\t", self.DELTAN, "veh")
        self.print(" number of timesteps:\t", self.TSIZE)
        self.print(" number of platoons:\t", len(self.VEHICLES))
        self.print(" number of links:\t", len(self.LINKS))
        self.print(" number of nodes:\t", len(self.NODES))
        self.print(
            " setup time:\t\t", f"{time.time() - self.world_start_time:.2f}", "s"
        )

        self.sim_start_time = time.time()
        self.print("simulating...")

    def exec_simulation(self, until_t=None, duration_t=None):
        """
        Execute the main loop of the simulation.

        Parameters
        ----------
        until_t : float or None, optional
            The time until the simulation is to be executed in seconds. If both `until_t` and `duration_t` are None, the simulation is executed until the end. Default is None.
        duration_t : float or None, optional
            The duration for which the simulation is to be executed in seconds. If both `until_t` and `duration_t` are None, the simulation is executed until the end. Default is None.

        Returns
        -------
        int
            Returns 1 if the simulation is finished, 0 otherwise.

        Notes
        -----
        The function executes the main simulation loop that update links, nodes, and vehicles for each time step.
        It also performs route search and updates the route preference for vehicles at specified intervals.
        The simulation is executed until the end time is reached or until the maximum simulation time is exceeded.
        The nodes, links, and vehicles must be defined before calling this function.
        """

        # RunTheMainLoopOfTheSimulation

        # IfTheScenarioIsUndecidedConfirmItHere
        if self.finalized == 0:
            self.finalize_scenario()

        # TimeDetermination
        start_ts = self.T
        if until_t != None:
            end_ts = int(until_t / self.DELTAT)
        elif duration_t != None:
            end_ts = start_ts + int(duration_t / self.DELTAT)
        else:
            end_ts = self.TSIZE
        if end_ts > self.TSIZE:
            end_ts = self.TSIZE

        # W.print(f"simulating: from t = {start_ts*W.DELTAT} to {(end_ts-1)*W.DELTAT}s...")

        if start_ts == end_ts == self.TSIZE:
            if self.print_mode and self.show_progress:
                self.analyzer.show_simulation_progress()
            self.simulation_terminated()
            return 1  # EndOfSimulation
        if end_ts < start_ts:
            raise Exception(
                "exec_simulation error: Simulation duration is negative. Check until_t or duration_t"
            )

        # MainLoop
        for self.T in range(start_ts, end_ts):
            if self.T == 0:
                self.print(
                    "      time| # of vehicles| ave speed| computation time", flush=True
                )
                self.analyzer.show_simulation_progress()

            for link in self.LINKS:
                link.update()

            for node in self.NODES:
                node.generate()

            for node in self.NODES:
                node.transfer()

            for veh in self.VEHICLES_RUNNING.values():
                veh.carfollow()

            for name in list(self.VEHICLES_LIVING.keys()):
                self.VEHICLES_LIVING[name].update()

            if self.T % self.DELTAT_ROUTE == 0:
                self.ROUTECHOICE.route_search_all(noise=self.DUO_NOISE)
                self.ROUTECHOICE.homogeneous_DUO_update()
                for veh in self.VEHICLES_LIVING.values():
                    veh.route_pref_update(weight=self.DUO_UPDATE_WEIGHT)

            self.TIME = self.T * self.DELTAT

            if (
                self.print_mode
                and self.show_progress
                and self.T % self.show_progress_deltat_timestep == 0
                and self.T > 0
            ):
                self.analyzer.show_simulation_progress()

        if self.T == self.TSIZE - 1:
            if self.print_mode and self.show_progress:
                self.analyzer.show_simulation_progress()
            self.simulation_terminated()
            return 1

        self.T += 1
        return 0  # ItSNotOverYet

    def check_simulation_ongoing(self):
        """
        Check whether the simulation is has not reached its final time.

        Returns
        -------
        int
            Returns 1 if the simulation is ongoing and has not reached its final time.
        """
        # DetermineIfSimulationIsInProgress
        if self.finalized == 0:
            return 1
        return self.T < self.TSIZE - 1

    def simulation_terminated(self):
        """
        Postprocessing after simulation finished
        """
        self.print(" simulation finished")
        self.analyzer.basic_analysis()

    def get_node(self, node):
        """Get a Node instance by name or object.

        Parameters
        ----------
        node : str or Node object
            The name of the node or the Node object itself.

        Returns
        -------
        Node object
            The found Node object.
        """
        if node == None:
            return None

        if type(node) is Node:
            if node in self.NODES:
                return node
            else:
                for n in self.NODES:
                    if n.name == node.name:
                        return n
        elif type(node) is str:
            for n in self.NODES:
                if n.name == node:
                    return n
        raise Exception(f"'{node}' is not Node in this World")

    def get_link(self, link):
        """
        Get a Link instance by name or object.

        Parameters
        ----------
        link : str or Link object
            The name of the link or the Link object itself.

        Returns
        -------
        Link object
            The found Link object.
        """
        if link == None:
            return None

        if type(link) is Link:
            if link in self.LINKS:
                return link
            else:
                for l in self.LINKS:
                    if l.name == link.name:
                        return l
        elif type(link) is str:
            for l in self.LINKS:
                if l.name == link:
                    return l
        raise Exception(f"'{link}' is not Link in this World")

    def get_nearest_node(self, x, y):
        """
        Get the nearest node to the given coordinates.

        Parameters
        ----------
        x : float
            The x-coordinate.
        y : float
            The y-coordinate.

        Returns
        -------
        object
            The nearest Node object.
        """
        min_dist = 1e10
        nearest_node = None
        for node in self.NODES:
            dist = (node.x - x) ** 2 + (node.y - y) ** 2
            if dist < min_dist:
                min_dist = dist
                nearest_node = node
        return nearest_node

    def get_nodes_in_area(self, x, y, r):
        """
        Get the nodes in the area defined by the center coordinates and radius.
        Parameters
        ----------
        x : float
            The x-coordinate of the center.
        y : float
            The y-coordinate of the center.
        r : float
            The radius of the area.

        Returns
        -------
        list
            A list of Node objects in the area.
        """
        nodes = []
        for node in self.NODES:
            if (node.x - x) ** 2 + (node.y - y) ** 2 < r**2:
                nodes.append(node)
        return nodes

    def load_scenario_from_csv(self, fname_node, fname_link, fname_demand, tmax=None):
        """
        Load a scenario from CSV files.

        Parameters
        ----------
        fname_node : str
            The file name of the CSV file containing node data.
        fname_link : str
            The file name of the CSV file containing link data.
        fname_demand : str
            The file name of the CSV file containing demand data.
        tmax : float or None, optional
            The maximum simulation time in seconds, default is None.
        """
        self.generate_Nodes_from_csv(fname_node)
        self.generate_Links_from_csv(fname_link)
        self.generate_demand_from_csv(fname_demand)

        if tmax != None:
            self.TMAX = tmax

    def generate_Nodes_from_csv(self, fname):
        """
        Generate nodes in the network from a CSV file.

        Parameters
        ----------
        fname : str
            The file name of the CSV file containing node data.
        """

        with open(fname) as f:
            for r in csv.reader(f):
                if r[1] != "x":
                    self.addNode(r[0], float(r[1]), float(r[2]))

    def generate_Links_from_csv(self, fname):
        """
        Generate links in the network from a CSV file.

        Parameters
        ----------
        fname : str
            The file name of the CSV file containing link data.
        """

        with open(fname) as f:
            for r in csv.reader(f):
                if r[3] != "length":
                    self.addLink(
                        r[0],
                        r[1],
                        r[2],
                        length=float(r[3]),
                        free_flow_speed=float(r[4]),
                        jam_density=float(r[5]),
                        merge_priority=float(r[6]),
                    )

    def generate_demand_from_csv(self, fname):
        """
        Generate demand in the network from a CSV file.

        Parameters
        ----------
        fname : str
            The file name of the CSV file containing demand data.
        """
        with open(fname) as f:
            for r in csv.reader(f):
                if r[2] != "start_t":
                    try:
                        self.adddemand(
                            r[0],
                            r[1],
                            float(r[2]),
                            float(r[3]),
                            float(r[4]),
                            float(r[5]),
                        )
                    except:
                        self.adddemand(
                            r[0], r[1], float(r[2]), float(r[3]), float(r[4])
                        )

    def on_time(self, time):
        """
        Check if the current time step is close to the specified time.

        Parameters
        ----------
        time : float
            The specified time in seconds.

        Returns
        -------
        bool
            Returns True if the current time step is close to the specified time, False otherwise.
        """
        if self.T == int(time / self.DELTAT):
            return True
        else:
            return False

    @catch_exceptions_and_warn()
    def show_network(
        self,
        width=1,
        left_handed=1,
        figsize=(6, 6),
        network_font_size=10,
        node_size=6,
        show_switches=False,
        show_links=False,
    ):
        """
        Visualizes the entire transportation network shape.
        """
        signal_symbols = []

        for signal in self.signal_attributes_low:
            # Mainline Green/Green Case
            if (
                self.signal_attributes_low[signal][2] != "yard"
                and self.signal_attributes_low[signal][0] == "green"
                and self.signal_attributes_low[signal][2] == "green"
            ):
                signal_icon = np.rot90(
                    plt.imread(
                        f"./railroad icons/{self.signal_attributes_low[signal][0]}_circle_{self.signal_attributes_low[signal][2]}_square.png"
                    )
                )

            # Mainline Green/Red Case
            elif (
                self.signal_attributes_low[signal][2] != "yard"
                and self.signal_attributes_low[signal][0] == "green"
                and self.signal_attributes_low[signal][2] == "red"
            ):
                signal_icon = np.rot90(
                    plt.imread(f"./railroad icons/red_circle_yellow_square.png")
                )

            # Mainline Red/Green Case
            elif (
                self.signal_attributes_low[signal][2] != "yard"
                and self.signal_attributes_low[signal][0] == "red"
                and self.signal_attributes_low[signal][2] == "green"
            ):
                signal_icon = np.rot90(
                    plt.imread(f"./railroad icons/red_circle_red_square.png")
                )

            # Mainline Red/Red Case
            elif (
                self.signal_attributes_low[signal][2] != "yard"
                and self.signal_attributes_low[signal][0] == "red"
                and self.signal_attributes_low[signal][2] == "red"
            ):
                signal_icon = np.rot90(
                    plt.imread(
                        f"./railroad icons/{self.signal_attributes_low[signal][0]}_circle_{self.signal_attributes_low[signal][2]}_square.png"
                    )
                )

            # Yard Case - Green
            elif (
                self.signal_attributes_low[signal][2] == "yard"
                and self.signal_attributes_low[signal][0] == "green"
            ):
                signal_icon = np.rot90(
                    plt.imread(
                        f"./railroad icons/{self.signal_attributes_low[signal][0]}_circle.png"
                    )
                )

            # Yard Case - Red
            elif (
                self.signal_attributes_low[signal][2] == "yard"
                and self.signal_attributes_low[signal][0] == "red"
            ):
                signal_icon = np.rot90(
                    plt.imread(
                        f"./railroad icons/{self.signal_attributes_low[signal][0]}_circle.png"
                    )
                )

            # Unexpected Case
            else:
                print(signal)

            im = OffsetImage(signal_icon, zoom=0.5)
            ab = AnnotationBbox(
                im,
                self.signal_attributes_low[signal][1],
                boxcoords="offset points",
                bboxprops=dict(visible=False),
            )
            signal_symbols.append(ab)

        for signal in self.signal_attributes_high:
            # Mainline Green/Green Case
            if (
                self.signal_attributes_high[signal][2] != "yard"
                and self.signal_attributes_high[signal][0] == "green"
                and self.signal_attributes_high[signal][2] == "green"
            ):
                signal_icon = np.rot90(
                    plt.imread(
                        f"./railroad icons/{self.signal_attributes_high[signal][0]}_circle_{self.signal_attributes_high[signal][2]}_square.png"
                    ),
                    3,
                )

            # Mainline Green/Red Case
            elif (
                self.signal_attributes_high[signal][2] != "yard"
                and self.signal_attributes_high[signal][0] == "green"
                and self.signal_attributes_high[signal][2] == "red"
            ):
                signal_icon = np.rot90(
                    plt.imread(f"./railroad icons/red_circle_yellow_square.png"), 3
                )

            # Mainline Red/Green Case
            elif (
                self.signal_attributes_high[signal][2] != "yard"
                and self.signal_attributes_high[signal][0] == "red"
                and self.signal_attributes_high[signal][2] == "green"
            ):
                signal_icon = np.rot90(
                    plt.imread(f"./railroad icons/red_circle_red_square.png"), 3
                )

            # Mainline Red/Red Case
            elif (
                self.signal_attributes_high[signal][2] != "yard"
                and self.signal_attributes_high[signal][0] == "red"
                and self.signal_attributes_high[signal][2] == "red"
            ):
                signal_icon = np.rot90(
                    plt.imread(
                        f"./railroad icons/{self.signal_attributes_high[signal][0]}_circle_{self.signal_attributes_high[signal][2]}_square.png"
                    ),
                    3,
                )

            # Yard Case - Green
            elif (
                self.signal_attributes_high[signal][2] == "yard"
                and self.signal_attributes_high[signal][0] == "green"
            ):
                signal_icon = np.rot90(
                    plt.imread(
                        f"./railroad icons/{self.signal_attributes_high[signal][0]}_circle.png"
                    ),
                    3,
                )

            # Yard Case - Red
            elif (
                self.signal_attributes_high[signal][2] == "yard"
                and self.signal_attributes_high[signal][0] == "red"
            ):
                signal_icon = np.rot90(
                    plt.imread(
                        f"./railroad icons/{self.signal_attributes_high[signal][0]}_circle.png"
                    ),
                    3,
                )

            # Unexpected Case
            else:
                print(signal)

            im = OffsetImage(signal_icon, zoom=0.5)
            ab = AnnotationBbox(
                im,
                self.signal_attributes_high[signal][1],
                boxcoords="offset points",
                bboxprops=dict(visible=False),
            )
            signal_symbols.append(ab)

        f = plt.figure(figsize=figsize)
        plt.subplot(111, aspect="equal")

        ax = plt.gca()

        if signal_symbols:
            for signal in signal_symbols:
                ax.add_artist(signal)

        for n in self.NODES:
            plt.plot(
                n.x, n.y, "o", color=n.color, ms=13, zorder=30, solid_capstyle="round"
            )  # ms
            if network_font_size > 0:
                if show_switches:
                    plt.text(
                        n.x - n.hoffset,
                        n.y - n.voffset,
                        n.name,
                        c="White",
                        horizontalalignment="center",
                        verticalalignment="center",
                        zorder=30,
                        fontsize=15,
                    )  # c, fontsize
                else:
                    plt.text(
                        n.x - n.hoffset,
                        n.y - n.voffset,
                        n.name,
                        c=n.label_color,
                        horizontalalignment="center",
                        verticalalignment="center",
                        zorder=3,
                        fontsize=15,
                    )  # c, fontsize
        for l in self.LINKS:
            x1, y1 = l.start_node.x, l.start_node.y
            x2, y2 = l.end_node.x, l.end_node.y
            # simpleMode
            xmid1, ymid1 = (x1 + x2) / 2, (y1 + y2) / 2
            if show_links:
                plt.plot(
                    [x1, x2],
                    [y1, y2],
                    color=l.color,
                    lw=14,
                    zorder=7,
                    solid_capstyle="round",
                )  # ms
                plt.text(
                    xmid1,
                    ymid1,
                    l.name,
                    c="white",
                    horizontalalignment="right",
                    verticalalignment="top",
                    zorder=30,
                    fontsize=15,
                )

            else:
                plt.plot(
                    [x1, x2],
                    [y1, y2],
                    color=l.color,
                    lw=14,
                    zorder=7,
                    solid_capstyle="round",
                )  # ms

        maxx = max([n.x for n in self.NODES])
        minx = min([n.x for n in self.NODES])
        maxy = max([n.y for n in self.NODES]) + 2
        miny = min([n.y for n in self.NODES])
        buffx, buffy = (maxx - minx) / 10, (maxy - miny) / 10

        if buffx == 0:
            buffx = buffy
        if buffy == 0:
            buffy = buffx

        # Assign the current plot axes to ax to start adding in signals
        plt.style.use("dark_background")

        ax.spines["bottom"].set_color("black")
        ax.spines["top"].set_color("black")
        ax.spines["right"].set_color("black")
        ax.spines["left"].set_color("black")

        ax.tick_params(which="both", colors="black")

        font1 = {"family": "serif", "color": "Yellow", "size": 40}
        ax.set_title(self.title, fontdict=font1, pad=40)
        ax.set_facecolor("black")

        # Vertical lines for the start and end of interlocking
        plt.vlines(
            x=2,
            ymin=0,
            ymax=14.5,
            color="black",
            label="AF-Start",
            linewidth=15,
            zorder=9,
        )
        plt.vlines(
            x=27,
            ymin=0,
            ymax=14.5,
            color="black",
            label="AF-End",
            linewidth=15,
            zorder=9,
        )

        # Establish the limits of the plot
        plt.xlim([minx - buffx, maxx + buffx])
        plt.ylim([0, maxy + buffy])  # miny - buffy
        plt.tight_layout()

        return f

    def copy(self):
        """
        Copy the World object.

        Returns
        -------
        World object
            The copied World object.
        """
        return pickle.loads(pickle.dumps(self))


class Route:
    """
    Class for a route that store concective links.
    """

    def __init__(self, W, links, name="", trust_input=False):
        """
        Define a route.

        Attributes
        ----------
        links : list
            List of links. The contents are Link objects.
        links_name : list
            List of name of links. The contents are str.
        trust_input : bool
            True if you trust the `links` in order to reduce the computation cost by omitting verification.

        Examples
        --------
        >>> route = Route(W, ["l1", "l2", "l3"])
        ... vehicle_object.links_prefer = route
        This will enforce the vehicle to travel the route if the route covers the entire links between the OD nodes of the vehicle.

        >>> route = Route(W, ["l1", "l2", "l3"])
        ... for link in route:
        ...     print(link)
        This will print the links in the route.
        """
        self.W = W
        self.name = name
        self.links = []
        if trust_input == False:
            # whenInspectingInputData
            for i in range(0, len(links) - 1):
                l1 = W.get_link(links[i])
                l2 = W.get_link(links[i + 1])
                if l2 in l1.end_node.outbound_traffic.values():
                    self.links.append(l1)
                else:
                    raise Exception(
                        f"route is not defined by concective links: {links}, {l1}"
                    )
                    # todo: interpolation based on shotest path
            self.links.append(l2)
        else:
            # Use as is without inspection (reducing calculation costs)
            self.links = links
        self.links_name = [l.name for l in self.links]

    def __repr__(self):
        return f"<Route {self.name}: {self.links}>"

    def __iter__(self):
        """
        Override `iter()` function. Iterate the links of the route.
        """
        return iter(self.links)

    def __len__(self):
        return len(self.links)

    def __eq__(self, other):
        """
        Override `==` operator. If the links of two route are the same, then the routes are the same.
        """
        if isinstance(other, Route):
            return self.links == other.links
        return NotImplemented

    def actual_travel_time(self, t, return_details=False):
        """
        Actual travel time for a (hypothetical) vehicle who start traveling this route on time t.

        Parameters
        ----------
        t : float
            Time in seconds.
        return_details : bool
            True if you want travel time per link.

        Returns
        -------
        float
            The actual travel time.
        list (if `return_details` is True)
            List of travel time per link.
        """
        tt = 0
        tts = []

        for l in self.links:
            link_tt = l.actual_travel_time(t)
            tt += link_tt
            t += link_tt
            tts.append(link_tt)

        if return_details:
            return tt, tts
        else:
            return tt
