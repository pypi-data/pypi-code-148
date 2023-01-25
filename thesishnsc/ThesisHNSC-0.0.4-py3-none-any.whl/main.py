import os
import pandas as pd
import tensorflow 
from tensorflow import keras

def predict(df):

  # Removing all the cells with zero values in it.i.e. all the rows have zero in it.
      
  df= df.loc[(df!=0).any(axis=1)]
      
  #df1 = df.loc[:,(df==0).mean()<0.8] ## removing all the columns with more than 80 % zeroes 
      
  selected_genes = ['PLAC9', 'UBB', 'ACKR1', 'AQP7', 'FXYD1', 'BTG1', 'B2M', 'CFD', 'LTBP4',
       'RPS11', 'MFAP4', 'ISG20', 'SARAF', 'RPL28', 'ABCA8', 'YPEL5', 'GSN',
       'IL2RG', 'OAZ1', 'DPT', 'RPLP1', 'TNXB', 'CD37', 'ARPC3', 'CYBRD1',
       'SDPR', 'RELB', 'CYBA', 'TIMP3', 'RPS19', 'CREM', 'NOVA1', 'RPS26',
       'PDGFRL', 'HLA-C', 'CXCL12', 'TGFBR3', 'RAC2', 'SERP1', 'VIT', 'RHOG',
       'ADH1B', 'RHOH', 'COPE', 'DCN', 'CNN2', 'REL', 'CD34', 'OST4', 'PRELP',
       'EPSTI1', 'PTGIS', 'SOD3', 'TNIP1', 'LIMD2', 'RPS15A', 'DUSP4',
       'SPARCL1', 'SCARA5', 'HLA-B', 'FBLN2', 'IDH2', 'ANGPTL1', 'HLA-A',
       'FHL1', 'EZR', 'GPSM3', 'F10', 'EEF1A1', 'CYTIP', 'FBLN5', 'CIB1',
       'CXCR4', 'ATP5E', 'FIGF', 'PLPP3', 'PIM3', 'PSME1', 'CILP', 'CD7',
       'EBF1', 'NDUFB11', 'ICAM3', 'MGP', 'SLC16A3', 'MEG3', 'VOPP1', 'TXNIP',
       'RPS15', 'SSPN', 'UBC', 'BMP4', 'TIGIT', 'ADAR', 'LRRN4CL', 'SUB1',
       'GDF10', 'WIPF1', 'ABI3BP', 'FAM177A1']      
  df1 = df[selected_genes]


  # Load the model

  dir_location = os.path.join(os.path.dirname(__file__), 'Model')
      
  #Load model
  model = keras.models.load_model(dir_location)



  y_pred = model.predict(df1)
      
  predictions = list(map(lambda x: 0 if x<0.5 else 1, y_pred))
      
  ones = 0
  zeros =0
      
  for i in range(len(predictions)):
      if (predictions[i]==1):
          ones +=1
      else:
          zeros+=1
              
  #print("The number of ones are ", ones)
  #print("The number of zeros are ", zeros)
  #print("Total number of cells are ", len(predictions))
  #print("Predicted percentage of Diseased cells are ", ones/len(predictions))
  #print("Predicted percentage of Normal cells are ", zeros/len(predictions))
      
  op= ones/len(predictions) 
  zp= zeros/len(predictions)
      
  if(op>0.6):
      print("HNSCC patient detected, {} percentage diseased cells detected".format(op))
        # Load the model

      dir_location1 = os.path.join(os.path.dirname(__file__), 'Model_hpv')

      #Load model
      model1 = keras.models.load_model(dir_location1)



      y_pred1 = model1.predict(df1)

      predictions1 = list(map(lambda x: 0 if x<0.5 else 1, y_pred1))

      ones1 = 0
      zeros1 =0

      for i in range(len(predictions1)):
          if (predictions1[i]==1):
              ones1 +=1
          else:
              zeros1+=1

      #print("The number of ones are ", ones)
      #print("The number of zeros are ", zeros)
      #print("Total number of cells are ", len(predictions))
      #print("Predicted percentage of Diseased cells are ", ones1/len(predictions1))
      #print("Predicted percentage of Normal cells are ", zeros1/len(predictions1))

      op1= ones1/len(predictions1) 
      zp1= zeros1/len(predictions1)
      if(op1>0.8):
            print("HNSCC HPV- patient detected, {} percentage HPV- cells classified".format(op1))
      else: 
            print("HNSCC HPV+ patient detected, {} percentage HPV+ cells classified".format(zp1))
  else:
      print("Normal patient detected, {} percentage normal cells detected".format(zp))
