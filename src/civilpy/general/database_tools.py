import psycopg2 as pg
from sshtunnel import SSHTunnelForwarder


def ssh_into_postgres(creds):
    """
    Function to open an ssh tunnel directly to a postgres database to gather
    data from it

    :param creds: dictionary of necessary parameters to connect to the database
    :return:
    """
    try:
        ssh_tunnel = SSHTunnelForwarder(
            (creds["SSH_HOST"], creds["SSH_PORT"]),
            ssh_username=creds["SSH_USER"],
            ssh_private_key=creds['SSH_PKEY'],
            ssh_private_key_password=creds["SSH_PKEY"],
            remote_bind_address=(creds["DB_HOST"], creds['PORT'])
        )

        ssh_tunnel.start()

        conn = pg.connect(
            host=creds["LOCALHOST"],
            port=ssh_tunnel.local_bind_port,
            user=creds["PG_UN"],
            password=creds["PG_DB_PW"],
            database=creds["PG_DB_NAME"]
        )

        return conn

    except:
        print("Connection Failed, ensure you have the correct values in the secrets/secrets.json file")



