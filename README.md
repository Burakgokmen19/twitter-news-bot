Twitter to WhatsApp Bot

This Python script fetches the latest tweet from a specified Twitter account and sends it as a message to a WhatsApp group using pywhatkit. The script runs continuously, checking for new tweets every 15 minutes.

Features

Fetches the latest tweet from a specific Twitter user.

Sends the tweet to a designated WhatsApp group.

Prevents duplicate messages by storing the last tweet ID.

Handles Twitter API rate limits.

Requirements

Ensure you have the following installed before running the script:

Python 3.x

Required Python packages:

pip install requests pywhatkit

Twitter API Bearer Token (from Twitter Developer Portal)

A WhatsApp Web session (logged in on the default browser)

Configuration

Before running the script, update the following variables in the script:

BEARER_TOKEN = "your_twitter_bearer_token"
USERNAME = "twitter_username"
WHATSAPP_GROUP_NAME = "your_whatsapp_group_name"

How to Run

Clone the repository or download the script.

Install the required dependencies.

Ensure WhatsApp Web is logged in on your browser.

Run the script:

python script.py

How It Works

The script fetches the latest tweet from the specified Twitter account.

If the tweet is new, it retrieves the tweet content.

The tweet is then sent to the specified WhatsApp group.

The script repeats this process every 15 minutes.

Handling Twitter API Rate Limits

If the script encounters a 429 Too Many Requests error, it will wait for the appropriate cooldown period before making another request.

Notes

Make sure pywhatkit can interact with WhatsApp Web.

The script should remain running to continue checking for new tweets.

Disclaimer

This script is for educational purposes only. Ensure you comply with Twitter and WhatsApp's terms of service while using this script.
