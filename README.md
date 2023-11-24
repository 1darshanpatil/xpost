![xpost-logo.png](xpost-logo.png)


# xpost - Python CLI for Twitter Operations

xpost is a command-line interface (CLI) Python package for interacting with Twitter. It allows users to tweet, store authentication credentials securely, and delete tweets.

## Features

- **Tweeting**: Post tweets directly from the command line.
- **Credential Storage**: Securely store your Twitter authentication credentials.
- **Tweet Deletion**: Delete tweets easily.

## Installation

Install xpost using pip:

```bash
pip install xpost
```

## Usage

### Help
`tweet-config -h`
```bash
$ tweet-config -h
usage: tweet-config [-h] {store,reset} ...

Twitter Bot CLI - Configuration Operations

positional arguments:
  {store,reset}

optional arguments:
  -h, --help     show this help message and exit
```


`tweet -h
`
```bash
$ tweet -h
usage: tweet [-h] [--creds CREDS] [--post POST] [--delete DELETE]

Twitter Bot CLI - Tweeting Operations

optional arguments:
  -h, --help       show this help message and exit
  --creds CREDS    Provide username and password in format username:password
  --post POST      Path to the tweet file
  --delete DELETE  Tweet ID to delete
```

### Storing Authentication Credentials

Store your Twitter authentication credentials securely with the `tweet-config store` command. Input your username, password, and the required Twitter API credentials as prompted.

```bash
# Start the process to store credentials
$ tweet-config store nameusr wordpass
Enter CLIENT_ID: client_id
Enter CLIENT_SECRET: client_secret
Enter API_KEY: api_key
Enter API_KEY_SECRET: api_key_secret
Enter BEARER_TOKEN: bearer_token
Enter ACCESS_TOKEN: access_token
Enter ACCESS_TOKEN_SECRET: access_token_secret
Your encrypted data is: b'gAAAAABlXwDpvIDqeRv_ZGroxjHEixflTzRChT9tdftSf6egl1k5gQWfghcsEMNkqGbS0FH2g7YsN9WhMNZLSvKOzUqdbm_Hbo279K8B-OwUc2UqhAxPiNdj-RhwUIFXs5G3ZJrHQDixh-O6JzSCbjJKBo9-7Hdf0bU3h5X8_SNJOh6fcxOnK1tyE1WZ-bkke0vu2h0_ZCl9_vGXRLRLdKpYxiAl07tFmMcceeuRb7q1ZE1zyjBMmdUcWjmAzwMkMYdW5NLtj-MS3eEwyLO-x9LEYMLgIWYBVjezk1anGDwerHrt4eI_MJn9DYuRAPw8Hzy7MAJEKezJgNYOXg8p9TY3YXDHCwm4vczqMW0arpFFfLR4s_dDMaYGVEgnSMTKa_yLQ-MytLBJ'
Saving your encrypted data at: ~/.tweet
Credentials encrypted and stored successfully.
```

#### Caution
Note: The above command presents a significant security risk because your Bash history records your `username` and `password`, which are used to encrypt the APIs. Therefore, it is strongly recommended to delete your Bash history to protect sensitive information.

```bash
history -d $(history 1 | awk '{print $1}')
```

Your encrypted credentials will be saved at `~/.tweet`.
```bash
$ ls ~/.tweet
nameusr_encrypted_credentials
```

### Viewing Stored Credentials

To view your stored credentials:

```bash
ls ~/.tweet
cat ~/.tweet/<username>_encrypted_credentials
```


To delete all stored credentials:
### Reset your APIs

To reset your APIs
```bash
$ tweet-config reset
You want to delete all the data [Y/n]: y
Are you absolutely sure? This action is not recommended and cannot be undone. It will also delete your production API keys. To confirm deletion, type 'Y'. To cancel, type 'N': y
All user files in ~/.tweet have been successfully deleted.
```

## Command Usage Examples

Use the `tweet` command to perform tweeting operations. Below are examples of how to use the command:

### Posting a Tweet

To post a tweet directly with a message:


```bash
$ tweet --creds <username>:<password> --post "Your message to be tweeted"
$ tweet --creds <username>:<password> --post  "path/to/text/file.txt"
```

Important: The username and password you provide are used for decrypting your encrypted API credentials.


```bash
$ tweet --creds usrName:passWord@69 --post "This is your xpost tweet!"
INFO:root:Tweet successfully posted. Tweet ID: 1727582713442689485

Tweeted:
This is your xpost tweet!

INFO:root:Tweet info saved to the database.
Tweet URL: https://twitter.com/eulerDavinci/status/1727582713442689485
```


### Deleting a Tweet

To delete a tweet:

```bash
tweet --creds <username>:<password> --delete <Tweet ID>
```

```bash
$ tweet --creds usrName:passWord@69 --delete 1727582713442689485
INFO:root:Tweet deleted successfully from twitter.com
INFO:root:Tweet with ID 1727582713442689485 removed from database.
```



## License

xpost is released under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributions

Contributions are welcome! Please read our contributing guidelines before submitting pull requests.

## Support

For support, please open an issue on the GitHub repository or contact.

