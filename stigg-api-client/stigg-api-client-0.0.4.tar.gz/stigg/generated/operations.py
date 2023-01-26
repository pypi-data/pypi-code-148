import sgqlc.types
import sgqlc.operation
from . import schema

_schema = schema
_schema_root = _schema.schema

__all__ = ('Operations',)


def fragment_coupon_fragment():
    _frag = sgqlc.operation.Fragment(_schema.Coupon, 'CouponFragment')
    _frag.id()
    _frag.discount_value()
    _frag.type()
    _frag.additional_meta_data()
    _frag.ref_id()
    _frag.name()
    _frag.description()
    _frag.created_at()
    _frag.updated_at()
    _frag.billing_id()
    _frag.billing_link_url()
    _frag.type()
    _frag.status()
    _frag_sync_states = _frag.sync_states()
    _frag_sync_states.vendor_identifier()
    _frag_sync_states.status()
    _frag_customers = _frag.customers()
    _frag_customers.id()
    return _frag


def fragment_price_fragment():
    _frag = sgqlc.operation.Fragment(_schema.Price, 'PriceFragment')
    _frag.billing_model()
    _frag.billing_period()
    _frag.billing_id()
    _frag.min_unit_quantity()
    _frag.max_unit_quantity()
    _frag_price = _frag.price()
    _frag_price.amount()
    _frag_price.currency()
    _frag_feature = _frag.feature()
    _frag_feature.feature_units()
    _frag_feature.feature_units_plural()
    _frag_feature.display_name()
    return _frag


def fragment_total_price_fragment():
    _frag = sgqlc.operation.Fragment(_schema.CustomerSubscriptionTotalPrice, 'TotalPriceFragment')
    _frag_sub_total = _frag.sub_total()
    _frag_sub_total.amount()
    _frag_sub_total.currency()
    _frag_total = _frag.total()
    _frag_total.amount()
    _frag_total.currency()
    return _frag


def fragment_package_entitlement_fragment():
    _frag = sgqlc.operation.Fragment(_schema.PackageEntitlement, 'PackageEntitlementFragment')
    _frag.usage_limit()
    _frag.has_unlimited_usage()
    _frag.feature_id()
    _frag.reset_period()
    _frag_feature = _frag.feature()
    _frag_feature.feature_type()
    _frag_feature.meter_type()
    _frag_feature.feature_units()
    _frag_feature.feature_units_plural()
    _frag_feature.display_name()
    _frag_feature.description()
    _frag_feature.ref_id()
    return _frag


def fragment_addon_fragment():
    _frag = sgqlc.operation.Fragment(_schema.Addon, 'AddonFragment')
    _frag.id()
    _frag.ref_id()
    _frag.billing_id()
    _frag.display_name()
    _frag.description()
    _frag.additional_meta_data()
    _frag_entitlements = _frag.entitlements()
    _frag_entitlements.__fragment__(fragment_package_entitlement_fragment())
    _frag.pricing_type()
    return _frag


def fragment_plan_fragment():
    _frag = sgqlc.operation.Fragment(_schema.Plan, 'PlanFragment')
    _frag.id()
    _frag.ref_id()
    _frag.display_name()
    _frag.description()
    _frag.billing_id()
    _frag.additional_meta_data()
    _frag_product = _frag.product()
    _frag_product.ref_id()
    _frag_product.display_name()
    _frag_product.description()
    _frag_product.additional_meta_data()
    _frag_product_product_settings = _frag_product.product_settings()
    _frag_product_product_settings_downgrade_plan = _frag_product_product_settings.downgrade_plan()
    _frag_product_product_settings_downgrade_plan.ref_id()
    _frag_product_product_settings_downgrade_plan.display_name()
    _frag_base_plan = _frag.base_plan()
    _frag_base_plan.id()
    _frag_base_plan.ref_id()
    _frag_base_plan.display_name()
    _frag_entitlements = _frag.entitlements()
    _frag_entitlements.__fragment__(fragment_package_entitlement_fragment())
    _frag_inherited_entitlements = _frag.inherited_entitlements()
    _frag_inherited_entitlements.__fragment__(fragment_package_entitlement_fragment())
    _frag_compatible_addons = _frag.compatible_addons()
    _frag_compatible_addons.__fragment__(fragment_addon_fragment())
    _frag_prices = _frag.prices()
    _frag_prices.__fragment__(fragment_price_fragment())
    _frag.pricing_type()
    _frag_default_trial_config = _frag.default_trial_config()
    _frag_default_trial_config.duration()
    _frag_default_trial_config.units()
    return _frag


