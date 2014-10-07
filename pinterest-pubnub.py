from Pubnub import Pubnub
from BeautifulSoup import BeautifulSoup, SoupStrainer
import feedparser
import time
from argparse import ArgumentParser
import sys



class pinterest(object):
    def __init__(self, publish_key,
                 subscribe_key):
        
        self.publish_key = publish_key
        self.subscribe_key = subscribe_key
        self.pubnub = Pubnub( 'pub-c-6f928209-b8a8-4131-9749-7470ead38747', 'sub-c-6d212f32-404e-11e4-a498-02ee2ddab7fe', None, False)
    
    
    
    def send(self, channel, message):
        # Sending message on the channel
        self.pubnub.publish({
                            'channel' : channel,
                            'message' : message})



PUBKEY = "pub-c-6dbe7bfd-6408-430a-add4-85cdfe856b47"
SUBKEY = "sub-c-2a73818c-d2d3-11e3-9244-02ee2ddab7fe"
CHANNEL = "pubnub-pinterest"

pinstream = pinterest(publish_key = PUBKEY, subscribe_key = SUBKEY)


statusarray = []
result = []
new_result = []

def init_parse(rss):
    feedurl = feedparser.parse(rss)
    for entry in feedurl.entries:
        statusarray.append(entry)
    return feedurl

def extract_img(statusarray):
    for r in statusarray:
        statusupdate = r.summary_detail.value
        soup = BeautifulSoup(statusupdate)
        for e in r:
            post = {}
            post["imgs"] = (soup.find("img")["src"])
            post["links"] = (soup.find("a")["href"])
            result.append(post)

    for x in result:
        if x not in new_result:
            new_result.append(x)

if __name__ == "__main__":
    parser = ArgumentParser(description="Options to parse RSS Feed")
    parser.add_argument("-r", "--rsslink", dest="rss_link", type=str, default="http://www.pinterest.com/caseyk/feed.rss", help="This is a link to the rss feed desired to scrape.")
    

    
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
    pn = Pubnub(PUBKEY, SUBKEY)

    while True:

        init_parse(rss)
        extract_img(statusarray)
        for message in new_result:
            pinstream.send(CHANNEL, message)












