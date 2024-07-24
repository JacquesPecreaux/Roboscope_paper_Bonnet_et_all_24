# Code associated with article "The Roboscope: Smart and Fast Microscopy for Generic Event-Driven Acquisition" by J. Bonnet et al. 2024
# Code author: Célia Martin
# Code creation date: 2024
# Inscoper, SAS, France
# CNRS, Univ Rennes, IGDR (Institut de Génétique et Développement de Rennes) – UMR 6290, Rennes, France
# License: [CeCILL v2.1, see file Licence_CeCILL_V2.1-en.txt](../LICENSE.txt)

import os
import cv2

dataset_path ='/media/celia/Data/Roboscope/datasets/Mitoses/SlicesClassified/SlicesFromYolo/Leica_vivant/crossvalidation1/'
datasetCpy_path ='/media/celia/Data/Roboscope/datasets/Mitoses/SlicesClassified/SlicesFromYolo/Leica_vivant/crossvalidation1_eq/'
A_path=dataset_path+"A/"	#class0
I_path=dataset_path+"I/"	#class1
J_path=dataset_path+"J/"		#class2
M_path=dataset_path+"M/"	#class3
P_path=dataset_path+"P/"		#class4
PM_path=dataset_path+"PM/"	#class5
T_path=dataset_path+"T/"	#class6
data_path=[A_path,I_path,J_path,M_path,P_path,PM_path,T_path]
dataClass=["A","I","J","M","P","PM","T"]

dataSize_idx=0
dataSize_min=1000000


for path in data_path:
    data_dir=os.listdir(path)
    if len(data_dir)<dataSize_min:
        dataSize_min=len(data_dir)

for path in data_path:
    data_dir=os.listdir(path)
    image_idx=0
    image_prop=int(len(data_dir)/dataSize_min)
    nbImagesCopied=0
    for imageFile in data_dir : 
        if ((image_idx%image_prop)==0) & (nbImagesCopied<dataSize_min):
            imagePath=os.path.join(path, str(imageFile))
            image=cv2.imread(imagePath,-1)
            filepath=datasetCpy_path+dataClass[dataSize_idx]+'/'
            if not os.path.exists(filepath):
                os.makedirs(filepath)
            cv2.imwrite(filepath+imageFile,image)
            nbImagesCopied=nbImagesCopied+1
        image_idx=image_idx+1
    dataSize_idx=dataSize_idx+1
