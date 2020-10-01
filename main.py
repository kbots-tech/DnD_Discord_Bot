import os
import json
import discord
import discord.utils
import difflib
import re
import random

from keep_alive import keep_alive
from discord.ext import commands

armorData = []
classData = []
spellData = []
weaponData = []
monsterData = []
raceData=[]
conditionData=[]
characters = []
message_num = 757046756478287882;


bot = commands.Bot(
 command_prefix=">",  # Change to desired prefix
 case_insensitive=True  # Commands aren't case-sensitive
)
bot.remove_command("Help")

bot.author_id = 480055359462178826  # Change to your discord id!!!

@bot.command()
async def ping(ctx):
    await ctx.send('Pong! {0}'.format(round(bot.latency, 1)))

@bot.command()
async def help(ctx):
    embed=discord.Embed(title='Help',description='Replace (Args) with an item name for a specific one or list for list of options\nSpelling can be slightly off for names the bot will search through for the best match')
    embed.set_footer(text = "Find Out More On Open5E")
    embed.add_field(name='>spell (args)',value='Returns a spell',inline=False)
    embed.add_field(name='>armor (args)',value='Returns an armor type',inline=False)
    embed.add_field(name='>weapon (args)',value='Returns a weapon',inline=False)
    embed.add_field(name='>race (args)',value='Returns a race',inline=False)
    embed.add_field(name='>class (args)',value='Returns a class',inline=False)
    embed.add_field(name='>condition (args)',value='Returns a condition',inline=False)
    embed.add_field(name='>roll (args)',value='Rolls a dice \nFormatting is (num dice)d(type of dice)+(optional modifier)\nEg: 4d12+3',inline=False)
    embed.add_field(name='>create (args)',value='Use this command to create a channel for your games on the server. Please note admins can still see these channels and normal club rules apply',inline=False)
    embed.add_field(name='>invite (user)',value='Use this command to add users to your game, this command will only work in channels created using the >create command',inline=False)
    embed.add_field(name='>leave',value='Use this command to leave a private channel for games, to rejoin someone in the channel will need to add you again',inline=False)
    await ctx.send(embed=embed)
    
@bot.command()
@commands.has_any_role("Bot Wrangler","Admin")
async def adminhelp(ctx):
    id = str(ctx.message.author.id)
    user = bot.get_user(int(id))
    embed=discord.Embed(title='Admin Help',description="Wow you must be one cool dude to see this help list here's your fancy admin help list")
    embed.set_footer(text = "Find Out More On Open5E")
    embed.add_field(name='>delete',value='When used in a channel created for a game this will delete the channel and role that goes with it',inline=False)
    embed.add_field(name='>setup',value='This will setup the table for role reactions if that ever gets broken for some reason',inline=False)
    await ctx.message.delete()
    await user.send(embed=embed)
        
@bot.command(aliases=["armors",'a'])
async def armor(ctx,*,args):
    id = str(ctx.message.author.id)
    user = bot.get_user(int(id))
    await ctx.send(user.mention+ ' Looking for armor')
    print('command get')
    global armorData
    if args == 'list':
        embed=discord.Embed(title='Armor List',url = 'https://open5e.com/sections/armor')
        embed.set_footer(text = "Find Out More On Open5E")
        embed.set_image(url="https://open5e.com/favicon.ico")

        with open('armor.json') as json_file:
            data = json.load(json_file)
            for p in data:
                embed.add_field(name='Name: ',value=p['name'],inline=True)
        await ctx.send(embed=embed)
    else:
        x= difflib.get_close_matches(args,armorData,10,0.6)
        matches=discord.Embed(title='Others Armor Matches',url = 'https://open5e.com/sections/armor',description="Not what your looking for? Try one of these")
        matches.set_footer(text = "Find Out More On Open5E")
        for d in x:
          matches.add_field(name = 'Armor Name',value = d)
       
        try:
            dateset = []
            print(x[0])
            with open('armor.json') as json_file:
                data = json.load(json_file)
                for p in data:
                    #print(p['name'])
                    if p['name'] == x[0]:
                        print('match found')
                        name = p['name']
                        rarity = 'n/a'
                        ac = 'n/a'
                        atype= 'n/a'
                        try:
                            rarity = p['rarity']
                            if rarity == '':
                              rarity = 'n/a'
                        except:
                            print('n/a')
                        try:
                            atype = p['type']
                        except:
                            print('n/a')
                        try:
                            ac = str(p['ac'])
                        except:
                            print('n/a')
                        try:
                            cost = p['cost']
                        except:
                            print('n/a')
                        try:
                            requirements = str(p['requirements'])
                        except:
                            print('n/a')

                        requirements = requirements.replace("{","")
                        requirements = requirements.replace("}",",")
                        if requirements == ',':
                            requirements = 'none'

                        embed=discord.Embed(title=name,url = 'https://open5e.com/sections/armor')
                        embed.set_footer(text = "Find Out More On Open5E")
                        embed.set_image(url="https://open5e.com/favicon.ico")
                        embed.add_field(name='Type',value=atype,inline=True)
                        embed.add_field(name="AC", value=ac, inline=True)
                        embed.add_field(name='Rarity',value=rarity,inline=False)
                        embed.add_field(name='Cost',value=cost,inline=True)
                        embed.add_field(name='Requirements',value=requirements,inline=False)
                        
                        await ctx.send(embed=embed)
                        await ctx.send(embed=matches)
                        json_file.close()
                        break
                    else:
                        print('next')
        except:
            await ctx.send('No Armor found for this value')

