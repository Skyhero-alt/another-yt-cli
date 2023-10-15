import requests
import re
import json
import sys
import subprocess
from lxml import etree
from bs4 import BeautifulSoup

# viraj edit
# from pytube import YouTube
# import vlc
# import time


def get_link(name, max_res=10):
    query = name.split()
    r = requests.get(
        'https://www.youtube.com/results?search_query=' + "+".join(query)).text

    print("Searching for " + name + "....\n")

    soup = BeautifulSoup(r, "lxml")

    script = soup.find_all("script")[35]

    json_text = re.search(
        "var ytInitialData = (.+)[,;]{1}", str(script)).group(1)
    json_data = json.loads(json_text)

    content = (
        json_data
        ['contents']['twoColumnSearchResultsRenderer']
        ['primaryContents']['sectionListRenderer']
        ['contents'][0]['itemSectionRenderer']
        ['contents']
    )

    links_and_titles = []
    for i in content:
        for key, val in i.items():
            if type(val) is dict:
                for k, v in val.items():
                    try:
                        if k == "videoId":
                            video_link = "https://www.youtube.com/watch?v=" + v

                        if k == "title":
                            video_title = v['runs'][0]['text']
                            links_and_titles.append([video_link, video_title])

                    except Exception as e:
                        pass

    return links_and_titles[:max_res]
    
def selc_video(links):
    """Select the link from list of youtube videos."""
    print("Choose a video to play: ")
    res = []
    for i, links in enumerate(links,1):
        print(f"{i}. {links[1]}")
        res.append(links[0])
        print()

        
    while True:
        try:
            num = int(input("Enter the number of the video link you want to play: "))
            if 1<=num<=len(res):
                return res[num-1]
            else:
                print("Index out of range.Enter in range of 1 to 10")
        except ValueError:
	        print("Invalid Input.Enter a numeric digit.")


def play(link):
    if str(type(link)) == "<class 'NoneType'>":
        print("An error occured!!!")
        return

    print("Trying to play: ", link) 
    subprocess.run(["mpv", "--ytdl-format=18", str(link)])
    

    print()


# MAIN PROGRAM starts here
if __name__ == "__main__":
  
    if len(sys.argv) > 1:
        url = " ".join(sys.argv[1:])
    else:
        url = input("Enter the video name you want to play: ")
    vids = get_link(url)
    if not vids:
        print("No video found.")
    else:
        sel_link = selc_video(vids)
        play(sel_link)
