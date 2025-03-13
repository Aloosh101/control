import requests
import os
import googleapiclient.discovery

def get_channel_info(api_key, channel_id):
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)
    request = youtube.channels().list(part='snippet', id=channel_id)
    response = request.execute()

    if 'items' in response:
        channel_name = response['items'][0]['snippet']['title']
    else:
        print(f"No channel found with ID: {channel_id}")
        channel_name = None

    return channel_name

def get_all_videos(api_key, channel_id):
    base_url = "https://www.googleapis.com/youtube/v3/search"
    videos = []
    page_token = None

    while True:
        params = {
            "part": "snippet",
            "channelId": channel_id,
            "type": "video",
            "key": api_key,
            "maxResults": 50,
            "pageToken": page_token
        }
        response = requests.get(base_url, params=params)
        data = response.json()
        videos.extend(data['items'])

        if 'nextPageToken' in data:
            page_token = data['nextPageToken']
        else:
            break

    return videos


def main():
    api_key = 'api_key'
    channel_id = 'token'
    channel_name = get_channel_info(api_key, channel_id)
    print(channel_name)
    videos = get_all_videos(api_key, channel_id)
    print(f"Total Videos: {len(videos)}")
if __name__ == '__main__':
    main()



 