import os

from dotenv import load_dotenv
load_dotenv()

var = os.getenv("ENV_KEY")

##################### Import #####################
import discord 
from discord.ext import commands 
import asyncio 
import random

### Connexion base de données ###
import sqlite3
connexionBD = sqlite3.connect("myDB.db")

from datetime import date

import validators

######################################################################################################################################################

##################### Préfixe #####################
client = commands.Bot(command_prefix='&',help_command = None) 

##################### Lancement du bot #####################
@client.event 
async def on_ready() : 
    print('______________________________________________')
    print("[CDS] PixelKorp est en ligne (à nouveau).")
    print('______________________________________________')

##################### Page du &help #####################
@client.command(pass_context=True, name="help")
async def help(ctx):
	page1 = discord.Embed (
		title = 'Page 1/3',
		description = 'Commande de base',
		colour = 0x8B0000
	)
	page1.add_field(
		inline=False,
		name="&create ou &crt",
		value=">    Créer un compte pour le jeu 🎮"
	)
	page1.add_field(
		inline=False,
		name="&info @Membre",
		value=">    Voir les stats d'un compte 📈"
	)
	page1.add_field(
		inline=False,
		name="&generate ou &gen",
		value=">    Générer de l'argent 💰"
	)
	page1.add_field(
		inline=False,
		name="&geninfo ou &gi",
		value=">    Voir les informations sur le gain d'argent 💰"
	)
	page2 = discord.Embed (
		title = 'Page 2/3',
		description = 'Personnage',
		colour = 0x8B0000
	)
	page2.add_field(
		inline=False,
		name="&new nomPersonnage",
		value=">    Pour 50€ vous pouvez créez un nouveau personnage 🌱"
	)
	page2.add_field(
		inline=False,
		name="&personnage nomPersonnage ou &p nomPersonnage",
		value=">    Donne des informations sur un personnage 🌱"
	)
	page2.add_field(
		inline=False,
		name="&imagepersonnage lienGif nomPersonnage ou &ip lienGif nomPersonnage",
		value=">    Change l'image d'un personnage (seulement disponible pour le propriétaire) 📷"
	)
	page2.add_field(
		inline=False,
		name="&buy nomPersonnagee",
		value=">    Achête le personnage d'un autre joueur pour le double de sa valeur (le propriétaire originel sera remboursé de la valeur du personnage) 💰"
	)
	page3 = discord.Embed (
		title = 'Page 3/3',
		description = 'Personnage',
		colour = 0x8B0000
	)
	page3.add_field(
		inline=False,
		name="&collection @Membre ou $clt @Membre",
		value=">    Voir les personnages d'une personne 📈"
	)
	page3.add_field(
		inline=False,
		name="&sell nomPersonnagee",
		value=">    Vendre un de ces personnages 💰"
	)
	page3.add_field(
		inline=False,
		name="&boost valeur nomPersonnagee",
		value=">    Booster la valeur d'un de ces personnages 💰"
	)
    
	pages = [page1, page2, page3]

	message = await ctx.send(embed = page1)
	await message.add_reaction('◀')
	await message.add_reaction('▶')

	def check(reaction, user):
		return user == ctx.author

	i = 0
	reaction = None

	while True:
		if str(reaction) == '◀':
			if i > 0:
				i -= 1
			await message.edit(embed = pages[i])
		elif str(reaction) == '▶':
			if i < 2:
				i += 1
				await message.edit(embed = pages[i])        
		try:
			reaction, user = await client.wait_for('reaction_add', timeout = 30.0, check = check)
			await message.remove_reaction(reaction, user)
		except:
			break
	await message.clear_reactions()

