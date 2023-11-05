import pytube
import re

base_folder = '/home/Andrew/Videos/'

def is_link_valid(link):
  video_regex = r'(https?://)?(www\.)?youtube\.com/watch\?v=.*'
  short_regex = r'(https?://)?(www\.)?youtu\.be/.*'

  pattern = f"({'|'.join([video_regex, short_regex])})"

  if re.match(pattern, link):
    return True
  else:
    return False

while True:
    print("Enter YouTube URL, or press Enter to exit:")
    video_url = input()
    if video_url == '':
        break
    elif is_link_valid(video_url):
        print("Choose folder: 1) Code Videos, 2) Tech Videos, 3) Maker Videos, 4) General Videos:")
        destination_folder = int(input())
        youtube = pytube.YouTube(video_url)
        video = youtube.streams.first()
        if destination_folder == 1:
            video.download(base_folder + 'Code_Vids')
            print("Video saved to Code_Vids!")
        elif destination_folder == 2:
            video.download(base_folder + 'Tech_Vids')
            print("Video saved to Tech_Vids!")
        elif destination_folder == 3:
            video.download(base_folder + 'Maker_Vids')
            print("Video saved to Maker_Vids!")
        elif destination_folder == 4:
            video.download(base_folder + 'General_Vids')
            print("Video saved to General_Vids!")
        else:
            print("Invalid Choice...")
    else:
      print("Invalid YouTube link, try again")
print("Thank you for using YouTubeCopier! Shutting down...")
