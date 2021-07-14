from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
)

import random

app = Flask(__name__)

line_bot_api = LineBotApi('iCw04qORsvX81qjY77WP2KH9TBrk0/WQX2RIgPm2wIYDU7URknX2doJLkl9X15bi7acNUqWyjNkr5Gd0HZhYfBrQnhAX6e59E44pfytqZL/CBuCEzC9BMZc97rHJYOUdqjp41DcgBIaPY9b/7uSlUwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f2327d686eec9367f95df51821e9028d')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text

    if msg == 'R':
        ran = random.randint(1988, 2027)
        sticker_message = StickerSendMessage(
        package_id='446',
        sticker_id= ran
        )

        line_bot_api.reply_message(
            event.reply_token,
            sticker_message)
        return

    r = '特殊指令有:["新北王先生"，"塞車"] 隨機貼圖請輸入:"R"'
    if msg == '新北王先生':
        r = '一路大順暢!'
    elif '塞車' in msg:
        r = '很誇張 我有行車紀錄器你知道嗎'
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))




if __name__ == "__main__":
    app.run()
