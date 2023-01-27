class DataAutomation():
    import pandas as pd
    import numpy as np
    import warnings
    warnings.filterwarnings("ignore")
    
    """
    DEVELOPED BY HRS
    """
    
    def __init__(self):
        import pandas as pd
        import numpy as np
        import warnings
        warnings.filterwarnings("ignore")
        #print("In the Data Automation Class")
        self.info = {}
        """
        self.originaldata = data
        self.target = target
        self.data = data
        """
        self.corrData = dict()
        self.Rinfo = ""
        
        
    
    def check_ftype(self,data,target):
        def check_date(df):
            df = df.astype(str)
            #print(df)
            s = ""
            def check_basic(x):
                l = x.split("-")
                if(len(l) == 3):
                    s = "-"
                    for i in l:
                        if(str(i).split()[0].isdigit() == False):
                            return False
                    return True
                l = x.split("/")
                if(len(l) == 3):
                    s = "/"
                    for i in l:
                        if(str(i).split()[0].isdigit() == False):
                            return False
                    return True
                return False
            """if(check_basic(x) == False):
                return False
            """
            try:
                x = df[0]
                if(check_basic(x)):
                    df = pd.to_datetime(df)
                    return True
                return False
            except:
                return False
        cols = data.columns
        info = {}
        i = 0
        for x in cols:
            #print(x)
            c = 0
            try:
                #Indexing
                if(i == 1):
                    pass
                elif(x.lower().strip() in ['id','userid','user']):
                    info[x] = 'index'
                    i = 1
                    c = 1
                else:    
                    df = data[x]
                    mn = min(df)
                    mx = max(df)
                    k = 0
                    for xx in df:
                        if(type(xx) != int):
                            k = 1
                            break
                    if(k == 0):
                        if(df.nunique() == len(df)):
                            i = 1
                            c = 1
                            info[x] = 'index'
            except:
                pass

            if(c == 1):
                continue

            if(data[x].dtype == 'O'):
                #Cat or Date
                #Cheking for date
                df = data[x].dropna()
                #Checking if it's  date
                if(check_date(df)):
                    c = 1
                    info[x] = 'date'
                else:
                    c = 1
                    #check if it's not Numeric in nature
                    try:
                        k = data[x].dropna().astype(int)
                        #v = int(data[x][0])
                        u = data[x].nunique()
                        if(u < 21 and u < len(data[x])/100):
                            
                            def insideapply(x):
                                try:
                                    return int(x)
                                except:
                                    try:
                                        return float(x)
                                    except:
                                        import numpy as np
                                        return np.nan
                            
                            self.data[x] = self.data[x].apply(insideapply)
                            info[x] = "cat" #'cat-num'
                            
                        else:

                            #v = data[x].mean()
                            info[x] = 'num'
                            
                    except:
                        info[x] = 'cat'
            else:
                df = data[x].dropna()
                if(check_date(df)):
                    c = 1
                    info[x] = 'date'
                else:
                    l = df.nunique()
                    n = len(df)
                    if(l < 15 and l < n/100):
                        #df[x] = df[x].astype(str)
                        
                        def insideapply(x):
                            try:
                                return str(x)
                            except:
                                return np.nan
                        
                        self.data[x] = self.data[x].apply(insideapply)
                        info[x] = 'cat' #num-cat
                    else:
                        info[x] = 'num'
            #print(x,info[x],data[x][0])

        return info
    
    
    
    def remove_outliers(self):
        
        #print(len(self.data))
        df = self.data
        for x in self.info:
            if(self.info[x] == 'num' and x != self.target):
                #remove outliers
                #df = self.data
                c = x
                s = df[x].skew()
                #print(len(df),x,s)
                if(s > 0.5):
                    c = x
                    q = df[c].quantile(0.97)
                    arr = []
                    for x in df[c]:
                        if(q - x > 0):
                            arr.append(x)

                    k = min(df[c].skew(),1)
                    df = df[df[c] <= q + (1 + k/1.3) * sum(arr) / len(arr)]

                elif(s < -0.5):
                    c = x
                    q = df[c].quantile(0.03)
                    arr = []
                    for x in df[c]:
                        if(q - x < 0):
                            arr.append(x)

                    k = abs(min(df[c].skew(),1))
                    df = df[df[c] >= q - (1 + k/1.3) * sum(arr) / len(arr)]

                else:
                    if(s > 0):
                        q9 = df[c].quantile(0.997)
                        q1 = df[c].quantile(0.25)
                        q3 = df[c].quantile(0.80)
                        q1 = df[c].quantile(0.01)

                        iqr = q3 - q1
                        df = df[df[c] <= q9 + (1.7 + s) * iqr]

                        #LEFT PART
                        df = df[df[c] >= q1 - iqr]
                    else:
                        q9 = df[c].quantile(0.99)
                        q01 = df[c].quantile(0.003)
                        q1 = df[c].quantile(0.25)
                        q3 = df[c].quantile(0.85)

                        iqr = q3 - q1
                        df = df[df[c] >= q01 - (1.7 + s) * iqr]

                        #RIGHT PART
                        df = df[df[c] <= q9 + iqr]
                self.data = df
                #print(len(df))
                
            elif(self.info[x] == "cat" and x != self.target):
                import numpy as np
                #Category Outliers == check any others value_counts
                vc = df[x].value_counts()
                l = len(df)/200
                df[x] = np.where(df[x].isin(vc.index[vc >= l]),df[x],'OTHERS')
            

        #Fill NaN Value
    def fill_nan(self):
        import numpy as np
        df = self.data
        self.data = df[df[self.target].isnull()== False]
        #print(len(df))
            
        ndf = df.isnull().sum()
        l = len(df)/200
        for k in ndf.keys():
            
            if(ndf[k] == 0 or k == self.target):
                continue
            if(ndf[k] <= l):
                #0.5% RULE 
                #print(k,self.info[k],end = " ")
                #print("0.5 RULE")
                #print(len(df))
                self.data = df[df[k].isnull()== False]
                #print(len(df))
            else:
                if(self.info[k] == "cat"):
                    df[k].fillna("isMissing",inplace = True)
                elif(self.info[k] == 'num'):
                     df[k].fillna(df[k].mean(),inplace = True)
                else:
                    #print("INELSE DATE")
                    if(self.info[k] == 'date'):
                        #print(k,"INDATE")
                        df[k].fillna(method = 'ffill',inplace = True)
                        df[k].fillna(method = 'bfill',inplace = True)
                        
                     #continue
        
        
    
    #Feature Engineering 
        
    def feature_engg(self):
        #print(self.data.shape)
        import pandas as pd
            
        cat_f = []
        num_f = []
        date_f = []
        for x in self.info:
            if(x != self.target):
                if(self.info[x] == 'cat'):
                    cat_f.append(x)
                elif(self.info[x] == 'num'):
                    num_f.append(x)
                elif(self.info[x] == 'date'):
                    date_f.append(x)
                else:
                    continue 
            
        for i1 in range(len(cat_f) - 1):
            x1 = cat_f[i1]
            for i2 in range(i1 + 1,len(cat_f)):
                x2 = cat_f[i2]
                self.data[x1 + "-" + x2 + "-N"] = self.data[x1] + "_" + self.data[x2]
                self.info[x1 + "-" + x2 + "-N"] = "cat"
        
        for x1 in num_f:
            self.data[x1 + "-q-N"] = pd.cut(self.data[x1],6)
            self.info[x1 + "-q-N"] = 'cat'
            
            
        for x1 in date_f:
            self.data[x1] = pd.to_datetime(self.data[x1])
            self.data[x1 + "-M"] = self.data[x1].apply(lambda x :x.month)
            self.data[x1 + "-D"] = self.data[x1].apply(lambda x :x.day)
            self.data[x1 + "-Y"] = self.data[x1].apply(lambda x :x.year)
            self.data[x1 + "-W"] = self.data[x1].apply(lambda x :x.week % 7 + 1)
            self.data.drop(x1,inplace = True, axis = 1)
            
            self.info[x1 + "-D"] = "cat"
            self.info[x1 + "-Y"] = "cat"
            self.info[x1 + "-M"] = "cat"
            self.info[x1 + "-W"] = "cat"
            
            self.info.pop(x1)
        
        #print(self.data.shape)
    
    
    #feature Selection
    def feature_sel(self):
        from scipy import stats as ss
        import pandas as pd
        import numpy as np
        
        
        masterData = self.corrData
        
        df = self.data
        def corr1(x,y):
            #(data['D-y'],data[target1]) ----> CAT - CAT
            confusion_matrix = pd.crosstab(x,y)
            chi2 = ss.chi2_contingency(confusion_matrix)[0]
            n = confusion_matrix.sum().sum()
            phi2 = chi2/n
            r,k = confusion_matrix.shape
            phi2corr = max(0, phi2-((k-1)*(r-1))/(n-1))
            rcorr = r-((r-1)**2)/(n-1)
            kcorr = k-((k-1)**2)/(n-1)
            return np.sqrt(phi2corr/min((kcorr-1),(rcorr-1)))
        
        
            
            
        corr = self.data.corr(method = "spearman")
        
        def corr2(x,y):
            #CAT-NUM
            ########################################## CHECK!!
            # Running the one-way anova test 
            # Assumption(H0) is that FuelType and CarPrices are NOT correlated
            #x : cat, y : num
            dff = self.data.groupby(x)[y].apply(list)
            ar = ss.f_oneway(*dff)
            ## We accept the Assumption(H0) only when P-Value >0 0.05
            return ar.pvalue < 0.05
        
        
        for x in self.data.columns:
            #print(x,end = " ")
            if(self.info[self.target] == 'cat'):
                if(self.info[x] == 'cat'):
                    if(self.target != x):
                        masterData[x] = corr1(self.data[x],self.data[self.target])
                        #print("CAT_CAT",end = " ")
                        #print(masterData[x])
                        #self.corrli.append(corr1(self.data[x],self.data[self.target]))
                elif(self.info[x] == 'num'):
                    if(self.target != x):
                        #cat - num
                        masterData[x] = corr2(self.target,x)
                        #print("CAT_NUM",end = " ")
                        #print(masterData[x])
                    
                        
                        
                
            elif(self.info[self.target] == 'num'):
                if(self.info[x] == 'num'):
                    if(self.target != x):
                        masterData[x] = corr[x][self.target]
                        #print("NUM_NUM",end = " ")
                        #print(masterData[x])
                elif(self.info[x] == 'cat'):
                    if(self.target != x):
                        #cat - num
                        masterData[x] = corr2(x,self.target)
                        #print("NUM_CAT",end = " ")
                        #print(masterData[x])
            
        #print(masterData)
        li = []
        li.append(self.target)
        for x in masterData:
            if(masterData[x] >= 0.06):
                li.append(x)
        
        self.data = self.data[li]
        
                        
    
    def reframe(self):
        import pandas as pd
        from scipy import stats as ss
        def corr2(x,y,df):
            #CAT-NUM
            ########################################## CHECK!!
            # Running the one-way anova test 
            # Assumption(H0) is that FuelType and CarPrices are NOT correlated
            #x : cat, y : num
            dff = df.groupby(x)[y].apply(list)
            ar = ss.f_oneway(*dff)
            ## We accept the Assumption(H0) only when P-Value >0 0.05
            return ar.pvalue < 0.05
        
        data = self.data
        cat = []
        num = []
        remF = [] #DISBURSED-AMT/HIGH CREDIT_2,00,000
        
        for x in self.data.columns:
            if(x != self.target and self.info[x] == 'cat'):
                cat.append(x)
            elif(x != self.target and self.info[x] == 'num'):
                num.append(x)
         
        if(self.info[self.target] == 'cat'):
            for x in cat:
                data[x] = data[x].astype(str)
                df = pd.DataFrame()
                df['target'] = self.data[self.target]

                for xx in data[x].unique():

                    df[xx] = data[x].apply(lambda y : 1 if y == xx else 0)
                    if(self.info[self.target] == 'num'):
                        if(df.corr(method = 'kendall')['target'][xx] < 0.1):
                            remF.append(x + "_" + xx)
                    if(self.info[self.target] == 'cat'):
                        if(corr2("target",xx,df) == False):
                            remF.append(x + "_" + xx)
            
                    
                
                
            
        self.data = pd.get_dummies(data)
        self.data.drop(remF,axis = 1,inplace = True)
        
        print(cat,data.shape)
        
        
    
    
    def run(self,data,target):
        
        self.originaldata = data
        self.target = target
        self.data = data
        
        print("Created by Himanshu & Amit \n")
        
        print("Checking Data Type... ",end = " ")
        #FInding the data type of the columns of the dataset
        self.info = self.check_ftype(data,target)
        print("   DONE!")
        
        #print(self.info)
        
        print("Dealing with Outliers & useless data... ",end = " ")
        self.remove_outliers()
        #removing outliers from Numeric dataset
        self.fill_nan()
        print("   DONE!")
        
        print("Building new features... ",end = " ")
        self.feature_engg()
        print("   DONE!")
        
        print("Finding best features... ",end = " ")
        self.feature_sel()
        print("   DONE!")
        
        print("Re-structing Dataset... ",end = " ")
        self.reframe()
        print("   DONE!")
        
        print("\n\n")
        print("DATASET is READY!!")
        print(self.Rinfo)
        return self.data
        
                

            
