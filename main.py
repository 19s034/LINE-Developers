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


app = Flask(__name__)



YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

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

    message_content = linae_bot_api.get_message_content(message_id)
    with open("static/" + message_id + ".jpg", "wb") as f:
        f.write(message_content.content)

    img = Image.open(message_id + ".jpg")
    message_content.content = img.filter(ImageFilter.GaussianBlur(4))

    # 画像の送信
    image_message = ImageSendMessage(
        original_content_url="https://secret-lake-56663.herokuapp.com/sttic/"+ message_id + ".jpg",
        preview_image_url="https://secret-lake-56663.herokuapp.com/static/"+ message_id + ".jpg",
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