import requests

url = "https://api.themoviedb.org/3/movie/550?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    print(response.json())
except requests.exceptions.RequestException as e:
    print(f"Connection error: {e}")

