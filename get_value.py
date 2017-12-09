#!/bin/env python
import requests
from pyyamlconfig import load_config
from pathlib import Path

# default message
default_msg = 'C20: Value: {token_sum} {currency} - Inc: {growth_sum} {currency} ({growth_percent})'

# Get tokens
home = str(Path.home())
config = load_config(f'{home}/.config/c20.yaml')
status_fmt = config.get('status_format', default_msg)
num_tokens = config.get('num_tokens')
total_investment = config.get('init_investment', False)
currency = config.get('currency', 'USD').upper()

increase_num = None
increase_percent = None
percent_prefix = ''

# Get token value
response = requests.get('https://us-central1-cryptodash1.cloudfunctions.net/fundValue')
value_per_token = response.json().get('nav_per_token')

if currency == 'USD':
  exchange_rate = 1
else:
  # Get dollar to chosen currency exchange rate
  response = requests.get('https://api.fixer.io/latest?base=USD')
  exchange_rate = response.json().get('rates').get(currency)

# Calculate token val
curr_token_value = round(value_per_token*num_tokens*exchange_rate, 2)
 
# Calculate value increase from investment amount
if total_investment:
  increase_num = round(curr_token_value - total_investment, 2)
  increase_percent = round((( \
    float(curr_token_value)/ \
    float(total_investment)) \
    - 1)*100, 1)

  if increase_percent > 0:
    percent_prefix = '+'
  

# Prepare data dict
data = {
  "nav": value_per_token,
  "token_sum": curr_token_value,
  "num_tokens": num_tokens,
  "currency": currency,
  "total_investment": total_investment,
  "exchange_rate": exchange_rate,
  "growth_sum": increase_num,
  "growth_percent": f'{percent_prefix}{increase_percent}%'
}

print(status_fmt.format(**data))
