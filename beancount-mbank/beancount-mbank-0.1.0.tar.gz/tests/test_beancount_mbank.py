
from beancount_mbank.mbank import MBankImporter


def test_main():
    importer = MBankImporter(account="Assets:MBank:Debit")
    assert importer.name() == 'beancount_mbank.mbank.MBankImporter: "Assets:MBank:Debit"'
