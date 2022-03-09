#Dacast API - Get all video information script

This is a python script that calls the Dacast API, downloading video information to a csv file.

The API key needs to be stored in a .env file within the folder under the variable "apiKey" to work.

This was written for the WBS account, iterable ranges will need to be updated for use elsewhere.

video information collected:
title
ID
duration
filename
password (if any)
video height and width
http link to the posterframe
http link to the video (it says share code but it's not an embed code)
http link to the subtitle file (if it has them)
the folder location on dacast (also read: category)
