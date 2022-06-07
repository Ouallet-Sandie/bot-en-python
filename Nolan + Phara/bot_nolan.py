from ast import Str
import discord
from discord.ext import commands
from random import randint
import random
import math
from discord_components import DiscordComponents, ComponentsBot, Button, SelectOption, Select


client = commands.Bot(command_prefix="=")
DiscordComponents(client)

message_aide = "``` Liste des commandes \n \n Sur tous les channels \n =clear nombre, pour supprimer le nombre de message que vous voulez \n =moderator, pour appeler les modérateurs \n =mathadd chiffre1 chiffre2, pour addition 2 chiffres \n =mathsub chiffre1 chiffre2, pour soustraire 2 chiffres \n =mathdiv chiffre1 chiffre2, pour diviser 2 chiffres \n =mathmult chiffre1 chiffre2, pour multiplier 2 chiffres \n =mathsqrt chiffre, pour obtenir la racine carré d'un chiffre \n =mathrando nombre1 nombre2, pour obtenir un nombre entre les 2 nombres entrés \n \n Channel tictactoe \n =tictactoe @joueur1 @joueur2, pour lancer une partie de tic tac toe \n =place numéro de la case, pour placer sa marque \n \n Channel joke \n =joke, pour avoir une blague/devinette \n =give_blague, pour connaitre la réponse de la blague/devinette \n =answer reponse, pour essayer de trouver la réponse \n =indice 1 ou =indice 2, pour avoir un indice sur la blague/devinette \n \n Channel pendu \n =pendu facile/moyen/difficile pour lancer un pendu \n =try_letter lettre, pour essayer de trouver une lettre \n =try_mot mot, pour essayer de trouver le mot \n =give_pendu, pour connaitre la réponse \n \n Channel plus ou moins \n =more_less minimum maximum, pour lancer une partie de plus ou moins \n =try_more_less nombre, pour tenter de trouver la réponse \n =give_more_less, pour connaitre la réponse \n \n Channel tu preferes \n =tu_preferes, pour lancer un tu préfères \n =je_prefere 1 ou =je_prefere 2, pour choisir la réponse \n =stop_prefere, pour arreter le tu preferes```"

@client.command()
async def commandes(ctx):
    await ctx.send(message_aide)

@client.command()
async def moderator(ctx):
    moderator = discord.utils.get(ctx.guild.roles, id=978559990577115167)
    await ctx.send(f'{moderator.mention}')

@client.command()
async def clear(ctx, amount=5):
	await ctx.channel.purge(limit=amount)

# ----------------------------------------------- TIC TAC TOE ----------------------------------------------- #

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

# tableau des possibilité de win
winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

# fonction pour lancer le jeu
@client.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    if ctx.channel.id == 980060663462391839:
        # recupere les variables qui sont en dehors de la fonction
        global count
        global player1
        global player2
        global turn
        global gameOver

        if gameOver:
            global board
            board = [
                        ":white_large_square:", ":white_large_square:", ":white_large_square:",
                        ":white_large_square:", ":white_large_square:", ":white_large_square:",
                        ":white_large_square:", ":white_large_square:", ":white_large_square:"
                    ]
            turn = ""
            gameOver = False
            count = 0

            player1 = p1
            player2 = p2

            # affiche le tableau
            line = ""
            for x in range(len(board)):
                # si c'est la case 2 5 ou 8 ca saute une ligne
                if x == 2 or x == 5 or x == 8:
                    line += " " + board[x]
                    await ctx.send(line)
                    line = ""
                else:
                    line += " " + board[x]

            # determine qui sera le premier a jouer
            num = random.randint(1, 2)
            # passe la variable turn sur la personne qui doit jouer et la mentionne
            if num == 1:
                turn = player1
                await ctx.send("c'est le tour de <@" + str(player1.id) + ">")
            elif num == 2:
                turn = player2
                await ctx.send("c'est le tour de <@" + str(player2.id) + ">")
        # Demande aux utilisateurs de finir leur partie avant d'en commencer une autre
        else:
            await ctx.send("il y a deja une partie en cours")
    else :
        await ctx.send("cette commande marche que dans le channel tictactoe")

