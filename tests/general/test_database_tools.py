import unittest
from unittest.mock import patch
from civilpy.general.database_tools import ssh_into_postgres


test_creds = {
    "SSH_HOST": 'ssh_host',
    "SSH_PORT": 22,
    "SSH_USER": 'ssh_user',
    "SSH_PASSWORD": 'ssh_password',
    "DB_HOST": '127.0.0.1',
    "PORT": 5432,
    "PG_DB_NAME": 'db_name',
    "PG_UN": 'db_user',
    "PG_DB_PW": 'db_password'
}


class TestSSHConnection(unittest.TestCase):

    @patch('civilpy.general.database_tools.SSHTunnelForwarder')
    @patch('civilpy.general.database_tools.pg.connect')
    def test_connect_via_ssh_tunnel(self, mock_connect, mock_ssh_tunnel):
        # Set up
        mock_ssh_tunnel.return_value.local_bind_port = 5432
        mock_ssh_tunnel.return_value.local_bind_host = '127.0.0.1'

        # Call the function with test data
        ssh_into_postgres(creds=test_creds)

        # Assertions
        mock_ssh_tunnel.assert_called_once_with(
            ('ssh_host', 22),
            ssh_username='ssh_user',
            ssh_password='ssh_password',
            remote_bind_address=('127.0.0.1', 5432),
            local_bind_address=('127.0.0.1', 5432)
        )
        mock_connect.assert_called_once_with(
            host='127.0.0.1',
            port=5432,
            user='db_user',
            password='db_password',
            database='db_name'
        )


if __name__ == '__main__':
    unittest.main()
