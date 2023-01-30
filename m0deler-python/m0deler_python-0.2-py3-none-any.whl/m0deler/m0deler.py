# Client side stubs and request objects
import requests, json, random, pandas as pd, numpy as np
import matplotlib.pyplot as plt

def MILLION(n):
  return n * 1000000
def PERCENT(n):
  return n / 100
host = 'https://api.m0deler.com'
#host = 'http://localhost:5000'

class M0deler:
  def __init__(self):
    pass
  @classmethod
  def gen_sandbox(cl,name,economy,cbdc):
    sandbox = Sandbox(name,economy,cbdc)
    data = {'economy_params':sandbox.economy.params,
          'cbdc_params':sandbox.cbdc.params,
          'sandbox_id':sandbox.sandbox_id,
          'sandbox_name':name}
    print(data)
    r = requests.post(f'{host}/api/sandbox/generate',json=data)
    sandbox.response_raw = r.content
    sandbox.response_dict = json.loads(r.content)
    sandbox.response_df = pd.DataFrame(columns=sandbox.response_dict['columns'],data=sandbox.response_dict['data'])
    return sandbox
  @classmethod
  def list_sandboxes(cls):
    r = requests.get(f'{host}/api/sandbox/list')
    print(r.content) 
  @classmethod
  def list_economies(cls):
    r = requests.get(f'{host}/api/economy/list')
    print(r.content)
  @classmethod
  def list_cbdcs(cls):
    r = requests.get(f'{host}/api/cbdc/list')
    print(r.content)

class Sandbox:
  def __init__(self,name,economy,cbdc):
    self.name = name
    self.economy = economy
    self.cbdc = cbdc
    self.response_raw = None
    self.response_dict = None
    self.response_df = None
    self.sandbox_id = random.getrandbits(128)
  def get_tx_df(self):
    return self.response_df
  def save_csv(self,f=None):
    if f==None:
      f = str('model-'+str(self.sandbox_id)[:8]+'-'+str(random.randint(20,10000))+'.csv')
    self.response_df.to_csv(f)
  def save_html(self,f=None):
    if f==None:
      f = str('model-'+str(self.sandbox_id)[:8]+'-'+str(random.randint(20,10000))+'.html')
    self.response_df.to_html(f)
  def save_md(self,f=None):
    if f==None:
      f = str('model-'+str(self.sandbox_id)[:8]+'-'+str(random.randint(20,10000))+'.md')
    self.response_df.to_markdown(f)
  def save_big_query(self,f=None):
    if f==None:
      f = str('model-'+str(self.sandbox_id)[:8]+'-'+str(random.randint(20,10000)))
    self.response_df.to_gbq(f)
  def charts(self):
    self.response_df['Timestamp'] = pd.to_datetime(self.response_df['Timestamp'])
    date = self.response_df['Timestamp']
    value = self.response_df['Ending Bal']
    fig, ax = plt.subplots(figsize=(8,6))
    ax.plot(date,value)
    plt.xlabel('Time')
    plt.ylabel('Ending Balance')
    plt.title('Ending Balances for Transacting Accounts')
    plt.show()


  @classmethod
  def load(cls,sandbox_id):
    data = {'sandbox_id':sandbox_id}
    r = requests.get('http://localhost:5000/api/engine/simple/load',json=data)
    print(r.content)

   


class Economy:
    def __init__(self, name, population, gdp_growth_rate, gdp, inflation_rate):
      self.params = {}
      self.params['population'] = population
      self.params['gdp_growth_rate'] = gdp_growth_rate
      self.params['gdp'] = MILLION(gdp)
      self.params['inflation_rate'] = inflation_rate
      self.params['name'] = name

    @property
    def name(self):
        return self.params['name']
    
    @property
    def population(self):
        return self.params['population']

    @property
    def gdp_growth_rate(self):
        return self.params['gdp_growth_rate']
    @property
    def gdp (self):
        return self.params['gdp']

    @property
    def inflation_rate(self):
        return self.params['inflation_rate']


class CBDC:
    def __init__(self,name, engine,tx_avg_nominal_amt,tx_nominal_amt_sd, txs, wallets_qty, initial_balance_avg, initial_bal_sd=0):
      self.params = {}
      self.params['name'] = name
      self.params['engine'] = engine
      self.params['tx_avg_nominal_amt'] = tx_avg_nominal_amt
      self.params['tx_nominal_amt_sd'] = tx_nominal_amt_sd
      self.params['txs'] = txs
      self.params['wallets_qty'] = wallets_qty
      self.params['initial_balance_avg'] = initial_balance_avg
      self.params['initial_bal_sd'] = initial_bal_sd

    @property
    def tx_avg_nominal_amt(self):
        return self.params['tx_avg_nominal_amt']
    @property
    def tx_nominal_amt_sd(self):
        return self.params['tx_nominal_amt_sd']

    @property
    def wallets(self):
        return self.params['wallets']
    @property
    def txs(self):
        return self.params['txs']      


# class M0deler:
#   def __init__(self,econ_params,cbdc):
#     self.__econ_params = econ_params
#     self.__cbdc = cbdc
#     self.__transactions = []
#     self.__df_transactions = pd.DataFrame(columns=['Timestamp','Sender','Receiver','Initial Bal','Amount','Ending Bal','Tx Count'])
#     self.model_id = random.getrandbits(128)
#   def run(self):
#     data = {'econ_params':self.__econ_params.params,
#             'cbdc_params':self.__cbdc.params}
#     print(data)
#     r = requests.post('http://localhost:5000/api/engine/simple',json=data)
#     return self.model_id
#     # transaction_amounts = abs(np.random.normal(
#     #   self.__cbdc.tx_avg_nominal_amt,
#     #   self.__cbdc.tx_nominal_amt_sd,self.__cbdc.txs).round(2))
#     # for amt in transaction_amounts:
#     #   sender = self.__cbdc.wallets.get_random_wallet()
#     #   receiver = self.__cbdc.wallets.get_random_wallet()
#     #   sender_initial_bal = sender.balance
#     #   sender.decrease(amt)
#     #   receiver.increase(amt)
#     #   sender.tx_count += 1
#     #   receiver.tx_count += 1
#     #   tx = Transaction(sender,receiver,amt)
#     #   self.__transactions.append(tx)
#     #   tx_row = [tx.date,tx.sender.displayable_id,tx.receiver.displayable_id,sender_initial_bal,tx.amt,sender.balance,sender.tx_count]
#     #   self.__df_transactions.loc[len(self.__df_transactions)] = tx_row
#   def display_txs(self):
#     with pd.option_context('display.max_rows', None,
#                        'display.max_columns', None,
#                        'display.precision', 3
#                        ): print(self.__df_transactions)
#   def balances(self):
#     balances = self.__cbdc.wallets.get_balances()
#     with pd.option_context('display.max_rows', None,
#                        'display.max_columns', None,
#                        'display.precision', 3
#                        ): print(balances)
# # wallets.print_balances()
