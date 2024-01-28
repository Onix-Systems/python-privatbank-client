from django.urls import path
from .views import (
    PrivatView,
    PrivatClientInfo,
    PrivatBalanceView,
    PrivatStatementView,
    PrivatPaymentView,
    PrivatCurrenciesCashRate,
    PrivatCurrenciesNonCashRate,
)

app_name = "drf_privat"


urlpatterns = [
    path("", PrivatView.as_view()),
    path(
        "currency/cash_rate/",
        PrivatCurrenciesCashRate.as_view(),
        name="privat_currency_cash_rate_list",
    ),
    path(
        "currency/non_cash_rate/",
        PrivatCurrenciesNonCashRate.as_view(),
        name="privat_currency_non_cash_rate_list",
    ),
    path("info/", PrivatClientInfo.as_view(), name="privat_info_detail"),
    path("balance/", PrivatBalanceView.as_view(), name="privat_balance_detail"),
    path("statement/", PrivatStatementView.as_view(), name="privat_statement_list"),
    path("payment/", PrivatPaymentView.as_view(), name="privat_payment_create"),
]
