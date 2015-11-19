import requests
import urllib
from bs4 import BeautifulSoup as bs4

SMBC = "http://www.smbc-comics.com/"
SMBC_COMIC_URL = "http://www.smbc-comics.com/index.php?id="
SMBC_ARCHIVE_URL = "http://www.smbc-comics.com/archives.php"

comic_dict = {}

def get_comic_num(comic_num, red_button = True):
    page = requests.get(SMBC_COMIC_URL + str(comic_num))

    if page.status_code == 200:

        comic = bs4(page.content, "html.parser")

        data = comic.find("div", {"id":"comicbody"}).find("img")

        comic_title = data.get("title")
    
        comic_url_raw = data.get("src")
        comic_url_index = comic_url_raw.rfind("comics")
        comic_url = comic_url_raw[comic_url_index:]
    
        comic_ext = comic_url[comic_url.rfind('.'):]

        urllib.urlretrieve(SMBC + comic_url, str(comic_num) + comic_ext)

        if red_button:
            after_comic_raw = comic.find("div", {"id":"aftercomic"})
            
            if after_comic_raw:
                after_comic = after_comic_raw.find("img")
            
                after_comic_url = after_comic.get("src")
                after_comic_ext = after_comic_url[after_comic_url.rfind("."):]
    
                urllib.urlretrieve(after_comic_url, str(comic_num) + "_after" + after_comic_ext)
            else:
                print "No red button for this comic"

def update_archive():
    page = requests.get(SMBC_ARCHIVE_URL)
    archive = bs4(page.content, "html.parser")
    comic_list = archive.find("select", {"name":"comic"}).find_all("option")

    for comic in comic_list:
        comic_num = comic.get("value")
    
        if len(comic_num) > 0:
        
            comic_raw = comic.contents[0].split(" - ")
            comic_date = comic_raw[0]
            comic_title = comic_raw[1]

            comic_dict[comic_num] = {"date": comic_date,
                                     "title": comic_title}
        

update_archive()            

comic_ints = map(int, comic_dict.keys())

comic_ints.sort()

for i in comic_ints:
    print "Getting comic {i}".format(i=i)
    get_comic_num(i, red_button = False)
