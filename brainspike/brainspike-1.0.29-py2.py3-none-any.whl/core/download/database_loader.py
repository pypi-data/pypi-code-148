"""
database_loader.py

Human brain patch-clamp data loader 
for neurophysiology archives (i.e. Allen Brain, DANDI). 

"""

import pandas as pd 

from tqdm import tqdm

from ...download.allenbrain.allenbrain_obj import AllenBrain

###################################################################################################
###################################################################################################

def database_load(database = 'Allen Brain', specimen_id = None, file_name = None, manifest_file = None, stimulus_type = 'Long Square'): 
    """ return metadata dict from select databases
    
    
    Arugments
    ----------
    
    manifest_file: str
        path to manifest file (.json) for 
        data load. Default is "cell_types_manifest.json".
    
    Database info: 
    --------------
    
    'Allen Brain': https://celltypes.brain-map.org/
    'DANDI': https://dandiarchive.org/ 
    
    Code info:
    -----------
    
    https://github.com/AllenInstitute/AllenSDK/blob/master/allensdk/core/cell_types_cache.py 
    
    """
    
    databases = ['Allen Brain']
    # dandi_numbers = [] 
    
    if database in databases: 
        if database == 'Allen Brain': 

            allenbrain_objects = []
            if isinstance(specimen_id, int) or (specimen_id is None): 
                
                try: 
                    allenbrain_objects.append(AllenBrain(specimen_id = specimen_id,\
                                                        manifest_file = manifest_file,\
                                                        stimulus_type = stimulus_type,\
                                                        file_name = file_name))
                except Exception as e: 
                    print(f'error {e} | check parsed specimen id ...')
        
            elif isinstance(specimen_id, pd.DataFrame): 
                
                specimen_ids = specimen_id.id.values
                
                pbar = tqdm(total=100, desc = 'Processed files', colour="blue",\
                            position=0, leave=True, mininterval=0, ascii=True)
                
                for id in specimen_ids:
                    try:  
                        allenbrain_objects.append(AllenBrain(specimen_id = id,\
                                                            manifest_file = manifest_file,\
                                                            stimulus_type = stimulus_type,\
                                                            file_name = file_name))
                        pbar.update(100/len(specimen_ids))
                    except:  
                        print(f'skipped loading {id} ...') # trunucate issue :: skip load 
                        pass 
                else: 
                    pass 
                
                pbar.close()
                
                
            elif isinstance(specimen_id, list): 
                
                pbar = tqdm(total=100, desc = 'Processed files', colour="blue",\
                            position=0, leave=True, mininterval=0, ascii=True)
                
                for id in specimen_id:
                    if isinstance(id, int): 
                        try:
                            allenbrain_objects.append(AllenBrain(specimen_id = id,\
                                                                manifest_file = manifest_file,\
                                                                stimulus_type = stimulus_type,\
                                                                file_name = file_name))
                            pbar.update(100/len(specimen_id))
                        except:  
                            print(f'skipped loading {id} ...') # trunucate issue :: skip load 
                            pass 
                    else: 
                        raise TypeError(f'specimen id {id} is not an int type ...')
                else: 
                    pass 
                
                pbar.close()
        
            else: 
                raise TypeError('specimen id not found | check file name type ...')
            
            return allenbrain_objects
        
    else: 
        raise ValueError(f'select a database: {databases} ...')