import json
import fire
import os
import time
import shutil
import base64
import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend


def colored(text, color_code):
    """
    Applies a color to the given text using ANSi escape codes.
    """
    return f"\033[{color_code}m{text}\033[0m"


class CredentialManager:
    """
    Manages the encryption and decryption of Twitter API credentials.

    This class provides methods to prompt for user credentials, encrypt them,
    save them to a file, and decrypt them from the file.

    Attributes
    ==========
    username : str
        The username associated with the credentials.
    credentials_file : str
        The file path where the encrypted credentials are stored.

    Methods
    =======
    prompt_for_credentials()
        Prompts the user for Twitter API credentials and returns them in a dictionary.
    Save_credentials(encrypted_data, password)
        Saves the encrypted credentials to a file.
    load_credentials(password)
        Loads and decrypts the credentials from a file.
    """

    def __init__(self, username):
        """
        username : str
            The username associated with the credentials.
        """
        self.username = username
        self.credentials_file = os.path.expanduser(f"~/.tweet/{username}-PBKDF2HMAC")

    @staticmethod
    def generate_key(password: str):
        """
        Generates a cryptographic key from a password using PBKDF2-HMAC

        Parameters
        ==========
        password : str
            The password to generate the key.

        Returns
        =======
        bytes
            The generated cryptographic key.
        """
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
        Encrypts the given data using a password.

        Parameters
        ==========
        data : str
            The data to encrypt.
        password : str
            The password used for encryption

        Returns
        =======
        bytes
            The encrypted data.
        """
        key = CredentialManager.generate_key(password)
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(data.encode())
        return encrypted_data

    @staticmethod
    def decrypt_data(encrypted_data: bytes, password: str):
        """
        Decrypts the given encrypted data using a password.

        Parameters
        ==========
        encrypted_data : bytes
            The data to decrypt.
        password : str
            The password used for decryption.

        Returns
        =======
        str
            The decrypted data.
        """
        key = CredentialManager.generate_key(password)
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data)
        return decrypted_data.decode()

    def prompt_for_credentials(self):
        """
        Prompts the user to input Twitter API credentials.

        Returns
        =======
        dict
            A dictionary containing the input credentials.
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
        Saves the encrypted credentials to a file.

        Parameters
        ==========
        encrypted_data : bytes
            The encrypted credentials
        password : str
            The password used for encryption.

        Notes
        =====
        The credentials are encrypted and stored in a file specific to the username.
        """
        # encrypted_data = self.encrypt_data(json.dumps(credentials), password)
        os.makedirs(os.path.dirname(self.credentials_file), exist_ok=True)
        with open(self.credentials_file, "wb") as file:
            file.write(encrypted_data)
        print(colored("Credentials encrypted and stored successfully.", 92))

    def load_credentials(self, password):
        """
        Loads and decrypts the credentials from a file.

        Parameters
        ==========
        password : str
            The password used for decryption.
        Returns
        =======
        dict
            The decrypt credentials.

        Raises
        ======
        FileNotFoundError
            If the credentials file does not exist.
        cryptographic.fernet.InvalidToken
            If the provided password is incorrect.
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
    Deletes the ~/.tweet directory and all its contents.

    This function forcefully removes the directory where user credentials and other data are stored.
    It's used to completely reset the environment.

    Returns
    =======

    str
        'success' if the deletion is successful, None if there's no ~/.tweet directory.

    Raises
    ======
    Exception
        If an unexpected error occurs during the deletion process.
    """
    tweet_dir = os.path.expanduser("~/.tweet")
    try:
        # Check if the directory exists
        if os.path.exists(tweet_dir):
            # Use shutil.rmtree to delete the directory and all its contents
            shutil.rmtree(tweet_dir)
            print("All user files in ~/.tweet have been successfully deleted.")
            return "success"
        else:
            print(colored("No ~/.tweet directory found.", 91))
            print("This could be due to no data was loaded before testing.")
            return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


class CredentialCLI:
    """
    Command Line Interface for managing Twitter credentials.

    This class provides a CLI for loading, storing, and resetting credentials
    using the CredentialManager class.

    Attributes
    ----------
    manager : CredentialManager or None
        An instance of CredentialManager, initialized when loading or storing credentials.

    Methods
    -------
    load(usr, passwd)
        Loads the credentials for the specified user.
    store(usr, passwd)
        Stores the credentials for the specified user.
    reset()
        Resets the credentials by deleting all stored data.
    """

    def __init__(self):
        self.manager = None

    def load(self, usr, passwd):
        """
        Loads the credentials for a given user.

        Parameters
        ----------
        usr : str
            The username for which to load credentials.
        passwd : str
            The password to decrypt the credentials.

        Returns
        -------
        dict or None
            The loaded credentials as a dictionary, or None if an error occurs.

        Notes
        -----
        If an error occurs during loading, the error message is printed.
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
        Stores the credentials for a given user.

        Parameters
        ----------
        usr : str
            The username for which to store credentials.
        passwd : str
            The password to encrypt the credentials.

        Notes
        -----
        This method prompts the user for credential details, encrypts them, and then
        saves them to a file. Visual feedback is provided during the saving process.
        """
        self.manager = CredentialManager(usr)
        taking_apis = self.manager.prompt_for_credentials()
        encrypted_data = self.manager.encrypt_data(json.dumps(taking_apis), passwd)

        print(colored("Saving your encrypted data...", 92))
        for char in ["\\", "|", "/", "-"]:
            print(f"\r{char}", end="")
            time.sleep(0.75)

        self.manager.save_credentials(encrypted_data, passwd)
        print(colored("\rSaving completed. Data stored at: ~/.tweet", 92))
        print("")
        # Reminder or warning message can be added here if needed, possibly in a different color.

    def reset(self):
        """
        Resets the credentials by deleting all stored data.

        Notes
        -----
        This method prompts the user for confirmation before deleting data.
        It provides visual feedback during the deletion process.
        """
        delete_data = input("Do you want to delete all data? [Y/n]: ")
        if delete_data.lower() == "y":
            red_warning = colored(
                "WARNING: This will permanently delete all data, including production API keys. Confirm with 'Y' or cancel with 'N': ",
                91,
            )
            confirm_delete = input(red_warning)

            if confirm_delete.lower() in ["y", "yes"]:
                print("Processing deletion", end="")
                for char in [".", "..", "...", "...."]:
                    print(f"\rProcessing deletion{char}", end="")
                    time.sleep(0.5)
                print("\n")
                files_deleted = force_delete()
                if files_deleted == "success":
                    print(colored("\rData deletion successfull.       ", 92))
            else:
                print(colored("Operation cancelled. Your files remain at ~/.tweet", 92))
        else:
            print(colored("Operation cancelled. Your files remain at ~/.tweet", 92))


if __name__ == "__main__":
    fire.Fire(CredentialCLI)
