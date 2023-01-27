import os
import gdown

def check_ckpt_exist(root):
    _root = os.path.expanduser(root)
    if not os.path.exists(_root):
            os.makedirs(_root)
            
    dir_path = os.path.join(_root, 'currface.pth')
    if os.path.exists(dir_path):
        return dir_path
    else:
        print('download_path :', dir_path)
        download_file(save_path = dir_path)
        return dir_path

def download_file(save_path, url_id = '15xnMCs8udpODpSGwbePuhJqDoDeE0SA7'):
    """
    https://github.com/wkentaro/gdown
    url default : https://drive.google.com/file/d/15xnMCs8udpODpSGwbePuhJqDoDeE0SA7
    save_path default : /.invz_package/id_extractor/ckpt/currface.pth
    
    https://drive.google.com/u/0/uc?id=15xnMCs8udpODpSGwbePuhJqDoDeE0SA7&export=download
    """
    url = 'https://drive.google.com/u/0/uc?id=' + url_id + '&export=download'
    gdown.download(url, save_path, quiet=False)
        