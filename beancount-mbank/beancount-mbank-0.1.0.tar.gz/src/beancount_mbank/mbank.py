import csv
import datetime
import re
from os import path
from dateutil.parser import parse

from beancount.core import amount, data, flags
from beancount.core.number import D
from beancount.ingest import importer

OP_DATE = "#Data operacji"
OP_BOOKDATE = "#Data księgowania"
OP_DESC = "#Opis operacji"
OP_TITLE = "#Tytuł"
OP_PAYEE = "#Nadawca/Odbiorca"
OP_ACCOUNT = "#Numer konta"
OP_AMOUNT = "#Kwota"
OP_BALANCE = "#Saldo po operacji"

HEADER = ';'.join([
    OP_DATE,
    OP_BOOKDATE,
    OP_DESC,
    OP_TITLE,
    OP_PAYEE,
    OP_ACCOUNT,
    OP_AMOUNT,
    OP_BALANCE
])


class MBankImporter(importer.ImporterProtocol):

    def __init__(self, account, currency='PLN', file_encoding='cp1250',
                 basename=None):
        self.account = account
        self.currency = currency
        self.file_encoding = file_encoding
        self.basename = basename
        self.FLAG = flags.FLAG_WARNING

    def name(self):
        return '{}: "{}"'.format(super().name(), self.file_account(None))

    def file_account(self, _):
        return self.account

    def file_name(self, file):
        if self.basename:
            return '{}.{}'.format(self.basename, path.basename(file.name))

    def file_date(self, file):
        # TODO: Get last date from file content
        match = re.match(r"\d+_\d+_(\d+)", path.basename(file.name))
        if match:
            return datetime.datetime.strptime(match.group(1), "%y%m%d").date()

    def identify(self, file):
        # Example: 78212544_210313_210613.csv
        file_name_pattern = self.account + r"_\d{6}_\d{6}.csv"
        print((re.match(file_name_pattern, path.basename(file.name))
              and re.match("mBank S.A.", file.head(10))))
        return True

    def extract(self, file, existing_entries=None):
        entries = []
        index = 0
        with open(file.name, newline="", encoding=self.file_encoding) as csvfile:
            offset = get_offset(csvfile, HEADER)
            dialect = csv.Sniffer().sniff(csvfile.readline(), delimiters=';')
            csvfile.seek(offset)

            # last_balance = None
            for index, record in enumerate(csv.DictReader(csvfile, dialect=dialect)):
                if not re.match(r"\d\d\d\d", record[OP_DATE]):
                    continue
                date = parse(record[OP_DATE]).date()
                payee = ' '.join(record[OP_PAYEE].split())
                narration = ' '.join(record[OP_TITLE].split())
                if not narration:
                    narration = record[OP_DESC]
                postings = [
                    data.Posting(
                        self.account,
                        parse_units(record[OP_AMOUNT], self.currency),
                        None,
                        None,
                        None,
                        None
                    )
                ]
                entries.append(data.Transaction(
                    data.new_metadata(file.name, index),
                    date,
                    self.FLAG,
                    payee,
                    narration,
                    data.EMPTY_SET,
                    data.EMPTY_SET,
                    postings=postings)
                )

        return entries


def get_offset(file, line_prefix):
    """Rewind file offset to csv header and skip metadata"""
    offset = 0
    for line in file.readlines():

        if line.startswith(line_prefix):
            file.seek(offset)
            break
        else:
            offset += len(line)
            continue
    return offset


def parse_units(value, unit):
    """ Returns amount from mbank money statement """
    price = to_decimal(value)
    return amount.Amount(price, unit)


def to_decimal(value):
    price = value.replace(",", ".")
    return D(price)
