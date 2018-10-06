import os, sys
from flask import Flask,request
from utils import wit_response, get_news_elements
from pymessenger import Bot

app=Flask(__name__)

PAGE_ACCESS_TOKEN="EAAEyGbC3w3YBAMqHQjZA3l1v7dHqbhxbYQJrNkv2prXdxoOviUP3B67c2soUF1l9MQuywmJLGZBWfowSWz5TZAGYSIh60dD4V8bGhQSZCbI2FCZCKDIAZB7l2LKWeZAY4XBJg57qClH0zzoU0QAhlGFzAXMLZBtOvbmXFpY2rkV35QZDZD"

bot = Bot(PAGE_ACCESS_TOKEN)
@app.route('/',methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verifiation token mismatch",403
        return request.args["hub.challenge"],200
    return "Privacy Policy: It is just a news CHATBOT created for minimal Use so there is no such privacy policies included.",200

@app.route('/', methods=['POST'])
def webhook():
    data=request.get_json()
    log(data)

    if data['object']=='page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']

                if messaging_event.get('message'):
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                    else:
                        messaging_text = 'no text'

                    categories= wit_response(messaging_text)
                    elements = get_news_elements(categories)
                    bot.send_generic_message(sender_id, elements)
    




    return "ok",200

def log(message):
    print(message)
    sys.stdout.flush()


if __name__=="__main__":
    app.run(debug = True,port = 80)

