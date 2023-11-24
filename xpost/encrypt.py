import json
import fire
import os
import shutil
import base64
import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend


class CredentialManager:
    """
    Manages encryption, decryption, and storage of Twitter API credentials.
    Uses Fernet symmetric encryption for securing credentials.

    Attributes:
        username (str): The username associated with the credentials.
        credentials_file (str): Path to the encrypted credentials file.
    """

    def __init__(self, username):
        """
        Initializes the CredentialManager with a username.

        Args:
            username (str): The username for which the credentials are managed.
        """
        self.username = username
        self.credentials_file = os.path.expanduser(
            f"~/.tweet/{username}_encrypted_credentials"
        )

    @staticmethod
    def generate_key(password: str):
        """
        Generates an encryption key based on the provided password using PBKDF2HMAC.

        Args:
            password (str): The password used to generate the encryption key.

        Returns:
            bytes: The generated encryption key.
        """
        # Use PBKDF2HMAC to generate a key
        password_bytes = password.encode()
        salt = (
            b"\x10" * 16
        )  # Fixed salt (alternatively, use a random salt and store it)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend(),
        )
        key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
        return key

    @staticmethod
    def encrypt_data(data: str, password: str):
        """
        Encrypts data using Fernet symmetric encryption.

        Args:
            data (str): The plaintext data to be encrypted.
            password (str): The password used for generating the encryption key.

        Returns:
            bytes: The encrypted data.
        """
        key = CredentialManager.generate_key(password)
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(data.encode())
        return encrypted_data

    @staticmethod
    def decrypt_data(encrypted_data: bytes, password: str):
        """
        Decrypts data that was encrypted with Fernet symmetric encryption.

        Args:
            encrypted_data (bytes): The data to be decrypted.
            password (str): The password used for generating the decryption key.

        Returns:
            str: The decrypted plaintext data.
        """
        key = CredentialManager.generate_key(password)
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data)
        return decrypted_data.decode()

    def prompt_for_credentials(self):
        """
        Prompts the user to enter their Twitter API credentials.

        Returns:
            dict: A dictionary containing the entered credentials.
        """
        client_id = input("Enter CLIENT_ID: ")
        client_secret = input("Enter CLIENT_SECRET: ")
        api_key = input("Enter API_KEY: ")
        api_key_secret = input("Enter API_KEY_SECRET: ")
        bearer_token = input("Enter BEARER_TOKEN: ")
        access_token = input("Enter ACCESS_TOKEN: ")
        access_token_secret = input("Enter ACCESS_TOKEN_SECRET: ")

        credentials = {
            "CLIENT_ID": client_id,
            "CLIENT_SECRET": client_secret,
            "API_KEY": api_key,
            "API_KEY_SECRET": api_key_secret,
            "BEARER_TOKEN": bearer_token,
            "ACCESS_TOKEN": access_token,
            "ACCESS_TOKEN_SECRET": access_token_secret,
        }
        return credentials

    def save_credentials(self, encrypted_data, password):
        """
        Saves encrypted credentials to a file.

        Args:
            encrypted_data (bytes): The encrypted data to be saved.
            password (str): The password used for encryption.
        """
        # encrypted_data = self.encrypt_data(json.dumps(credentials), password)
        os.makedirs(os.path.dirname(self.credentials_file), exist_ok=True)
        with open(self.credentials_file, "wb") as file:
            file.write(encrypted_data)
        print("Credentials encrypted and stored successfully.")

    def load_credentials(self, password):
        """
        Loads and decrypts the Twitter API credentials form the stored file.

        Args:
            password (str): The password used to decrypt the credentials.

        Returns:
            dict: A dictionary containing the decrypted credentials.

        Raises:
            FileNotFoundError: If the credentials file does not exist.
            cryptography.fernet.InvalidToken: If the provided password is incorrect.
        """
        try:
            with open(self.credentials_file, "rb") as file:
                encrypted_data = file.read()
            decrypted_data = self.decrypt_data(encrypted_data, password)
            return json.loads(decrypted_data)
        except FileNotFoundError:
            print(
                "Credentials file not found. This could be due to a non-existent username, a typo in the username, or the credentials file might have been moved or deleted."
            )
        except cryptography.fernet.InvalidToken:
            print("Invalid password provided. Unable to decrypt credentials.")
        # except Exception as e:
        #    print(f"An unexpected error occurred: {e}")


def force_delete():
    """
    Deletes all user files in the `~/.tweet` directory, including the credentials.

    This method is used to completely remove all stored data related to the TwitterBot

    Raise:
        Exception: For any unexpected error that occurs during the deletion process.

    """
    tweet_dir = os.path.expanduser("~/.tweet")
    try:
        # Check if the directory exists
        if os.path.exists(tweet_dir):
            # Use shutil.rmtree to delete the directory and all its contents
            shutil.rmtree(tweet_dir)
            print("All user files in ~/.tweet have been successfully deleted.")
        else:
            print("No ~/.tweet directory found.")
            print("This could be due to no data was loaded before testing.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


class CredentialCLI:
    """
    A command-line interface for managing Twitter API credentials. It provides functionalities
    to load, store, and reset credentials using the CredentialManager class.

    Attributes:
        manager (CredentialManager): An instance of CredentialManager for handling credentials.
    """

    def __init__(self):
        """
        Initializes the CredentialCLI with no CredentialManager instance.
        """
        self.manager = None

    def load(self, usr, passwd):
        """
        Loads and returns the Twitter API credentials for a specified user.

        Args:
            usr (str): The username associated with the credentials.
            passwd (str): The password to decrypt the credentials.

        Returns:
            dict: The loaded credentials, if successful.

        Prints:
            Error message, if an exception occurs.
        """
        self.manager = CredentialManager(usr)
        try:
            loaded_creds = self.manager.load_credentials(passwd)
            return loaded_creds
        #            print("Credentials: ", loaded_creds)
        except Exception as e:
            print(f"Error: {e}")

    def store(self, usr, passwd):
        """
        Stores Twitter API credentials for a specified user after encrypting them.

        Args:
            usr (str): The username associated with the credentials.
            passwd (str): The password to encrypt the credentials.

        Prints:
            The process of storing credentials and confirmation messages.
        """
        self.manager = CredentialManager(usr)
        taking_apis = self.manager.prompt_for_credentials()
        encrypted_data = self.manager.encrypt_data(json.dumps(taking_apis), passwd)
        print("Your encrypted data is:", encrypted_data)
        print("Saving your encrypted data at: ~/.tweet")
        self.manager.save_credentials(encrypted_data, passwd)
        print("")
        # print("Please make sure you delete your .bash_history after storing your password!")

    def reset(self):
        """
        Provides an option to delete all stored credentials and data related to the TwitterBot.

        Prompts the user for confirmation before proceeding with the deletion.

        Prints:
            Confirmation messages and status of the reset operation.
        """
        delte_data = input("You want to delete all the data [Y/n]: ")
        if delte_data.lower() == "y":
            confirm_delete = input(
                "Are you absolutely sure? This action is not recommended and cannot be undone. It will also delete your production API keys. To confirm deletion, type 'Y'. To cancel, type 'N': "
            )
            if confirm_delete.lower() in ["y", "yes"]:
                force_delete()
            else:
                print("Operation cancelled. Find your files at ~/.tweet")
        else:
            print("Operation cancelled. Find your files at ~/.tweet")


if __name__ == "__main__":
    fire.Fire(CredentialCLI)
