import asyncio
import discord
import requests
import re
import json
from requests_oauthlib import OAuth1Session

f = open("config.json", encoding='utf-8')
config = json.load(f)
f.close()

hashtag = config["twitter"]["hashtag"]
url = config["twitter"]["api_url"]
consumer_key = config["twitter"]["consumer_key"]
consumer_secret = config["twitter"]["consumer_secret"]
access_token_key = config["twitter"]["access_token_key"]
access_token_secret = config["twitter"]["access_token_secret"]

token = config["discord"]["token"]
channel_id = config["discord"]["channel_id"]

client = discord.Client()
twitter = OAuth1Session(consumer_key, consumer_secret, access_token_key, access_token_secret)

@client.event
async def on_ready():
    print(client.user.name)
    print(client.user.id)
    print('It is ready')

@client.event
async def on_message(message):
    if message.channel.id == channel_id:
        user = message.author.display_name
        text = message.content
        
        while True:
            r = re.search(r"<@[0-9]+>", text)
            if r:
                member = message.server.get_member(r.group()[2:-1])
                text = text.replace(r.group(), ">>"+member.name)
            else:
                break

        while True:
            r = re.search(r"<@![0-9]+>", text)
            if r:
                member = message.server.get_member(r.group()[3:-1])
                text = text.replace(r.group(), ">>"+member.name)
            else:
                break

        while True:
            r = re.search(r"<#[0-9]+>", text)
            if r:
                channel = message.server.get_channel(r.group()[2:-1])
                text = text.replace(r.group(), channel.name+"channel")
            else:
                break

        while True:
            r = re.search(r"<#![0-9]+>", text)
            if r:
                channel = message.server.get_channel(r.group()[3:-1])
                text = text.replace(r.group(), channel.name+"channel")
            else:
                break

        params = {"status": user+" : "+text+"\n"+hashtag}
        
        try:
            req = twitter.post(url, params = params)
            if req.status_code == 200:
                print ("OK")
            else:
                print ("Error: %d" % req.status_code)
        except:
            print ("Error")

if __name__ == "__main__":
    client.run(token)