def fragment_slim_subscription_fragment():
    _frag = sgqlc.operation.Fragment(_schema.CustomerSubscription, 'SlimSubscriptionFragment')
    _frag.id()
    _frag.ref_id()
    _frag.status()
    _frag.additional_meta_data()
    _frag.billing_id()
    _frag.billing_link_url()
    _frag.effective_end_date()
    _frag.current_billing_period_end()
    _frag.pricing_type()
    _frag_experiment_info = _frag.experiment_info()
    _frag_experiment_info.name()
    _frag_experiment_info.id()
    _frag_experiment_info.group_name()
    _frag_experiment_info.group_type()
    _frag_prices = _frag.prices()
    _frag_prices.usage_limit()
    _frag_prices_price = _frag_prices.price()
    _frag_prices_price.__fragment__(fragment_price_fragment())
    _frag_total_price = _frag.total_price()
    _frag_total_price.__fragment__(fragment_total_price_fragment())
    _frag_plan = _frag.plan()
    _frag_plan.id()
    _frag_plan.ref_id()
    _frag_addons = _frag.addons()
    _frag_addons.quantity()
    _frag_addons_addon = _frag_addons.addon()
    _frag_addons_addon.id()
    _frag_addons_addon.ref_id()
    _frag_customer = _frag.customer()
    _frag_customer.id()
    _frag_customer.ref_id()
    return _frag


def fragment_subscription_fragment():
    _frag = sgqlc.operation.Fragment(_schema.CustomerSubscription, 'SubscriptionFragment')
    _frag.id()
    _frag.start_date()
    _frag.end_date()
    _frag.trial_end_date()
    _frag.cancellation_date()
    _frag.effective_end_date()
    _frag.status()
    _frag.ref_id()
    _frag.current_billing_period_end()
    _frag.additional_meta_data()
    _frag.billing_id()
    _frag.billing_link_url()
    _frag_experiment_info = _frag.experiment_info()
    _frag_experiment_info.name()
    _frag_experiment_info.group_type()
    _frag_experiment_info.group_name()
    _frag_experiment_info.id()
    _frag_prices = _frag.prices()
    _frag_prices.usage_limit()
    _frag_prices_price = _frag_prices.price()
    _frag_prices_price.__fragment__(fragment_price_fragment())
    _frag_total_price = _frag.total_price()
    _frag_total_price.__fragment__(fragment_total_price_fragment())
    _frag.pricing_type()
    _frag_plan = _frag.plan()
    _frag_plan.__fragment__(fragment_plan_fragment())
    _frag_addons = _frag.addons()
    _frag_addons.id()
    _frag_addons.quantity()
    _frag_addons_addon = _frag_addons.addon()
    _frag_addons_addon.__fragment__(fragment_addon_fragment())
    return _frag


def fragment_promotional_entitlement_fragment():
    _frag = sgqlc.operation.Fragment(_schema.PromotionalEntitlement, 'PromotionalEntitlementFragment')
    _frag.status()
    _frag.usage_limit()
    _frag.feature_id()
    _frag.has_unlimited_usage()
    _frag.reset_period()
    _frag.end_date()
    _frag.is_visible()
    _frag_feature = _frag.feature()
    _frag_feature.feature_type()
    _frag_feature.meter_type()
    _frag_feature.feature_units()
    _frag_feature.feature_units_plural()
    _frag_feature.display_name()
    _frag_feature.description()
    _frag_feature.ref_id()
    return _frag


