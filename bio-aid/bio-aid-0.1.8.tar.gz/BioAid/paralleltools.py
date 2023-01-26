import os
import pandas as pd
from math import ceil

def split_df(df, slices_num, *savecsv_path_root):

    slice_size = ceil(len(df) / slices_num)
    slices_out = []
    for slice in range(slices_num):
        df_slice = df[slice*slice_size:(slice+1)*slice_size].copy()
        if savecsv_path_root:
            df_slice_name = f"{savecsv_path_root[0]}_{slice}.csv"
            df_slice.to_csv(df_slice_name, index=False)
            print(f'Slice {slice} saved to {df_slice_name}')
        
        slices_out.append(df_slice)
    
    print(f'Input df split into {slices_num} slices.')
    return slices_out

def join_slices(slices_num, slice_path_root, *savecsv_path):
    #this function combines the results from each slice into one df and saves it

    df = pd.DataFrame()
    for slice in range(slices_num):
        df_slice = pd.read_csv(f"{slice_path_root}_{slice}.csv")
        df = pd.concat([df, df_slice], ignore_index=True)
    
    if savecsv_path:
        df.to_csv(savecsv_path[0], index=False)
        print(f'Slices joined! Results saved to {savecsv_path[0]}')
    
    return df

def clean_up_slices(slices_num, slice_path_root):
    #this function deletes the slice files

    for slice in range(slices_num):
        os.remove(f"{slice_path_root}_{slice}.csv")

    print(f'Clean up Finished! Deleted slice files.')