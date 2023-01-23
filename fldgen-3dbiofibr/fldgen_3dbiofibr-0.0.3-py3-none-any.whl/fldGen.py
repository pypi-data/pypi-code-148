import cv2, numpy as np, matplotlib.pyplot as plt, warnings, os, pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
from scipy.signal import convolve2d
from scipy.ndimage import label 
from skimage.morphology import skeletonize
from datetime import datetime

# All for Filter A - Settings defaults
pixel_conversion_2x = 0.5940 #pixels/um
pixel_conversion_4x = 1.1764 #pixels/um
pixel_conversion_10x = 2.9473 #pixels/um
pixel_conversion_20x = 6.0014 #pixels/um
correcting_distance = 11.1 # this is the max distance between fiber ends which will be joined
dist_between_endpoints_of_one_fiber = 2
bins = np.linspace(20, 300, 15)
bins = np.append(bins, 10000)
num_pbars = 9

now = datetime.now()
date_and_time= now.strftime("%d-%m-%Y_%H:%M:%S")
warnings.filterwarnings("ignore")



def generate_img_files(image_folder_directory):
    img_files = []
    try:
        for path in os.listdir(image_folder_directory):
            if os.path.isfile(os.path.join(image_folder_directory, path)):
                fileName = os.path.join(image_folder_directory, path)
                img_files.append(fileName)
    except:
        img_files.append(image_folder_directory)
    return img_files

def dog(img, sigmaA=2.2, sigmaB=2, ksize=5): #1,0.85 works well for sigmas
    blurA = cv2.GaussianBlur(img,ksize=(ksize,ksize),sigmaX=sigmaA,sigmaY=sigmaA)
    blurB = cv2.GaussianBlur(img,ksize=(ksize,ksize),sigmaX=sigmaB,sigmaY=sigmaB)
    DoG = blurB-blurA
    return DoG

# Changes images form 0-255 to 0-
def normalize_255_1(img, pbar, num_pbars, img_files):
    for i1, e1 in enumerate(img):
        pbar.update(100/(len(img)*num_pbars*len(img_files)))
        for i2, e2 in enumerate(img[i1]):
            if e2 > 0:
                img[i1][i2] = 1 #this needs to be changed to 255 if you want to display a nice image 
            else:
                img[i1][i2] = 0
    return img

# Changing from True False to 1 0 
def normalize_TF_10(skeleton, img_files, num_pbars, pbar):
    normalized_data = []
    for rowIndex, row in enumerate(skeleton):
        pbar.update(100/(len(skeleton)*num_pbars*len(img_files)))
        rowData = []
        for colIndex, pixel in enumerate(skeleton[rowIndex]):
            if pixel == True:
                rowData.append(1)
            else:
                rowData.append(0)
        normalized_data.append(rowData)
    return np.array(normalized_data)

# Kills pixels with over 2 neighbours 
def remove_3_neighbor_pixels(skeleton,pbar,num_pbars,img_files):
    for indexRow, row in enumerate(skeleton[0:-1]):
        pbar.update(100/(len(skeleton)*num_pbars*len(img_files)))
        for indexCol, pixel in enumerate(skeleton[indexRow][0:-1]):
            if pixel == 1:
                if skeleton[indexRow,indexCol+1] + skeleton[indexRow,indexCol-1] \
                + skeleton[indexRow-1,indexCol] + skeleton[indexRow+1,indexCol]  \
                + skeleton[indexRow+1,indexCol+1] + skeleton[indexRow+1,indexCol-1] \
                + skeleton[indexRow-1,indexCol+1] + skeleton[indexRow-1,indexCol-1]  >= 3:
                    skeleton[indexRow, indexRow] = 0
                    skeleton[indexRow,indexCol+1], skeleton[indexRow,indexCol-1] = 0,0
                    skeleton[indexRow-1,indexCol], skeleton[indexRow+1,indexCol] = 0,0,
                    skeleton[indexRow+1,indexCol+1], skeleton[indexRow+1,indexCol-1] = 0,0
                    skeleton[indexRow-1,indexCol+1], skeleton[indexRow-1,indexCol-1] = 0,0,
            else:
                pass
    return skeleton

# Get the coordinate of each line.
def get_coordinates(lab, pbar, num_pbars, img_files):
    coord = []
    for ii in range(lab[1]):
        pbar.update(100/(lab[1]*num_pbars*len(img_files)))
        coord.append(np.vstack(np.where(lab[0]==(ii+1))))
    return coord

