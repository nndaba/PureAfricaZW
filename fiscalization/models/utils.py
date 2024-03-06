import requests


def get_details():
    url = 'http://154.119.80.13:3000/revmax/report'  # Replace with your URL
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()  # If the response is JSON data
        print(data)
    else:
        print('Request failed with status code:', response.status_code)
        
get_details()