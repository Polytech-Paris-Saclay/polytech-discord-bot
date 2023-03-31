import discord
from discord.utils import find


async def createRoleGroupeAnglais(guild, groupe_anglais, semester):
    await guild.create_role(name=f'Anglais groupe {groupe_anglais} - {semester}', colour=discord.Colour(0x269407))

async def createRoleGroupeTDTP(guild, groupe, semester):
    await guild.create_role(name=f'Groupe {groupe} - {semester}', colour=discord.Colour.random())

async def createRoleOption(guild, option, semester):
    await guild.create_role(name=f'{option[0]} - {semester}', colour=discord.Colour.yellow())

async def updateGroupeEtOptionChannel(guild, semester, year_name, role_year, subjectDatabase):
    channel = find(lambda c: c.name == f'groupe-et-option-{year_name}', guild.channels)
    await channel.set_permissions(role_year, read_messages=False)
    await channel.purge()
    embed = discord.Embed(
        title=f'① Choisissez votre groupe de TD pour le {semester}',
        color=0x029DE4
    )
    await channel.send(embed=embed)
    desc = "```"
    for option in subjectDatabase[semester]['options']:
        desc += f'{option[1]} - {option[0]}\n'
    desc += "```"
    embed = discord.Embed(
        title=f'② Choisissez votre option pour le {semester}',
        description= desc,
        color=0x029DE4
    )
    await channel.send(embed=embed)
    embed = discord.Embed(
        title="③ Choisissez votre groupe d'anglais",
        color=0x029DE4
    )
    await channel.send(embed=embed)
    input("Type 'y' when setup reaction role done")
    await channel.set_permissions(role_year, read_messages=True)

async def archiveThisCategory(guild, category_name, archive_category):
    this_category = None
    for category in guild.categories:
        if category.name == category_name:
            this_category = category
            break
    for channel in this_category.channels:
        if channel.last_message_id is not None:
            await channel.edit(category=archive_category)
            await channel.set_permissions(guild.default_role, read_messages=True)
        else :
            await channel.delete()
    await this_category.delete()