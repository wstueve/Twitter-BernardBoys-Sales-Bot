# Twitter-Cardano-NFT-Sales-Bot

## Preface

[[Back to contents]](https://github.com/WilliamAmbrozic/Twitter-Cardano-NFT-Sales-Bot#contents)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This bot allows for custom tweet text and fast response times. The bot utilizes [opencnft.io](https://opencnft.io/)'s ```transactions``` API call (source of NFT & sales data), responding to sales in less than a minute while allowing for NFT image uploading. This bot is designed to run on an external server. **This bot was tested on an EC2 AWS instance and a [Raspberry Pi 4](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)**. Usable on Unix based servers.

**1st Note: In the rare case that your NFT file sizes are greater than 3mb, they will have to be compressed prior to being uploaded.** Please see the comment <#compress here> in the send_tweet function - place your function that compresses the ```tmp``` file there. For standard image files there are many resources online for python compression. For gifs, [this gist](https://gist.github.com/skywodd/8b68bd9c7af048afcedcea3fb1807966) may be of help.

**2nd Note:** This bot assumes the [opencnft.io](https://opencnft.io/) transactions api endpoint only outputs sales data and outputs the correct data. Please test the bot prior to production.

## Contents
- [Setup](https://github.com/WilliamAmbrozic/Twitter-Cardano-NFT-Sales-Bot#Setup)  
  - [Installing](https://github.com/WilliamAmbrozic/Twitter-Cardano-NFT-Sales-Bot#Installing-the-Bot) 
  - [Adding Credentials](https://github.com/WilliamAmbrozic/Twitter-Cardano-NFT-Sales-Bot#Adding-Credentials)
  - [Running](https://github.com/WilliamAmbrozic/Twitter-Cardano-NFT-Sales-Bot#Running-the-Bot)  
- [Config (Customize)](https://github.com/WilliamAmbrozic/Twitter-Cardano-NFT-Sales-Bot#Config)
- [Free Use](https://github.com/WilliamAmbrozic/Twitter-Cardano-NFT-Sales-Bot#Free-Use)
- [Find Me](https://github.com/WilliamAmbrozic/Twitter-Cardano-NFT-Sales-Bot#find-me)
- [Tip Jar](https://github.com/WilliamAmbrozic/Twitter-Cardano-NFT-Sales-Bot#ADA-Tip-Jar)

## Setup

[[Back to contents]](https://github.com/WilliamAmbrozic/Twitter-Cardano-NFT-Sales-Bot#contents)

## Installing the Bot

[[Back to contents]](https://github.com/WilliamAmbrozic/Twitter-Cardano-NFT-Sales-Bot#contents)

Clone and install Python requirements with
```
git clone https://github.com/WilliamAmbrozic/Twitter-Cardano-NFT-Sales-Bot.git
cd Twitter-Cardano-NFT-Sales-Bot
pip install -r requirements.txt
```

## Adding Credentials

[[Back to contents]](https://github.com/WilliamAmbrozic/Twitter-Cardano-NFT-Sales-Bot#contents)

### 1. Add Your NFT Policy ID to the Config.json

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A collection's policy ID can be found by going to [opencnft.io](https://opencnft.io/) and searching for your collection. Once on the project page look for Policy ID and copy, this is needed for the bot to know what collection to tweet out. Paste this value in the **./config/config.json** attribute called **policy** as seen [here](https://github.com/WilliamAmbrozic/Twitter-Cardano-NFT-Sales-Bot#Config).

### 2. Add your Twitter Developer Credentials to the Config.json

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A. Make a Twitter account and sign up to become a Twitter developer [here](https://developer.twitter.com/).

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;B. Make sure your Twitter developer account has elevated access for image uploading [here](https://developer.twitter.com/en/portal/products/elevated).

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;C. Make sure that the Access Token and Secret has been created with Read and Write permissions.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;D. Place your Twitter developer credentials in **./config/config.json** as seen [here](https://github.com/WilliamAmbrozic/Twitter-Cardano-NFT-Sales-Bot#Config).

## Running the Bot

[[Back to contents]](https://github.com/WilliamAmbrozic/Twitter-Cardano-NFT-Sales-Bot#contents)

Run with 
```
python3 bot.py
```
Or recommended with (if you do not want an ssh exit or general exit to halt the bot)
```
nohup python3 bot.py &
```

## Config

[[Back to contents]](https://github.com/WilliamAmbrozic/Twitter-Cardano-NFT-Sales-Bot#contents)

The config file **./config/config.json** will look something like this:
```
{
  "policy": "ADD_YOUR_POLICY_HERE",
  "twitter_credentials": {
    "bearer_token": "ADD_YOURS_HERE",
    "consumer_key": "ADD_YOURS_HERE",
    "consumer_secret": "ADD_YOURS_HERE",
    "access_token": "ADD_YOURS_HERE",
    "access_token_secret": "ADD_YOURS_HERE"
  },
  "tweet_text": "BOOM💥 [-n] just sold for [-p] ([-f])",
  "fiat_currency": "USD",
  "TPS": 1
}
```

### Optional Attributes
**tweet_text**: You can customize the text that is tweeted out with the NFT image. Tweet text follows this notation (the bot will replace the following syntax with ...):
* [-n]: The NFT name (Ex. SpaceBudz 0001)
* [-f]: The fiat price with respect to the fiat_currency value described below (Ex. $199.19 USD)
* [-p]: The sale price in ADA (Ex. 10 ADA)
* [-u]: The NFT's unit ID
* [-i]: The NFT image url (Not needed to display the NFT image)
* [-s]: The source of the sale (Ex. jpg.store)
* [-t]: tx_id (transaction id) - can be appended to adascan for proof

For example, 
```
BOOM💥 [-n] just sold for [-p] ([-f])
```
would become
```
BOOM💥 SpaceBudz #001 just sold for 1000.54 ADA ($500.37 USD)
```

**fiat_currency**: The bot currently supports the following currencies: EUR, USD, CAD, JPY, GPB, AUD, CNY, INR. Change this value to change the currency in which ADA is converted if you choose to output fiat price.


## Free Use

[[Back to contents]](https://github.com/WilliamAmbrozic/Twitter-Cardano-NFT-Sales-Bot#contents)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This bot is 100% free to use. Use of this bot for your project is encouraged. **No credit is needed for the creator**; however, please credit [opencnft.io](https://api.opencnft.io/1/) (data provider) according to their preference (check link). If you find this bot useful and insist on crediting the creator, you can add @williamambrozic in the bot's Twitter bio or have the bot follow @williamambrozic on Twitter.

## Find Me

- [Twitter](https://twitter.com/WilliamAmbrozic)
- [About](https://williamambrozic.github.io/about)

## ADA Tip Jar
  * addr1q8mhqvmp4g0chp87v8ydrlrmxf4402thtd26a3a3e8fxx2q9yu4vpjf6g5t7ygf0cy08ayr3hc8zxtefx0d7qq4hw2tsug75ry
### Bitcoin
  * bc1qa7vkam2w4cgw8njqx976ga5ns8egsq3yzxzlrt

