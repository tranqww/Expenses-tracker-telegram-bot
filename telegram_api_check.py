import requests

response = requests.get("https://api.telegram.org")
if response.status_code == 200:
    print(f"Server is working: {response.status_code}")
elif response.status_code == 404:
    print(f"Server not respond: {response.status_code}")
else:
    print(f"This link doesn't exist: {response.status_code}")

    