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

async def createCategoryTroncCommun(guild, tronc_commun, semester, role_year):
    category = await guild.create_category(name=f'═══ Tronc commun - {semester} ═══', position=4)
    await category.set_permissions(guild.default_role, read_messages=False)
    await category.set_permissions(role_year, read_messages=True)
    for subject in tronc_commun:
        await category.create_text_channel(name=f'{subject}')

async def createCategoryGroupeTDTP(guild, nbr_groupes, semester):
    category = await guild.create_category(name=f'═══ Groupe TD/TP - {semester} ════', position=4)
    await category.set_permissions(guild.default_role, read_messages=False)
    for i in range(1, nbr_groupes+1):
        channel = await category.create_text_channel(name=f'groupe {i}')
        await channel.set_permissions(find(lambda r: r.name == f'Groupe {i} - {semester}', guild.roles), read_messages=True)

async def createCategoryOptions(guild, options, semester):
    category = await guild.create_category(name=f'══════ Option - {semester} ══════', position=4)
    await category.set_permissions(guild.default_role, read_messages=False)
    for subject in options:
        channel = await category.create_text_channel(name=f'{subject[0]}')
        await channel.set_permissions(find(lambda r: r.name == f'{subject[0]} - {semester}', guild.roles), read_messages=True)

async def createCategoryParcours(guild, parcours, parcours_groupes_peip2, semester, year_name):
    category = await guild.create_category(name=f'════ parcours - {year_name} ════', position=4)
    await category.set_permissions(guild.default_role, read_messages=False)
    for subject in parcours:
        channel = await category.create_text_channel(name=f'{subject}')
        for i in range(1,len(parcours_groupes_peip2)+1):
            if subject == parcours_groupes_peip2[i-1]:
                await channel.set_permissions(find(lambda r: r.name == f'Groupe {i} - {semester}', guild.roles), read_messages=True)

async def createCategoryAnglais(guild, groupes_anglais, semester, year_name):
    category = await guild.create_category(name=f'════ anglais - {year_name} ═════', position=4)
    await category.set_permissions(guild.default_role, read_messages=False)
    for groupe in groupes_anglais:
        channel = await category.create_text_channel(name=f'groupe {groupe}')
        await channel.set_permissions(find(lambda r: r.name == f'Anglais groupe {groupe} - {semester}', guild.roles), read_messages=True)
