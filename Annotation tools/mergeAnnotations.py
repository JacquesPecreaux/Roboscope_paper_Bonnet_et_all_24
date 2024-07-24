
# Code associated with article "The Roboscope: Smart and Fast Microscopy for Generic Event-Driven Acquisition" by J. Bonnet et al. 2024
# Code author: Célia Martin
# Code creation date: 2024
# Inscoper, SAS, France
# CNRS, Univ Rennes, IGDR (Institut de Génétique et Développement de Rennes) – UMR 6290, Rennes, France
# License: [CeCILL v2.1, see file Licence_CeCILL_V2.1-en.txt](../LICENSE.txt)

from libs.pascal_voc_io import PascalVocReader
import cv2
import numpy as np
from libs.labelFile import LabelFile
import os
try:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
except ImportError:
    # needed for py3+qt4
    # Ref:
    # http://pyqt.sourceforge.net/Docs/PyQt4/incompatible_apis.html
    # http://stackoverflow.com/questions/21217399/pyqt4-qtcore-qvariant-object-instead-of-a-string
    if sys.version_info.major >= 3:
        import sip
        sip.setapi('QVariant', 2)
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *

def iou(bboxA, bboxB):
    # intersect rectangle
    xmin = max(bboxA[1][0][0], bboxB[1][0][0])
    ymin = max(bboxA[1][0][1], bboxB[1][0][1])
    xmax = min(bboxA[1][2][0], bboxB[1][2][0])
    ymax = min(bboxA[1][2][1], bboxB[1][2][1])
    
    areaI = max(0, xmax-xmin) * max(0, ymax-ymin)
    areaA = (bboxA[1][2][0]-bboxA[1][0][0]) * (bboxA[1][2][1]-bboxA[1][0][1])
    areaB = (bboxB[1][2][0]-bboxB[1][0][0]) * (bboxB[1][2][1]-bboxB[1][0][1])
    
    IoU = areaI / (areaA + areaB - areaI)
    return IoU

def mergeShapes(bboxA, bboxB) : 
    # intersect rectangle
    xmin = min(bboxA[1][0][0], bboxB[1][0][0])
    ymin = min(bboxA[1][0][1], bboxB[1][0][1])
    xmax = max(bboxA[1][2][0], bboxB[1][2][0])
    ymax = max(bboxA[1][2][1], bboxB[1][2][1])
    return [bboxA[0],[(xmin,ymin),(xmax,ymin),(xmax,ymax),(xmin,ymax)], None, None, False]

def format_shape(s):
    return dict(label=s[0],
                line_color=s[2],
                fill_color=s[3],
                points=s[1],
                difficult=s[4])

annotation1FolderPath='/media/celia/Data/Roboscope/datasets/Mitoses/Yolo/Vivant/Leica/dim_2048_2048/NT_1_1_Split/film1_Claire/'
annotation2FolderPath='/media/celia/Data/Roboscope/datasets/Mitoses/Yolo/Vivant/Leica/dim_2048_2048/NT_1_1_Split/NT_1_1_Split_Louis/'
annotationMerged='/media/celia/Data/Roboscope/datasets/Mitoses/Yolo/Vivant/Leica/dim_2048_2048/NT_1_1_Split/Merged/'
if not os.path.exists(annotationMerged):
    os.makedirs(annotationMerged)
nms_threshold=0.3
partialAnnotation=False

annotation1FolderDir = sorted(os.listdir(annotation1FolderPath))
annotation2FolderDir = sorted(os.listdir(annotation2FolderPath))

for annotation1File in annotation1FolderDir:  
    if annotation1File.lower().endswith('.xml'):  
        for annotation2File in annotation2FolderDir:    
            if(annotation1File==annotation2File) : 
                t_voc_parse_reader = PascalVocReader(annotation1FolderPath+annotation1File)
                shapes_ann1 = t_voc_parse_reader.get_shapes()
                for i in range(len(shapes_ann1)) : 
                    for j in range (i+1,len(shapes_ann1)) : 
                        iou2 = iou(shapes_ann1[i], shapes_ann1[j])
                        if iou2 > nms_threshold:
                            nms_threshold=iou2

                t_voc_parse_reader = PascalVocReader(annotation2FolderPath+annotation2File)
                shapes_ann2 = t_voc_parse_reader.get_shapes()
                for i in range(len(shapes_ann2)) : 
                    for j in range (i+1,len(shapes_ann2)) : 
                        iou2 = iou(shapes_ann2[i], shapes_ann2[j])
                        if iou2 > nms_threshold:
                            nms_threshold=iou2

                shapes_merged=[]
                for i in range(len(shapes_ann1)) : 
                    foundInAnn2=False
                    for j in range (len(shapes_ann2)) : 
                        iou2 = iou(shapes_ann1[i], shapes_ann2[j])
                        if iou2 > nms_threshold:
                            foundInAnn2=True
                            if shapes_ann1[i][0] == shapes_ann2[j][0] :
                                shape=mergeShapes(shapes_ann1[i],shapes_ann2[j])
                                shapes_merged.append(shape)
                    if partialAnnotation : 
                        if not foundInAnn2 :
                            shapes_merged.append(shapes_ann1[i])
                
                if partialAnnotation : 
                    for i in range(len(shapes_ann2)) : 
                        foundInMerged=False
                        for j in range (len(shapes_merged)) : 
                            iou2 = iou(shapes_ann2[i], shapes_merged[j])
                            if iou2 > nms_threshold:
                                foundInMerged=True
                        if not foundInMerged : 
                            shapes_merged.append(shapes_ann2[i])

                shapes = [format_shape(shape) for shape in shapes_merged]

                label_file = LabelFile()
                imagePath=annotation1FolderPath+annotation2File
                imagePath=imagePath.replace('.xml', '.tif')
                label_file.save_pascal_voc_format(annotationMerged+annotation2File, shapes, imagePath, None)