@bot.command(aliases=["spells",'s'])
async def spell(ctx,*,args):
    id = str(ctx.message.author.id)
    user = bot.get_user(int(id))
    await ctx.send(user.mention+ ' Looking for spell')
    print('command get')
    global spellData
    if args == 'list':
        embed=discord.Embed(title='Spell List',url = 'https://open5e.com/spells/spells-table',description= 'Click the link for full spell list')
        embed.set_footer(text = "Find Out More On Open5E")
        embed.set_image(url="https://open5e.com/favicon.ico")
        await ctx.send(embed=embed)
    else:
        x= difflib.get_close_matches(args,spellData,10,0.5)
        matches=discord.Embed(title='Others Spell Matches',url = 'https://open5e.com/sections/armor',description="Not what you were looking for? Try one of these")
        matches.set_footer(text = "Find Out More On Open5E")
        matches.set_footer(text = "Find Out More On Open5E")
        for d in x:
          matches.add_field(name = 'Spell Name',value = d)
        try:
            print(x[0])
            with open('spells.json') as json_file:
                data = json.load(json_file)
                for p in data:
                    #print(p['name'])
                    if p['name'] == x[0]:
                        print('match found')
                        name = p['name']

                        embed=discord.Embed(title=name,url = 'https://open5e.com/sections/armor',description=p['desc'])
                        embed.set_footer(text = "Find Out More On Open5E")
                        
                        try:
                          embed.add_field(name='Higher Levels',value= p['higher_level'],inline=False)
                        except:
                            print('n/a')
                        try:
                          embed.add_field(name='Materials',value= p['material'],inline=False)
                        except:
                            print('n/a')
                        try:
                          embed.add_field(name='Components: ',value= p['components'],inline=True)
                        except:
                            print('n/a')
                        try:
                          embed.add_field(name='Range',value= p['range'],inline=True)
                        except:
                            print('n/a')
                        try:
                          embed.add_field(name='Page',value= p['page'],inline=True)
                        except:
                            print('n/a')
                        try:
                          embed.add_field(name='Ritual',value= p['ritual'],inline=True)
                        except:
                            print('n/a')
                        try:
                          embed.add_field(name='Duration',value= p['duration'],inline=True)
                        except:
                            print('n/a')
                        try:
                          embed.add_field(name='Concentration',value= p['concentration'],inline=True)
                        except:
                            print('n/a')
                        try:
                          embed.add_field(name='Casting Time',value= p['casting_time'],inline=True)
                        except:
                            print('n/a')
                        try:
                          embed.add_field(name='Level',value= p['level'],inline=True)
                        except:
                            print('n/a')
                        try:
                          embed.add_field(name='School',value= p['school'],inline=True)
                        except:
                            print('n/a')
                        try:
                          embed.add_field(name='Class',value= p['class'],inline=True)
                        except:
                            print('n/a')
                        try:
                          embed.add_field(name='Archetype',value= p['archetypy'],inline=True)
                        except:
                            print('n/a')
                        
                        
                        
                        
                        
                        
                        await ctx.send(embed=embed)
                        await ctx.send(embed=matches)
                        json_file.close()
                        break
                    else:
                        print('next')
        except:
            await ctx.send('No Spells found for this value')

