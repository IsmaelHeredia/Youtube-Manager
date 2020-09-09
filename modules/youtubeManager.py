#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pip install youtube-dl
# pip install --upgrade youtube-dl
# Clean cache : youtube-dl --rm-cache-dir
# Date : 07/09/2020

from functions import functions
from modules import googleSearch

import os,re,time
import youtube_dl
import moviepy.editor as mp
import urllib.request,urllib.parse
from requests.utils import quote
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class youtubeManager(object):

    def __init__(self):
        self.functions = functions.Functions()
        self.gs = googleSearch.googleSearch()

        self.directory = os.path.join(os.path.expanduser("~"), "Music") + "\\Youtube_downloads"
        self.directory_videos = os.path.join(os.path.expanduser("~"), "Videos") + "\\Youtube_downloads"
        self.directory_original = self.directory

        self.TEMP_VIDEO = self.directory + "\\temp_video.mp4"

        self.ydl_opts_videos = {
            "format": "mp4",
            "outtmpl": self.TEMP_VIDEO,
            "ignoreerrors": True,
            "cachedir": False
        }

        self.ydl_opts_playlists = {
            "format": "mp4",
            "ignoreerrors": True,
            "quiet": True,
            "cachedir": False
        }

        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        if not os.path.exists(self.directory_videos):
            os.makedirs(self.directory_videos)

        self.clear_temp()

    def clear_temp(self):
        temp_songs = self.directory  + "\\temp_video.mp4"
        temp_videos = self.directory_videos + "\\temp_video.mp4"
        if os.path.isfile(temp_songs):
            os.remove(temp_songs)
        if os.path.isfile(temp_videos):
            os.remove(temp_videos)

    def download_video(self,video,only_video=False):
        if os.path.isfile(self.TEMP_VIDEO):
            os.remove(self.TEMP_VIDEO)
        print("\n[+] Downloading video %s ...\n" % (video,))
        filename = ""
        try:
            with youtube_dl.YoutubeDL(self.ydl_opts_videos) as ydl:
                info_dict = ydl.extract_info(video, download=False)
                video_title = info_dict.get("title", None)
                print("\n[+] Title : %s\n" % (video_title,))
                video_title = re.sub(r'[\\/*?:"<>|]',"",video_title)
                filename = self.directory + "\\" + video_title + ".mp4"
                ydl.download([video])
                if only_video:
                    video_path = self.directory_videos + "\\" + video_title + ".mp4"
                    if not os.path.isfile(video_path):
                        os.rename(self.TEMP_VIDEO,video_path)
                    print("\n[!] Saved in %s" % (video_path,))
                return filename
        except:
            pass
        if not os.path.isfile(filename):
            print("\n[-] Error downloading video")

    def download_videos(self,listvideo,only_video=False):
        print("\n[+] Opening file %s ..." % (listvideo,))
        if os.path.exists(listvideo): 
            with open(listvideo) as videos:
                for video in videos:
                    self.download_video(video,only_video)
                    time.sleep(5)
        else:
            print("\n[-] File not found")

    def convert_to_mp3(self,video,name=""):
        if os.path.isfile(video):
            print("\n[+] Converting video %s to mp3 ...\n" % (video,))
            filename = name
            pre, ext = os.path.splitext(filename)
            filename = pre + ".mp3"
            try:
                clip = mp.VideoFileClip(video)
                clip = clip.subclip(0,clip.duration)
                clip.audio.write_audiofile(filename)
                self.close_clip(clip)
                print("\n[!] Saved in %s" % (filename,))
                return filename
            except:
                print("\n[-] Error converting mp3")
                pass

    def download_songs(self,listsong):
        print("\n[+] Opening file %s ..." % (listsong,))
        if os.path.exists(listsong): 
            with open(listsong) as links:
                for link in links:
                    filename = self.download_video(link,False)
                    self.convert_to_mp3(self.TEMP_VIDEO,filename)
                    time.sleep(5)
        else:
            print("\n[-] File not found")

    def findsong_and_download(self,name):
        name = name.strip("\n")
        print("\n[+] Searching song %s ..." % (name,))
        string = quote("site:https://www.youtube.com "+name, safe="")
        link = self.gs.send_first_result(string)
        if link:
            filename = self.download_video(link,False)
            mp3_file = self.convert_to_mp3(self.TEMP_VIDEO,filename)
            return mp3_file
        else:
            print("\n[-] Song not found")

    def findsongs_and_download(self,listsong):
        print("\n[+] Opening file %s ..." % (listsong,))
        if os.path.exists(listsong): 
            with open(listsong) as names:
                for name in names:
                    self.findsong_and_download(name)
                    time.sleep(5)
        else:
            print("\n[-] File not found")

    def download_playlist_and_convert(self,link):
        print("\n[+] Reading playlist %s ..." % (link,))

        try:
            with youtube_dl.YoutubeDL(self.ydl_opts_playlists) as ydl:
                playlist_dict = ydl.extract_info(link, download=False)
                title = playlist_dict.get("title",None)
                title = title.replace(":","")

                newdir = self.directory_original + "\\" + title

                if not os.path.exists(newdir):
                    os.makedirs(newdir)

                for video in playlist_dict["entries"]:
                    if video:
                        id_video = video.get("id")
                        title = video.get("title")
                        link = "https://www.youtube.com/watch?v=" + id_video
                        print("\n[+] Video found : %s" % (link,))
                        filename = self.download_video(link,False)
                        only_name = os.path.basename(filename)
                        savefile = newdir + "\\" + only_name 
                        self.convert_to_mp3(self.TEMP_VIDEO,savefile)
                        time.sleep(5)
        except:
            print("\n[-] Error download playlist")
            pass

    def download_playlists_and_convert(self,listsong):
        print("\n[+] Opening file %s ..." % (listsong,))
        if os.path.exists(listsong): 
            with open(listsong) as links:
                for link in links:
                    print("\n[+] Reading playlist %s ..." % (link,))
                    try:
                        with youtube_dl.YoutubeDL(self.ydl_opts_playlists) as ydl:
                            playlist_dict = ydl.extract_info(link, download=False)
                            title = playlist_dict.get("title",None)
                            title = title.replace(":","")
                            newdir = self.directory_original + "\\" + title

                            if not os.path.exists(newdir):
                                os.makedirs(newdir)

                            for video in playlist_dict["entries"]:
                                if video:
                                    id_video = video.get("id")
                                    title = video.get("title")
                                    link = "https://www.youtube.com/watch?v=" + id_video
                                    print("\n[+] Video found : %s" % (link,))
                                    filename = self.download_video(link,False)
                                    only_name = os.path.basename(filename)
                                    savefile = newdir + "\\" + only_name 
                                    self.convert_to_mp3(self.TEMP_VIDEO,savefile)
                                    time.sleep(5)
                    except:
                        print("\n[-] Error download playlist")
                        pass
        else:
            print("\n[-] File not found")

    def close_clip(self,video_clip):
        try:
            video_clip.reader.close()
            del video_clip.reader
            if video_clip.audio is not None:
                video_clip.audio.reader.close_proc()
                del video_clip.audio
            del video_clip
        except Exception:
            pass