Async PrivatBank API Client Usage
=================================

This FastAPI application serves as an asynchronous client for interacting with the PrivatBank API.
It facilitates operations such as managing Privat model data, fetching currency rates, retrieving client information,
checking account balances, managing account statements, and executing payments.
Designed similar to the Django DRF app, the FastAPI app leverages asynchronous capabilities for higher performance.

Manage Privat Model (CRUD Operations)
--------------------------------------
Perform Create, Read, Update, and Delete (CRUD) actions on the Privat model.

**POST - Add Privat model entry**

.. code-block:: http

   POST /privat HTTP/1.1
   Content-Type: application/json
   Host: example.com

**Request Body Example**:

.. code-block:: json

   {
      "name": "Example",
      "description": "Sample entry"
   }

**Response Example**:

.. code-block:: json

   {
      "id": 1,
      "name": "Example",
      "description": "Sample entry",
      "created_at": "2023-11-01T12:00:00"
   }

**PUT - Update Privat model entry**

.. code-block:: http

   PUT /privat/{id} HTTP/1.1
   Content-Type: application/json
   Host: example.com

**Request Body Example**:

.. code-block:: json

   {
      "name": "Updated Name",
      "description": "Updated description"
   }

**Response Example**:

.. code-block:: json

   {
      "id": 1,
      "name": "Updated Name",
      "description": "Updated description",
      "updated_at": "2023-11-01T12:30:00"
   }

**DELETE - Remove Privat model entry**

.. code-block:: http

   DELETE /privat/{id} HTTP/1.1
   Host: example.com

**Response Example**:

.. code-block:: json

   {
      "message": "Privat model entry deleted successfully."
   }

Fetch Currency Rates
---------------------
Retrieve current currency rates.

**GET - /currencies**

The `/currencies` endpoint supports fetching rates for both cash and non-cash transactions.

**Request Example**:

.. code-block:: http

   GET /currencies?type=cash HTTP/1.1
   Host: example.com

**Response Example**:

.. code-block:: json

   {
      "currencies": [
         {
            "currency": "USD",
            "rate": 27.5,
            "type": "cash"
         },
         {
            "currency": "EUR",
            "rate": 31.0,
            "type": "cash"
         }
      ]
   }

Retrieve Client Information
---------------------------
Fetch detailed information about a client.

**GET - /client_info**

**Request Example**:

.. code-block:: http

   GET /client_info?client_id=123 HTTP/1.1
   Host: example.com

**Successful Response Example**:

.. code-block:: json

   {
      "client_id": 123,
      "name": "John Doe",
      "email": "john.doe@example.com",
      "phone": "+380123456789"
   }

**Error Response Example**:

.. code-block:: json

   {
      "detail": "Client not found."
   }

Fetch Account Balance
---------------------
Retrieve the balance of a specific account.

**GET - /balance**

**Request Example**:

.. code-block:: http

   GET /balance?account_id=456 HTTP/1.1
   Host: example.com

**Response Example**:

.. code-block:: json

   {
      "account_id": 456,
      "currency": "UAH",
      "balance": 10000.50
   }

Fetch Account Statements
------------------------
Retrieve detailed account statements by posting request data.

**Request Body Example**:


.. code-block:: http

   POST /statement HTTP/1.1
   Content-Type: application/json

   {
      "account_id": 456,
      "start_date": "2023-10-01",
      "end_date": "2023-10-31"
   }

**Successful Response Example**:

.. code-block:: json

   {
      "account_id": 456,
      "statements": [
         {
            "date": "2023-10-01",
            "amount": -500.0,
            "description": "ATM withdrawal"
         },
         {
            "date": "2023-10-05",
            "amount": 2000.0,
            "description": "Salary deposit"
         }
      ]
   }

**Error Response Example**:

.. code-block:: json

   {
      "detail": "No statements found for the provided date range."
   }

Execute Payment
---------------
Process a payment through the PrivatBank API.



**Request Body Example**:

.. code-block:: http

   POST /payment HTTP/1.1
   Content-Type: application/json

   {
      "source_account": 456,
      "destination_account": 789,
      "amount": 1500.0,
      "currency": "UAH",
      "description": "Payment for services"
   }

**Successful Response Example**:

.. code-block:: json

   {
      "status": "success",
      "transaction_id": "TRX12345678",
      "description": "Payment successfully processed."
   }

**Error Response Example**:

.. code-block:: json

   {
      "status": "error",
      "detail": "Insufficient funds."
   }
