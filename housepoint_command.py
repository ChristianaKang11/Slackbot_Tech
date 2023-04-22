import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

load_dotenv()
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]

app = App(token=SLACK_BOT_TOKEN)

def handle_housepoints("#test_slackbot"):
    # Acknowledge the command received
    ack()

    # Add your logic to calculate or retrieve house points
    house_points = {
        "Pandas": 1,
        "Booty Nuggets": 1,
        "Top Dogs": 1,
        "Stepbros": 1,
        "Akatsuki":1,
        "Subway":1
    }

    # Format the message
    message = "House Points:\n"
    for house, points in house_points.items():
        message += f"{house}: {points}\n"

    # Post the message in the channel where the command was used
    app.client.chat_postMessage(channel="#test_slackbot", text=message)

@app.command("/housepoints")
def handle_housepoints(ack, body, logger):
    # Acknowledge the command received
    ack()

    # Run the rest of the logic asynchronously
    thread = Thread(target=post_house_points, args=(body['#test_slackbot'],))
    thread.start()

if __name__ == "__main__":
    handler = SocketModeHandler(app, "SLACK_APP_TOKEN")
    handler.start()