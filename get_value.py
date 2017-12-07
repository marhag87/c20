#!/bin/env python
import requests
from pyyamlconfig import load_config
from pathlib import Path

# Get tokens
home = str(Path.home())
config = load_config(f'{home}/.config/c20.yaml')
num_tokens = config.get('num_tokens')
currency = config.get('currency', 'USD').upper()
  
# Get token value
response = requests.get('https://us-central1-cryptodash1.cloudfunctions.net/fundValue')
value_per_token = response.json().get('nav_per_token')

if currency == 'USD':
  exchange_rate = 1
else:
  # Get dollar to chosen currency exchange rate
  response = requests.get('https://api.fixer.io/latest?base=USD')
  exchange_rate = response.json().get('rates').get(currency)
 
print(int(value_per_token*num_tokens*exchange_rate))
