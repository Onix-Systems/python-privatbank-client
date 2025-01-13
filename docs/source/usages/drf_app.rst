DRF PrivatBank API Client Usage
===============================

This document provides examples of how to use the `privatbank_apiclient/drf_privat` Django Rest Framework (DRF) app
for managing PrivatBank API operations.

Overview
--------
The `privatbank_apiclient/drf_privat` app provides API endpoints for interacting with PrivatBank services. The endpoints enable:

- Managing user credentials for the PrivatBank API (CRUD operations)
- Fetching currency exchange rates (cash/non-cash)
- Retrieving client information
- Fetching account balance and transaction statements
- Creating payment transactions


Manage Privat Model (CRUD Operations)
-------------------------------------

- **Endpoint:** `/`

- **Methods:** POST, PUT, DELETE

- **Description:** Handles operations for the `Privat` model linked with a user's account.


Create New Privat Instance (POST Example)
-----------------------------------------

   **Request:**

   .. code-block:: http

       POST / HTTP/1.1
       Content-Type: application/json

       {
           "privat_token": "your_privattokenhere",
           "iban_UAH": "UA123456789012345678901234567"
       }

   **Response (Success):**

   .. code-block:: json

       {
           "code": 201,
           "message": "Privat instance created successfully."
       }

   **Response (Error - Instance Exists):**

   .. code-block:: json


       {
           "code": 400,
           "message": "A Privat instance already exists for the user."
       }

Update Existing Privat Instance (PUT Example)
---------------------------------------------

   **Request:**

   .. code-block:: http

       PUT / HTTP/1.1
       Content-Type: application/json

       {
           "privat_token": "newtokenabc123",
           "iban_UAH": "UA123456789012345678901234567"
       }

   **Response (Success):**

   .. code-block:: json

       {
           "code": 200,
           "message": "Privat instance updated successfully."
       }


   **Response (Error - Instance Not Found):**

   .. code-block:: json

       {
           "code": 404,
           "message": "Privat instance does not exist."
       }

Delete Privat Instance (DELETE Example)
---------------------------------------

   .. code-block:: http

          DELETE / HTTP/1.1

   **Response (Success):**

   .. code-block:: json

       {
           "code": 200,
           "message": "Privat instance deleted successfully."
       }


   **Response (Error - Instance Not Found):**

   .. code-block:: json

       {
           "code": 404,
           "message": "Privat instance does not exist."
       }


Fetch Currency Rates
---------------------
   - **Cash Rates:**
   - **Endpoint:** `/currency/cash_rate/`
   - **Method:** GET

   - **Non-Cash Rates:**
   - **Endpoint:** `/currency/non_cash_rate/`
   - **Method:** GET

   Request (Cash Rates Example)

   .. code-block:: http

       GET /currency/cash_rate/ HTTP/1.1

   **Response:**

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

Retrieve Client Information
---------------------------
   - **Endpoint:** `/info/`
   - **Method:** GET
   - **Description:** Retrieves account and personal information associated with stored Privat credentials.



   .. code-block:: http

       GET /info/ HTTP/1.1

   **Response (Success):**

   .. code-block:: json

       {
           "code": 200,
           "detail": {
               "name": "John Doe",
               "balances": [
                   {
                       "account": "12345678",
                       "balanceOutEq": 5000.0
                   }
               ]
           }
       }


   **Response (Error - Credentials Missing):**

   .. code-block:: json

       {
           "code": 404,
           "message": "Privat instance does not exist."
       }


Fetch Account Balance
---------------------

   - **Endpoint:** `/balance/`
   - **Method:** GET
   - **Description:** Retrieves the account balance.


   .. code-block:: http

       GET /balance/ HTTP/1.1

   **Response:**

   .. code-block:: json

       {
           "code": 200,
           "detail": {
               "balance": 1000.0
           }
       }

Fetch Account Statements
------------------------

   - **Endpoint:** `/statement/`
   - **Method:** POST

   **Request**

   .. code-block:: http

       POST /statement/ HTTP/1.1
       Content-Type: application/json

       {
           "period": 7,
           "limit": 5
       }

   **Response (Success):**

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

   **Response (Error - Credentials Missing):**

   .. code-block:: json

       {
           "code": 404,
           "message": "Privat instance does not exist."
       }


Execute Payment
---------------

   - **Endpoint:** `/payment/`
   - **Method:** POST
   - **Description:** Processes payments to the specified recipient.

    **Request**

   .. code-block:: http

       POST /payment/ HTTP/1.1
       Content-Type: application/json

       {
           "recipient": "987654321",
           "amount": 500.0
       }

   **Response (Success):**

   .. code-block:: json

       {
           "code": 200,
           "detail": {
               "status": "Success",
               "transactionId": "12345"
           }
       }


   **Response (Error - Credentials Missing):**

   .. code-block:: json

       {
           "code": 404,
           "message": "Privat instance does not exist."
       }