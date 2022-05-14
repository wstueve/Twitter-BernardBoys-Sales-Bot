import requests
import time
import json
import tweepy
import yfinance as yf
import os.path
from os import path
from PIL import Image
import PIL

######################### GLOBAL DEFINITIONS #########################################

#Fetching config data
conf = open("./config/config.json")
config = json.load(conf)

#List of supported currency
supported_fiat = ["EUR", "USD", "CAD", "JPY", "GPB", "AUD", "CNY", "INR"]

#This value is added to the delay in case opencnft thinks we are cutting too close into their TPS
#If you feel risky lower this value or make it 0
safety_delay = 0.05
delay = (1/config['TPS']) + safety_delay

#MAX TWEEPY IMAGE SIZE
COMP_SIZE = 3072000

client = tweepy.Client(bearer_token=config['twitter_credentials']['bearer_token'],
                       consumer_key=config['twitter_credentials']['consumer_key'],
                       consumer_secret=config['twitter_credentials']['consumer_secret'],
                       access_token=config['twitter_credentials']['access_token'],
                       access_token_secret=config['twitter_credentials']['access_token_secret'])

auth = tweepy.OAuth1UserHandler(config['twitter_credentials']['consumer_key'],
                        config['twitter_credentials']['consumer_secret'],
                        config['twitter_credentials']['access_token'],
                        config['twitter_credentials']['access_token_secret'])

api = tweepy.API(auth)

######################### FUNCTION DEFINITIONS #########################################

def init_collections():
    #Hasmap: Activity Signature => Activity
    ret = {}
    url = "https://api.opencnft.io/1/policy/" + config['policy'] + "/transactions"
    response = requests.request("GET", url).json()['items']

    for x in response:
        ret[x['tx_id']] = x
    return ret

#Fetches the latest Cardano price in selected currency
def get_current_price(symbol):
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period='1d')
    return todays_data['Close'][0]

#Converts tweet text to config text
def convert_tweet(sale_data):
    text = config['tweet_text']
    text = text.replace("[-f]", "$" + str(round((get_current_price("ADA-" + config['fiat_currency'])*sale_data["price"]/10**6), 2)) + " " + config['fiat_currency'])
    text = text.replace("[-n]", sale_data['unit_name'])
    text = text.replace("[-p]", str(sale_data["price"]/10**6) + " ADA")
    text = text.replace("[-u]", str(sale_data["unit"]))
    text = text.replace("[-i]", str(sale_data["thumbnail"]["thumbnail"]))
    text = text.replace("[-s]", str(sale_data["marketplace"]))
    return text

#optional compression
def compress(filename):
    picture = Image.open(filename)
    size = os.stat(filename).st_size

    while size > COMP_SIZE:
        picture = picture.resize((int(picture.size[0]/2), int(picture.size[0]/2)))
        size = os.stat(filename).st_size
        if size > COMP_SIZE:
            break;
        picture.save(filename,optimize=True,quality=65)
        size = os.stat(filename).st_size

#Sends a tweet based on sale data and NFT metadata
def send_tweet(api, client, meta):
    image = requests.get(meta['thumbnail']['thumbnail'].replace("ipfs://", "https://ipfs.io/ipfs/")).content
    filename = './tmp'
    with open(filename, 'wb') as handler:
        handler.write(image)
    #compress(filename)
    mediaID = api.media_upload(filename)
    client.create_tweet(text=convert_tweet(sale_data), media_ids=[mediaID.media_id])

######################### DRIVER CODE #########################################

#Checking valid currency
if config['fiat_currency'] not in supported_fiat:
    print("INVALID FIAT_CURRENCY: CHECK CONFIG")

#Getting initial state of sales
activities = init_collections()
last_activities = activities

print(f"LISTENING FOR SALES: {config['policy']}")

#Bot loop
while True:
    #Getting hashmap
    try:
        activities = init_collections()
        time.sleep(delay)
    except:
        continue

    #Checking all activities (by signature, key values)
    for activity in activities.keys():
        #Checking if there is a new activity
        if activity not in last_activities.keys():
            try:
                send_tweet(api, client, activities[activity])
                print(f"Tweeting: {convert_tweet(activities[activity])}")
            except:
                print(f"ERROR: with NFT that Sold for {str(activities[activity]['price'])} Not Tweeted")

    last_activities = dict(activities)
