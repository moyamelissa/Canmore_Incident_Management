import requests

url = "http://127.0.0.1:5000/api/incidents"
data = {
	"type": "Fire",
	"description": "Test fire incident",
	"latitude": 51.089,
	"longitude": -115.359,
	"timestamp": "2026-01-24T12:00:00"
}

response = requests.post(url, json=data)
print(response.status_code)
print(response.json())