# fonction pour placer les markeur
@client.command()
async def place(ctx, pos: int):
    if ctx.channel.id == 980060663462391839:
        # recupere les variables qui sont en dehors de la fonction
        global turn
        global player1
        global player2
        global board
        global count
        global gameOver

        if not gameOver:
            mark = ""
            if turn == ctx.author:
                # change le markeur en fonction du tour de la personne qui doit jouer
                if turn == player1:
                    mark = ":regional_indicator_x:"
                elif turn == player2:
                    mark = ":o2:"
                # verifie si c bien entre 1 et 9 et si c'est pas déjà remplie
                if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                    # si c'est pas remplie ca remplace le carré blanc par le markeur de la personne qui a jouer
                    board[pos - 1] = mark
                    count += 1

                    # affiche le tableau
                    line = ""
                    for x in range(len(board)):
                        # si c'est la case 2 5 ou 8 ca saute une ligne
                        if x == 2 or x == 5 or x == 8:
                            line += " " + board[x]
                            await ctx.send(line)
                            line = ""
                        else:
                            line += " " + board[x]

                    # verifie si quelqu'un a gagné
                    checkWinner(winningConditions, mark)
                    print(count)
                    # si quelqu'un a gagné, ca met le markeur + win
                    if gameOver == True:
                        await ctx.send(mark + " a gagné")
                    # si count est > 9 et que personne a gagné c'est une égalité
                    elif count >= 9:
                        gameOver = True
                        await ctx.send("Egalité")

                    # si c'était le tour de la personne 1 c'est a la personne 2 de jouer et inversement
                    if turn == player1:
                        turn = player2
                    elif turn == player2:
                        turn = player1
                # verifie si l'utilisateur entre bien un chiffre entre 1 et 9 et si c'est pas déjà rempli d'un signe
                else:
                    await ctx.send("Il faut choisir un chiffre entre 1 et 9 et une case pas déjà rempli")
            # envoie ce message a l'utilisateur si c'est pas a son tour de jouer
            else:
                await ctx.send("Ce n'est pas ton tour")
        # demande de lancer une nouvelle partie a l'utilisateur
        else:
            await ctx.send("Lance une nouvelle partie avec =tictactoe")
    else :
        await ctx.send("cette commande marche que dans le channel tictactoe")

# fonction pour verifier qui est le gagnant
def checkWinner(winningConditions, mark):
    global gameOver
    # parcours tout le tableau winningConditions
    for condition in winningConditions:
        # si une des lignes du tableau est rempli du meme signe le partie se fini
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

# fonction pour gerer les erreurs lors de la creation du jeu
@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    # verifie si la personne a bien mentionner 2 utilisateurs
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Mentionne 2 personnes")
    # envoie un message d'erreur si la personne a mal mentionner
    elif isinstance(error, commands.BadArgument):
        await ctx.send("La mention n'est pas bonne")

# fonction pour gerer les erreurs lors du placement
@place.error
async def place_error(ctx, error):
    # si la personne a oublié de préciser la position de la case ou il veut jouer
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Precise la case ou tu veux placer ton markeur")
    # si l'utilisateur n'entre pas un chiffre
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Entre un chiffre")

# ----------------------------------------------- TIC TAC TOE ----------------------------------------------- #

# ------------------------------------------------- BLAGUES ------------------------------------------------- #

blagues = [
    ["Pourquoi Harry Potter chuchotte","par ce que Dumbledore","Une personne dort","Directeur de Poudlard"],
    ["Qu'est ce qui est transparent et qui cours dans un champ","un troupeau de vitre","Un troupeau de ...","il y en a 2 a l'avant et 2 a l'arriere d'une voiture"],
    ["Qu'est ce qui est jaune et qui attend","jonathan","C'est un prenom","Il faut lier 2 mots"]
]

reponse = ""
question = ""
blague_aleatoire = 0

# fonction pour lancer une blague
@client.command()
async def joke(ctx):
    if ctx.channel.id == 978573528297250817:
        # recupere les variables qui sont en dehors de la fonction
        global blagues
        global reponse
        global question
        global blague_aleatoire

        # si il y a deja une blague en cours ca previent l'utilisateur
        if question != "" :
            await ctx.send("Il y a déjà une blague en cours, trouvez la réponse ou entre =give_blague pour obtenir la réponse")
        # envoie une blague a l'utilisateur
        else :
            blague_aleatoire = randint(0,len(blagues) - 1)
            question = blagues[blague_aleatoire][0]
            reponse = blagues[blague_aleatoire][1]
            await ctx.send(question)
    else :
        await ctx.send("cette commande marche que dans le channel joke")

