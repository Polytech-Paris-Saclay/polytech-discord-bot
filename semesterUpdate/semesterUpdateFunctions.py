import discord
from discord.utils import find

# ------------------ #

# Peip1 - Peip2
async def createRoleGroupeAnglais(guild, groupe_anglais, semester):
    await guild.create_role(name=f'Anglais groupe {groupe_anglais} - {semester}', colour=discord.Colour(0x269407))

async def createRoleGroupeTDTP(guild, groupe, semester):
    await guild.create_role(name=f'Groupe {groupe} - {semester}', colour=discord.Colour.random())

async def createRoleOption(guild, option, semester):
    await guild.create_role(name=f'{option[0]} - {semester}', colour=discord.Colour.yellow())

# 3eme année - 5eme année
async def createRoleGroupeTroncCommunAPP(guild, year_name, groupe):
    await guild.create_role(name=f'Groupe TC {groupe} - APP{year_name[0]}', colour=discord.Colour.random())

async def createRoleGroupeAnglaisComAPP(guild, year_name, groupe):
    await guild.create_role(name=f'Groupe AnCom {groupe} - APP{year_name[0]}', colour=discord.Colour(0x269407))

async def createRoleSpecialiteAPP(guild, year_name, specialite):
    await guild.create_role(name=f'{specialite} - APP{year_name[0]}', colour=discord.Colour(0x001368))

async def createRoleSpecialiteET(guild, year_name, specialite):
    await guild.create_role(name=f'{specialite} - ET{year_name[0]}', colour=discord.Colour(0x001368))


# ------------------ #

# only works for Peip1 - Peip2
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
    if this_category is not None:
        for channel in this_category.channels:
            if channel.last_message_id is not None:
                await channel.edit(category=archive_category)
                await channel.set_permissions(guild.default_role, read_messages=True)
            else :
                await channel.delete()
        await this_category.delete()

# ------------------ #

# Peip1 - Peip2

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
        role = discord.utils.get(guild.roles, name=f'Groupe {i} - {semester}')
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            role: discord.PermissionOverwrite(read_messages=True)
        }
        await category.create_text_channel(name=f'groupe {i}', overwrites=overwrites)

async def createCategoryOptions(guild, options, semester):
    category = await guild.create_category(name=f'══════ Option - {semester} ══════', position=4)
    await category.set_permissions(guild.default_role, read_messages=False)
    for subject in options:
        role = discord.utils.get(guild.roles, name=f'{subject[0]} - {semester}')
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            role: discord.PermissionOverwrite(read_messages=True)
        }
        await category.create_text_channel(name=f'{subject[0]}', overwrites=overwrites)

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
        role = discord.utils.get(guild.roles, name=f'Anglais groupe {groupe} - {semester}')
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            role: discord.PermissionOverwrite(read_messages=True)
        }
        await category.create_text_channel(name=f'groupe {groupe}', overwrites=overwrites)

# 3eme année - 5eme année

async def createCategoryTroncCommunAPP(guild, tronc_commun_APP, year_name, groupes_tc_app):
    category = await guild.create_category(name=f'══ Tronc commun - APP{year_name[0]} ══', position=4)
    await category.set_permissions(guild.default_role, read_messages=False)
    for groupe in groupes_tc_app:
        await category.set_permissions(find(lambda r: r.name == f'Groupe TC {groupe} - APP{year_name[0]}', guild.roles), read_messages=True)
    for subject in tronc_commun_APP:
        await category.create_text_channel(name=f'{subject}')

async def createCategoryAnglaisComAPP(guild, nbr_gr_anglais_com_APP, year_name):
    category = await guild.create_category(name=f'═══ Anglais com - APP{year_name[0]} ═══', position=4)
    await category.set_permissions(guild.default_role, read_messages=False)
    for groupe in range(1, nbr_gr_anglais_com_APP+1):
        role = discord.utils.get(guild.roles, name=f'Groupe AnCom {groupe} - APP{year_name[0]}')
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            role: discord.PermissionOverwrite(read_messages=True)
        }
        await category.create_text_channel(name=f'Anglais groupe {groupe}', overwrites=overwrites)
        await category.create_text_channel(name=f'Communication groupe {groupe}', overwrites=overwrites)

async def createCategoryGroupeTroncCommunAPP(guild, groupes_tc_app, year_name):
    category = await guild.create_category(name=f'════ Groupe TC - APP{year_name[0]} ════', position=4)
    await category.set_permissions(guild.default_role, read_messages=False)
    for groupe in groupes_tc_app:
        channel = await category.create_text_channel(name=f'Groupe {groupe}')
        await channel.set_permissions(find(lambda r: r.name == f'Groupe TC {groupe} - APP{year_name[0]}', guild.roles), read_messages=True)

async def createCategorySpecialiteAPP(guild, year_name, specialites, subjects):
    category = await guild.create_category(name=f'══════ Spe - APP{year_name[0]} ═══════', position=4)
    await category.set_permissions(guild.default_role, read_messages=False)
    for specialite in specialites:
        role = discord.utils.get(guild.roles, name=f'{specialite} - APP{year_name[0]}')
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            role: discord.PermissionOverwrite(read_messages=True)
        }
        for subject in subjects[f"specialite_app_{specialite}"]:
            await category.create_text_channel(name=f'{subject}', overwrites=overwrites)

# ------------------ #

async def deletePreviousRoles(guild, previous_semester):
    for role in guild.roles:
        if previous_semester in role.name:
            await role.delete()

