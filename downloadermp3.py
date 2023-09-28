from pytube import YouTube
from moviepy.editor import VideoFileClip
import os

def DownloadAndConvertToMP3(link, output_directory, title):
    try:
        youtubeObject = YouTube(link)
        video_stream = youtubeObject.streams.get_highest_resolution()
        video_path = video_stream.download()

        video_clip = VideoFileClip(video_path)
        mp3_path = os.path.join(output_directory, title + '.mp3')
        video_clip.audio.write_audiofile(mp3_path)
        video_clip.close()

        os.remove(video_path)  # Remove the downloaded video file

        print("Download and conversion to MP3 completed successfully")
    except Exception as e:
        print("An error has occurred:", str(e))

if __name__ == "__main__":
    link = input("Enter the YouTube video URL: ")
    output_directory = os.path.expanduser('~/Musique')  # Expand ~ to user's home directory
    DownloadAndConvertToMP3(link, output_directory)

