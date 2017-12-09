"""
Module for calculating value of c20 tokens
"""
from pathlib import Path
from typing import Optional
import requests
from pyyamlconfig import load_config

TOKEN_ERROR = 'Could not get token data'
CURRENCY_ERROR = 'Could not get currency data'
CURRENCY_NOT_FOUND = 'Could not find the currency'
DEFAULT_MESSAGE = (
    'C20: Value: {token_sum} {currency} - Inc: {growth_sum} {currency} ({growth_percent})'
)


class C20:
    """Class for calculating value of c20 tokens"""
    def __init__(self):
        self._value_per_token = None
        self._exchange_rate = None
        self._config = None

    @property
    def config(self):
        """Fetch config from ~/.config/c20.yaml"""
        if self._config is None:
            self._config = load_config(f'{Path.home()}/.config/c20.yaml')
        return self._config

    @property
    def status_fmt(self):
        """Fetch status format config"""
        return self.config.get('status_format', DEFAULT_MESSAGE)

    @property
    def num_tokens(self):
        """Fetch number of tokens config"""
        return self.config.get('num_tokens')

    @property
    def total_investment(self):
        """Fetch total investment config"""
        return self.config.get('total_investment', False)

    @property
    def currency(self):
        """Fetch currency config"""
        return self.config.get('currency', 'USD').upper()

    @property
    def value_per_token(self) -> float:
        """Fetch token value"""
        if self._value_per_token is None:
            response = requests.get('https://crypto20.com/status')
            if response.status_code == 200:
                self._value_per_token = response.json().get('nav_per_token')
            else:
                raise Exception(TOKEN_ERROR)
        return self._value_per_token

    @property
    def exchange_rate(self) -> float:
        """Fetch exchange rate if not in USD"""
        if self._exchange_rate is None:
            if self.currency == 'USD':
                self._exchange_rate = 1.0
            else:
                response = requests.get(
                    f'https://api.fixer.io/latest?symbols={self.currency}&base=USD',
                )
                if response.status_code == 200:
                    self._exchange_rate = response.json().get('rates').get(self.currency)
                else:
                    raise Exception(CURRENCY_ERROR)
                if self._exchange_rate is None:
                    raise Exception(CURRENCY_NOT_FOUND)
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

    @property
    def increase_percent(self) -> Optional[str]:
        """Increase in percent, if total investment has been specified"""
        if self.total_investment:
            percent = ((self.curr_token_value/self.total_investment) - 1)*100
            return "{0:+.01f}%".format(percent)

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
            "growth_percent": self.increase_percent,
        }

    def status(self) -> str:
        """Return formatted status string"""
        return self.status_fmt.format(**self.data)