@bot.command(aliases=["class",'c'])
async def classes(ctx,*,args):
  id = str(ctx.message.author.id)
  user = bot.get_user(int(id))
  await ctx.send(user.mention + ' Looking for class')
  if args == 'list':
    embed=discord.Embed(title='Class List',url = 'https://open5e.com/classes')
    embed.set_footer(text = "Find Out More On Open5E")
    embed.set_image(url="https://open5e.com/favicon.ico")
    with open('classes.json') as json_file:
            data = json.load(json_file)
            for p in data:
                embed.add_field(name='Name: ',value=p['name'],inline=True)
    await ctx.send(embed=embed)
  
  else:
    print('command get')
    global classData
    print(classData)
    x= difflib.get_close_matches(args,classData,1,0.4)
    print(x)
    try:
      print(x[0])
      with open('classes.json') as json_file:
                data = json.load(json_file)
                for p in data:
                  if p['name']==x[0]:
                    print('match found')
                    name = p['name']
                    features= p['features']
                    json_file.close()
                    break
                  else:
                    print('next')
      embed=discord.Embed(title=name,url = 'https://open5e.com/classes')
      embed.set_footer(text = "Find Out More On Open5E")
      embed.set_image(url="https://open5e.com/classes")
  
      embed.add_field(name='Hit Dice: ',value=features['hit-dice'],inline=True)

      embed.add_field(name='HP at 1st level: ', value=features['hp-at-1st-level'],inline=True)

      embed.add_field(name='Armor proficencies: ',value=features['prof-armor'],inline=True)

      embed.add_field(name='Weapon proficencies: ',value=features['prof-weapons'],inline=True)

      embed.add_field(name='Tool proficencies: ',value=features['prof-tools'],inline=True)

      embed.add_field(name='Proficent saving throws: ',value=features['prof-saving-throws'],inline=True)

      embed.add_field(name='Proficent skills: ',value=features['prof-skills'],inline=False)

      embed.add_field(name='Starting equipment: ',value=features['equipment'],inline=False)
      
      if features['spellcasting-ability'] == '':
        features['spellcasting-ability'] = 'n/a'
      embed.add_field(name='Spellcasting Ability: ',value=features['spellcasting-ability'],inline=False)

      
      await ctx.send(embed=embed)
    except Exception as e:
      print(e)

@bot.command(aliases=["weapon",'w'])
async def weapons(ctx,*,args):
  id = str(ctx.message.author.id)
  user = bot.get_user(int(id))
  await ctx.send(user.mention + ' Looking for weapon')
  if args == 'list':
    embed=discord.Embed(title='Weapons List',url = 'https://open5e.com/sections/weapons',description = 'Click the URL for full weapon list')
    embed.set_footer(text = "Find Out More On Open5E")
    embed.set_image(url="https://open5e.com/favicon.ico")
    await ctx.send(embed=embed)

  else:
    print('command get')
    global classData
    print(classData)
    x= difflib.get_close_matches(args,weaponData,10,0.4)
    print(x)
    matches=discord.Embed(title='Others Weapon Matches',url = 'https://open5e.com/sections/weapons',description="Not what you were looking for? Try one of these")
    matches.set_footer(text = "Find Out More On Open5E")
    for d in x:
          matches.add_field(name = 'Weapon Name',value = d)
    
    try:
      print(x[0])
      with open('weapons.json') as json_file:
                data = json.load(json_file)
                for p in data:
                  if p['name']==x[0]:
                    print('match found')
                    name = p['name']
                    try:
                      embed=discord.Embed(title=name,url = 'https://open5e.com/classes')
                    except:
                      print('n/a')
                    try:
                      embed.add_field(name='Category',value=p['category'],inline=False)
                    except:
                      print('n/a')
                    try:
                      embed.add_field(name='Cost',value=p['cost'],inline=True)
                    except:
                      print('n/a')
                    try:
                      embed.add_field(name='Damage',value=p['damage_dice'],inline=True)
                    except:
                      print('n/a')
                    try:
                      embed.add_field(name='Type',value=p['damage_type'],inline=True)
                    except:
                      print('n/a')
                    try:
                      embed.add_field(name='Weight',value=p['weight'],inline=True)
                    except:
                      print('n/a')
                    properties = str(p['properties'])
                    properties = properties.replace('[',' ')
                    properties = properties.replace(']',' ')
                    
                    
                    embed.add_field(name='Properties',value=properties,inline=True)
                    json_file.close()
                    break
                  else:
                    print('next')
      
      
      await ctx.send(embed=embed)
      await ctx.send(embed=matches)
    except Exception as e:
      print(e)

@bot.command(aliases=["condition"])
async def conditions(ctx,*,args):
  id = str(ctx.message.author.id)
  user = bot.get_user(int(id))
  await ctx.send(user.mention + ' Looking for condition')
  if args == 'list':
    embed=discord.Embed(title='Weapons List',url = 'https://open5e.com/sections/conditions',description = 'Click the URL for full condition list')
    embed.set_footer(text = "Find Out More On Open5E")
    embed.set_image(url="https://open5e.com/favicon.ico")
    await ctx.send(embed=embed)

  else:
    print('command get')
    global classData
    print(classData)
    x= difflib.get_close_matches(args,conditionData,10,0.4)
    print(x)
    matches=discord.Embed(title='Others Condition Matches',url = 'https://open5e.com/sections/weapons',description="Not what you were looking for? Try one of these")
    matches.set_footer(text = "Find Out More On Open5E")
    for d in x:
          matches.add_field(name = 'Weapon Name',value = d)
    
    try:
      print(x[0])
      with open('conditions.json') as json_file:
                data = json.load(json_file)
                for p in data:
                  if p['name']==x[0]:
                    print('match found')
                    name = p['name']
                    try:
                      embed=discord.Embed(title=name,url = 'https://open5e.com/classes',description=p['desc'])
                    except:
                      print('n/a')
                    json_file.close()
                    break
                  else:
                    print('next')
      
      
      await ctx.send(embed=embed)
      await ctx.send(embed=matches)
    except Exception as e:
      print(e)