##################### Fonction &create #####################
@client.command(pass_context=True, name = "create", aliases =["crt"])
async def create(ctx) :
	texte = "texte base"
	gif = "https://c.tenor.com/q6vmV7JzZaAAAAAd/anime-oops-my-fault.gif"
	recherche = False

	cursor = connexionBD.cursor()
	requete = "select * from Utilisateur"
	cursor.execute(requete)
	rows = cursor.fetchall()
	for row in rows:
	  if (str(ctx.author.id) == row[0]) :
	  	recherche = True
	  	
	if (recherche == True) :
		texte = "Vous avez déjà un compte existant"
		gif = "https://c.tenor.com/P-8ZvqnS4AwAAAAC/dancing-cat-dancing-kitten.gif"
	else : 
		texte = "Votre compte à été créé"
		gif = "https://c.tenor.com/St6dO-mo8jkAAAAC/meliodas-nanatsu-no-taizai.gif"
		requete = "INSERT INTO Utilisateur(id, nom, argent, possession, dernierVote) VALUES ('" + str(ctx.author.id) + "', '" + str(ctx.author.name) + "', 0, 0, 0000-00-00)"
		cursor.execute(requete)
		connexionBD.commit()

	cursor.close()	

	embed=discord.Embed(
		title= "Bonjour " + str(ctx.author.name),
		description= texte,
		color=0x8B0000
	)
	embed.set_image(url=gif)
	await ctx.send(embed=embed)

##################### Fonction &info #####################
@client.command(pass_context=True, name = "info")
async def info(ctx, member : discord.Member) :
	personneConcerne = member


	cursor = connexionBD.cursor()
	requete = "SELECT nom, argent, possession, dernierVote FROM Utilisateur WHERE id='" + str(personneConcerne.id) + "'"
	cursor.execute(requete)
	rows = cursor.fetchall()

	if (rows == []) :
		texte = "Cette personne n'as pas encore de compte (&create pour avoir un compte)"
		gif = "https://c.tenor.com/1n8v0zuWPDUAAAAd/make-a-wish-miss-you.gif"

		embed=discord.Embed(
			title= "Information sur " + str(personneConcerne.name),
			description=texte,
			color=0x8B0000
		)
		embed.set_image(url=gif)
		await ctx.send(embed=embed)
	else :
		personne = rows[0]

		embed=discord.Embed(
			title= "Information sur " + str(personne[0]),
			description=
			"**Nom du joueur** : " + str(personne[0]) + "\n" + 
			"**Argent** : " + str(personne[1]) + "\n" + 
			"**Possession** : " + str(personne[2]) + "\n"
			"**Date du dernier vote** : " + str(personne[3]) + "\n",
			color=0x8B0000
		)
		author = personneConcerne
		pfp = author.avatar_url
		embed.set_image(url=pfp)
		await ctx.send(embed=embed)


	cursor.close()	

##################### Fonction &generate #####################
@client.command(pass_context=True, name = "generate", aliases =["gen"])
async def generate(ctx) :
	texte = "Erreur"
	gif = "https://c.tenor.com/q6vmV7JzZaAAAAAd/anime-oops-my-fault.gif"

	today = date.today()

	cursor = connexionBD.cursor()
	requete = "SELECT dernierVote FROM Utilisateur WHERE id='" + str(ctx.author.id) + "'"
	cursor.execute(requete)
	rows = cursor.fetchall()
	dateDernierVote = rows[0]
	if (str(dateDernierVote[0]) != str(today)) :
		requete = "UPDATE Utilisateur SET dernierVote = '" + str(today) + "' WHERE id='" + str(ctx.author.id) + "'"
		cursor.execute(requete)
		connexionBD.commit()

		valeurAleatoire = random.randint(0, 99)
		if (valeurAleatoire <= 39) :
			gain = random.randint(25, 50)
			texte = "Pas beaucoup de chance aujourd'hui !\n  **Vous gagnez : " + str(gain) + "€**" 
			gif = "https://c.tenor.com/Tn9mzxqYNs4AAAAd/kukuru-misakino-anime.gif"
		elif ( (valeurAleatoire > 39) and (valeurAleatoire <= 69) ) :
			gain = random.randint(60, 80)
			texte = "Vous avez fait une bonne trouvaille !\n  **Vous gagnez : " + str(gain) + "€**"
			gif = "https://c.tenor.com/DVbymBMiCtoAAAAd/omg-happy.gif"
		elif ( (valeurAleatoire > 69) and (valeurAleatoire <= 89) ) :
			gain = random.randint(100, 250)
			texte = "Wow ! Quel beau pactole !\n  **Vous gagnez : " + str(gain) + "€**"
			gif = "https://c.tenor.com/fxuUKyzBcG8AAAAC/anime-wow.gif"
		else :
			gain = random.randint(300, 500)
			texte = "MAIS C'EST INCROYABLE !\n  **Vous gagnez : " + str(gain) + "€**"
			gif = "https://c.tenor.com/KQOYQrlNMNYAAAAC/goku-anime.gif"

		requete = "SELECT argent FROM Utilisateur WHERE id='" + str(ctx.author.id) + "'"
		cursor.execute(requete)
		rows = cursor.fetchall()
		argent = rows[0]
		nouvelleValeurArgent = argent[0] + gain

		requete = "UPDATE Utilisateur SET argent = '" + str(nouvelleValeurArgent) + "' WHERE id='" + str(ctx.author.id) + "'"
		cursor.execute(requete)
		connexionBD.commit()

		texte += "\n**Argent du compte : " + str(nouvelleValeurArgent) + "€**"

	else : 
		texte = "Désolé, mais vous avez déjà voté aujourd'hui"
		gif = "https://c.tenor.com/mSqEgKfI3uUAAAAd/my-hero-academia-anime.gif"

	cursor.close()	

	embed=discord.Embed(
		title= "Génération de " + str(ctx.author.name) + " effectué",
		description= texte,
		color=0x8B0000
	)
	embed.set_image(url=gif)
	await ctx.send(embed=embed)

