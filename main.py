from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, ImageMessage, FlexSendMessage,CarouselContainer,BubbleContainer
import json
import os
import cv2
import imutils
import numpy as np
import colorsys


work = {}
path_w1 = 'saveid.txt'
path_w2 = 'savereply.txt'
app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)
FQDN = os.environ["FQDN"]


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]

    body = request.get_data(as_text=True)
    print("Request body" + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(event.reply_token,
       [
           TextSendMessage(text=event.message.text),
           #TextSendMessage(text="おはよ------"),
           #TextSendMessage(text="顔、目を検知できませんでした。"),
           #TextSendMessage(text=event.message.id),
       ]
       )
    print("取得イヴェント:{}".format(event))
    print("取得イヴェントメッセージID:{}".format(event.message.id))
    print("リプライトークン：{}".format(event.reply_token))
    print("------リプライ型------")
    print(type(event.reply_token))
    if event.message.text == "1":
        print("通過: {}".format(event.message.text))
        with open(path_w1) as f:
            work = f.read()
        with open(path_w2) as f2:
            work1 = f2.read()
        handle_send_message2(work,work1)
    if event.message.text == "2":
        print("通過: {}".format(event.message.text))
        with open(path_w1) as f:
            work = f.read()
        with open(path_w2) as f2:
            work1 = f2.read()
        handle_send_message3(work,work1)



def text_save_id(work):
    s = work
    print("取得イヴェントメッセージIDDDDDDDDDDDDDDDD_text_saveID:{}".format(work))
    with open(path_w1, mode='w') as f:
        f.write(s)

def text_save_reply(work):
    s = work
    print("取得イヴェントメッセージIDDDDDDDDDDDDDDDD_text_saveReply:{}".format(work))
    with open(path_w2, mode='w') as f:
        f.write(s)


def flex(event):
    work = event.message.id
    reply_work = event.reply_token
    print("取得イヴェントメッセージIDDDDDDDDDDDDDDDD:{}".format(work))
    text_save_id(work)
    text_save_reply(reply_work)
    json_open = open('test.json', 'r')
    json_data = json.load(json_open)
    user_id = os.environ["USER_ID"]
    #print("json_data: {}".format(json_data.get("hero").get("url")))
    #print(json_data.get("hero").get("url"))
    #json_data["hero"]
    #message = line_bot_api.reply_message(
    #    event.reply_token,
    #    [
    #        FlexSendMessage(
    #        alt_text="flex",
    #        contents=BubbleContainer.new_from_json_dict(json_data)
    #        )
    #    ]
    #)

    messages = FlexSendMessage(alt_text="test", contents=json_data)
    print("フレックスメッセージ中身: {}".format(messages))
    if event.reply_token == "00000000000000000000000000000000":
        return
    if event.reply_token == "ffffffffffffffffffffffffffffffff":
        return
        
    line_bot_api.push_message(user_id, messages=messages)


def handle_textmessage(event):
    line_bot_api.reply_message(event.reply_token,
        [
            #TextSendMessage(text=event.message.text),
            TextSendMessage(text="顔、目を検知できませんでした。"),
            #TextSendMessage(text=event.message.id),
        ]
        )

#画像受信後処理
@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    print("メッセージID")
    print(event.message.id)
    message_content = line_bot_api.get_message_content(event.message.id)
    if not os.path.exists('static'):
        os.mkdir('static/')
    with open("static/" + event.message.id + ".jpg", "wb") as f:
        f.write(message_content.content)
    
    
    flex(event)

    

    
# #画像送信処理
# def handle_send_message(event):
#     #mozaiku(event)
#     result = change_image(event)

#     if result:
#         line_bot_api.reply_message(
#             event.reply_token, ImageSendMessage(
#                 original_content_url=FQDN + "/static/" + event.message.id + "_face.jpg",
#                 preview_image_url=FQDN + "/static/" + event.message.id + "_face.jpg",
#             )
#             )

#     else:
#         handle_textmessage(event)


#画像送信処理
def handle_send_message2(event,relpy):
    #mozaiku(event)
    result = change_image(event)
    reply = str(relpy)
    if result:
        line_bot_api.reply_message(
            reply, ImageSendMessage(
                original_content_url=FQDN + "/static/" + event + "_face.jpg",
                preview_image_url=FQDN + "/static/" + event + "_face.jpg",
            )
        )

    else:
        handle_textmessage(event)

#画像送信処理
def handle_send_message3(event,relpy):
    #mozaiku(event)
    result = change_image2(event)
    reply = str(relpy)

    if result:
        line_bot_api.reply_message(
            reply, ImageSendMessage(
                original_content_url=FQDN + "/static/" + event + "_face.jpg",
                preview_image_url=FQDN + "/static/" + event + "_face.jpg",
            )
        )

    else:
        handle_textmessage(event)

#囲う処理
def change_image(event):
    bool = True
    cascade_path = "haarcascade_frontalface_default.xml"
    cascade_eye_path = "haarcascade_eye.xml"

    image_file = event + ".jpg"
    save_file = event + "_face.jpg"
    #save_file2 = event.message.id + "_face2.jpg"
    print("イメージファイル: {} // {}".format(image_file, save_file))
    image_path = "static/" + image_file
    print("イメージパス: {}".format(image_path))
    output_path = "static/" + save_file
    #output_path2 = "static/" + save_file2
    print("アウトプットパス: {}".format(output_path))
    # ファイル読み込みo
    image = cv2.imread(image_path)

    # グレースケール変換
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # カスケード分類器の特徴量を取得する
    cascade = cv2.CascadeClassifier(cascade_path)
    cascade_eye = cv2.CascadeClassifier(cascade_eye_path)
    # 物体認識（顔認識）の実行
    # image – CV_8U 型の行列．ここに格納されている画像中から物体が検出されます
    # objects – 矩形を要素とするベクトル．それぞれの矩形は，検出した物体を含みます
    # scaleFactor – 各画像スケールにおける縮小量を表します
    # minNeighbors – 物体候補となる矩形は，最低でもこの数だけの近傍矩形を含む必要があります
    # flags – このパラメータは，新しいカスケードでは利用されません．古いカスケードに対しては，cvHaarDetectObjects 関数の場合と同じ意味を持ちます
    # minSize – 物体が取り得る最小サイズ．これよりも小さい物体は無視されます
    facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=2, minSize=(30, 30))
    eyerect = cascade_eye.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=2, minSize=(20, 20))
    print("レクト:{} // {}".format(facerect, eyerect))
    print("ぎっとぽっど")

    color = (255, 0, 0)  # 青

    ## 検出した場合
    #if len(facerect) > 0:
    #    # 検出した顔を囲む矩形の作成
    #    for rect in facerect:
    #        cv2.rectangle(image, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), color, thickness=1)
    #        print(facerect)
    #        print(rect)
    #else:
    #    bool = False

    ratio = 0.05  # 縮小処理時の縮小率(小さいほどモザイクが大きくなる)
    if len(eyerect) > 0:
        # for rect in eyerect:
        #     cv2.rectangle(image, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), color, thickness=1)
        #     print(eyerect)
        #     print(rect)
           

        for x, y, w, h in eyerect:  # 引数でeyesで取得した数分forループ
           # y:はHEIGHT、x:はWEIGHT  fxはxの縮小率、fyはyの縮小率
           small = cv2.resize(image[y: y + h, x: x + w], None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
           image[y: y + h, x: x + w] = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
           
    else:
        bool = False

    if bool:
        # 認識結果の保存
        cv2.imwrite(output_path, image)
        #cv2.imwrite(output_path2, image)
        return True
    else:
        return False




def get_head_mask(img):
 

    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)

    """
    The algorithm works best when a person is on a background that does not merge with his hair. Also, the hair should not merge with the complexion.
    """
    """
    Get the mask of the head
    Cuting  BG
    :param img: source image
    :return:   Returns the mask with the cut out BG
    """
    mask = np.zeros(img.shape[:2], np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    faces = faceCascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))    # Find faces
    if len(faces) != 0:
        x, y, w, h = faces[0]
        (x, y, w, h) = (x - 40, y - 100, w + 80, h + 200)
        rect1 = (x, y, w, h)
        cv2.grabCut(img, mask, rect1, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)     #Crop BG around the head
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')  # Take the mask from BG

    return mask2

