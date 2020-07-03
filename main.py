import os
from pathlib import Path

from flask import Flask, abort, request
from linebot import (
   LineBotApi, WebhookHandler
)
from linebot.exceptions import InvalidSignatureError
from linebot.models import (ImageMessage, ImageSendMessage, MessageEvent,
                            TextMessage, TextSendMessage)


from PIL import Image, ImageFilter
import numpy as np

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
    signature = request.headers["X-Line-Signature"]

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
    with open("static/" + message_id + ".jpg", "wb") as f:
        f.write(message_content.content)


    img = Image.open("static/" + message_id + ".jpg")
    width, height = img.size

    filter_size = 10
    out = Image.new('RGB', (width - filter_size, height - filter_size))

    img_pixels = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(img.getpixel((x, y)))
        # height毎に二次元配列としてappend
        img_pixels.append(row)
    # numpyのarrayに変換
    img_pixels = np.array(img_pixels)


    for y in range(height - filter_size):
        for x in range(width - filter_size):
            # 縦、横 filter_size(pixel)分、RGB情報取得
            partial_img = img_pixels[y:y + filter_size, x:x + filter_size]
            # 行をfilter_sizeの二乗、列を3(R/G/B)に変換
            color_array = partial_img.reshape(filter_size ** 2, 3)
            # RGB平均値を算出
            mean_r, mean_g, mean_b = color_array.mean(axis=0)
            # 算出されたRGB情報を該当ピクセルに設定
            out.putpixel((x, y), (int(mean_r), int(mean_g), int(mean_b)))

    out.show()
    # 画像比較用にfilter_sizeをファイル名に入れておく
    out.save('out/bokashi_{0}.jpg'.format(filter_size))

    #"static/" + message_id + ".jpg" = "out/bokashi_{0}.jpg"

    # 画像の送信
    image_message = ImageSendMessage(
        original_content_url="https://secret-lake-56663.herokuapp.com/sttic/out/bokashi_{0}.jpg",
        preview_image_url="https://secret-lake-56663.herokuapp.com/static/out/bokashi_{0}.jpg",
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