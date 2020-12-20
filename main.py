import discord 
import os 
import requests
import json 
import random 
from replit import db

#discord.py library is used in this project. 
#os provides a portable way of using operating system dependent functionality
#requests allows us to request from http stuff
#json JSON is a lightweight format for storing and transporting data, often used when data is sent from a server to a web page

client = discord.Client()
sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"] #a list of sad words, if the bot sees one, it will respond
starter_encouragements = ['cheer up!', "Hang in there.", "You are better than what you think you are!"]

if "responding" not in db.keys():
  db["responding"] = True

#request quote from api
def get_quote(): 
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

#update encouragement list
def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db['encouragements']
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

#register library 
#A callback function is a function passed into another function as an argument, which is then invoked inside the outer function to complete some kind of routine or action.
@client.event 
async def on_ready():
  print("we have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return 

  msg = message.content
  if msg.startswith('$hello'):
    await message.channel.send('Hello!')

  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + db["encouragements"]

    #check if it has any of the words in the sadwords list
    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ", 1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith('$del'):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del", 1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith('$lists'):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$responding"):
    val = msg.split("$responding ", 1)[1]

    if val.lower() == "true":
      db["responding"] = True
      await message.channel.send("responding is on")
    else:
      db["responding"] = False
      await message.channel.send("responding is off")

client.run(os.getenv('TOKEN'))
