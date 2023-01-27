import typing_extensions

from circle.apis.tags import TagValues
from circle.apis.tags.payments_api import PaymentsApi
from circle.apis.tags.on_chain_payments_api import OnChainPaymentsApi
from circle.apis.tags.cards_api import CardsApi
from circle.apis.tags.wires_api import WiresApi
from circle.apis.tags.ach_api import ACHApi
from circle.apis.tags.sepa_api import SEPAApi
from circle.apis.tags.settlements_api import SettlementsApi
from circle.apis.tags.chargebacks_api import ChargebacksApi
from circle.apis.tags.reversals_api import ReversalsApi
from circle.apis.tags.balances_api import BalancesApi
from circle.apis.tags.health_api import HealthApi
from circle.apis.tags.management_api import ManagementApi
from circle.apis.tags.encryption_api import EncryptionApi
from circle.apis.tags.subscriptions_api import SubscriptionsApi
from circle.apis.tags.stablecoins_api import StablecoinsApi
from circle.apis.tags.channels_api import ChannelsApi
from circle.apis.tags.wallets_api import WalletsApi
from circle.apis.tags.transfers_api import TransfersApi
from circle.apis.tags.payouts_api import PayoutsApi
from circle.apis.tags.on_chain_payouts_api import OnChainPayoutsApi
from circle.apis.tags.returns_api import ReturnsApi
from circle.apis.tags.payment_intents_api import PaymentIntentsApi
from circle.apis.tags.address_book_api import AddressBookApi
from circle.apis.tags.addresses_api import AddressesApi
from circle.apis.tags.deposits_api import DepositsApi
from circle.apis.tags.sen_api import SENApi
from circle.apis.tags.signet_api import SignetApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.PAYMENTS: PaymentsApi,
        TagValues.ONCHAIN_PAYMENTS: OnChainPaymentsApi,
        TagValues.CARDS: CardsApi,
        TagValues.WIRES: WiresApi,
        TagValues.ACH: ACHApi,
        TagValues.SEPA: SEPAApi,
        TagValues.SETTLEMENTS: SettlementsApi,
        TagValues.CHARGEBACKS: ChargebacksApi,
        TagValues.REVERSALS: ReversalsApi,
        TagValues.BALANCES: BalancesApi,
        TagValues.HEALTH: HealthApi,
        TagValues.MANAGEMENT: ManagementApi,
        TagValues.ENCRYPTION: EncryptionApi,
        TagValues.SUBSCRIPTIONS: SubscriptionsApi,
        TagValues.STABLECOINS: StablecoinsApi,
        TagValues.CHANNELS: ChannelsApi,
        TagValues.WALLETS: WalletsApi,
        TagValues.TRANSFERS: TransfersApi,
        TagValues.PAYOUTS: PayoutsApi,
        TagValues.ONCHAIN_PAYOUTS: OnChainPayoutsApi,
        TagValues.RETURNS: ReturnsApi,
        TagValues.PAYMENT_INTENTS: PaymentIntentsApi,
        TagValues.ADDRESS_BOOK: AddressBookApi,
        TagValues.ADDRESSES: AddressesApi,
        TagValues.DEPOSITS: DepositsApi,
        TagValues.SEN: SENApi,
        TagValues.SIGNET: SignetApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.PAYMENTS: PaymentsApi,
        TagValues.ONCHAIN_PAYMENTS: OnChainPaymentsApi,
        TagValues.CARDS: CardsApi,
        TagValues.WIRES: WiresApi,
        TagValues.ACH: ACHApi,
        TagValues.SEPA: SEPAApi,
        TagValues.SETTLEMENTS: SettlementsApi,
        TagValues.CHARGEBACKS: ChargebacksApi,
        TagValues.REVERSALS: ReversalsApi,
        TagValues.BALANCES: BalancesApi,
        TagValues.HEALTH: HealthApi,
        TagValues.MANAGEMENT: ManagementApi,
        TagValues.ENCRYPTION: EncryptionApi,
        TagValues.SUBSCRIPTIONS: SubscriptionsApi,
        TagValues.STABLECOINS: StablecoinsApi,
        TagValues.CHANNELS: ChannelsApi,
        TagValues.WALLETS: WalletsApi,
        TagValues.TRANSFERS: TransfersApi,
        TagValues.PAYOUTS: PayoutsApi,
        TagValues.ONCHAIN_PAYOUTS: OnChainPayoutsApi,
        TagValues.RETURNS: ReturnsApi,
        TagValues.PAYMENT_INTENTS: PaymentIntentsApi,
        TagValues.ADDRESS_BOOK: AddressBookApi,
        TagValues.ADDRESSES: AddressesApi,
        TagValues.DEPOSITS: DepositsApi,
        TagValues.SEN: SENApi,
        TagValues.SIGNET: SignetApi,
    }
)
