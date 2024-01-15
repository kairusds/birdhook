import configparser
from discord import Colour, Embed, SyncWebhook
from threading import Timer
from tweety import Twitter
import requests
import os.path

config = configparser.ConfigParser()
config.read("config.ini")

app = Twitter("session")
# User will be prompted to enter their password (and 2FA code if applicable)
app.start(config["twitter"]["login"]);

def get_saved_tweet():
	with open("latest_tweet.txt", "r") as file:
		return file.read()

def save_latest_tweet(id):
	with open("latest_tweet.txt", "w") as file:
		file.write(id)

def send_webhook():
	target = app.get_user_info(config["twitter"]["target"])
	tweet = app.get_tweets(target.username)[0]
	
	if os.path.isfile("latest_tweet.txt"):
		if get_saved_tweet() == str(tweet.id):
			print("The latest tweet has already been posted as a webhook. Ignoring this iteration...")
			return
	
	with requests.Session() as session:
		webhook = SyncWebhook.from_url(config["discord"]["webhook_url"], session=session)
		
		embed = Embed(
			colour=Colour.from_rgb(29, 161, 242),
			# Truncate, since Twitter doesn't have a text limit for verified users.
			description=(tweet.text[:4093] + "...") if len(tweet.text) > 4096 else tweet.text,
			url=tweet.url,
			timestamp=tweet.created_on
		).set_author(
			name="{display_name} (@{username})".format(display_name=target.name, username=target.username),
			url=f"https://twitter.com/{target.username}",
			icon_url=target.profile_image_url_https
		)
		
		if len(tweet.media) > 0:
			embed.set_image(url=tweet.media[0].media_url_https)
		
		webhook.send(
			avatar_url=target.profile_image_url_https,
			# Can't use the Twitter user's screen name because, for some reason,
			# special characters like the ones from zalgo aren't accepted by
			# discord.py as a webhook username.
			username=config["twitter"]["target"],
			content=f"<{tweet.url}>",
			embed=embed
		)
		save_latest_tweet(tweet.id)
		print("Webhook Sent")

def run():
	Timer(int(config["webhook"]["interval"]), run).start()
	send_webhook()

run()
