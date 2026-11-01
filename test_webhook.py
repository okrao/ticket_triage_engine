import requests

# Replace this with your exact copied Test URL
WEBHOOK_URL = "http://localhost:5678/webhook-test/2eed5566-04c3-43bb-937d-d8d4d719051d"

# The mock customer ticket data
ticket_data = {
    "customer_name": "Otis Lee",
    "issue_description": "My Flash Furniture desk arrived with a massive scratch on the side.",
    "brand": "Flash Furniture"
}

# Send the POST request to n8n
response = requests.post(WEBHOOK_URL, json=ticket_data)

print(f"Sent! Status Code: {response.status_code}")