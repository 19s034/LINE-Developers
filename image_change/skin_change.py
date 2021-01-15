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
import random


def skin_image(event,userid):
    image_path, output_path = path_data.get_image_path(event,userid)
  
 
    image = cv2.imread(image_path)     # Load image
 

 
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) # BGR->HSV変換
    hsv_2 = np.copy(hsv)

    #a = random.randint(1,5)
    #if a == 1:
    #    hsv_2[:, :, 0] = np.where((hsv[:, :, 0]>6) & (hsv[:, :, 0]<30) ,hsv[:, :, 0] + 50,hsv[:, :, 0]) #緑
    #elif a == 2:
    #    hsv_2[:, :, 0] = np.where((hsv[:, :, 0]>6) & (hsv[:, :, 0]<30) ,hsv[:, :, 0] + 100,hsv[:, :, 0]) #青
    #elif a == 3:
    #    hsv_2[:, :, 0] = np.where((hsv[:, :, 0]>6) & (hsv[:, :, 0]<30) ,hsv[:, :, 0] + 15,hsv[:, :, 0]) #黄色
    #elif a == 4:
    #    hsv_2[:, :, 0] = np.where((hsv[:, :, 0]>6) & (hsv[:, :, 0]<30) ,hsv[:, :, 0] + 140,hsv[:, :, 0]) #ピンク
    #elif a == 5:
    #    hsv_2[:, :, 0] = np.where((hsv[:, :, 0]>6) & (hsv[:, :, 0]<30) ,hsv[:, :, 0] *0.001,hsv[:, :, 0]) #赤色
    #elif a == 6:
    hsv_2[:, :, 2] = np.where((hsv[:, :, 0]>6) & (hsv[:, :, 0]<30) ,hsv[:, :, 2] *0.3,hsv[:, :, 2]) #黒色
    hsv_2[:, :, 2] = np.where((hsv_2[:, :, 0]>6) & (hsv_2[:, :, 0]<30) ,hsv_2[:, :, 1] *0.3,hsv_2[:, :, 2]) #黒色
    #0.001 赤
    #0.3 緑
    bgr = cv2.cvtColor(hsv_2, cv2.COLOR_HSV2BGR)
    

    bgr = cv2.cvtColor(hsv_2, cv2.COLOR_HSV2BGR)
    cv2.imwrite(output_path, bgr)