import shutil
import os
class AutoChecker():
    def __init__(self,weight):
        self.separator  = '/'
        self.dot = '.'
        self.weight = weight
        self.weights_path =  self.dot + self.separator  + self.separator.join(self.weight.split(self.separator)[1:-1])
        self.version = self.weights_path + self.separator + "version"
        self.name = self.weight.split(self.separator)[-1]
    def auto_check(self, net):
        files = os.listdir(self.weights_path)
        if len(files) > 2:
            list_file = ['version', self.name]
            new_weights = [x for x in files if x not in list_file]
            new_weight = self.weights_path + self.separator + new_weights[0]
            net.load_model(new_weight)
            self.changing(new_weight)
    def changing(self,new_weight):
        shutil.move(self.weight, self.version)
        self.weight = new_weight
        self.name = self.weight.split(self.separator)[-1]