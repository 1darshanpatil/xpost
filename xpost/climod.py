#!/usr/bin/env python3
from .encrypt import *
from .engine import *
from .encrypt import CredentialCLI
import json
import getpass
import fire


def print_color(txt, color_colde):
    print(colored(txt, color_colde))


def add_user():
    """
    Adds new user credentials for Twitter API access.

    This function prompts the user for a username and password, confirms the password,
    and stores the encrypted credentials using the CredentialCLI class.

    Notes
    -----
    The function ensures password confirmation for security. If the password confirmation
    fails twice, the function exits to prevent repeated unsuccessful attempts.
    """
    username = input("Enter a username to encrypt your APIs: ")
    password = getpass.getpass("Set a password to secure your encrypted APIs: ")
    password_confirmation = getpass.getpass("Confirm your password: ")
    confirmation_chances = 0

    while password != password_confirmation:
        print_color("Passwords do not match. Please try again.", 91)
        password = getpass.getpass("Set a new password to secure your encrypted APIs: ")
        password_confirmation = getpass.getpass("Confirm your new password: ")
        confirmation_chances += 1

        if confirmation_chances == 2:
            print_color("Maximum number of attempts reached!", 91)
            sys.exit(1)

    CredentialCLI().store(username, password)


def show_credentials():
    """
    Displays the decrypted credentials of a user.

    Prompts the user for a username and password, then decrypts and returns the
    stored credentials.

    Returns
    -------
    dict
        A dictionary containing the decrypted credentials, if successful.
    """
    username = input("Enter your username to decrypt your APIs: ")
    password = getpass.getpass("Enter your password to decrypt your APIs: ")
    credential_cli = CredentialCLI()
    return credential_cli.load(username, password)


def reset_credentials():
    """
    Resets the stored credentials for all users.

    This function clears all stored credentials by calling the reset method of the
    CredentialCLI class. It provides a command line interface for credential reset.
    """
    credential_cli = CredentialCLI()
    print("Resetting credentials...")
    credential_cli.reset()


def post_tweet(tweet_path):
    """
    Posts a tweet using the specified tweet file path.

    Parameters
    ----------
    tweet_path : str
        The path to the file containing the tweet content.

    Notes
    -----
    Prompts the user for credentials, reads the tweet content from the specified file,
    posts the tweet, and then saves the tweet information. The function provides a
    command line interface for tweeting.
    """
    username = input("Enter your username to decrypt your APIs: ")
    password = getpass.getpass("Enter your password to decrypt your APIs: ")
    credential_cli = CredentialCLI()
    apis = credential_cli.load(username, password)

    if not apis:
        raise Exception("Invalid credentials.")

    twitter_bot = TwitterBot(apis)
    post_content = twitter_bot.read_post_file(tweet_path)
    tweeted_id = twitter_bot.post_tweet(tweet_path)
    twitter_bot.save_tweet_info(tweet_id=tweeted_id, message=post_content)
    print("Twitter post:")
    print_color(f"{post_content}\n", 93)


def delete_tweet(tweet_id):
    """
    Deletes a tweet based on the specified tweet ID.

    Parameters
    ----------
    tweet_id : str
        The ID of the tweet to be deleted.

    Notes
    -----
    Prompts the user for credentials, then deletes the tweet corresponding to the
    provided tweet ID. It also saves the information that the tweet has been deleted.
    The function provides a command line interface for tweet deletion.
    """
    username = input("Enter your username to decrypt your APIs: ")
    password = getpass.getpass("Enter your password to decrypt your APIs: ")
    credential_cli = CredentialCLI()
    apis = credential_cli.load(username, password)

    if not apis:
        raise Exception("Invalid credentials.")

    twitter_bot = TwitterBot(apis)
    twitter_bot.delete_tweet(tweet_id)
    twitter_bot.save_tweet_info(tweet_id, delete=True)
    print_color("Tweet successfully deleted.", 93)
