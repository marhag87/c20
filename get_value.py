#!/bin/env python
import requests
from pyyamlconfig import load_config
from pathlib import Path

# Get tokens
home = str(Path.home())
config = load_config(f'{home}/.config/c20.yaml')
num_tokens = config.get('num_tokens')

# Get token value
response = requests.get('https://us-central1-cryptodash1.cloudfunctions.net/fundValue')
value_per_token = response.json().get('nav_per_token')

# Get dollar to sek value
response = requests.get('https://api.fixer.io/latest?base=USD')
sek = response.json().get('rates').get('SEK')


print(int(value_per_token*num_tokens*sek))
