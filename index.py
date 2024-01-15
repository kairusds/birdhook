import configparser
from discord import Colour, Embed, SyncWebhook
from threading import Timer
from tweety import Twitter
import requests
import os.path

twitter_color = Colour.from_rgb(29, 161, 242)
divider_color = Colour.from_rgb(62, 83, 100)
secondary_color = Colour.from_rgb(34,48,60)

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

def create_base_embed(target, tweet, color=twitter_color):
	embed = Embed(
		colour=color,
		# Truncate, since Twitter doesn't have a text limit for verified users.
		description=(tweet.text[:4093] + "...") if len(tweet.text) > 4096 else tweet.text,
		url=tweet.url,
		timestamp=tweet.created_on
	).set_author(
		name="{display_name} (@{username})".format(display_name=target.name, username=target.username),
		url=f"https://twitter.com/{target.username}",
		icon_url=target.profile_image_url_https
	)
	return embed

def create_media_embed(media, color):
	embed = Embed(colour=color).set_image(url=media.media_url_https)
	return embed

def create_media_embeds(medias, color=twitter_color):
	embeds = []
	medias.pop(0)
	for media in medias:
		embeds.append(create_media_embed(media, color=color))
	return embeds

def send_webhook():
	target = app.get_user_info(config["twitter"]["target"])
	tweet = app.get_tweets(target.username)[0]
	
	if os.path.isfile("latest_tweet.txt"):
		if get_saved_tweet() == str(tweet.id):
			print("The latest tweet has already been posted as a webhook. Ignoring this iteration...")
			return
	
	if not config["webhook_message"].getboolean("replies") and tweet.is_reply:
		print("The latest tweet is a reply. Ignoring this iteration...")
		return
	
	if tweet.is_retweet:
		print("The latest tweet is a retweet. Ignoring this iteration...")
		return
	
	if not config["webhook_message"].getboolean("quotes") and tweet.is_quoted:
		print("The latest tweet is a quote. Ignoring this iteration...")
		return
	
	with requests.Session() as session:
		webhook = SyncWebhook.from_url(config["discord"]["webhook_url"], session=session)
		
		embeds = [create_base_embed(target, tweet)]
		
		if len(tweet.media) > 0:
			embeds[0].set_image(url=tweet.media[0].media_url_https)
			
			if config["webhook_message"].getboolean("all_images"):
				embeds.extend(create_media_embeds(tweet.media.copy()))
		
		if tweet.is_reply:
			embeds.append(Embed(colour=divider_color, title=":arrow_right_hook: Replied to:"))
			embeds.append(
				create_base_embed(tweet.replied_to.author, tweet.replied_to, color=secondary_color)
				.set_image(url=tweet.replied_to.media[0].media_url_https)
			)
			if config["webhook_message"].getboolean("sub_images"):
				embeds.extend(create_media_embeds(tweet.replied_to.media.copy(), color=secondary_color))
		elif tweet.is_quoted:
			embeds.append(Embed(colour=divider_color, title=":repeat: Quoted:"))
			embeds.append(
				create_base_embed(tweet.quoted_tweet.author, tweet.quoted_tweet, color=secondary_color)
				.set_image(url=tweet.quoted_tweet.media[0].media_url_https)
			)
			if config["webhook_message"].getboolean("sub_images"):
				embeds.extend(create_media_embeds(tweet.quoted_tweet.media.copy(), color=secondary_color))
		
		webhook.send(
			avatar_url=target.profile_image_url_https,
			# Can't use the Twitter user's screen name because, for some reason,
			# special characters like the ones from zalgo aren't accepted by
			# discord.py as a webhook username.
			username=target.username,
			content=f"<{tweet.url}>",
			embeds=embeds
		)
		save_latest_tweet(tweet.id)
		print("Webhook Sent")

def run():
	Timer(config["webhook"].getint("interval"), run).start()
	send_webhook()

run()
