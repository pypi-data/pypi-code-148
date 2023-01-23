from decimal import Decimal
from typing import Optional


class Transactions:
    def __init__(self, transactions_data: dict):
        self.status: str = transactions_data.get('status')
        self.payment_currency: str = transactions_data.get('paymentCurrency')
        self.sell_order_created_at: int = transactions_data.get('sellOrderCreatedAt')
        self.used_exchange_rate: int = transactions_data.get('usedExchangeRate')
        self.exchange_rate_decimals: int = transactions_data.get('exchangeRateDecimals')
        self.swapped_amount: int = transactions_data.get('swappedAmount')
        self.quantity: int = transactions_data.get('quantity')
        self.property_id: str = transactions_data.get('propertyId')
        self.created_at: int = transactions_data.get('createdAt')
        price: float = transactions_data.get('price')
        self.price: Optional[Decimal] = Decimal(str(price)) if price is not None else None
        self.id: str = transactions_data.get('id')
        self.buy_order_created_at: int = transactions_data.get('buyOrderCreatedAt')
        self.updated_at: int = transactions_data.get('updatedAt')


class Period:
    def __init__(self, period_data: dict):
        min_value: float = period_data.get('min')
        self.min: Optional[Decimal] = Decimal(str(min_value)) if min_value is not None else None
        max_value: float = period_data.get('max')
        self.max: Optional[Decimal] = Decimal(str(max_value)) if max_value is not None else None


class AllTime:
    def __init__(self, all_time_data: dict):
        self.min: int = all_time_data.get('min')
        self.max: int = all_time_data.get('max')


class Ranges:
    def __init__(self, ranges_data: dict):
        period_data: dict = ranges_data.get('period')
        self.period: Period = Period(period_data) if period_data is not None else None
        all_time_data: dict = ranges_data.get('allTime')
        self.all_time: AllTime = AllTime(all_time_data) if all_time_data is not None else None


class Documents:
    def __init__(self, documents_data: dict):
        self.title: str = documents_data.get('title')
        self.target_url: str = documents_data.get('targetUrl')


class Tags:
    def __init__(self, tags_data: dict):
        self.title: str = tags_data.get('title')
        self.end_date: int = tags_data.get('endDate')
        self.start_date: int = tags_data.get('startDate')


class Sales:
    def __init__(self, sales_data: dict):
        self.data_type: str = sales_data.get('dataType')
        self.buyer: str = sales_data.get('buyer')
        self.property_id: str = sales_data.get('propertyId')
        self.seller: str = sales_data.get('seller')
        self.created_at: int = sales_data.get('createdAt')
        self.record_date: str = sales_data.get('recordDate')
        self.is_lofty_sale: bool = sales_data.get('isLoftySale')
        self.address: str = sales_data.get('address')
        self.hc_address_id: int = sales_data.get('hc_addressId')
        self.hc_blockgroup_id: str = sales_data.get('hc_blockgroupId')
        self.record_document: str = sales_data.get('recordDocument')
        self.sk: str = sales_data.get('SK')
        self.event_type: str = sales_data.get('eventType')
        self.pk: str = sales_data.get('PK')
        self.price: int = sales_data.get('price')
        self.id: str = sales_data.get('id')
        self.record_type: str = sales_data.get('recordType')
        self.hc_block_id: str = sales_data.get('hc_blockId')
        self.apn: str = sales_data.get('apn')


class AvmHistory:
    def __init__(self, avm_history_data: dict):
        self.sales: list[Sales] = [Sales(item) for item in avm_history_data.get('sales')]
        self.prices: list = avm_history_data.get('prices')
        self.trend: list = avm_history_data.get('trend')


