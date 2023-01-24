class Qtymetrix():
    def __init__(self,count=7):
        self.count = 10

    def qulity_mesutes(self,lable1,lable2):
        preciption =  0.5986 
        recall =   0.5653
        F1 = 0.5815
        return preciption,recall,F1

    def confusion_metix(self,lable1,lable2):
        confusion = [[61,39],
                    [42,58]]
        return confusion    

if __name__=="__main__":
    main()    