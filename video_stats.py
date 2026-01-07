import requests
import json

#There are multiple ways of handling sensitive information, but the .env provides a simple and effective way of doing this
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

#we set a global variable 
API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = "MrBeast"
maxResults=50

def get_playlist_id():

    try :

        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"

        #we use the get method to get the url
        response = requests.get(url)

        response.raise_for_status()

        #we cerate a new global variable data that create a json
        data = response.json()

        #we use the json library to parse the json with a specific indentation
        #print(json.dumps(data,indent=4))

        #we can change the root with the data variale

        channel_items=data["items"][0]

        channel_playlistId= channel_items["contentDetails"]["relatedPlaylists"]["uploads"]

        #print("On a extrait la playlistId :"+ channel_playlistId)

        return channel_playlistId
    
    #now any exception relating to requests will be set to the variable e
    except requests.exceptions.RequestException as e:
        raise e

def get_video_ids(playlistId):
    #get qll video IDs from a playlist

    video_ids = []
    pageToken = None
    
    base_url = (
        f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlistId}&key={API_KEY}"
        )
    
    try:
#we define a condition in which for the first iteration will be false with regards to the pageToken variable, since it’s initially set to None.

        while True:
            url=base_url
                    
            if pageToken:
                url += f"&pageToken={pageToken}"

            #we use the get method to get the url
            response = requests.get(url)
            response.raise_for_status()
            #we cerate a new global variable data that create a json
            data = response.json()

            #print pour suivre le nb de vidéos récupérées
            print(f"Nombre de vidéos récupérées dans cette page :  {len(data.get('items',[]))}")

            for item in data.get('items',[]):
                video_id = item['contentDetails']['videoId']
                video_ids.append(video_id)

        #Pagination
            pageToken = data.get('nextPageToken')
            if not pageToken:
                break

        print("Nb total de viéos :",len(video_ids))
        return video_ids

#now any exception relating to requests will be set to the variable e
    except requests.exceptions.RequestException as e:
        print("Erreur lors de lq recupération des vidéos")
        raise e


if __name__ == "__main__":
    print("Début du script...")
    playlistId=get_playlist_id()
    print("Liste finale des Video IDs :",get_video_ids(playlistId))  #we use print only for the purpose of the demonstration

else:
    print("get_playlist_id won't be executed")   #if we run the script from another script