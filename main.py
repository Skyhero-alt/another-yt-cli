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


def get_link(name,max_res = 10):
    query = name.split()
    r = requests.get(
        'https://www.youtube.com/results?search_query=' + "+".join(query)).text

    # html = r.content
    # print('https://www.youtube.com/results?search_query=' + "+".join(name))
    print("Searching for "+name+"....\n")

    soup = BeautifulSoup(r, "lxml")

    script = soup.find_all("script")[35]

    json_text = re.search(
        "var ytInitialData = (.+)[,;]{1}", str(script)).group(1)
    json_data = json.loads(json_text)

    # ME TESTING :)
    # with open("file.html", "w", encoding='utf-8') as output:
    #     output.write(soup.prettify())

    # with open("script.txt", "w", encoding="utf-8") as output:
    #     output.write(json_text)

    content = (
        json_data
        ['contents']['twoColumnSearchResultsRenderer']
        ['primaryContents']['sectionListRenderer']
        ['contents'][0]['itemSectionRenderer']
        ['contents']
    )

    links = []
    for i in content:
        for key, val in i.items():
            if type(val) is dict:
                for k, v in val.items():
                    try:
                        if k == "videoId":
                            video_link = "https://www.youtube.com/watch?v=" + v
                            links.append(video_link)
                            # return "https://www.youtube.com/watch?v="+v
                        # if k =="title":
                            # print(v["runs"][0]["text"])
                    except Exception as e:
                        print("An error occured:", e)
    
    return links[:max_res]

    # dom = etree.HTML(str(soup))
    # print(dom.xpath('//*[@id="video-title"]')[0].text)
    # for i in res:
    # 	print(i)
        # print(i.a['id'])
        # if i.a['id'] == "video-title":
        # 	print(i)

# get_link()

    
def selc_video(links):
    """Select the link from list of youtube videos."""
    print("Choose a video to play: ")
    for i, links in enumerate(links,1):
        print(f"{i}. {links}")
        
    while True:
        try:
            num = int(input("Enter the number of the video link you want to play: "))
            if 1<=num<=len(links):
                return links[num-1]
            else:
                print("Index out of range.Enter in range of 1 to 10")
        except ValueError:
	        print("Invalid Input.Enter a numeric digit.")
        
# def get_video_name():
#     name = input("Enter the video name you want to play: ")
#     return name


def play(link):
    if str(type(link)) == "<class 'NoneType'>":
        print("An error occured!!!")
        return

    print("Trying to play: ", link) 
    mpv_path = r"C:\\Users\\Viraj Sawant\\Downloads\\bootstrapper\\mpv.exe"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    try:
        subprocess.run([mpv_path, "--ytdl-format=18", "--user-agent=" + user_agent, str(link)])
    except subprocess.CalledProcessError as e:
        print("Error occurred while playing the video:", e)

    print()


# MAIN PROGRAM starts here
if __name__ == "__main__":
    # if (len(sys.argv) > 1):
    #     res = get_link(" ".join(sys.argv[1:]))
    #     play(res)
    # else:
    #     n = get_video_name()
    #     res = get_link(n)
    #     play(res)
    if len(sys.argv) > 1:
        url = " ".join(sys.argv[1:])
    else:
        url = input("Enter the video name you want to play: ")
    links = get_link(url)
    if not links:
        print("No video found.")
    else:
        sel_link = selc_video(links)
        play(sel_link)