@bot.command(aliases=["monsters",'m'])
async def monster(ctx,*,args):
  id = str(ctx.message.author.id)
  user = bot.get_user(int(id))
  await ctx.send(user.mention + ' Looking for Monster')
  if args == 'list':
    embed=discord.Embed(title='Monsters List',url = 'https://open5e.com/monsters/monster-list',description= 'List not avaliable for monsters due to amount sorry :crying_cat_face: Click the link for the full list')
    embed.set_footer(text = "Find Out More On Open5E")
    embed.set_image(url="https://open5e.com/favicon.ico")
    await ctx.send(embed=embed)

  else:
    print('command get')
    x= difflib.get_close_matches(args,monsterData,10,0.4)
    print(x)
    matches=discord.Embed(title='Others Monster Matches',url = 'https://open5e.com/monsters/monster-list',description="The first match will be sent below, if it's not what your looking for try one of the others below")
    matches.set_footer(text = "Find Out More On Open5E")
    for d in x:
          matches.add_field(name = 'Monster',value = d)
    try:
      print(x[0])
      with open('monsters.json') as json_file:
                data = json.load(json_file)
                for p in data:
                  if p['name']==x[0]:
                    print('match found')
                    name = p['name']

                    try:
                      embed1=discord.Embed(title=name,url = 'https://open5e.com/classes')
                      embed2=discord.Embed(title=name +' Special Abilities')
                      embed3=discord.Embed(title=name+' Actions')
                      try:
                        desc=p['legendary_desc']
                      except:
                        desc='N/A'
                      embed4=discord.Embed(title=name+' Legendary Actions',description=desc)
                    except:
                      print('n/a')
                    #1
                    try:
                      embed1.add_field(name='Size' ,value=p['size'],inline =True )
                    except:
                      print('n/a')
                    #2
                    try:
                      embed1.add_field(name='Type' ,value=p['type'],inline =True )
                    except:
                      print('n/a')
                    #3
                    try:
                      embed1.add_field(name='Subtype',value=p['subtype'],inline =True )
                    except:
                      print('n/a')
                    #4
                    try:
                      embed1.add_field(name='Allignment' ,value=p['alignment'],inline =True )
                    except:
                      print('n/a')
                    #5
                    try:
                      embed1.add_field(name='Armor Class' ,value=p['armor_class'],inline =True )
                    except:
                      print('n/a')
                    #6
                    try:
                      embed1.add_field(name='Hit Points',value=p['hit_points'],inline =True )
                    except:
                      print('n/a')
                    #7
                    try:
                      embed1.add_field(name='Speed',value=p['speed'],inline =False )
                    except:
                      print('n/a')
                    #8
                    try:
                      abilityScores='\n\n**Strength:** '+str(p['strength'])+'----**Dexterity:** '+str(p['dexterity'])+'----**Constitution:** '+str(p['constitution'])+'----**Intelligence:** '+str(p['intelligence'])+'\n**Wisdom:** '+str(p['wisdom'])+'----**Charisma:** '+str(p['charisma'])
                      embed1.add_field(name='Ability Scores',value=abilityScores,inline =False)+'\t\tHistory: '+str(p['history'])+'\t\tPerception: '+str(p['perception'])
                    except:
                      print('n/a')
                    #14
                    try:
                      embed1.add_field(name='Constitution Saving Throw',value=p['constitution_save'],inline =True)
                    except:
                      print('n/a')
                    #15
                    try:
                      embed1.add_field(name='Intelligence Saving Throw',value=p['intelligence_save'],inline =True )
                    except:
                      print('n/a')
                     #16
                    try:
                      embed1.add_field(name='Wisdom Saving Throw',value=p['wisdom_save'],inline =True )
                    except:
                      print('n/a')
                    #19
                    try:
                      embed1.add_field(name='Damage Vulnerabilities',value=p['damage_vulnerabilities'],inline =True )
                    except:
                      print('n/a')
                    #20
                    try:
                      embed1.add_field(name='Damage Resistances',value=p['damage_resistances'],inline =True )
                    except:
                      print('n/a')
                    #21
                    try:
                      embed1.add_field(name='Damage Immunities',value=p['damage_immunities'],inline =True )
                    except:
                      print('n/a')
                    #22
                    try:
                      embed1.add_field(name='Condition Immunities',value=p['condition_immunities'],inline =True )
                    except:
                      print('n/a')
                    #23
                    try:
                      embed1.add_field(name='Senses',value=p['senses'],inline =True )
                    except:
                      print('n/a')
                    #24
                    try:
                      embed1.add_field(name='Challenge Rating',value=p['challenge_rating'],inline =True )
                    except:
                      print('n/a')

                    #1
                    try:
                      for w in p['special_abilities']:
                        embed2.add_field(name='--------------------\nName:',value=w['name'],inline =False )
                        embed2.add_field(name='Description:',value=w['desc'],inline =True )
                        embed2.add_field(name='Attack Bonus:',value=w['attack_bonus'],inline =True )
                    except:
                      print('n/a')
                    #1
                    try:
                      for j in p['actions']:
                        try:
                          embed3.add_field(name='--------------------\nName:',value=j['name'],inline =False )
                        except:
                          print('n/a')
                        try:
                          embed3.add_field(name='Description:',value=w['desc'],inline =True )
                        except:
                          print('n/a')
                        try:
                          embed3.add_field(name='Attack Bonus:',value=j['attack_bonus'],inline =True )
                        except:
                          print('n/a')
                        try:
                          embed3.add_field(name='Damage Dice:',value=j['damage_dice'],inline =True )
                        except:
                          print('n/a')
                        try:
                          embed3.add_field(name='Damage Bonus:',value=w['damage_bonus'],inline =True )
                        except:
                          print('n/a')
                        
                    except:
                      print('n/a')
                    
                    try:
                      for m in p['legendary_actions']:
                        embed4.add_field(name='--------------------\nName',value=m['name'],inline =False)
                        embed4.add_field(name='Description',value=m['desc'],inline =True)
                        embed4.add_field(name='Attack Bonus',value=m['attack_bonus'],inline =True)
                    except:
                      print('error legendary')
                    
                    json_file.close()
                    break
                  else:
                    print('next')
      
      
      await ctx.send(embed=embed1)
      await ctx.send(embed=embed2)
      await ctx.send(embed=embed3)
      await ctx.send(embed=embed4)
      await ctx.send(embed=matches)
    except Exception as e:
      print(e)

