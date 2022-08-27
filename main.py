import os
import datetime
import discord
from discord.ext import commands
from dotenv import load_dotenv
from typing import Any
import constants.channels as channels

load_dotenv('./.env')
BOT_TOKEN = os.getenv('TOKEN')

# intents = discord.Intents.all()

bot = commands.Bot(command_prefix='~')

@bot.command(name='ping')
async def _ping(ctx, *args):
    print(type(ctx))
    await ctx.send('pong')

@bot.command(name='upload')
async def _image_reupload(ctx: commands.Context, *args):
    f = await ctx.message.attachments[0].to_file()
    embed = discord.Embed()
    embed.set_image(url=f"attachment://{f.filename}")
    channel: discord.TextChannel = bot.get_channel(channels.LIBRARY_TEST)
    await channel.send(file=f, embed=embed)


async def _get_response(ctx: commands.Context, prompt: str) -> discord.Message:
    def check(message: discord.Message):
        return message.channel == ctx.channel and message.author != ctx.me

    await ctx.send(prompt)
    response: discord.Message = await bot.wait_for('message', check=check)
    return response

@bot.command(name='add_game')
async def add_game(ctx: commands.Context, *args):

    title_msg = await _get_response(ctx, 'What is the title of the game?')
    description_msg = await _get_response(ctx, 'Give me a short description of the game')
    duration_msg = await _get_response(ctx, 'How long will the game last (in minutes)?')
    player_count_msg = await _get_response(ctx, 'How many players can play at once (ex. 2-4)?')
    image_msg = await _get_response(ctx, 'Please upload an image of the game.')

    title = title_msg.content
    description = description_msg.content
    duration = int(duration_msg.content)
    player_count = player_count_msg.content
    image = await image_msg.attachments[0].to_file()

    channel: discord.TextChannel = bot.get_channel(channels.LIBRARY_TEST)
    game_duration: datetime.timedelta = datetime.timedelta(minutes=duration)
    game_message: str = f'```Game: {title}\nEst. Game Time: {game_duration}\nNo. of Players: {player_count}\nDescription: {description}```'
    await channel.send(game_message, file=image)
    
async def _send_to_library(title: str, playtime: int, player_count: str, description: str, game_image: discord.File):
    channel: discord.TextChannel = bot.get_channel(channels.LIBRARY_TEST)
    game_duration: datetime.timedelta = datetime.timedelta(minutes=playtime)
    game_message: str = f'```Game: {title}\nEst. Game Time: {game_duration}\nNo. of Players: {player_count}\nDescription: {description}```'

    await channel.send(game_message, file=game_image)


# bot.add_cog(Misc(bot))
# bot.add_cog(Suggestions(bot))
# bot.add_cog(Verification(bot, os.getcwd() + "/authentication/forms/"))
# bot.add_cog(Nickname(bot))
# bot.add_cog(InviteRole(bot))
# bot.add_cog(Stats(bot))
# bot.add_cog(Maintenance(bot))

@bot.event
async def on_ready():
    print("Ready!")
    # invite_object = InviteRole(bot)
    # await invite_object.first_run()
    print("Initialized Sponsor Invite Uses")

# @bot.event
# async def on_member_remove(member):
#     invite_object = InviteRole(bot)
#     await invite_object.first_run()
#     modmail_channel = await bot.fetch_channel(channels.MODMAIL_LOG)
#     channel_message = f'Member {member} left the server. Refreshing cache.'
#     await modmail_channel.send(channel_message)


bot.run(BOT_TOKEN)