# Finds endpoints and deletes fibers with near endpoints
def find_endpoints(coord, skeleton, pbar, num_pbars, img_files):
    goodFibers = []
    allEndpoints = []
    for i, e in enumerate(coord):
        pbar.update(100/(len(coord)*num_pbars*len(img_files)))
        endPoints = []
        for ii, ee in enumerate(e[0]):
            # 'x' is the sum of all of the pixel values around x 
            x = skeleton[e[0][ii]+1][e[1][ii]] + skeleton[e[0][ii]-1][e[1][ii]] + skeleton[e[0][ii]][e[1][ii]+1] + skeleton[e[0][ii]][e[1][ii]-1] + skeleton[e[0][ii]+1][e[1][ii]-1] + skeleton[e[0][ii]+1][e[1][ii]+1] + skeleton[e[0][ii]-1][e[1][ii]-1] + skeleton[e[0][ii]-1][e[1][ii]+1]
            if x==1:  # if the sum of the pixels around x is 1 that means it is an endpoint
                endPoints.append([e[0][ii],e[1][ii]]) 
            else:
                pass
        flat_list = [item for sublist in endPoints for item in sublist]
        if len(flat_list) == 4:
            allEndpoints.append(endPoints) # This appends the x and y value of both endpoints of one fiber
            y2, x2, y1, x1 = endPoints[0][0], endPoints[0][1], endPoints[1][0], endPoints[1][1]
            d = np.sqrt((y2-y1)**2+(x2-x1)**2)
            if d > dist_between_endpoints_of_one_fiber:
                goodFibers.append(e)
        else:
            pass
    return goodFibers, allEndpoints, skeleton

# Gets the distance between two cartesian points
def dist_between_points(x1,y1,x2,y2):
    return np.sqrt((y2-y1)**2+(x2-x1)**2)

#Creating a list of all near end points
def get_near_endpoints(allEndpoints, correcting_distance, pbar, num_pbars, img_files):
    allNearEndpoints = []
    for index_of_fiber1, fiber1 in enumerate(allEndpoints):
        pbar.update(100/(len(allEndpoints)*num_pbars*len(img_files)))
        for index_of_fiber2, fiber2 in enumerate(allEndpoints): 
            if index_of_fiber1 != index_of_fiber2: # won't check endpoints on the same fiber
                f1_x1, f1_y1, f1_x2, f1_y2 = fiber1[0][0], fiber1[0][1], fiber1[1][0], fiber1[1][1] # gets the coords of the two endpoints in question
                f2_x1, f2_y1, f2_x2, f2_y2 = fiber2[0][0], fiber2[0][1], fiber2[1][0], fiber2[1][1]
                d1 = dist_between_points(f1_x1, f1_y1, f2_x1, f2_y1)
                d2 = dist_between_points(f1_x1, f1_y1, f2_x2, f2_y2)
                d3 = dist_between_points(f1_x2, f1_y2, f2_x1, f2_y1)
                d4 = dist_between_points(f1_x2, f1_y2, f2_x2, f2_y2)
                d1_endpoints = [[f1_x1, f1_y1],[f2_x1, f2_y1]]
                d2_endpoints = [[f1_x1, f1_y1],[f2_x2, f2_y2]]
                d3_endpoints = [[f1_x2, f1_y2],[f2_x1, f2_y1]]
                d4_endpoints = [[f1_x2, f1_y2],[f2_x2, f2_y2]]
                try:
                    if d1 < correcting_distance and list(reversed(d1_endpoints)) not in allNearEndpoints:
                        allNearEndpoints.append(d1_endpoints)
                        break
                    if d2 < correcting_distance and list(reversed(d2_endpoints)) not in allNearEndpoints:
                        allNearEndpoints.append(d2_endpoints)
                        break
                    if d3 < correcting_distance and list(reversed(d3_endpoints)) not in allNearEndpoints:                
                        allNearEndpoints.append(d3_endpoints)
                        break
                    if d4 < correcting_distance and list(reversed(d4_endpoints)) not in allNearEndpoints:                
                        allNearEndpoints.append(d4_endpoints)
                        break
                except TypeError:
                    print('TypeError')
                    pass
    return allNearEndpoints

# Fills in the pixels between two points
def fill_in(x1,y1,x2,y2): 
    list1 = []
    if x1 > x2: 
        x_vals = np.arange(x1-1,x2,-1)
    else:
        x_vals = np.arange(x1+1,x2,1)
    if y1 > y2:
        y_vals = np.arange(y1-1,y2,-1)
    else:
        y_vals = np.arange(y1+1,y2,1)
    if len(x_vals)==0:
        for y in y_vals:
            list1.append([x1, y])
    elif len(y_vals)==0:
        for x in x_vals:
            list1.append([x, y1])
    else:
        for x in x_vals:
            list1.append([x, y_vals[0]])
        for y in y_vals:
            list1.append([x_vals[-1],y])
    return list1

# Fills in the space between endpoints
def error_correction(allNearEndpoints, skeleton, pbar, num_pbars, img_files):
    for endpoints in allNearEndpoints:
        pbar.update(100/(len(allNearEndpoints)*num_pbars*len(img_files)))
        for points in fill_in(endpoints[0][0],
                            endpoints[0][1],
                            endpoints[1][0],
                            endpoints[1][1]):
            skeleton[points[0],points[1]]=1
    return skeleton

