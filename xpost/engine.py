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
    """
    A class to interact with Twitter using the Tweepy library. This class handles
    authentication with the Twitter API and provides methods for reading credentials
    and accessing the API. Requires the Tweepy library and expects Twitter API credentials
    in a specific JSON format.

    Attributes:
        creds_file (str): Path to the file containing Twitter API credentials.
        creds (dict): Twitter API credentials.
        client (tweepy.Client): Tweepy client for API interaction.
    """

    def __init__(self, creds_file):
        """
        Initialize the TwitterBot with credentials. Sets up the Tweepy client for Twitter API interaction.

        Args:
            creds_file (str): Path to the JSON file with Twitter credentials. The file should
                              contain keys: BEARER_TOKEN, API_KEY, API_KEY_SECRET,
                              ACCESS_TOKEN, ACCESS_TOKEN_SECRET.
        """
        self.creds_file = creds_file
        # self.creds = self.read_credentials()
        self.creds = creds_file
        self.client = self.authenticate()

    def read_credentials(self):
        """
        Read and return credentials from the credentials file. Expects a JSON file format.

        Returns:
            dict: The credentials for Twitter API.

        Raises:
            FileNotFoundError: If the credentials file is not found.
            JSONDecodeError: If there is an error in parsing the JSON file.
        """
        try:
            with open(self.creds_file, "r") as file:
                return json.load(file)
        except Exception as e:
            logging.error(f"Error reading credentials: {e}")
            sys.exit(1)

    def authenticate(self):
        """
        Authenticate with Twitter API using credentials. Sets up the Tweepy client.

        Returns:
            tweepy.Client: The authenticated Tweepy client.

        Raises:
            KeyError: If a required credential is missing.
            tweepy.TweepyException: If there is an error during authentication.
        """
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
        """
        Read and return the tweet message from a plain text file.

        Args:
            post_file (str): Path to the text file containing the message to be posted.

        Returns:
            str: The tweet message.

        Raises:
            FileNotFoundError: If the specified file is not found.
            Exception: For other errors that occur while reading the file.
        """
        try:
            with open(post_file, "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            return post_file
        except Exception as e:
            logging.error(f"Error reading post file: {e}")
            sys.exit(1)

    def post_tweet(self, post_file):
        """
        Post a tweet on Twitter using the message from the specified file.

        Args:
            post_file (str): Path to the text file containing the message to be posted.

        Returns:
            str: The ID of the successfully posted tweet.

        Raises:
            Exception: If the tweet exceeds 280 characters or an error occurs while posting.
        """
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
        """
        Retrieve and return the Twitter user details of the authenticated account.

        Returns:
            dict: A dictionary containing user details such as username.

        Raises:
            Exception: If an error occurs while fetching user details.
        """
        try:
            user_details = self.client.get_me()
            username = user_details.data.username
            return {"username": username}
        except Exception as e:
            logging.error(f"Error retrieving user details: {e}")

    def save_tweet_info(self, tweet_id, message=None, delete=False):
        """
        Save or remove tweet information in the 'tweets.json' file.

        Args:
            tweet_id (str): The ID of the tweet.
            message (str, optional): The tweet message. Defaults to None.
            delete (bool, optional): Flag to indicate if the tweet is to be deleted. Defaults to False.

        Raises:
            Exception: For any error that occurs while updating the file.
        """

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
        """
        Delete a tweet from Twitter based on its ID.

        Args:
            tweet_id (str): The ID of the tweet to be deleted.

        Raises:
            Exception: If an error occurs during the deletion process.
        """
        try:
            self.client.delete_tweet(tweet_id)
            logging.info("Tweet deleted successfully from twitter.com")
        except Exception as e:
            logging.error(f"Error occurred: {e}")


def cli():
    """
    This function serves as a command-line interface (CLI) for a Twitter bot. It allows users to perform various actions
    with Twitter through the command line by parsing arguments and invoking the appropriate methods of a TwitterBot object.

    The CLI provides three main functionalities:
    1. Posting a tweet: Users can specify the path to a file containing the tweet's content using the `--post` argument.
    2. Deleting a tweet: Users can delete a tweet by providing its ID with the `--delete` argument.
    3. Specifying credentials: Users must provide the path to a credentials file using the `--creds` argument.
    This file is required for the bot to authenticate with Twitter's API.

    The function first parses the command-line arguments. If the `--post` argument is provided, it attempts to read
    the tweet's content from the specified file and then post the tweet, handling any exceptions that occur.
    If the `--delete` argument is provided, it attempts to delete the tweet with the given ID, also handling exceptions.

    Exceptions during posting or deleting are caught and printed to the console, allowing the user to understand
    what went wrong without crashing the program.

    Args:
        None

    Returns:
        None
    """

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