@bot.command(aliases=["racess",'r'])
async def race(ctx,*,args):
  id = str(ctx.message.author.id)
  user = bot.get_user(int(id))
  await ctx.send(user.mention + ' Looking for Race')
  if args == 'list':
    embed=discord.Embed(title='Race List',url = 'https://open5e.com/races',description= 'Click the url to get full face list')
    embed.set_footer(text = "Find Out More On Open5E")
    embed.set_image(url="https://open5e.com/favicon.ico")
    await ctx.send(embed=embed)

  else:
    print('command get')
    x= difflib.get_close_matches(args,raceData,10,0.4)
    print(x)
    matches=discord.Embed(title='Others Race Matches',url = 'https://open5e.com/races',description="The first match will be sent below, if it's not what your looking for try one of the others")
    matches.set_footer(text = "Find Out More On Open5E")
    for d in x:
          matches.add_field(name = 'Race',value = d)
    try:
      print(x[0])
      with open('races.json') as json_file:
                data = json.load(json_file)
                for p in data:
                  if p['name']==x[0]:
                    print('match found')
                    name = p['name']

                    try:
                      embed1=discord.Embed(title=name,url = 'https://open5e.com/classes',description=p['desc'] )
                      embed2=discord.Embed(title=name +' Traits',description=p['traits'])
                    except:
                      print('n/a')
                    try:
                      embed1.add_field(name='\u200b',value=p['asi-desc'],inline =False)
                    except:
                      print('n/a')
                    try:
                      embed1.add_field(name='\u200b',value=p['age'],inline=False)
                    except:
                      print('n/a')
                    try:
                      embed1.add_field(name='\u200b',value=p['alignment'],inline=False)
                    except:
                      print('n/a')
                    try:
                      embed1.add_field(name='\u200b',value=p['size'],inline=False)
                    except:
                      print('n/a')
                    try:     
                      embed1.add_field(name='\u200b',value=p['speed-desc'],inline=False)
                    except Exception as e:
                      print(e)
                      print('n/a')
                    try:
                      embed1.add_field(name='\u200b',value=p['languages'],inline=False)
                    except Exception as e:
                      print(e)
                      print('n/a')
                    try:
                      embed1.add_field(name='\u200b',value=p['vision'],inline=False)
                    except Exception as e:
                      print(e)
                      print('n/a')
                    await ctx.send(embed=embed1)
                    await ctx.send(embed=embed2)
                    try:
                      s = p['subtypes']
                      for r in s:
                        embed3=discord.Embed(title='Subtype: '+r['name'],description=r['traits'])
                        try:
                          embed3.add_field(name='Description',value=r['desc'],inline=False)
                        except Exception as e:
                          print(e)
                          print('n/a')
                        try:
                          embed3.add_field(name='\u200b',value=r['asi-desc'],inline=False)
                        except Exception as e:
                          print(e)
                          print('n/a')
                        await ctx.send(embed=embed3)
                    except Exception as e:
                      print(e)
                      print('n/a')
                    json_file.close()
                    await ctx.send(embed=matches)
                    break
                  else:
                    print('next')
                  
    except Exception as e:
      print(e)

