from faker import Faker

fake = Faker()


def generate_fake_value(provider: str, unique=False):
    """ Generates fake value with Faker library """
    if provider == 'user_name':
        fake_value = fake.user_name()
    elif provider == 'first_name':
        fake_value = fake.first_name()
    elif provider == 'first_name_male':
        fake_value = fake.first_name_male()
    elif provider == 'first_name_female':
        fake_value = fake.first_name_female()
    elif provider == 'last_name':
        fake_value = fake.last_name()
    elif provider == 'last_name_male':
        fake_value = fake.last_name_male()
    elif provider == 'last_name_female':
        fake_value = fake.last_name_female()
    elif provider == 'name':
        fake_value = fake.name()
    elif provider == 'name_male':
        fake_value = fake.name_male()
    elif provider == 'name_female':
        fake_value = fake.name_female()
    elif provider == 'prefix':
        fake_value = fake.prefix()
    elif provider == 'prefix_male':
        fake_value = fake.prefix_male()
    elif provider == 'prefix_female':
        fake_value = fake.prefix_female()
    elif provider == 'phone_number':
        fake_value = fake.phone_number()
    elif provider == 'random_int':
        fake_value = fake.random_int()
    elif provider == 'random_digit':
        fake_value = fake.random_digit()
    elif provider == 'random_digit_not_null':
        fake_value = fake.random_digit_not_null()
    elif provider == 'random_letter':
        fake_value = fake.random_letter()
    elif provider == 'random_lowercase_letter':
        fake_value = fake.random_lowercase_letter()
    elif provider == 'boolean':
        fake_value = fake.boolean()
    elif provider == 'job':
        fake_value = fake.job()
    elif provider == 'isbn10':
        fake_value = fake.isbn10()
    elif provider == 'ascii_company_email':
        fake_value = fake.ascii_company_email()
    elif provider == 'ascii_email':
        fake_value = fake.ascii_email()
    elif provider == 'ascii_safe_email':
        fake_value = fake.ascii_safe_email()
    elif provider == 'company_email':
        fake_value = fake.company_email()
    elif provider == 'email':
        fake_value = fake.email()
    elif provider == 'domain_name':
        fake_value = fake.domain_name()
    elif provider == 'hostname':
        fake_value = fake.hostname()
    elif provider == 'image_url':
        fake_value = fake.image_url()
    elif provider == 'ipv4':
        fake_value = fake.ipv4()
    elif provider == 'url':
        fake_value = fake.url()
    elif provider == 'date':
        fake_value = fake.date()
    elif provider == 'day_of_month':
        fake_value = fake.day_of_month()
    elif provider == 'day_of_week':
        fake_value = fake.day_of_week()
    elif provider == 'month':
        fake_value = fake.month()
    elif provider == 'year':
        fake_value = fake.year()
    elif provider == 'month_name':
        fake_value = fake.month_name()
    elif provider == 'time':
        fake_value = fake.time()
    elif provider == 'currency_code':
        fake_value = fake.currency_code()
    elif provider == 'currency_name':
        fake_value = fake.currency_name()
    elif provider == 'pricetag':
        fake_value = fake.pricetag()
    elif provider == 'credit_card_expire':
        fake_value = fake.credit_card_expire()
    elif provider == 'credit_card_number':
        fake_value = fake.credit_card_number()
    elif provider == 'company':
        fake_value = fake.company()
    elif provider == 'color_name':
        fake_value = fake.color_name()
    elif provider == 'hex_color':
        fake_value = fake.hex_color()
    elif provider == 'license_plate':
        fake_value = fake.license_plate()
    elif provider == 'address':
        fake_value = fake.address()
    elif provider == 'street_address':
        fake_value = fake.street_address()
    elif provider == 'street_name':
        fake_value = fake.street_name()
    elif provider == 'city':
        fake_value = fake.city()
    elif provider == 'country':
        fake_value = fake.country()
    elif provider == 'country_code':
        fake_value = fake.country_code()
    else:
        raise Exception('Invalid provider')

    return fake_value
