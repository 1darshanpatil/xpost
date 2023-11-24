#!/usr/bin/env python3
from .encrypt import * 
from .engine import *
import argparse
import json
import sys
import tweepy
import logging
import fire

def tweet():
    """
    Function to handle tweeting operations such as posting and deleting tweets.

    Usage:
    - To post a tweet: `tweet --creds <username:password> --post <path_to_tweet_file>`
    - To delete a tweet: `tweet --creds <username:password> --delete <tweet_id>`

    Command-line arguments:
    - --creds: Provide username and password in 'username:password' format.
    - --post: Path to the tweet file for posting.
    - --delete: Tweet ID to delete a tweet.
    """
    parser = argparse.ArgumentParser(description="Twitter Bot CLI - Tweeting Operations")
    parser.add_argument("--creds", help="Provide username and password in format username:password", required=False)
    parser.add_argument("--post", help="Path to the tweet file", required=False)
    parser.add_argument("--delete", help="Tweet ID to delete", required=False)
    
    args = parser.parse_args()

    if args.creds:
        try:
            username, password = args.creds.split(':')
            apis = CredentialCLI().load(username, password)
            bot = TwitterBot(apis)
        except ValueError:
            print("Error: Invalid format for --creds. Please use username:password format.")
            return

        if args.post:
            try:    
                reading_post_file = bot.read_post_file(args.post)
                tweeted_id = bot.post_tweet(args.post)
                print(f"\nTweeted:\n{reading_post_file}\n")
                bot.save_tweet_info(tweet_id=tweeted_id, message=reading_post_file)
            except Exception as e:
                print(f"An error occurred while posting the tweet: {e}")

        if args.delete:
            try:
                bot.delete_tweet(args.delete)
                bot.save_tweet_info(args.delete, delete=True)
            except Exception as e:
                print(f"An error occurred while deleting the tweet: {e}")

def tweet_config():
    """
    Function to handle configuration operations such as storing and resetting credentials.

    Usage:
    - To store credentials: `tweet_config store <username> <password>`
    - To reset stored data: `tweet_config reset`

    Command-line arguments:
    - store: Store credentials for a given username and password.
    - reset: Reset (delete) all stored credentials and data.
    """
    parser = argparse.ArgumentParser(description="Twitter Bot CLI - Configuration Operations")
    
    # Subparser for the config argument
    subparsers = parser.add_subparsers(dest='config_command')
    
    # Subparser for 'store' command
    store_parser = subparsers.add_parser('store')
    store_parser.add_argument('username', help="Username for storing credentials")
    store_parser.add_argument('password', help="Password for storing credentials")

    # Subparser for 'reset' command
    reset_parser = subparsers.add_parser('reset')

    args = parser.parse_args()

    if args.config_command == 'store':
        CredentialCLI().store(args.username, args.password)
    elif args.config_command == 'reset':
        CredentialCLI().reset()

if __name__ == "__main__":
    # Example usage: 'python script_name.py tweet' or 'python script_name.py tweet_config'
    fire.Fire({
        "tweet": tweet,
        "tweet_config": tweet_config
    })