def fragment_customer_fragment():
    _frag = sgqlc.operation.Fragment(_schema.Customer, 'CustomerFragment')
    _frag.id()
    _frag.name()
    _frag.email()
    _frag.created_at()
    _frag.updated_at()
    _frag.has_payment_method()
    _frag.ref_id()
    _frag.billing_id()
    _frag.default_payment_expiration_month()
    _frag.default_payment_expiration_year()
    _frag.default_payment_method_last4_digits()
    _frag.additional_meta_data()
    _frag_trialed_plans = _frag.trialed_plans()
    _frag_trialed_plans.product_ref_id()
    _frag_trialed_plans.plan_ref_id()
    _frag_experiment_info = _frag.experiment_info()
    _frag_experiment_info.group_type()
    _frag_experiment_info.group_name()
    _frag_experiment_info.id()
    _frag_experiment_info.name()
    _frag_coupon = _frag.coupon()
    _frag_coupon.__fragment__(fragment_coupon_fragment())
    _frag_promotional_entitlements = _frag.promotional_entitlements()
    _frag_promotional_entitlements.__fragment__(fragment_promotional_entitlement_fragment())
    _frag_subscriptions = _frag.subscriptions()
    _frag_subscriptions.__fragment__(fragment_subscription_fragment())
    return _frag


def fragment_subscription_preview_fragment():
    _frag = sgqlc.operation.Fragment(_schema.SubscriptionPreview, 'SubscriptionPreviewFragment')
    _frag_sub_total = _frag.sub_total()
    _frag_sub_total.amount()
    _frag_sub_total.currency()
    _frag_total = _frag.total()
    _frag_total.amount()
    _frag_total.currency()
    _frag_billing_period_range = _frag.billing_period_range()
    _frag_billing_period_range.start()
    _frag_billing_period_range.end()
    _frag_proration = _frag.proration()
    _frag_proration.proration_date()
    _frag_proration_credit = _frag_proration.credit()
    _frag_proration_credit.amount()
    _frag_proration_credit.currency()
    _frag_proration_debit = _frag_proration.debit()
    _frag_proration_debit.amount()
    _frag_proration_debit.currency()
    return _frag


def fragment_feature_fragment():
    _frag = sgqlc.operation.Fragment(_schema.EntitlementFeature, 'FeatureFragment')
    _frag.feature_type()
    _frag.meter_type()
    _frag.feature_units()
    _frag.feature_units_plural()
    _frag.ref_id()
    return _frag


def fragment_entitlement_fragment():
    _frag = sgqlc.operation.Fragment(_schema.Entitlement, 'EntitlementFragment')
    _frag.is_granted()
    _frag.access_denied_reason()
    _frag.customer_id()
    _frag.usage_limit()
    _frag.has_unlimited_usage()
    _frag.current_usage()
    _frag.requested_usage()
    _frag.next_reset_date()
    _frag.reset_period()
    _frag_reset_period_configuration = _frag.reset_period_configuration()
    _frag_reset_period_configuration__as__MonthlyResetPeriodConfig = _frag_reset_period_configuration.__as__(_schema.MonthlyResetPeriodConfig)
    _frag_reset_period_configuration__as__MonthlyResetPeriodConfig.monthly_according_to()
    _frag_reset_period_configuration__as__WeeklyResetPeriodConfig = _frag_reset_period_configuration.__as__(_schema.WeeklyResetPeriodConfig)
    _frag_reset_period_configuration__as__WeeklyResetPeriodConfig.weekly_according_to()
    _frag_feature = _frag.feature()
    _frag_feature.__fragment__(fragment_feature_fragment())
    return _frag