# fonction pour demander la reponse
@client.command()
async def give_blague(ctx):
    if ctx.channel.id == 978573528297250817:
        # recupere les variables qui sont en dehors de la fonction
        global blagues
        global reponse
        global question
        global blague_aleatoire

        # si il n y a pas de blague en cours ca previent l'utilisateur
        if question == "":
            await ctx.send("vous devez d'abord utiliser la commande !joke pour avoir une blague")
        # envoie la reponse
        else :
            await ctx.send(reponse)
            reponse = ""
            question = ""
    else :
        await ctx.send("cette commande marche que dans le channel joke")

# fonction pour essayer de trouver la blague
@client.command()
async def answer(ctx, *args):
    if ctx.channel.id == 978573528297250817:
        # recupere les variables qui sont en dehors de la fonction
        global blagues
        global reponse
        global question
        global blague_aleatoire
        sentence = ""
        i = 0
        # recpuere tous les mots que l'utilisateur a entré après la commande answer
        for words in args :
            i = i + 1
            # met tous les mots les uns a la suite des autres avec un espace entre chaque mots
            sentence = sentence + words
            # si c'est le dernier mot ce ne met pas d'espace
            if i < len(args) :
                sentence = sentence + " "

        # si il n y a pas de blague en cours ca previent l'utilisateur
        if question == "":
            await ctx.send("vous devez d'abord utiliser la commande !joke pour avoir une blague")
        # compare la reponse de l'utilisateur a la reponse de la blague
        elif sentence == reponse :
            await ctx.send("Bravo tu as trouvé la réponse")
            reponse = ""
            question = ""
        else :
            await ctx.send("Essaye encore ou entre !give_blague")
    else :
        await ctx.send("cette commande marche que dans le channel joke")

@client.command()
async def indice(ctx, num_indice : int):
    if ctx.channel.id == 978573528297250817:
        # recupere les variables qui sont en dehors de la fonction
        global blagues
        global reponse
        global question
        global blague_aleatoire
        # si il n y a pas de blague en cours ca previent l'utilisateur
        if question == "":
            await ctx.send("vous devez d'abord utiliser la commande !joke pour avoir une blague")
        # si il entre indice 1
        elif num_indice == 1 :
            await ctx.send(blagues[blague_aleatoire][2])
        # si il entre indice 2
        elif num_indice == 2 :
            await ctx.send(blagues[blague_aleatoire][3])
        # sinon ca dit a l'utilisateur ce qu'il doit entrer
        else :
            await ctx.send("Entrez !indice 1 ou !indice 2 selon l'indice que vous voulez")
    else :
        await ctx.send("cette commande marche que dans le channel joke")

# ------------------------------------------------- BLAGUES ------------------------------------------------- #

# -------------------------------------------------- PENDU -------------------------------------------------- #

pendu_facile = ["chat","bleu","vert","moto"]
pendu_moyen = ["oiseau","joyaux","joueur","lettre"]
pendu_difficile = ["baguette","elephant","tracteur","vehicule"]

letter_versus_emoji = [
    ["a",":regional_indicator_a:"],
    ["b",":regional_indicator_b:"],
    ["c",":regional_indicator_c:"],
    ["d",":regional_indicator_d:"],
    ["e",":regional_indicator_e:"],
    ["f",":regional_indicator_f:"],
    ["g",":regional_indicator_g:"],
    ["h",":regional_indicator_h:"],
    ["i",":regional_indicator_i:"],
    ["j",":regional_indicator_j:"],
    ["k",":regional_indicator_k:"],
    ["l",":regional_indicator_l:"],
    ["m",":regional_indicator_m:"],
    ["n",":regional_indicator_n:"],
    ["o",":regional_indicator_o:"],
    ["p",":regional_indicator_p:"],
    ["q",":regional_indicator_q:"],
    ["r",":regional_indicator_r:"],
    ["s",":regional_indicator_s:"],
    ["t",":regional_indicator_t:"],
    ["u",":regional_indicator_u:"],
    ["v",":regional_indicator_v:"],
    ["w",":regional_indicator_w:"],
    ["x",":regional_indicator_x:"],
    ["y",":regional_indicator_y:"],
    ["z",":regional_indicator_z:"],
    ["-",":blue_square:"]
]

essai_versus_image = [
    [1,'essai_1.PNG'],
    [2,'essai_2.PNG'],
    [3,'essai_3.PNG'],
    [4,'essai_4.PNG'],
    [5,'essai_5.PNG'],
    [6,'essai_6.PNG'],
    [7,'essai_7.PNG'],
    [8,'essai_8.PNG'],
    [9,'essai_9.PNG'],
    [10,'essai_10.PNG'],
    [11,'essai_11.PNG'],
    [12,'essai_12.PNG']
]

