import os
from palantir.datasets import dataset as fds

# Download
def foundry_download(sourcefile_foundry):
    """Upload a Pandas dataframe to Foundry"""
    
    # Check that Token and Foundry-Host are set
    if 'PALANTIR_HOSTNAME' not in os.environ: 
        raise TypeError("Hostname for Foundry is not set as an environment variable...")
    elif os.environ.get('PALANTIR_HOSTNAME') == '':
        raise TypeError("Hostname for Foundry is not set as an environment variable...")

    if 'PALANTIR_TOKEN' not in os.environ:
        raise TypeError("Token for Hostname is not set as an environment variable...")
    elif os.environ.get('PALANTIR_TOKEN') == '':
        raise TypeError("Hostname for Foundry is not set as an environment variable...")
    
    # Download data from Foundry
    df = fds(sourcefile_foundry).read_pandas()

    return(df)

def foundry_upload(df, targetfile_foundry):
    """Download a dataset from Foundry and return a Pandas dataframe"""

    # Check that Token and Foundry-Host are set
    if 'PALANTIR_HOSTNAME' not in os.environ: 
        raise TypeError("Hostname for Foundry is not set as an environment variable...")
    elif os.environ.get('PALANTIR_HOSTNAME') == '':
        raise TypeError("Hostname for Foundry is not set as an environment variable...")

    if 'PALANTIR_TOKEN' not in os.environ:
        raise TypeError("Token for Hostname is not set as an environment variable...")
    elif os.environ.get('PALANTIR_TOKEN') == '':
        raise TypeError("Hostname for Foundry is not set as an environment variable...")
    
    # Write dataset to foundry
    fds(targetfile_foundry, create=True).write_pandas(df)
    
    # Check if dataset was uploaded correctly
    df_check = fds(targetfile_foundry).read_pandas()
    
    if not df.equals(df_check):
        raise TypeError("Dataframe may not have been uploaded correctly!")