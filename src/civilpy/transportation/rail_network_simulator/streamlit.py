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

import streamlit as st

from src.rail_network_simulator.rail_simulator import *

# Use the full page instead of a narrow central column
st.set_page_config(layout="wide")

st.markdown(
    "<h1 style='text-align: center; color: teal;'>AF-RO Outage Visualizer</h1>",
    unsafe_allow_html=True,
)

st.markdown(
    "<h1 style='text-align: center; color: green;'>Construction Phases</h1>",
    unsafe_allow_html=True,
)

phase1, phase2, phase3, phase4 = st.columns(4)

with phase1:
    phase1.header("Phase 1")
    phase_1_opt_1 = st.checkbox("Option 1", key="const_phase_1_opt_1")

with phase2:
    phase2.header("Phase 2")
    phase_2_opt_1 = st.checkbox("Option 1", key="const_phase_2_opt_1")

with phase3:
    phase3.header("Phase 3")
    phase_3_opt_1 = st.checkbox("Option 1", key="const_phase_3_opt_1")

with phase4:
    phase4.header("Phase 4")
    phase_4_opt_1 = st.checkbox("Option 1", key="const_phase_4_opt_1")


# Outage Selection Overrides
st.markdown(
    "<h1 style='text-align: center; color: green;'>Outage Selection Override</h1>",
    unsafe_allow_html=True,
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    col1.header("After RO")
    Main2AfterRO = st.checkbox("Main 2 Outage", key="After_RO_main2_disabled")
    Main3AfterRO = st.checkbox("Main 3 Outage", key="After_RO_main3_disabled")

with col2:
    col2.header("RO-Slaters Lane")
    SlatersROMain0Closed = st.checkbox("Main 0 Outage", key="Slaters_RO_main0_disabled")
    SlatersROMain1Closed = st.checkbox("Main 1 Outage", key="Slaters_RO_main1_disabled")
    SlatersROMain2Closed = st.checkbox("Main 2 Outage", key="Slaters_RO_main2_disabled")
    SlatersROMain3Closed = st.checkbox("Main 3 Outage", key="Slaters_RO_main3_disabled")

with col3:
    col3.header("Slaters Lane-AF")
    AFSlatersMain0Closed = st.checkbox("Main 0 Outage", key="AF_Slaters_main0_disabled")
    AFSlatersMain1Closed = st.checkbox("Main 1 Outage", key="AF_Slaters_main1_disabled")
    AFSlatersMain2Closed = st.checkbox("Main 2 Outage", key="AF_Slaters_main2_disabled")
    AFSlatersMain3Closed = st.checkbox("Main 3 Outage", key="AF_Slaters_main3_disabled")

with col4:
    col4.header("Before AF")
    option1 = st.checkbox("Yard 1 Outage", key="pre_AF_yard1_disabled")
    option2 = st.checkbox("Yard 2 Outage", key="pre_AF_yard2_disabled")
    option3 = st.checkbox("Yard 3 Outage", key="pre_AF_yard3_disabled")
    option4 = st.checkbox("Main 3 Outage", key="pre_AF_main3_disabled")
    option5 = st.checkbox("Main 2 Outage", key="pre_AF_main2_disabled")
    option6 = st.checkbox("Main 1 Outage", key="pre_AF_main1_disabled")
    option7 = st.checkbox("NS Outage", key="pre_AF_ns_disabled")


# =====================================          RO        ========================================================

# Create the World Object
RO = World(
    name="RO",
    deltan=1,
    tmax=1000,
    print_mode=1,
    save_mode=0,
    show_mode=1,
    random_seed=0,
)

# Define Southern (Low MP) Origins
RO.addNode("Main 0", 30, 8, label_color="white", voffset=0.4)  # 0
RO.addNode("Main 1", 30, 6, label_color="white", voffset=0.4)  # 1
RO.addNode("Main 2", 30, 4, label_color="white", voffset=0.4)  # 2
RO.addNode("Main 3", 30, 2, label_color="white", voffset=0.4)  # 3

# Define Northern (High MP) Origins
RO.addNode("Existing 2", 0, 8, label_color="white", voffset=0.4)  # 4
RO.addNode("Existing 3", 0, 6, label_color="white", voffset=0.4)  # 5
RO.addNode("Proposed_2_org", 6, 4)  # 6
RO.addNode("Proposed_3_org", 10, 2)  # 7

# Define Switch Points
RO.addNode("1_S", 10, 8)  # 8
RO.addNode("3_S", 12, 6)  # 9
RO.addNode("5_S", 16, 6)  # 10
RO.addNode("7_S", 18, 8)  # 11
RO.addNode("9_S", 4, 6)  # 12
RO.addNode("11_S", 20, 6)  # 13
RO.addNode("13_S", 22, 4)  # 14
RO.addNode("15_S", 8, 4)  # 15

# Define Links
RO.addLink("Ex 2", "Existing 2", "1_S", length=20)  # 0
RO.addLink("0_1", "1_S", "7_S", length=20)  # 1
RO.addLink("Main 0", "7_S", "Main 0", length=20)  # 2
RO.addLink("Ex 3", "Existing 3", "9_S", length=20)  # 3
RO.addLink("1_1", "9_S", "3_S", length=20)  # 4
RO.addLink("1_2", "3_S", "5_S", length=20)  # 5
RO.addLink("1_3", "5_S", "11_S", length=20)  # 6
RO.addLink("Main 1", "11_S", "Main 1", length=20)  # 7
RO.addLink("9_S", "9_S", "Proposed_2_org", length=20)  # 8
RO.addLink("2_1", "Proposed_2_org", "15_S", length=20)  # 9
RO.addLink("2_2", "15_S", "13_S", length=20)  # 10
RO.addLink("Main 2", "13_S", "Main 2", length=20)  # 11
RO.addLink("15_S", "15_S", "Proposed_3_org", length=20)  # 12
RO.addLink("Main 3", "Proposed_3_org", "Main 3", length=20)  # 13

# Define X-Overs
RO.addLink("1-3", "1_S", "3_S", length=20)  # 14
RO.addLink("5-7", "5_S", "7_S", length=20)  # 15
RO.addLink("11-13", "11_S", "13_S", length=20)  # 16


if Main2AfterRO & Main3AfterRO:
    for link in RO.LINKS:
        link.color = "red"
    for node in RO.NODES:
        node.color = "red"

if Main2AfterRO:
    RO.LINKS[0].color = "red"  # Existing 2
    RO.LINKS[1].color = "red"  # 0_1
    RO.LINKS[14].color = "red"  # 1-3

    RO.NODES[4].color = "red"  # Existing 2
    RO.NODES[8].color = "red"  # 1_S

elif Main3AfterRO:
    RO.LINKS[3].color = "red"  # Ex 3
    RO.LINKS[4].color = "red"  # 1_1
    RO.LINKS[8].color = "red"  # 9_S
    RO.LINKS[9].color = "red"  # 2_1
    RO.LINKS[10].color = "red"  # 2_2
    RO.LINKS[12].color = "red"  # 15_S
    RO.LINKS[13].color = "red"  # Main 3

    RO.NODES[5].color = "red"  # Existing 3
    RO.NODES[6].color = "red"  # Proposed_2_org
    RO.NODES[7].color = "red"  # Proposed_3_org
    RO.NODES[12].color = "red"  # 9_S
    RO.NODES[15].color = "red"  # 15_S

# Update the graph depending on what routes are closed
# 1 combination with all 4 tracks closed
if (
    SlatersROMain3Closed
    and SlatersROMain2Closed
    and SlatersROMain1Closed
    and SlatersROMain0Closed
):
    for link in RO.LINKS:
        link.color = "red"
    for node in RO.NODES:
        node.color = "red"

# 4 combos of 3 tracks closed
elif SlatersROMain0Closed and SlatersROMain1Closed and SlatersROMain2Closed:
    RO.LINKS[0].color = "red"  # Ex 2
    RO.LINKS[1].color = "red"  # 0_1
    RO.LINKS[2].color = "red"  # Main 0
    RO.LINKS[4].color = "red"  # 1_1
    RO.LINKS[5].color = "red"  # 1_2
    RO.LINKS[6].color = "red"  # 1_3
    RO.LINKS[7].color = "red"  # Main 1
    RO.LINKS[10].color = "red"  # 2_2
    RO.LINKS[11].color = "red"  # Main 2
    RO.LINKS[14].color = "red"  # 1-3
    RO.LINKS[15].color = "red"  # 5-7
    RO.LINKS[16].color = "red"  # 11-13

    RO.NODES[0].color = "red"  # Main 0
    RO.NODES[1].color = "red"  # Main 1
    RO.NODES[2].color = "red"  # Main 2
    RO.NODES[4].color = "red"  # Exisiting 2
    RO.NODES[8].color = "red"  # 1_S
    RO.NODES[9].color = "red"  # 3_S
    RO.NODES[10].color = "red"  # 5_S
    RO.NODES[11].color = "red"  # 7_S
    RO.NODES[13].color = "red"  # 11_S
    RO.NODES[14].color = "red"  # 13_S

elif SlatersROMain0Closed and SlatersROMain1Closed and SlatersROMain3Closed:
    RO.LINKS[1].color = "red"  # 0_1
    RO.LINKS[2].color = "red"  # Main 0
    RO.LINKS[7].color = "red"  # Main 1
    RO.LINKS[12].color = "red"  # 15_S
    RO.LINKS[13].color = "red"  # Main 3
    RO.LINKS[15].color = "red"  # 5-7

    RO.NODES[0].color = "red"  # Main 0
    RO.NODES[1].color = "red"  # Main 1
    RO.NODES[3].color = "red"  # Main 3
    RO.NODES[7].color = "red"  # Proposed_3_org
    RO.NODES[11].color = "red"  # 7_S

elif SlatersROMain0Closed and SlatersROMain2Closed and SlatersROMain3Closed:
    RO.LINKS[1].color = "red"  # 0_1
    RO.LINKS[2].color = "red"  # Main 0
    RO.LINKS[8].color = "red"  # 9_S
    RO.LINKS[9].color = "red"  # 2_1
    RO.LINKS[10].color = "red"  # 2_2
    RO.LINKS[11].color = "red"  # Main 2
    RO.LINKS[12].color = "red"  # 15_S
    RO.LINKS[13].color = "red"  # Main 3
    RO.LINKS[15].color = "red"  # 5-7
    RO.LINKS[16].color = "red"  # 11-13

    RO.NODES[0].color = "red"  # Main 0
    RO.NODES[2].color = "red"  # Main 2
    RO.NODES[3].color = "red"  # Main 3
    RO.NODES[6].color = "red"  # Proposed_2_org
    RO.NODES[7].color = "red"  # Proposed_3_org
    RO.NODES[11].color = "red"  # 7_S
    RO.NODES[14].color = "red"  # 13_S
    RO.NODES[15].color = "red"  # 15_S

elif SlatersROMain1Closed and SlatersROMain2Closed and SlatersROMain3Closed:
    RO.LINKS[6].color = "red"  # 1_3
    RO.LINKS[7].color = "red"  # Main 1
    RO.LINKS[8].color = "red"  # 9_S
    RO.LINKS[9].color = "red"  # 2_1
    RO.LINKS[10].color = "red"  # 2_2
    RO.LINKS[11].color = "red"  # Main 2
    RO.LINKS[12].color = "red"  # 15_S
    RO.LINKS[13].color = "red"  # Main 3
    RO.LINKS[14].color = "red"  # 1-3
    RO.LINKS[16].color = "red"  # 11-13

    RO.NODES[1].color = "red"  # Main 1
    RO.NODES[2].color = "red"  # Main 2
    RO.NODES[3].color = "red"  # Main 3
    RO.NODES[6].color = "red"  # Proposed_2_org
    RO.NODES[7].color = "red"  # Proposed_3_org
    RO.NODES[13].color = "red"  # 11_S
    RO.NODES[14].color = "red"  # 13_S
    RO.NODES[15].color = "red"  # 15_S

# 6 combos of 2 tracks closed
elif SlatersROMain0Closed and SlatersROMain1Closed:
    RO.LINKS[1].color = "red"  # 0_1
    RO.LINKS[2].color = "red"  # Main 0
    RO.LINKS[7].color = "red"  # Main 1
    RO.LINKS[15].color = "red"  # 5-7

    RO.NODES[0].color = "red"  # Main 0
    RO.NODES[1].color = "red"  # Main 1
    RO.NODES[11].color = "red"  # 7_S

elif SlatersROMain0Closed and SlatersROMain2Closed:
    RO.LINKS[1].color = "red"  # 0_1
    RO.LINKS[2].color = "red"  # Main 0
    RO.LINKS[10].color = "red"  # 2_2
    RO.LINKS[11].color = "red"  # Main 2
    RO.LINKS[15].color = "red"  # 5-7
    RO.LINKS[16].color = "red"  # 11-13

    RO.NODES[0].color = "red"  # Main 0
    RO.NODES[2].color = "red"  # Main 2
    RO.NODES[11].color = "red"  # 7_S
    RO.NODES[14].color = "red"  # 13_S

elif SlatersROMain0Closed and SlatersROMain3Closed:
    RO.LINKS[1].color = "red"  # 0_1
    RO.LINKS[2].color = "red"  # Main 0
    RO.LINKS[12].color = "red"  # 15_S
    RO.LINKS[13].color = "red"  # Main 3
    RO.LINKS[15].color = "red"  # 5-7

    RO.NODES[0].color = "red"  # Main 0
    RO.NODES[3].color = "red"  # Main 3
    RO.NODES[7].color = "red"  # Proposed_3_org
    RO.NODES[11].color = "red"  # 7_S

elif SlatersROMain1Closed and SlatersROMain2Closed:
    RO.LINKS[6].color = "red"  # 1_3
    RO.LINKS[7].color = "red"  # Main 1
    RO.LINKS[10].color = "red"  # 2_2
    RO.LINKS[11].color = "red"  # Main 2
    RO.LINKS[14].color = "red"  # 1-3
    RO.LINKS[16].color = "red"  # 11-13

    RO.NODES[1].color = "red"  # Main 1
    RO.NODES[2].color = "red"  # Main 2
    RO.NODES[13].color = "red"  # 11_S
    RO.NODES[14].color = "red"  # 13_S

elif SlatersROMain1Closed and SlatersROMain3Closed:
    RO.LINKS[12].color = "red"  # 15_S
    RO.LINKS[13].color = "red"  # Main 3
    RO.LINKS[7].color = "red"  # Main 1

    RO.NODES[1].color = "red"  # Main 1
    RO.NODES[3].color = "red"  # Main 3
    RO.NODES[7].color = "red"  # Proposed_3_org

elif SlatersROMain3Closed and SlatersROMain2Closed:
    RO.LINKS[8].color = "red"  # 9_S
    RO.LINKS[9].color = "red"  # 2_1
    RO.LINKS[10].color = "red"  # 2_2
    RO.LINKS[11].color = "red"  # Main 2
    RO.LINKS[12].color = "red"  # 15_S
    RO.LINKS[13].color = "red"  # Main 3
    RO.LINKS[16].color = "red"  # 11-13

    RO.NODES[2].color = "red"  # Main 2
    RO.NODES[3].color = "red"  # Main 3
    RO.NODES[6].color = "red"  # Proposed_2_org
    RO.NODES[7].color = "red"  # Proposed_3_org
    RO.NODES[14].color = "red"  # 13_S
    RO.NODES[15].color = "red"  # 15_S

# 4 versions of 1 track closed (0,0,0,0 is 16th possible combo and not included since it's the default state)
elif SlatersROMain3Closed:
    RO.LINKS[12].color = "red"  # 15_S
    RO.LINKS[13].color = "red"  # Main 3

    RO.NODES[3].color = "red"  # Main 3
    RO.NODES[7].color = "red"  # Proposed_3_org

elif SlatersROMain2Closed:
    RO.LINKS[10].color = "red"  # 2_2
    RO.LINKS[11].color = "red"  # Main 2
    RO.LINKS[16].color = "red"  # 11-13

    RO.NODES[2].color = "red"  # Main 2
    RO.NODES[14].color = "red"  # 13_S

elif SlatersROMain1Closed:
    RO.LINKS[7].color = "red"  # Main 1

    RO.NODES[1].color = "red"  # Main 1

elif SlatersROMain0Closed:
    RO.LINKS[1].color = "red"  # 0_1
    RO.LINKS[2].color = "red"  # Main 0
    RO.LINKS[15].color = "red"  # 5-7

    RO.NODES[0].color = "red"  # Main 0
    RO.NODES[11].color = "red"  # 7_S

# Determine if the Routes are open or closed on either side of the interlocking
RO.signal_attributes_high = {
    # Origin Values (color, position, opp end color)
    "Existing 2": (RO.LINKS[0].color, (1, 6.75), RO.LINKS[2].color),
    "Existing 3": (RO.LINKS[3].color, (1, 4.75), RO.LINKS[7].color),
}

RO.signal_attributes_low = {
    # Destinations
    "Proposed 0": (RO.LINKS[2].color, (27.5, 8.75), RO.LINKS[0].color),
    "Proposed 1": (RO.LINKS[7].color, (27.5, 6.75), RO.LINKS[3].color),
    "Proposed 2": (RO.LINKS[11].color, (27.5, 4.75), RO.LINKS[3].color),
    "Proposed 3": (RO.LINKS[13].color, (27.5, 2.75), RO.LINKS[3].color),
}

RO.title = "←L'Enfant                       RO (CFP 110.1/Sta. 325+00)                       Slaters Lane→"

# ===========================================    AF    ===========================================================
AF = World(
    name="AF-RO",
    deltan=1,
    tmax=1000,
    print_mode=1,
    save_mode=0,
    show_mode=1,
    random_seed=0,
)

# Define Southern (Low MP) Origins
AF.addNode("NS Horn Track 1", 30, 1, label_color="white", voffset=0.4, hoffset=1)  # 0
AF.addNode("y1e", 24, 1)  # 1
AF.addNode("NS Horn Track 2", 30, 3.5, label_color="white", voffset=0.4, hoffset=1)  # 2
AF.addNode("NS Horn Track 3", 30, 6, label_color="white", voffset=0.4, hoffset=1)  # 3
AF.addNode("Ex Main 3", 30, 8, label_color="white", voffset=0.4, hoffset=0.5)  # 4
AF.addNode("Ex Main 2", 30, 10, label_color="white", voffset=0.4, hoffset=0.5)  # 5
AF.addNode("Ex Main 1", 30, 12, label_color="white", voffset=0.4, hoffset=0.5)  # 6
AF.addNode("NS_org", 16, 14)  # 7
AF.addNode("NS_yard", 30, 14, label_color="white", voffset=0.4, hoffset=0.25)  # 8
AF.addNode("Setoff_org", 8, 14)  # 9
AF.addNode("Setoff Track", 1, 14, label_color="white", voffset=0.4, hoffset=1)  # 10

# Define Switches
AF.addNode("1_S", 26.5, 3.5)  # 11
AF.addNode("3_S", 24, 6)  # 12
AF.addNode("5_S", 22, 6)  # 13
AF.addNode("6_S", 19, 6)  # 14
AF.addNode("7_S", 20, 8)  # 15
AF.addNode("9_S", 20, 10)  # 16
AF.addNode("11_S", 18, 12)  # 17
AF.addNode("13_S", 18, 8)  # 18
AF.addNode("19_S", 16, 10)  # 19
AF.addNode("21_S", 15, 10)  # 20
AF.addNode("23_S", 13, 8)  # 21
AF.addNode("25_S", 14, 10)  # 22
AF.addNode("27_S", 14, 12)  # 23
AF.addNode("29_S", 12, 12)  # 24
AF.addNode("31_S", 11, 12)  # 25
AF.addNode("33_S", 9, 10)  # 26
AF.addNode("35_S", 10, 12)  # 27
AF.addNode("37_S", 8, 10)  # 28
AF.addNode("39_S", 6, 12)  # 29
AF.addNode("41_S", 10, 8)  # 30
AF.addNode("43_S", 8, 6)  # 31
AF.addNode("45_S", 7, 10)  # 32
AF.addNode("47_S", 5, 8)  # 33

# Add Destinations
AF.addNode("Main 0", 0, 12, label_color="white", voffset=0.4)  # 34
AF.addNode("Main 1", 0, 10, label_color="white", voffset=0.4)  # 35
AF.addNode("Main 2", 0, 8, label_color="white", voffset=0.4)  # 36
AF.addNode("Main 3", 0, 6, label_color="white", voffset=0.4)  # 37

# Define links between Values
# Crossovers
AF.addLink("1-3X", "1_S", "3_S", length=50, free_flow_speed=30, number_of_lanes=1)  # 0
AF.addLink("5-7X", "5_S", "7_S", length=50, free_flow_speed=30, number_of_lanes=1)  # 1
AF.addLink(
    "9-11X", "9_S", "11_S", length=50, free_flow_speed=30, number_of_lanes=1
)  # 2
AF.addLink(
    "13-19X", "13_S", "19_S", length=50, free_flow_speed=30, number_of_lanes=1
)  # 3
AF.addLink(
    "21-23X", "21_S", "23_S", length=50, free_flow_speed=30, number_of_lanes=1
)  # 4
AF.addLink(
    "25-29X", "25_S", "29_S", length=50, free_flow_speed=30, number_of_lanes=1
)  # 5
AF.addLink(
    "31-33X", "31_S", "33_S", length=50, free_flow_speed=30, number_of_lanes=1
)  # 6
AF.addLink(
    "37-39X", "37_S", "39_S", length=50, free_flow_speed=30, number_of_lanes=1
)  # 7
AF.addLink(
    "41-43X", "41_S", "43_S", length=50, free_flow_speed=30, number_of_lanes=1
)  # 8
AF.addLink(
    "45-47X", "45_S", "47_S", length=50, free_flow_speed=30, number_of_lanes=1
)  # 9

# Yard Segments
AF.addLink(
    "yard1",
    "NS Horn Track 1",
    "y1e",
    length=50,
    free_flow_speed=50,
    number_of_lanes=1,
    merge_priority=0.1,
)  # 10
AF.addLink(
    "y1_2",
    "y1e",
    "6_S",
    length=50,
    free_flow_speed=50,
    number_of_lanes=1,
    merge_priority=0.1,
)  # 11
AF.addLink(
    "yard2",
    "NS Horn Track 2",
    "1_S",
    length=50,
    free_flow_speed=50,
    number_of_lanes=1,
    merge_priority=0.1,
)  # 12
AF.addLink(
    "NS",
    "NS_org",
    "27_S",
    length=50,
    free_flow_speed=50,
    number_of_lanes=1,
    merge_priority=0.1,
)  # 13
AF.addLink(
    "NS Yard",
    "NS_yard",
    "NS_org",
    length=50,
    free_flow_speed=50,
    number_of_lanes=1,
    merge_priority=0.1,
)  # 14
AF.addLink(
    "Setoff_Track",
    "Setoff Track",
    "Setoff_org",
    length=50,
    free_flow_speed=50,
    number_of_lanes=1,
    merge_priority=0.1,
)  # 15
AF.addLink(
    "Setoff Track",
    "35_S",
    "Setoff_org",
    length=50,
    free_flow_speed=50,
    number_of_lanes=1,
    merge_priority=0.1,
)  # 16

# Main 0 Segments
AF.addLink(
    "0_0",
    "Ex Main 1",
    "11_S",
    length=50,
    free_flow_speed=50,
    number_of_lanes=1,
    merge_priority=0.1,
)  # 17
AF.addLink(
    "0_1",
    "11_S",
    "27_S",
    length=50,
    free_flow_speed=50,
    number_of_lanes=1,
    merge_priority=0.1,
)  # 18
AF.addLink(
    "0_2", "27_S", "29_S", length=50, free_flow_speed=50, number_of_lanes=1
)  # 19
AF.addLink(
    "0_3", "29_S", "31_S", length=50, free_flow_speed=50, number_of_lanes=1
)  # 20
AF.addLink(
    "0_4", "31_S", "35_S", length=50, free_flow_speed=50, number_of_lanes=1
)  # 21
AF.addLink(
    "0_5", "35_S", "39_S", length=50, free_flow_speed=50, number_of_lanes=1
)  # 22
AF.addLink(
    "0_6", "39_S", "Main 0", length=50, free_flow_speed=50, number_of_lanes=1
)  # 23

# Main 1 Segments
AF.addLink(
    "1_0",
    "Ex Main 2",
    "9_S",
    length=50,
    free_flow_speed=50,
    number_of_lanes=1,
    merge_priority=0.1,
)  # 24
AF.addLink(
    "1_1",
    "9_S",
    "19_S",
    length=50,
    free_flow_speed=50,
    number_of_lanes=1,
    merge_priority=0.1,
)  # 25
AF.addLink(
    "1_2",
    "19_S",
    "21_S",
    length=50,
    free_flow_speed=50,
    number_of_lanes=1,
    merge_priority=0.1,
)  # 26
AF.addLink(
    "1_3",
    "21_S",
    "25_S",
    length=50,
    free_flow_speed=50,
    number_of_lanes=1,
    merge_priority=0.1,
)  # 27
AF.addLink(
    "1_4",
    "25_S",
    "33_S",
    length=50,
    free_flow_speed=50,
    number_of_lanes=1,
    merge_priority=0.1,
)  # 28
AF.addLink(
    "1_5",
    "33_S",
    "37_S",
    length=50,
    free_flow_speed=50,
    number_of_lanes=1,
    merge_priority=0.1,
)  # 29
AF.addLink(
    "1_6",
    "37_S",
    "45_S",
    length=50,
    free_flow_speed=50,
    number_of_lanes=1,
    merge_priority=0.1,
)  # 30
AF.addLink(
    "1_7",
    "45_S",
    "Main 1",
    length=50,
    free_flow_speed=50,
    number_of_lanes=1,
    merge_priority=0.1,
)  # 31

# Main 2 Segments
AF.addLink(
    "2_0",
    "Ex Main 3",
    "7_S",
    length=50,
    free_flow_speed=50,
    number_of_lanes=1,
    merge_priority=0.1,
)  # 32
AF.addLink(
    "2_1",
    "7_S",
    "13_S",
    length=50,
    free_flow_speed=50,
    number_of_lanes=1,
    merge_priority=0.1,
)  # 33
AF.addLink(
    "2_2",
    "13_S",
    "23_S",
    length=50,
    free_flow_speed=50,
    number_of_lanes=1,
    merge_priority=0.1,
)  # 34
AF.addLink(
    "2_3",
    "23_S",
    "41_S",
    length=50,
    free_flow_speed=50,
    number_of_lanes=1,
    merge_priority=0.1,
)  # 35
AF.addLink(
    "2_4",
    "41_S",
    "47_S",
    length=50,
    free_flow_speed=50,
    number_of_lanes=1,
    merge_priority=0.1,
)  # 36
AF.addLink(
    "2_5",
    "47_S",
    "Main 2",
    length=50,
    free_flow_speed=50,
    number_of_lanes=1,
    merge_priority=0.1,
)  # 37

# Main 3 Segments
AF.addLink(
    "3_0",
    "NS Horn Track 3",
    "3_S",
    length=50,
    free_flow_speed=50,
    number_of_lanes=1,
    merge_priority=0.1,
)  # 38
AF.addLink(
    "3_1",
    "3_S",
    "5_S",
    length=50,
    free_flow_speed=50,
    number_of_lanes=1,
    merge_priority=0.1,
)  # 39
AF.addLink(
    "3_2",
    "5_S",
    "6_S",
    length=50,
    free_flow_speed=50,
    number_of_lanes=1,
    merge_priority=0.1,
)  # 40
AF.addLink(
    "3_3",
    "6_S",
    "43_S",
    length=50,
    free_flow_speed=50,
    number_of_lanes=1,
    merge_priority=0.1,
)  # 41
AF.addLink(
    "3_4",
    "43_S",
    "Main 3",
    length=50,
    free_flow_speed=50,
    number_of_lanes=1,
    merge_priority=0.1,
)  # 42

# Update the graph depending on what routes are closed
# 1 combination with all 4 tracks closed
if (
    AFSlatersMain0Closed
    and AFSlatersMain1Closed
    and AFSlatersMain2Closed
    and AFSlatersMain3Closed
):
    for link in AF.LINKS:
        link.color = "red"
    for node in AF.NODES:
        node.color = "red"

# 4 combos of 3 tracks closed
elif AFSlatersMain0Closed and AFSlatersMain1Closed and AFSlatersMain2Closed:
    # Example of closing main 0/1/2
    AF.LINKS[1].color = "red"  # 25-29X
    AF.LINKS[2].color = "red"  # 9-11X
    AF.LINKS[3].color = "red"  # 13-19X
    AF.LINKS[5].color = "red"  # 25-29X
    AF.LINKS[6].color = "red"  # 31-33X
    AF.LINKS[7].color = "red"  # 37-39X
    AF.LINKS[9].color = "red"  # 45-47X
    AF.LINKS[13].color = "red"  # NS
    AF.LINKS[14].color = "red"  # NS Yard
    AF.LINKS[17].color = "red"  # 0_0
    AF.LINKS[18].color = "red"  # 0_1
    AF.LINKS[19].color = "red"  # 0_2
    AF.LINKS[20].color = "red"  # 0_3
    AF.LINKS[21].color = "red"  # 0_4
    AF.LINKS[22].color = "red"  # 0_5
    AF.LINKS[23].color = "red"  # 0_6
    AF.LINKS[28].color = "red"  # 1_4
    AF.LINKS[29].color = "red"  # 1_5
    AF.LINKS[30].color = "red"  # 1_6
    AF.LINKS[31].color = "red"  # 1_7
    AF.LINKS[37].color = "red"  # 2_5

    AF.NODES[6].color = "red"  # Ex Main 1
    AF.NODES[7].color = "red"  # NS_org
    AF.NODES[8].color = "red"  # NS_Yard
    AF.NODES[15].color = "red"  # 7_S
    AF.NODES[16].color = "red"  # 9_S
    AF.NODES[17].color = "red"  # 11_S
    AF.NODES[18].color = "red"  # 13_S
    AF.NODES[19].color = "red"  # 19_S
    AF.NODES[23].color = "red"  # 27_S
    AF.NODES[25].color = "red"  # 31_S
    AF.NODES[26].color = "red"  # 33_S
    AF.NODES[27].color = "red"  # 35_S
    AF.NODES[22].color = "red"  # 25_S
    AF.NODES[24].color = "red"  # 29_S
    AF.NODES[28].color = "red"  # 37_S
    AF.NODES[29].color = "red"  # 39_S
    AF.NODES[32].color = "red"  # 45_S
    AF.NODES[33].color = "red"  # 47_S
    AF.NODES[34].color = "red"  # Main 0
    AF.NODES[35].color = "red"  # Main 1
    AF.NODES[36].color = "red"  # Main 2

elif AFSlatersMain0Closed and AFSlatersMain1Closed and AFSlatersMain3Closed:
    # Example of closing main 0/1/3
    AF.LINKS[7].color = "red"  # 37-39X
    AF.LINKS[8].color = "red"  # 41-43X
    AF.LINKS[10].color = "red"  # yard1
    AF.LINKS[11].color = "red"  # y1_2
    AF.LINKS[22].color = "red"  # 0_5
    AF.LINKS[23].color = "red"  # 0_6
    AF.LINKS[31].color = "red"  # 1_7
    AF.LINKS[40].color = "red"  # 3_2
    AF.LINKS[41].color = "red"  # 3_3
    AF.LINKS[42].color = "red"  # 3_4

    AF.NODES[0].color = "red"  # NS Horn Track 1
    AF.NODES[1].color = "red"  # y1e
    AF.NODES[14].color = "red"  # 6_S
    AF.NODES[29].color = "red"  # 39_S
    AF.NODES[31].color = "red"  # 43_S
    AF.NODES[34].color = "red"  # main0_dest
    AF.NODES[35].color = "red"  # Main1_dest
    AF.NODES[37].color = "red"  # main3_dest

elif AFSlatersMain0Closed and AFSlatersMain2Closed and AFSlatersMain3Closed:
    # Example of closing main 0/2/3
    AF.LINKS[4].color = "red"  # 13-19X
    AF.LINKS[7].color = "red"  # 37-39X
    AF.LINKS[8].color = "red"  # 41-43X
    AF.LINKS[9].color = "red"  # 45-47X
    AF.LINKS[10].color = "red"  # yard1
    AF.LINKS[11].color = "red"  # y1_2
    AF.LINKS[22].color = "red"  # 0_5
    AF.LINKS[23].color = "red"  # 0_6
    AF.LINKS[34].color = "red"  # 2_2
    AF.LINKS[35].color = "red"  # 2_4
    AF.LINKS[36].color = "red"  # 2_5
    AF.LINKS[37].color = "red"  # 2_6
    AF.LINKS[40].color = "red"  # 3_2
    AF.LINKS[41].color = "red"  # 3_3

    AF.NODES[0].color = "red"  # NS Horn Track 1
    AF.NODES[1].color = "red"  # y1e
    AF.NODES[14].color = "red"  # 6_S
    AF.NODES[21].color = "red"  # 23_S
    AF.NODES[29].color = "red"  # 39_S
    AF.NODES[30].color = "red"  # 41_S
    AF.NODES[31].color = "red"  # 43_S
    AF.NODES[33].color = "red"  # 47_S
    AF.NODES[34].color = "red"  # main0_dest
    AF.NODES[36].color = "red"  # main2_dest
    AF.NODES[37].color = "red"  # main3_dest

elif AFSlatersMain1Closed and AFSlatersMain2Closed and AFSlatersMain3Closed:
    # Example of closing main 1/2/3
    AF.LINKS[4].color = "red"  # 21-23X
    AF.LINKS[6].color = "red"  # 31-33X
    AF.LINKS[7].color = "red"  # 37-39X
    AF.LINKS[8].color = "red"  # 41-43X
    AF.LINKS[9].color = "red"  # 45-47X
    AF.LINKS[10].color = "red"  # yard1
    AF.LINKS[11].color = "red"  # y1_2
    AF.LINKS[28].color = "red"  # 1_4
    AF.LINKS[29].color = "red"  # 1_5
    AF.LINKS[30].color = "red"  # 1_6
    AF.LINKS[31].color = "red"  # 1_7
    AF.LINKS[34].color = "red"  # 2_2
    AF.LINKS[35].color = "red"  # 2_4
    AF.LINKS[36].color = "red"  # 2_5
    AF.LINKS[37].color = "red"  # 2_6
    AF.LINKS[40].color = "red"  # 3_2
    AF.LINKS[41].color = "red"  # 3_3
    AF.LINKS[42].color = "red"  # 3_4

    AF.NODES[0].color = "red"  # NS Horn Track 1
    AF.NODES[1].color = "red"  # y1e
    AF.NODES[14].color = "red"  # 6_S
    AF.NODES[21].color = "red"  # 23_S
    AF.NODES[26].color = "red"  # 33_S
    AF.NODES[28].color = "red"  # 37_S
    AF.NODES[30].color = "red"  # 41_S
    AF.NODES[31].color = "red"  # 43_S
    AF.NODES[32].color = "red"  # 45_S
    AF.NODES[33].color = "red"  # 47_S
    AF.NODES[35].color = "red"  # Main1_dest
    AF.NODES[36].color = "red"  # main2_dest
    AF.NODES[37].color = "red"  # main3_dest

# 6 combos of 2 tracks closed
elif AFSlatersMain0Closed and AFSlatersMain1Closed:
    # Example of closing main 0/1
    AF.LINKS[7].color = "red"  # 37-39X
    AF.LINKS[22].color = "red"  # 0_5
    AF.LINKS[23].color = "red"  # 0_6
    AF.LINKS[31].color = "red"  # 1_7

    AF.NODES[29].color = "red"  # 39_S
    AF.NODES[34].color = "red"  # main0_dest
    AF.NODES[35].color = "red"  # Main1_dest

elif AFSlatersMain0Closed and AFSlatersMain2Closed:
    # Example of closing main 0/2
    AF.LINKS[7].color = "red"  # 37-39X
    AF.LINKS[9].color = "red"  # 45-47X
    AF.LINKS[22].color = "red"  # 0_5
    AF.LINKS[23].color = "red"  # 0_6
    AF.LINKS[36].color = "red"  # 2_5
    AF.LINKS[37].color = "red"  # 2_6

    AF.NODES[29].color = "red"  # 39_S
    AF.NODES[33].color = "red"  # 47_S
    AF.NODES[34].color = "red"  # main0_dest
    AF.NODES[36].color = "red"  # main2_dest

elif AFSlatersMain0Closed and AFSlatersMain3Closed:
    # Example of closing main 0/3
    AF.LINKS[7].color = "red"  # 37-39X
    AF.LINKS[8].color = "red"  # 41-43X
    AF.LINKS[22].color = "red"  # 0_5
    AF.LINKS[23].color = "red"  # 0_6
    AF.LINKS[41].color = "red"  # 3_3
    AF.LINKS[42].color = "red"  # 3_4

    AF.NODES[29].color = "red"  # 39_S
    AF.NODES[31].color = "red"  # 43_S
    AF.NODES[34].color = "red"  # main0_dest
    AF.NODES[37].color = "red"  # main3_dest

elif AFSlatersMain1Closed and AFSlatersMain2Closed:
    # Example of closing main 1/2
    AF.LINKS[6].color = "red"  # 31-33X
    AF.LINKS[9].color = "red"  # 45-47X
    AF.LINKS[30].color = "red"  # 1_6
    AF.LINKS[31].color = "red"  # 1_7
    AF.LINKS[36].color = "red"  # 2_5
    AF.LINKS[37].color = "red"  # 2_6

    AF.NODES[32].color = "red"  # 45_S
    AF.NODES[33].color = "red"  # 47_S
    AF.NODES[35].color = "red"  # Main1_dest
    AF.NODES[36].color = "red"  # main2_dest

elif AFSlatersMain2Closed and AFSlatersMain3Closed:
    AF.LINKS[4].color = "red"  # 21-23X
    AF.LINKS[8].color = "red"  # 41-43X
    AF.LINKS[9].color = "red"  # 45-47X
    AF.LINKS[10].color = "red"  # yard1
    AF.LINKS[11].color = "red"  # y1_2
    AF.LINKS[34].color = "red"  # 2_2
    AF.LINKS[35].color = "red"  # 2_3
    AF.LINKS[36].color = "red"  # 2_4
    AF.LINKS[37].color = "red"  # 2_5
    AF.LINKS[40].color = "red"  # 3_2
    AF.LINKS[41].color = "red"  # 3_3
    AF.LINKS[42].color = "red"  # 3_4

    AF.NODES[0].color = "red"  # NS Horn Track 1
    AF.NODES[1].color = "red"  # y1e
    AF.NODES[14].color = "red"  # 6_S
    AF.NODES[21].color = "red"  # 23_S
    AF.NODES[30].color = "red"  # 41_S
    AF.NODES[31].color = "red"  # 43_S
    AF.NODES[33].color = "red"  # 47_S
    AF.NODES[37].color = "red"  # Main 3
    AF.NODES[36].color = "red"  # Main 2

elif AFSlatersMain1Closed and AFSlatersMain3Closed:
    # Example of closing main 1/3
    AF.LINKS[8].color = "red"  # 41-43X
    AF.LINKS[10].color = "red"  # yard1
    AF.LINKS[11].color = "red"  # y1_2
    AF.LINKS[31].color = "red"  # 1_7
    AF.LINKS[40].color = "red"  # 3_2
    AF.LINKS[41].color = "red"  # 3_3
    AF.LINKS[42].color = "red"  # 3_4

    AF.NODES[0].color = "red"  # NS Horn Track 1
    AF.NODES[1].color = "red"  # y1e
    AF.NODES[14].color = "red"  # 6_S
    AF.NODES[31].color = "red"  # 43_S
    AF.NODES[35].color = "red"  # Main1_dest
    AF.NODES[37].color = "red"  # main3_dest

# 4 versions of 1 track closed (0,0,0,0 is 16th possible combo and not included since it's the default state)
elif AFSlatersMain3Closed:
    AF.LINKS[8].color = "red"  # 41-43X
    AF.LINKS[10].color = "red"  # yard1
    AF.LINKS[11].color = "red"  # y1_2
    AF.LINKS[40].color = "red"  # 3_2
    AF.LINKS[41].color = "red"  # 3_3
    AF.LINKS[42].color = "red"  # 3_4

    AF.NODES[0].color = "red"  # NS Horn Track 1
    AF.NODES[1].color = "red"  # y1e
    AF.NODES[14].color = "red"  # 6_S
    AF.NODES[31].color = "red"  # 43_S
    AF.NODES[37].color = "red"  # Main 3

elif AFSlatersMain2Closed:
    AF.LINKS[36].color = "red"  # Main 2
    AF.LINKS[37].color = "red"  # Main 3
    AF.LINKS[9].color = "red"  # 45-47X

    AF.NODES[33].color = "red"  # 47_S
    AF.NODES[36].color = "red"  # Main 2

elif AFSlatersMain1Closed:
    AF.LINKS[31].color = "red"  # 1_7

    AF.NODES[35].color = "red"  # 2_3

elif AFSlatersMain0Closed:
    AF.LINKS[7].color = "red"  # 37-39X
    AF.LINKS[22].color = "red"  # 0_5
    AF.LINKS[23].color = "red"  # 0_6

    AF.NODES[28].color = "red"  # 1_4
    AF.NODES[29].color = "red"  # 1_5
    AF.NODES[34].color = "red"  # 2_2

# Determine if the Routes are open or closed on either side of the interlocking
AF.signal_attributes_low = {
    # Origin Values (color, position)
    "NS_Yard": (AF.LINKS[14].color, (27.5, 14.75), "yard"),
    "Main 1": (AF.LINKS[17].color, (27.5, 12.75), AF.LINKS[23].color),
    "Main 2": (AF.LINKS[24].color, (27.5, 10.75), AF.LINKS[31].color),
    "Main 3": (AF.LINKS[32].color, (27.5, 8.75), AF.LINKS[37].color),
    "NS Horn Track 3": (AF.LINKS[38].color, (27.5, 6.75), AF.LINKS[41].color),
    "NS Horn Track 2": (AF.LINKS[12].color, (27.5, 4.5), "yard"),
    "NS Horn Track 1": (AF.LINKS[10].color, (27.5, 2), "yard"),
}

AF.signal_attributes_high = {
    # Destinations
    "Setoff Track": (AF.LINKS[16].color, (1, 12.75), "yard"),
    "Main 0": (AF.LINKS[23].color, (1, 10.75), AF.LINKS[17].color),
    "Main 1": (AF.LINKS[31].color, (1, 8.75), AF.LINKS[24].color),
    "Main 2": (AF.LINKS[37].color, (1, 6.75), AF.LINKS[32].color),
    "Main 3": (AF.LINKS[41].color, (1, 4.75), AF.LINKS[38].color),
}

AF.title = "←Slaters Lane         AF (CFP 104.3/Sta. 25+00)                             Franconia→"

# =======================================      Slaters Lane        ==============================================

# Create the World Object
Slaters = World(
    name="Slaters",
    deltan=1,
    tmax=1000,
    print_mode=1,
    save_mode=0,
    show_mode=1,
    random_seed=0,
)

# Define Southern (Low MP) Origins
Slaters.addNode("RO-Slaters Main 0", 0, 8, label_color="white", voffset=0.4)  # 0
Slaters.addNode("RO-Slaters Main 1", 0, 6, label_color="white", voffset=0.4)  # 1
Slaters.addNode("RO-Slaters Main 2", 0, 4, label_color="white", voffset=0.4)  # 2
Slaters.addNode("RO-Slaters Main 3", 0, 2, label_color="white", voffset=0.4)  # 3

# Define Northern (High MP) Origins
Slaters.addNode("OOS_NS", 28.5, 10, label_color="white", voffset=0.4, hoffset=-0.5)  # 4
Slaters.addNode("Slaters-AF Main 0", 30, 8, label_color="white", voffset=0.4)  # 5
Slaters.addNode("Slaters-AF Main 1", 30, 6, label_color="white", voffset=0.4)  # 6
Slaters.addNode("Slaters-AF Main 2", 30, 4, label_color="white", voffset=0.4)  # 7
Slaters.addNode("Slaters-AF Main 3", 30, 2, label_color="white", voffset=0.4)  # 8

# Define Switch Points
Slaters.addNode("NS_OOS", 24, 10)  # 9
Slaters.addNode("3_S", 22, 8)  # 10
Slaters.addNode("5_S", 24, 2)  # 11
Slaters.addNode("7_S", 22, 4)  # 12
Slaters.addNode("9_S", 15, 4)  # 13
Slaters.addNode("11_S", 13, 6)  # 14
Slaters.addNode("13_S", 20, 6)  # 15
Slaters.addNode("15_S", 18, 8)  # 16
Slaters.addNode("17_S", 8, 8)  # 17
Slaters.addNode("19_S", 6, 6)  # 18
Slaters.addNode("21_S", 8, 4)  # 19
Slaters.addNode("23_S", 6, 2)  # 20

# Track Segments
Slaters.addLink("PepCo  Lead", "OOS_NS", "NS_OOS", length=50)  # 0
Slaters.addLink("3_S", "NS_OOS", "3_S", length=50)  # 1
Slaters.addLink("0_0", "Slaters-AF Main 0", "3_S", length=50)  # 2
Slaters.addLink("0_1", "3_S", "15_S", length=50)  # 3
Slaters.addLink("0_2", "15_S", "17_S", length=50)  # 4
Slaters.addLink("0_3", "17_S", "RO-Slaters Main 0", length=50)  # 5
Slaters.addLink("1_0", "Slaters-AF Main 1", "13_S", length=50)  # 6
Slaters.addLink("1_1", "13_S", "11_S", length=50)  # 7
Slaters.addLink("1_2", "11_S", "19_S", length=50)  # 8
Slaters.addLink("1_3", "19_S", "RO-Slaters Main 1", length=50)  # 9
Slaters.addLink("2_0", "Slaters-AF Main 2", "7_S", length=50)  # 10
Slaters.addLink("2_1", "7_S", "9_S", length=50)  # 11
Slaters.addLink("2_2", "9_S", "21_S", length=50)  # 12
Slaters.addLink("2_3", "RO-Slaters Main 2", "21_S", length=50)  # 13
Slaters.addLink("3_0", "Slaters-AF Main 3", "5_S", length=50)  # 14
Slaters.addLink("3_1", "5_S", "23_S", length=50)  # 15
Slaters.addLink("3_2", "23_S", "RO-Slaters Main 3", length=50)  # 16

# Cross Overs
Slaters.addLink("13_15X", "13_S", "15_S", length=20)  # 17
Slaters.addLink("5_7X", "5_S", "7_S", length=20)  # 18
Slaters.addLink("9_11X", "9_S", "11_S", length=20)  # 19
Slaters.addLink("17_19X", "17_S", "19_S", length=20)  # 20
Slaters.addLink("21_23X", "21_S", "23_S", length=20)  # 21

# Match the links in slaters to their values in other areas
Slaters.NODES[0].color = RO.NODES[0].color  # RO-Slaters Main 0
Slaters.NODES[1].color = RO.NODES[1].color  # RO-Slaters Main 1
Slaters.NODES[2].color = RO.NODES[2].color  # RO-Slaters Main 2
Slaters.NODES[3].color = RO.NODES[3].color  # RO-Slaters Main 3

Slaters.LINKS[5].color = RO.LINKS[2].color  # Slaters 0_3 = RO Main 0
Slaters.LINKS[9].color = RO.LINKS[7].color  # Slaters 1_3 = RO Main 1
Slaters.LINKS[13].color = RO.LINKS[11].color  # Slaters 2_3 = RO Main 2
Slaters.LINKS[16].color = RO.LINKS[13].color  # Slaters 3_2 = RO Main 3

Slaters.NODES[5].color = AF.NODES[34].color  # RO-Slaters Main 0
Slaters.NODES[6].color = AF.NODES[35].color  # RO-Slaters Main 1
Slaters.NODES[7].color = AF.NODES[36].color  # RO-Slaters Main 2
Slaters.NODES[8].color = AF.NODES[37].color  # RO-Slaters Main 3

Slaters.LINKS[2].color = AF.LINKS[23].color  # Slaters 0_0 = AF 0_6
Slaters.LINKS[6].color = AF.LINKS[31].color  # Slaters 1_0 = AF 1_7
Slaters.LINKS[10].color = AF.LINKS[37].color  # Slaters 2_0 = AF 2_5
Slaters.LINKS[14].color = AF.LINKS[42].color  # Slaters 3_0 = AF 3_4

# Either of all 4 tracks closed on either side
if (
    AFSlatersMain0Closed
    and AFSlatersMain1Closed
    and AFSlatersMain2Closed
    and AFSlatersMain3Closed
) or (
    SlatersROMain0Closed
    and SlatersROMain1Closed
    and SlatersROMain2Closed
    and SlatersROMain3Closed
):
    for link in Slaters.LINKS:
        link.color = "red"
    for node in Slaters.NODES:
        node.color = "red"

# All combos of 2 closed tracks
elif SlatersROMain0Closed & SlatersROMain1Closed:
    Slaters.LINKS[0].color = "red"  # Pepco Lead
    Slaters.LINKS[1].color = "red"  # 3_S
    Slaters.LINKS[2].color = "red"  # 0_0
    Slaters.LINKS[3].color = "red"  # 0_1
    Slaters.LINKS[4].color = "red"  # 0_2
    Slaters.LINKS[6].color = "red"  # 1_0
    Slaters.LINKS[7].color = "red"  # 1_1
    Slaters.LINKS[8].color = "red"  # 1_2
    Slaters.LINKS[17].color = "red"  # 13_15X
    Slaters.LINKS[19].color = "red"  # 9_11X
    Slaters.LINKS[20].color = "red"  # 17_19X

    Slaters.NODES[4].color = "red"  # OOS_NS
    Slaters.NODES[5].color = "red"  # Slaters-AF Main 0
    Slaters.NODES[6].color = "red"  # Slaters-AF Main 1
    Slaters.NODES[9].color = "red"  # NS_OOS
    Slaters.NODES[10].color = "red"  # 3_S
    Slaters.NODES[14].color = "red"  # 11_S
    Slaters.NODES[15].color = "red"  # 13_S
    Slaters.NODES[16].color = "red"  # 15_S
    Slaters.NODES[17].color = "red"  # 17_S
    Slaters.NODES[18].color = "red"  # 18_S

elif SlatersROMain0Closed & SlatersROMain2Closed:
    # Comment to collapse in IDE
    Slaters.LINKS[17].color = "red"  # 13_15X

elif SlatersROMain0Closed & SlatersROMain3Closed:
    Slaters.NODES[20].color = "red"  # 23_S

    Slaters.LINKS[17].color = "red"  # 13_15X
    Slaters.LINKS[21].color = "red"  # 21_23X
    Slaters.LINKS[15].color = "red"  # 3_1

elif SlatersROMain1Closed & SlatersROMain2Closed:
    Slaters.LINKS[7].color = "red"  # 1_1
    Slaters.LINKS[8].color = "red"  # 1_2
    Slaters.LINKS[18].color = "red"  # 5_7X
    Slaters.LINKS[19].color = "red"  # 9_11X
    Slaters.LINKS[20].color = "red"  # 17_19X

    Slaters.NODES[14].color = "red"  # 11_S
    Slaters.NODES[18].color = "red"  # 19_S

elif SlatersROMain1Closed & SlatersROMain3Closed:
    Slaters.LINKS[7].color = "red"  # 1_2
    Slaters.LINKS[8].color = "red"  # 1_1
    Slaters.LINKS[19].color = "red"  # 9_11X
    Slaters.LINKS[20].color = "red"  # 17_19X

    Slaters.NODES[14].color = "red"  # 11_S
    Slaters.NODES[18].color = "red"  # 19_S
    Slaters.NODES[20].color = "red"  # 23_S
    Slaters.LINKS[21].color = "red"  # 21_23X
    Slaters.LINKS[15].color = "red"  # 3_1

elif SlatersROMain2Closed & SlatersROMain3Closed:
    Slaters.NODES[19].color = "red"  # 21_S
    Slaters.NODES[20].color = "red"  # 23_S

    Slaters.LINKS[12].color = "red"  # 2_2
    Slaters.LINKS[15].color = "red"  # 3_1
    Slaters.LINKS[21].color = "red"  # 21_23X

elif SlatersROMain0Closed & AFSlatersMain0Closed:
    Slaters.LINKS[0].color = "red"  # Pepco Lead
    Slaters.LINKS[1].color = "red"  # 3_S
    Slaters.LINKS[3].color = "red"  # 0_1
    Slaters.LINKS[4].color = "red"  # 0_2
    Slaters.LINKS[20].color = "red"  # 17_19X
    Slaters.LINKS[17].color = "red"  # 13_15X

    Slaters.NODES[10].color = "red"  # 3_S
    Slaters.NODES[16].color = "red"  # 15_S
    Slaters.NODES[17].color = "red"  # 17_S
    Slaters.NODES[4].color = "red"  # OOS_NS
    Slaters.NODES[9].color = "red"  # NS_OOS

elif SlatersROMain0Closed & AFSlatersMain1Closed:
    Slaters.LINKS[7].color = "red"  # 1_1
    Slaters.LINKS[17].color = "red"  # 13_15X

    Slaters.NODES[15].color = "red"  # 13_S


# AF/Slaters Closed
elif AFSlatersMain0Closed & AFSlatersMain1Closed:
    Slaters.LINKS[0].color = "red"  # Pepco Lead
    Slaters.LINKS[1].color = "red"  # 3_S
    Slaters.LINKS[3].color = "red"  # 0_1
    Slaters.LINKS[4].color = "red"  # 0_2
    Slaters.LINKS[5].color = "red"  # 0_3
    Slaters.LINKS[7].color = "red"  # 1_1X
    Slaters.LINKS[17].color = "red"  # 13_15X
    Slaters.LINKS[20].color = "red"  # 17_19X

    Slaters.NODES[0].color = "red"  # RO-Slaters Main 0
    Slaters.NODES[4].color = "red"  # OOS_NS
    Slaters.NODES[9].color = "red"  # NS_OOS
    Slaters.NODES[10].color = "red"  # 3_S
    Slaters.NODES[15].color = "red"  # 13_S
    Slaters.NODES[16].color = "red"  # 15_S
    Slaters.NODES[17].color = "red"  # 17_S

elif AFSlatersMain0Closed & AFSlatersMain2Closed:
    Slaters.LINKS[3].color = "red"  # 0_1
    Slaters.LINKS[20].color = "red"  # 17_19X

    Slaters.NODES[10].color = "red"  # 3_S
    Slaters.NODES[17].color = "red"  # 17_S

elif AFSlatersMain0Closed & AFSlatersMain3Closed:
    Slaters.LINKS[3].color = "red"  # 0_1
    Slaters.LINKS[15].color = "red"  # 3_1
    Slaters.LINKS[18].color = "red"  # 5_7X
    Slaters.LINKS[20].color = "red"  # 17_19X

    Slaters.NODES[10].color = "red"  # 3_S
    Slaters.NODES[11].color = "red"  # 5_S
    Slaters.NODES[17].color = "red"  # 17_S

elif AFSlatersMain1Closed & AFSlatersMain2Closed:
    Slaters.LINKS[7].color = "red"  # 1_1
    Slaters.LINKS[17].color = "red"  # 13_15X

    Slaters.NODES[15].color = "red"  # 13_S

elif AFSlatersMain1Closed & AFSlatersMain3Closed:
    Slaters.LINKS[7].color = "red"  # 1_1
    Slaters.LINKS[15].color = "red"  # 3_1
    Slaters.LINKS[17].color = "red"  # 13_15X
    Slaters.LINKS[18].color = "red"  # 5_7X

    Slaters.NODES[11].color = "red"  # 5_S
    Slaters.NODES[15].color = "red"  # 13_S

elif AFSlatersMain2Closed & AFSlatersMain3Closed:
    Slaters.LINKS[11].color = "red"  # 2_1
    Slaters.LINKS[12].color = "red"  # 2_2
    Slaters.LINKS[13].color = "red"  # 2_3
    Slaters.LINKS[15].color = "red"  # 3_1
    Slaters.LINKS[16].color = "red"  # 3_2
    Slaters.LINKS[18].color = "red"  # 5_7X
    Slaters.LINKS[19].color = "red"  # 9_11X
    Slaters.LINKS[21].color = "red"  # 21_23X

    Slaters.NODES[2].color = "red"  # RO-Slaters Main 2
    Slaters.NODES[3].color = "red"  # RO-Slaters Main 3
    Slaters.NODES[11].color = "red"  # 5_S
    Slaters.NODES[12].color = "red"  # 7_S
    Slaters.NODES[13].color = "red"  # 9_S
    Slaters.NODES[19].color = "red"  # 21_S
    Slaters.NODES[20].color = "red"  # 23_S

elif AFSlatersMain1Closed & SlatersROMain1Closed:
    Slaters.LINKS[7].color = "red"  # 1_1
    Slaters.LINKS[8].color = "red"  # 1_2
    Slaters.LINKS[17].color = "red"  # 13_15X
    Slaters.LINKS[19].color = "red"  # 9_11X
    Slaters.LINKS[20].color = "red"  # 17_19X

    Slaters.NODES[14].color = "red"  # 11_S
    Slaters.NODES[18].color = "red"  # 19_S
    Slaters.NODES[15].color = "red"  # 13_S

elif AFSlatersMain2Closed & SlatersROMain2Closed:
    Slaters.LINKS[11].color = "red"  # 2_1
    Slaters.LINKS[12].color = "red"  # 2_2
    Slaters.LINKS[18].color = "red"  # 5_7X
    Slaters.LINKS[19].color = "red"  # 9_11X
    Slaters.LINKS[21].color = "red"  # 21_23X

    Slaters.NODES[12].color = "red"  # 7_S
    Slaters.NODES[13].color = "red"  # 9_S
    Slaters.NODES[19].color = "red"  # 21_S

elif AFSlatersMain3Closed & SlatersROMain3Closed:
    Slaters.LINKS[15].color = "red"  # 3_1
    Slaters.LINKS[18].color = "red"  # 5_7X
    Slaters.LINKS[21].color = "red"  # 21_23X

    Slaters.NODES[11].color = "red"  # 5_S
    Slaters.NODES[20].color = "red"  # 23_S

# 1 track of RO-Slaters Closed
elif SlatersROMain0Closed and not (AFSlatersMain2Closed or AFSlatersMain3Closed):
    # Comment to make the statement collapsible in IDE
    Slaters.LINKS[17].color = "red"  # 13_15X

elif SlatersROMain1Closed:
    Slaters.LINKS[7].color = "red"  # 1_2
    Slaters.LINKS[8].color = "red"  # 1_1
    Slaters.LINKS[19].color = "red"  # 9_11X
    Slaters.LINKS[20].color = "red"  # 17_19X

    Slaters.NODES[14].color = "red"  # 11_S
    Slaters.NODES[18].color = "red"  # 19_S

elif SlatersROMain2Closed:
    # Handled by the associated track segment logic alone
    pass

elif SlatersROMain3Closed:
    Slaters.NODES[20].color = "red"  # 23_S
    Slaters.LINKS[21].color = "red"  # 21_23X
    Slaters.LINKS[15].color = "red"  # 3_1

# 1 Track of AF - SlatersMain closed
elif AFSlatersMain0Closed:
    Slaters.LINKS[3].color = "red"  # 0_1
    Slaters.NODES[10].color = "red"  # 3_S

elif AFSlatersMain1Closed:
    Slaters.LINKS[7].color = "red"  # 1_1X
    Slaters.LINKS[17].color = "red"  # 13_15X

    Slaters.NODES[15].color = "red"  # 13_S

elif AFSlatersMain2Closed:
    # Handled by the associated track segment logic alone
    pass

elif AFSlatersMain3Closed:
    Slaters.LINKS[15].color = "red"  # 3_1
    Slaters.LINKS[18].color = "red"  # 5_7X

    Slaters.NODES[11].color = "red"  # 5_S

# Determine if the Routes are open or closed on either side of the interlocking
Slaters.signal_attributes_high = {
    # Slaters RO (color, position, opp end color)
    "Proposed 0": (Slaters.LINKS[5].color, (1, 6.75), Slaters.LINKS[2].color),
    "Proposed 1": (Slaters.LINKS[9].color, (1, 4.75), Slaters.LINKS[6].color),
    "Proposed 2": (Slaters.LINKS[13].color, (1, 2.75), Slaters.LINKS[10].color),
    "Proposed 3": (Slaters.LINKS[16].color, (1, 0.75), Slaters.LINKS[14].color),
}

Slaters.signal_attributes_low = {
    # AF to Slaters
    "OOS_NS": (Slaters.LINKS[0].color, (27.5, 10.75), "yard"),
    "Proposed 0": (Slaters.LINKS[2].color, (27.5, 8.75), Slaters.LINKS[5].color),
    "Proposed 1": (Slaters.LINKS[6].color, (27.5, 6.75), Slaters.LINKS[9].color),
    "Proposed 2": (Slaters.LINKS[10].color, (27.5, 4.75), Slaters.LINKS[13].color),
    "Proposed 3": (Slaters.LINKS[14].color, (27.5, 2.75), Slaters.LINKS[16].color),
}


Slaters.title = "←RO                         Slater's Lane (CFP 106.3/Sta. 130+00)                           AF→"

st.pyplot(RO.show_network(figsize=(20, 20)))

st.pyplot(Slaters.show_network(figsize=(20, 20)))

st.pyplot(AF.show_network(figsize=(20, 20)))