mot_a_trouver = ""
mot_en_recherche = ""
essais = 0

# fonction pour lancer le pendu
@client.command()
async def pendu(ctx, difficulte = ""):
    # verifie si l'utilisateur est bien dans le canal pendu
    if ctx.channel.id == 980124791652646972:
        global pendu_facile
        global pendu_moyen
        global pendu_difficile
        global mot_aleatoire
        global mot_a_trouver
        global mot_en_recherche
        global essais
        global essai_versus_image
        # si l'utilisateur n'a pas lancer le jeu alors ca le lance
        if mot_a_trouver == "" :
            # si il a choisis facile alors ca prend un mot aleatoire dans le tableau facile
            if difficulte == "facile":
                mot_aleatoire = randint(0,len(pendu_facile) - 1)
                mot_a_trouver = pendu_facile[mot_aleatoire]
                mot_en_recherche = "----"
            # si il a choisis moyen alors ca prend un mot aleatoire dans le tableau moyen
            elif difficulte == "moyen":
                mot_aleatoire = randint(0,len(pendu_moyen) - 1)
                mot_a_trouver = pendu_moyen[mot_aleatoire]
                mot_en_recherche = "------"
            # si il a choisis difficile alors ca prend un mot aleatoire dans le tableau difficile
            elif difficulte == "difficile":
                mot_aleatoire = randint(0,len(pendu_difficile) - 1)
                mot_a_trouver = pendu_difficile[mot_aleatoire]
                mot_en_recherche = "--------"
            # si il a pas entré de difficulté ou une mauvaise difficulté, ca lui explique ce qu'il doit faire
            else :
                await ctx.send("Il faut choisir une difficulté entre facile/moyen/difficile")
                return
            # affiche le mot qui est en train d'etre recherché ( 4 cases vides pour le moment ) et affiche les commandes qu'il doit utiliser
            mot_letter_to_emoji = letter_to_emoji(mot_en_recherche)
            await ctx.send("Entrez =try_letter avec la lettre que vous voulez derriere ou =try_word avec le mot que vous voulez derriere, si vous voulez la reponse tapez : =give_pendu")
            await ctx.send(mot_letter_to_emoji)
            essais = 0
        # si il a deja une partie en cours ca le previent
        else :
            await ctx.send("Il y a deja un pendu en cours, finissez le ou entrez =give_pendu pour avoir la reponse et pouvoir lancer une nouvelle partie")
    # si l'utilisateur est dans le mauvais canal ca le previent
    else :
        await ctx.send("cette commande marche que dans le channel pendu")

# fonction pour tenter une lettre
@client.command()
async def try_letter(ctx, letter = ""):
    # verifie si l'utilisateur est bien dans le canal pendu
    if ctx.channel.id == 980124791652646972:
        global mot_aleatoire
        global mot_a_trouver
        global mot_en_recherche
        global essais
        global essai_versus_image

        image = ""
        # si il y a pas de partie en cours ca previent l'utilisateur qu'il ne peut pas utiliser cette commande
        if mot_a_trouver == "" :
            await ctx.send("Vous devez lancer une partie avant de pouvoir utiliser cette commande")
        else :
            # si l'utilisateur n'a pas entré de lettre ca le previent
            if letter == "":
                await ctx.send("Vous devez d'abord entrer une lettre")
            # si l'utilisateur a entré plus d'une lettre ca le previent
            elif len(letter) > 1 :
                await ctx.send("Vous devez entrer une seule lettre")
            else :
                # passe les 2 listes en tableau
                list_mot_a_trouver = list(mot_a_trouver)
                list_mot_en_recherche = list(mot_en_recherche)
                lettre_trouvees = 0
                # verifie si la lettre est dans la liste du mot a trouver
                for i in range(len(list_mot_a_trouver)) :
                    # si elle est dans la liste du mot a trouver ça l'ajoute dans la liste du mot qui est en train d'etre cherché
                    if list_mot_a_trouver[i] == letter :
                        list_mot_en_recherche[i] = letter
                        lettre_trouvees = lettre_trouvees + 1
                # convertis la liste du mot en recherche en chaine de caractere
                str_mot_en_recherche = ''.join(list_mot_en_recherche)
                mot_en_recherche = str_mot_en_recherche
                # si le joueur a trouvé toutes les lettres il a gagné
                if mot_en_recherche == mot_a_trouver :
                    await ctx.send("bien joué le mot à trouver était bien :")
                    mot_letter_to_emoji = letter_to_emoji(mot_a_trouver)
                    await ctx.send(mot_letter_to_emoji)
                    mot_a_trouver = ""
                else :
                    # si il a trouvé 0 lettre il a utilisé un essai
                    if lettre_trouvees == 0 :
                        essais = essais + 1
                    # si il est a 12 essai, il a perdu, ca met l'image du pendu du dernier essai et ca envoie le mot qu'il fallait trouver
                    if essais == 12 :
                        await ctx.send("Tu as perdu")
                        await ctx.send(file=discord.File('essai_12.PNG'))
                        await ctx.send("Le mot à trouver était :")
                        mot_letter_to_emoji = letter_to_emoji(mot_a_trouver)
                        await ctx.send(mot_letter_to_emoji)
                        mot_a_trouver = ""
                        return
                    # parcours le tableau avec la correspondance image - essai et attribu a la variable image, l'image de l'essai ou l'utilisateur en est
                    for i in range(len(essai_versus_image)):
                        if essais == essai_versus_image[i][0]:
                            image = essai_versus_image[i][1]
                    # affiche l'image du pendu correspondant au nombre d'essai
                    await ctx.send(file=discord.File(image))
                    # affiche l'avancé du mot qui est en train d'etre recherché
                    mot_letter_to_emoji = letter_to_emoji(mot_en_recherche)
                    await ctx.send(mot_letter_to_emoji)
    # si l'utilisateur est dans le mauvais canal ca le previent
    else :
        await ctx.send("cette commande marche que dans le channel pendu")

