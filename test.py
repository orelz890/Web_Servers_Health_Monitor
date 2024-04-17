import requests
import json

# Define the base URL of your Flask application
base_url = 'http://localhost:5000'  # Update the URL as needed


"""
    Print the response status code and content.
""" 
def print_response(response: json = None):
    if response:
        print('Response Status Code:', response.status_code)
        print('Response Content:', response.json())
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


if __name__ == '__main__':
    
    # check_create_webserver()
    check_list_webservers()
    
    