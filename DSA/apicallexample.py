import requests
def make_api_call(url,userId):
    try:
        headers = {
            'Content-Type': 'application/json',
        }
        params = {
            'id': userId
        }
        response = requests.get(url, 
                            headers=headers,
                            params=params
                            )
        print(response.url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data =  response.json()  # Return the JSON response if successful
        print(data)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        
url = "https://jsonplaceholder.typicode.com/users"
userId = 1
make_api_call(url, userId)