def is_bold(pnt, hair_mask):
    """
    Check band or not
    :param pnt: The upper point of the head
    :param hair_mask: Mask with hair
    :return: True if Bald, else False
    """
    roi = hair_mask[pnt[1]:pnt[1] + 40, pnt[0] - 40:pnt[0] + 40]    # Select the rectangle under the top dot
    cnt = cv2.countNonZero(roi) # Count the number of non-zero points in this rectangle
    # If the number of points is less than 25%, then we think that the head is bald
    if cnt < 800:
        print("Bald human on phoro")
        return True
    else:
        print("Not Bold")
        return False

#def hsv_to_rgb(h,s,v):
##    h = 0 ~ 360
##    s = 0 ~ 255
##    v = 0 ~ 255
#    i = int(h / 60.0)
#    mx = v
#    mn = v - ((s / 255.0) * v)
#    if h is None:
#        return(0,0,0)
#    if i == 0:
#        (r1,g1,b1) = (mx,(h/60.0)*(mx-mn)+mn,mn)
#    elif i == 1:
#        (r1,g1,b1) = (((120.0-h)/60.0)*(mx-mn)+mn,mx,mn)
#    elif i == 2:
#        (r1,g1,b1) = (mn,mx,((h-120.0)/60.0)*(mx-mn)+mn)
#    elif i == 3:
#        (r1,g1,b1) = (mn,((240.0-h)/60.0)*(mx-mn)+mn,mx)
#    elif i == 4:
#        (r1,g1,b1) = (((h-240.0)/60.0)*(mx-mn)+mn,mn,mx)
#    elif 5 <= i:
#        (r1,g1,b1) = (mx,mn,((360.0-h)/60.0)*(mx-mn)+mn)
#    return (int(r1), int(g1), int(b1))

