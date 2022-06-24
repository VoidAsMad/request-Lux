import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext  
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow
import asyncio
import random
import os
import sys
import urllib.request
import json
from replit import db
from PIL import Image
from io import BytesIO
import requests


prefixs = '봇의 접두사를 입력해주세요!'
token = '봇의 토큰을 입력해주세요!'

bot = commands.Bot(command_prefix=prefixs, intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)



@bot.event
async def on_ready():
  print('로딩완료')
  await bot.change_presence(activity=discord.Game("미용실 관리"))







@bot.event
async def on_component(ctx):
  id = ctx.custom_id

  if id == 'pichelp':
    try:
      value = db[f"{ctx.author.id}"]
    except:
      value = 0
    if value == 1:
      await ctx.send('이미 의뢰가 신청되어 있는 상태입니다!', hidden = True)
      return None
    category = discord.utils.get(ctx.guild.categories, name="상담")
    guild = ctx.guild
    msg = await guild.create_text_channel(f"{ctx.author.name}님의 의뢰(그림)", category = category)
    await msg.set_permissions(ctx.author,speak=True,send_messages=True,read_message_history=True,read_messages=True)


  if id == "close":
    if ctx.author.guild_permissions.administrator:
      await ctx.send('의뢰가 정상적으로 종료하였습니다.\n> 3초후 채널이 삭제됩니다.')
      await asyncio.sleep(3)
      channel = bot.get_channel(ctx.channel.id)
      await channel.delete()
      return
  
    else:
      await ctx.send("의뢰완료는 관리자만 가능합니다.", hidden = True)
      return

    chan = bot.get_channel(msg.id)
    embed = discord.Embed(title="상담 신청이 완료되었습니다!", description = f"<@&989792363566215199>또는 <@&989792415676264458>가 곧 연락이 갈 예정입니다.")
    embed.add_field(name="미리 준비해주세요!", value=f"```\n1. 종류\n2. 요구사항\n3. 구상도\n4. 밝기 정도\n```", inline=False)
    await chan.send(f'{ctx.author.mention}',embed=embed)
    chan = bot.get_channel(989793794859864104)
    await chan.send(f"<@&989792363566215199> <@&989792415676264458>님 의뢰가 들어왔어요!\n<#{msg.id}>")
    await ctx.send(f"상담채널이 생성되었습니다! <#{msg.id}>", hidden = True)
    db[f"{ctx.author.id}"] = 1
    return

  if id == 'ritouching':
    try:
      value = db[f"{ctx.author.id}"]
    except:
      value = 0
    if value == 1:
      await ctx.send('이미 의뢰가 신청되어 있는 상태입니다!', hidden = True)
      return None
    category = discord.utils.get(ctx.guild.categories, name="상담")
    guild = ctx.guild
    msg = await guild.create_text_channel(f"{ctx.author.name}님의 의뢰(리터칭)", category = category)
    await msg.set_permissions(ctx.author,speak=True,send_messages=True,read_message_history=True,read_messages=True)
    

    chan = bot.get_channel(msg.id)
    embed = discord.Embed(title="상담 신청이 완료되었습니다!", description = f"<@&989792363566215199>또는 <@&989792415676264458>가 곧 연락이 갈 예정입니다.")
    embed.add_field(name="미리 준비해주세요!", value=f"```\n1. 염색할 이미지\n2. 요구사항(구체적으로)\n```", inline=False)
    await chan.send(f'{ctx.author.mention}',embed=embed)
    chan = bot.get_channel(989793794859864104)
    await chan.send(f"<@&989792363566215199> <@&989792415676264458>님 의뢰가 들어왔어요!\n<#{msg.id}>")
    await ctx.send(f"상담채널이 생성되었습니다! <#{msg.id}>", hidden = True)
    db[f"{ctx.author.id}"] = 1
    return




