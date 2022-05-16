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

import psycopg as pg
from sshtunnel import SSHTunnelForwarder


def ssh_into_postgres(creds):
    """
    Function to open an ssh tunnel directly to a postgres database to gather
    data from it

    :param creds: dictionary of necessary parameters to connect to the database
    :return:
    """
    ssh_tunnel = SSHTunnelForwarder(
        (creds["SSH_HOST"], creds["SSH_PORT"]),
        ssh_username=creds["SSH_USER"],
        ssh_password=creds["SSH_PASSWORD"],
        remote_bind_address=(creds["DB_HOST"], creds["PORT"]),
        local_bind_address=(creds["DB_HOST"], creds["PORT"]),
    )

    ssh_tunnel.start()

    conn = pg.connect(
        host=ssh_tunnel.local_bind_host,
        port=ssh_tunnel.local_bind_port,
        user=creds["PG_UN"],
        password=creds["PG_DB_PW"],
        database=creds["PG_DB_NAME"],
    )

    return conn