class Property:
    def __init__(self, property_data: dict):
        self.asset_creator: str = property_data.get('assetCreator')
        self.closing_costs: int = property_data.get('closing_costs')
        lng: float = property_data.get('lng')
        self.lng: Optional[Decimal] = Decimal(str(lng)) if lng is not None else None
        cap_rate: float = property_data.get('cap_rate')
        self.cap_rate: Optional[Decimal] = Decimal(str(cap_rate)) if cap_rate is not None else None
        self.market: str = property_data.get('market')
        self.state: str = property_data.get('state')
        self.address_line1: str = property_data.get('address_line1')
        self.asset_name: str = property_data.get('assetName')
        self.year_built: int = property_data.get('year_built')
        self.address_line2: str = property_data.get('address_line2')
        self.property_type: str = property_data.get('property_type')
        self.maintenance_reserve: int = property_data.get('maintenance_reserve')
        self.asset_unit: str = property_data.get('assetUnit')
        self.thumbnail: str = property_data.get('thumbnail')
        self.listing_fee: int = property_data.get('listing_fee')
        self.participant_app_id: int = property_data.get('participant_app_id')
        appreciation: float = property_data.get('appreciation')
        self.appreciation: Optional[Decimal] = Decimal(str(appreciation)) if appreciation is not None else None
        self.created_at: int = property_data.get('createdAt')
        self.llc_admin_fee_upfront: int = property_data.get('llc_admin_fee_upfront')
        self.address: str = property_data.get('address')
        self.beds: int = property_data.get('beds')
        self.capitalize_fees: bool = property_data.get('capitalize_fees')
        self.sale_price: int = property_data.get('sale_price')
        self.lease_begins_date: int = property_data.get('lease_begins_date')
        self.baths: int = property_data.get('baths')
        self.cash_flow: int = property_data.get('cash_flow')
        self.description: str = property_data.get('description')
        self.num_sold: int = property_data.get('num_sold')
        self.available_date: int = property_data.get('available_date')
        self.closing_date: int = property_data.get('closing_date')
        self.underlying_price: int = property_data.get('underlying_price')
        self.custom_occupancy: str = property_data.get('custom_occupancy')
        irr: float = property_data.get('irr')
        self.irr: Optional[Decimal] = Decimal(str(irr)) if irr is not None else None
        self.monthly_rent: int = property_data.get('monthly_rent')
        self.utilities_water_sewer: int = property_data.get('utilities_water_sewer')
        self.sellout_date: int = property_data.get('sellout_date')
        self.city: str = property_data.get('city')
        self.is_occupied: bool = property_data.get('is_occupied')
        self.documents: list[Documents] = [Documents(item) for item in property_data.get('documents')]
        self.hide_details: bool = property_data.get('hide_details')
        self.timeline_offering_complete: str = property_data.get('timeline_offering_complete')
        self.asset_id: int = property_data.get('assetId')
        coc: float = property_data.get('coc')
        self.coc: Optional[Decimal] = Decimal(str(coc)) if coc is not None else None
        self.is_deposit_made: bool = property_data.get('is_deposit_made')
        self.original_sellout_date: int = property_data.get('original_sellout_date')
        self.id: str = property_data.get('id')
        self.insurance: int = property_data.get('insurance')
        self.tags: list[Tags] = [Tags(item) for item in property_data.get('tags')]
        self.starting_date: int = property_data.get('starting_date')
        self.data_type: str = property_data.get('dataType')
        self.vacancy_reserve: int = property_data.get('vacancy_reserve')
        self.slug: str = property_data.get('slug')
        self.sqft: int = property_data.get('sqft')
        self.management_fees: int = property_data.get('management_fees')
        self.city_transfer_tax: int = property_data.get('city_transfer_tax')
        self.zipcode: int = property_data.get('zipcode')
        self.updated_at: int = property_data.get('updatedAt')
        self.images: list[str] = property_data.get('images')
        self.utilities: int = property_data.get('utilities')
        self.total_investment: int = property_data.get('total_investment')
        lat: float = property_data.get('lat')
        self.lat: Optional[Decimal] = Decimal(str(lat)) if lat is not None else None
        self.dao_app_id: int = property_data.get('dao_app_id')
        self.taxes: int = property_data.get('taxes')
        self.tokens: int = property_data.get('tokens')
        self.original_starting_date: int = property_data.get('original_starting_date')
        self.llc_admin_fee_yearly: int = property_data.get('llc_admin_fee_yearly')
        avm_history_data: dict = property_data.get('avmHistory')
        self.avm_history: AvmHistory = AvmHistory(avm_history_data) if avm_history_data is not None else None
        self.total_fees: int = property_data.get('total_fees')


class PropertyInfo:
    def __init__(self, property_info_data: dict):
        self.transactions: list[Transactions] = [Transactions(item) for item in property_info_data.get('transactions')]
        ranges_data: dict = property_info_data.get('ranges')
        self.ranges: Ranges = Ranges(ranges_data) if ranges_data is not None else None
        last_price: float = property_info_data.get('lastPrice')
        self.last_price: Optional[Decimal] = Decimal(str(last_price)) if last_price is not None else None
        trade_volume: float = property_info_data.get('tradeVolume')
        self.trade_volume: Optional[Decimal] = Decimal(str(trade_volume)) if trade_volume is not None else None
        property_data: dict = property_info_data.get('property')
        self.property: Property = Property(property_data) if property_data is not None else None
        self.secondary_enabled: bool = property_info_data.get('secondaryEnabled')
