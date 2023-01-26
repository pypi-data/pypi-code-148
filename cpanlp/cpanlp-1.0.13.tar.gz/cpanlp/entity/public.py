from cpanlp.entity.LLC import *
class PublicCompany(LLC):
    def __init__(self,name,type,capital):
        super().__init__(name,type,capital)
        self.shareholders=[]
        self.stock_price = 0.0
def main():
    print("hello")
    a=PublicCompany("华为","niu",1000)
if __name__ == '__main__':
    main()