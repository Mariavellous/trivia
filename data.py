# requests module allows you to send HTTP requests. Install requests module.
import requests


parameters = {
    "amount": 1,
    # Category is Entertainment: Film
    "category": 11,
    "type": "multiple",
}

# make a get request to API endpoint including parameters
response = requests.get("https://opentdb.com/api.php", params=parameters)
# check any error status
response.raise_for_status()
# retrieve the data in json format
data = response.json()
print(data)

