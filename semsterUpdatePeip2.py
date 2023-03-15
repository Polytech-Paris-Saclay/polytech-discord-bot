import discord
from discord.ext import commands
from discord.ext import tasks
from discord.utils import find
from discord import app_commands

from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from lxml import etree
import json

from oasis import getSubjects

load_dotenv()
LOGIN = os.environ['LOGIN']
PASSWORD = os.environ['PASSWORD']
TOKEN = os.environ['TOKEN']

''' Load subjectDatabase '''
with open('subjectDatabase.json','r',encoding="utf-8") as f:
    subjectDatabase = json.load(f)
year = subjectDatabase['S3']['year']

''' Manual Variables '''
nbr_groupes = 4
parcours_groupes = ['Physique','Chimie','Numérique','Numérique']
groupes_anglais = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

''' Discord bot '''
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name='updateS3')
async def updateS3(ctx):
    channelinit = bot.get_channel(899980108985688065)
    guild = channelinit.guild
    role_peip2 = find(lambda r: r.name == 'PeiP 2', guild.roles)

    ''' Delete S2 roles '''
    for role in guild.roles:
        if 'S2' in role.name:
            await role.delete()

    ''' Create new roles '''
    for groupe_anglais in groupes_anglais:
        await guild.create_role(name=f'Anglais groupe {groupe_anglais} - S3', colour=discord.Colour(0x269407))
    for groupe in range(1, nbr_groupes+1):
        await guild.create_role(name=f'Groupe {groupe} - S3', colour=discord.Colour.random())
    for option in subjectDatabase['S3']['options']:
        await guild.create_role(name=f'{option[0]} - S3', colour=discord.Colour.yellow())

    ''' Update channel "groupe et option peip2" '''
    channel = find(lambda c: c.name == "groupe et option peip2", guild.channels)
    await channel.set_permissions(role_peip2, read_messages=False)
    await channel.purge()
    embed = discord.Embed(
        title="① Choisissez votre groupe de TD pour le S3",
        color=0x029DE4
    )
    await channel.send(embed=embed)
    desc= "```"
    for option in subjectDatabase['S3']['options']:
        desc += f'{option[1]} - {option[0]}\n'
    desc += "```"
    embed = discord.Embed(
        title="② Choisissez votre option pour le S3",
        description= desc,
        color=0x029DE4
    )
    await channel.send(embed=embed)
    embed = discord.Embed(
        title="③ Choisissez votre groupe d'anglais",
        color=0x029DE4
    )
    await channel.send(embed=embed)
    reaction_role_setup = input("Type 'y' when setup reaction role done")
    await channel.set_permissions(role_peip2, read_messages=True)

    ''' Archive previous categories (into '═ [Archives S2 - previous year] ═') and give permissions '''
    archive_category = await guild.create_category(name=f'═ [Archives S2 - {int(year[0])-1}/{int(year[1])-1}] ═')
    categories_to_archive = [
        '═══ Tronc commun - S2 ═══',
        '══════ Option - S2 ══════',
        '════ Parcours - S2 ════',
        '════ anglais - peip1 ═════',
        '═══ Groupe TD/TP - S2 ════'
    ]
    for category_name in categories_to_archive:
        this_category = None
        for category in guild.categories:
            if category.name == category_name:
                this_category = category
        for channel in this_category.channels:
            if channel.last_message_id is not None:
                await channel.edit(category=archive_category)
                await channel.set_permissions(guild.default_role, read_messages=True)
            else :
                await channel.delete()
        await this_category.delete()

    ''' Create new categories with subjects channels and permissions '''
    # tronc commun 
    tronc_commun = subjectDatabase['S3']['tronc_commun']
    category = await guild.create_category(name='═══ Tronc commun - S3 ═══', position=4)
    await category.set_permissions(guild.default_role, read_messages=False)
    await category.set_permissions(role_peip2, read_messages=True)
    for subject in tronc_commun:
        await category.create_text_channel(name=f'{subject}')
    # groupes TD/TP
    category = await guild.create_category(name='═══ Groupe TD/TP - S3 ════', position=4)
    await category.set_permissions(guild.default_role, read_messages=False)
    for i in range(1, nbr_groupes+1):
        channel = await category.create_text_channel(name=f'groupe {i}')
        await channel.set_permissions(find(lambda r: r.name == f'Groupe {i} - S3', guild.roles), read_messages=True)
    # options
    options = subjectDatabase['S3']['options']
    category = await guild.create_category(name='══════ Option - S3 ══════', position=4)
    await category.set_permissions(guild.default_role, read_messages=False)
    for subject in options:
        channel = await category.create_text_channel(name=f'{subject[0]}')
        await channel.set_permissions(find(lambda r: r.name == f'{subject[0]} - S3', guild.roles), read_messages=True)
    # parcours
    parcours = subjectDatabase['S3']['parcours']
    category = await guild.create_category(name='════ parcours - peip2 ════', position=4)
    await category.set_permissions(guild.default_role, read_messages=False)
    for subject in parcours:
        channel = await category.create_text_channel(name=f'{subject}')
        for i in range(1,len(parcours_groupes)+1):
            if subject == parcours_groupes[i-1]:
                await channel.set_permissions(find(lambda r: r.name == f'Groupe {i} - S3', guild.roles), read_messages=True)    
    # anglais
    category = await guild.create_category(name='════ anglais - peip2 ═════', position=4)
    await category.set_permissions(guild.default_role, read_messages=False)
    for groupe in groupes_anglais:
        channel = await category.create_text_channel(name=f'groupe {groupe}')
        await channel.set_permissions(find(lambda r: r.name == f'Anglais groupe {groupe} - S3', guild.roles), read_messages=True)
    
