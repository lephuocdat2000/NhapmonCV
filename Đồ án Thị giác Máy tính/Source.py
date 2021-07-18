import cv2
import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from numpy import asarray
from PIL import Image, ImageFilter, ImageTk
import math
from tkinter import *
from tkinter import ttk

def Cluster_pixel(array,value):
  kmeans_kwargs={
         "init" : "k-means++",
         "n_init": 3,
         "max_iter":200,
         "random_state":42
  }
  kmeans=KMeans(n_clusters=3, **kmeans_kwargs)
  kmeans.fit(array)
  labels=kmeans.labels_
  centroids=kmeans.cluster_centers_
  centroids=centroids.reshape(len(centroids))
  vt_min=np.argmin(abs(centroids-value))
  backgr_pixel= array[np.where(labels==vt_min)]
  return backgr_pixel


def UyXma(arr):
  uy=arr.sum()/len(arr)
  temp=(uy-arr)**2
  print(temp)
  t=temp.sum()
  xma=math.sqrt(t*(1/len(arr)))
  return uy,xma


def CreateMaskObj(img_hsv, upper_arr, lower_arr):
  mask=cv2.inRange(img_hsv, lower_arr, upper_arr)
  mask=1-mask/255
  mask_obj1=[mask,mask,mask]
  mask_obj1=(np.stack(mask_obj1,axis=2)).astype('uint8')
  return mask_obj1


def ImagetoImage(img, H_thresh, S_thresh):
  img_hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
  H_channel=img_hsv[:,:,0].copy()
  H_vecfit=H_channel.reshape((H_channel.shape[0]*H_channel.shape[1], 1))
  S_channel=img_hsv[:,:,1].copy()
  S_vecfit=S_channel.reshape((S_channel.shape[0]*S_channel.shape[1], 1))
  H_backgr=Cluster_pixel(H_vecfit, H_thresh)
  S_backgr=Cluster_pixel(S_vecfit, S_thresh)
  H_max,H_min=np.max(H_backgr), np.min(H_backgr)
  S_max,S_min=np.max(S_backgr), np.min(S_backgr)
  lower_green=np.array([H_min, S_min, 0])
  upper_green=np.array([H_max, S_max, 255])
  return lower_green, upper_green

def Get_threshold(img, H_thresh, S_thresh):
  lower, upper = ImagetoImage(img, H_thresh, S_thresh)
  return lower, upper

def Remove_background(img, background, lower, upper):
  background=cv2.resize(background, (img.shape[1],img.shape[0]))
  mask_obj1=CreateMaskObj(cv2.cvtColor(img, cv2.COLOR_BGR2HSV), upper, lower)
  res=(img*mask_obj1).astype('uint8')+(background*(1-mask_obj1)).astype('uint8')
  return res

# threshold = 0
# video = cv2.VideoCapture('chromavid.mp4')
# background = cv2.imread('1.jpg')
# while(video.isOpened()):
#   ret, frame = video.read()
#   if ret:
#     if threshold==0:
#       lower, upper = Get_threshold(frame)
#       threshold=1
#     res = Remove_background(frame, background, lower, upper)
#     res = cv2.resize(res, (500, 300))
#     cv2.imshow('1', res)
#     cv2.waitKey(10)
#   else:
#     break
# video.release()
# cv2.destroyAllWindows()

