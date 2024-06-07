import requests

# List of song URLs
song_urls = [
    "https://songbase.life/6200",
    # Add more URLs as needed
]

def fetch_song_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        return response.text
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    return None

def main():
    for url in song_urls:
        print(f"Fetching data from {url}")
        song_data = fetch_song_data(url)
        if song_data:
            print(f"Data fetched from {url}:")
            print(song_data)  # Print the first 500 characters of the response for preview
        else:
            print(f"Failed to fetch data from {url}")

if __name__ == "__main__":
    main()
