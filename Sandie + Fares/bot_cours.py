from re import X
import discord
from discord.ext import commands

default_intents = discord.Intents.default()
default_intents.members= True
client = discord.Client(intents=default_intents)


client = commands.Bot(command_prefix="!")





class Node:
    def __init__(self, phrase, keyword, liste_child):
        self.phrase = phrase
        self.keyword = keyword
        self.liste_child = liste_child
    

tree = Node("      As-tu besoin d'un cours ou d'un tuto ?", "aide", [
    Node("     En quoi veux-tu un tuto ?", "tuto", [
        Node("Voici un lien vers un tuto de JS :**https://www.w3schools.com/js/default.asp**", "js", None), 
        Node("Voici un lien vers un tuto de HTML :**https://www.w3schools.com/html/**", "html", None), 
        Node("Voici un lien vers un tuto de CSS :**https://www.w3schools.com/css/default.asp**", "css", None), 
        Node("Voici un lien vers un tuto de PYTHON :**https://www.w3schools.com/python/default.asp**", "python", None), 
        Node("Voici un lien vers un tuto de PHP :**https://www.w3schools.com/php/default.asp**", "php", None)
        ]), 
    Node("     En quoi veux-tu un cours ?", "cours", [
        Node("Voici un lien vers un cours de JS :**https://grafikart.fr/formations/debuter-javascript**", "js", None), 
        Node("Voici un lien vers un cours de HTML :**https://grafikart.fr/formations/html**", "html", None), 
        Node("Voici un lien vers un cours de CSS :**https://grafikart.fr/formations/css**", "css", None), 
        Node("Voici un lien vers un cours de PYTHON :**https://www.youtube.com/watch?v=psaDHhZ0cPs&list=PLMS9Cy4Enq5JmIZtKE5OHJCI3jZfpASbR**", "python", None), 
        Node("Voici un lien vers un cours de PHP :**https://grafikart.fr/formations/php**", "php", None)
        ])
])



liste_users = []

@client.event
async def on_message(message):
    message.content = message.content.lower()
    if message.author == client.user:
        return

    help_channel = client.get_channel(981844037403287635)
    # role = client.get_role(978559990577115167)

    if message.content == "!hello":
        await message.channel.send('Bonjour :smiley: !')




            # version de del sans permission avec les roles

    # if message.content == "!del":    
    #     await message.channel.purge(limit= 5)

    # if message.content.startswith("!del"):
    #     number = int(message.content.split()[1])
    #     testnb = number + 1
    #     await message.channel.purge(limit= testnb)


            # del autoriser seulement au rôle modo


    if message.content.startswith("!del"):
        my_role = message.author.roles
        nb = len(my_role)
        i = 0
        valid_role = 0
        while i < nb:
            if my_role[i].id == 978559990577115167:
                valid_role += 1
            i += 1
        if valid_role == 1 :
            if len(message.content.split()) > 1:
                number = int(message.content.split()[1])
            else:
                number = 5
            testnb = number + 1
            await message.channel.purge(limit= testnb)
        else:
            await message.channel.send("Tu n'as pas la permission d'utiliser cette commande :confused:")



    if message.content == "!command" and message.channel == help_channel :
        await message.channel.send('-> **!hello**\n-> **!command_cours** :\n      commandes pour les cours/tutos\n-> **!del/del nb** :\n      supprimer message (réserver aux modérateurs)')

    if message.content == "!command_cours" and message.channel == help_channel:
        await message.channel.send('-> **aide** :\n     appelle le bot cours\n-> **retour** :\n     retourne à la précédente étape\n-> **reset/stop** :\n     arrête la conversation avec le bot cours')




    #système sauvegarde progressions utilisateurs
    #amélioration possible : créer une classe user

    global liste_users  
  
    user = message.author.id
    on_list = False

    
    for i in range(len(liste_users)):
        if liste_users[i] == user :
            on_list = True

    if on_list == True :
        pass    
    else:
        liste_users.append(user)
        liste_users.append(message.author.mention)
        liste_users.append(0)
        liste_users.append("")
        liste_users.append("")
        liste_users.append(0)

    
    for i in range(len(liste_users)):
        if liste_users[i] == user :
            on_list = True
            user_m = i+1
            user_etape = i+2
            user_etat = i+3
            user_phrase = i+4
            valid_word = i+5


    # bot :

    if "retour" in message.content and message.channel == help_channel:
        if liste_users[user_etape] == 0: 
            return
        elif liste_users[user_etape] == 2:
            liste_users[user_etat] = ""
            liste_users[user_etape] -=1    
            await message.channel.send("->"+liste_users[user_m]+",\n"+liste_users[user_phrase])        
        else:
            liste_users[user_etape] = 0
            liste_users[user_etat] = ""
            liste_users[user_phrase] = ""
            await message.channel.send("-> A bientot "+liste_users[user_m]+", appelle moi de nouveau si tu as besoin d'aide :smiley: !") 

            

    if "reset" in message.content and message.channel == help_channel and liste_users[user_etape] != 0:
        liste_users[user_etape] = 0
        liste_users[user_etat] = ""
        liste_users[user_phrase] = ""
        await message.channel.send("-> A bientot "+liste_users[user_m]+", appelle moi de nouveau si tu as besoin d'aide :smiley: !") 
    if "stop" in message.content and message.channel == help_channel and liste_users[user_etape] != 0:
        liste_users[user_etape] = 0
        liste_users[user_etat] = ""
        liste_users[user_phrase] = ""
        await message.channel.send("-> A bientot "+liste_users[user_m]+", appelle moi de nouveau si tu as besoin d'aide :smiley: !") 




    #demande aide au bot
    if tree.keyword in message.content and message.channel == help_channel and liste_users[user_etape] == 0:
        liste_users[user_etape] += 1
        await message.channel.send("-> Bonjour "+liste_users[user_m]+",\n"+tree.phrase)
    

    #choisi si on veut un cours ou un tuto
    if message.channel == help_channel and liste_users[user_etape] == 1:
        i = 0
        while i < len(tree.liste_child):
            if tree.liste_child[i].keyword in message.content:
                liste_users[user_etape] += 1
                liste_users[user_etat] = tree.liste_child[i]
                liste_users[user_phrase] = tree.phrase
                await message.channel.send("-> Bien "+liste_users[user_m]+",\n"+tree.liste_child[i].phrase)
                return
            
            i += 1

    # on choisit le langage du tuto
    if message.channel == help_channel and liste_users[user_etape] == 2:
        j = 0
        liste_users[valid_word] = 0
        while j < len(liste_users[user_etat].liste_child):
            if liste_users[user_etat].liste_child[j].keyword in message.content:
                liste_users[user_etape] += 1
                liste_users[user_phrase] = liste_users[user_etat].liste_child[j].phrase
                await message.channel.send("-> Voilà "+liste_users[user_m]+",\n"+liste_users[user_etat].liste_child[j].phrase)
                liste_users[valid_word] += 1
            j+= 1
        if liste_users[valid_word] == 0 :
            await message.channel.send("-> Désolé "+liste_users[user_m]+",\n je n'ai rien concernant ce que tu recherches. En revanche je peux t'aider en JS, HTML, CSS, SQL et PHP.")
            


    if liste_users[user_etape] >= 3:
        liste_users[user_etape] = 0
        liste_users[user_etat] = ""
        liste_users[user_phrase] = ""
        liste_users[valid_word] = 0
        await message.channel.send("A bientot "+liste_users[user_m]+", j'espère avoir pu t'aider, refait appel à moi si besoin :smiley: !") 





client.run("token a mettre")










    