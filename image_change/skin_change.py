from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, ImageMessage, FlexSendMessage,CarouselContainer,BubbleContainer
import main
import json
import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
import path_data


def skin_image(event,userid):
    image_path, output_path = path_data.get_image_path(event,userid)
  
 
    image = cv2.imread(image_path)     # Load image
 
    # h_th_low = 0 
    # h_th_up = 30
    # s_th = 30
    # v_th = 150
 
    # hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # h, s, v = cv2.split(hsv)
 
    # if h_th_low > h_th_up:
    #     ret, h_dst_1 = cv2.threshold(h, h_th_low, 255, cv2.THRESH_BINARY) 
    #     ret, h_dst_2 = cv2.threshold(h, h_th_up,  255, cv2.THRESH_BINARY_INV)
        
    #     dst = cv2.bitwise_or(h_dst_1, h_dst_2)
 
    # else:
    #     ret, dst = cv2.threshold(h,   h_th_low, 255, cv2.THRESH_TOZERO) 
    #     ret, dst = cv2.threshold(dst, h_th_up,  255, cv2.THRESH_TOZERO_INV)
 
    #     ret, dst = cv2.threshold(dst, 0, 255, cv2.THRESH_BINARY)
        
    # ret, s_dst = cv2.threshold(s, s_th, 255, cv2.THRESH_BINARY)
    # ret, v_dst = cv2.threshold(v, v_th, 255, cv2.THRESH_BINARY)
 
    # dst = cv2.bitwise_and(dst, s_dst)
    # dst = cv2.bitwise_and(dst, v_dst)
 
    HSV_MIN = np.array([0, 30, 30])
    HSV_MAX = np.array([30, 150, 255])
 
 
    # #convert hsv
    # img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
 
    # #mask hsv region
    # mask_hsv = cv2.inRange(img_hsv, HSV_MIN, HSV_MAX)
 
    # hsv_2 = np.copy(mask_hsv)
    # hsv_2[:, :, 0] = np.where((mask_hsv[:, :, 0]>16) & (mask_hsv[:, :, 0]<25) ,mask_hsv[:, :,(2)]*0.2,mask_hsv[:, :, 0])
    
    height = image.shape[0]
    width = image.shape[1]
    img2 = cv2.resize(image , (int(width*0.5), int(height*0.5)))
    hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV) # BGR->HSV変換
    hsv_2 = np.copy(hsv)
    hsv_2[:, :, 0] = np.where((hsv[:, :, 0]>4) & (hsv[:, :, 0]<30) ,hsv[:, :,(2)]*0.3,hsv[:, :, 0])
    bgr = cv2.cvtColor(hsv_2, cv2.COLOR_HSV2BGR)
    
    
    # white = [255, 255, 255]
    # green = [156,100,71]
    # image[mask_hsv>0]=(130,190,70)
    
    # img_bgr =cv2.cvtColor(mask_hsv, cv2.COLOR_HSV2BGR)
    # image[img_bgr>0]=(65,155,50,0.8)
    bgr = cv2.cvtColor(hsv_2, cv2.COLOR_HSV2BGR)
    cv2.imwrite(output_path, bgr)