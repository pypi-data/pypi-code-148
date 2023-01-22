import topsis.topsis as tp
tp.calculate("mydata.csv","output.csv",weights="1,1,1,1,1",impacts="+,+,-,+,+", verbose=True, overwrite=True)