import os
import json
import requests
from pathlib import Path

# Load the secrets.json file from the parent directory
try:
    civilpy_secrets_path = Path(os.getcwd()).parent.parent.parent
    with open('../../../secrets.json', 'r') as f:
        data = json.load(f)
        MIDAS_API_KEY = data['MIDAS_API_KEY']
except FileNotFoundError as e:
    print(''''
            Could not call the MIDAS API, ensure it\'s running and your key is correctly
            Stored in your secrets.json file located at the following location:
            ''')
    print(f"{e}")


# function for MIDAS Open API
def midas_api(method, command, body=None):
    base_url = "https://moa-engineers.midasit.com:443/civil/"
    mapi_key = MIDAS_API_KEY

    url = base_url + command
    headers = {
        "Content-Type": "application/json",
        "MAPI-Key": mapi_key
    }

    try:
        if method.upper() == "POST":
            response = requests.post(url=url, headers=headers, json=body)
        elif method.upper() == "PUT":
            response = requests.put(url=url, headers=headers, json=body)
        elif method.upper() == "GET":
            response = requests.get(url=url, headers=headers)
        elif method.upper() == "DELETE":
            response = requests.delete(url=url, headers=headers)

        print(method, command, response.status_code)
        return response.json()
    except NameError as not_defined:
        print(''''
        Could not call the MIDAS API, ensure it\'s running and your key is correctly
        Stored in your secrets.json file located at the following location:
        ''')
        print(f"{not_defined}")


def convert_units(to: str) -> None:
    # Get the current list of nodes in midas
    nodes = midas_api('GET', "db/node")

    # Go through every node and multiply/divide depending on need
    for index_value in nodes['NODE']:
        print(index_value, end=': ')
        for xyz_value in nodes['NODE'][index_value]:
            print(f"{xyz_value}: {nodes['NODE'][index_value][xyz_value]}", end=', ')
            if to == 'feet':
                nodes['NODE'][index_value][xyz_value] *= 12  # Convert from inches to feet
                print(f"Updated to {xyz_value}: {nodes['NODE'][index_value][xyz_value]}", end=', ')
            elif to == 'inches':
                nodes['NODE'][index_value][xyz_value] *= 12  # Convert from inches to feet
                print(f"Updated to {xyz_value}: {nodes['NODE'][index_value][xyz_value]}", end=', ')
            else:
                print('Please specify units to convert to ("feet"/"inches")')
                print('\n')

                # MidasAPI expects the first key in the values to be 'Assign'
                nodes['Assign'] = nodes.pop('NODE')

                # Send the updated values back to midas
                midas_api('PUT', "db/node", nodes)