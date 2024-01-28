## python-internal-privat
This module is designed for quick interaction with the privatbank API.

## Name
privatbank-api-client

## Installation
This framework is published at the PyPI, install it with pip:

  1.This package makes it possible to use module methods in synchronous frameworks:

    pip install privatbank-api-client[http]

  2.This package makes it possible to use module methods in asynchronous frameworks:

    pip install privatbank-api-client[aio]

  3.This package makes it possible to use ready-made views with a synchronous script based on the Django Rest framework:

    pip install privatbank-api-client[drf]

  To get started, add the following packages to INSTALLED_APPS:

    INSTALLED_APPS = [
        ...
        'rest_framework',
        'drf_privat',
    ]

  Include drf_mono urls to your urls.py:

      urlpatterns = [
          ...
          path('privat/', include('drf_privat.urls', namespace='drf_privat')),
      ]

  4.This package makes it possible to use ready-made routers with an asynchronous script based on the FastAPI framework:

    pip install privatbank-api-client[fastapi]

  5.To install all packages at once:

    pip install privatbank-api-client[all]

## Usage
1. First, install the "Autoclient" module of the "Privat24 for Business" complex designed to serve corporate clients and private entrepreneurs."Autoclient" is software that allows you to set up periodic automatic receipt of statements / account balances and import payments into Privat24.
2. Then use this token to obtain personal data of a privatbank client.
3. For a synchronous request use this token and your account's iban to initialize client:

    from sync_privat.manager import SyncPrivatManager

    token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    iban = "UAxxxxxxxxxxxxxxxxxxxxxxxxxxx"

    mng = SyncPrivatManager(token, iban)

3. For a asynchronous request use this token and your account's iban to initialize client:

    from async_privat.manager import AsyncPrivatManager

    token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    iban = "UAxxxxxxxxxxxxxxxxxxxxxxxxxxx"

    mng = AsyncPrivatManager(token, iban)

## Methods
Get currencies (cashe rate)
PrivatBank cash rate in branches
```python
>>> mng.get_currencies(cashe_rate=True)
{
  "code": 200,  
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
}

```

Get currencies (non cashe rate)
Non-cash rate of PrivatBank conversion by cards, Privat24, replenishment of deposits
```python
>>> mng.get_currency(cashe_rate=False)
{
  "code": 200,
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
}

```

Get client info
```python
>>> mng.get_client_info()
{
  "code": 200,
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
}
```

Get balance
```python
>>> mng.get_balance()
{
  "code": 200,
  {
    "balance": "x.xx"
  }
}
```

Get statement
```python
>>> period = 31
>>> limit = 100
>>> mng.get_statement(period, limit)
{
  "code": 200,
  {
    "status": "SUCCESS",
    "type": "transactions",
    "exist_next_page": 'false',
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
}
```

Create payment
```python
>>> recipient = 5363************
>>> amount = 0.01
>>> mng.create_payment(recipient, amount)
{
  "code": 200,
  {
    "code": 201,
    "detail": {
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
        "payer_name": "ФОП xxxxxx xxxxx xxxxxxx",
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
        "recipient_card": "xxxxxxxxxxxxxxxx",
        "recipient_nceo": "xxxxxxxx",
        "service_update_utime": "xxxxxxxxxx",
        "source": "aup",
        "tabs": [
          "all",
          "saved"
        ],
        "user_id": "xxxxxxxx"
      },
      "payment_pack_ref": "xxxxxxxxxxxx",
      "payment_ref": "xxxxxxxxxxxxxxxxxxx"
    }
  }
}
```