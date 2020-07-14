import os
from pathlib import Path

from flask import Flask, abort, request
from linebot import (
   LineBotApi, WebhookHandler
)
from linebot.exceptions import InvalidSignatureError
from linebot.models import (ImageMessage, ImageSendMessage, MessageEvent,
                            TextMessage, TextSendMessage)
import cv2
#import cv2,numpy


app = Flask(__name__)



YOUR_CHANNEL_ACCESS_TOKEN = "d9TJaXv1KYVppBbVUrSZxF+XGe4N+IL9JtUpAA8VgJXk4OVmiYhiEgUMaDLq8Ic2idBZbBYcdwksMd3THXzSf5CHrLdtXi2i0Irq2iVaKw72MVNrKShwNr2JMQJ/yi0+XLA6hkEaE+0JqoXWzbDtTAdB04t89/1O/w1cDnyilFU="
YOUR_CHANNEL_SECRET = "e0b5ca81f71074e9639844976085b288"

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

#SRC_IMAGE_PATH = "https://secret-lake-56663.herokuapp.com/static/{}.jpg"
#MAIN_IMAGE_PATH = "https://secret-lake-56663.herokuapp.com/static/{}_main.jpg"
#PREVIEW_IMAGE_PATH = "https://secret-lake-56663.herokuapp.com/static/{}_preview.jpg"



@app.route("/")
def hello_world():
    return "hello world!"


@app.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]     #lineしか受け付けない

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=event.message.text)
    )


@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    message_id = event.message.id

    # 画像を保存

    message_content = line_bot_api.get_message_content(message_id)



    fname = "static/" + message_id + ".jpg"  # 画像ファイル名
    img = cv2.imread(fname)  # 画像を読み出しオブジェクトimgに代入

    # オブジェクトimgのshapeメソッドの1つ目の戻り値(画像の高さ)をimg_heightに、2つ目の戻り値(画像の幅)をimg_widthに代入
    img_height, img_width = img.shape[:2]

    scale_factor = 0.1  # 縮小処理時の縮小率(小さいほどモザイクが大きくなる)
    img = cv2.resize(img, None, fx=scale_factor, fy=scale_factor)  # 縮小率の倍率で画像を縮小
    # 画像を元の画像サイズに拡大。ここで補完方法に'cv2.INTER_NEAREST'を指定することでモザイク状になる
    img = cv2.resize(img, (img_width, img_height), interpolation=cv2.INTER_NEAREST)
    cv2.imwrite('mosaic.png', img)  # ファイル名'mosaic.png'でimgを保存

    with open("static/mosaic.jpg", "wb") as f:
        f.write(message_content.content)

    # 画像の送信
    image_message = ImageSendMessage(
        original_content_url="https://secret-lake-56663.herokuapp.com/static/mosaic.jpg",
        preview_image_url="https://secret-lake-56663.herokuapp.com/static/mosaic.jpg",
    )

    #app.logger.info("https://secret-lake-56663.herokuapp.com/static/{main_image_path}")
    line_bot_api.reply_message(event.reply_token, image_message)

    # 画像を削除する
    #src_image_path.unlink()


#def save_image(message_id: str, save_path: str) -> None:
    #"""保存"""
    #message_content = line_bot_api.get_message_content(message_id)
    #with open(save_path, "wb") as f:
       # for chunk in message_content.iter_content():
        #    f.write(chunk)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)