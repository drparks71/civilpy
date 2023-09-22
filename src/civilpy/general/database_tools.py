import psycopg2 as pg
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
        ssh_password=creds['SSH_PASSWORD'],
        remote_bind_address=(creds["DB_HOST"], creds['PORT']),
        local_bind_address=(creds["DB_HOST"], creds['PORT'])
    )

    ssh_tunnel.start()

    conn = pg.connect(
        host=ssh_tunnel.local_bind_host,
        port=ssh_tunnel.local_bind_port,
        user=creds["PG_UN"],
        password=creds["PG_DB_PW"],
        database=creds["PG_DB_NAME"]
    )

    return conn
