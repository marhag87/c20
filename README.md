c20
===

[![Build Status](https://travis-ci.org/marhag87/c20.svg?branch=master)](https://travis-ci.org/marhag87/c20)

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

<!--- example 10000 --->
```
C20: NAV: {nav} USD - Value: {token_sum} {currency} ({growth_percent})
C20: NAV: 1.3022 USD - Value: 13219.93 SEK (+32.2%)
```

<!--- example 10000 --->
```
C20: Value: {token_sum} {currency} ({growth_percent})
C20: Value: 13219.93 SEK (+32.2%)
```

<!--- example 10000 --->
```
C20: NAV: {nav} - Tokens: {num_tokens} - Value: {token_sum}{currency}
C20: NAV: 1.3022 - Tokens: 1200 - Value: 13219.93SEK
```

<!--- example 15000 --->
```
{token_sum}kr ({growth_percent})
13219.93kr (-11.9%)
```
Usage
-----
```
pip install c20
echo "num_tokens: <tokens>" > ~/.config/c20.yaml
echo "total_investment: <investment>" >> ~/.config/c20.yaml
c20
```

Development
-----------
```
pip install -e .
pip install -r requirements.txt
# Run tests
tox
```