class DataAutomation2():
    import pandas as pd
    import numpy as np
    import warnings
    warnings.filterwarnings("ignore")
    
    def __init__(self,data,target):
        import pandas as pd
        import numpy as np
        import warnings
        warnings.filterwarnings("ignore")
        #print("In the Data Automation Class")
        self.info = {}
        self.originaldata = data
        self.target = target
        self.data = data
        self.idata = data #initial
        
        self.corrData = dict()
        self.Rinfo = ""
        self.ogc = self.data.columns
        
        
    
    def check_ftype(self,data,target):
        def check_date(df):
            df = df.astype(str)
            #print(df)
            s = ""
            def check_basic(x):
                l = x.split("-")
                if(len(l) == 3):
                    s = "-"
                    for i in l:
                        if(str(i).split()[0].isdigit() == False):
                            return False
                    return True
                l = x.split("/")
                if(len(l) == 3):
                    s = "/"
                    for i in l:
                        if(str(i).split()[0].isdigit() == False):
                            return False
                    return True
                return False
            """if(check_basic(x) == False):
                return False
            """
            try:
                x = df[0]
                if(check_basic(x)):
                    df = pd.to_datetime(df)
                    return True
                return False
            except:
                return False
        cols = data.columns
        info = {}
        i = 0
        for x in cols:
            #print(x)
            c = 0
            try:
                #Indexing
                if(i == 1):
                    pass
                elif(x.lower().strip() in ['id','userid','user']):
                    info[x] = 'index'
                    i = 1
                    c = 1
                else:    
                    df = data[x]
                    mn = min(df)
                    mx = max(df)
                    k = 0
                    for xx in df:
                        if(type(xx) != int):
                            k = 1
                            break
                    if(k == 0):
                        if(df.nunique() == len(df)):
                            i = 1
                            c = 1
                            info[x] = 'index'
            except:
                pass

            if(c == 1):
                continue

            if(data[x].dtype == 'O'):
                #Cat or Date
                #Cheking for date
                df = data[x].dropna()
                #Checking if it's  date
                if(check_date(df)):
                    c = 1
                    info[x] = 'date'
                else:
                    c = 1
                    #check if it's not Numeric in nature
                    try:
                        k = data[x].dropna().astype(int)
                        #v = int(data[x][0])
                        u = data[x].nunique()
                        if(u < 21 and u < len(data[x])/100):
                            
                            def insideapply(x):
                                try:
                                    return int(x)
                                except:
                                    try:
                                        return float(x)
                                    except:
                                        import numpy as np
                                        return np.nan
                            
                            self.data[x] = self.data[x].apply(insideapply)
                            info[x] = "cat" #'cat-num'
                            
                        else:

                            #v = data[x].mean()
                            info[x] = 'num'
                            
                    except:
                        info[x] = 'cat'
            else:
                df = data[x].dropna()
                if(check_date(df)):
                    c = 1
                    info[x] = 'date'
                else:
                    l = df.nunique()
                    n = len(df)
                    if(l < 15 and l < n/100):
                        #df[x] = df[x].astype(str)
                        
                        def insideapply(x):
                            try:
                                return str(x)
                            except:
                                return np.nan
                        
                        self.data[x] = self.data[x].apply(insideapply)
                        info[x] = 'cat' #num-cat
                    else:
                        info[x] = 'num'
            #print(x,info[x],data[x][0])

        return info
    
    
    
    def remove_outliers(self):
        
        #print(len(self.data))
        df = self.data
        for x in self.info:
            if(self.info[x] == 'num' and x != self.target):
                #remove outliers
                #df = self.data
                c = x
                s = df[x].skew()
                #print(len(df),x,s)
                if(s > 0.5):
                    c = x
                    q = df[c].quantile(0.97)
                    arr = []
                    for x in df[c]:
                        if(q - x > 0):
                            arr.append(x)

                    k = min(df[c].skew(),1)
                    df = df[df[c] <= q + (1 + k/1.3) * sum(arr) / (len(arr) + 1)]

                elif(s < -0.5):
                    c = x
                    q = df[c].quantile(0.03)
                    arr = []
                    for x in df[c]:
                        if(q - x < 0):
                            arr.append(x)

                    k = abs(min(df[c].skew(),1))
                    df = df[df[c] >= q - (1 + k/1.3) * sum(arr) / len(arr)]

                else:
                    if(s > 0):
                        q9 = df[c].quantile(0.997)
                        q1 = df[c].quantile(0.25)
                        q3 = df[c].quantile(0.80)
                        q1 = df[c].quantile(0.01)

                        iqr = q3 - q1
                        df = df[df[c] <= q9 + (1.7 + s) * iqr]

                        #LEFT PART
                        df = df[df[c] >= q1 - iqr]
                    else:
                        q9 = df[c].quantile(0.99)
                        q01 = df[c].quantile(0.003)
                        q1 = df[c].quantile(0.25)
                        q3 = df[c].quantile(0.85)

                        iqr = q3 - q1
                        df = df[df[c] >= q01 - (1.7 + s) * iqr]

                        #RIGHT PART
                        df = df[df[c] <= q9 + iqr]
                self.data = df
                #print(len(df))
                
            elif(self.info[x] == "cat" and x != self.target):
                import numpy as np
                #Category Outliers == check any others value_counts
                vc = df[x].value_counts()
                l = len(df)/200
                df[x] = np.where(df[x].isin(vc.index[vc >= l]),df[x],'OTHERS')
            

        #Fill NaN Value
    def fill_nan(self):
        import numpy as np
        df = self.data
        self.data = df[df[self.target].isnull()== False]
        #print(len(df))
            
        ndf = df.isnull().sum()
        l = len(df)/200
        for k in ndf.keys():
            
            if(ndf[k] == 0 or k == self.target):
                continue
            if(ndf[k] <= l):
                #0.5% RULE 
                #print(k,self.info[k],end = " ")
                #print("0.5 RULE")
                #print(len(df))
                self.data = df[df[k].isnull()== False]
                #print(len(df))
            else:
                if(self.info[k] == "cat"):
                    df[k].fillna("isMissing",inplace = True)
                elif(self.info[k] == 'num'):
                     df[k].fillna(df[k].mean(),inplace = True)
                else:
                    #print("INELSE DATE")
                    if(self.info[k] == 'date'):
                        #print(k,"INDATE")
                        df[k].fillna(method = 'ffill',inplace = True)
                        df[k].fillna(method = 'bfill',inplace = True)
                        
                     #continue
        
        
    
    #Feature Engineering 
        
    def feature_engg(self):
        #print(self.data.shape)
        import pandas as pd
            
        cat_f = []
        num_f = []
        date_f = []
        for x in self.info:
            if(x != self.target):
                if(self.info[x] == 'cat'):
                    cat_f.append(x)
                elif(self.info[x] == 'num'):
                    num_f.append(x)
                elif(self.info[x] == 'date'):
                    date_f.append(x)
                else:
                    continue 
            
        for i1 in range(len(cat_f) - 1):
            x1 = cat_f[i1]
            for i2 in range(i1 + 1,len(cat_f)):
                x2 = cat_f[i2]
                self.data[x1 + "-" + x2 + "-N"] = self.data[x1] + "_" + self.data[x2]
                self.info[x1 + "-" + x2 + "-N"] = "cat"
        
        for x1 in num_f:
            try:
                self.data[x1 + "-q-N"] = pd.cut(self.data[x1],6)
                self.info[x1 + "-q-N"] = 'cat'
            except:
                pass
            
        for x1 in date_f:
            self.data[x1] = pd.to_datetime(self.data[x1])
            self.data[x1 + "-M"] = self.data[x1].apply(lambda x :x.month)
            self.data[x1 + "-D"] = self.data[x1].apply(lambda x :x.day)
            self.data[x1 + "-Y"] = self.data[x1].apply(lambda x :x.year)
            self.data[x1 + "-W"] = self.data[x1].apply(lambda x :x.week % 7 + 1)
            self.data.drop(x1,inplace = True, axis = 1)
            
            self.info[x1 + "-D"] = "cat"
            self.info[x1 + "-Y"] = "cat"
            self.info[x1 + "-M"] = "cat"
            self.info[x1 + "-W"] = "cat"
            
            self.info.pop(x1)
        
        #print(self.data.shape)
    
    
    #feature Selection
    def feature_sel(self):
        from scipy import stats as ss
        import pandas as pd
        import numpy as np
        
        
        masterData = self.corrData
        
        df = self.data
        def corr1(x,y):
            #(data['D-y'],data[target1]) ----> CAT - CAT
            confusion_matrix = pd.crosstab(x,y)
            chi2 = ss.chi2_contingency(confusion_matrix)[0]
            n = confusion_matrix.sum().sum()
            phi2 = chi2/n
            r,k = confusion_matrix.shape
            phi2corr = max(0, phi2-((k-1)*(r-1))/(n-1))
            rcorr = r-((r-1)**2)/(n-1)
            kcorr = k-((k-1)**2)/(n-1)
            return np.sqrt(phi2corr/min((kcorr-1),(rcorr-1)))
        
        
            
            
        corr = self.data.corr(method = "spearman")
        
        def corr2(x,y):
            #CAT-NUM
            ########################################## CHECK!!
            # Running the one-way anova test 
            # Assumption(H0) is that FuelType and CarPrices are NOT correlated
            #x : cat, y : num
            dff = self.data.groupby(x)[y].apply(list)
            if(len(dff) < 2): ##############CHECK THIS
                return False
            ar = ss.f_oneway(*dff)
            ## We accept the Assumption(H0) only when P-Value >0 0.05
            return ar.pvalue < 0.05
        
        
        for x in self.data.columns:
            #print(x,end = " ")
            if(self.info[self.target] == 'cat'):
                if(self.info[x] == 'cat'):
                    if(self.target != x):
                        masterData[x] = corr1(self.data[x],self.data[self.target])
                        #print("CAT_CAT",end = " ")
                        #print(masterData[x])
                        #self.corrli.append(corr1(self.data[x],self.data[self.target]))
                elif(self.info[x] == 'num'):
                    if(self.target != x):
                        #cat - num
                        masterData[x] = corr2(self.target,x)
                        #print("CAT_NUM",end = " ")
                        #print(masterData[x])
                    
                        
                        
                
            elif(self.info[self.target] == 'num'):
                if(self.info[x] == 'num'):
                    if(self.target != x):
                        masterData[x] = corr[x][self.target]
                        #print("NUM_NUM",end = " ")
                        #print(masterData[x])
                elif(self.info[x] == 'cat'):
                    if(self.target != x):
                        #cat - num
                        masterData[x] = corr2(x,self.target)
                        #print("NUM_CAT",end = " ")
                        #print(masterData[x])
            
        #print(masterData)
        li = []
        li.append(self.target)
        for x in masterData:
            if(masterData[x] >= 0.06):
                li.append(x)
            elif(x in self.ogc):
                li.append(x)
        
        self.data = self.data[li]
        self.idata = self.data.copy()
        
                        
    
    def reframe(self):
        import pandas as pd
        from scipy import stats as ss
        def corr2(x,y,df):
            #CAT-NUM
            ########################################## CHECK!!
            # Running the one-way anova test 
            # Assumption(H0) is that FuelType and CarPrices are NOT correlated
            #x : cat, y : num
            dff = df.groupby(x)[y].apply(list)
            ar = ss.f_oneway(*dff)
            ## We accept the Assumption(H0) only when P-Value >0 0.05
            return ar.pvalue < 0.05
        
        data = self.data
        cat = []
        num = []
        remF = [] #DISBURSED-AMT/HIGH CREDIT_2,00,000
        
        for x in self.data.columns:
            if(x != self.target and self.info[x] == 'cat'):
                cat.append(x)
            elif(x != self.target and self.info[x] == 'num'):
                num.append(x)
                
        for x in cat:
            data[x] = data[x].astype(str)
            df = pd.DataFrame()
            df['target'] = self.data[self.target]
            
            for xx in data[x].unique():
                
                df[xx] = data[x].apply(lambda y : 1 if y == xx else 0)
                if(self.info[self.target] == 'num'):
                    if(df.corr(method = 'kendall')['target'][xx] < 0.1):
                        remF.append(x + "_" + xx)
                if(self.info[self.target] == 'cat'):
                    if(corr2("target",xx,df) == False):
                        remF.append(x + "_" + xx)
            
                    
                
                
            
        self.data = pd.get_dummies(data,columns = cat)
        self.data.drop(remF,axis = 1,inplace = True)
        
        print(cat,data.shape)
        
        
    
    
    def run(self):
        print("Created by Himanshu & Amit & d\Dr. S. Vigneshwari\n")
        
        print("Checking Data Type... ",end = " ")
        #FInding the data type of the columns of the dataset
        self.info = self.check_ftype(self.data,self.target)
        print("   DONE!")
        
        #print(self.info)
        
        print("Dealing with Outliers & useless data... ",end = " ")
        self.remove_outliers()
        #removing outliers from Numeric dataset
        self.fill_nan()
        print("   DONE!")
        
        print("Building new features... ",end = " ")
        self.feature_engg()
        print("   DONE!")
        
        print("Finding best features... ",end = " ")
        self.feature_sel()
        print("   DONE!")
        
        
        print("Re-structing Dataset... ",end = " ")
        self.reframe()
        print("   DONE!")
        
        print("\n\n")
        print("DATASET is READY!!")
        print(self.Rinfo)
        return self.data
        
        
    def insight(self):
        print("Inside Insight Function!")
        import matplotlib.pyplot as plt
        import seaborn as sns
        import numpy as np
        plt.style.use('ggplot')
        
        best_f = [x for x in self.corrData if self.corrData[x] > 0.3]
        
        #fig, axes = plt.subplots(figsize=(40, 20))
        #fig, axes = plt.subplots(len(best_f), 1,figsize=(40,20))
        #fig.subplots_adjust(hspace=0.8)
        sns.set(font_scale=1.2)
        sns.set()
        color=[plt.cm.prism_r(each) for each in np.linspace(0, 1, len(best_f))]
        #axs = axes.flatten()
        
        
        i = 0
        for f in best_f:
            if(self.corrData[f] < 0.3 or f == self.target):
                continue
            print(f)
            #ax = axs[i]
            if(self.info[self.target] == 'num'):
                #Targte is Num        
                
                if(self.info[f] == 'cat'):
                    sns.swarmplot(x=self.idata[f], y=self.idata[self.target], fit_reg=True,marker='o',scatter_kws={'s':50,'alpha':0.7},color=color[i],ax=ax)
                    plt.xlabel(str(f),fontsize=12)
                    plt.ylabel(str(self.target),fontsize=12)
                    ax.set_title(str(self.target)+' - '+str(f),color=color[i],fontweight='bold',size=20)
                    plt.xticks(rotation=60)
                    
                elif(self.info[f] == 'num'):
                    sns.regplot(x=f, y=self.target,color=color[i],ax=ax,data = self.idata)
                    plt.xlabel(str(f),fontsize=12)
                    plt.ylabel(str(self.target),fontsize=12)
                    ax.set_title(str(self.target)+' - '+str(f),color=color[i],fontweight='bold',size=20)

                    
                elif(self.info[f] == 'date'):
                    pass
                else:
                    continue

            elif(self.info[self.target] == 'cat'):
                #Target is Cat
                
                if(self.info[f] == 'cat'):
                    sns.catplot(x=f,kind = 'count', hue = self.target,data = self.idata)
                    plt.ylabel(str(f),fontsize=12)
                    plt.xlabel(str(self.target),fontsize=12)
                    #ax.set_title(str(self.target)+' - '+str(f),color=color[i],fontweight='bold',size=20)
                    plt.xticks(rotation=60)
                    
                elif(self.info[f] == 'num'):
                    sns.boxplot(x=self.target,y=f,data = self.idata)
                    plt.ylabel(str(f),fontsize=12)
                    plt.xlabel(str(self.target),fontsize=12)
                    #ax.set_title(str(self.target)+' - '+str(f),color=color[i],fontweight='bold',size=20)
                    plt.xticks(rotation=60)
                    
                elif(self.info[f] == 'date'):
                    pass
                else:
                    continue

            else:
                assert "SORRy!"
            
            i += 1
                
                
        
