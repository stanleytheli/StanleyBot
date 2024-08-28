import discord
from discord.ext import commands

tokenFile = "C:/Users/stanl/OneDrive/Desktop/python programs/discordBot/token.txt"

intents = discord.Intents.all()

client = discord.Client(intents = intents)
bot = commands.Bot(command_prefix = "!", intents = intents)
defaultRoles = {}

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'We have logged in as {bot.user}')

@bot.tree.command(name = "setdefaultrole", description = "Sets the default role, will be given to all joining users.")
async def _set_default_role(interaction : discord.Interaction, role : discord.Role):
    defaultRoles[interaction.guild.id] = role
    await interaction.response.send_message("Default role set.")

@bot.tree.command(name = "removedefaultrole", description = "Sets the default role to none.")
async def _remove_default_role(interaction : discord.Interaction):
    del defaultRoles[interaction.guild.id]
    await interaction.response.send_message("Removed default role.")

@bot.tree.command(name = "getdefaultrole", description = "Print the name of the default role.")
async def _get_default_role(interaction : discord.Interaction):
    if (id := interaction.guild.id) in defaultRoles:
        await interaction.response.send_message(f"This server's default role is {defaultRoles[id].name}")
    else:
        await interaction.response.send_message("This server has no default role. Use /setdefaultrole to set a default role.")

@bot.tree.command(name = "applydefaultrole", description = "Assigns the default role to all users without roles.")
async def _apply_default_role(interaction : discord.Interaction):
    if (id := interaction.guild.id) in defaultRoles:
        defaultRole = defaultRoles[id]
    else:
        return
    
    rolesGiven = 0
    async for member in interaction.guild.fetch_members(limit = None):
        print(member.name + " : " + (str)(len(member.roles)))
        try:
            if len(member.roles) == 1:
                await member.add_roles(defaultRole, reason = "Default role applied")
                rolesGiven += 1
        except RuntimeError:
            print(member.name + "caused an issue!")
            
    await interaction.response.send_message(f"Default role updated. Assigned {(str)(rolesGiven)} users the {defaultRole.name} role.")

@bot.tree.command(name = "assignrole", description = "Assign a role to a member")
async def _assign_role(interaction : discord.Interaction, member : discord.Member, role : discord.Role):
    try:
        await member.add_roles(role)
        await interaction.response.send_message(f"Assigned {role.name} to @{member.name}.")
    except:
        await interaction.response.send_message("Error, role assignment failed.")

@bot.tree.command(name = "removerole", description = "Remove a role from a member")
async def _remove_role(interaction : discord.Interaction, member : discord.Member, role : discord.Role):
    try:
        await member.remove_roles(role)
        await interaction.response.send_message(f"Removed {role.name} from @{member.name}")
    except:
        await interaction.response.send_message("Error, role removal failed.")


@bot.event
async def on_member_join(member : discord.Member):
    
    if (id := member.guild.id) in defaultRoles:
        await member.add_roles(defaultRoles[id], reason = "Default role applied")


@bot.tree.command(name = "boop")
async def _boop(interaction : discord.Interaction, boop_target : discord.User):
    await interaction.response.send_message("<@" + (str)(boop_target.id) + f"> Boop! You were booped by {interaction.user.name}!")

@bot.tree.command(name = "getmembercount")
async def _get_member_count(interaction : discord.Interaction):
    count = (str) (interaction.guild.member_count)
    await interaction.response.send_message("Members: " + count)

@bot.tree.command(name = "createnewinvite")
async def _create_new_invite(interaction : discord.Interaction):
    invite = (str) (await interaction.channel.create_invite(reason = f"@{interaction.user} ran /create_new_invite command", unique = True))
    await interaction.response.send_message("Here's a new invite link: " + invite)

@bot.tree.command(name = "getinvite")
async def _get_invite(interaction : discord.Interaction):
    invite = (str) (await interaction.channel.create_invite(reason = f"@{interaction.user} ran /get_invite command", unique = False))
    await interaction.response.send_message("Here's this server's invite link: " + invite)

@bot.tree.command(name = "sayhello")
async def _say_hello(interaction : discord.Interaction):
    await interaction.response.send_message(f"Hello {interaction.user.name}!")

@bot.tree.command(name = "kill")
async def _kill(interaction : discord.Interaction):
    print("Bot closed!")
    await interaction.response.send_message("Closing bot.")
    await bot.close()

@bot.event
async def on_message(message : discord.Message):
    if message.author == bot.user:
        return
    
    #Important piece of code
    if message.author.id == 694990501375377460:
        await message.channel.send("Shut up HelloComrade")

bot.run(open(tokenFile).read())