def fragment_paywall_package_entitlement_fragment():
    _frag = sgqlc.operation.Fragment(_schema.PackageEntitlement, 'PaywallPackageEntitlementFragment')
    _frag.usage_limit()
    _frag.has_unlimited_usage()
    _frag.feature_id()
    _frag.reset_period()
    _frag_feature = _frag.feature()
    _frag_feature.feature_type()
    _frag_feature.meter_type()
    _frag_feature.feature_units()
    _frag_feature.feature_units_plural()
    _frag_feature.display_name()
    _frag_feature.description()
    _frag_feature.ref_id()
    return _frag


def fragment_paywall_addon_fragment():
    _frag = sgqlc.operation.Fragment(_schema.Addon, 'PaywallAddonFragment')
    _frag.id()
    _frag.ref_id()
    _frag.billing_id()
    _frag.display_name()
    _frag.description()
    _frag_entitlements = _frag.entitlements()
    _frag_entitlements.__fragment__(fragment_paywall_package_entitlement_fragment())
    _frag_prices = _frag.prices()
    _frag_prices.__fragment__(fragment_price_fragment())
    _frag.additional_meta_data()
    _frag.pricing_type()
    return _frag


def fragment_paywall_plan_fragment():
    _frag = sgqlc.operation.Fragment(_schema.Plan, 'PaywallPlanFragment')
    _frag.id()
    _frag.ref_id()
    _frag.description()
    _frag.display_name()
    _frag.billing_id()
    _frag_product = _frag.product()
    _frag_product.ref_id()
    _frag_product.display_name()
    _frag_product.description()
    _frag_product.additional_meta_data()
    _frag_product_product_settings = _frag_product.product_settings()
    _frag_product_product_settings_downgrade_plan = _frag_product_product_settings.downgrade_plan()
    _frag_product_product_settings_downgrade_plan.ref_id()
    _frag_product_product_settings_downgrade_plan.display_name()
    _frag_base_plan = _frag.base_plan()
    _frag_base_plan.id()
    _frag_base_plan.ref_id()
    _frag_base_plan.display_name()
    _frag_entitlements = _frag.entitlements()
    _frag_entitlements.__fragment__(fragment_paywall_package_entitlement_fragment())
    _frag.additional_meta_data()
    _frag_inherited_entitlements = _frag.inherited_entitlements()
    _frag_inherited_entitlements.__fragment__(fragment_paywall_package_entitlement_fragment())
    _frag_prices = _frag.prices()
    _frag_prices.__fragment__(fragment_price_fragment())
    _frag.pricing_type()
    _frag_default_trial_config = _frag.default_trial_config()
    _frag_default_trial_config.duration()
    _frag_default_trial_config.units()
    _frag_compatible_addons = _frag.compatible_addons()
    _frag_compatible_addons.__fragment__(fragment_paywall_addon_fragment())
    return _frag


class Fragment:
    addon_fragment = fragment_addon_fragment()
    coupon_fragment = fragment_coupon_fragment()
    customer_fragment = fragment_customer_fragment()
    entitlement_fragment = fragment_entitlement_fragment()
    feature_fragment = fragment_feature_fragment()
    package_entitlement_fragment = fragment_package_entitlement_fragment()
    paywall_addon_fragment = fragment_paywall_addon_fragment()
    paywall_package_entitlement_fragment = fragment_paywall_package_entitlement_fragment()
    paywall_plan_fragment = fragment_paywall_plan_fragment()
    plan_fragment = fragment_plan_fragment()
    price_fragment = fragment_price_fragment()
    promotional_entitlement_fragment = fragment_promotional_entitlement_fragment()
    slim_subscription_fragment = fragment_slim_subscription_fragment()
    subscription_fragment = fragment_subscription_fragment()
    subscription_preview_fragment = fragment_subscription_preview_fragment()
    total_price_fragment = fragment_total_price_fragment()