@bot.command()
async def roll(ctx,*,args):
  try:
      math = ""
      id = str(ctx.message.author.id)
      print(11)
      value = characters[id][str(args)]["modifier"]
      print(12)
      print(value)
      print(13)
      roll = random.randint(1,20)
      print(14)
      math = str(roll)+' + '+str(value)
      print(15)
      roll = roll+value
      print(16)
      print(characters[id][args]["proficent"])
      if characters[id][args]["proficent"] == True:
        print(5)
        roll+=characters[id]["proficiency"]
        print(6)
        math=math+' + '+str(characters[id]["proficiency"])
      print(7)

      embed=discord.Embed(title=args+' roll',url = 'https://open5e.com/classes')
      print(8)
      embed.set_footer(text='Math for your roll '+math)
      print(9)
      embed.add_field(name='Your Role',value=roll)
      print(10)
      await ctx.send(embed=embed)
  except:
    numbers = re.split(r'[+]',args)
    print(numbers)
    total = 0;
    roll = ''
    for d in numbers:
      if 'd' in d:
        broken = re.split(r'[d]',d)
        print('broken is '+str(broken))
        for i in range(0,int(broken[0])):
          value =(random.randint(1,int(broken[1])))
          total = total+value
          if roll == '':
            roll = str(value)
          else:
            roll = roll+'+'+str(value)
      elif 'D' in d:
        broken = re.split(r'[D]',d)
        print('broken is '+str(broken))
        for i in range(0,int(broken[0])):
          value =(random.randint(1,int(broken[1])))
          total = total+value
          if roll == '':
            roll = str(value)
          else:
            roll = roll+'+'+str(value)
      else:
        total = total+int(d)
        roll = roll+'+'+str(d)
    await ctx.send(total)   

    embed=discord.Embed(title='Roll',description='Rolling: '+args)
    embed.add_field(name="Your Roll",value=str(total))
    embed.set_footer(text="Math for your role: "+roll)
    await ctx.send(embed=embed)

@bot.command()
async def create(ctx,*,args):
  
  guild = ctx.guild
  args = args.lower()
  print(args+' lowered')
  if discord.utils.get(ctx.guild.roles, name=args+' player'):
        await ctx.send('A game with this name already exists')
  else:
    role = await guild.create_role(name=args+' player')
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True),
        role: discord.PermissionOverwrite(read_messages=True)
      }
    if role is not None:
        print(role.name)
        member = ctx.message.author
        if member is not None:
            await member.add_roles(role)
    category = guild.get_channel(757773199101657109)
    channel = await guild.create_text_channel(args, overwrites=overwrites,category=category)
    await channel.send('Welcome to your private channel, to add user type >invite (username) to invite them! Please note that usernames are case sensitive Also note that all server rules still apply and server admins can still view these channels. ')
    await ctx.message.delete()

@bot.command()
async def invite(ctx,*,args):
  guild = ctx.guild
  channel = str(ctx.channel)
  print(channel)
  channel = channel.replace('-',' ')+' player'
  print(channel)
  role = discord.utils.get(guild.roles,name=channel)
  user = discord.utils.get(guild.members,name=args)
  if role is not None:
        print(role.name)
        if user is not None:
            await user.add_roles(role)
            await ctx.send('Welcome, '+user.mention)

@bot.command()
async def leave(ctx,*,args):
  guild = ctx.guild
  channel = str(ctx.channel)
  print(channel)
  channel = channel.replace('-',' ')+' player'
  print(channel)
  role = discord.utils.get(guild.roles,name=channel)
  user = discord.utils.get(guild.members,name=args)
  if role is not None:
        print(role.name)
        if user is not None:
            await user.remove_roles(role)
            await ctx.send('Goodbye, '+user.mention)

@bot.command()
async def createcharacter(ctx):
  id = str(ctx.message.author.id)
  user = bot.get_user(int(id))
  characters[id]["help"]=True
  if id not in characters:
        data = characters["user id"]
        print(data)
        characters[id] = characters['user id']
        await ctx.send("Check your DM's")
        await user.send("You are now registered\nType >ok to continue")
        _save()
  else:
    await ctx.send("Check your DM's")
    await user.send("You already have a character, if you wish to reset it type >yes to continue")

@bot.command()
async def yes(ctx):
  id = str(ctx.message.author.id)
  user = bot.get_user(int(id))
  await user.send('THIS WILL CLEAR YOUR DATA IF YOU ARE SURE TYPE >ok to continue')

@bot.command()
async def ok(ctx):
    id = str(ctx.message.author.id)
    user = bot.get_user(int(id))
    data = characters["user id"]
    characters[id]["help"]=True
    print(data)
    characters[id] = characters['user id']
    await user.send("Your character has been cleared, please enter your strength with >set strength (value)")
    _save()

