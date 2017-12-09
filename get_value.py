#!/bin/env python
import requests
from pyyamlconfig import load_config
from pathlib import Path
from typing import Optional


class C20:
    def __init__(self):
        self.default_msg = 'C20: Value: {token_sum} {currency} - Inc: {growth_sum} {currency} ({growth_percent})'
        self.home = str(Path.home())
        self.config = load_config(f'{self.home}/.config/c20.yaml')
        self.status_fmt = self.config.get('status_format', self.default_msg)
        self.num_tokens = self.config.get('num_tokens')
        self.total_investment = self.config.get('init_investment', False)
        self.currency = self.config.get('currency', 'USD').upper()
        self._value_per_token = None
        self._exchange_rate = None

    @property
    def value_per_token(self) -> float:
        """Fetch token value"""
        if self._value_per_token is None:
            response = requests.get('https://us-central1-cryptodash1.cloudfunctions.net/fundValue')
            if response.status_code == 200:
                self._value_per_token = response.json().get('nav_per_token')
            else:
                raise Exception('Could not get token data')
        return self._value_per_token

    @property
    def exchange_rate(self) -> float:
        """Fetch exchange rate if not in USD"""
        if self._exchange_rate is None:
            if self.currency == 'USD':
                self._exchange_rate = 1.0
            else:
                response = requests.get('https://api.fixer.io/latest?base=USD')
                if response.status_code == 200:
                    self._exchange_rate = response.json().get('rates').get(self.currency)
                else:
                    raise Exception('Could not get currency data')
        return self._exchange_rate

    @property
    def curr_token_value(self) -> float:
        """Current token value"""
        return round(self.value_per_token * self.num_tokens * self.exchange_rate, 2)

    @property
    def increase_num(self) -> Optional[float]:
        """Value increase, if total investment has been specified"""
        if self.total_investment:
            return round(self.curr_token_value - self.total_investment, 2)
        else:
            return None

    @property
    def increase_percent(self) -> Optional[float]:
        """Increase in percent, if total investment has been specified"""
        if self.total_investment:
            return ((self.curr_token_value/self.total_investment) - 1)*100
        else:
            return None

    @property
    def data(self) -> dict:
        """Data dict with all variables that can be used in status_format"""
        return {
            "nav": self.value_per_token,
            "token_sum": self.curr_token_value,
            "num_tokens": self.num_tokens,
            "currency": self.currency,
            "total_investment": self.total_investment,
            "exchange_rate": self.exchange_rate,
            "growth_sum": self.increase_num,
            "growth_percent": "{0:+.01f}%".format(self.increase_percent),
        }

    def status(self) -> str:
        return self.status_fmt.format(**self.data)


if __name__ == '__main__':
    c20 = C20()
    print(c20.status())