# fonction pour tenter un mot
@client.command()
async def try_word(ctx, word = ""):
    # verifie si l'utilisateur est bien dans le canal pendu
    if ctx.channel.id == 980124791652646972:
        global mot_aleatoire
        global mot_a_trouver
        global mot_en_recherche
        global essais
        global essai_versus_image

        image = ""
        # si il y a pas de partie en cours ca previent l'utilisateur qu'il ne peut pas utiliser cette commande
        if mot_a_trouver == "" :
            await ctx.send("Vous devez lancer une partie avant de pouvoir utiliser cette commande")
        else :
            #si l'utilisateur a trouvé la bonne reponse ca le previent, ca envoie le mot qu'il fallait trouvé et ca met la variable vide pour pouvoir lancer une nouvelle partie
            if word == mot_a_trouver :
                await ctx.send("bien joué le mot à trouver était bien :")
                mot_letter_to_emoji = letter_to_emoji(mot_a_trouver)
                await ctx.send(mot_letter_to_emoji)
                mot_a_trouver = ""
            else :
                essais = essais + 1
                # si il est a 12 essai, il a perdu, ca met l'image du pendu du dernier essai et ca envoie le mot qu'il fallait trouver
                if essais == 12 :
                    await ctx.send("Tu as perdu")
                    await ctx.send(file=discord.File('essai_12.PNG'))
                    await ctx.send("Le mot à trouver était :")
                    mot_letter_to_emoji = letter_to_emoji(mot_a_trouver)
                    await ctx.send(mot_letter_to_emoji)
                    mot_a_trouver = ""
                    return
                # parcours le tableau avec la correspondance image - essai et attribu a la variable image, l'image de l'essai ou l'utilisateur en est
                for i in range(len(essai_versus_image)):
                    if essais == essai_versus_image[i][0]:
                        image = essai_versus_image[i][1]
                # affiche l'image du pendu correspondant au nombre d'essai
                await ctx.send(file=discord.File(image))
                # affiche l'avancé du mot qui est en train d'etre recherché
                mot_letter_to_emoji = letter_to_emoji(mot_en_recherche)
                await ctx.send(mot_letter_to_emoji)
    # si l'utilisateur est dans le mauvais canal ca le previent
    else :
        await ctx.send("cette commande marche que dans le channel pendu")

# fonction pour connaitre la reponse
@client.command()
async def give_pendu(ctx):
    # verifie si l'utilisateur est bien dans le canal pendu
    if ctx.channel.id == 980124791652646972:
        global mot_aleatoire
        global mot_a_trouver
        global mot_en_recherche
        global essais
        global essai_versus_image
        # si il y a pas de partie en cours ca previent l'utilisateur qu'il ne peut pas utiliser cette commande
        if mot_a_trouver == "" :
            await ctx.send("Vous devez lancer une partie avant de pouvoir utiliser cette commande")
        # envoie le mot qui etait a trouvé
        else :
            await ctx.send("Le mot à trouver était :")
            # transforme le mot en emoji
            mot_letter_to_emoji = letter_to_emoji(mot_a_trouver)
            await ctx.send(mot_letter_to_emoji)
            # remet la varialbe vide pour pouvoir lancer une nouvelle partie
            mot_a_trouver = ""
    # si l'utilisateur est dans le mauvais canal ca le previent
    else :
        await ctx.send("cette commande marche que dans le channel pendu")

