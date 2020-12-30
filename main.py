import discord #importing the discord library
import os
import requests #impoorting an html request function
import json #importing json to work with api
import random #to ensure bot replies randomly 
from replit import db  #to import the repl database
from keepalive import keep_alive #importing an html client
from dotenv import load_dotenv
import allphrase
from allphrase import *
from greetings import greetings

client = discord.Client()

#making sure that the bot responds
if "responding" not in db.keys():
  db["responding"] = True
#function to collect quotes from external api
def find_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)
#function to enable users to add cheering words
def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]
#function to enable users to delete cheering words
def delete_encouragment(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements
#the event to check if the bot's ready
@client.event
async def on_ready():
  print('{0.user} joined the party!'.format(client))

@client.event
async def on_member_join(member):
  await member.channel.send(f'{member.mention} has joined the server!')


#event when a message is received
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content


  if message.content == '99!':
    response = random.choice(brooklyn_99_quotes)
    await message.channel.send(response)
  if 'suggest me an anime to watch' in message.content.lower():
    response = random.choice(anime_search)
    await message.channel.send(response+' {0.author.mention}'.format(message))

  if 'happy birthday' in message.content.lower():
    await message.channel.send('Happy Birthday! 🎈🎉')
  if 'christmas' in message.content.lower():
    await message.channel.send('Happy Christmas! 🎈🎉')
  if any(word in msg for word in greetings):
    response = random.choice(greetings)
    await message.channel.send(response  + '{0.author.mention}'.format(message))

  if 'how are you?' in message.content.lower():
    k = 'Fine. What about you? {0.author.mention}'.format(message)
    await message.channel.send(k)  
  if msg.startswith('$inspireme'):
    quote = find_quote()
    await message.channel.send(quote + '  {0.author.mention}'.format(message))

  if db["responding"]:
    options = initial
    if "encouragements" in db.keys():
      options = options + db["encouragements"]

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

    if any(word in msg for word in list_2):
      await message.channel.send(random.choice(apex_legend_quotes) + ' {0.author.mention}'.format(message))


  #to let user add new cheer words and add them to db
  if msg.startswith("$newmsg"):
    encouraging_message = msg.split("$newmsg ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")


  #to let user delete cheer word from database
  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragment(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)


  #This is to show a list of cheer words in the db
  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")

keep_alive()
client.run(os.getenv('TOKEN'))

