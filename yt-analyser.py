import os
import json
import google_auth_oauthlib.flow 
import googleapiclient.discovery
import googleapiclient.errors
import csv
import time
import random
import datetime
from googleapiclient.errors import HttpError
import sys
import textwrap
from path_selection import *
from timestamp import *
from inputs_management import *
from search_properties import *
from comment_generator import *
from terminate import *
from gpt_paraphrase import *
#Determine the current path, date
timestamp_file = build_path()
current_date = datetime.date.today()

#If timestamp file exists, call read function
if os.path.isfile(timestamp_file):
    
    if read_timestamp(timestamp_file):
        flush_data()
        write_timestamp(timestamp_file)
        print("Data is removed, timestamp updated.")
        print()
        time.sleep(5)
    else:
         print("No updates needed.")
         print()
         time.sleep(5)
#If it doesn't, create it
else:
    write_timestamp(timestamp_file)
    print("Timestamp file is being created - don't delete it please.")
    print()
    time.sleep(5)

#Configure API properties
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = os.environ.get("JSON_FILE_YT")
print(client_secrets_file)
# Get credentials and create an API client
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
client_secrets_file, scopes)
credentials = flow.run_console()
youtube = googleapiclient.discovery.build(
api_service_name, api_version, credentials=credentials)

#Get user input
print()
choice = get_user_input()
parameters = set_properties(choice)
video_order = sort_videos(choice)
query, desired_sub_count, upper_limit = parameters
print()

#Initial values for some variables
search_counter = 0
display = True
comments = 0
search_request = True

#Perform multiple searches if necessary
for i in range(0,len(video_order)):
    search_counter = search_counter + 1
    
    #Search for channels
    request = youtube.search().list(
    part="snippet",
    maxResults=25,
    q=query,
    type="channel",
    order=video_order[i]
    )
    response = request.execute()

    #Display some info regarding current search
    print(f'Here comes {search_counter} search')
    print(f'Channels sorted by {video_order[i]}')
    print()
    
    #Extract channel data
    for item in response["items"]:
        id = (item["id"].get("channelId"))
        
        #Check if a record already exists in a file
        if check_record_exists(id, display):
            print("Record already exists - we're skipping it.")
            print()
            time.sleep(1)
            continue
        else:
            
            print("There's a new one, let me extract some details:")
            time.sleep(1)
            display = False
        
        #Extract channel data
        request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=id
        )
        response = request.execute()       
        
        #Determine sub count
        channel_data = response["items"][0]
        sub_count = int(channel_data["statistics"].get("subscriberCount"))
        
        if (desired_sub_count <= sub_count <= upper_limit if upper_limit else sub_count >= desired_sub_count):
        
            print(f'Channel ID: {id}')
            print(f'Subscriber count: {sub_count}')
        
        #Extract playlistID
            playlists = channel_data["contentDetails"].get("relatedPlaylists")
            playlist_id = playlists.get("uploads")

        #Store id and video count of each video
            videos = []    
            nextPageToken = None
            max_count_video = None
        
        #Extract playlist items 
            while True: 
                try:
                    request = youtube.playlistItems().list(
                    part="contentDetails",
                    playlistId=playlist_id,
                    maxResults = 50,
                    pageToken = nextPageToken
                    )
                    response_videos = request.execute()       
                    nextPageToken = response_videos.get("nextPageToken")
                    
                    videos_number = response_videos["pageInfo"].get("totalResults")
                    #print(response_videos)
                    print(videos_number)
                    
                    #Don't execute if there are more videos than X
                    if videos_number > 200:
                        break
                    
                    #Extract video details
                    for video in response_videos["items"]:
                        video_id = video["contentDetails"].get("videoId")
                        
                        request_video = youtube.videos().list(
                        part="snippet,contentDetails,statistics",
                        id=video_id
                        )
                        video_data = request_video.execute()
                        video_data = video_data["items"][0]
                        #print(video_data)
                          
                        view_count = video_data["statistics"].get("viewCount")
                        videos.append({video_id: view_count})
                        print(view_count)
                        print(videos)
    
                    if not nextPageToken:
                        
                        #Extract most viewed videoID
                        max_count = 0
                        for video in videos:
                            for id, count in video.items():
                                if int(count) > max_count:
                                    max_count = int(count)
                                    max_count_video = id    
                        
                        break
                
                except HttpError:
                    print("Playlist details can't be extracted - the channel may feature more of them.")
                    print()
                    time.sleep(2)
                    continue
            
            if max_count_video is None:       
        
        #Extract most recent videoID
                video_data = response_videos["items"][0]
                video_id = video_data["contentDetails"].get("videoId")
                publish_date = video_data["contentDetails"].get("videoPublishedAt")
                
                print(publish_date)
                print(publish_date.day)
                print(f'Most recent video: https://www.youtube.com/watch?v={video_id}')
            else:
                print(f'Max view count: {max_count}')
                video_id = max_count_video
                print(f'Most viewed video: https://www.youtube.com/watch?v={video_id}') 
            
            #Call the function which generates comments#
            content_comment = generate_comment()
            print("Comment below that video:")
            print(f'{content_comment}')
            
            gpt_content_comment = paraphrase(content_comment)
            print("Refined by Chat GPT:")
            print(f'{gpt_content_comment}')
        #     #Post a comment
        #     try:
        #         request = youtube.commentThreads().insert(
        #         part="snippet",
        #         body={
        #         "snippet": {
        #         "videoId": video_id,
        #         "topLevelComment": {
        #         "snippet": {
        #         "textOriginal": content_comment
        #         }
        #         }
        #         }
        #         }
        #         )
        #         response = request.execute()
        
        # #Move on to the next one if comments are disabled, or a video turns out to be a live
        #     except HttpError:
                
        #         print("Either comments are disabled or we stumble upon a live.")
        #         print()
        #         time.sleep(2)
        #         continue
            
            #Display the time to wait, how many comments were posted, wait
            comments = comments + 1
            interval = random.uniform(180,720)
            
            print(f'{comments} comments posted')
            print(f'We need to wait: {round(interval)} seconds.')
            print()
            time.sleep(interval)
            
            #Write the data to the CSV file
            with open("SUBS.csv", 'a', newline='', encoding='utf-8') as file:
                writer =csv.writer(file, delimiter=';', quotechar='"')
                writer.writerow([id, sub_count, current_date, choice])
            
        else:
            print("The channel didn't meet the criteria:")
            print(f'Subscriber count: {sub_count}')
            print()
            time.sleep(1)
        
        #Break if 10 comments were posted - maximum in one sitting
        if comments == 10:
            search_request = False
            break

    #Don't request another search
    if search_request == False:
        break

#Display results
print("Comments posted:", comments)

if comments < 10:
    print()
    print("Unfortunately we didn't find enough channels :(")

#Wait for the user to close the program
terminate()