import discord
from discord.ext import commands
from discord import app_commands
from os import linesep
import discord.ui as ui
from discord.interactions import Interaction

intents = discord.Intents().all()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="$", intents=intents)
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client=client)

class cadastro(ui.Modal, title = "Modal de ex"):
    usuario = ui.TextInput(label="Usuario:", style= discord.TextStyle.short, required=True, max_length=8)
    senha = ui.TextInput(label="Senha:", style= discord.TextStyle.long, required=True, max_length=8)  
    async def on_submit(self, interaction: Interaction):
        await interaction.response.send_message("Cadastro bem sucedido!")


@bot.event
async def on_ready():
    synced = await bot.tree.sync(guild=discord.Object(id=None))    
    print(f"O bot {bot.user.name} já está pronto!\nSincronizando {len(synced)} comando(s)")

@bot.tree.command(guild=discord.Object(id=None), name='regras', description='Não tem descrição!')
async def slash_command1(interaction: discord.Interaction):
    channel = bot.get_channel(None)
    await channel.send(f"As regras são:{linesep}1-Não desrespeitar os outros{linesep}2-Não fazer spam de mensagems{linesep}3-Não fazer propaganda!")
    await interaction.response.send_message(f"As regras foram enviadas para o canal {channel.mention}")

@bot.tree.command(guild=discord.Object(id=None), name='denunciar', description='Não tem descrição!')
async def slash_command2(interaction: discord.Interaction, user: discord.Member, *, denuncia:str = None):
    if denuncia is None:
        denuncia = "Denuncia sem razão"
    await user.send(f"O usuário {interaction.user.mention} fez uma denúncia contra você!{linesep}O motivo foi: `{denuncia}`!")

@bot.tree.command(guild=discord.Object(id=None), name="apagar", description="Comando para apagar mensagens, apenas admins podem usar este comando")
async def slash_command3(interaction:discord.Interaction, quantidade:int):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("Você não tem permissão para usar esse comando.", ephemeral=True)
        msg =  msg = await bot.fetch_user(interaction.guild.owner.id)
        await msg.send(f"O usuario {interaction.user.mention} tentou usar um comando de administrador!")
        return

    await interaction.response.send_message("Apagando.")
    await interaction.channel.purge(limit=quantidade+1)

@bot.tree.command(guild=discord.Object(id=None), name="banir", description="Comando para banir membros, apenas admins podem usar este comando")
async def slash_command4(interaction:discord.Interaction, user:discord.Member, reason:str = None):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("Você não tem permissão para usar esse comando.", ephemeral=True)
        msg =  msg = await bot.fetch_user(interaction.guild.owner.id)
        await msg.send(f"O usuario {interaction.user.mention} tentou usar um comando de administrador!")
        return
    
    if reason is None:
        reason = "Nenhuma razão fornecida"

    
    await user.send(f"O usuário {interaction.user.mention} te baniu do servidor!{linesep}O motivo foi: `{reason}`!")
    await interaction.guild.ban(user, reason=reason)
    

@bot.tree.command(guild=discord.Object(id=None), name="expulsar", description="Comando para expulsar membros, apenas admins podem usar este comando")
async def slash_command5(interaction:discord.Interaction, user:discord.Member, reason:str = None):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("Você não tem permissão para usar esse comando.", ephemeral=True)
        msg =  msg = await bot.fetch_user(interaction.guild.owner.id)
        await msg.send(f"O usuario {interaction.user.mention} tentou usar um comando de administrador!")
        return
    
    if reason is None:
        reason = "Nenhuma razão fornecida"

    
    await user.send(f"O usuário {interaction.user.mention} te expulsou do servidor!{linesep}O motivo foi: `{reason}`!")
    await interaction.guild.kick(user=user, reason=reason)
    
@tree.command(guild=discord.Object(id=None), name="modal", description="Modal de cadastro") 
async def modal(interaction:discord.Interaction):
    await interaction.response.send_modal(cadastro())   













    
    
    
bot.run("None")

