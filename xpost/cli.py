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
    print(colored(txt, color_colde))


def tweet():
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
    parser = argparse.ArgumentParser(description="xpost --version")
    parser.add_argument("--version", action='version', version=f'xpost {__version__}')
    args = parser.parse_args()

if __name__ == "__main__":
    fire.Fire({"tweet": tweet, "tweet_config": tweet_config, "virgin": virgin})
