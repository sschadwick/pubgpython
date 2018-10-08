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
        api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI5MDk4YmRiMC03" \
                  "NzEyLTAxMzYtZjJmMC01Nzc3ZmRiNmJmOTEiLCJpc3MiOiJnYW1lbG9ja2VyI" \
                  "iwiaWF0IjoxNTMzMDU3MDM2LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicH" \
                  "ViZyIsImFwcCI6ImRpc2NvcmRib3RwdWJnIn0.AlPEy2r-Bz86pf3J4jfe6sV" \
                  "SAtcFNbcjRy6h_guniIg"
        header = {
            "Authorization": "Bearer {}".format(api_key),
            "Accept": "application/vnd.api+json"
        }
        url = "https://api.pubg.com/shards/pc-sa/players?filter[playerNames]={}".format(cont)
        response = requests.get(url, headers=header)
        js = response.json()
        js2 = js['data'][0]
        js3 = js2['id']
        link = "https://api.pubg.com/shards/steam/seasons"
        reponse2 = requests.get(url=link, headers=header)
        jso = reponse2.json()
        jso2 = jso['data'][0]['id']
        link2 = 'https://api.pubg.com/shards/steam/players/{}/seasons/division.bro.official.pc-2018-01'.format(js3)
        response3 = requests.get(link2, headers=header)
        json1 = response3.json()
        json2 = json1['data']['attributes']['gameModeStats']
        json3 = json2['solo']
        json4 = json2['duo']
        json5 = json2['squad']

#        PontosSolo = json3['winPoints']
#        PontosDuo = json4['winPoints']
#        PontosSquad = json5['winPoints']

#        KillPSolo = json3['killPoints']
#        KillPDuo = json4['killPoints']
#        KillPSquad = json5['killPoints']

        rankPSolo = json3['rankPoints']
        rankPSolo = int(rankPSolo)
        rankPDuo = json4['rankPoints']
        rankPDuo = int(rankPDuo)
        rankPSquad = json5['rankPoints']
        rankPSquad = int(rankPSquad)

#        PSolo = KillPSolo * 0.2 + PontosSolo
#        PSolo4 = int(PSolo)
#        PDuo = KillPDuo * 0.2 + PontosDuo
#        PDuo4 = int(PDuo)
#        PSquad = KillPSquad * 0.2 + PontosSquad
#        PSquad4 = int(PSquad)

        bronze = ':third_place:'
        prata = ':second_place:'
        ouro = ':first_place:'

        if rankPSolo <= 1780:
            Solo = bronze
        elif rankPSolo >= 2000:
            Solo = ouro
        else:
            Solo = prata

        if rankPDuo <= 1780:
            Duo = bronze
        elif rankPDuo >= 2000:
            Duo = ouro
        else:
            Duo = prata

        if rankPSquad <= 1780:
            Squad = bronze
        elif rankPSquad >= 2000:
            Squad = ouro
        else:
            Squad = prata


        EmbedPu = discord.Embed(title="PlayerUnknown's Battlegrounds\n"
                                      "Servers WW | TPP | New Season 1",
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
                                                        rankPSolo, Solo,
                                                        json4['roundsPlayed'],
                                                        json4['kills'],
                                                        json4['assists'],
                                                        json4['roundMostKills'],
                                                        json4['headshotKills'],
                                                        json4['top10s'],
                                                        json4['wins'],
                                                        rankPDuo, Duo,
                                                        json5['roundsPlayed'],
                                                        json5['kills'],
                                                        json5['assists'],
                                                        json5['roundMostKills'],
                                                        json5['headshotKills'],
                                                        json5['top10s'],
                                                        json5['wins'],
                                                        rankPSquad, Squad
                                                                            ))
        EmbedPu.set_author(name=message.author.name, icon_url=message.author.avatar_url)
        EmbedPu.set_footer(text='Developed by: Jacques Jacob | Integrado com API Oficial PUBG®')
        EmbedPu.set_thumbnail(url='https://i2.wp.com/gamerfocus.co/wp-content/uploads/2017/12/PUBG.jpg')
        await client.send_message(message.channel, embed=EmbedPu)

        ######### CONEXAO COM O BANCO DE DADOS MYSQL ##############

        cnx = mysql.connector.connect(user='pubgdiscordpy', database='pubg_discord_db', port='3306', host='db4free.net',
                                      password='Jacs1139')

        cursor = cnx.cursor()

        pubg_name = cont
        solo_points = rankPSolo
        duo_points = rankPDuo
        squad_points = rankPSquad

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

client.run('NDczNTYxODU0MjEyNDQwMDY0.DkEBaA.yd3K3oLSozWMyBMvCbj5qFAYpCM')