##################### Page du &geninfo #####################
@client.command(pass_context=True,name="geninfo", aliases =["gi"])
async def geninfo(ctx):
	embed=discord.Embed(
		title="Page d'aide :",
		description="Voici les informations sur le gain d'argent de la commande &generate",
		color=0x8B0000
	)
	embed.add_field(
		inline=False,
		name="**Petite somme :** 40% de chance",
		value=">    Entre 25€ et 50€"
	)
	embed.add_field(
		inline=False,
		name="**Somme moyenne :** 30% de chance",
		value=">    Entre 60€ et 80€"
	)
	embed.add_field(
		inline=False,
		name="**Grande somme :** 20% de chance",
		value=">    Entre 100€ et 250€"
	)
	embed.add_field(
		inline=False,
		name="**Somme gigantesque :** 10% de chance",
		value=">    Entre 300€ et 500€"
	)
	await ctx.send(embed=embed)

##################### Fonction &new #####################
@client.command(pass_context=True, name = "new")
async def new(ctx, *args) :
	texte = "Erreur"
	gif = "https://c.tenor.com/q6vmV7JzZaAAAAAd/anime-oops-my-fault.gif"

	nomPersonnage = ""
	for i in range(0, len(args)) :
		nomPersonnage += args[i] + " "
	nomPersonnage = nomPersonnage[:-1]
	nomPersonnage = nomPersonnage.lower()
	nomPersonnage = nomPersonnage.capitalize()

	erreur = False
	for lettre in nomPersonnage :
		if (lettre.isalpha() == False) :
			if (lettre.isspace() == False) :
				erreur = True

	if erreur == True :
		texte = "Caractères spéciaux refusés"
		gif = "https://c.tenor.com/REzNL4LDpEsAAAAC/anime-nope.gif"
	else :
		texte = "Nom validé"
		gif = "https://c.tenor.com/HXcF3phTDOoAAAAC/anime-headbang-left-anime-girl-rave.gif"

		cursor = connexionBD.cursor()
		requete = "SELECT nomPersonnage FROM Personnage WHERE nomPersonnage='" + str(nomPersonnage) + "'"
		cursor.execute(requete)
		rows = cursor.fetchall()

		if (rows != []) :
			texte = "Le personnage existe déjà"
			gif = "https://c.tenor.com/0xU9LZX3oZ0AAAAC/futami.gif"
		else :
			cursor = connexionBD.cursor()
			requete = "SELECT argent FROM Utilisateur WHERE id='" + str(ctx.author.id) + "'"
			cursor.execute(requete)
			rows = cursor.fetchall()
			argent = rows[0]
			
			if (argent[0] >= 50) :
				argent = argent[0] - 50

				requete = "UPDATE Utilisateur SET argent = '" + str(argent) + "' WHERE id='" + str(ctx.author.id) + "'"
				cursor.execute(requete)
				connexionBD.commit()

				requete = "INSERT into Personnage(nomPersonnage, valeur, proprietaire, image, classement) values ('" + str(nomPersonnage) + "', '50', '" + str(ctx.author.id) + "', 'https://c.tenor.com/VvRWjXXeNTIAAAAC/loop.gif', 0)"
				cursor.execute(requete)
				connexionBD.commit()

				requete = "SELECT possession FROM Utilisateur WHERE id='" + str(ctx.author.id) + "'"
				cursor.execute(requete)
				rows = cursor.fetchall()
				possession = rows[0]
				possession = possession[0] + 1

				requete = "UPDATE Utilisateur SET possession = '" + str(possession) + "' WHERE id='" + str(ctx.author.id) + "'"
				cursor.execute(requete)
				connexionBD.commit()

				fonctionClassement()

				texte = "Un nouveau personnage est né !"
				gif = "https://c.tenor.com/St6dO-mo8jkAAAAC/meliodas-nanatsu-no-taizai.gif"

			else :
				texte = "Pas assez d'argent (50$ nécéssaire)"
				gif = "https://c.tenor.com/SqW6kmYUeGYAAAAC/money-anime.gif"

		cursor.close()	

	embed=discord.Embed(
		title= "Création du personnage : " + nomPersonnage,
		description= texte,
		color=0x8B0000
	)
	embed.set_image(url=gif)
	await ctx.send(embed=embed)