# fonction pour transformer un mot en mot avec des lettres emoji
def letter_to_emoji(mot_a_convertir):
    global letter_versus_emoji
    # transforme le mot a convertire en liste
    mot_a_convertir_list = list(mot_a_convertir)
    # parcours le mot a convertire
    for i in range(len(mot_a_convertir_list)):
        # parcours le tableau avec la correspondance lettre - emoji
        for j in range(len(letter_versus_emoji)):
            # remplace la lettre par un emoji
            if mot_a_convertir_list[i] == letter_versus_emoji[j][0]:
                mot_a_convertir_list[i] = letter_versus_emoji[j][1]
    # renvoie le mot avec les emoji en string
    mot_convertis = ' '.join(mot_a_convertir_list)
    return mot_convertis

# -------------------------------------------------- PENDU -------------------------------------------------- #

# ---------------------------------------------- PLUS OU MOINS ---------------------------------------------- #

max = 0
min = 0
more_less_aleatoire = 0

numbre_versus_emoji = [
    ["0",":zero:"],
    ["1",":one:"],
    ["2",":two:"],
    ["3",":three:"],
    ["4",":four:"],
    ["5",":five:"],
    ["6",":six:"],
    ["7",":seven:"],
    ["8",":eight:"],
    ["9",":nine:"]
]

# fonction pour lancer le jeu plus ou moins
@client.command()
async def more_less(ctx, nombre_1 = 0, nombre_2 = 0):
    global max
    global min
    global more_less_aleatoire
    # verifie si l'utilisateur est bien dans le canal plus ou moins
    if ctx.channel.id == 980407531623030954:
        # si il y a déjà une partie en cours
        if more_less_aleatoire != 0 :
            await ctx.send("Il y a déjà une partie en cours, finissez la partie ou entrez =give_more_less pour connaitre la réponse et pouvoir commencer une nouvelle partie")
        else :
            # si les nombres sont pas entre 1 et 999 999
            if nombre_1 > 999999 or nombre_1 < 1 or nombre_2 > 999999 or nombre_2 < 1:
                await ctx.send("Il faut choisir deux nombres entre 1 et 999 999, par exemple =more_less 1 999 donnera un nombre entre 1 et 999")
            # si les deux nombres sont pareils
            elif nombre_1 == nombre_2 :
                await ctx.send("Il faut choisir deux nombres différents")
            else :
                # determine qui sera le minimum et qui sera le maximum
                if nombre_2 > nombre_1 :
                    max = nombre_2
                    min = nombre_1
                else :
                    min = nombre_2
                    max = nombre_1
                more_less_aleatoire = randint(min,max)
                await ctx.send("Bonne chance, entre =try_more_less et le nombre que tu veux pour trouver la réponse")
    # si l'utilisateur est dans le mauvais canal ca le previent
    else :
        await ctx.send("Cette commande marche que dans le channel plus ou moins")

# fonction pour essayer de trouver le nombre
@client.command()
async def try_more_less(ctx, reponse = 0):
    global max
    global min
    global more_less_aleatoire
    # verifie si l'utilisateur est bien dans le canal plus ou moins
    if ctx.channel.id == 980407531623030954:
        # si il n y a pas de partie en cours
        if more_less_aleatoire == 0 :
            await ctx.send("Il faut lancer une partie avec =more_less avant de pouvoir utiliser cette commande")
        else :
            # si il entre un nombre plus haut ou plus bas que le max et le min
            if reponse < min or reponse > max :
                await ctx.send("Il faut que votre réponse soit entre les 2 nombres que vous avez entrer au début de la partie")
            else :
                # si la reponse est plus haute que le nombre a trouver
                if reponse > more_less_aleatoire :
                    await ctx.send(":regional_indicator_m: :regional_indicator_o: :regional_indicator_i: :regional_indicator_n: :regional_indicator_s:")
                # si la reponse est plus basse que le nombre a trouver
                elif reponse < more_less_aleatoire :
                    await ctx.send(":regional_indicator_p: :regional_indicator_l: :regional_indicator_u: :regional_indicator_s:")
                # si la reponse est la meme que le nombre a trouver
                else :
                    await ctx.send(":regional_indicator_b: :regional_indicator_r: :regional_indicator_a: :regional_indicator_v: :regional_indicator_o:")
                    await ctx.send("Le nombre à trouver était bien")
                    more_less_aleatoire_to_emoji = number_to_emoji(more_less_aleatoire)
                    await ctx.send(more_less_aleatoire_to_emoji)
                    more_less_aleatoire = 0
    # si l'utilisateur est dans le mauvais canal ca le previent
    else :
        await ctx.send("Cette commande marche que dans le channel plus ou moins")

