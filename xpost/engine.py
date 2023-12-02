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
    A class to interact with the Twitter API for operations like posting tweets, deleting tweets, and fetching user details.

    Parameters
    ==========

    creds_files : str
        The file path where the Twitter API credentials are stored.

    Attributes
    ==========

    creds_file : str
        The path to the credentials file.
    client : tweepy.Client
        An authenticated Tweepy client instance for interacting with Twitter API.

    Raises
    ======

    Exception
        Raised during the initialization if there is an error in reading credentials,
        authenticating the client, or in any of the Twitter API interactions.

    Methods
    =======

    read_credentials
        Reads the Twitter API credentials from the credentials file.
    authenticate
        Authenticates with the Twitter API using the credentials.
    read_post_file
        Reads and returns the content of a post file.
    post_tweet
        Posts a tweet the content from the specified file.
    get_user_details
        Fetches and returns the Twitter user details.
    save_tweet_info
        Saves or deletes tweet information in a local file.
    delete_tweet
        Delete a tweet based on the given tweet ID.

    See Also
    ========

    tweepy.Client: The Tweepy library client class for accessing Twitter API.

    Notes
    =====

    This class is designed to facilitate some of the common Twitter operations via
    the Twitter API. It requires proper authentication using Twitter API credentials.
    It allows reading tweets from a file, posting tweets, deleting tweets, and saving tweet
    information. Error handling is implemented for all interactions with the TWitter API
    to ensure smooth execution.

    """

    def __init__(self, creds_file):
        self.creds_file = creds_file
        # self.creds = self.read_credentials()
        self.creds = creds_file
        self.client = self.authenticate()

    def read_credentials(self):
        """
        Reads the TWitter API credentials from the credentials file.

        Raises
        ======
        Exception
            If there is an error reading the credentials file.

        Returns
        =======
        dict
            A dictionary containing the loaded API credentials.
        """
        try:
            with open(self.creds_file, "r") as file:
                return json.load(file)
        except Exception as e:
            logging.error(f"Error reading credentials: {e}")
            sys.exit(1)

    def authenticate(self):
        """
        Authenticates with the Twitter API using the credentials.

        Raises
        ======
        KeyError
            If any of the required credentials is missing the creds dictionary.
        Exception
            For any other errors during authentication.

        Returns
        =======
        tweepy.Client
            An authenticated TWeepy client instance.
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
        Reads and returns the content of a post file.

        Parameters
        ==========
        post_file : str
            The file path where the post content is stored.

        Raises
        ======
        FileNotFoundError
           If the specified post file does not exist.
        Exception
            If there is an error reading the post file.

        Returns
        =======
        str
            The content of the post file.
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
        Posts a tweet with content from the specified file

        Parameters
        ==========
        post-file : str
            The file path containing the tweet content.

        Raises
        ======
        Exception
            If there is an error posting the tweet or if the tweet the character limit.

        Returns
        =======
        str
            The ID of the successfully posted tweet.
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
        Fetches and returns the TWitter user details.

        Raises
        ======
        Exception
            If there is an error retrieving user details

        Returns
        =======
        dict
            A dictionary containing the user's details associated with twitter account.
        """
        try:
            user_details = self.client.get_me()
            username = user_details.data.username
            return {"username": username}
        except Exception as e:
            logging.error(f"Error retrieving user details: {e}")

    def save_tweet_info(self, tweet_id, message=None, delete=False):
        """
        Saves or deleted information about a tweet in a local file and from twitter server.

        Parameters
        ==========k
        tweet_id : str
            The ID of the tweet.
        message : str, optional
            The message content of the tweet. Default is None.
        delete : bool,  optional
            Whether to delete the tweet info. Default is False.

        Raises
        ======
        Exception
            If there is an error in processing tweet information.

        Notes
        =====
        This method either appends the tweet information to a file or removes the specified tweet's information from the file, based
        on the 'delete' parameter.
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
        Deletes a tweet based on the given tweet ID.

        Parameters
        ==========
        tweet_id : str
            The ID of the tweet to be deleted.

        Raises
        ======
        Exception
            If there is an error during the tweet deletion.

        Notes
        =====
        This method uses the Tweepy client to delete a tweet from Twitter. It requires
        the tweet ID of the tweet to be deleted.
        """
        try:
            self.client.delete_tweet(tweet_id)
            logging.info("Tweet deleted successfully from twitter.com")
        except Exception as e:
            logging.error(f"Error occurred: {e}")


def cli():
    """
    Command Line Interface for the TWitterBot.

    This function sets up an argument parser and processes command line arguments to
    perform operations like posting and deleting tweets.

    Parameters
    ----------
    None

    Returns
    -------
    None

    Raises
    ------
    Exception
        If there is an error in processing the command line arguments or in executing the Twitter operations.

    Notes
    -----
    The function supports command line arguments for specifying the credentials file,
    the tweet post file, and the tweet ID for deletion. Based on the provided arguments, it either posts a new tweet
    or deletes an existing tweet.


                    +--------------------------------------------------+
                    | This function is not in use!                     |
                    | We call the TwitterBot class for CLI commands.   |
                    | However, this function is used for testing the   |
                    | TwitterBot class.                                |
                    +--------------------------------------------------+
    Example
    -------
    $ python3 engine.py --creds path/to/the/API/file/.json [--post msg.txt] [--delete tweet_id]

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
    