##################### Fonction &personnage #####################
@client.command(pass_context=True, name = "personnage", aliases =["p"])
async def personnage(ctx, *args) :	
	if (str(args) != "()") :
		nomPersonnage = ""
		for i in range(0, len(args)) :
			nomPersonnage += args[i] + " "
		nomPersonnage = nomPersonnage[:-1]
		nomPersonnage = nomPersonnage.lower()
		nomPersonnage = nomPersonnage.capitalize()

		cursor = connexionBD.cursor()
		requete = "SELECT nomPersonnage, valeur, nom, image, classement FROM Personnage INNER JOIN Utilisateur ON Utilisateur.id = Personnage.proprietaire WHERE nomPersonnage='" + nomPersonnage + "'"
		cursor.execute(requete)
		rows = cursor.fetchall()
		
		if (rows == []) :
			texte = "Le personnage n'existe pas"
			gif = "https://c.tenor.com/REzNL4LDpEsAAAAC/anime-nope.gif"
		else :
			perso = rows[0]
			texte = "**Nom du personnage** : " + str(perso[0]) + "\n" + "**Valeur** : " + str(perso[1]) + "\n" + "**Proprietaire** : " + str(perso[2]) + "\n" + "**Classement** : " + str(perso[4]) + "\n"
			gif = perso[3]

		cursor.close()	

		embed=discord.Embed(
			title= "Information sur " + str(nomPersonnage),
			description= texte,
			color=0x8B0000
		)
		embed.set_image(url=gif)
		await ctx.send(embed=embed)

##################### Fonction &imagepersonnage #####################
@client.command(pass_context=True, name = "imagepersonnage", aliases =["ip"])
async def imagepersonnage(ctx, lien, *args) :
	if (str(args) != "()") :
		nomPersonnage = ""
		for i in range(0, len(args)) :
			nomPersonnage += args[i] + " "
		nomPersonnage = nomPersonnage[:-1]
		nomPersonnage = nomPersonnage.lower()
		nomPersonnage = nomPersonnage.capitalize()

		cursor = connexionBD.cursor()

		valid = validators.url(lien)

		if valid==True:
			requete = "SELECT proprietaire FROM Personnage WHERE nomPersonnage='" + nomPersonnage + "'"
			cursor.execute(requete)
			rows = cursor.fetchall()
			rows = rows[0]
			if (rows[0] == ctx.author.id) :
				texte = "Voici la nouvelle image :"
				gif = str(lien)

				requete = "UPDATE Personnage SET image = '" + str(lien) + "' WHERE nomPersonnage='" + str(nomPersonnage) + "'"
				cursor.execute(requete)
				connexionBD.commit()
			else :
				texte = "Vous n'avez pas le droit de modifié le personnage"
				gif = "https://c.tenor.com/REzNL4LDpEsAAAAC/anime-nope.gif"

			cursor.close()	

			embed=discord.Embed(
				title= "Modification de l'image de " + str(nomPersonnage),
				description= texte,
				color=0x8B0000
			)
			embed.set_image(url=gif)
			await ctx.send(embed=embed)
		else : 
			gif = "https://c.tenor.com/REzNL4LDpEsAAAAC/anime-nope.gif"
			embed=discord.Embed(
				title= "Modification de l'image de " + str(nomPersonnage),
				description= "Image non accepté",
				color=0x8B0000
			)
			embed.set_image(url=gif)
			await ctx.send(embed=embed)

