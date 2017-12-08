#!/bin/env python
import requests
from pyyamlconfig import load_config
from pathlib import Path

# default message
default_msg = 'C20: Value: {curr_token_value} {currency} - Inc: {increase_num} {currency} ({percent_prefix}{increase_percent}%)'

# Get tokens
data = dict()
home = str(Path.home())
config = load_config(f'{home}/.config/c20.yaml')
status_fmt = config.get('status_format', default_msg)
data['num_tokens'] = config.get('num_tokens')
data['total_investment'] = config.get('init_investment', False)
data['currency'] = config.get('currency', 'USD').upper()

# Get token value
response = requests.get('https://us-central1-cryptodash1.cloudfunctions.net/fundValue')
data['value_per_token'] = response.json().get('nav_per_token')

if data['currency'] == 'USD':
  data['exchange_rate'] = 1
else:
  # Get dollar to chosen currency exchange rate
  response = requests.get('https://api.fixer.io/latest?base=USD')
  data['exchange_rate'] = response.json().get('rates').get(data['currency'])

# Calculate token val
data['curr_token_value'] = round(data['value_per_token']*data['num_tokens']*data['exchange_rate'], 2)
 
# Calculate value increase from investment amount
if data['total_investment']:
  data['increase_num'] = round(data['curr_token_value'] - data['total_investment'], 2)
  data['increase_percent'] = round((( \
    float(data['curr_token_value'])/ \
    float(data['total_investment'])) \
    - 1)*100, 1)

  data['percent_prefix'] =''
  if data['increase_percent'] > 0:
    data['percent_prefix'] = '+'

print(status_fmt.format(**data))
