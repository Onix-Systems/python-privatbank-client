# python-internal-privat
This module is designed for quick interaction with the privatbank API.

## Name
python-internal-privat

## Installation
This framework is published at the TestPyPI, install it with pip:

    py -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ python-internal-privat

## Usage
1. First, install the "Autoclient" module of the "Privat24 for Business" complex designed to serve corporate clients and private entrepreneurs."Autoclient" is software that allows you to set up periodic automatic receipt of statements / account balances and import payments into Privat24.
2. Then use this token to obtain personal data of a privatbank client.
3. Finally, use this token and your account's iban to retrieve your personal data and create payments.