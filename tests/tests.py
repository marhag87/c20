#!/bin/env python
import unittest
import mock
import re
import pyyamlconfig
mock_load_config = mock.Mock()
pyyamlconfig.load_config = mock_load_config
from c20 import C20
from c20.c20 import (
    TOKEN_ERROR,
    CURRENCY_ERROR,
    CURRENCY_NOT_FOUND,
    MISSING_TOTAL_INVESTMENT,
)


class TestC20(unittest.TestCase):
    def setUp(self):
        self.mock_load_config = mock_load_config
        self.mock_get = mock.patch('requests.get').start()
        self.mock_response = mock.Mock()
        self.mock_json = mock.Mock()
        self.mock_response.json = self.mock_json
        self.mock_response.status_code = 200
        self.mock_json.return_value = {'nav_per_token': 1.5}
        self.mock_get.return_value = self.mock_response
        self.mock_load_config.return_value = {'num_tokens': 2, 'total_investment': 200}
        self.c20 = C20()

    def test_default_string(self):
        """
        Test that status returns a sane string
        """
        self.assertEqual(
            self.c20.status(),
            'C20: Value: 3.0 USD - Inc: -197.0 USD (-98.5%)',
        )

    def test_value_per_token_exception(self):
        """
        Test that value_per_token raises on failure
        """
        self.mock_response.status_code = 404
        with self.assertRaises(Exception) as err:
            print(self.c20.value_per_token)
        self.assertEqual(
            str(err.exception),
            TOKEN_ERROR,
        )

    def test_exchange_rate_usd(self):
        """
        Test that USD always has an exchange rate of 1
        """
        self.assertEqual(
            self.c20.exchange_rate,
            1.0,
        )

    def test_exchange_rate_sek(self):
        """
        Test that setting a custom currency fetches the currency
        """
        self.mock_load_config.return_value = {
            'num_tokens': 2,
            'total_investment': 200,
            'currency': 'sek',
        }
        self.mock_json.return_value = {
            'nav_per_token': 1.5,
            'USD_SEK': {
                'val': 7,
            }
        }
        c20sek = C20()
        self.assertEqual(
            c20sek.exchange_rate,
            7,
        )

    def test_exchange_rate_exception(self):
        """
        Test that exchange_rate raises on failure
        """
        self.mock_load_config.return_value = {
            'num_tokens': 2,
            'total_investment': 200,
            'currency': 'sek',
        }
        self.mock_response.status_code = 404
        c20exception = C20()
        with self.assertRaises(Exception) as err:
            print(c20exception.exchange_rate)
        self.assertEqual(
            str(err.exception),
            CURRENCY_ERROR,
        )

    def test_exchange_rate_currency_missing(self):
        """
        Test that exchange_rate raises if the currency doesn't exist
        """
        self.mock_load_config.return_value = {
            'num_tokens': 2,
            'total_investment': 200,
            'currency': 'sek',
        }
        self.mock_json.return_value = {
            'nav_per_token': 1.5,
            'USD_SEK': {}
        }
        c20missing = C20()
        with self.assertRaises(Exception) as err:
            print(c20missing.exchange_rate)
        self.assertEqual(
            str(err.exception),
            CURRENCY_NOT_FOUND,
        )

    def test_curr_token_value(self):
        """
        Test that curr_token_value returns a sane number
        """
        self.assertEqual(
            self.c20.curr_token_value,
            3.0,
        )

    def test_increase(self):
        """
        Test that increase_num and increase_percent returns sane values
        """
        self.assertEqual(
            self.c20.increase_num,
            -197.0,
        )
        self.assertEqual(
            self.c20.increase_percent,
            '-98.5%',
        )

        self.mock_load_config.return_value = {
            'num_tokens': 200,
            'total_investment': 10,
        }
        c20increase = C20()
        self.assertEqual(
            c20increase.increase_num,
            290,
        )
        self.assertEqual(
            c20increase.increase_percent,
            '+2900.0%',
        )

    def test_status(self):
        """
        Test that a custom status_format returns the expected values
        """
        self.mock_load_config.return_value = {
            'num_tokens': 2,
            'total_investment': 200,
            'status_format': (
                '{nav} {token_sum} {num_tokens} {currency} {total_investment} '
                '{exchange_rate} {growth_sum} {growth_percent}'
            ),
        }
        c20status = C20()
        self.assertEqual(
            c20status.status(),
            '1.5 3.0 2 USD 200 1.0 -197.0 -98.5%',
        )

    def test_empty_total_investment(self):
        """
        Test that increase_num and increase_percent returns None when total_investment is not set
        """
        self.mock_load_config.return_value = {
            'num_tokens': 2,
        }
        c20empty = C20()
        with self.assertRaises(Exception) as err:
            print(c20empty.increase_num)
        self.assertEqual(
            str(err.exception),
            MISSING_TOTAL_INVESTMENT,
        )

        with self.assertRaises(Exception) as err:
            print(c20empty.increase_percent)
        self.assertEqual(
            str(err.exception),
            MISSING_TOTAL_INVESTMENT,
        )

    def test_readme_examples(self):
        """
        Test that the examples in the readme give the expected result
        """
        with open('README.md') as file:
            started = False
            previous_line = ''
            line_number = 0
            investment = 10000
            for line in file.readlines():
                if re.match('^<!--- example .* --->\\n$', line):
                    started = True
                    investment = float(line.split(' ')[2])
                if started:
                    if line_number == 3:
                        self.mock_load_config.return_value = {
                            'num_tokens': 1200,
                            'total_investment': investment,
                            'currency': 'sek',
                            'status_format': previous_line,
                        }
                        self.mock_json.return_value = {
                            'nav_per_token': 1.3022,
                            'USD_SEK': {
                                'val': 8.46,
                            }
                        }
                        c20status = C20()
                        self.assertEqual(
                            c20status.status(),
                            line,
                        )
                        started = False
                        line_number = 0
                        continue
                    previous_line = line
                    line_number = line_number + 1


if __name__ == '__main__':
    unittest.main()
