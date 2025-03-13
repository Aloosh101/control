
def get_channel_videos(api_key, channel_id):
    from googleapiclient.discovery import build


    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.search().list(
        part='snippet',
        channelId=channel_id,
        type='video',
        order='date',
        maxResults=9999
    )

    response = request.execute()
    videos = []

    while response:
        for item in response['items']:
            video_id = item['id']['videoId']
            video_title = item['snippet']['title']
            video_published_date = item['snippet']['publishedAt']
            video_link = f'https://www.youtube.com/watch?v={video_id}'
            videos.append((video_title, video_published_date, video_link))

        if 'nextPageToken' in response:
            request = youtube.search().list_next(request, response)
            response = request.execute()
        else:
            response = None

    return videos

if __name__ == '__main__':
    api_key = 'AIz'
    channel_id = ''
    videos = get_channel_videos(api_key, channel_id)
    print(len(videos))
