import requests
import time
import logging

# Set up logging for better error tracking
logging.basicConfig(level=logging.INFO)

url = "https://random-data-api.com/api/v2/credit_cards"

while True:
    try:
        # Sending a GET request to fetch data from the API
        response = requests.get(url)
        
        if response.status_code == 200:
            # If the response is successful, print the data
            logging.info("Data fetched successfully.")
            data = response.json()
            print(data)  # You can process the data here, if needed
        else:
            logging.error(f"Error fetching data: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        # Handle any request-related errors
        logging.error(f"Request failed: {e}")
    
    # Sleep for 5 seconds before the next request
    time.sleep(5)