##################### Fonction &buy #####################
@client.command(pass_context=True, name = "buy")
async def buy(ctx, *args) :
	if (str(args) != "()") :
		nomPersonnage = ""
		for i in range(0, len(args)) :
			nomPersonnage += args[i] + " "
		nomPersonnage = nomPersonnage[:-1]
		nomPersonnage = nomPersonnage.lower()
		nomPersonnage = nomPersonnage.capitalize()

		cursor = connexionBD.cursor()

		requete = "SELECT nomPersonnage, valeur, proprietaire FROM Personnage WHERE nomPersonnage='" + str(nomPersonnage) + "'"
		cursor.execute(requete)
		rows = cursor.fetchall()

		if (rows != []) :
			texte = "Le personnage existe déjà"
			gif = "https://c.tenor.com/0xU9LZX3oZ0AAAAC/futami.gif"

			infoPersonnage = rows[0]

			proprietairePersonnage = infoPersonnage[2]

			if (proprietairePersonnage == ctx.author.id) :
				texte = "Vous ne pouvez pas acheté votre propre personnage"
				gif = "https://c.tenor.com/6WJATrb4esIAAAAC/atsushi-nakajima-lost.gif"
			else :
				requete = "SELECT id, nom, argent, possession FROM Utilisateur WHERE id='" + str(ctx.author.id) + "'"
				cursor.execute(requete)
				rows = cursor.fetchall()

				infoUtilisateur = rows[0]

				if infoUtilisateur[2] >= (infoPersonnage[1] * 2) :
					valeur = infoUtilisateur[2] - (infoPersonnage[1] * 2)

					requete = "UPDATE Utilisateur SET argent = '" + str(valeur) + "' WHERE id='" + str(ctx.author.id) + "'"
					cursor.execute(requete)
					connexionBD.commit()

					nouvellePossession = infoUtilisateur[3] + 1

					requete = "UPDATE Utilisateur SET possession = '" + str(nouvellePossession) + "' WHERE id='" + str(ctx.author.id) + "'"
					cursor.execute(requete)
					connexionBD.commit()

					requete = "SELECT argent, possession FROM Utilisateur WHERE id='" + str(infoPersonnage[2]) + "'"
					cursor.execute(requete)
					rows = cursor.fetchall()
					info = rows[0]
					argent = info[0]
					argent += infoPersonnage[1]
					requete = "UPDATE Utilisateur SET argent = '" + str(argent) + "' WHERE id='" + str(infoPersonnage[2]) + "'"
					cursor.execute(requete)
					connexionBD.commit()
					possession = info[1]
					possession -= 1
					requete = "UPDATE Utilisateur SET possession = '" + str(possession) + "' WHERE id='" + str(infoPersonnage[2]) + "'"
					cursor.execute(requete)
					connexionBD.commit()

					requete = "UPDATE Personnage SET valeur = '" + str((infoPersonnage[1] * 2)) + "' WHERE nomPersonnage='" + str(nomPersonnage) + "'"
					cursor.execute(requete)
					connexionBD.commit()

					requete = "UPDATE Personnage SET proprietaire = '" + str(ctx.author.id) + "' WHERE nomPersonnage='" + str(nomPersonnage) + "'"
					cursor.execute(requete)
					connexionBD.commit()

					fonctionClassement()

					texte = str(ctx.author.name) + "à racheter le personngae de "
					gif = "https://c.tenor.com/6WJATrb4esIAAAAC/atsushi-nakajima-lost.gif"
		else :
			texte = "Le personnage n'existe pas"
			gif = "https://c.tenor.com/6WJATrb4esIAAAAC/atsushi-nakajima-lost.gif"

		embed=discord.Embed(
			title= "Achat de " + str(nomPersonnage),
			description= texte,
			color=0x8B0000
		)
		embed.set_image(url=gif)
		await ctx.send(embed=embed)

		cursor.close()	

