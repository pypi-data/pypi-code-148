from monte import run_monte
import numpy as np, pandas as pd, random
class Wallet:
    def __init__(self, id, initial_bal=0):
        self.initial_balance = initial_bal
        self.id = id
        self.displayable_id = str(id)[:5]
        self.balance = initial_bal
        self.tx_count = 0

    def decrease(self, amt):
        self.balance = self.balance - amt

    def increase(self, amt):
        self.balance = self.balance + amt

class Wallets:
    def __init__(self, wallets_qty, initial_balance_avg, initial_bal_sd=0):
        self.wallets = []
        self.wallets_qty = wallets_qty
        self.initial_balance_avg = initial_balance_avg
        self.initial_bal_sd = initial_bal_sd
        for q in range(wallets_qty):
          initial_balance = np.random.normal(initial_balance_avg,initial_bal_sd)
          self.wallets.append(Wallet(random.getrandbits(128), initial_balance))
    def get_random_wallet(self):
        return random.choice(self.wallets)

    def get_balances(self):
      balances = pd.DataFrame(columns=['Wallet','Initial Bal','Curr. Balance','Tx Count'])
      for w in self.wallets:
        row = [w.id,w.initial_balance,w.balance,w.tx_count]
        balances.loc[len(balances)] = row
      return balances          

class CBDCServer:
    def __init__(self,name,wallets,tx_avg_nominal_amt,tx_nominal_amt_sd, txs):
      self.name = name
      self.wallets = wallets
      self.tx_avg_nominal_amt = tx_avg_nominal_amt
      self.tx_nominal_amt_sd = tx_nominal_amt_sd
      self.txs = txs

class EconomyServer:
    def __init__(self, name, population, gdp_growth_rate, gdp, inflation_rate):
      self.population = population
      self.gdp_growth_rate = gdp_growth_rate
      self.gdp = gdp
      self.inflation_rate = inflation_rate
      self.name = name

class SandboxServer:
   
  def __init__(self,name,econ_params,cbdc_params,sandbox_id):
    self.name = name
    self.economy = EconomyServer(gdp=econ_params['gdp'],
                    gdp_growth_rate=econ_params['gdp_growth_rate'],
                    inflation_rate=econ_params['inflation_rate'],
                    name=econ_params['name'],
                    population=econ_params['population'])
    self.wallets = Wallets(
                initial_bal_sd=cbdc_params['initial_bal_sd'],
                initial_balance_avg=cbdc_params['initial_balance_avg'],
                wallets_qty=cbdc_params['wallets_qty'])
    self.cbdc = CBDCServer (
      name=cbdc_params['name'],
      wallets=self.wallets,
      tx_avg_nominal_amt=cbdc_params['tx_avg_nominal_amt'],
      tx_nominal_amt_sd=cbdc_params['tx_nominal_amt_sd'],
      txs=cbdc_params['txs']
    )
    self.transactions = []
    self.df_transactions = pd.DataFrame(columns=['Timestamp','Sender','Receiver','Initial Bal','Amount','Ending Bal','Tx Count'])
    self.sandbox_id = sandbox_id
  def run(self):
    model = run_monte(self.economy,self.cbdc,self.wallets)
    return model
  def display_txs(self):
    with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 3
                       ): print(self.df_transactions)
  def balances(self):
    balances = self.cbdc.wallets.get_balances()
    return balances
    # with pd.option_context('display.max_rows', None,
    #                    'display.max_columns', None,
    #                    'display.precision', 3
    #                    ): print(balances)