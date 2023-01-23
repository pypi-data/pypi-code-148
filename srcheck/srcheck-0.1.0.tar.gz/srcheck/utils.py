import re
import cv2
import pathlib
import pytorch_msssim
import kornia
import numpy as np

# -----------------------------------------------------------------------------
# list files in a R-like manner
# -----------------------------------------------------------------------------
def list_files(path, pattern=None, full_names=False, recursive=False):
    """list.file (like in R) function"""
    files = list(list_file_gen(path, pattern, full_names, recursive))
    files_str = [str(file) for file in files]
    files_str.sort()
    return files_str


def list_file_gen(path, pattern=None, full_names=False, recursive=False):
    """List files like in R - generator"""
    path = pathlib.Path(path)
    for file in path.iterdir():
        if file.is_file():
            if pattern is None:
                if full_names:
                    yield file
                else:
                    yield file.name
            elif pattern is not None:
                regex_cond = re.compile(pattern=pattern)
                if regex_cond.search(str(file)):
                    if full_names:
                        yield file
                    else:
                        yield file.name
        elif recursive:
            yield from list_files(file, pattern, full_names, recursive)


def resize_3Dextended(data, size=(4, 1054, 1054)):
    tmpdata = np.zeros(size)
    for index, layer in enumerate(data):
        tmpdata[index] = cv2.resize(layer, dsize=(size[-2], size[-1]), interpolation=cv2.INTER_LINEAR)
    return tmpdata



def resize_4Dextended(data, size=(16, 4, 158, 158)):
    tmpdata = np.zeros(size)
    for index1, layer1 in enumerate(data):
        for index2, layer2 in enumerate(layer1):
            tmpdata[index1, index2] = cv2.resize(layer2, dsize=(size[-2], size[-1]), interpolation=cv2.INTER_NEAREST)
    return tmpdata


def standarization(img):
    return (img - np.min(img))/(np.max(img) - np.min(img))

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

def hallucination_map(lowimg, hrimg, methods=["nearest", "linear", "cubic", "lanczos4"]):
    clist = dict()
    
    if "nearest" in methods:
        clist["nearest"] = cv2.resize(lowimg, dsize=hrimg.shape, interpolation=cv2.INTER_NEAREST)
    if "linear" in methods:
        clist["linear"] = cv2.resize(lowimg, dsize=hrimg.shape, interpolation=cv2.INTER_LINEAR)
    if "cubic" in methods:
        clist["cubic"] = cv2.resize(lowimg, dsize=hrimg.shape, interpolation=cv2.INTER_CUBIC)
    if "lanczos4" in methods:
        clist["lanczos4"] = cv2.resize(lowimg, dsize=hrimg.shape, interpolation=cv2.INTER_LANCZOS4)
    hr_h = np.array(list(clist.values()))
    
    # get the most extreme value to
    min_diff = np.min(hrimg - hr_h, axis=0)
    max_diff = np.max(hrimg - hr_h, axis=0)
    mask_diff = np.abs(max_diff) > np.abs(min_diff)
    extreme_diff = max_diff*(mask_diff*1) + min_diff*(mask_diff == 0)
    
    return extreme_diff


def sr_comparison(hr_layer, hr_layer_p, lr_layer, thresholds=[0.01, 0.02, 0.05]):
    # MAE
    mae = np.mean(np.abs(hr_layer_p - hr_layer))
    
    # MAE balanced
    hallucination = hallucination_map(
        np.mean(lr_layer[0:3], axis=0),
        np.mean(hr_layer[0:3], axis=0), 
        methods=["nearest", "linear", "cubic", "lanczos4"]
    )
    masked_maes = list()
    for threshold in thresholds:
        mask = (np.abs(hallucination) > threshold)*1.
        mask[mask == 0] = np.nan
        # mask MAE
        masked_maes.append(np.nanmean(np.abs(hr_layer_p - hr_layer)*mask))
    mae_01, mae_02, mae_05  = masked_maes
        
    # PSNR
    psnr = 10*np.log10(1/mae)
    
    # MS-SSIM
    msssim = pytorch_msssim.ms_ssim(
        X=torch.Tensor(hr_layer_p[None]),
        Y=torch.Tensor(hr_layer[None]),
        data_range=1,
        win_size=5,
        size_average=False
    ).detach().numpy()
    
    # SSIM
    ssim = kornia.losses.ssim_loss(
        torch.Tensor(hr_layer_p[None]),
        torch.Tensor(hr_layer[None]),
        window_size=5,
        reduction="none"
    ).mean(
        dim=(-1, -2, -3)
    ).detach().numpy()
    
    return mae, mae_01, mae_02, mae_05, psnr, float(msssim), float(ssim)