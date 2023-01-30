import subprocess
import shutil
from . import utils
import glob
import os

class files_from_data_dir():
    def __init__(self,name,root_path,spartan_path,ini_date):
        self.name = name
        self.run_path = f'{root_path}run/{ini_date.strftime("%Y%m%d%H")}/'
        self.spartan_path = spartan_path
        self.idate = ini_date

    def copy_files(self):
        self.out_grd_path=f'{self.spartan_path}{self.idate.strftime("%Y%m%d%H")}_{self.name}/out_grd.ww3'
        self.out_pnt_path=f'{self.spartan_path}{self.idate.strftime("%Y%m%d%H")}_{self.name}/out_pnt.ww3'
        if utils.verify_files(self.out_grd_path) and utils.verify_files(self.out_pnt_path):
            os.system(f'cp {self.out_grd_path} {self.run_path}')
            os.system(f'cp {self.out_pnt_path} {self.run_path}')
            os.system(f'cp {self.spartan_path}{self.idate.strftime("%Y%m%d%H")}_{self.name}/log.ww3 {self.run_path}')
            os.system(f'cp {self.spartan_path}{self.idate.strftime("%Y%m%d%H")}_{self.name}/restart*.ww3 {self.run_path}')
        else:
            raise UserWarning('WW3 has to be runned before post-processing the results')

class ounf():
    def __init__(self,root_path,ini_date,ounf_dict):
        self.run_path = f'{root_path}run/{ini_date.strftime("%Y%m%d%H")}/'
        self.inp_path = f'{root_path}info/inp/'
        self.ounf_dict = ounf_dict

    def fill_ounf(self):
        shutil.copy(f'{self.inp_path}ww3_ounf.inp_code', f'{self.run_path}ww3_ounf.inp')
        utils.fill_files(f'{self.run_path}ww3_ounf.inp',self.ounf_dict)

    def run_ounf(self):
        print ('\n*** Running post-processing to generate field outputs ***\n')
        f = open(f'{self.run_path}ounf.log', "w") 
        subprocess.call([f'{self.run_path}ww3_ounf'],cwd=self.run_path,stdout=f)  

class ounp():
    def __init__(self,root_path,ini_date,ounp_dict):
        self.run_path = f'{root_path}run/{ini_date.strftime("%Y%m%d%H")}/'
        self.inp_path = f'{root_path}info/inp/'
        self.ounp_dict = ounp_dict

    def fill_ounp(self):
        shutil.copy(f'{self.inp_path}ww3_ounp.inp_code', f'{self.run_path}ww3_ounp.inp')
        utils.fill_files(f'{self.run_path}ww3_ounp.inp',self.ounp_dict)

    def run_ounp(self):
        print ('\n*** Running post-processing to generate point outputs ***\n')     
        f = open(f'{self.run_path}ounp.log', "w") 
        subprocess.call([f'{self.run_path}ww3_ounp'],cwd=self.run_path,stdout=f)  

class copy_results():
    def __init__(self,root_path,ini_date) -> None:
        self.run_path = f'{root_path}run/{ini_date.strftime("%Y%m%d%H")}/'
        self.data_path = f'{root_path}data/{ini_date.strftime("%Y%m%d%H")}/'

    def copy(self):
        print ('\n*** Copying results to data folder ***\n')

        for filename in glob.glob(f'{self.run_path}ww3.*.nc'):
            shutil.copy(filename, f'{self.data_path}')

        for filename in glob.glob(f'{self.run_path}ww3_*.inp'):
            shutil.copy(filename, f'{self.data_path}')

        for filename in glob.glob(f'{self.run_path}*'):
            if 'log' in filename:
                shutil.copy(filename, f'{self.data_path}')

if __name__ == '__main__':
    # print_a() is only executed when the module is run directly.
    print('executed directly')