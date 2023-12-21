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
3. Finally, use this token and your account's iban to initialize client:

    from python_internal_privat.managers import PrivatManager

    token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    iban = "UAxxxxxxxxxxxxxxxxxxxxxxxxxxx"

    mng = PrivatManager(token, iban)

## Methods
Get currencies (cashe rate)
```python
>>> mng.get_currency(cashe_rate=True)
[
  {
    "ccy": "EUR",
    "base_ccy": "UAH",
    "buy": "40.80000",
    "sale": "41.80000"
  },
  {
    "ccy": "USD",
    "base_ccy": "UAH",
    "buy": "37.30000",
    "sale": "37.80000"
  }
]
```

Get currencies (cashe rate)

```python
>>> mng.get_currency(cashe_rate=False)
[
  {
    "ccy": "EUR",
    "base_ccy": "UAH",
    "buy": "40.44000",
    "sale": "41.49378"
  },
  {
    "ccy": "USD",
    "base_ccy": "UAH",
    "buy": "37.07500",
    "sale": "37.73585"
  }
]
```

Get client info
```python
>>> mng.get_client_info()
{
  "status": "SUCCESS",
  "type": "balances",
  "exist_next_page": false,
  "balances": [
    {
      "acc": "UAxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      "currency": "UAH",
      "balanceIn": "xx",
      "balanceInEq": "xx",
      "balanceOut": "xx",
      "balanceOutEq": "xx",
      "turnoverDebt": "xx",
      "turnoverDebtEq": "xx",
      "turnoverCred": "xx",
      "turnoverCredEq": "xx",
      "bgfIBrnm": " ",
      "brnm": "KPPN",
      "dpd": "xx.xx.xxxx xx:xx:xx",
      "nameACC": "xxxxxxxxxx",
      "state": "a",
      "atp": "T",
      "flmn": "KP",
      "date_open_acc_reg": "xx.xx.xxxx xx:xx:xx",
      "date_open_acc_sys": "xx.xx.xxxx xx:xx:xx",
      "date_close_acc": "xx.xx.xx xx:xx:xx",
      "is_final_bal": false
    }
  ]
}
```

Get balance
```python
>>> mng.get_balance()
{
  "balance": "x.xx"
}
```

Get statement
```python
>>> period = 31
>>> limit = 100
>>> mng.get_statement(period, limit)
{
  "status": "SUCCESS",
  "type": "transactions",
  "exist_next_page": false,
  "next_page_id": "2988607044_online",
  "transactions": [
    {
      "AUT_MY_CRF": "xxxxxxxxxx",
      "AUT_MY_MFO": "xxxxxx",
      "AUT_MY_ACC": "UAxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      "AUT_MY_NAM": "xxxxxxxxxx",
      "AUT_MY_MFO_NAME": "АТ КБ \"ПРИВАТБАНК\"",
      "AUT_MY_MFO_CITY": "Дніпро",
      "AUT_CNTR_CRF": "xxxxxxxxxx",
      "AUT_CNTR_MFO": "305299",
      "AUT_CNTR_ACC": "UAxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      "AUT_CNTR_NAM": "xxxxxxxxxx xxxxxxxxxx xxxxxxxxxx",
      "AUT_CNTR_MFO_NAME": "АТ КБ \"ПРИВАТБАНК\"",
      "AUT_CNTR_MFO_CITY": "Дніпро",
      "CCY": "UAH",
      "FL_REAL": "r",
      "PR_PR": "r",
      "DOC_TYP": "p",
      "NUM_DOC": "autoclient",
      "DAT_KL": "xx.xx.xxxx",
      "DAT_OD": "xx.xx.xxxx",
      "OSND": "xxxx **** **** xxxx test create pmnt to rest API",
      "SUM": "x.xx",
      "SUM_E": "x.xx",
      "REF": "xxxxxxxxxxxxxx",
      "REFN": "x",
      "TIM_P": "xx:xx",
      "DATE_TIME_DAT_OD_TIM_P": "xx.xx.xxxx xx:xx:xx",
      "ID": "2934180427",
      "TRANTYPE": "D",
      "DLR": "xxx/xxxxxxxx",
      "TECHNICAL_TRANSACTION_ID": "xxxxxxxxxx_online",
      "UETR": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "ULTMT": "N"
    },
    ...
  ]
}
```

Create payment
```python
>>> recipient = 5363************
>>> amount = 0.01
>>> mng.create_payment(recipient, amount)
{
  "payment_data": {
    "can_copy": "1",
    "can_edit": "1",
    "checked_on_pred": "true",
    "document_number": "autoclient",
    "document_type": "cr",
    "fields_for_sign": {
      "fields": [
        "payment_ref",
        "user_id",
        "document_type",
        "document_number",
        "payer_account",
        "payment_accept_date",
        "recipient_account",
        "recipient_card",
        "recipient_nceo",
        "payment_naming",
        "payment_amount",
        "payment_destination",
        "payment_ccy",
        "recipient_document_series",
        "recipient_document_number",
        "recipient_document_id_number",
        "recipient_country_code",
        "payer_ultmt_nceo",
        "payer_ultmt_name",
        "payer_ultmt_document_series",
        "payer_ultmt_document_number",
        "payer_ultmt_document_id_number",
        "recipient_ultmt_nceo",
        "recipient_ultmt_name",
        "recipient_ultmt_document_series",
        "recipient_ultmt_document_number",
        "recipient_ultmt_document_id_number",
        "struct_code",
        "struct_category",
        "struct_type"
      ],
      "version": "v3.4.0"
    },
    "id": "xxxxxxxxxxxxxxxxxxx",
    "internal_type": "card",
    "level_sign": {
      "1_sign_level": "false"
    },
    "payer_account": "UAxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "payer_bank_name": "АТ КБ \"ПРИВАТБАНК\"",
    "payer_name": "xxxxxx xxxxxxxx xxxxxxxxx",
    "payer_nceo": "xxxxxxxxxx",
    "payment_amount": "0.01",
    "payment_ccy": "UAH",
    "payment_date_unix": "xxxxxxxxxxxxxxxxxxx",
    "payment_destination": "test create pmnt to rest API",
    "payment_naming": "ПАО, ПАО КБ ПРИВАТБАНК",
    "payment_ref": "xxxxxxxxxxxxxxxxxxx",
    "payment_sign": [],
    "payment_status": "new",
    "payment_status_short": "n",
    "recipient_card": "xxxxxxxxxxxxxxxxx",
    "recipient_nceo": "xxxxxxxx",
    "service_update_utime": "xxxxxxxxxx",
    "source": "aup",
    "tabs": [
      "all",
      "saved"
    ],
    "user_id": "xxxxxxxx"
  },
  "payment_pack_ref": "xxx/xxxxxxxx",
  "payment_ref": "xxxxxxxxxxxxxxxxxxx"
}
```