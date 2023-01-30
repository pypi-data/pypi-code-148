import subprocess
import os
import shutil
from . import utils
import wget
import fileinput

class buoys_matcher():
    def __init__(self,root_path,ini_date) -> None:
        self.run_path = f'{root_path}run/{ini_date.strftime("%Y%m%d%H")}/'
        self.inp_plots_path = f'{root_path}info/plots/'
    
    def dwnd_one_buoy(self,buoy_id):
            name_buoy_file=buoy_id+'h2020.txt.gz'
            url = 'https://www.ndbc.noaa.gov/data/historical/stdmet/'+name_buoy_file
            filename = wget.download(url,self.inp_plots_path)
            os.system(f'gzip -d {self.inp_plots_path}{name_buoy_file}')
            os.system(f'rm {self.inp_plots_path}{name_buoy_file}')

    def dwnd_all_buoys(self):
        name_buoys=['42056','42057','42058','42059','42060']
        for buoy in name_buoys:
            self.check_file=utils.verify_files(f'{self.inp_plots_path}{buoy}h2020.txt')
            if not self.check_file:
                self.dwnd_one_buoy(buoy)

class running_ww3():
    def __init__(self,name,root_path,spartan_path,ini_date,shel_dict,run_mode):
        self.name = name
        self.run_path = f'{root_path}run/{ini_date.strftime("%Y%m%d%H")}/'
        self.spartan_path = spartan_path
        self.inp_path = f'{root_path}info/inp/'
        self.shel_dict = shel_dict
        self.run_mode = run_mode
        self.idate = ini_date
    
    def fill_shel(self):
        print ('\n*** Editing ww3_shel.inp ***\n')
        shutil.copy(f'{self.inp_path}ww3_shel.inp_code', f'{self.run_path}ww3_shel.inp')
        utils.fill_files(f'{self.run_path}ww3_shel.inp',self.shel_dict)

    def run_shel(self):
        print ('\n*** Running main program: ww3_shel ***\n')
        if self.run_mode!='spartan':
            f = open('shel.log', "w") 
            subprocess.call([f'{self.run_path}ww3_shel'],cwd=self.run_path,stdout=f)  
            shutil.move('shel.log', f'{self.run_path}shel.log')
        else:
            shutil.copy(f'{self.inp_path}template.slurm', f'{self.run_path}{self.name}.slurm')
            with fileinput.FileInput(f'{self.run_path}{self.name}.slurm',inplace=True, backup='') as file:
                for line in file:
                    print(line.replace('name_job',self.name),end='')

            os.system(f'mkdir -p {self.spartan_path}{self.idate.strftime("%Y%m%d%H")}_{self.name}')
            os.system(f'cp -r {self.run_path}*.ww3 {self.spartan_path}{self.idate.strftime("%Y%m%d%H")}_{self.name}')
            os.system(f'cp -r {self.run_path}ww3_shel* {self.spartan_path}{self.idate.strftime("%Y%m%d%H")}_{self.name}')
            os.system(f'cp -r {self.run_path}*.slurm {self.spartan_path}{self.idate.strftime("%Y%m%d%H")}_{self.name}')
        self.out_grd_path=f'{self.spartan_path}{self.idate.strftime("%Y%m%d%H")}_{self.name}/out_grd.ww3'
        self.out_pnt_path=f'{self.spartan_path}{self.idate.strftime("%Y%m%d%H")}_{self.name}/out_pnt.ww3'
        if utils.verify_files(self.out_grd_path) and utils.verify_files(self.out_pnt_path):
            print('\n The case has been runned in Spartan \n')
        else:
            raise UserWarning('The slurm file has to be launched to the queue for the execution \n with 2 nodes and 16 tasks can take around 3.5 hours')