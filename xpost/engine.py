#!/usr/bin/env python3
import argparse
from time import sleep
import json
import sys
import tweepy
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)


class TwitterBot:
    def __init__(self, creds_file):
        self.creds_file = creds_file
        # self.creds = self.read_credentials()
        self.creds = creds_file
        self.client = self.authenticate()

    def read_credentials(self):
        try:
            with open(self.creds_file, "r") as file:
                return json.load(file)
        except Exception as e:
            logging.error(f"Error reading credentials: {e}")
            sys.exit(1)

    def authenticate(self):
        try:
            return tweepy.Client(
                bearer_token=self.creds["BEARER_TOKEN"],
                consumer_key=self.creds["API_KEY"],
                consumer_secret=self.creds["API_KEY_SECRET"],
                access_token=self.creds["ACCESS_TOKEN"],
                access_token_secret=self.creds["ACCESS_TOKEN_SECRET"],
            )
        except KeyError as e:
            logging.error(f"Missing credential: {e}")
            sys.exit(1)
        except Exception as e:
            logging.error(f"Error during authentication: {e}")
            sys.exit(1)

    def read_post_file(self, post_file):
        try:
            with open(post_file, "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            return post_file
        except Exception as e:
            logging.error(f"Error reading post file: {e}")
            sys.exit(1)

    def post_tweet(self, post_file):
        tweet = self.read_post_file(post_file)
        if len(tweet) > 280:
            logging.error("Tweet exceeds 280 characters. Exiting.")
            sys.exit(1)

        try:
            response = self.client.create_tweet(text=tweet)
            tweet_id = response.data["id"]
            logging.info(f"Tweet successfully posted. Tweet ID: {tweet_id}")
            # self.save_tweet_info(tweet_id, self.tweet)
            return tweet_id
        except Exception as e:
            logging.error(f"Error posting tweet: {e}")
            sys.exit(1)

    def get_user_details(self):
        try:
            user_details = self.client.get_me()
            username = user_details.data.username
            return {"username": username}
        except Exception as e:
            logging.error(f"Error retrieving user details: {e}")

    def save_tweet_info(self, tweet_id, message=None, delete=False):
        if delete == True:
            try:
                # Load existing tweets and filter out the one to delete
                with open("tweets.json", "r") as file:
                    tweets = [json.loads(line) for line in file if line.strip()]

                if any(tweet["tweet_id"] == tweet_id for tweet in tweets):
                    tweets = [
                        tweet for tweet in tweets if tweet["tweet_id"] != tweet_id
                    ]

                    # Rewrite the file without the deleted tweet
                    with open("tweets.json", "w") as file:
                        for tweet in tweets:
                            json.dump(tweet, file)
                            file.write("\n")
                    logging.info(f"Tweet with ID {tweet_id} removed from database.")
                else:
                    logging.warning(f"Tweet with ID {tweet_id} not found in database.")
            except Exception as e:
                logging.error(f"Error updating tweet info for deletion: {e}")
        else:
            # Retrieve username
            user_details = self.get_user_details()
            tweet_url = (
                f"https://twitter.com/{user_details['username']}/status/{tweet_id}"
            )

            tweet_info = {
                "tweet_id": tweet_id,
                "message": message,
                "tweet_url": tweet_url,
            }
            try:
                with open("tweets.json", "a") as file:
                    json.dump(tweet_info, file)
                    file.write("\n")
                logging.info(
                    f"Tweet info saved to the database.\nTweet URL: {tweet_url}"
                )
            except Exception as e:
                logging.error(f"Error saving tweet info: {e}")

    def delete_tweet(self, tweet_id):
        try:
            self.client.delete_tweet(tweet_id)
            logging.info("Tweet deleted successfully from twitter.com")
        except Exception as e:
            logging.error(f"Error occurred: {e}")


def cli():
    parser = argparse.ArgumentParser(description="Twitter Bot CLI")
    parser.add_argument("--creds", help="Path to the credentials file", required=True)
    parser.add_argument("--post", help="Path to the tweet file", required=False)
    parser.add_argument("--delete", help="Tweet ID to delete", required=False)

    args = parser.parse_args()
    bot = TwitterBot(args.creds)

    if args.post:
        try:
            reading_post_file = bot.read_post_file(args.post)
            tweeted_id = bot.post_tweet(args.post)
            print(f"\nTweeted:\n{reading_post_file}\n")

            # Save tweet information
            bot.save_tweet_info(tweet_id=tweeted_id, message=reading_post_file)
            # print("Tweet information saved.")
        except Exception as e:
            print(f"An error occurred while posting the tweet: {e}")

    if args.delete:
        try:
            bot.delete_tweet(args.delete)
            bot.save_tweet_info(args.delete, delete=True)
            # print(f"Tweet with ID {args.delete} deleted.")
        except Exception as e:
            print(f"An error occurred while deleting the tweet: {e}")


if __name__ == "__main__":
    cli()