# fonction pour connaitre la reponse
@client.command()
async def give_more_less(ctx):
    global max
    global min
    global more_less_aleatoire
    # verifie si l'utilisateur est bien dans le canal plus ou moins
    if ctx.channel.id == 980407531623030954:
        # si il n y a pas de partie en cours
        if more_less_aleatoire == 0 :
            await ctx.send("Il faut lancer une partie avec =more_less avant de pouvoir utiliser cette commande")
        # donne la reponse et fini la partie
        else :
            await ctx.send("La réponse était")
            more_less_aleatoire_to_emoji = number_to_emoji(more_less_aleatoire)
            await ctx.send(more_less_aleatoire_to_emoji)
            more_less_aleatoire = 0
    # si l'utilisateur est dans le mauvais canal ca le previent
    else :
        await ctx.send("Cette commande marche que dans le channel plus ou moins")

# convertir un nombre en emoji
def number_to_emoji(nombre_a_convertir):
    global numbre_versus_emoji
    # transforme le nombre en str ("40")
    str_nombre_a_convertir = str(nombre_a_convertir)
    # transforme le nombre en liste (["4","0"])
    nombre_a_convertir_list = list(str_nombre_a_convertir)
    # parcours le tableau avec le nombre
    for i in range(len(nombre_a_convertir_list)):
        # parcours le tableau avec la correspondance chiffre emoji
        for j in range(len(numbre_versus_emoji)):
            # si le nombre correspond a un emoji ca remplace le nombre par un emoji
            if nombre_a_convertir_list[i] == numbre_versus_emoji[j][0]:
                nombre_a_convertir_list[i] = numbre_versus_emoji[j][1]
    # renvoie le nombre transformé en emoji
    nombre_convertis = ' '.join(nombre_a_convertir_list)
    return nombre_convertis

# ---------------------------------------------- PLUS OU MOINS ---------------------------------------------- #

# ----------------------------------------------- TU PREFERES ----------------------------------------------- #

all_tu_preferes = [
    ["manger une limasse","manger un escargot",[],0,0],
    ["manger des crottes de nez","manger des cires d'oreille",[],0,0],
    ["perdre tes mains","perdre tes pieds",[],0,0],
    ["mourir bruler","mourir noyer",[],0,0]
]

tu_preferes_aleatoire = ""
liste_a_faire = []
tu_preferes_on_off = "off"

# fonction pour lancer un tu preferes
@client.command()
async def tu_preferes(ctx):
    global all_tu_preferes
    global user_tu_preferes
    global liste_a_faire
    global tu_preferes_on_off

    user_tu_preferes = ctx.author.id
    liste_a_faire = []

    # verifie si l'utilisateur est bien dans le tu preferes
    if ctx.channel.id == 980145249005494293:
        # si il y a deja une partie en cours
        if tu_preferes_on_off == "on" :
            await ctx.send("Il y a déjà une partie en cours")
        else :
            # ajoute toutes les questions possibles dans un tableau
            for i in range(len(all_tu_preferes)) :
                liste_a_faire.append(i)

            # supprime les questions du tableau aux quelles l'utilisateur a déjà repondu
            for i in range(len(all_tu_preferes)) :
                if user_tu_preferes in all_tu_preferes[i][2] :
                    liste_a_faire.remove(i)
            
            # si l'utilisateur a déjà repondu a toutes les questions
            if len(liste_a_faire) == 0 :
                await ctx.send("Vous avez déjà répondu a toutes les questions, d'autres questions seront bientot disponible")
            # donne une question aleatoire a l'utilisateur
            else :
                random.shuffle(liste_a_faire)
                await ctx.send(liste_a_faire)
                await ctx.send("Tu préfères")
                await ctx.send(f"réponse 1 {all_tu_preferes[liste_a_faire[0]][0]}")
                await ctx.send(f"réponse 2 {all_tu_preferes[liste_a_faire[0]][1]}")
                tu_preferes_on_off = "on"

    # si l'utilisateur est dans le mauvais canal ca le previent
    else :
        await ctx.send("Cette commande marche que dans le channel tu préfères")

