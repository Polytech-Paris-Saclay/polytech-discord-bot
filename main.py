from datetime import datetime
from markdownify import markdownify

import disnake
from disnake.ext import commands
from disnake.ext import tasks
from disnake.utils import find

from dotenv import load_dotenv
import os

from oasis import getGrades
from tesla import getInternships, getInternshipInfos


load_dotenv()
# TOKEN = os.getenv('TOKEN')
TOKEN = os.environ['TOKEN']


bot = commands.Bot()


@tasks.loop(minutes=30)
async def tesla():
    internships = getInternships()

    ### Polytech
    guild = find(lambda g: 'PEIP' in g.name, bot.guilds)
    channel = find(lambda c: 'tesla' in c.name, guild.text_channels)
    
    messages = await channel.history(limit=None).flatten()
    
    previousListings = [
        int(message.embeds[0].footer.text)
        for message in messages
        if len(message.embeds)
    ]
    
    newListings = [l for l in internships if not int(l['id']) in previousListings]
    
    if len(newListings):
        await channel.send('||@everyone||')
    
    for listing in newListings:
        infosListing = getInternshipInfos(listing['id'])
        embed = disnake.Embed(
            title = f"Nouveau stage Tesla : {infosListing['title']}",
            color = 0xC90000,
            url = f'https://www.tesla.com/fr_FR/careers/search/job/{listing["id"]}',
            description = markdownify(
                infosListing['description']
                .replace('</div>', '</div> ')
            ),
            timestamp = datetime.now()
        )
        embed.set_thumbnail('https://www.tesla.com/themes/custom/tesla_frontend/assets/favicons/favicon-196x196.png')
        embed.set_footer(text=listing['id'])
        embed.add_field(name ='Localisation', value=infosListing['location'], inline=False)
        embed.add_field(name ='Département', value=infosListing['department'], inline=False)
        
        await channel.send(embed=embed)
        print(infosListing['title'])


@tasks.loop(minutes=10)
async def grades():
    grades = getGrades()

    ### Polytech
    guild = find(lambda g: 'PEIP' in g.name, bot.guilds)
    channel = find(lambda c: 'nouvelles-notes' in c.name, guild.text_channels)

    messages = await channel.history(limit=None).flatten()
    
    previousGrades = [
        message.embeds[0].footer.text
        for message in messages
        if len(message.embeds)
    ]
    
    newGrades = [
        grade for grade in grades
        if not f"{grade['subject-id']} - {grade['name']}" in previousGrades
    ]
    newGrades.sort(key=lambda g: g['date'])

    if len(newGrades):
        await channel.send('||@everyone||')
    
    for grade in newGrades:
        embed = disnake.Embed(
            title=f"Nouvelle note en {grade['subject']} !",
            color=0x00A8E8,
            url='https://oasis.polytech.universite-paris-saclay.fr/',
            description=grade['name'],
            timestamp=grade['date'],
        )

        oasis_icon = 'https://oasis.polytech.universite-paris-saclay.fr/prod/bo/picture/favicon/polytech_paris_oasis/favicon-194x194.png'
        embed.set_thumbnail(oasis_icon)
        embed.set_footer(text = f"{grade['subject-id']} - {grade['name']}")

        await channel.send(embed=embed)
        print(f"{grade['subject-id']} - {grade['name']}")
        
@bot.event
async def on_ready():
    tesla.start()
    grades.start()

bot.run(TOKEN)
