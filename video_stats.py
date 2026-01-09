import requests
import json
from datetime import date

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
            #ßprint(f"Nombre de vidéos récupérées dans cette page :  {len(data.get('items',[]))}")

            for item in data.get('items',[]):
                video_id = item['contentDetails']['videoId']
                video_ids.append(video_id)

        #Pagination
            pageToken = data.get('nextPageToken')
            if not pageToken:
                break

        #print("Nb total de viéos :",len(video_ids))
        return video_ids

#now any exception relating to requests will be set to the variable e
    except requests.exceptions.RequestException as e:
        print("Erreur lors de lq recupération des vidéos")
        raise e
    
def extract_video_data(video_Ids):
    extracted_data = []

    def batch_list(video_id_lst,batch_size):
        for video_id in range (0,len(video_id_lst),batch_size):
        #yield sert à produire des valeurs une par une, sans tout stocker en mémoire. 
        # Une fonction avec yield ne renvoie pas une liste Elle renvoie un générateur
            yield video_id_lst[video_id : video_id + batch_size]
    
    try:
        for batch in batch_list(video_ids,maxResults):
            videos_ids_lst=",".join(batch)

            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={videos_ids_lst}&maxResults=1&key={API_KEY}"

            #we use the get method to get the url
            response = requests.get(url)
            response.raise_for_status()
            #we cerate a new global variable data that create a json
            data = response.json()

            for item in data.get('items',[]): #if the specify kex doesn't exist, it will return and empty list
                video_id = item['id']
                snippet = item['snippet']
                contentDetails = item['contentDetails']
                statistics = item['statistics']

                video_data = {
                    "video_id" : video_id,
                    "title": snippet['title'],
                    "publishedAt":snippet['publishedAt'],
                    "duration":contentDetails['duration'],
                    #the next 3 don't always exist for a video, so we use the get method with a None value if not available
                    "viewCount":statistics.get('viewCount',None),
                    "likeCount":statistics.get('likeCount', None),
                    "commentCount":statistics.get('commentCount',None)
                    }
                
                extracted_data.append(video_data)

        return extracted_data
    
    except requests.exceptions.RequestException as e:
        print("Erreur lors de lq recupération des vraiables des videos")
        raise e

def save_to_json(extracted_data):
    file_path = f"data/{date.today()}.json"

    #we can use a content manager to organize the file  : with statement
    with open(file_path,"w", encoding="utf-8") as json_outfile:
        json.dump(extracted_data,json_outfile,indent=4,ensure_ascii=False)

if __name__ == "__main__":
    print("Début du script...")
    playlistId=get_playlist_id()
    video_ids=get_video_ids(playlistId)
    video_data = extract_video_data(video_ids)
    #print("Liste finale des Video IDs :",playlistId)  #we use print only for the purpose of the demonstration
    print("Liste finale des variables des Video IDs :",extract_video_data(video_ids))  #we use print only for the purpose of the demonstration
    save_to_json(video_data)
else:
    print("get_playlist_id won't be executed")   #if we run the script from another script