def change_image2(event):
    image_file = event + ".jpg"
    save_file = event + "_face.jpg"
    #save_file2 = event.message.id + "_face2.jpg"
    print("イメージファイル: {} // {}".format(image_file, save_file))
    image_path = "static/" + image_file
    print("イメージパス: {}".format(image_path))
    output_path = "static/" + save_file
    #output_path2 = "static/" + save_file2
    print("アウトプットパス: {}".format(output_path))

    image = cv2.imread(image_path)     # Load image
    image = imutils.resize(image, height=500)     # We result in 500px in height
    mask = get_head_mask(image)      # We get the mask of the head (without BG)

    # Find the contours, take the largest one and memorize its upper point as the top of the head
    cnts = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[0]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    cnt=cnts[0]
    topmost = tuple(cnt[cnt[:,:,1].argmin()][0])


    # We remove the face by the color of the skin
    lower = np.array([0, 0, 100], dtype="uint8")  # Lower limit of skin color
    upper = np.array([255, 255, 255], dtype="uint8")  # Upper skin color limit
    converted = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)   # We translate into HSV color format
    skinMask = cv2.inRange(converted, lower, upper)     # Write a mask from places where the color is between the outside
    mask[skinMask == 255] = 0   # We remove the face mask from the mask of the head

    kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.dilate(mask, kernel1, iterations=1)
    i1 = cv2.bitwise_and(image, image, mask=mask)


    # 髪の毛なし
    if is_bold(topmost,mask):
        cv2.rectangle(image,topmost,topmost,(0,0,255),5)
        print(topmost)



    # 髪の毛あり
    else:
        #輪郭取得
        cnts = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        cv2.drawContours(image,[cnts[0]],-1,(0,0,255),2)
       # green = np.uint8([[[0,255,0 ]]])
        #bgr = cv2.cvtColor(np.array([[[0,255,0]]], dtype=np.uint8), cv2.COLOR_HSV2BGR)[0][0]
        #ポリゴンの領域を塗りつぶす
        
        #test_color = hsv_to_rgb(300, 200 , 200)
        
        
        cv2.fillPoly(image, pts =[cnts[0]], color=(0,0,10))

        #green = np.uint8([[[0,255,0 ]]])
        #hsv_green = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
        #image[:] = hsv_green
        for c in cnts[0]:
            print(c)


    if bool:
        # 認識結果の保存
        cv2.imwrite(output_path, image)
        #cv2.imwrite(output_path2, image)
        return True
    else:
        return False
    # # Display the image in a loop
    # while True:
    #     cv2.imwrite(output_path, image)
    #     #cv2.imshow("image1", image)
    #     # Exit to Esc
    #     if cv2.waitKey(5) == 27:
    #         break


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