# creates length distribution and filters out fibers that aren't included in length distribution
def generate_length_distrubution(coord):
    filtered_Coord = []
    length_distrubution = []
    for i, e in enumerate(coord):
        x = len(e[0])*(1/0.717) # dimension: 594.0249 pixels for 1 mm or 0.594 pixel per micron (= 0.717 accounting for diagonal)
        if x > 20: # and x < 70: # only picks fibers greater than 20 microns
            length_distrubution.append(x)
            filtered_Coord.append(e)

    return length_distrubution, filtered_Coord





def fld_gen(image_folder_directory, min_fiber_length, max_fiber_length, csv_directory = None, 
            filename = f"{date_and_time}_distribution_data", pixel_conversion = pixel_conversion_4x, 
            correcting_distance=correcting_distance,dist_between_endpoints_of_one_fiber=dist_between_endpoints_of_one_fiber):
    
    pbar = tqdm(total=100)

    print("\nThis should take roughly 2 minutes per image\n\nIt it also normal if the appication becomes unresponsive\n")

    img_files = generate_img_files(image_folder_directory)
    
    for index, img_file in enumerate(img_files):

        # Importing and filtering image
        origional_img = cv2.imread(img_file)
        gray = cv2.cvtColor(origional_img, cv2.COLOR_BGR2GRAY)
        DoG = dog(gray, 2.2, 2, ksize=15) 
        blur = cv2.GaussianBlur(DoG,ksize=(5,5),sigmaX=0.7,sigmaY=0.7)
        _,thresh = cv2.threshold(blur,200,255,cv2.THRESH_BINARY)
        
        # Changes images form 0-255 to 0-1
        img = normalize_255_1(thresh, pbar, num_pbars, img_files)

        # Image thinning
        skeleton = skeletonize(img)

        # Changing skeleton for T,F to 1,0
        skeleton = normalize_TF_10(skeleton, img_files, num_pbars, pbar)

        # Adds zeros around the perimiter
        skeleton = np.pad(skeleton, 2)

        # Kills pxels with have three or more neighbors 
        skeleton = remove_3_neighbor_pixels(skeleton,pbar,num_pbars,img_files)

        # Check if neighboring cells are zero using a 2d convolution
        ker = np.array([[1,1,1],
                        [1,0,1],
                        [1,1,1]])
        res = convolve2d(skeleton,ker,mode='same')
        skeleton = np.int32((res>0)&(skeleton>0)) 

        # Seperates the image into labeled fibers 
        ker2= np.array([[1,1,1],
                        [1,1,1],
                        [1,1,1]])
        lab = label(skeleton, ker2) 

        # Gets the corrdinates of the labeled fibers
        coord = get_coordinates(lab, pbar, num_pbars, img_files)

        # generates: coords that contain only two endpoints, skeleton 
        coord, allEndpoints, skeleton = find_endpoints(coord, skeleton, pbar, num_pbars, img_files)
        # I think the skeleton ^^^^ can be deleted

        allNearEndpoints = get_near_endpoints(allEndpoints, correcting_distance, pbar, num_pbars, img_files)
      
        # Fills in the spaces between endpoints
        skeleton = error_correction(allNearEndpoints, skeleton, pbar, num_pbars, img_files)

        # generates: coords that contain only two endpoints, skeleton 
        coord, allEndpoints, skeleton = find_endpoints(coord, skeleton, pbar, num_pbars, img_files)
        
        # Seperates the skeleton array for the 2nd time
        lab = label(skeleton, ker2) 

        # Get the coordinate of each line for the 2nd time 
        coord = get_coordinates(lab, pbar, num_pbars, img_files)

        # creates length distribution and filters out fibers that aren't included in length distribution
        length_distrubution, filtered_Coord = generate_length_distrubution(coord)

    if csv_directory != None:
        df = pd.DataFrame(length_distrubution)
        df.to_csv(rf"{csv_directory}\{filename}.csv", index=False)

    if len(img_files) == 1:
        fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18,6))
        axes[0].imshow(origional_img)
        for i, e in enumerate(filtered_Coord):
            axes[1].scatter(filtered_Coord[i][1], abs(1800-filtered_Coord[i][0]), s = 0.1)
        axes[2].hist(length_distrubution, bins=bins, width=15) # company uses 17 bins
        axes[1].set_title("separated Fiber Arrays")
        axes[2].set_xticks(np.linspace(20, 300, 8))
        axes[2].set_xlim(20, 330)
        axes[2].set_title("FIber Length Distribution")
        axes[2].set_xlabel("Fiber Length (µm)")
        axes[2].set_ylabel("Occurence")
        fig.tight_layout()
        plt.show()
    else:
        plt.hist(length_distrubution, bins=bins) # company uses 17 bins
        plt.xticks(np.linspace(20, 300, 8))
        plt.xlim(20, 330)
        plt.title("FIber Length Distribution")
        plt.xlabel("Fiber Length (µm)")
        plt.ylabel("Occurence")
        plt.show() 