import requests
import json


# Define the base URL of your Flask application
base_url = 'http://localhost:5000'


"""
    Print the response status code and content.
""" 
def print_response(response: json = {}):
    if response:
        print('Response Status Code:', response.status_code)
        try:
            data = response.json()
            print(data)
        except Exception as e:        
            for v in response:
                print(v)
    else:
        print("Didn't get a response...")


def check_create_webserver(data: json = None):
    # Define the data for creating a new Webserver
    data = data or {'name': 'Example Webserver', 'http_url': 'https://example.com'}

    # Send a POST request to the create_webserver endpoint
    response = requests.post(f'{base_url}/webservers', json=data)

    print_response(response)



def check_list_webservers():
    # Send a GET request to the list_webservers endpoint
    response = requests.get(f'{base_url}/webservers')
    
    print_response(response)


def get_specific_webserver(id: int = 1):
    # Send a GET request to retrieve the web server
    response = requests.get(f'{base_url}/webservers/{id}')
    
    print_response(response)

def get_specific_history(id: int = 1):
    # Send a GET request to retrieve the web server
    response = requests.get(f'{base_url}/history/{id}')
    
    print_response(response)


def check_delete_webserver(id: int = 1):
    
    response = requests.delete(f'{base_url}/webservers/{id}')

    print_response(response)


def check_update_specific_webserver(id: int = 1, name: str = None, http_url: str = None):
    
    update_data = {'name': name, 'http_url': http_url}
    print(f"update_data = {update_data}")
    
    response = requests.put(f'{base_url}/webservers/{id}', json=update_data)

    print_response(response)


""" =========================================================
    TODO - Check load, error handling ...
    =========================================================
"""

if __name__ == '__main__':
    
    # ======================== TODO - Check giving wrong input (already exist ...) ========================
    
    # check_create_webserver({"name": "Youtube", "http_url": "https://www.youtube.com/"})
    # check_create_webserver({"name": "Google", "http_url": "https://www.google.com/"})
    # check_create_webserver({"name": "stackoverflow", "http_url": "https://stackoverflow.com/"})
    # check_list_webservers()
    
    # get_specific_webserver(id=20)
    
    # get_specific_history(id=20)
    
    # # # # # Doesn't work yet
    # check_update_specific_webserver(id=20,name="Test")
    
    
    # check_delete_webserver(id=18)
    
    check_list_webservers()
    
    print(-3 % 4)
    
    
    
    