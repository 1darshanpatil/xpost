#!/usr/bin/env python3
from .encrypt import *
from .engine import *
from .encrypt import CredentialCLI
import json


def store_credentials(usr, passwd):
    """
    Stores user credentials using the CredentialCLI class. This function is designed to
    securely store the Twitter API credentials encrypted with the provided password.

    Args:
        usr (str): The username associated with the Twitter credentials.
                   This is used as an identifier for the stored credentials.
        passwd (str): The password used for encrypting the credentials.
                      It's crucial for the decryption of the stored credentials later.

    Returns:
        None
    """
    cli = CredentialCLI()
    cli.store(usr, passwd)


def reset_credentials():
    """
    Resets (deletes) all stored credentials and data related to the TwitterBot.
    This function will remove all the stored, encrypted credentials and any
    related configuration data, effectively resetting the application to its
    initial state.

    Returns:
        None
    """
    cli = CredentialCLI()
    cli.reset()


def post_tweet(creds, tweet_path):
    """
    Posts a tweet using the credentials and the path to the tweet's content.
    This function handles the process of decrypting the stored credentials,
    initializing the TwitterBot with these credentials, and posting the tweet.

    Args:
        creds (str): Combined username and password in 'username:password' format,
                     used for decrypting the stored Twitter API credentials.
        tweet_path (str): The file path containing the tweet's content to be posted.

    Returns:
        str: A message indicating the successful posting of the tweet or an error message.
    """
    username, password = creds.split(":")
    cli = CredentialCLI()
    apis = cli.load(username, password)
    if not apis:
        raise Exception("Invalid credentials")
    bot = TwitterBot(apis)
    reading_post_file = bot.read_post_file(tweet_path)
    tweeted_id = bot.post_tweet(tweet_path)
    bot.save_tweet_info(tweet_id=tweeted_id, message=reading_post_file)
    return f"Tweeted:\n{reading_post_file}\n"


def delete_tweet(creds, tweet_id):
    """
    Deletes a tweet using the credentials and the tweet ID. This function
    handles the process of decrypting the stored credentials, initializing the
    TwitterBot with these credentials, and deleting the specified tweet.

    Args:
        creds (str): Combined username and password in 'username:password' format,
                     used for decrypting the stored Twitter API credentials.
        tweet_id (str): The ID of the tweet to be deleted.

    Returns:
        str: A message indicating the successful deletion of the tweet or an error message.
    """
    username, password = creds.split(":")
    cli = CredentialCLI()
    apis = cli.load(username, password)
    if not apis:
        raise Exception("Invalid credentials")
    bot = TwitterBot(apis)
    bot.delete_tweet(tweet_id)
    bot.save_tweet_info(tweet_id, delete=True)
    return "Tweet deleted."
