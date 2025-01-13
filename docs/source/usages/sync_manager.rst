SyncPrivatManager Methods
=========================

The ``SyncPrivatManager`` provides synchronous methods to interact with PrivatBank APIs, including:

- Performing HTTP requests
- Retrieving exchange rates, client information, account balances, transaction statements
- Creating payments

Methods
=======

session
-------
**Description:** Creates and returns a session object for making HTTP requests.

.. code-block:: python

   session = SyncPrivatManager().session()

**Response:** Returns a ``requests.sessions.Session`` instance.


sync_request
------------
**Description:** Performs an HTTP request using the specified method, URI, headers, and data.

.. code-block:: python

   method = "POST"
   uri = "https://api.someurl.com/resource"
   headers = {"Authorization": "Bearer your_token"}
   data = {"key": "value"}

   response = SyncPrivatManager().sync_request(method, uri, headers, data)
   print(response)

**Response:** A dictionary containing the server response. For example:

.. code-block:: json

   {
       "code": 200,
       "detail": {
           "key": "value"
       }
   }


get_currencies
--------------
**Description:** Retrieves exchange rates from PrivatBank APIs.

**Parameters:**
- ``cashe_rate`` (bool): Whether to fetch cash exchange rates.

.. code-block:: python

   cashe_rate = True
   currencies = SyncPrivatManager().get_currencies(cashe_rate)
   print(currencies)

**Response:** A dictionary with exchange rate information. Example:

.. code-block:: json

   {
       "code": 200,
       "detail": [
           {
               "currency": "USD",
               "rate": 27.5
           },
           {
               "currency": "EUR",
               "rate": 30.5
           }
       ]
   }

get_client_info
---------------
**Description:** Retrieves client account information such as balances and transactions.

.. code-block:: python

   client_info = SyncPrivatManager().get_client_info()
   print(client_info)

**Response:** A dictionary with client information. Example:

.. code-block:: json

   {
       "code": 200,
       "detail": {
           "name": "John Doe",
           "balances": [
               {
                   "account": "123456789",
                   "balanceOutEq": 1000.0
               }
           ]
       }
   }


get_balance
-----------
**Description:** Retrieves the account balance.

.. code-block:: python

   balance = SyncPrivatManager().get_balance()
   print(balance)

**Response:** A dictionary containing the balance. Example:

.. code-block:: json

   {
       "code": 200,
       "detail": {
           "balance": 1000.0
       }
   }


get_statement
-------------
**Description:** Retrieves the account statement for a specific period and transaction limit.

**Parameters:**
- ``period`` (int): Number of days prior to fetch transactions.
- ``limit`` (int): Maximum number of transactions to retrieve.

.. code-block:: python

   statement = SyncPrivatManager().get_statement(period=7, limit=10)
   print(statement)

**Response:** A dictionary containing transaction details. Example:

.. code-block:: json

   {
       "code": 200,
       "detail": [
           {
               "transactionId": "54321",
               "amount": -50.0,
               "date": "2023-10-01"
           },
           {
               "transactionId": "98765",
               "amount": 100.0,
               "date": "2023-09-30"
           }
       ]
   }


create_payment
--------------
**Description:** Creates a payment transaction to a specified recipient.

**Parameters:**
- ``recipient`` (str): The recipient's account identifier.
- ``amount`` (float): The amount to be transferred.

.. code-block:: python

   recipient = "987654321"
   amount = 500.0

   payment = SyncPrivatManager().create_payment(recipient, amount)
   print(payment)

**Response:** A dictionary denoting the payment response. Example:

.. code-block:: json

   {
       "code": 200,
       "detail": {
           "status": "Success",
           "transactionId": "12345"
       }
   }

.. tip:: Learn More. To learn more about deposits functionality, refer to::mod:`privatbank_api_client.sync_privat.manager`