def mutation_provision_customer():
    _op = sgqlc.operation.Operation(_schema_root.mutation_type, name='provisionCustomer', variables=dict(input=sgqlc.types.Arg(sgqlc.types.non_null(_schema.ProvisionCustomerInput))))
    _op_provision_customer = _op.provision_customer(input=sgqlc.types.Variable('input'))
    _op_provision_customer_customer = _op_provision_customer.customer()
    _op_provision_customer_customer.__fragment__(fragment_customer_fragment())
    _op_provision_customer.subscription_decision_strategy()
    _op_provision_customer_subscription = _op_provision_customer.subscription()
    _op_provision_customer_subscription.__fragment__(fragment_slim_subscription_fragment())
    return _op


def mutation_import_customer():
    _op = sgqlc.operation.Operation(_schema_root.mutation_type, name='importCustomer', variables=dict(input=sgqlc.types.Arg(sgqlc.types.non_null(_schema.ImportCustomerInput))))
    _op_import_customer = _op.import_one_customer(input=sgqlc.types.Variable('input'), __alias__='import_customer')
    _op_import_customer.__fragment__(fragment_customer_fragment())
    return _op


def mutation_update_customer():
    _op = sgqlc.operation.Operation(_schema_root.mutation_type, name='updateCustomer', variables=dict(input=sgqlc.types.Arg(sgqlc.types.non_null(_schema.UpdateCustomerInput))))
    _op_update_customer = _op.update_one_customer(input=sgqlc.types.Variable('input'), __alias__='update_customer')
    _op_update_customer.__fragment__(fragment_customer_fragment())
    return _op


def mutation_provision_subscription():
    _op = sgqlc.operation.Operation(_schema_root.mutation_type, name='provisionSubscription', variables=dict(input=sgqlc.types.Arg(sgqlc.types.non_null(_schema.ProvisionSubscriptionInput))))
    _op_provision_subscription_v2 = _op.provision_subscription_v2(input=sgqlc.types.Variable('input'))
    _op_provision_subscription_v2.checkout_url()
    _op_provision_subscription_v2.status()
    _op_provision_subscription_v2_subscription = _op_provision_subscription_v2.subscription()
    _op_provision_subscription_v2_subscription.__fragment__(fragment_slim_subscription_fragment())
    return _op


def mutation_update_subscription():
    _op = sgqlc.operation.Operation(_schema_root.mutation_type, name='updateSubscription', variables=dict(input=sgqlc.types.Arg(sgqlc.types.non_null(_schema.UpdateSubscriptionInput))))
    _op_update_subscription = _op.update_one_subscription(input=sgqlc.types.Variable('input'), __alias__='update_subscription')
    _op_update_subscription.__fragment__(fragment_slim_subscription_fragment())
    return _op


def mutation_cancel_subscription():
    _op = sgqlc.operation.Operation(_schema_root.mutation_type, name='cancelSubscription', variables=dict(input=sgqlc.types.Arg(sgqlc.types.non_null(_schema.SubscriptionCancellationInput))))
    _op_cancel_subscription = _op.cancel_subscription(input=sgqlc.types.Variable('input'))
    _op_cancel_subscription.__fragment__(fragment_slim_subscription_fragment())
    return _op


def mutation_initiate_checkout():
    _op = sgqlc.operation.Operation(_schema_root.mutation_type, name='initiateCheckout', variables=dict(input=sgqlc.types.Arg(sgqlc.types.non_null(_schema.InitiateCheckoutInput))))
    _op_initiate_checkout = _op.initiate_checkout(input=sgqlc.types.Variable('input'))
    _op_initiate_checkout.checkout_url()
    _op_initiate_checkout.checkout_billing_id()
    return _op


def mutation_estimate_subscription():
    _op = sgqlc.operation.Operation(_schema_root.mutation_type, name='estimateSubscription', variables=dict(input=sgqlc.types.Arg(sgqlc.types.non_null(_schema.EstimateSubscriptionInput))))
    _op_estimate_subscription = _op.estimate_subscription(input=sgqlc.types.Variable('input'))
    _op_estimate_subscription.__fragment__(fragment_subscription_preview_fragment())
    return _op


