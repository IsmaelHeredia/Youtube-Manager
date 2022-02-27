#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Youtube Manager 1.1
# Written by Ismael Heredia
# Date : 01/01/2022

import argparse, os

from functions import functions
from modules import youtubeManager

def main():

    parser = argparse.ArgumentParser(add_help=False)   
    
    parser.add_argument("-download-video", dest="download_video", help="Enter link to download in MP4")
    parser.add_argument("-download-videos", dest="download_videos", help="Enter file with links to download in MP4")
    parser.add_argument("-download-song", dest="download_song", help="Enter link to download and convert in MP3")
    parser.add_argument("-download-songs", dest="download_songs", help="Enter file with links for download to finally convert in MP3")
    parser.add_argument("-findsong-and-download", dest="findsong_and_download", help="Enter name to find in google and download to finally convert in MP3")
    parser.add_argument("-findsongs-and-download", dest="findsongs_and_download", help="Enter file with names to find in google and download to finally convert in MP3")
    parser.add_argument("-download-playlist", dest="download_playlist", help="Enter playlists link to download and convert in MP3")
    parser.add_argument("-download-playlists", dest="download_playlists", help="Enter file with playlists to download and convert in MP3")

    results = parser.parse_args()

    download_video = results.download_video
    download_videos = results.download_videos
    download_song = results.download_song
    download_songs = results.download_songs
    findsong_and_download = results.findsong_and_download
    findsongs_and_download = results.findsongs_and_download
    download_playlist = results.download_playlist
    download_playlists = results.download_playlists

    function = functions.Functions()

    if download_video != None:
        ym = youtubeManager.youtubeManager()
        ym.download_video(download_video,True)
    elif download_videos != None:
        ym = youtubeManager.youtubeManager()
        ym.download_videos(download_videos,True)
    elif download_song != None:
        ym = youtubeManager.youtubeManager()
        filename = ym.download_video(download_song,False)
        ym.convert_to_mp3(ym.TEMP_VIDEO,filename)
    elif download_songs != None:
        ym = youtubeManager.youtubeManager()
        ym.download_songs(download_songs)
    elif findsong_and_download != None:
        ym = youtubeManager.youtubeManager()
        ym.findsong_and_download(findsong_and_download)
    elif findsongs_and_download != None:
        ym = youtubeManager.youtubeManager()
        ym.findsongs_and_download(findsongs_and_download)
    elif download_playlist != None:
        ym = youtubeManager.youtubeManager()
        ym.download_playlist_and_convert(download_playlist)
    elif download_playlists != None:
        ym = youtubeManager.youtubeManager()
        ym.download_playlists_and_convert(download_playlists)
    else:
        parser.print_help()
        
    ym_clean = youtubeManager.youtubeManager()
    ym_clean.clear_temp()

if __name__ == "__main__":
    main()