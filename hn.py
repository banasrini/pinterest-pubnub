from BeautifulSoup import BeautifulSoup, SoupStrainer
import feedparser
from Pubnub import Pubnub
from cover import pinterest
import time
from argparse import ArgumentParser
import sys

pinstream = pinterest(publish_key = 'pub-c-6dbe7bfd-6408-430a-add4-85cdfe856b47', subscribe_key = 'sub-c-2a73818c-d2d3-11e3-9244-02ee2ddab7fe', uuid = 'bana')
channel = 'button-reply'

statusarray = []

def init_parse(rss):
    feedurl = feedparser.parse(rss)
    for entry in feedurl.entries:
        statusarray.append(entry)
    return feedurl

result = []

def extract_img(statusarray):
    for r in statusarray:
        statusupdate = r.summary_detail.value
        soup = BeautifulSoup(statusupdate)
        for e in r:
            post = {}
            post["imgs"] = (soup.find("img")["src"])
            post["links"] = (soup.find("a")["href"])
            result.append(post)
    new_result = []
    for x in result:
        if x not in new_result:
            new_result.append(x)

    for message in new_result:
        pinstream.send(channel, message)
        print message
        print("\n")


'''def check_for_change(mode, pin, rss):
    new_pin = init_parse(rss)
    if mode == "entire":
        if str(new_pin) != str(pin):
            init_parse(new_pin)
            extract_img(statusarray)
    elif mode == "new":
        new_pin = extract_img(new_pin)
        pin = extract_img(pin)
        hn_titles = []
        message = []
        for new_img in new_hn:
            if new_img["title"] not in hn_titles:
                message.append(new_title)
        return message
    else:
        return None
'''

if __name__ == "__main__":
    parser = ArgumentParser(description="Options to parse RSS Feed")
    parser.add_argument("-r", "--rsslink", dest="rss_link", type=str, default="http://pinterest.com/janew/feed.rss", help="This is a link to the rss feed desired to scrape.")
    

    
    argv = sys.argv[1:]
    
    try:
        argp = parser.parse_args(argv)
    except SystemExit as ex:
        print("Eception when parsing args because of => " + str(ex))
        sys.exit()
    
    try:
        rss = argp.rss_link
    except Exception as ex:
        print("Something went wrong because of => " + str(ex))

while True:
    
    init_parse(rss)
    extract_img(statusarray)












