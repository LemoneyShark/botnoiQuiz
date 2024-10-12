from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import json
import aiohttp

app = FastAPI()

# Your LINE Channel Access Token
LINE_CHANNEL_ACCESS_TOKEN = '2006449220'

@app.post("/callback")
async def callback(request: Request):
    body = await request.json()
    events = body.get("events", [])

    for event in events:
        if event["type"] == "message" and event["message"]["type"] == "text":
            reply_token = event["replyToken"]
            user_message = event["message"]["text"]
            await reply_message(reply_token, user_message)

    return JSONResponse(status_code=200)

async def reply_message(reply_token: str, user_message: str):
    # Prepare the reply message
    reply_message = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "text",
                "text": f"You said: {user_message}"
            },
            {
                "type": "template",
                "altText": "this is a button template",
                "template": {
                    "type": "buttons",
                    "title": "Menu",
                    "text": "Please select",
                    "actions": [
                        {
                            "type": "postback",
                            "label": "Postback",
                            "data": "action=buy&itemid=123"
                        },
                        {
                            "type": "message",
                            "label": "Say Hello",
                            "text": "Hello"
                        }
                    ]
                }
            },
            {
                "type": "sticker",
                "packageId": "1",
                "stickerId": "1"
            },
            {
                "type": "flex",
                "altText": "Carousel",
                "contents": {
                    "type": "carousel",
                    "contents": [
                        {
                            "type": "bubble",
                            "hero": {
                                "type": "image",
                                "url": "https://example.com/image1.jpg",
                                "size": "full",
                                "aspectRatio": "20:13",
                                "aspectMode": "cover"
                            },
                            "body": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "Title 1",
                                        "weight": "bold",
                                        "size": "xl"
                                    },
                                    {
                                        "type": "text",
                                        "text": "Description 1",
                                        "wrap": True
                                    }
                                ]
                            },
                            "footer": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "button",
                                        "style": "link",
                                        "action": {
                                            "type": "uri",
                                            "label": "View",
                                            "uri": "https://example.com"
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            "type": "bubble",
                            "hero": {
                                "type": "image",
                                "url": "https://example.com/image2.jpg",
                                "size": "full",
                                "aspectRatio": "20:13",
                                "aspectMode": "cover"
                            },
                            "body": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "Title 2",
                                        "weight": "bold",
                                        "size": "xl"
                                    },
                                    {
                                        "type": "text",
                                        "text": "Description 2",
                                        "wrap": True
                                    }
                                ]
                            },
                            "footer": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "button",
                                        "style": "link",
                                        "action": {
                                            "type": "uri",
                                            "label": "View",
                                            "uri": "https://example.com"
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        ]
    }

    # Send the reply message
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post("https://api.line.me/v2/bot/message/reply", headers=headers, json=reply_message) as response:
            if response.status != 200:
                raise HTTPException(status_code=response.status, detail=await response.text())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