@slash.slash(name="의뢰상태", description = "자신이 현재 의뢰가 되어 있는 상태인지 체크합니다.", guild_ids=[987973946706133072])
async def 의뢰상태(ctx):
  try:
      value = db[f"{ctx.author.id}"]   
  except:
      value = 0

  if value == 1:
      await ctx.send(f'<@{ctx.author.id}>님은 의뢰신청이 되어 있는 상태입니다')
  else:
      await ctx.send(f'<@{ctx.author.id}>님은 의뢰신청이 되어 있지 않은 상태입니다')

@slash.slash(name="의뢰종료", description = "의뢰를 강제종료합니다.(오류발생시에만 사용하세요)", guild_ids=[987973946706133072], default_permission = False)
async def 의뢰종료(ctx, user : discord.Member):
  db[f"{user.id}"] = 0
  await ctx.send(f'<@{user.id}>님의 의뢰를 종료하였습니다.')

  

@slash.slash(name="의뢰완료", description = "반드시!!! 의뢰인의 채널에서만 사용하세요!!!(대신 channel에 의뢰인의 채널을 넣으면 무시)", guild_ids=[987973946706133072], default_permission = False)
async def 의뢰완료(ctx, 의뢰인 : discord.Member, channel : discord.TextChannel = None):
  await ctx.send('의뢰가 정상적으로 종료되었습니다.\n곧 채널이 삭제됩니다...')
  await asyncio.sleep(3)

  if channel == None:
    ch = ctx.channel.id

  else:
    ch == channel.id

    
  channel = bot.get_channel(ch)
  db[f"{의뢰인.id}"] = 0
  await channel.delete()
  return







  
#docs
@bot.event
async def on_member_join(member):
    image = Image.open("image.png")
    profile_bytes = BytesIO(requests.get(member.avatar_url).content)
    profile = Image.open(profile_bytes)
    
    profile = profile.convert('RGBA').resize((400, 400))
    image.paste(profile, (1450, 300))
    final = image
    final_bytes = BytesIO()
    final.save(final_bytes, 'png')
    final_bytes.seek(0)
    file = discord.File(fp=final_bytes, filename='image.png')
    ctx = bot.get_channel(989045536738922506)
    await ctx.send(f'{member.mention}님이 미용실에 입장하셨습니다!', file = file)

@slash.slash(name="clear", description = "메세지를 삭제합니다.", guild_ids=[987973946706133072], default_permission = False)
async def clear(ctx, amount : int):
  amounts = amount + 1
  await ctx.channel.purge(limit=amounts)
  msg = await ctx.send(f'{amount}개의 메세지를 삭제하였습니다.')
  await asyncio.sleep(3.0)
  await msg.delete()


@bot.command()
@commands.has_permissions(administrator=True)
async def 신청광고(ctx):
  embed = discord.Embed(title=f"의뢰(그림) 안내", description = "", color = 0xDC3462)
  embed.add_field(name=f"⚠️주의사항", value=f"1. 양식에 맞춰 작성해주세요\n2. 최대한 자세하게 작성해주세요\n3. 주인장의 사심이 가득 들어갈 수 있는 점 유의해주세요.\n4. **재촉 금지입니다**\n5. 장난으로 누르면 __최대 밴__입니다", inline=False)
  buttons = [
    create_button(style=ButtonStyle.gray, label="의뢰 신청하기", custom_id = 'pichelp')
  ]
  action_row = create_actionrow(*buttons)
  await ctx.send(embed = embed,components=[action_row])

@bot.command()
@commands.has_permissions(administrator=True)
async def 원신청광고(ctx):
  embed = discord.Embed(title=f"의뢰(리터칭) 안내", description = "", color = 0xDC3462)
  embed.add_field(name=f"⚠️주의사항", value=f"1. 양식에 맞춰 작성해주세요\n2. 최대한 자세하게 작성해주세요\n3. 주인장의 사심이 가득 들어갈 수 있는 점 유의해주세요.\n4. **재촉 금지입니다**\n5. 장난으로 누르면 __최대 밴__입니다", inline=False)
  buttons = [
    create_button(style=ButtonStyle.gray, label="의뢰 신청하기", custom_id = 'ritouching')
  ]
  action_row = create_actionrow(*buttons)
  await ctx.send(embed = embed,components=[action_row])


bot.run(token)
