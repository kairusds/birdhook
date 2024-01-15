# birdhook
Post Tweets into Discord as a webhook without limits.

Requires Python 3.8 or higher.

**WARNING: It is recommended to use a separate Twitter account (a throwaway one) for fetching tweets from another account, as the account used for fetching tweets is always at risk of being put into a read-only state by Twitter.**

**INFO: After the first run of the script, a file named `session.tw_session` will be saved in this project's directory. Keep this file safe as it contains the cookies for logging into the Twitter account. As long as this file exists in the same directory/folder, it will be used for login instead of the `twitter login username` from the config.**

## Setup
###### I didn't include images because I'm too lazy, feel free to make a Pull Request to add them.
0. Download this repository by clicking `Code > Download ZIP` or [this link](https://github.com/kairusds/birdhook/archive/master.zip) Then extract the ZIP file somewhere, and goto the extracted `birdhook-master` folder and open `Terminal` or `Command Prompt` inside of it.
1. Install the dependencies of the project by running `pip install -r requirements.txt` in the same directory/folder.
2. Make a copy of `config.ini.bak` and rename the new copy into `config.ini`.
3. Change the contents of `config.ini` as needed, there's descriptions for each of the value in the config file. You don't need to change the lines that starts with `;`.
4. Where to get the `webhook_url` from `config.ini`:
	- For **Desktop**: Right-click a text channel's name, choose `Edit Channel`, go to `Integrations`, click `Create Webhook` (or `View Webhooks` if you already have one), select a Webhook, find the `Copy Webhook URL` button below it.
	- For mobile (**Aliucord**): Download the [EditWebhooks plugin](https://github.com/c10udburst-discord/aliucord-plugins/raw/builds/EditWebhooks.zip), move the downloaded ZIP file to `Primary external storage > Aliucord > plugins (or /storage/emulated/0/Aliucord/plugins)`. Hold-click a text channel name, go to `Edit channel > Edit webhooks > Create webhook`, click the created webhook, and then click `Copy Link` from the bottom menu.
	- For mobile (**Vendetta**): Get the **Create webhooks plugin** by joining the official [Vendetta server](https://discord.gg/n9QQ4XhhJP), heading to the **plugins forum channel**, searching for `Create webhooks`, and installing it through the link in the first message of the thread at the very top. The steps are similar to Aliucord, but you need to go to `Webhooks` instead of `Edit webhooks`.
5. Run the script using `python3 index.py` or clicking the `index.py` file, and everything should be good to go. 
