import configparser
import os
from SWANi.utils.APPLABELS import APPLABELS

class SWANiConfig(configparser.ConfigParser):
    configFile=os.path.abspath(os.path.join(os.path.expanduser("~"),"."+APPLABELS.APPNAME+"config"))
    patientConfiguration= configparser.ConfigParser()
    INPUTLIST=['mr_t13d',
                            'mr_flair3d',
                            'mr_mdc',
                            'mr_venosa',
                            'mr_venosa2',
                            'mr_dti',
                            'mr_asl',
                            'ct_brain',
                            'mr_fmri',
                            'pet_brain',
                            'op_mr_flair2d_tra',
                            'op_mr_flair2d_cor',
                            'op_mr_flair2d_sag']

    TRACTS={}
    TRACTS["af"]=['Arcuate Fasciculus','true']
    TRACTS["cst"]=['Corticospinal Tract','true']
    TRACTS["or"]=['Optic Radiation','true']
    TRACTS["ar"]=['Acoustic Radiation','false']
    TRACTS["fa"]=['Frontal Aslant','false']
    TRACTS["fx"]=['Fornix','false']
    TRACTS["ifo"]=['Inferior Fronto-Occipital Fasciculus','false']
    TRACTS["ilf"]=['Inferior Longitudinal Fasciculus','false']
    TRACTS["uf"]=['Uncinate Fasciculus','false']

    def __init__(self):
        super(SWANiConfig,self).__init__()

        self.createDefaultConfig()

        if os.path.exists(self.configFile):
            self.read(self.configFile)

        self.save()

    def reLoad(self):
        self.read(self.configFile)

    def createDefaultConfig(self):


        self['MAIN'] = {'patientsfolder': '',
                        'patientsprefix': 'pt_',
                        'slicerPath':'',
                        'shortcutPath':'',
                        'freesurfer':'true',
                        'hippoAmygLabels':'true',
                        'domap':'false',
                        'maxPt':'1',
                        'maxPtCPU':'-1',
                        'defaultWfType':'0'}

        self['OPTIONAL_SERIES'] = {'mr_flair2d':'false'}

        self['DEFAULTFOLDERS']={}
        for this in self.INPUTLIST:
            self['DEFAULTFOLDERS']['default_'+this+'_folder']='dicom/'+this+'/'

        self['DEFAULTNAMESERIES'] = {}
        for name in self.INPUTLIST:
            self['DEFAULTNAMESERIES']["Default_"+name+"_name"]=""

        self['DEFAULTTRACTS'] = {}

        for index,key in enumerate(self.TRACTS):
            self['DEFAULTTRACTS'][key]= self.TRACTS[key][1]

        self['PIDS'] = {}


    def save(self):
        with open(self.configFile,"w") as openedFile:
            self.write(openedFile)

    def getConfig(self,section,name):
        try:
            return self[section][name]
        except NameError:
            return ""

    def setConfig(self,section,name,value):
        self[section][name]=value

    def getPatientsFolder(self):
        return self.getConfig("MAIN","PatientsFolder")
