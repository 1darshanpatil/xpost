#!/usr/bin/env python3
from .encrypt import *
from .engine import *
import argparse
import json
import sys
import tweepy
import logging
import fire
from xpost import __version__
import getpass

def print_color(txt, color_colde):
    """
    Prints the given text in the specified color.

    Parameters
    ==========
    txt : str
        The text to be printed.
    color_code : int
        The ANSI color code to apply to the text.

    Notes
    =====
    Utilizes the 'colored' function to apply ANSI color codes to the text.
    """
    print(colored(txt, color_colde))


def tweet():
    """
    Handles the tweet operations for the Twitter Bot CLI.

    This function allows the user to post or delete tweets using command line arguments.

    Notes
    -----
    The user is prompted to enter credentials which are then used to perform
    the requested tweet operations. The function handles both posting new tweets
    and deleting existing ones.
    """    
    parser = argparse.ArgumentParser(
        description="Twitter Bot CLI - Tweeting Operations"
    )
    parser.add_argument("--post", help="Path to the tweet file.", required=False)
    parser.add_argument("--delete", help="Tweet ID to delete.", required=False)
    args = parser.parse_args()

    try:
        username = input("Enter your username to decrypt your saved APIs: ")
        password = getpass.getpass("Enter your password to decrypt your saved APIs: ")
        apis = CredentialCLI().load(username, password)
        bot = TwitterBot(apis)
    except ValueError:
        print(
            "Error: Invalid credential format. Please use the username:password format."
        )
        return

    if args.post:
        try:
            post_content = bot.read_post_file(args.post)
            tweeted_id = bot.post_tweet(args.post)
            print("Twitter post:")
            print_color(f"{post_content}\n", 93)
            bot.save_tweet_info(tweet_id=tweeted_id, message=post_content)
        except Exception as e:
            print(f"An error occurred while posting the tweet: {e}")

    if args.delete:
        try:
            bot.delete_tweet(args.delete)
            bot.save_tweet_info(args.delete, delete=True)
            print_color("Tweet successfully deleted.", 93)
        except Exception as e:
            print(f"An error occurred while deleting the tweet: {e}")


def tweet_config():
    """
    Manages the configuration operations for the Twitter Bot CLI.

    This function provides subcommands for adding user credentials and resetting
    the configuration.

    Notes
    -----
    The function uses subparsers to handle different configuration commands like
    'add_user' and 'reset'.
    """    
    parser = argparse.ArgumentParser(
        description="Twitter Bot CLI - Configuration Operations"
    )
    subparsers = parser.add_subparsers(dest="config_command")
    subparsers.add_parser("add_user")
    subparsers.add_parser("reset")
    args = parser.parse_args()

    if args.config_command == "add_user":
        add_user_credentials()
    elif args.config_command == "reset":
        files_deleted= CredentialCLI().reset()
        if files_deleted == 'success':
            print_color("Credentials successfully reset.", 92)


def add_user_credentials():
    """
    Adds new user credentials for the Twitter Bot.

    Prompts the user for a username and password, and stores the encrypted credentials.

    Notes
    -----
    If the password confirmation fails twice, the function exits. Successfully added
    credentials are encrypted and stored.

    Example:
        $ x-config add_user
        $ x-config reset
    """    
    username = input("Enter a username to encrypt your APIs: ")
    password = getpass.getpass("Set a password to secure your encrypted APIs: ")
    password_confirmation = getpass.getpass("Confirm your password: ")
    confirmation_chances = 0

    while password != password_confirmation:
        print("Passwords do not match. Please try again.")
        password = getpass.getpass("Set a new password to secure your encrypted APIs: ")
        password_confirmation = getpass.getpass("Confirm your new password: ")
        confirmation_chances += 1
        if confirmation_chances == 2:
            print("Maximum attempt limit reached. Exiting.")
            sys.exit(1)

    CredentialCLI().store(username, password)
    print_color("User credentials successfully added.", 92)


def virgin():
    """
    Provides version information for the xpost application.

    This function is a part of the CLI and responds to the '--version' argument.

    Notes
    -----
    Utilizes the global '__version__' variable to display the current version of xpost.

    Example: 
    $ xpost --version
    """    
    parser = argparse.ArgumentParser(description="xpost --version")
    parser.add_argument("--version", action='version', version=f'xpost {__version__}')
    args = parser.parse_args()

if __name__ == "__main__":
    fire.Fire({"tweet": tweet, "tweet_config": tweet_config, "virgin": virgin})
