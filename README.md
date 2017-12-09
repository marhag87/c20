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
nav - Token NAV value
token_sum - Total value for all your tokens in your currency
num_tokens - Number of tokens you have specified in config
currency - The currency you have chosen
total_investment - The amount of money you invested
exchange_rate - The current exchange rate to your currency from USD
growth_sum - The value increase from your investment cost to the current value_per_token * num_tokens
growth_percent - The percentage increase to your investment
```

Format String Examples
----------------------
Some examples when building your string format.

This is the default string format if none is specified
```
'C20: NAV: {nav} USD - Value: {token_sum} {currency} ({growth_percent})'
C20: NAV: 1.3022 USD - Value: 12990.78 SEK (+36.5)
```

```
'C20: Value: {token_sum} {currency} ({growth_percent})'
C20: Value: 12990.78 SEK (+36.5%)
```

```
'C20: NAV: {nav} - Tokens: {num_tokens} - Value: {token_sum}{currency}'
C20: NAV: 1.3005 - Tokens: 1181 - Value: 12973.82SEK
```

Usage
-----
```
pip install -r requirements.txt
echo "num_tokens: <tokens>" > ~/.config/c20.yaml
./get_value.py
```
