import discord
import requests
import mysql.connector

client = discord.Client()

@client.event
async def on_ready():
    print('BOT ONLINE!')
    print(client.user.name)
    print(client.user.id)
    print('-----PR------')

@client.event
async def on_message(message):

    if message.content.lower().startswith('!pubg'):
      try:
        cont = str(message.content[6:]).strip(' ')
        api_key = "API_TOKEN"
        header = {
            "Authorization": "Bearer {}".format(api_key),
            "Accept": "application/vnd.api+json"
        }
        url = "https://api.pubg.com/shards/pc-sa/players?filter[playerNames]={}".format(cont)
        response = requests.get(url, headers=header)
        js = response.json()
        js2 = js['data'][0]
        js3 = js2['id']
        link = "https://api.pubg.com/shards/pc-sa/seasons"
        reponse2 = requests.get(url=link, headers=header)
        jso = reponse2.json()
        jso2 = jso['data'][0]['id']
        link2 = 'https://api.pubg.com/shards/pc-sa/players/{}/seasons/division.bro.official.2018-09'.format(js3)
        response3 = requests.get(link2, headers=header)
        json1 = response3.json()
        json2 = json1['data']['attributes']['gameModeStats']
        json3 = json2['solo']
        json4 = json2['duo']
        json5 = json2['squad']

        PontosSolo = json3['winPoints']
        PontosDuo = json4['winPoints']
        PontosSquad = json5['winPoints']

        KillPSolo = json3['killPoints']
        KillPDuo = json4['killPoints']
        KillPSquad = json5['killPoints']

        PSolo = KillPSolo * 0.2 + PontosSolo
        PSolo4 = int(PSolo)
        PDuo = KillPDuo * 0.2 + PontosDuo
        PDuo4 = int(PDuo)
        PSquad = KillPSquad * 0.2 + PontosSquad
        PSquad4 = int(PSquad)

        bronze = ':third_place:'
        prata = ':second_place:'
        ouro = ':first_place:'

        if PSolo <= 1780:
            Solo = bronze
        elif PSolo >= 2000:
            Solo = ouro
        else:
            Solo = prata

        if PDuo <= 1780:
            Duo = bronze
        elif PDuo >= 2000:
            Duo = ouro
        else:
            Duo = prata

        if PSquad <= 1780:
            Squad = bronze
        elif PSquad >= 2000:
            Squad = ouro
        else:
            Squad = prata


        EmbedPu = discord.Embed(title="PlayerUnknown's Battlegrounds\n"
                                      "Servers SA | TPP | Season 9",
                                description="----------------------\n"
                                            "Player: {}\n"
                                            "----------------------\n"
                                            "Solo\n"
                                            "Partida(s): {}\n"
                                            "Kills Total: {}\n"
                                            "Record Kills em partida: {}\n"
                                            "Kills por Headshot: {}\n"
                                            "Top 10: {}\n"
                                            "Vitórias: {}\n"
                                            "Pontos: {} {}\n"
                                            "----------------------\n"
                                            "Duo\n"
                                            "Partida(s): {}\n"
                                            "Kills: {}\n"
                                            "Assistencias: {}\n"
                                            "Record Kills em partida: {}\n"
                                            "Kills por Headshot: {}\n"
                                            "Top 10: {}\n"
                                            "Vitórias: {}\n"
                                            "Pontos: {} {}\n"
                                            "----------------------\n"
                                            "Squad\n"
                                            "Partida(s): {}\n"
                                            "Kills: {}\n"
                                            "Assistencias: {}\n"
                                            "Record Kills em partida: {}\n"
                                            "Kills por Headshot: {}\n"
                                            "Top 10: {}\n"
                                            "Vitórias: {}\n"
                                            "Pontos: {} {}\n"
                                            "----------------------\n".format(
                                                        cont,
                                                        json3['roundsPlayed'],
                                                        json3['kills'],
                                                        json3['roundMostKills'],
                                                        json3['headshotKills'],
                                                        json3['top10s'],
                                                        json3['wins'],
                                                        PSolo4, Solo,
                                                        json4['roundsPlayed'],
                                                        json4['kills'],
                                                        json4['assists'],
                                                        json4['roundMostKills'],
                                                        json4['headshotKills'],
                                                        json4['top10s'],
                                                        json4['wins'],
                                                        PDuo4, Duo,
                                                        json5['roundsPlayed'],
                                                        json5['kills'],
                                                        json5['assists'],
                                                        json5['roundMostKills'],
                                                        json5['headshotKills'],
                                                        json5['top10s'],
                                                        json5['wins'],
                                                        PSquad4, Squad
                                                                            ))
        EmbedPu.set_author(name=message.author.name, icon_url=message.author.avatar_url)
        EmbedPu.set_footer(text='Developed by: Jacques Jacob | Integrado com API Oficial PUBG®')
        EmbedPu.set_thumbnail(url='https://i2.wp.com/gamerfocus.co/wp-content/uploads/2017/12/PUBG.jpg')
        await client.send_message(message.channel, embed=EmbedPu)

        ######### CONEXAO COM O BANCO DE DADOS MYSQL ##############

        cnx = mysql.connector.connect(user='USER', database='DATABASE', port='3306', host='IP',
                                      password='PASSWORD')

        cursor = cnx.cursor()

        pubg_name = cont
        solo_points = PSolo4
        duo_points = PDuo4
        squad_points = PSquad4

        insert = """
                    INSERT INTO pubgdiscord (pubg_name, solo_points, duo_points, squad_points)
                    VALUES (%s, %s, %s, %s) 
                    ON DUPLICATE KEY UPDATE   
                    solo_points=%s, duo_points=%s, squad_points=%s
                 """

        cursor.execute(insert, (pubg_name, solo_points, duo_points, squad_points, solo_points, duo_points, squad_points))

        cnx.commit()
        cursor.close()
        cnx.close()

        ######### FIM CONEXAO COM O BANCO DE DADOS MYSQL ##############

      except KeyError:
          await client.send_message(message.channel, "Não foi possivel encontrar este jogador! Verifique se o "
                                                     "NickName esta correto!")

client.run('DISCORD_TOKEN')
