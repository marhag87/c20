c20
===

Keep track of the value of your https://crypto20.com/ investment.

Config
------
```
num_tokens: <int> - Number of tokens owned>
currency: <string> - Currency to show token value in (eg. GBP) Default is 'USD'
total_investment: <int> - Total amount invested in C20 *Should be the same currency as {currency}*)
status_format: <string> - Custom format string for the message
```

Format String Options
---------------------
```
value_per_token - Token NAV value
num_tokens - Number of tokens you have specified in config
currency - The currency you have chosen
total_investment - The amount of money you invested
exchange_rate - The current exchange rate to your currency from USD
increase_num - The value increase from your investment cost to the current value_per_token * num_tokens
increase_percent - The percentage increase to your investment
precent_prefix - Adds a + or a minus infront of the increase_percent (eg. +23.33%, -34.44%)
```

Format String Examples
----------------------
Some examples when building your string format.

This is the default string format if none is specified
```
'C20: NAV: {value_per_token} USD - Value: {curr_token_value} {currency} ({percent_prefix}{increase_percent})'
C20: NAV: 1.3022 USD - Value: 12990.78 SEK (+36.5)
```

```
'C20: Value: {curr_token_value} {currency} ({percent_prefix}{increase_percent}%)'
C20: Value: 12990.78 SEK (+36.5%)
```

```
'C20: NAV: {value_per_token} - Tokens: {num_tokens} - Value: {curr_token_value}{currency}'
C20: NAV: 1.3005 - Tokens: 1181 - Value: 12973.82SEK
```

Usage
-----
```
pip install -r requirements.txt
echo "num_tokens: <tokens>" > ~/.config/c20.yaml
./get_value.py
```