@bot.command()
async def set(ctx,category,value:int):
  id = str(ctx.message.author.id)
  user = bot.get_user(int(id))
  try:
    modifier=value-10
    modifier=int(modifier/2)
    if category == "strength":
      characters[id]["strength"]["value"]=int(value)
      characters[id]["strength"]["modifier"]=int(modifier)
      characters[id]["athletics"]["modifier"]=int(value)
      await user.send('Value added succesfuly')
      await user.send(str(characters[id][category]["value"]))
      if characters[id]["help"]:
        await user.send('Enter >set dexterity (value) to continue')
    elif category == "dexterity":
      characters[id]["dexterity"]["value"]=int(value)
      characters[id]["dexterity"]["modifier"]=int(modifier)
      characters[id]["acrobatics"]["modifier"]=int(modifier)
      characters[id]["stealth"]["modifier"]=int(modifier)
      characters[id]["sleight of hand"]["modifier"]=int(modifier)
      await user.send('Value added succesfuly')
      await user.send(str(characters[id][category]["value"]))
      if characters[id]["help"]:
        await user.send('Enter >set constitution (value) to continue')
    elif category == "constitution":
      characters[id]["constitution"]["value"]=int(value)
      characters[id]["constitution"]["modifier"]=int(modifier)
      await user.send('Value added succesfuly')
      await user.send(str(characters[id][category]["value"]))
      if characters[id]["help"]:
        await ctx.send('Enter >set intelligence (value) to continue')
    elif category == "intelligence":
      characters[id]["intelligence"]["value"]=int(value)
      characters[id]["intelligence"]["modifier"]=int(modifier)
      characters[id]["arcana"]["modifier"]=int(modifier)
      characters[id]["history"]["modifier"]=int(modifier)
      characters[id]["investigation"]["modifier"]=int(value)
      characters[id]["nature"]["modifier"]=int(modifier)
      characters[id]["religion"]["modifier"]=int(modifier)
      await user.send('Value added succesfuly')
      await user.send(str(characters[id][category]["value"]))
      if characters[id]["help"]:
        await user.send('Enter >set wisdom (value) to continue')
    elif category == "wisdom":
      characters[id]["wisdom"]["value"]=int(value)
      print(1)
      characters[id]["wisdom"]["modifier"]=int(modifier)
      print(2)
      characters[id]["animal handling"]["modifier"]=int(modifier)
      print(3)
      characters[id]["medicine"]["modifier"]=int(modifier)
      print(4)
      characters[id]["perception"]["modifier"]=int(modifier)
      print(5)
      characters[id]["survival"]["modifier"]=int(modifier)
      print(6)
      characters[id]["insight"]["modifier"]=int(modifier)
      await user.send('Value added succesfuly')
      await user.send(str(characters[id][category]["value"]))
      if characters[id]["help"]:
        await user.send('Enter >set charisma (value) to continue')
    elif category=="charisma":
      characters[id]["charisma"]["value"]=int(value)
      print(1)
      characters[id]["charisma"]["modifier"]=int(modifier)
      print(2)
      characters[id]["deception"]["modifier"]=int(modifier)
      print(3)
      characters[id]["intimidation"]["modifier"]=int(modifier)
      print(4)
      characters[id]["performance"]["modifier"]=int(modifier)
      print(5)
      characters[id]["persuasion"]["modifier"]=int(modifier)
      print(6)
      characters[id]["sleight of hand"]["modifier"]=int(modifier)
      print(7)
      await user.send('Value added succesfuly')
      await user.send(str(characters[id][category]["value"]))
      if characters[id]["help"]:
        await user.send('Enter >set proficiency (value) to continue')
    elif category=='proficiency':
      characters[id]['proficiency']=value
      await user.send('Proficiency Set')
      if characters[id]["help"]:
        await user.send('Finally use >proficient (skill) to add your proficiency bonus to that skill')


    else:
      await user.send('no category')
    _save()
  except: 
    await user.send("invalid category or value :(")

@bot.command()
async def proficient(ctx,category):
  id = str(ctx.message.author.id)
  user = bot.get_user(int(id))
  try:
    if characters[id][category]['proficent']==True:
      characters[id][category]['proficent']=False
      await user.send('Set '+category+' to not proficent')
      if characters[id]["help"]:
        await user.send('Use this command again to add another proficiency or >done to continue')
    else:
      characters[id][category]['proficent']=True
      await user.send('Set '+category+' to proficent')
      if characters[id]["help"]:
        await user.send('Use this command again to add another proficiency or >done to continue')
    _save()
  except:
    await user.send('Invalid Category')

