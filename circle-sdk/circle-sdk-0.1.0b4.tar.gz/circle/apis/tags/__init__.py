# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from circle.apis.tag_to_api import tag_to_api

import enum


class TagValues(str, enum.Enum):
    PAYMENTS = "Payments"
    ONCHAIN_PAYMENTS = "On-chain payments"
    CARDS = "Cards"
    WIRES = "Wires"
    ACH = "ACH"
    SEPA = "SEPA"
    SETTLEMENTS = "Settlements"
    CHARGEBACKS = "Chargebacks"
    REVERSALS = "Reversals"
    BALANCES = "Balances"
    HEALTH = "Health"
    MANAGEMENT = "Management"
    ENCRYPTION = "Encryption"
    SUBSCRIPTIONS = "Subscriptions"
    STABLECOINS = "Stablecoins"
    CHANNELS = "Channels"
    WALLETS = "Wallets"
    TRANSFERS = "Transfers"
    PAYOUTS = "Payouts"
    ONCHAIN_PAYOUTS = "On-chain payouts"
    RETURNS = "Returns"
    PAYMENT_INTENTS = "Payment Intents"
    ADDRESS_BOOK = "Address Book"
    ADDRESSES = "Addresses"
    DEPOSITS = "Deposits"
    SEN = "SEN"
    SIGNET = "Signet"