async def createNewRoles(guild, semester, year_name, roles, subjectDatabase, semesterUpdateInstructions): 
    # Peip1 - Peip2
    nbr_groupes = semesterUpdateInstructions[year_name]['nbr_groupes'] if 'nbr_groupes' in semesterUpdateInstructions[year_name] else None
    groupes_anglais = semesterUpdateInstructions[year_name]['groupes_anglais'] if 'groupes_anglais' in semesterUpdateInstructions[year_name] else None
    # 3eme année 
    specialites = semesterUpdateInstructions[year_name]['specialites'] if 'specialites' in semesterUpdateInstructions[year_name] else None
    nbr_groupes_anglais_com_app = semesterUpdateInstructions[year_name]['nbr_groupes_anglais_com_app'] if 'nbr_groupes_anglais_com_app' in semesterUpdateInstructions[year_name] else None
    groupes_tc_app = semesterUpdateInstructions[year_name]['groupes_tc_app'] if 'groupes_tc_app' in semesterUpdateInstructions[year_name] else None

    for role in roles:
        match role:
            case 'anglais' : 
                for groupe in groupes_anglais:
                    await createRoleGroupeAnglais(guild, groupe, semester)
            case 'TDTP' :
                for groupe in range(1, nbr_groupes+1):
                    await createRoleGroupeTDTP(guild, groupe, semester)
            case 'options' :
                for option in subjectDatabase[semester]['options']:
                    await createRoleOption(guild, option, semester)
            case 'tronc_commun_APP' :
                for groupe in groupes_tc_app:
                    await createRoleGroupeTroncCommunAPP(guild, year_name, groupe)
            case 'anglais_com_APP' :
                for groupe in range(1, nbr_groupes_anglais_com_app+1):
                    await createRoleGroupeAnglaisComAPP(guild, year_name, groupe)
            case 'specialite_APP' : 
                for specialite in specialites:
                    await createRoleSpecialiteAPP(guild, year_name, specialite)
            case 'specialite_ET' :
                for specialite in specialites:
                    await createRoleSpecialiteET(guild, year_name, specialite)



async def archivePreviousCategories(guild, previous_semester, year, previous_year, categories_to_archive):
    #if previous semester number is not pair, year is the same, else year is the previous year
    year = year if int(previous_semester[1]) % 2 != 0 else [int(year[0])-1, int(year[1])-1]
    archive_category_name = f'═ [Archives {previous_semester} - {int(year[0])}/{int(year[1])}] ═'
    archive_category = find(lambda c: c.name == archive_category_name, guild.categories)
    if archive_category is None:
        archive_category = await guild.create_category(name=archive_category_name)
        await archive_category.set_permissions(find(lambda r: r.name == f'Accès aux archives', guild.roles), read_messages=True)
    discord_categories_to_archive = [
        f'═══ Tronc commun - {previous_semester} ═══' if category_name == 'tronc_commun' else
        f'══════ Option - {previous_semester} ══════' if category_name == 'options' else
        f'════ parcours - {previous_year} ════' if category_name == 'parcours' else
        f'════ anglais - {previous_year} ═════' if category_name == 'anglais' else
        f'═══ Groupe TD/TP - {previous_semester} ════' if category_name == 'TDTP' else
        None
        for category_name in categories_to_archive
    ]
    for category in discord_categories_to_archive:
        await archiveThisCategory(guild, category, archive_category)

async def createNewCategories(guild, semester, categories, role_year, semesterUpdateInstructions, year_name, subjectDatabase):
    # Peip1 - Peip2
    nbr_groupes = semesterUpdateInstructions[year_name]['nbr_groupes'] if 'nbr_groupes' in semesterUpdateInstructions[year_name] else None
    parcours_groupes = semesterUpdateInstructions[year_name]['parcours_groupes'] if 'parcours_groupes' in semesterUpdateInstructions[year_name] else None
    groupes_anglais = semesterUpdateInstructions[year_name]['groupes_anglais'] if 'groupes_anglais' in semesterUpdateInstructions[year_name] else None
    # 3eme année - 5eme année
    nbr_groupes_anglais_com_app = semesterUpdateInstructions[year_name]['nbr_groupes_anglais_com_app'] if 'nbr_groupes_anglais_com_app' in semesterUpdateInstructions[year_name] else None
    groupes_tc_app = semesterUpdateInstructions[year_name]['groupes_tc_app'] if 'groupes_tc_app' in semesterUpdateInstructions[year_name] else None
    specialites = semesterUpdateInstructions[year_name]['specialites'] if 'specialites' in semesterUpdateInstructions[year_name] else None


    for category in categories:
        match category:
            case "tronc_commun" : await createCategoryTroncCommun(guild, subjectDatabase[semester]['tronc_commun'], semester, role_year)
            case "TDTP" : await createCategoryGroupeTDTP(guild, nbr_groupes, semester)
            case "options" : await createCategoryOptions(guild, subjectDatabase[semester]['options'], semester)
            case "parcours" : await createCategoryParcours(guild, subjectDatabase[semester]['parcours'], parcours_groupes, semester, year_name)
            case "anglais" : await createCategoryAnglais(guild, groupes_anglais, semester, year_name)
            case "tronc_commun_APP" : await createCategoryTroncCommunAPP(guild, subjectDatabase[semester]['tronc_commun_app'], year_name, groupes_tc_app)
            case "anglais_com_APP" : await createCategoryAnglaisComAPP(guild, nbr_groupes_anglais_com_app , year_name)
            case "specialite_APP" : await createCategorySpecialiteAPP(guild, year_name, specialites, subjectDatabase[semester])
            case "groupe_tc_APP" : await createCategoryGroupeTroncCommunAPP(guild, groupes_tc_app, year_name)