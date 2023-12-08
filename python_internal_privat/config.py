from dotenv import load_dotenv
import os

load_dotenv()


PRIVATBANK_BALANCE_URI = os.getenv(
    'PRIVATBANK_BALANCE_URI', 'https://acp.privatbank.ua/api/statements/balance',
) 
PRIVATBANK_STATEMENT_URI = os.getenv(
    'PRIVATBANK_STATEMENT_URI', 'https://acp.privatbank.ua/api/statements/transactions',
)
PRIVATBANK_PAYMENT_URI = os.getenv(
    'PRIVATBANK_PAYMENT_URI', 'https://acp.privatbank.ua/api/proxy/payment/create_pred',
)
# PrivatBank cash rate (in branches)
PRIVATBANK_CURRENCY_CASHE_RATE_URI = os.getenv(
    'PRIVATBANK_CURRENCY_CASHE_RATE_URI', 'https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5'
)
# Non-cash rate of PrivatBank (conversion by cards, Privat24, replenishment of deposits)
PRIVATBANK_CURRENCY_NON_CASHE_RATE_URI = os.getenv(
    'PRIVATBANK_CURRENCY_NON_CASHE_RATE_URI', 'https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=11'
)

PAYMENT_DESTINATION = os.getenv(
    'PAYMENT_DESTINATION', 'test create payment to rest API'
)

DOCUMENT_NUMBER='autoclient'
RECIPIENT_NCEO='14360570'
PAYMENT_NAMING='ПАО, ПАО КБ ПРИВАТБАНК'
RECIPIENT_IFI="305299"
RECIPIENT_IFI_TEXT='ПАТ КБ \"ПРИВАТБАНК\"'
PAYMENT_CCY='UAH'
DOCUMENT_TYPE='cr'
DAY_UTC=86400   # 1 day (UNIX)