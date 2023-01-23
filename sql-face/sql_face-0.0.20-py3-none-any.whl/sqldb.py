# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_sqldb.ipynb.

# %% auto 0
__all__ = ['get_output_dir', 'SQLDataBase']

# %% ../nbs/01_sqldb.ipynb 4
from typing import List
from tqdm import tqdm

from sql_face.alchemy import * 
from sql_face.databases import get_image_db

# %% ../nbs/01_sqldb.ipynb 5
def get_output_dir(output_dir_name:str, # The name of the output directory.
                    save_in_drive:bool # Flag indicating whether the output directory should be saved in Google Drive or in the local file system.
                    )-> str: # The path to the output directory.
    "Obtains the path to the output directory"

    if save_in_drive:
        return os.path.join('../drive', 'MyDrive', output_dir_name)
    else:
        return output_dir_name 

# %% ../nbs/01_sqldb.ipynb 6
class SQLDataBase:
    "A SQL `class` to save face attributes"
    
    def __init__(self,
        db_name: str, # Dataset file name
        input_dir:str, # Folder with face datasets files
        output_dir_name:str, #Folder where the .db will be saved
        database_names: List[str], # List of database names to be processed
        detector_names: List[str], # List of detector names to be processed
        embedding_model_names: List[str], # List of embedding model names to be processed
        quality_model_names: List[str], # List of quality names to be processed
        save_in_drive: bool = False # Flag for working in local / Google Colab
        
    ): 
    
        self.db_name=db_name
        self.input_dir = input_dir        
        self.save_in_drive = save_in_drive
        self.output_dir = get_output_dir(output_dir_name, save_in_drive)
        self.session = get_session(output_dir_name, db_name) 
        self.databases = get_image_db(input_dir, database_names)
        self.detector_names = detector_names
        self.embedding_model_names = embedding_model_names
        self.quality_model_names = quality_model_names

    def create_tables(self, 
                    serfiq=None # object used to calculate the SERFIQ quality score.
                    ):
        "Creates the SQL tables and fills ONLY the Cropped Images."
        create_detectors(self.session, self.detector_names)
        create_embedding_models(self.session, self.embedding_model_names)
        create_quality_models(self.session, self.quality_model_names)

        for db in self.databases:
            db.create_images(self.session)
        # todo: optimize creating facevacs pairs.
        # self.create_facevacs_pairs()
        

        create_cropped_images(self.session, self.input_dir, serfiq) 
        create_face_images(self.session)
        create_quality_images(self.session)

    def update_tables(self, 
                    attributes_to_update:List[str], # The list of attributes to update in the tables.
                    force_update:bool=False, # Flag indicating whether to update the attributes even if they are already present in the tables.
                    serfiq = None # object used to calculate the SERFIQ quality score.
                    ):        
        update_images(self.session, self.input_dir, self.databases, attributes_to_update, force_update = force_update)
        update_cropped_images(self.session, self.input_dir, force_update = force_update, serfiq = serfiq)
        update_face_images(self.session, self.input_dir, force_update = force_update, serfiq= serfiq)
        update_quality_images(self.session, self.input_dir, serfiq = serfiq, force_update = force_update)