def mutation_estimate_subscription_update():
    _op = sgqlc.operation.Operation(_schema_root.mutation_type, name='estimateSubscriptionUpdate', variables=dict(input=sgqlc.types.Arg(sgqlc.types.non_null(_schema.EstimateSubscriptionUpdateInput))))
    _op_estimate_subscription_update = _op.estimate_subscription_update(input=sgqlc.types.Variable('input'))
    _op_estimate_subscription_update.__fragment__(fragment_subscription_preview_fragment())
    return _op


def mutation_report_usage():
    _op = sgqlc.operation.Operation(_schema_root.mutation_type, name='reportUsage', variables=dict(input=sgqlc.types.Arg(sgqlc.types.non_null(_schema.UsageMeasurementCreateInput))))
    _op_create_usage_measurement = _op.create_usage_measurement(usage_measurement=sgqlc.types.Variable('input'))
    _op_create_usage_measurement.id()
    return _op


class Mutation:
    cancel_subscription = mutation_cancel_subscription()
    estimate_subscription = mutation_estimate_subscription()
    estimate_subscription_update = mutation_estimate_subscription_update()
    import_customer = mutation_import_customer()
    initiate_checkout = mutation_initiate_checkout()
    provision_customer = mutation_provision_customer()
    provision_subscription = mutation_provision_subscription()
    report_usage = mutation_report_usage()
    update_customer = mutation_update_customer()
    update_subscription = mutation_update_subscription()


def query_get_customer_by_id():
    _op = sgqlc.operation.Operation(_schema_root.query_type, name='getCustomerById', variables=dict(input=sgqlc.types.Arg(sgqlc.types.non_null(_schema.GetCustomerByRefIdInput))))
    _op_get_customer_by_ref_id = _op.get_customer_by_ref_id(input=sgqlc.types.Variable('input'))
    _op_get_customer_by_ref_id.__fragment__(fragment_customer_fragment())
    return _op


def query_get_coupons():
    _op = sgqlc.operation.Operation(_schema_root.query_type, name='getCoupons')
    _op_coupons = _op.coupons(filter={'status': {'eq': 'ACTIVE'}}, paging={'first': 50})
    _op_coupons_edges = _op_coupons.edges()
    _op_coupons_edges_node = _op_coupons_edges.node()
    _op_coupons_edges_node.__fragment__(fragment_coupon_fragment())
    return _op


def query_get_paywall():
    _op = sgqlc.operation.Operation(_schema_root.query_type, name='getPaywall', variables=dict(input=sgqlc.types.Arg(sgqlc.types.non_null(_schema.GetPaywallInput))))
    _op_get_paywall = _op.get_paywall(input=sgqlc.types.Variable('input'))
    _op_get_paywall.__fragment__(fragment_paywall_plan_fragment())
    return _op


def query_get_entitlements():
    _op = sgqlc.operation.Operation(_schema_root.query_type, name='getEntitlements', variables=dict(query=sgqlc.types.Arg(sgqlc.types.non_null(_schema.FetchEntitlementsQuery))))
    _op_entitlements = _op.cached_entitlements(query=sgqlc.types.Variable('query'), __alias__='entitlements')
    _op_entitlements.__fragment__(fragment_entitlement_fragment())
    return _op


def query_get_entitlement():
    _op = sgqlc.operation.Operation(_schema_root.query_type, name='getEntitlement', variables=dict(query=sgqlc.types.Arg(sgqlc.types.non_null(_schema.FetchEntitlementQuery))))
    _op_entitlement = _op.entitlement(query=sgqlc.types.Variable('query'))
    _op_entitlement.__fragment__(fragment_entitlement_fragment())
    return _op


class Query:
    get_coupons = query_get_coupons()
    get_customer_by_id = query_get_customer_by_id()
    get_entitlement = query_get_entitlement()
    get_entitlements = query_get_entitlements()
    get_paywall = query_get_paywall()


class Operations:
    fragment = Fragment
    mutation = Mutation
    query = Query
