import os
import pytube
import re
import json

base_folder = '/media/seagate/Jellyfin/'

def is_link_valid(link):
    playlist_regex = r'(https?://)?(www\.)?youtube\.com/playlist\?list=.*'
    video_regex = r'(https?://)?(www\.)?youtube\.com/watch\?v=.*'
    short_regex = r'(https?://)?(www\.)?youtu\.be/.*'

    pattern = f"({'|'.join([playlist_regex, video_regex, short_regex])})"

    if re.match(pattern, link):
        return True
    else:
        return False

def is_video_downloaded(video_id, destination_folder):
    file_path = os.path.join(base_folder, destination_folder, f"{video_id}.mp4")
    return os.path.exists(file_path)

def download_video(video_url, destination_folder):
    youtube = pytube.YouTube(video_url)
    video_id = youtube.video_id
    if not is_video_downloaded(video_id, destination_folder):
        streams = youtube.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
        highest_resolution_stream = streams.first()
        highest_resolution_stream.download(base_folder + destination_folder)
        print(f"Video saved to {destination_folder}!")
    else:
        print("Video already downloaded, skipping...")

def download_playlist(playlist_url, destination_folder):
    playlist = pytube.Playlist(playlist_url)
    playlist_name = playlist.title
    playlist_folder = os.path.join(base_folder, destination_folder, playlist_name)
    os.makedirs(playlist_folder, exist_ok=True)
    for video_url in playlist.video_urls:
        download_video(video_url, os.path.join(destination_folder, playlist_name))

with open('urls.json') as file:
    data = json.load(file)

for group, urls in data.items():
    print(f"Processing videos for {group}:")
    for url in urls:
        if is_link_valid(url):
            print(f"Processing {url}...")
            if 'playlist' in url:
                download_playlist(url, group)
            else:
                download_video(url, group)
        else:
            print(f"Invalid YouTube link for {url}, skipping...")

print("Thank you for using YouTubeCopier! Shutting down...")
