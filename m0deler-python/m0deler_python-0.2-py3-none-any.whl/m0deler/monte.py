import numpy as np, pandas as pd
from transaction import Transaction
from datetime import date
import plotly.express as px
import chart_studio as cs
cs.tools.set_credentials_file(
    username='jamielsheikh', api_key='')
import chart_studio.plotly as py
import plotly.graph_objs as go
from transaction import Transaction

def run_monte(economy,cbdc,wallets):
    transactions = []
    df_transactions = pd.DataFrame(columns=['Timestamp','Sender','Receiver','Initial Bal','Amount','Ending Bal','Tx Count'])

    # generate distribution of transaction amounts
    transaction_amounts = abs(np.random.normal(
      cbdc.tx_avg_nominal_amt,
      cbdc.tx_nominal_amt_sd,cbdc.txs).round(2))

    # generate transactions
    for amt in transaction_amounts:
      sender = cbdc.wallets.get_random_wallet()
      receiver = cbdc.wallets.get_random_wallet()
      sender_initial_bal = sender.balance
      sender.decrease(amt)
      receiver.increase(amt)
      sender.tx_count += 1
      receiver.tx_count += 1
      tx = Transaction(sender,receiver,amt)
      transactions.append(tx)
      tx_row = [tx.date,tx.sender.displayable_id,tx.receiver.displayable_id,sender_initial_bal,tx.amt,sender.balance,sender.tx_count]
      df_transactions.loc[len(df_transactions)] = tx_row
      model = df_transactions.to_json(orient='split')
    # series = px.scatter(df_transactions,x='Timestamp',y='Ending Bal',x=df_transactions['Timestamp'].tolist(),y=df_transactions['Ending Bal'].tolist(),title='Balances of Transacting Sender Accounts') 
    # data = [series]
    # chart1 = py.plot(data,filename='transactions')

    # fig = px.scatter(df_transactions,x='Timestamp',y='Ending Bal',title='Ending Balance for Transacting Accounts')
    # chart1 = fig.show()

    # df_balances = cbdc.wallets.get_balances()
    # fig = px.histogram(df_balances,x='Wallet',y='Curr. Balance',title='Histogram of Ending Account Balances')
    # chart2 = fig.show()

    # fig = px.histogram(df_transactions,x='Sender',y='Amount',title='Chart of Transaction Amounts')
    # chart2 = fig.show()

    # # df_balances = cbdc.wallets.get_balances()
    # # series = go.Histogram(x=df_balances['Wallet'].tolist(),y=df_balances['Curr. Balance'].tolist())
  
    # # data = [series]
    # # chart2 = py.plot(data,filename='balances') 
    # print('resp',chart1)
    return model