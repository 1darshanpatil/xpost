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
    username = input("Enter your username to decrypt your APIs: ")
    password = getpass.getpass("Enter your password to decrypt your APIs: ")
    credential_cli = CredentialCLI()
    return credential_cli.load(username, password)


def reset_credentials():
    credential_cli = CredentialCLI()
    print("Resetting credentials...")
    credential_cli.reset()


def post_tweet(tweet_path):
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
    
