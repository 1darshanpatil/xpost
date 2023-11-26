![xpost-logo.png](xpost-logo.png)


# xpost - Python CLI for Twitter Operations

xpost is a command-line interface (CLI) Python package for interacting with Twitter. It allows users to tweet, add users, store API credentials securely, and delete tweets.

## Features

- **Tweeting**: Effortlessly post tweets from the command line.
- **Credential Storage**: Securely encrypt and store your Twitter API credentials using the robust `PBKDF2HMAC` algorithms, ensuring security.
- **Tweet Deletion**: Conveniently delete tweets with a simple command.

## Installation

Install xpost using pip:

```bash
pip install xpost
```

Verify the installation by checking the versio: 
```bash
xpost --version
```

## Usage

### Adding user Authentication Credentials
Securely store your Twitter API credentials:

```bash
$ x-config add_user
Enter a username to encrypt your APIs: usrDarwin
Set a password to secure your encrypted APIs:
Confirm your password:
Enter CLIENT_ID: client_id
Enter CLIENT_SECRET: client_secret
Enter API_KEY: api_key
Enter API_KEY_SECRET: apiKey
Enter BEARER_TOKEN: bTokn
Enter ACCESS_TOKEN: aTokn
Enter ACCESS_TOKEN_SECRET: aTokn_secret
Saving your encrypted data...
-Credentials encrypted and stored successfully.
Saving completed. Data stored at: ~/.tweet

User credentials successfully added.
```

### Viewing Stored Credentials
Check your encrypted credentials:
```bash
$ ls ~/.tweet
```
Or view decrypted credentials:
```python
>>> import xpost as x
>>> x.show_credentials()
Enter your username to decrypt your APIs: test_usr
Enter your password to decrypt your APIs:
{'CLIENT_ID': 'client_id', 'CLIENT_SECRET': 'client_secret', 'API_KEY': 'api_key', 'API_KEY_SECRET': 'apiKey', 'BEARER_TOKEN': 'bTokn', 'ACCESS_TOKEN': 'aTokn', 'ACCESS_TOKEN_SECRET': 'aTokn_secret'}
```


### Reset your APIs

Permanently delete all stored credentials:


To reset your APIs
```bash
$ x-config reset
Do you want to delete all data? [Y/n]: Y
WARNING: This will permanently delete all data, including production API keys. Confirm with 'Y' or cancel with 'N': Y
Processing deletion....

All user files in ~/.tweet have been successfully deleted.
Data deletion successfull.
```

## Command Usage Examples

Use the `x` command to perform tweeting operations. Below are examples of how to use the command:

### Posting a Tweet

To post a tweet directly message or from a text file:


```bash
$ x --post "Your message to be tweeted"
$ x --post  "path/to/text/file.txt"
```

Important: The username and password you provide are used for decrypting your encrypted API credentials.


```bash
$ x --post "Hello, X!"
Enter your username to decrypt your saved APIs: test_usr
Enter your password to decrypt your saved APIs:
INFO:root:Tweet successfully posted. Tweet ID: 1728786247492247770
Twitter post:
Hello, X!

INFO:root:Tweet info saved to the database.
Tweet URL: https://twitter.com/eulerDavinci/status/1728786247492247770
```


### Deleting a Tweet

Remove a tweet by its ID: 

```bash
$ x --delete <Tweet ID>
```

```bash
$ x --delete 1728786247492247770
Enter your username to decrypt your saved APIs: test_usr
Enter your password to decrypt your saved APIs:
INFO:root:Tweet deleted successfully from twitter.com
INFO:root:Tweet with ID 1728786247492247770 removed from database.
Tweet successfully deleted.
```



## License

xpost is released under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributions
Contributions are welcome from anyone, even if you are new to open source. If you are new and looking for some way to contribute, a good place to start is documentation and docstring.

Please note that all participants in this project are expected to follow our Code of Conduct. By participating in this project you agree to abide by its terms. See [CODE OF CONDUCTS](CODE_OF_CONDUCT.md)


## Support
For support, please open an issue on the GitHub repository.

## Tests
To ensure the functionality of `xpost`, you can run the following test commands. These commands test various functionalities of the xpost package.

First, import the necessary functions from `xpost`:

```python
from xpost import *
```
### Testing Configuration Commands
Use these functions to test configuration-related operations:
 * Adding a User: Adds a new user and stores their credentials. `add_user()`
 * Resets all stored credentials. `reset_credentials()`
 * Display the stored credentials. `show_credentials()`

### Testing Tweet Operations
To test tweeting functionalities, use these functions: 
 * Posts a new tweet. `post_tweet()`
 * Deletes an existing tweet. `delete_tweet()`


## Feedback and Feature Requests
Your feedback is incredibly valuable to us! For any feedback or feature requests, please reach out via email. We appreciate your input in enhancing xpost.

Please note, `xpost` is intentionally designed with a focus on basic features. This is to minimize distractions often associated with social media platforms, allowing users to concentrate on meaningful content creation. Our goal is to facilitate a simplified and efficient tweeting experience, enabling users to reflect on their past posts in the future.