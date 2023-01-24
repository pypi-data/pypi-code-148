"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/stable/plugins/guides.html?#widgets

Replace code below according to your needs.
"""
from typing import TYPE_CHECKING
from napari.utils.notifications import show_info
from napari.utils import progress
from magicgui import magic_factory
from qtpy.QtWidgets import QHBoxLayout, QPushButton, QWidget, QLineEdit, QLabel, QFileDialog, QVBoxLayout, QGridLayout, QFormLayout, QGroupBox, QDialog, QSpinBox, QListWidget, QListWidgetItem, QComboBox
from PyQt5.QtGui import QPalette, QColor
from magicgui.widgets import Table
from skimage import img_as_ubyte
from skimage.io import imread, imsave
from collections import Counter
import numpy as np
import pandas as pd

import os
import pathlib
import tempfile
import subprocess
import shutil
import sys

from manini.script2 import TableWidget,comboCompanies

from zipfile import ZipFile        
from magicgui.tqdm import trange

from time import process_time

if TYPE_CHECKING:
    import napari

class Image_segmentation(QDialog):
    
    def __init__(self, parent: QWidget):
        print("Image segmentation OPEN")
        super().__init__(parent)
        self.setWindowTitle("Image segmentation")
        self.number = QSpinBox()
        
        self.filename_edit = QLineEdit()  
        
        self.file_name_image = QPushButton("File")
        self.filename_edit_image = QLineEdit()  
        self.file_name_image.clicked.connect(self.open_file_dialog_image)
        
        self.file_name_model = QPushButton("File")
        self.filename_edit_model = QLineEdit()  
        self.file_name_model.clicked.connect(self.open_file_dialog_model)

        self.file_name_class_name = QPushButton("File")
        self.filename_edit_class_name = QLineEdit()  
        self.file_name_class_name.clicked.connect(self.open_file_dialog_class_name)
        
        self.ok_btn = QPushButton("OK") #OK
        self.cancel_btn = QPushButton("Cancel") #Cancel
        
        layout = QGridLayout()
        
        notice_utilization = """
        Dedicated tool for image segmentation.
        Import two elements:
        - A compressed file in zip format including only one or more images
        - A file in h5 format which is an image segmentation model
        - A file in txt format which is located classes names (optional)
        """
        
        layout.addWidget(QLabel(notice_utilization), 0, 1)        
        layout.addWidget(QLabel("Image:"), 1, 0)        
        layout.addWidget(self.filename_edit_image, 1, 1)
        layout.addWidget(self.file_name_image, 1, 2)
        layout.addWidget(QLabel("Model:"), 2, 0)        
        layout.addWidget(self.filename_edit_model, 2, 1)
        layout.addWidget(self.file_name_model, 2, 2)
        layout.addWidget(QLabel("Class (optional):"), 3, 0)        
        layout.addWidget(self.filename_edit_class_name, 3, 1)
        layout.addWidget(self.file_name_class_name, 3, 2)
        
        layout.addWidget(self.ok_btn, 4, 1)
        layout.addWidget(self.cancel_btn, 4, 2)
        self.setLayout(layout)
               
        self.ok_btn.clicked.connect(self.accept) #OK
        self.cancel_btn.clicked.connect(self.reject) #Cancel
        
        self.setFixedHeight(400)
        
    def open_file_dialog_image(self):
        filename, ok = QFileDialog.getOpenFileName(
            self,
            "Select a File", 
            str(pathlib.Path.home()), 
            "Images (*.png *.jpg *.zip)"
        )
        if filename:
            path = pathlib.Path(filename)
            self.filename_edit_image.setText(str(path))     
            name_file = str(path)
            if name_file.endswith((".jpg",".JPG",".png",".PNG",".tiff",".tif")):
                print('Image DETECTED')
            elif name_file.endswith((".zip",".ZIP")):
                print('Compressed file DETECTED')
            else:
                print('Image NOT DETECTED')
            
    def open_file_dialog_model(self):
        filename, ok = QFileDialog.getOpenFileName(
            self,
            "Select a File", 
            str(pathlib.Path.home()), 
            "Model (*.ilp *.h5)"
        )
        if filename:
            path = pathlib.Path(filename)
            self.filename_edit_model.setText(str(path))  
            name_file = str(path)
            if name_file.endswith(".ilp"):
                print('Ilastik model DETECTED')
            elif name_file.endswith(".h5"):
                print('Tensorflow model DETECTED')
            else:
                print('Model NOT DETECTED')

    def open_file_dialog_class_name(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select a File", 
            str(pathlib.Path.home()), 
            "File (*.txt)"
        )
        if filename:
            path = pathlib.Path(filename)
            self.filename_edit_class_name.setText(str(path))  
            name_file = str(path)
            if name_file.endswith(".txt"):
                print('.txt file DETECTED')
            elif len(name_file)==0:
                print('No .txt file DETECTED')
            else:
                print('.txt file NOT DETECTED')

                            
class Image_classification(QDialog):
    
    def __init__(self, parent: QWidget):
        print("Image classification OPEN")
        super().__init__(parent)
        self.setWindowTitle("Image classification")
        self.number = QSpinBox()
        
        self.filename_edit = QLineEdit()  
        
        self.file_name_image = QPushButton("File")
        self.filename_edit_image = QLineEdit()  
        self.file_name_image.clicked.connect(self.open_file_dialog_image)
        
        self.file_name_model = QPushButton("File")
        self.filename_edit_model = QLineEdit()  
        self.file_name_model.clicked.connect(self.open_file_dialog_model)

        self.file_name_class_name = QPushButton("File")
        self.filename_edit_class_name = QLineEdit()  
        self.file_name_class_name.clicked.connect(self.open_file_dialog_class_name)
        
        self.ok_btn = QPushButton("OK") #OK
        self.cancel_btn = QPushButton("Cancel") #Cancel
        
        layout = QGridLayout()
        # layout.addWidget(QLabel("Number:"), 0, 0)
        # layout.addWidget(self.number, 0, 1)
        
        notice_utilization = """
        Dedicated tool for instance segmentation.
        Import two elements:
        - A compressed file in zip format including only one or more images
        - A file in ilp format which is an image segmentation template
        """
        
        layout.addWidget(QLabel(notice_utilization), 0, 1)        
        layout.addWidget(QLabel("Image:"), 1, 0)        
        layout.addWidget(self.filename_edit_image, 1, 1)
        layout.addWidget(self.file_name_image, 1, 2)
        layout.addWidget(QLabel("Model:"), 2, 0)        
        layout.addWidget(self.filename_edit_model, 2, 1)
        layout.addWidget(self.file_name_model, 2, 2)
        layout.addWidget(QLabel("Class:"), 3, 0)        
        layout.addWidget(self.filename_edit_class_name, 3, 1)
        layout.addWidget(self.file_name_class_name, 3, 2)
        
        layout.addWidget(self.ok_btn, 4, 1)
        layout.addWidget(self.cancel_btn, 4, 2)
        self.setLayout(layout)
               
        self.ok_btn.clicked.connect(self.accept) #OK
        self.cancel_btn.clicked.connect(self.reject) #Cancel
        
        self.setFixedHeight(400)
        
    def open_file_dialog_image(self):
        filename, ok = QFileDialog.getOpenFileName(
            self,
            "Select a File", 
            str(pathlib.Path.home()), 
            "Images (*.zip)"
        )
        if filename:
            path = pathlib.Path(filename)
            self.filename_edit_image.setText(str(path))     
            name_file = str(path)
            if name_file.endswith((".zip")):
                print('Compressed file DETECTED')
            else:
                print('Compressed file NOT DETECTED')
            
    def open_file_dialog_model(self):
        filename, ok = QFileDialog.getOpenFileName(
            self,
            "Select a File", 
            str(pathlib.Path.home()), 
            "Model (*.h5)"
        )
        if filename:
            path = pathlib.Path(filename)
            self.filename_edit_model.setText(str(path))  
            name_file = str(path)
            if name_file.endswith(".ilp"):
                print('Ilastik model DETECTED')
            elif name_file.endswith(".h5"):
                print('Tensorflow model DETECTED')
            else:
                print('Model NOT DETECTED')

    def open_file_dialog_class_name(self):
        filename, ok = QFileDialog.getOpenFileName(
            self,
            "Select a File", 
            str(pathlib.Path.home()), 
            "File (*.txt)"
        )
        if filename:
            path = pathlib.Path(filename)
            self.filename_edit_class_name.setText(str(path))  
            name_file = str(path)
            if name_file.endswith(".txt"):
                print('.txt file DETECTED')
            else:
                print('.txt file NOT DETECTED')

class Object_detection(QDialog):
    
    def __init__(self, parent: QWidget):
        print("Object detection OPEN")
        super().__init__(parent)
        self.setWindowTitle("Object detection")
        self.number = QSpinBox()
        
        self.filename_edit = QLineEdit()  
        
        self.file_name_darknet = QPushButton("File")
        self.filename_edit_darknet = QLineEdit()  
        self.file_name_darknet.clicked.connect(self.open_file_dialog_darknet)
        
        self.file_name_obj_data = QPushButton("File")
        self.filename_edit_obj_data = QLineEdit()  
        self.file_name_obj_data.clicked.connect(self.open_file_dialog_obj_data)
        
        self.file_name_architecture = QPushButton("File")
        self.filename_edit_architecture = QLineEdit()  
        self.file_name_architecture.clicked.connect(self.open_file_dialog_architecture)
        
        self.file_name_weight = QPushButton("File")
        self.filename_edit_weight = QLineEdit()  
        self.file_name_weight.clicked.connect(self.open_file_dialog_weight)
        
        self.file_name_folder_image_txt = QPushButton("File")
        self.filename_edit_folder_image_txt = QLineEdit()  
        self.file_name_folder_image_txt.clicked.connect(self.open_file_dialog_folder_image_txt)
        
        self.ok_btn = QPushButton("OK") #OK
        self.cancel_btn = QPushButton("Cancel") #Cancel
    
        layout = QGridLayout()
        # layout.addWidget(QLabel("Number:"), 0, 0)
        # layout.addWidget(self.number, 0, 1)
        
        notice_utilization = """
        Dedicated tool for detection object based on YOLOv4 algorithm.
        Import four elements:
        - The obj.data file that indicates the path of the obj.names file 
        - A file presenting the architecture of your YOLOv4 model
        - A file presenting your weights of the model
        - A file in txt format that indicates the path of the images
        """
        
        layout.addWidget(QLabel(notice_utilization), 0, 1)      
        layout.addWidget(QLabel("Darknet folder :"), 1, 0)        
        layout.addWidget(self.filename_edit_darknet, 1, 1)
        layout.addWidget(self.file_name_darknet, 1, 2)    
        layout.addWidget(QLabel("Obj.data (.data format):"), 2, 0)        
        layout.addWidget(self.filename_edit_obj_data, 2, 1)
        layout.addWidget(self.file_name_obj_data, 2, 2)
        layout.addWidget(QLabel("Model architecture (.cfg format):"), 3, 0)        
        layout.addWidget(self.filename_edit_architecture, 3, 1)
        layout.addWidget(self.file_name_architecture, 3, 2)
        layout.addWidget(QLabel("Weight (.weights format):"), 4, 0)        
        layout.addWidget(self.filename_edit_weight, 4, 1)
        layout.addWidget(self.file_name_weight, 4, 2)
        layout.addWidget(QLabel("File of image paths (.txt format):"), 5, 0)        
        layout.addWidget(self.filename_edit_folder_image_txt, 5, 1)
        layout.addWidget(self.file_name_folder_image_txt, 5, 2)
        
        layout.addWidget(self.ok_btn, 6, 1)
        layout.addWidget(self.cancel_btn, 6, 2)
        self.setLayout(layout)
               
        self.ok_btn.clicked.connect(self.accept) #OK
        self.cancel_btn.clicked.connect(self.reject) #Cancel
        
        self.setFixedHeight(400)
        
    def open_file_dialog_obj_data(self):
        filename, ok = QFileDialog.getOpenFileName(
            self,
            "Select a File", 
            str(pathlib.Path.home()), 
            "File (*.data)"
        )
        if filename:
            path = pathlib.Path(filename)
            self.filename_edit_obj_data.setText(str(path))     
            name_file = str(path)
            if name_file.endswith(".data"):
                print('.data file DETECTED')
            else:
                print('.data file NOT DETECTED')

    def open_file_dialog_architecture(self):
        filename, ok = QFileDialog.getOpenFileName(
            self,
            "Select a File", 
            str(pathlib.Path.home()), 
            "Model (*.cfg)"
        )
        if filename:
            path = pathlib.Path(filename)
            self.filename_edit_architecture.setText(str(path))  
            name_file = str(path)
            if name_file.endswith(".cfg"):
                print('Model DETECTED')
            else:
                print('Model NOT DETECTED')
                
    def open_file_dialog_weight(self):
        filename, ok = QFileDialog.getOpenFileName(
            self,
            "Select a File", 
            str(pathlib.Path.home()), 
            "Model (*.weights)"
        )
        if filename:
            path = pathlib.Path(filename)
            self.filename_edit_weight.setText(str(path))  
            name_file = str(path)
            if name_file.endswith(".weights"):
                print('Weight model DETECTED')
            else:
                print('Weight model NOT DETECTED')
                                
    def open_file_dialog_folder_image_txt(self):
        filename, ok = QFileDialog.getOpenFileName(
            self,
            "Select a File", 
            str(pathlib.Path.home()), 
            "Model (*.txt)"
        )
        if filename:
            path = pathlib.Path(filename)
            self.filename_edit_folder_image_txt.setText(str(path))  
            name_file = str(path)
            if name_file.endswith(".txt"):
                print('File of image paths DETECTED')
            else:
                print('File of image paths NOT DETECTED')
                
    def open_file_dialog_darknet(self):
        filename = QFileDialog.getExistingDirectory(
            self,
            "Select a Directory", 
            str(pathlib.Path.home())
        )
        if filename:
            path = pathlib.Path(filename)
            self.filename_edit_darknet.setText(str(path))  
            name_file = str(path)
            if os.path.isdir(name_file):
                print('Folder DETECTED')
            else:
                print('Folder NOT DETECTED')
                
class Run_interface_classification:
    def __init__(self,x,y_list,current_viewer,output_dir):
        self.idx = x
        self.image_zip = y_list[0]
        self.model = y_list[1]
        self.classe_file = y_list[2]
        self.napari_current_viewer = current_viewer
        self.temp_output_dir = output_dir
    def run_model(self):
        dico = {1:'Image Segmentation',2:'Object Classification',3:'Image Classification',4:'Detection'}
        if self.model.endswith(".ilp"):
            root_pc = str(pathlib.Path.home()).split("\\")[0]+"\\Program Files"
            check_version = [ix for ix in os.listdir(root_pc) if ix.find('ilastik')!=-1]
            if len(check_version)==0:
                show_info('ILASTIK NOT INSTALLED')
                return (dico[self.idx],'') #NO ILASTIK INSTALLED
            else:
                ilastik_version = check_version[0]
                show_info('ILASTIK VERSION:'+ilastik_version)
                return (dico[self.idx],ilastik_version)
        elif self.model.endswith(".h5"):
            return (dico[self.idx],'Run tensorflow')
    
    def run_tensorflow_classification(self,tensorflow_version):
        import tensorflow as tf
        from tensorflow.keras import backend as K
        import cv2
        import random
        
        model_New_load = tf.keras.models.load_model(self.model)
        
        _, IMG_SIZE_H, IMG_SIZE_W,_ = list(model_New_load.input.shape)
        
        def create_data(path):
            image_name = []
            data = []
            print()
            
            for img in os.listdir(path):  # iterate over each image per plants and weeds
                img_procee = img.lower()
                if img_procee.endswith(('.tif','.png','.jpg')):
                    image_name.append(img)
                    img_array = cv2.imread(os.path.join(path,img))  # convert to array 
                    new_array = cv2.resize(img_array, (IMG_SIZE_H, IMG_SIZE_W))  # resize to normalize data size
                    data.append(new_array)  # add this to our training_data
            random.shuffle(data)
            X = data  # An Array for images
            X = np.array(X).reshape(-1, IMG_SIZE_H, IMG_SIZE_W, 3)  # Reshape data in a form that is suitable for keras
            return X,image_name

        with ZipFile(self.image_zip,'r') as zipObject:
            listOfFileNames = zipObject.namelist()

    
            pbar = progress(range(len(listOfFileNames)))

            for i in pbar:
                image_name = listOfFileNames[i]
                zipObject.extract(listOfFileNames[i],path=self.temp_output_dir.name)
                
            txt_file_path = self.classe_file

            X_test,image_name = create_data(self.temp_output_dir.name)
            X_test = X_test.astype('float32') / 255.

            with open(txt_file_path) as file:
                lines = file.readlines()
            file.close()

            self.LABEL_CATEGORY = [x.split('\n')[0] for x in lines]
            image_name_temp = [ ix.split(".")[0] for ix in image_name]

            dico_pred = {}
            n = len(image_name_temp)
            m = len(self.LABEL_CATEGORY)
            class_list = [[] for _ in range(m+1)] #Classe predite , % class1, % class2, ..., % classn
            self.prob_class = []
            for idx in range(n):
                temp = np.zeros((1,224,224,3))
                temp[0] = X_test[idx,:,:,:]
                preds_test_0 = model_New_load.predict(temp, verbose=1)

                preds_test_0 = preds_test_0.flatten()

                for imx,ipx in zip(range(m),preds_test_0):
                    class_list[imx].append(ipx)

                dico_pred_idx = {}
                for i,j in zip(self.LABEL_CATEGORY,preds_test_0):
                    dico_pred_idx[i]=j

                label_pred = max(dico_pred_idx, key=dico_pred_idx.get)
                class_list[-1].append(label_pred)
                self.prob_class.append(max(preds_test_0))

            dico_pred['nom']=image_name_temp
            dico_pred['prediction']=class_list[-1]
            dico_pred['prob']=self.prob_class
            for class_nom,idx in zip(self.LABEL_CATEGORY,range(m)):
                dico_pred[class_nom]=class_list[idx]
            self.dico_output_prediction = dico_pred
    
    def image_vis(self):

        def table_to_widget(table: dict, LABEL_CATEGORY: list) -> QWidget:
            """
            Takes a table given as dictionary with strings as keys and numeric arrays as values and returns a QWidget which
            contains a QTableWidget with that data.
            """
            # self.view_table = Table(value=table)

            # widget = QWidget()
            # widget.setWindowTitle("Prediction")
            # widget.setLayout(QGridLayout())
            # widget.layout().addWidget(self.view_table.native)

            # return widget,self.view_table
            widget = QWidget()
            widget.setWindowTitle("Prediction")
            widget.setLayout(QVBoxLayout())
            self.v_table = TableWidget(table,self.LABEL_CATEGORY)
            widget.setFixedWidth(500)
            widget.setFixedHeight(200)
            widget.layout().addWidget(self.v_table)
            return widget,self.v_table
        
        images_folder = os.listdir(self.temp_output_dir.name)

        old_subfolder_image = []
                
        names = []
        dico_name = {}
        for image_name in images_folder:
            image_name_without_extension, _ = os.path.splitext(image_name)
            dico_name[image_name_without_extension]=image_name
            names.append(image_name_without_extension)

        def open_name(item):

            name = item.text()
            old_subfolder_image.append(dico_name[name])
            print(old_subfolder_image)
            
            image_name_without_extension, extension_format = os.path.splitext(dico_name[name])
            
            # fname = f'{self.temp_output_dir.name}\{dico_name[name]}'
            fname = os.path.join(self.temp_output_dir.name,dico_name[name])
            print(fname)
            print('Loading', name, '...')

            layer_list = self.napari_current_viewer.layers
            
            if len(old_subfolder_image)>1:
                nom_layer = layer_list[0].name
                # REMOVE
                path_to_remove_image = os.path.join(self.temp_output_dir.name,old_subfolder_image[-2])
                # supprime l'image rgb
                print(path_to_remove_image)
                data_rgb = imread(os.path.join(path_to_remove_image))
                
                os.remove(f'{path_to_remove_image}')

                image_name_without_extension_1, _ = os.path.splitext(old_subfolder_image[-2])

                dico_name[image_name_without_extension_1]=nom_layer+extension_format
                # print('>',f'{self.temp_output_dir.name}\{nom_layer}{extension_format}')
                # imsave(f'{self.temp_output_dir.name}\{nom_layer}{extension_format}', data_rgb) 
                print('>',os.path.join(self.temp_output_dir.name,nom_layer+extension_format))
                imsave(os.path.join(self.temp_output_dir.name,nom_layer+extension_format), data_rgb)   
                    
            self.napari_current_viewer.layers.select_all()
            self.napari_current_viewer.layers.remove_selected()  
            data_segment0 = imread(fname) 
            self.napari_current_viewer.add_image(data_segment0,name=f'{image_name_without_extension}')

            print('... done.')
        
        widget = QWidget()
        
        list_widget = QListWidget()
        for n in names:
            list_widget.addItem(n)    
        list_widget.currentItemChanged.connect(open_name)
        self.napari_current_viewer.window.add_dock_widget([list_widget], area='right',name="Images")
        list_widget.setCurrentRow(0)

        dock_widget,self.v_table = table_to_widget(self.dico_output_prediction,self.LABEL_CATEGORY)
        self.napari_current_viewer.window.add_dock_widget(dock_widget, area='right')

        return self.v_table,self.dico_output_prediction

class Run_interface_detection:
    def __init__(self,x,y_list,current_viewer,output_dir):
        self.idx = x
        self.to_darknet = y_list[0]
        self.to_obj_data = y_list[1]
        self.to_architecture = y_list[2]
        self.to_weight = y_list[3]
        self.to_folder_image_txt = y_list[4] 
       

        self.napari_current_viewer = current_viewer
        self.temp_output_dir = output_dir
        self.to_folder_prediction_json = None 
        self.color_class = [
        'brown',
        'burlywood',
        'cadetblue',
        'chartreuse',
        'chocolate',
        'coral',
        'cornflowerblue',
        'crimson',
        'cyan',
        'darkblue',
        'darkcyan',
        'darkgoldenrod',
        'darkgreen',
        'darkmagenta',
        'darkolivegreen',
        'darkorange',
        'darkorchid',
        'darkred',
        'darksalmon',
        'darkslateblue',
        'darkslategray',
        'darkslategrey',
        'darkturquoise',
        'darkviolet',
        'deeppink',
        'deepskyblue',
        'dimgray',
        'dimgrey',
        'dodgerblue',
        'firebrick',
        'forestgreen',
        'fuchsia',
        'gold',
        'goldenrod',
        'gray',
        'green',
        'greenyellow',
        'grey',
        'hotpink',
        'indianred',
        'indigo',
        'lawngreen',
        'lightblue',
        'lightcoral',
        'lightgray',
        'lightgreen',
        'lightpink',
        'lightsalmon',
        'lightseagreen',
        'lightskyblue',
        'lightslategray',
        'lightslategrey',
        'lightsteelblue',
        'lime',
        'limegreen',
        'magenta',
        'maroon',
        'mediumaquamarine',
        'mediumblue',
        'mediumorchid',
        'mediumpurple',
        'mediumseagreen',
        'mediumslateblue',
        'mediumspringgreen',
        'mediumturquoise',
        'mediumvioletred',
        'midnightblue',
        'navy',
        'olive',
        'orange',
        'orangered',
        'orchid',
        'palevioletred',
        'pink',
        'plum',
        'powderblue',
        'purple',
        'red',
        'rosybrown',
        'royalblue',
        'saddlebrown',
        'salmon',
        'sandybrown',
        'seagreen',
        'sienna',
        'skyblue',
        'slateblue',
        'springgreen',
        'steelblue',
        'tan',
        'teal',
        'thistle',
        'tomato',
        'turquoise',
        'violet',
        'wheat',
        'yellow',
        'yellowgreen']
        
        
    def run_model(self):
        dico = {1:'Image Segmentation',2:'Object Classification',3:'Image Classification',4:'Detection'}        
        os.chdir(self.to_darknet)        
        try:
            if sys.platform in ["linux2","linux"]:
                subprocess.Popen(["./darknet"], stdout = subprocess.PIPE) 
            elif sys.platform=="win32":
                subprocess.Popen(["darknet.exe"], stdout = subprocess.PIPE)
            else:
                print('IMPOSSIBLE TO RUN darknet in ',sys.platform)
        except:
            print("Darknet NOT INSTALLED")
            return (dico[self.idx],'')
        else:
            print("Darknet already INSTALLED")
            return (dico[self.idx],'Run darknet')
        
    def run_darknet(self,darknet_version):

        head,_ = os.path.split(self.to_folder_image_txt)
        self.to_folder_prediction_json = os.path.join(head,"Prediction.json")
        if sys.platform in ["linux2","linux"]:
            cmdd = './darknet detector test '+self.to_obj_data+' '+self.to_architecture+' '+self.to_weight+'  -ext_output -dont_show -out '+self.to_folder_prediction_json+' < '+self.to_folder_image_txt
        elif sys.platform=="win32":
            cmdd = 'darknet.exe detector test '+self.to_obj_data+' '+self.to_architecture+' '+self.to_weight+'  -ext_output -dont_show -out '+self.to_folder_prediction_json+' < '+self.to_folder_image_txt
        else:
            cmdd = 'exit()'
            print('[BREAK] exit run_darknet() because ',sys.platform)
        os.system(cmdd)
        
    def bbx_vis(self):
        
        file_test = open(self.to_folder_image_txt)
        names = []
        self.dico_name_extension = {}
        for ix in list(file_test.readlines()):
            head,tail = os.path.split(ix.rstrip())
            self.dico_name_extension[tail]=head
            names.append(os.path.basename(ix.rstrip()))
        file_test.close()
        
        Bounding_boxes_doc= pd.read_json(self.to_folder_prediction_json)
        obj = Bounding_boxes_doc["objects"].apply(pd.DataFrame)
        file = Bounding_boxes_doc["filename"]

        file_obj_data = open(self.to_obj_data)
        for ix in list(file_obj_data.readlines()):
            une_liste = ix.split('=')
            if une_liste[0]=='names':
                chemin_classe_file = une_liste[1].rstrip()
                break
        file_obj_data.close()
        
        file1 = open(chemin_classe_file)
        names_class = [ line.rstrip() for line in list(file1.readlines())]
        file1.close()

        namess=[os.path.basename(idx) for idx in file]

        self.classe_dico_idx = {key:value for key,value in zip(names_class,np.arange(len(names_class)))}

        self.dico = {}
        for ix in range(len(obj)):            
            self.dico[namess[ix]]=obj[ix]
            
        dico_path = {}
        for idx,path_im in zip(namess,file):
            dico_path[idx]=path_im

        def get_correct_coords(matrice_selected):
            tx1 = matrice_selected[0][1]
            tx2 = matrice_selected[2][1]
            if tx1 > tx2:
                x1 = tx2
                x2 = tx1
            if tx1 < tx2:
                x1 = tx1
                x2 = tx2
            ty1 = matrice_selected[0][0]
            ty2 = matrice_selected[2][0]
            if ty1 > ty2:
                y1 = ty2
                y2 = ty1
            if ty1 < ty2:
                y1 = ty1
                y2 = ty2
            return x1,x2,y1,y2

        def get_relative_coordinates(liste_de_x_y,width,height):
            x1=liste_de_x_y[0]
            x2=liste_de_x_y[1]
            y1=liste_de_x_y[2]
            y2=liste_de_x_y[3]

            h = y2-y1
            c_y = y1+h/2-1
            
            w = x2-x1    
            c_x = x1+w/2-1
            
            c_x,c_y,w,h=c_x/width,c_y/height,w/width,h/height
            
            return c_x,c_y,w,h

        def func_to_update_dico_(doc_nom_image,liste_des_coords,liste_des_classes,size_of_image):
            height_img,width_img,_ = size_of_image
            dico_idi_coords_conf = {}
            idi_coords_cx = doc_nom_image['center_x'].values.tolist()
            idi_coords_cy = doc_nom_image['center_y'].values.tolist()
            idi_coords_w = doc_nom_image['width'].values.tolist()
            idi_coords_h = doc_nom_image['height'].values.tolist()
            idi_coords_conf = doc_nom_image['confidence'].values.tolist()
            for idcx,idcy,idw,idh,idconf in zip(idi_coords_cx,idi_coords_cy,idi_coords_w,idi_coords_h,idi_coords_conf):
                # dico_idi_coords_conf[f'{idcx,idcy,idw,idh}']=idconf
                dico_idi_coords_conf['('+str(np.round(idcx,2))+','+str(np.round(idcy,2))+','+str(np.round(idw,2))+','+str(np.round(idh,2))+')']=idconf

            objects_update = []

            x_y_liste = [get_correct_coords(matrice_selected) for matrice_selected in liste_des_coords] #x1,x2,y1,y2
            Class_id_lst = [self.classe_dico_idx[xi] for xi in liste_des_classes]

            for idi in range(len(x_y_liste)):
                cx,cy,w,h = get_relative_coordinates(x_y_liste[idi],width_img,height_img)
                var_tps = '('+str(np.round(cx,2))+','+str(np.round(cy,2))+','+str(np.round(w,2))+','+str(np.round(h,2))+')'
                if var_tps in list(dico_idi_coords_conf.keys()):
                    conf_idi = dico_idi_coords_conf[var_tps]
                else:
                    conf_idi = 1
                dico_relatives_coord_idi = {'center_x': cx,
                'center_y': cy,
                'width': w,
                'height': h}
                label_idi = liste_des_classes[idi]
                label_id_idi = Class_id_lst[idi]
                objects_update.append({'class_id':label_id_idi,'name':label_idi,'relative_coordinates':dico_relatives_coord_idi,'confidence':conf_idi})
            dico_update = pd.DataFrame(objects_update)
            return dico_update

        def open_name(item):        
            
            name = item.text()
            print(f"===============NEW IMAGE : {name}===============")
            self.napari_current_viewer.layers.select_all()
            self.napari_current_viewer.layers.remove_selected()

            img = imread(os.path.join(self.dico_name_extension[name],name))

            layer = self.napari_current_viewer.add_image(img,name=f'{os.path.splitext(name)[0]}')  

            def dico_image(nom_image,dico_nom_image):
                print(nom_image)
                dico = {}
                df = dico_nom_image[nom_image]

                center_x = []
                center_y = []
                width = []
                height = []
                if df.empty:
                    U1 = []
                    U2 = []
                    U3 = {"center_x":None, "center_y":None, "width":None, "height":None}
                    U4 = []
                else:
                    U1 = list(df['class_id'])
                    U2 = list(df['name'])
                    U3 = dict(df['relative_coordinates'])
                    U4 = list(df['confidence'])

                    for cle in U3.keys():
                        dico_cle = U3[cle]
                        center_x.append(dico_cle['center_x'])
                        center_y.append(dico_cle['center_y'])
                        width.append(dico_cle['width'])
                        height.append(dico_cle['height'])
                dico = {"class_id":U1,"name":U2,"confidence":U4,"center_x":center_x,"center_y":center_y,"width":width,"height":height}
                dfp = pd.DataFrame(dico)
                return dfp

            nom_image = name
            dico_detail = dico_image(nom_image,self.dico)
            height,width = img.shape[:2]
            dt_max = len(dico_detail)
            
            bbox_rect = []
            dico_bbx_class = []
            for i in range(dt_max):
                A = list(dico_detail.iloc[i])
                nom=A[1]
                confidence=A[2]
                x=A[3]
                y=A[4]
                w=A[5]
                h=A[6]

                x *= width
                y *= height
                w *= width
                h *= height

                x1 = int(x - w / 2 + 1)
                x2 = int(x1 + w)
                y1 = int(y - h / 2 + 1)
                y2 = int(y1 + h)       
                
                dico_bbx_class.append(nom)
                bbox_rect.append(np.array([[y1, x1], [y2, x1], [y2, x2], [y1, x2]]))
            
            properties = {
                'label': dico_bbx_class,
            }

            text_parameters = {
                'string': '{label}',
                'size': 12,
                'color': 'red',
                'anchor': 'upper_left',
                'translation': [-3, 0]
            }

            color_list_from_dico_bbx_class = []
            for name_ids in dico_bbx_class:
                idx = names_class.index(name_ids)
                color_list_from_dico_bbx_class.append(self.color_class[idx])

            shapes_layer = self.napari_current_viewer.add_shapes(
                bbox_rect,
                face_color='transparent',
                edge_color=color_list_from_dico_bbx_class, edge_width=5,
                properties=properties,
                text=text_parameters,
                name='bounding box',
            )
            
            print("original number of bbx displayed",len(shapes_layer.data))  
            
            current_layer_bbx = self.napari_current_viewer.layers['bounding box']
            
            def open_name_classe(item):
                idx = names_class.index(item.text())
                
                current_layer_bbx.mode = 'add_rectangle'
                current_layer_bbx.current_edge_color = self.color_class[idx]
                current_class_displayed=None
                
                
                @current_layer_bbx.mouse_drag_callbacks.append
                def profile_lines_drag(layer,event):           
                    
                    add_new_class = list(current_layer_bbx.properties['label'])
                    add_new_class[-1]=item.text()
                    current_layer_bbx.properties = {
                    'label': add_new_class,
                    }
                    
                    # print("number of bbx displayed:",len(current_layer_bbx.data))
                    # print("number of class displayed",len(add_new_class))
                    # print("last coordinate displayed:",napari_viewer.layers['bounding box'].data[-1])       
                    self.DICO_DETAIL_list_displayed.append(dico_detail)
                    self.CLASS_list_displayed.append(current_layer_bbx)
                    self.NOM_IMAGE_list_displayed.append(nom_image)
                self.CLASS_list_displayed.append(current_layer_bbx)
                self.DICO_DETAIL_list_displayed.append(dico_detail)
                self.NOM_IMAGE_list_displayed.append(nom_image)
            
            self.CLASS_list_displayed.append(current_layer_bbx)
            self.SIZE_list_displayed.append(img.shape)
            self.DICO_DETAIL_list_displayed.append(dico_detail)
            self.NOM_IMAGE_list_displayed.append(nom_image)
            
            list_class_select = QListWidget()
            for n,idx in zip(names_class,range(len(self.color_class))):
                i = QListWidgetItem(n)
                i.setBackground(QColor(self.color_class[idx]))
                list_class_select.addItem(i)
            

            list_class_select.currentItemChanged.connect(open_name_classe)

            if len(display_bbx_list)==0:
                dock_widget_display = self.napari_current_viewer.window.add_dock_widget(list_class_select, area='right',name="Class")
                display_bbx_list.append(dock_widget_display)
            else:
                # Enregistrement dans la liste CLASS_list_saved du dernier Shape_layer affiché [c'est le shape layer avec ou non modif]
                # Cet enregistrement arrive lorsque l'utilisateur change d'image
                CLASS_list_saved.append(self.CLASS_list_displayed[-2]) 
                SIZE_list_saved.append(self.SIZE_list_displayed[-2]) 
                DICO_DETAIL_list_saved.append(self.DICO_DETAIL_list_displayed[-2])
                NOM_IMAGE_list_saved.append(self.NOM_IMAGE_list_displayed[-2])

                liste_des_classes = CLASS_list_saved[-1].properties['label']
                liste_des_coords = CLASS_list_saved[-1].data
                taille_de_limage = SIZE_list_saved[-1]
                doc_nom_image = DICO_DETAIL_list_saved[-1]
                last_nom_image = NOM_IMAGE_list_saved[-1]
                
                print('last_nom_image',last_nom_image)
                
                pandas_nom_image_update = func_to_update_dico_(doc_nom_image,liste_des_coords,liste_des_classes,taille_de_limage)    
                self.dico[last_nom_image] = pandas_nom_image_update
                
                dock_widget_display = self.napari_current_viewer.window.add_dock_widget(list_class_select, area='right',name="Class")
                display_bbx_list.append(dock_widget_display)
                self.napari_current_viewer.window.remove_dock_widget(display_bbx_list[-2])
            dock_widget_display

        NOM_IMAGE_list_saved = []
        SIZE_list_saved = []
        CLASS_list_saved = []
        DICO_DETAIL_list_saved = []

        self.NOM_IMAGE_list_displayed = []
        self.SIZE_list_displayed = []
        self.CLASS_list_displayed = []  
        self.DICO_DETAIL_list_displayed = []

        display_bbx_list = []
        list_widget = QListWidget()
        for n in names:
            list_widget.addItem(n)


        list_widget.currentItemChanged.connect(open_name)
        self.napari_current_viewer.window.add_dock_widget([list_widget], area='right',name="Images")
        list_widget.setCurrentRow(0)
        
        return self.NOM_IMAGE_list_displayed,self.SIZE_list_displayed,self.CLASS_list_displayed,self.DICO_DETAIL_list_displayed,self.classe_dico_idx,self.dico,self.dico_name_extension
            
class Run_interface_segmentation:
    def __init__(self,x,y_list,current_viewer,output_dir):
        self.idx = x
        self.image_zip = y_list[0]
        self.model = y_list[1]
        self.classe_file = y_list[2]
        self.napari_current_viewer = current_viewer
        self.temp_output_dir = output_dir
        self.nbr_classe = None
        self.label_name_current = None
        
    def run_model(self):
        dico = {1:'Image Segmentation',2:'Object Classification',3:'Image Classification',4:'Detection'}
        if self.model.endswith(".ilp"):
            root_pc = str(pathlib.Path.home()).split("\\")[0]+"\\Program Files"
            check_version = [ix for ix in os.listdir(root_pc) if ix.find('ilastik')!=-1]
            if len(check_version)==0:
                show_info('ILASTIK NOT INSTALLED')
                return (dico[self.idx],'') #NO ILASTIK INSTALLED
            else:
                ilastik_version = check_version[0]
                show_info('ILASTIK VERSION:'+ilastik_version)
                return (dico[self.idx],ilastik_version)
        elif self.model.endswith(".h5"):
            return (dico[self.idx],'Run tensorflow')
    
    def run_tensorflow_segmentation(self,tensorflow_version):
        import tensorflow as tf
        from tensorflow.keras import backend as K
        from skimage.transform import resize
        
        from skimage import img_as_bool    

        def dice_coefficient(y_true, y_pred):
            eps = 1e-6
            y_true_f = K.flatten(y_true)
            y_pred_f = K.flatten(y_pred)
            intersection = K.sum(y_true_f * y_pred_f)
            return (2. * intersection) / (K.sum(y_true_f * y_true_f) + K.sum(y_pred_f * y_pred_f) + eps) #eps pour éviter la division par 0 

        def get_output_size_image(new_model):
            n = len(new_model.layers)-1
            for i in range(n,0,-1):
                A = list(new_model.layers[i].output.shape)
                if len(A) ==4:
                    _, IMG_HEIGHT, IMG_WIDTH,IMG_CHANNELS = A
                    return IMG_HEIGHT, IMG_WIDTH # 4 argument pour une image

        model_New = tf.keras.models.load_model(self.model,custom_objects={'dice_coefficient': dice_coefficient})
        _, IMG_HEIGHT, IMG_WIDTH,IMG_CHANNELS = list(model_New.input.shape)
        h_p,w_p = get_output_size_image(model_New)
        self.nbr_classe = list(model_New.output_shape)[-1]

        with ZipFile(self.image_zip,'r') as zipObject:
            listOfFileNames = zipObject.namelist()
            if len(listOfFileNames)==1:
                zipObject.extract(listOfFileNames[0],path=self.temp_output_dir.name)
                image_path = os.path.join(self.temp_output_dir.name,listOfFileNames[0])
                
                matrix_img = imread(image_path)
                or_h,or_w,_  = matrix_img.shape
                
                X_ensemble = np.zeros((1, IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS), dtype=np.uint8)
                img = resize(matrix_img, (IMG_HEIGHT, IMG_WIDTH), mode='constant', preserve_range=True)
                X_ensemble[0] = img

                preds_test = model_New.predict(X_ensemble, verbose=1)

                A = []
                pr_shape = preds_test.shape
                pr_shape_int = len(pr_shape)
                
                if pr_shape_int==3:
                    _,height_p,width_p = preds_test.shape
                    for i in range(height_p):
                        allonger = list(preds_test[0,i,:].flatten())
                        ids = allonger.index(np.max(allonger))
                        A.append(ids)

                    seg_img = np.zeros((h_p,w_p))
                    k=0
                    for i in range(h_p):
                        for j in range(w_p):
                            seg_img[i][j]=A[k]
                            k+=1

                elif pr_shape_int==4: #une_classe
                    preds_test = (preds_test > 0.5).astype(np.uint8)
                    seg_img = preds_test[0,:,:,0]
                    self.nbr_classe = 2


                final_output = resize(seg_img, (or_h, or_w), mode='constant', preserve_range=True)

                head,_ = os.path.splitext(image_path)

                image_data_path = head+'_mask.png'
                imsave(image_data_path,final_output.astype(np.uint8))

            else:

                pbar = progress(range(len(listOfFileNames)))
                for i in pbar:
                    image_name = listOfFileNames[i]
                    image_folder = self.temp_output_dir.name+'\\'+image_name[:-4]
                    os.mkdir(image_folder)
                    zipObject.extract(listOfFileNames[i],path=image_folder)
                    image_path = os.path.join(image_folder,listOfFileNames[i])

                    matrix_img = imread(image_path)
                    or_h,or_w,_  = matrix_img.shape
                    
                    X_ensemble = np.zeros((1, IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS), dtype=np.uint8)
                    img = resize(matrix_img, (IMG_HEIGHT, IMG_WIDTH), mode='constant', preserve_range=True)
                    X_ensemble[0] = img

                    preds_test = model_New.predict(X_ensemble, verbose=1)

                    A = []
                    pr_shape = preds_test.shape
                    pr_shape_int = len(pr_shape)
                    
                    if pr_shape_int==3:
                        _,height_p,width_p = preds_test.shape
                        for i in range(height_p):
                            allonger = list(preds_test[0,i,:].flatten())
                            ids = allonger.index(np.max(allonger))
                            A.append(ids)

                        seg_img = np.zeros((h_p,w_p))
                        k=0
                        for i in range(h_p):
                            for j in range(w_p):
                                seg_img[i][j]=A[k]
                                k+=1

                    elif pr_shape_int==4: #une_classe
                        preds_test = (preds_test > 0.5).astype(np.uint8)
                        seg_img = preds_test[0,:,:,0]
                        self.nbr_classe = 2


                    final_output = resize(seg_img, (or_h, or_w), mode='constant', preserve_range=True)
                    image_data_path = os.path.join(image_folder,image_name[:-4])+'_mask.png'
                    imsave(image_data_path,final_output.astype(np.uint8))
                    pbar.set_description("sds")
####
####
####
####
####
####
####
    
    def run_ilastik(self,ilastik_version):
        
        with ZipFile(self.image_zip,'r') as zipObject:
            
            listOfFileNames = zipObject.namelist()
            print(listOfFileNames)
            # lazy_arrays = []
            # lazy_masks = []
            
            if len(listOfFileNames)==1:
                zipObject.extract(listOfFileNames[0],path=self.temp_output_dir.name)
                image_path = os.path.join(self.temp_output_dir.name,listOfFileNames[0])
                projet_path = '--project='+self.model
                path_to_run = os.path.join("C:/Program Files",os.path.join(ilastik_version,"ilastik.exe"))
                recevoir = '--output_filename_format="'+os.path.join(self.temp_output_dir.name,listOfFileNames[0][:-4])+'_mask.jpg"'
                subprocess.run([path_to_run,
                                    '--headless',
                                    projet_path,
                                    '--export_source=Simple Segmentation',
                                    '--raw_data="'+image_path+'"',
                                    recevoir])
                print("IMAGE: 1")
            else:
                for i in progress(range(len(listOfFileNames))):
                    image_name = listOfFileNames[i]
                    
                    image_folder = self.temp_output_dir.name+'\\'+image_name[:-4]
                    os.mkdir(image_folder)
                    zipObject.extract(listOfFileNames[i],path=image_folder)
                    image_path = os.path.join(image_folder,listOfFileNames[i])
                                        
                    projet_path = '--project='+self.model
                    path_to_run = os.path.join("C:/Program Files",os.path.join(ilastik_version,"ilastik.exe"))
                    recevoir = '--output_filename_format="'+os.path.join(image_folder,image_name[:-4])+'_mask.jpg"'
                    subprocess.run([path_to_run,
                                    '--headless',
                                    projet_path,
                                    '--export_source=Simple Segmentation',
                                    '--raw_data="'+image_path+'"',
                                    recevoir])
                print("IMAGE:",i+1)
                    
    def segmentation_vis(self):

        path_to_txt = self.classe_file
        if len(path_to_txt)==0:
            print("NO CLASS LABEL REFERENCED")
            idn_classe = [str(i) for i in range(self.nbr_classe)]
        else:
            with open(path_to_txt) as file:
                lines = file.readlines()
            file.close()
            idn_classe = [x.split('\n')[0] for x in lines]
            if len(idn_classe)==self.nbr_classe:
                print("CLASS LABEL REFERENCED")
                pass
            else:
                print("TOTAL CLASS LABEL NOT EQUAL TO MODEL")
                idn_classe = [str(i) for i in range(self.nbr_classe)]


        
        image_folder = os.listdir(self.temp_output_dir.name)

        old_subfolder_image = []
        
        if os.path.isfile(os.path.join(self.temp_output_dir.name,image_folder[0])): #si c'est un fichier
            print(image_folder)
            names = [file_image[:-4] for file_image in image_folder if file_image[:-4].find('mask')==-1]
            print(names)
        
            def open_name(item):
                
                name = item.text()

                old_subfolder_image.append(name)
                
                print('Loading', name, '...')

                self.napari_current_viewer.layers.select_all()
                self.napari_current_viewer.layers.remove_selected()    
                fname = f'{self.temp_output_dir.name}'

                data_temp_subfolder = os.listdir(fname)

                for fname_i in data_temp_subfolder:
                    if fname_i.find('mask')!=-1:
                        # data_label_original = imread(f'{fname}\{fname_i}')                        
                        data_label_original = imread(os.path.join(fname,fname_i))
                        data_label = np.array(data_label_original)
                        self.napari_current_viewer.add_labels(data_label,name=f'{fname_i[:-4]}')
                        self.label_name_current = f'{fname_i[:-4]}'                                  
                    else:
                        # self.napari_current_viewer.add_image(imread(f'{fname}\{fname_i}'),name=f'{fname_i[:-4]}')
                        self.napari_current_viewer.add_image(imread(os.path.join(fname,fname_i)),name=f'{fname_i[:-4]}')

                current_layer_bbx = self.napari_current_viewer.layers[self.label_name_current]

                def open_name_classe(item):
                    idx = idn_classe.index(item.text())
                    current_layer_bbx.mode = "PAINT"
                    current_layer_bbx.selected_label = int(idx)
                    current_class_displayed=None

                list_class_select = QListWidget()
                for n,idx in zip(idn_classe,range(self.nbr_classe)):
                    i = QListWidgetItem(n)
                    col_temp = current_layer_bbx.get_color(idx)
                    if idx==0:
                        pass
                    else:
                        i.setBackground(QColor(int(col_temp[0]*255),int(col_temp[1]*255),int(col_temp[2]*255),int(col_temp[3]*255)))
                    list_class_select.addItem(i)
                        
                list_class_select.currentItemChanged.connect(open_name_classe)
                self.napari_current_viewer.window.add_dock_widget(list_class_select, area='right',name="Class")

                print('... done.')
        
        
        else: #sinon
            names = []
            for subfolder in image_folder:
                if len(os.listdir(os.path.join(self.temp_output_dir.name,subfolder)))!=0:
                    names.append(subfolder)

            def open_name(item):

                name = item.text()
                old_subfolder_image.append(name)
                print(old_subfolder_image)

                # fname = f'{self.temp_output_dir.name}\{name}'
                fname = os.path.join(self.temp_output_dir.name,name)
                print('Loading', name, '...')
                layer_list = self.napari_current_viewer.layers
                if layer_list!=[] and len(old_subfolder_image)>1:
                    sample0 = layer_list[0]
                    sample1 = layer_list[1]

                    n_shape_image = len(sample0.data.shape)

                    if n_shape_image == 3:
                        nom_layer_rgb = sample0.name                        
                        nom_layer = sample1.name
                        data_label = sample1.data
                    else:
                        nom_layer_rgb = sample1.name                        
                        nom_layer = sample0.name
                        data_label = sample0.data

                    # REMOVE
                    path_to_remove_subfolder = os.path.join(self.temp_output_dir.name,old_subfolder_image[-2])
                    element_remove = os.listdir(path_to_remove_subfolder)
                    # supprime limage segmenté
                    data_segment0 = imread(os.path.join(path_to_remove_subfolder,element_remove[0]))
                    
                    n_shape_image = len(data_segment0.shape)

                    if n_shape_image == 3:
                        # os.remove(f'{self.temp_output_dir.name}\{old_subfolder_image[-2]}\{element_remove[1]}')
                        os.remove(os.path.join(self.temp_output_dir.name,old_subfolder_image[-2],element_remove[1]))
                    else:
                        # os.remove(f'{self.temp_output_dir.name}\{old_subfolder_image[-2]}\{element_remove[0]}')
                        os.remove(os.path.join(self.temp_output_dir.name,old_subfolder_image[-2],element_remove[0]))
                    # imsave(f'{self.temp_output_dir.name}\{old_subfolder_image[-2]}\{nom_layer}.png', img_as_ubyte(data_label))
                    imsave(os.path.join(self.temp_output_dir.name,old_subfolder_image[-2],nom_layer+'.png'), img_as_ubyte(data_label))   
                    
                self.napari_current_viewer.layers.select_all()
                self.napari_current_viewer.layers.remove_selected()    
                data_temp_subfolder = os.listdir(fname)
                data_segment0 = imread(os.path.join(fname,data_temp_subfolder[0]))
                data_segment1 = imread(os.path.join(fname,data_temp_subfolder[1]))
                n0_class = len(list(dict(Counter(data_segment0.flatten())).keys()))
                n1_class = len(list(dict(Counter(data_segment1.flatten())).keys()))
                
                if n0_class > n1_class:
                    data_label = np.array(data_segment1)                    
                    self.napari_current_viewer.add_image(data_segment0,name=f'{data_temp_subfolder[0][:-4]}')
                    self.napari_current_viewer.add_labels(data_label,name=f'{data_temp_subfolder[1][:-4]}')
                    self.label_name_current = f'{data_temp_subfolder[1][:-4]}'
                else:
                    data_label = np.array(data_segment0)                    
                    self.napari_current_viewer.add_image(data_segment1,name=f'{data_temp_subfolder[1][:-4]}')
                    self.napari_current_viewer.add_labels(data_label,name=f'{data_temp_subfolder[0][:-4]}')
                    self.label_name_current = f'{data_temp_subfolder[0][:-4]}'

                ## color
                current_layer_bbx = self.napari_current_viewer.layers[self.label_name_current]

                if self.nbr_classe <= 255:

                    ######################################
                    ## FUNCTION FROM NAPARI
                    # import napari.layers.labels as lbl_get_color


                    def open_name_classe(item):
                        idx = idn_classe.index(item.text())
                        current_layer_bbx.mode = "PAINT"
                        current_layer_bbx.selected_label = int(idx)
                        current_class_displayed=None

                    list_class_select = QListWidget()
                    for n,idx in zip(idn_classe,range(self.nbr_classe)):
                        i = QListWidgetItem(n)
                        col_temp = current_layer_bbx.get_color(idx)
                        if idx==0:
                            pass
                        else:
                            i.setBackground(QColor(int(col_temp[0]*255),int(col_temp[1]*255),int(col_temp[2]*255),int(col_temp[3]*255)))
                        list_class_select.addItem(i)
                        
                    list_class_select.currentItemChanged.connect(open_name_classe)

                    if len(display_bbx_list)==0:
                        dock_widget_display = self.napari_current_viewer.window.add_dock_widget(list_class_select, area='right',name="Class")
                        display_bbx_list.append(dock_widget_display)
                    else:
                        # Enregistrement dans la liste CLASS_list_saved du dernier Shape_layer affiché [c'est le shape layer avec ou non modif]
                        # Cet enregistrement arrive lorsque l'utilisateur change d'image
                        dock_widget_display = self.napari_current_viewer.window.add_dock_widget(list_class_select, area='right',name="Class")
                        display_bbx_list.append(dock_widget_display)
                        self.napari_current_viewer.window.remove_dock_widget(display_bbx_list[-2])
                    dock_widget_display

                print('... done.')
        
        widget = QWidget()
        display_bbx_list = []
        
        list_widget = QListWidget()
        for n in names:
           list_widget.addItem(n)    
        list_widget.currentItemChanged.connect(open_name)
        self.napari_current_viewer.window.add_dock_widget([list_widget], area='right',name="Images")
        list_widget.setCurrentRow(0)

        return old_subfolder_image

class Run_save_segmentation:
    def __init__(self,current_viewer,output_dir,old_subfolder_image):
        self.napari_current_viewer = current_viewer
        self.temp_output_dir = output_dir
        self.path_to_temp_output_dir = output_dir.name
        self.old_subfolder_image = old_subfolder_image
        
    def get_label_path(self):
        list_layers = self.napari_current_viewer.layers
        # print("list_layers",list_layers)
        # print("self.old_subfolder_image",self.old_subfolder_image)

        data_sample0 = list_layers[0].data.shape

        if len(data_sample0)==3:
            current_name_layer_label = list_layers[1].name
            current_name_layer_rgb = list_layers[0].name
        else:
            current_name_layer_label = list_layers[0].name
            current_name_layer_rgb = list_layers[1].name            
        # print("current_name_layer_label",current_name_layer_label)
        # print("current_name_layer_rgb",current_name_layer_rgb)
            
        list_folder = os.listdir(self.path_to_temp_output_dir)
        # print("list_folder",list_folder)
        
        if os.path.isfile(os.path.join(self.path_to_temp_output_dir,list_folder[0])):
            current_subfolder = self.old_subfolder_image[-1]
            files_in_subfolder = os.listdir(os.path.join(self.path_to_temp_output_dir))
            data_temp = imread(os.path.join(self.path_to_temp_output_dir,files_in_subfolder[0]))
            if len(data_temp.shape)==3:
                path_current_layer = os.path.join(self.path_to_temp_output_dir,files_in_subfolder[1])
            else:
                path_current_layer = os.path.join(self.path_to_temp_output_dir,files_in_subfolder[0])
            return [path_current_layer,current_name_layer_label]

        else:
            current_subfolder = self.old_subfolder_image[-1]
            files_in_subfolder = os.listdir(os.path.join(self.path_to_temp_output_dir,current_subfolder))
            data_temp = imread(os.path.join(self.path_to_temp_output_dir,current_subfolder,files_in_subfolder[0]))
            if len(data_temp.shape)==3:
                path_current_layer = os.path.join(self.path_to_temp_output_dir,current_subfolder,files_in_subfolder[1])
            else:
                path_current_layer = os.path.join(self.path_to_temp_output_dir,current_subfolder,files_in_subfolder[0])
            # print("[path_current_layer,current_name_layer_label]",[path_current_layer,current_name_layer_label])
            return [path_current_layer,current_name_layer_label]

        
    def save_data_mask(self,path_mask,name_mask):
        data_label = self.napari_current_viewer.layers[name_mask].data
        os.remove(path_mask)


        list_temporaire,old_name = path_mask.split("\\")[:-1],path_mask.split("\\")[-1] #['path','to','subfolder'],image1.png
        image_format = old_name.split(".")[-1] # png jpg tiff ...
        new_name_label = name_mask+'.'+image_format # new_name_image.png

        path_to_subfolder = '\\'.join(list_temporaire)
        # print("path_to_subfolder",path_to_subfolder)
        # print("new_name_label",new_name_label)
        new_name_label_path = os.path.join(path_to_subfolder,new_name_label)
        # print("new_name_label_path",new_name_label_path)
        imsave(new_name_label_path, img_as_ubyte(data_label))
        
class Run_save_detection:
    def __init__(self,last_image,last_size,last_bbx,last_info_detail,classe_et_id,dico,dico_name_ext):
        self.lst_image = last_image
        self.lst_size = last_size
        self.lst_bbx = last_bbx
        self.lst_info_detail = last_info_detail
        self.cls_et_id = classe_et_id
        self.all_info = dico
        self.dc_name_ext = dico_name_ext
        
    def update_last_data(self):

        def get_correct_coords(matrice_selected):
            tx1 = matrice_selected[0][1]
            tx2 = matrice_selected[2][1]
            if tx1 > tx2:
                x1 = tx2
                x2 = tx1
            if tx1 < tx2:
                x1 = tx1
                x2 = tx2
            ty1 = matrice_selected[0][0]
            ty2 = matrice_selected[2][0]
            if ty1 > ty2:
                y1 = ty2
                y2 = ty1
            if ty1 < ty2:
                y1 = ty1
                y2 = ty2
            return x1,x2,y1,y2

        def get_relative_coordinates(liste_de_x_y,width,height):
            x1=liste_de_x_y[0]
            x2=liste_de_x_y[1]
            y1=liste_de_x_y[2]
            y2=liste_de_x_y[3]

            h = y2-y1
            c_y = y1+h/2-1
            
            w = x2-x1    
            c_x = x1+w/2-1
            
            c_x,c_y,w,h=c_x/width,c_y/height,w/width,h/height
            
            return c_x,c_y,w,h

        def func_to_update_dico_(doc_nom_image,liste_des_coords,liste_des_classes,size_of_image):
            height_img,width_img,_ = size_of_image
            dico_idi_coords_conf = {}
            idi_coords_cx = doc_nom_image['center_x'].values.tolist()
            idi_coords_cy = doc_nom_image['center_y'].values.tolist()
            idi_coords_w = doc_nom_image['width'].values.tolist()
            idi_coords_h = doc_nom_image['height'].values.tolist()
            idi_coords_conf = doc_nom_image['confidence'].values.tolist()
            for idcx,idcy,idw,idh,idconf in zip(idi_coords_cx,idi_coords_cy,idi_coords_w,idi_coords_h,idi_coords_conf):
                dico_idi_coords_conf['('+str(np.round(idcx,2))+','+str(np.round(idcy,2))+','+str(np.round(idw,2))+','+str(np.round(idh,2))+')']=idconf

            objects_update = []

            x_y_liste = [get_correct_coords(matrice_selected) for matrice_selected in liste_des_coords] #x1,x2,y1,y2
            Class_id_lst = [self.cls_et_id[xi] for xi in liste_des_classes]

            for idi in range(len(x_y_liste)):
                cx,cy,w,h = get_relative_coordinates(x_y_liste[idi],width_img,height_img)
                var_tps = '('+str(np.round(cx,2))+','+str(np.round(cy,2))+','+str(np.round(w,2))+','+str(np.round(h,2))+')'
                if var_tps in list(dico_idi_coords_conf.keys()):
                    conf_idi = dico_idi_coords_conf[var_tps]
                else:
                    conf_idi = 1
                dico_relatives_coord_idi = {'center_x': cx,
                'center_y': cy,
                'width': w,
                'height': h}
                label_idi = liste_des_classes[idi]
                label_id_idi = Class_id_lst[idi]
                objects_update.append({'class_id':label_id_idi,'name':label_idi,'relative_coordinates':dico_relatives_coord_idi,'confidence':conf_idi})
            dico_update = pd.DataFrame(objects_update)
            return dico_update
        
        last_nom_image_ = self.lst_image[-1]
        taille_de_limage = self.lst_size[-1]
        liste_des_classes = self.lst_bbx[-1].properties['label']
        liste_des_coords = self.lst_bbx[-1].data
        doc_nom_image = self.lst_info_detail[-1]
        
        pandas_nom_image_update = func_to_update_dico_(doc_nom_image,liste_des_coords,liste_des_classes,taille_de_limage)
        self.all_info[last_nom_image_]=pandas_nom_image_update
        
        ct=1
        FRAME_ID_LIST = []
        FILENAME = []
        OBJECT = []
        list_of_images_names = list(self.all_info.keys())
        for idd in list_of_images_names:
            FRAME_ID_LIST.append(ct)
            ct+=1
            FILENAME.append(os.path.join(self.dc_name_ext[idd],idd))
            OBJECT.append(self.all_info[idd])
            
        bbx_temp = {'frame_id':FRAME_ID_LIST,'filename':FILENAME,'objects':OBJECT}
        df = pd.DataFrame(bbx_temp)
        return df
        
        
class ManiniWidget(QWidget):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer
        self.ix = None
        self.iy = None
        self.old_subfolder_image = None
        self.view_table = None
        self.v_table = None
        self.dico_output_prediction = None
        
        self.NOM_IMAGE_list_displayed = None
        self.SIZE_list_displayed = None
        self.CLASS_list_displayed = None
        self.DICO_DETAIL_list_displayed = None
        self.classe_dico_idx = None
        self.dico = None
        self.dico_name_extension = None

        
        self.output_directory = tempfile.TemporaryDirectory()
                
        click1 = QPushButton("Image segmentation")
        click1.clicked.connect(self._on_click1)    
        click3 = QPushButton("Image classification")
        click3.clicked.connect(self._on_click3)        
        click4 = QPushButton("Object Detection")
        click4.clicked.connect(self._on_click4)        
        click_run = QPushButton("Run")
        click_run.clicked.connect(self._on_click_run)        
        click_save = QPushButton("Save")
        click_save.clicked.connect(self._on_click_save)
                
        self.setLayout(QGridLayout())       
    
        self.layout().addWidget(click1,1,0)
        self.layout().addWidget(click3,2,0)
        self.layout().addWidget(click4,3,0)
        
        self.layout().addWidget(click_run,4,0)
        self.layout().addWidget(click_save,4,1)
        
    def _on_click1(self):
        dialog = Image_segmentation(self)  
        dialog.exec_()        
        print("Image segmentation CLOSE")
        if dialog.result() == QDialog.Accepted:
            self._on_click_idx = 1
            self._on_click_list = [dialog.filename_edit_image.text(),dialog.filename_edit_model.text(),dialog.filename_edit_class_name.text()]
            
    def _on_click3(self):
        dialog = Image_classification(self)  
        dialog.exec_()
        print("Image classification CLOSE")
        if dialog.result() == QDialog.Accepted:
            self._on_click_idx = 3
            self._on_click_list = [dialog.filename_edit_image.text(),dialog.filename_edit_model.text(),dialog.filename_edit_class_name.text()]
            
    def _on_click4(self):
        dialog = Object_detection(self)  
        dialog.exec_()        
        print("Object detection CLOSE")
        if dialog.result() == QDialog.Accepted:
            # print(dialog.number.value())
            self._on_click_idx = 4
            self._on_click_list = [dialog.filename_edit_darknet.text(),
                                   dialog.filename_edit_obj_data.text(),
                                   dialog.filename_edit_architecture.text(),
                                   dialog.filename_edit_weight.text(),
                                   dialog.filename_edit_folder_image_txt.text()
                                   ]
            
    def _on_click_run(self):
        if self._on_click_idx==1:
            a = Run_interface_segmentation(self._on_click_idx,self._on_click_list,self.viewer,self.output_directory)
            val1,val2 = a.run_model() # {1:'Image Segmentation',2:'Object Classification',3:'Image Classification',4:'Detection'}
            
            t1_start = process_time() #time start      
            if val2 != 'Run tensorflow':
                a.run_ilastik(val2)
            else:  
                a.run_tensorflow_segmentation(val2)
            t1_stop = process_time() #time stop
            print("TOTAL PROCESSING TIME:",np.round(t1_stop-t1_start,2),"seconds")
            self.old_subfolder_image = a.segmentation_vis()
        elif self._on_click_idx==3:
            a = Run_interface_classification(self._on_click_idx,self._on_click_list,self.viewer,self.output_directory)
            val1,val2 = a.run_model()
            t1_start = process_time()
            a.run_tensorflow_classification(val2)
            t1_stop = process_time() #time stop
            print("TOTAL PROCESSING TIME:",np.round(t1_stop-t1_start,2),"seconds")
            self.v_table,self.dico_output_prediction = a.image_vis()
        elif self._on_click_idx==4:
            a = Run_interface_detection(self._on_click_idx,self._on_click_list,self.viewer,self.output_directory)
            val1,val2 = a.run_model()
            t1_start = process_time()
            a.run_darknet(val2)
            t1_stop = process_time()
            print("TOTAL PROCESSING TIME:",np.round(t1_stop-t1_start,2),"seconds")
            self.NOM_IMAGE_list_displayed,self.SIZE_list_displayed,self.CLASS_list_displayed,self.DICO_DETAIL_list_displayed,self.classe_dico_idx,self.dico,self.dico_name_extension = a.bbx_vis()           
            
    def _on_click_save(self):
        if self._on_click_idx==1:
            a = Run_save_segmentation(self.viewer,self.output_directory,self.old_subfolder_image)

            list_mask_info = a.get_label_path()
            a.save_data_mask(list_mask_info[0],list_mask_info[1])
            filename, _ = QFileDialog.getSaveFileName(self, "Save compressed file", str(pathlib.Path.home()),".")
            
            output_temp_file = os.listdir(self.output_directory.name)
            if len(output_temp_file)==2:
                for image_rgb_binary in output_temp_file:
                    path_to_img_rgb_bin = os.path.join(self.output_directory.name,image_rgb_binary)
                    image_matrix = imread(path_to_img_rgb_bin)
                    if len(image_matrix.shape)==2:
                        os.remove(path_to_img_rgb_bin)
                        gray = image_matrix*255
                        imsave(path_to_img_rgb_bin,gray)
            else:
                for subfolder in output_temp_file:
                    path_to_subfolder = os.path.join(self.output_directory.name,subfolder)
                    for image in os.listdir(path_to_subfolder):
                        image_matrix = imread(os.path.join(path_to_subfolder,image))
                        if len(image_matrix.shape)==2:
                            os.remove(os.path.join(path_to_subfolder,image))
                            or_h,or_w = image_matrix.shape
                            X = np.zeros((or_h, or_w, 3), dtype=np.uint8)
                            X[:,:,0]=image_matrix.astype(np.uint8)
                            X[:,:,1]=image_matrix.astype(np.uint8)
                            X[:,:,2]=image_matrix.astype(np.uint8)
                            gray = 0.2989 * X[:,:,0] + 0.5870 * X[:,:,1] + 0.1140 * X[:,:,2]
                            imsave(os.path.join(path_to_subfolder,image),gray)
            #Here, loop to convert image into grayscale
            
            if filename!='':
                print("EXPORT...")
                shutil.make_archive(filename,format="zip",root_dir=self.output_directory.name)
                print("...done")
                name_compressed_file = filename.split('/')[-1]
                print(f"{name_compressed_file} SAVED")
                show_info(f"{name_compressed_file} SAVED")
    
        elif self._on_click_idx==3:
            filename, _ = QFileDialog.getSaveFileName(self, "Save as csv", str(pathlib.Path.home()),"*.csv")
            if filename!='':
                
                rowCount = self.v_table.rowCount()
                columnCount = 3
                
                Nom_image = []
                Prediction = []
                for row in range(rowCount):
                    rowData = []
                    for column in range(columnCount):
                        widgetItem = self.v_table.item(row, column)
                        if widgetItem and widgetItem.text:
                            rowData.append(widgetItem.text())
                        else:
                            widget = self.v_table.cellWidget(row, column)
                            if isinstance(widget,QComboBox):
                                rowData.append(widget.currentText())
                    Nom_image.append(rowData[0])
                    Prediction.append(rowData[1])
                
                dico_data_displayed = {"nom":Nom_image,"prediction":Prediction}

                for cle in self.dico_output_prediction:
                    if cle not in ['nom','prediction','prob']:
                        dico_data_displayed[cle] = self.dico_output_prediction[cle]

                df = pd.DataFrame(dico_data_displayed)
                df.to_csv(filename)
                print(f"{filename} SAVED")
                show_info(f"{filename} SAVED")
                
        elif self._on_click_idx==4:
            a = Run_save_detection(self.NOM_IMAGE_list_displayed,self.SIZE_list_displayed,self.CLASS_list_displayed,self.DICO_DETAIL_list_displayed,self.classe_dico_idx,self.dico,self.dico_name_extension)
            df = a.update_last_data()
            
            filename, _ = QFileDialog.getSaveFileName(self, "Save as json", str(pathlib.Path.home()),"*.json")
            if filename!='':
                df.to_json(filename,orient="records")
                
                _,name_json = os.path.split(filename)
                print(f"{name_json} SAVED")
                show_info(f"{name_json} SAVED")