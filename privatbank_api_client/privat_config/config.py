from dotenv import load_dotenv
import os

load_dotenv()


PRIVATBANK_BALANCE_URI_BODY = "{0}?acc={1}&startDate={2}"
PRIVATBANK_STATEMENT_URI_BODY = "{0}?acc={1}&startDate={2}&limit={3}"

PRIVATBANK_BALANCE_URI = os.getenv(
    "PRIVATBANK_BALANCE_URI",
    "https://acp.privatbank.ua/api/statements/balance",
)
PRIVATBANK_STATEMENT_URI = os.getenv(
    "PRIVATBANK_STATEMENT_URI",
    "https://acp.privatbank.ua/api/statements/transactions",
)
PRIVATBANK_PAYMENT_URI = os.getenv(
    "PRIVATBANK_PAYMENT_URI",
    "https://acp.privatbank.ua/api/proxy/payment/create_pred",
)
# PrivatBank cash rate (in branches)
PRIVATBANK_CURRENCIES_CASHE_RATE_URI = os.getenv(
    "PRIVATBANK_CURRENCIES_CASHE_RATE_URI",
    "https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5",
)
# Non-cash rate of PrivatBank (conversion by cards, Privat24, replenishment of deposits)
PRIVATBANK_CURRENCIES_NON_CASHE_RATE_URI = os.getenv(
    "PRIVATBANK_CURRENCIES_NON_CASHE_RATE_URI",
    "https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=11",
)

DOCUMENT_NUMBER = os.getenv("DOCUMENT_NUMBER", "autoclient")
RECIPIENT_NCEO = os.getenv("RECIPIENT_NCEO", "14360570")
PAYMENT_NAMING = os.getenv("PAYMENT_NAMING", "ПАО, ПАО КБ ПРИВАТБАНК")
RECIPIENT_IFI = os.getenv("RECIPIENT_IFI", "305299")
RECIPIENT_IFI_TEXT = os.getenv("RECIPIENT_IFI_TEXT", 'ПАТ КБ "ПРИВАТБАНК"')
PAYMENT_DESTINATION = os.getenv("PAYMENT_DESTINATION", "test create pmnt to rest API")
PAYMENT_CCY = os.getenv("PAYMENT_CCY", "UAH")
DOCUMENT_TYPE = os.getenv("DOCUMENT_TYPE", "cr")

PRIVAT_CREATE_SUCCESS_CODE = 201
PRIVAT_CREATE_SUCCESS_DETAIL = "Privat added successfully."

PRIVAT_UPDATE_SUCCESS_CODE = 200
PRIVAT_UPDATE_SUCCESS_DETAIL = "Privat chanched successfully."

PRIVAT_DELETE_SUCCESS_CODE = 204
PRIVAT_DELETE_SUCCESS_DETAIL = "Privat deleted successfully."

PRIVAT_EXISTS_EXCEPTION_CODE = 400
PRIVAT_EXISTS_EXCEPTION_DETAIL = "Your privat is already exists."

PRIVAT_DOES_NOT_EXISTS_EXCEPTION_CODE = 404
PRIVAT_DOES_NOT_EXISTS_EXCEPTION_DETAIL = "Your privat has not been added yet."
