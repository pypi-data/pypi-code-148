import stelix

sellix = stelix.Sellix(
    secret_key='SECRET_KEY'
)

payment = sellix.request(
    method='create', # What you want to do, in this case we want to create a new coupon code
    endpoint='payments', # The API Endpoint you are trying to access

    title='Developer Title',
    gateways=[
        'BITCOIN'
    ],
    email='email@gmail.com',
    currency='USD',

    value=26,
    quantity=1,

    confirmations=1,
    white_label=True
)

order = sellix.request(
    method='get',
    endpoint='order',

    uniqid=payment['data']['invoice']['uniqid']
)

print(order['data']['order']['status_history'][0]['status']) # A successfully completed order should have the "COMPLETED" tag