@bot.command()
async def done(ctx):

  id = str(ctx.message.author.id)
  user = bot.get_user(int(id))
  characters[id]['help']=False
  await ctx.send(user.mention)
  embed=discord.Embed(title='Character')
  embed.add_field(name='Strength',value=str(characters[id]["strength"]["value"])+'\n**Strength Mod**\n'+str(characters[id]["strength"]["modifier"]))
  embed.add_field(name='Dexterity',value=str(characters[id]["dexterity"]["value"])+'\n**Dexterity Mod**\n'+str(characters[id]["dexterity"]["modifier"]))
  embed.add_field(name='Constitution',value=str(characters[id]["constitution"]["value"])+'\n**Constitution Mod**\n'+str(characters[id]["constitution"]["modifier"]))
  embed.add_field(name='Intelligence',value=str(characters[id]["intelligence"]["value"])+'\n**Intelligence Mod**\n'+str(characters[id]["intelligence"]["modifier"]))
  embed.add_field(name='Wisdom',value=str(characters[id]["wisdom"]["value"])+'\n**Wisdom Mod**\n'+str(characters[id]["wisdom"]["modifier"]))
  
  embed.add_field(name='Charisma',value=str(characters[id]["charisma"]["value"])+'\n**Charisma Mod**\n'+str(characters[id]["charisma"]["modifier"]))
  proficiencies = ''
  for d in characters[id]:
    try:
      if characters[id][d]['proficent'] == True:
        proficiencies = proficiencies +d+', '
    except:
        print('n/a')
  print(proficiencies)
  embed.add_field(name='Proficiencies',value=proficiencies)
  await ctx.send(embed=embed)

@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier
    activity = discord.Game(name="Inside the Tomb Of Horrors", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    global armorData
    global classData
    with open('armor.json') as json_file:
        data = json.load(json_file)
        for p in data:
            armorData.append(p['name'])
    json_file.close()
    with open('classes.json') as json_file:
        data = json.load(json_file)
        for p in data:
            classData.append(p['name']) 
    json_file.close()
    with open('spells.json') as json_file:
        data = json.load(json_file)
        for p in data:
            spellData.append(p['name'])
    json_file.close()
    with open('weapons.json') as json_file:
        data = json.load(json_file)
        for p in data:
            weaponData.append(p['name']) 
    json_file.close()
    with open('monsters.json') as json_file:
        data = json.load(json_file)
        for p in data:
            monsterData.append(p['name'])
    json_file.close()
    with open('races.json') as json_file:
        data = json.load(json_file)
        for p in data:
            raceData.append(p['name'])
    json_file.close()
    with open('conditions.json') as json_file:
        data = json.load(json_file)
        for p in data:
            conditionData.append(p['name'])
    json_file.close()
    with open('characters.json') as json_file:
      global characters
      characters = json.load(json_file)
    json_file.close()
    
@bot.command(pass_context=True)
@commands.has_any_role("Bot Wrangler","Admin")
async def setup(ctx):
  
  embed=discord.Embed(title='Role List',description='React with the emoji matching the role you want to recieve')
  embed.add_field(name='DM workshop access: 🏰 ',value='------------------')
  message = await ctx.send(embed=embed)
  global message_num
  message_id = message.id
  message_num = message_id
  await message.add_reaction('🏰')
  await ctx.message.delete()

@bot.command(pass_context=True)
@commands.has_any_role("Bot Wrangler","Admin")
async def id(ctx,args):
  global message_num
  message_num = int(args)
  await ctx.message.delete()

@bot.command(pass_context=True)
@commands.has_any_role("Bot Wrangler","Admin")
async def category(ctx,*,args):
  await ctx.guild.create_category(args)
  await ctx.message.delete()

@bot.command(pass_context=True)
@commands.has_any_role("Bot Wrangler","Admin")
async def delete(ctx):

  guild = ctx.guild
  category = guild.get_channel(757671111021297797)
  messagecat = ctx.channel.category
  print('message cat is'+str(messagecat))
  if str(messagecat) == "D&D Games" :
    channels = str(ctx.channel)
    print(channels)
    channels = channels.replace('-',' ')+' player'
    print(channels)
    role = discord.utils.get(guild.roles,name=channels)
    try:
      await role.delete()
    except:
      print('kept role')
    await ctx.channel.delete()
  else:
    await ctx.send("Wait you don't want to delete this channel!")

@bot.command(pass_context=True)
@commands.has_any_role("Bot Wrangler","Admin")
async def deleteRole(ctx,*,args):
  guild = ctx.guild
  role = discord.utils.get(guild.roles,name=args)
  await role.delete()
  await ctx.message.delete()


@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == message_num:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)
        print(payload.emoji.name)
        if payload.emoji.name == '🏰':
            print('thumbs up role')
            role = discord.utils.get(guild.roles,name = 'DM workshop access')
    print('Reaction Added')

    if role is not None:
        print(role.name)
        member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
        if member is not None:
            await member.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == message_num:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)
        print(payload.emoji.name)
        if payload.emoji.name == '🏰':
            print('thumbs up role')
            role = discord.utils.get(guild.roles,name = 'DM workshop access')
    print('Reaction Added')

    if role is not None:
        print(role.name)
        member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
        if member is not None:
            await member.remove_roles(role)


def _save():
    with open('characters.json', 'w+') as f:
        json.dump(characters, f)
    f.close()

extensions = [
 'cogs.cog_example'  # Same name as it would be if you were importing it
]

if __name__ == '__main__':  # Ensures this is the file being ran
    for extension in extensions:
        bot.load_extension(extension)  # Loades every extension.

keep_alive()  # Starts a webserver to be pinged.
token = os.environ.get("DISCORD_BOT_SECRET")

bot.run(token)  # Starts the bot