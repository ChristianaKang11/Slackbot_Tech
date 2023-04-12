import slack 
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter
env_path=Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

app=Flask(__name__)
slack_event_adapter=SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events',app)

client=slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID=client.api_call("auth.test")['user_id']
#client.chat_postMessage(channel='#test_slackbot_ck',text="hi")
@slack_event_adapter.on('message')

def message(payload):
    event=payload.get('event',{})
    channel_id=event.get('channel')
    user_id=event.get('user')
    text=event.get('text')

    return_txt = parse_message(text)
    if BOT_ID!=user_id:
        client.chat_postMessage(channel='#test_slackbot_ck',text=return_txt)
    
def parse_message(text):
    houses = {"bootynug": "Booty Nuggets",
            "pandas" : "Pandas", 
            "top" : "Top Dogs",
            "step" : "Stepbros",
            "akatsuki": "Akatsuki",
            "subway": "Subway"
        } 
    result = ""
    mentioned_houses = []
    people = []

    for house in houses:
        if house in text:
            mentioned_houses.append(house)
    
    #@ are at end
    ats = text.split(text, "@", 1) [1]
    ats = ats.split("@")
    for at in ats:
        at = at.strip()
        people.append(at)

    num_people = len(people)

    #format final result
    result += "House(s): "
    for house in houses:
        result += house
        result += " "

    result += "\n People: "
    for person in people:
        result += person
        result += " "

    result += f"\n Count: {num_people}"

    return result


if __name__=="__main__":
    app.run(debug=True)