##################### Fonction &collection #####################
@client.command(pass_context=True, name = "collection", aliases =["clt"])
async def collection(ctx, member : discord.Member) :
	idUtilisateur = member.id

	cursor = connexionBD.cursor()

	requete = "SELECT nomPersonnage, valeur, classement FROM Personnage WHERE proprietaire='" + str(idUtilisateur) + "' ORDER BY Classement"
	cursor.execute(requete)
	rows = cursor.fetchall()

	texte = ""

	for i in range (len(rows)) :
		elementActuel = rows[i]
		texte += "**" + elementActuel[0] + "** - " + str(elementActuel[1]) + " - [" + str(elementActuel[2]) + "]\n"

	cursor.close()

	embed=discord.Embed(
		title= "Collection de " + str(member.name),
		description= texte,
		color=0x8B0000
	)
	await ctx.send(embed=embed)

##################### Fonction &sell #####################
@client.command(pass_context=True, name = "sell")
async def sell(ctx, *args) :
	if (str(args) != "()") :
		nomPersonnage = ""
		for i in range(0, len(args)) :
			nomPersonnage += args[i] + " "
		nomPersonnage = nomPersonnage[:-1]
		nomPersonnage = nomPersonnage.lower()
		nomPersonnage = nomPersonnage.capitalize()

		cursor = connexionBD.cursor()

		requete = "SELECT nomPersonnage, valeur, proprietaire FROM Personnage WHERE nomPersonnage='" + str(nomPersonnage) + "'"
		cursor.execute(requete)
		rows = cursor.fetchall()


		### Si le Personnage existe ###
		if (rows != []) :
			infoPersonnage = rows[0]

			proprietairePersonnage = infoPersonnage[2]

			### Si le Personnage appartient à l'auteur du message ###
			if (proprietairePersonnage == ctx.author.id) :
				requete = "SELECT id, nom, argent, possession FROM Utilisateur WHERE id='" + str(ctx.author.id) + "'"
				cursor.execute(requete)
				rows = cursor.fetchall()

				infoUtilisateur = rows[0]

				### Ajout de la valeur du personnage à l'argent du propriétaire ###
				valeur = infoUtilisateur[2] + infoPersonnage[1]
				requete = "UPDATE Utilisateur SET argent = '" + str(valeur) + "' WHERE id='" + str(ctx.author.id) + "'"
				cursor.execute(requete)
				connexionBD.commit()

				### Suppresion d'une possession du propriétaire ###
				nouvellePossession = infoUtilisateur[3] - 1
				requete = "UPDATE Utilisateur SET possession = '" + str(nouvellePossession) + "' WHERE id='" + str(ctx.author.id) + "'"
				cursor.execute(requete)
				connexionBD.commit()

				### Suppresion du Personnnage ###
				requete = "DELETE FROM Personnage WHERE nomPersonnage='" + str(nomPersonnage) + "'"
				cursor.execute(requete)
				connexionBD.commit()

				### Mise à jour du classement ###
				fonctionClassement()

				texte = "**"+ str(nomPersonnage) + "** à été vendu pour " + str(infoPersonnage[1]) + "€"
				gif = "https://c.tenor.com/YvaE5INKypcAAAAC/money-cash.gif"
				

			### Si le Personnage n'appartient pas à l'auteur du message ###
			else :
				texte = "Vous ne pouvez pas vendre un personnage qui ne vous appartient pas..."
				gif = "https://c.tenor.com/-d4FrVwQg6EAAAAd/blinking-guy.gif"

		### Si le Personnage n'existe pas ###		
		else :
			texte = "Le personnage n'existe pas"
			gif = "https://c.tenor.com/6WJATrb4esIAAAAC/atsushi-nakajima-lost.gif"

		embed=discord.Embed(
			title= "Vente de " + str(nomPersonnage),
			description= texte,
			color=0x8B0000
		)
		embed.set_image(url=gif)
		await ctx.send(embed=embed)

		cursor.close()	

