import discord

client = discord.Client()

@client.event
async def on_ready():
    print('BOT ONLINE!')
    print(client.user.name)
    print(client.user.id)
    print('-----PR------')

palavrao = ["caralho", "filho da puta", "porra", "pqp", "puta queu pariu", "se foder", "foder", "viado", "bicha", "tomar no cu", "cacete", "cassete"] #pode colocar varios, somente continuar a lista

@client.event
async def on_message(message):
    for palavra in palavrao:
        if palavra in message.content.lower():
            return await client.delete_message(message), await client.send_message(message.channel, message.author.mention +", você não pode falar isso aqui cara.")

client.run('DISCORD_TOKEN')
