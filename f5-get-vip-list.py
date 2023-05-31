import urllib3
import requests

urllib3.disable_warnings()

TARGET_URL = "https://bigip.f5.com"

def authenticate(username, password):
    """
    Authenticates the user and returns the authentication token.

    Args:
        username (str): The username for authentication.
        password (str): The password for authentication.

    Returns:
        str: The authentication token.

    Raises:
        requests.exceptions.RequestException: If there is an error in the authentication request.
    """
    auth_payload = {
        "username": username,
        "password": password
    }

    auth_response = requests.post(
        TARGET_URL + "/mgmt/shared/authn/login",
        json=auth_payload,
        verify=False  # Disable SSL verification if needed
    )

    auth_response.raise_for_status()

    return auth_response.json()["token"]["token"]

def retrieve_virtual_servers(auth_token):
    """
    Retrieves a list of virtual servers using the provided authentication token.

    Args:
        auth_token (str): The authentication token.

    Returns:
        dict: The JSON response containing the virtual servers data.

    Raises:
        requests.exceptions.RequestException: If there is an error in the request to retrieve virtual servers.
    """
    headers = {
        "X-F5-Auth-Token": auth_token
    }

    virtual_servers_response = requests.get(
        TARGET_URL + "/mgmt/tm/ltm/virtual",
        headers=headers,
        verify=False  # Disable SSL verification if needed
    )

    virtual_servers_response.raise_for_status()

    return virtual_servers_response.json()

def process_virtual_servers(virtual_servers_data):
    """
    Processes the virtual servers data and returns a list of VIP details.

    Args:
        virtual_servers_data (dict): The JSON response containing the virtual servers data.

    Returns:
        list: A list of dictionaries containing the VIP details with 'name' and 'address' keys.
    """
    vip_list = []

    for virtual_server in virtual_servers_data["items"]:
        vip_name = virtual_server["name"]
        vip_address = virtual_server["destination"].replace("/Common/", "")

        vip_list.append({
            "name": vip_name,
            "address": vip_address
        })

    return vip_list

def save_vip_details_to_file(vip_list, file_path):
    """
    Saves the VIP details to a text file.

    Args:
        vip_list (list): A list of dictionaries containing the VIP details.
        file_path (str): The path to the file where the VIP details will be saved.
    """
    with open(file_path, "w") as file:
        for vip in vip_list:
            file.write("Name: {}\n".format(vip["name"]))
            file.write("Address: {}\n".format(vip["address"]))
            file.write("\n")

    print("VIP details saved to '{}'.".format(file_path))

def main():
    """
    Main function to execute the steps for retrieving and saving VIP details.
    """
    username = "admin"
    password = "password"
    file_path = "vip-details.txt"

    try:
        auth_token = authenticate(username, password)
        virtual_servers_data = retrieve_virtual_servers(auth_token)
        vip_list = process_virtual_servers(virtual_servers_data)
        save_vip_details_to_file(vip_list, file_path)
    except requests.exceptions.RequestException as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    main()