@bot.command(name='updateS4')
async def updateS4(ctx):
    channelinit = bot.get_channel(899980108985688065)
    guild = channelinit.guild
    role_peip2 = find(lambda r: r.name == 'PeiP 2', guild.roles)

    ''' Delete S3 roles '''
    for role in guild.roles:
        if 'S3' in role.name:
            await role.delete()

    ''' Create new roles '''
    for groupe_anglais in groupes_anglais:
        await guild.create_role(name=f'Anglais groupe {groupe_anglais} - S4', colour=discord.Colour(0x269407))
    for groupe in range(1, nbr_groupes+1):
        await guild.create_role(name=f'Groupe {groupe} - S4', colour=discord.Colour.random())
    for option in subjectDatabase['S4']['options']:
        await guild.create_role(name=f'{option[0]} - S4', colour=discord.Colour.yellow())

    ''' Update channel "groupe et option peip2" '''
    channel = find(lambda c: c.name == "groupe-et-option-peip2", guild.channels)
    print(channel.name)
    await channel.set_permissions(role_peip2, read_messages=False)
    await channel.purge()
    embed = discord.Embed(
        title="① Choisissez votre groupe de TD pour le S4",
        color=0x029DE4
    )
    await channel.send(embed=embed)
    desc= "```"
    for option in subjectDatabase['S4']['options']:
        desc += f'{option[1]} - {option[0]}\n'
    desc += "```"
    embed = discord.Embed(
        title="② Choisissez votre option pour le S4",
        description= desc,
        color=0x029DE4
    )
    await channel.send(embed=embed)
    embed = discord.Embed(
        title="③ Choisissez votre groupe d'anglais",
        color=0x029DE4
    )
    await channel.send(embed=embed)
    reaction_role_setup = input("Type 'y' when setup reaction role done")
    await channel.set_permissions(role_peip2, read_messages=True)

    ''' Archive previous categories (into '═ [Archives S3 - this year] ═') and give permissions '''
    archive_category = await guild.create_category(name=f'═ [Archives S3 - {int(year[0])}/{int(year[1])}] ═')
    categories_to_archive = [
        '═══ Tronc commun - S3 ═══',
        '══════ Option - S3 ══════',
        '═══ Groupe TD/TP - S3 ════'
    ]
    for category_name in categories_to_archive:
        this_category = None
        for category in guild.categories:
            if category.name == category_name:
                this_category = category
        for channel in this_category.channels:
            if channel.last_message_id is not None:
                await channel.edit(category=archive_category)
                await channel.set_permissions(guild.default_role, read_messages=True)
            else :
                await channel.delete()
        await this_category.delete()

    ''' Create new categories with subjects channels and permissions '''
    # tronc commun 
    tronc_commun = subjectDatabase['S4']['tronc_commun']
    category = await guild.create_category(name='═══ Tronc commun - S4 ═══', position=4)
    await category.set_permissions(guild.default_role, read_messages=False)
    await category.set_permissions(role_peip2, read_messages=True)
    for subject in tronc_commun:
        await category.create_text_channel(name=f'{subject}')
    # groupes TD/TP
    category = await guild.create_category(name='═══ Groupe TD/TP - S4 ════', position=4)
    await category.set_permissions(guild.default_role, read_messages=False)
    for i in range(1, nbr_groupes+1):
        channel = await category.create_text_channel(name=f'groupe {i}')
        await channel.set_permissions(find(lambda r: r.name == f'Groupe {i} - S4', guild.roles), read_messages=True)
    # options
    options = subjectDatabase['S4']['options']
    category = await guild.create_category(name='══════ Option - S4 ══════', position=4)
    await category.set_permissions(guild.default_role, read_messages=False)
    for subject in options:
        channel = await category.create_text_channel(name=f'{subject[0]}')
        await channel.set_permissions(find(lambda r: r.name == f'{subject[0]} - S4', guild.roles), read_messages=True) 

''' Tests '''
@bot.command(name='test')
async def test(ctx):
    channelinit = bot.get_channel(899980108985688065)
    guild = channelinit.guild
    print('test')

bot.run(TOKEN)