##################### Fonction &boost #####################
@client.command(pass_context=True, name = "boost")
async def boost(ctx, val, *args) :
	if (str(args) != "()") :
		nomPersonnage = ""
		for i in range(0, len(args)) :
			nomPersonnage += args[i] + " "
		nomPersonnage = nomPersonnage[:-1]
		nomPersonnage = nomPersonnage.lower()
		nomPersonnage = nomPersonnage.capitalize()

		cursor = connexionBD.cursor()

		requete = "SELECT valeur, proprietaire FROM Personnage WHERE nomPersonnage='" + str(nomPersonnage) + "'"
		cursor.execute(requete)
		rows = cursor.fetchall()

		### Si le Personnage existe ###
		if (rows != []) :
			infoPersonnage = rows[0]

			proprietairePersonnage = infoPersonnage[1]

			### Si le Personnage appartient à l'auteur du message ###
			if (proprietairePersonnage == ctx.author.id) :
				requete = "SELECT argent FROM Utilisateur WHERE id='" + str(ctx.author.id) + "'"
				cursor.execute(requete)
				rows = cursor.fetchall()

				infoUtilisateur = rows[0]

				### Vérification argent nécéssaire pour le boost ###
				argentUtilisateur = int(infoUtilisateur[0])
				val = int(val)

				### Si l'Utilisateur a assez d'argent ###
				if argentUtilisateur >= val :
					argentUtilisateur -= val

					### Diminution de l'argent du propriétaire ###
					requete = "UPDATE Utilisateur SET argent = '" + str(argentUtilisateur) + "' WHERE id='" + str(ctx.author.id) + "'"
					cursor.execute(requete)
					connexionBD.commit()

					### Augmentation de la valeur du personnage ###
					valeurPersonnage = infoPersonnage[0] + val
					requete = "UPDATE Personnage SET valeur = '" + str(valeurPersonnage) + "' WHERE nomPersonnage='" + nomPersonnage + "'"
					cursor.execute(requete)
					connexionBD.commit()

					### Mise à jour du classement et du texte ###
					fonctionClassement()
					texte = "**"+ str(nomPersonnage) + "** à été boosté !\n **Ancienne valeur :** " + str(infoPersonnage[0]) + "€\n **Nouvelle valeur :** " + str(valeurPersonnage) + "€"
					gif = "https://c.tenor.com/YrkzNV2ajyUAAAAC/dragon-ball-super-saiyan-blue.gif"

				### Si l'Utilisateur n'a pas assez d'argent ###
				else :
					### Mise à jour du texte ###
					texte = "Vous n'avez que **" + str(argentUtilisateur) + "€** sur votre compte"
					gif = "https://c.tenor.com/rFL0-cu5Cg4AAAAM/bad-bunny-anime.gif"

			### Si le Personnage n'appartient pas à l'auteur du message ###
			else :
				texte = "Vous ne pouvez pas boost un personnage qui ne vous appartient pas..."
				gif = "https://c.tenor.com/-d4FrVwQg6EAAAAd/blinking-guy.gif"

		### Si le Personnage n'existe pas ###		
		else : 
			texte = "Le personnage n'existe pas"
			gif = "https://c.tenor.com/6WJATrb4esIAAAAC/atsushi-nakajima-lost.gif"

		embed=discord.Embed(
			title= "Boost de " + str(nomPersonnage),
			description= texte,
			color=0x8B0000
		)
		embed.set_image(url=gif)
		await ctx.send(embed=embed)

		cursor.close()	

##################### Fonction classement #####################
def fonctionClassement() :
	cursor = connexionBD.cursor()

	requete = "SELECT nomPersonnage, valeur, classement FROM Personnage ORDER BY valeur DESC"
	cursor.execute(requete)
	rows = cursor.fetchall()
	compteur = 1

	for i in range (len(rows)) :
		elementActuel = rows[i]

		requete = "UPDATE Personnage SET classement = '" + str(compteur) + "' WHERE nomPersonnage='" + elementActuel[0] + "'"
		cursor.execute(requete)
		connexionBD.commit()

		compteur += 1

	cursor.close()

######################################################################################################################################################
client.run(var)