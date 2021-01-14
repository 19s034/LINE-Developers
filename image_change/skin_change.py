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
 

 
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) # BGR->HSV変換
    hsv_2 = np.copy(hsv)
    hsv_2[:, :, 0] = np.where((hsv[:, :, 0]>10) & (hsv[:, :, 0]<35) ,hsv[:, :, 0] + 80,hsv[:, :, 0])
    #0.001 赤
    #0.3 緑
    bgr = cv2.cvtColor(hsv_2, cv2.COLOR_HSV2BGR)
    

    bgr = cv2.cvtColor(hsv_2, cv2.COLOR_HSV2BGR)
    cv2.imwrite(output_path, bgr)