# fonction pour repondre
@client.command()
async def je_prefere(ctx, reponse = 0):
    global all_tu_preferes
    global user_je_preferes
    global liste_a_faire
    global tu_preferes_on_off

    user_je_preferes = ctx.author.id
    # verifie si l'utilisateur est bien dans le tu preferes
    if ctx.channel.id == 980145249005494293:
        # si il n'y a pas de partie en cours
        if tu_preferes_on_off == "off" :
            await ctx.send("Vous devez lancer un tu préfères avnat de pouvoir utiliser cette commande")
        else :
            # si la personne qui a lancé le tu preferes n'est pas celle qui repond
            if user_tu_preferes != user_je_preferes :
                await ctx.send("Ce n'est pas vous qui avez lancer ce tu préfères")
            else : 
                # si l'utilisateur n'entre pas 1 ou 2
                if reponse != 1 and reponse != 2 :
                    await ctx.send("Vous devez choisir une réponse entre 1 et 2")
                else :
                    # si c'est la réponse 1
                    if reponse == 1 :
                        # donne les stats
                        await ctx.send(f"Tu préfères {all_tu_preferes[liste_a_faire[0]][0]} comme {all_tu_preferes[liste_a_faire[0]][3]} autres personnes")
                        await ctx.send(f"{all_tu_preferes[liste_a_faire[0]][4]} personnes ont choisis : {all_tu_preferes[liste_a_faire[0]][1]}")
                        # ajoute l'utilisateur dans les personnes qui ont voté cette réponse
                        all_tu_preferes[liste_a_faire[0]][3] = all_tu_preferes[liste_a_faire[0]][3] + 1
                    # si c'est la réponse 2
                    else :
                        # donne les stats
                        await ctx.send(f"Tu préfères {all_tu_preferes[liste_a_faire[0]][1]} comme {all_tu_preferes[liste_a_faire[0]][4]} autres personnes")
                        await ctx.send(f"{all_tu_preferes[liste_a_faire[0]][3]} personnes ont choisis : {all_tu_preferes[liste_a_faire[0]][0]}")
                        # ajoute l'utilisateur dans les personnes qui ont voté cette réponse
                        all_tu_preferes[liste_a_faire[0]][4] = all_tu_preferes[liste_a_faire[0]][4] + 1
                    # ajoute l'utilisateur dans le tableau des personnes qui ont déjà répondu a cette question
                    all_tu_preferes[liste_a_faire[0]][2].append(user_tu_preferes)
                    tu_preferes_on_off = "off"
    # si l'utilisateur est dans le mauvais canal ca le previent
    else :
        await ctx.send("Cette commande marche que dans le channel tu préfères")

# fonction pour repondre
@client.command()
async def stop_prefere(ctx):
    global tu_preferes_on_off

    # verifie si l'utilisateur est bien dans le tu preferes
    if ctx.channel.id == 980145249005494293:
        # si il n'y a pas de partie en cours
        if tu_preferes_on_off == "off" :
            await ctx.send("Vous devez lancer un tu préfères avnat de pouvoir utiliser cette commande")
        else :
            tu_preferes_on_off = "off"
    # si l'utilisateur est dans le mauvais canal ca le previent
    else :
        await ctx.send("Cette commande marche que dans le channel tu préfères")

# ----------------------------------------------- TU PREFERES ----------------------------------------------- #

# --------------------------------------------------- MATH --------------------------------------------------- #
# Phara :
@client.command()
async def mathadd(ctx, x: float, y: float):
    await ctx.send(x + y)

@client.command()
async def mathsub(ctx, x: float, y: float):
     await ctx.send(x - y)

@client.command()
async def mathdiv(ctx, x: float, y: float):
    await ctx.send(x / y)

@client.command()
async def mathmult(ctx, x: float, y: float):
    await ctx.send(x * y)

@client.command()
async def mathrandom(ctx, x: int, y: int):
    await ctx.send(random.randint(x, y))

@client.command()
async def mathracine(ctx, x: float):
    await ctx.send(math.sqrt(x))

# --------------------------------------------------- MATH --------------------------------------------------- #

# ----------------------------------------------- PUISSANCE 4 ----------------------------------------------- #

puissance_4 = []

# ----------------------------------------------- PUISSANCE 4 ----------------------------------------------- #

client.run('OTc4MjI5MTUwNDI0OTIwMDc0.GTFsq3.uomKxew7wl-gobOTyd5Y4f1qAS03etcrLaEQyM')