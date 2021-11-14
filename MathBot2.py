## BOT FOR PRACTICAL COMMANDS
import os
import io
import random
import math
import time
import datetime
import asyncio
from fractions import Fraction
from csv import writer
import codecs
import discord
from discord.ext import commands
from discord.ext.commands import Cog
import chess
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN2')

daily_days = 0
daily_hour = 0
daily_minute = 0
daily_second = 0
total_rolls = ''
amount = 0
fun_fact = ''
lmao = None
pi = math.pi
sqrt = math.sqrt
asin = math.asin
sin = math.sin
acos = math.acos
cos = math.cos
atan = math.atan
tan = math.tan
log = math.log10
fsum = math.fsum
radians = math.radians
degrees = math.degrees
fact = math.factorial
fabs = math.fabs
ft_users = {}

bot = commands.Bot(command_prefix='*')

@bot.event
async def on_ready():
    print('MathBot 2.0 Has Connected!')

@bot.command(name='math', help='Example: *math "2 + 2" 2 = 4.00; *math "2 * 3" 1 = 6.0')
async def math(ctx, equation, x=None):
    
    global lmao
    try:
        if x == None:
            x = 5
        
        elif x != None:
            x = int(x)
        
        equation = equation.strip(" ")
        equation = f"{equation}"
        solve = eval(equation)

        solvedString = f"{solve}"

        if solvedString[0] == '6' and solvedString[1] == '9':
            thingy = ['lmao', 'nice']
            lmao = random.choice(thingy)

        if x == 0:
            solve += 0.0000000000003
            solve = f'{solve:.{x}f}'
            if solvedString[0] == '6' and solvedString[1] == '9':
                thingy = ['lmao', 'nice']
                lmao = random.choice(thingy)
            
            if lmao == 'lmao' or lmao == 'nice':
                embed=discord.Embed(title = f'{equation} =', description=f"{solve} {lmao}", color=0xFF5733)
                await ctx.send(embed=embed)
                lmao = None
            else:
                embed=discord.Embed(title = f'{equation} =', description=solve, color=0xFF5733)
                await ctx.send(embed=embed)
                lmao = None

        elif lmao == 'lmao' or lmao == 'nice':
            embed=discord.Embed(title = f'{equation} =', description=f"{solve:.{x}f} {lmao}", color=0xFF5733)
            await ctx.send(embed=embed)
            lmao = None
        else:
            embed=discord.Embed(title = f'{equation} =', description=f"{solve:.{x}f}", color=0xFF5733)
            await ctx.send(embed=embed)
            lmao = None

    except ZeroDivisionError:
        embed=discord.Embed(title= f'{equation} =', description='Error: Can\'t divide by zero!', color=0xFF5733)
        await ctx.send(embed=embed)
    
    except:
        embed=discord.Embed(title= f'{equation} =', description='Invalid Syntax!', color=0xFF5733)
        await ctx.send(embed=embed)

@bot.command(name="conch", help="Ask the Magic conch anything")
async def conch(ctx, question):

    responses = ["I don't see why not.",
                 "Definitely.",
                 "I believe so...",
                 "Why don't you ask later?",
                 "I don't feel comfortable answering that...",
                 "No.",
                 "Definitely not.",
                 "Ask again Later.",
                 "Nope.",
                 "What kind of question is that?",
                 "I think you already know the answer to that.",
                 "I want to answer, but I don't think you'll like my response.",
                 "Take a guess.",
                 "I guess.",
                 "Probably.",
                 "I'm not sure.",
                 "Ask me again tomorrow.",
                 "That's a dumb question.",
                 "What kind of question is that?"]

    response = random.choice(responses)

    embed=discord.Embed(title= 'Magic Conch', description= response, color=0xFF5733)
    await ctx.send(embed=embed)

@bot.command(name='symbols', help='Teaches you how to use each symbol for you math equations!')
async def symbols(ctx):

    response = '+ is for addition\n- is used for subtraction\n* is used for multiplication\n/ is used for division\n** is used as a carrot\npi = Base pi (3.14159....)\nsqrt() = Finds the square root of an expression.\nsin() = Finds the sine of the expression.\ncos() = Finds the cosine of the expression.\ntan() = Finds the tangent of the expression.\nasin() = Finds the arc of the sine input\nacos() = Finds the arc of the cosine input\natan() = Finds the arc of the tangent input\nlog() = Calculates an expression using base 10 Log.\nfsum([x,y]) = Finds the sum of any amount of numbers, separated by commas.\nradians() = Converts an expression to radians.\ndegrees() = Converts an expression to degrees.\nfact() = takes the factorial of a number or expression.\nfabs() = Finds the absolute value of an expression.'
    embed=discord.Embed(title= 'Math Symbols', description= response, color=0xFF5733)
    await ctx.send(embed=embed)

class NewHelpName(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page)
            await destination.send(embed=emby)

bot.help_command = NewHelpName()

@bot.command(name='idea', help='Gives me suggestions for what to add to my bot!')
async def idea(ctx, response, error=None):
    username = ctx.author.name
    if len(response) > 250:
        await ctx.send('Please Keep your response up to 250 characters!')
    else:
        with open('bot.csv', 'a') as f_object: 
            all_data = []
            writer_object = writer(f_object) 
            all_data.append(username)
            all_data.append(response)

            if error != None:
                await ctx.send(f'Looks like your message didn\'t have quotes! Your message should look something like this! i.e.(-idea "example text")')
            elif error == None:
                await ctx.send(f'Your message has been recieved, {username}!')
                writer_object.writerow(all_data)
            f_object.close()

@bot.command(name='balance', help='Checks your current balance.')
async def balance(ctx):
    with open('casino_currency.csv', 'r+') as file:
        username = ctx.author.name
        # Saves the file into a list
        stronk = ''
        names = []
        grab_currency = {}
        for i in file:
            new_list = i.strip()
            if new_list != '':
                names.append(new_list)
        # Makes a list so that you can access your balance in the future
        for i in names:
            naim = i.split(',')
            grab_currency[naim[0]] = naim [1]

        # Adds you to the file if you are not currently on it and gives a base balance of 1000 Credits
        if username not in grab_currency:
            name_list = []
            stronk += str(username)
            stronk += ','
            stronk += '1000'
            names.append(stronk)
            name_list.append(stronk)
            await ctx.send(f'You did not have an account with us so we opened up an account for you, {username}!\nPlease type //balance again to view your balance!\nTo learn more about how you earn credits, type //creditshelp!')
            # Rewrites the file so that the user can be added to the list
            dos = writer(file)
            strur = []
            strur.append(stronk)

            for i in strur:
                new_i = i.strip()
                new_i = new_i.split(',')
                dos.writerow(new_i)
        else:
            embed=discord.Embed(title = f'{ctx.author.name.capitalize()}\'s Balance', description=f'Balance: {int(grab_currency[username]):,} mChips!', color=0xF4513B)
            await ctx.send(embed=embed)

    return int(grab_currency[username])

@bot.command(name='timerhelp', help="A command to show help on the timer.")
async def timerhelp(ctx):

    i = 0

    await ctx.send("The timer module goes in the order, Hours, Minutes, and Seconds Here are a few examples of this code being used.")

    time.sleep(5)

    while i != 2:
        hours = random.randint(0, 24)
        minutes = random.randint(0, 60)
        seconds = random.randint(0, 60)

        await ctx.send(f"*timer {hours} {minutes} {seconds}, will set a {hours} hour, {minutes} minute, {seconds} second timer.")
        time.sleep(2)
        i += 1

@bot.command(name="timeleft",help="Checks how much time is left on your timer.")
async def timer(ctx):
    global ft_users
    name = ctx.author.name

    for i in ft_users:
        if name in ft_users:
            items = ft_users[name]
            time = items[0]
            current_time = datetime.datetime.now()
            times = time - current_time
            splitt = str(times)
            urdad = splitt.split(",")
            
            try:
                if urdad[1] != None:
                    urmom = urdad[1].split(":")
            except:
                urmom = splitt.split(":")
            
            try:
                if urdad[1] != None:
                    days = urdad[0]
                    hours = int(urmom[0])
                    minutes = int(urmom[1])
                    seconds = float(urmom[2])

            except:
                days = 0
                hours = int(urmom[0])
                minutes = int(urmom[1])
                seconds = float(urmom[2])
            if days == 0:
                if hours == 0:
                    if minutes == 0:
                        embed=discord.Embed(title=f"{items[2]}", description=f"You have *{seconds:.0f}* seconds left, {name}", color=0xFF5733)
                        await ctx.send(embed=embed)
                    else:
                        embed=discord.Embed(title=f"{items[2]}", description=f"You have *{minutes}* minutes, and *{seconds:.0f}* seconds left, {name}", color=0xFF5733)
                        await ctx.send(embed=embed)
                else:
                    embed=discord.Embed(title=f"{items[2]}", description=f"You have *{hours}* hours, *{minutes}* minutes, and *{seconds:.0f}* seconds left, {name}", color=0xFF5733)
                    await ctx.send(embed=embed)
            else:
                embed=discord.Embed(title=f"{items[2]}", description=f"You have *{days}*, *{hours}* hours, *{minutes}* minutes, and *{seconds:.0f}* seconds left, {name}", color=0xFF5733)
                await ctx.send(embed=embed)

@bot.command(name='timer', help='Will set a timer for you. *timerhelp for more info.')
async def timer(ctx,hourss=None,minutess=None,secondss=None, message=None):
    
    global ft_users

    if hourss != None:

        test = hourss.isdecimal() 

        if test:
            
            #hourss = int(hourss)

            if minutess == None:
                minutess = 0
            if secondss == None:
                secondss = 0

            current_time = datetime.datetime.now()
            
            future_result = datetime.datetime(current_time.year, current_time.month, current_time.day, current_time.hour, current_time.minute, current_time.second)

            ft = future_result + datetime.timedelta(hours=int(hourss), minutes=int(minutess), seconds=int(secondss))
            
            final = ((float(hourss) * 60 * 60) + (float(minutess) * 60) + (float(secondss)))
            final_time = final
            embed=discord.Embed(title="Timer Set", description=f"Timer started for {ctx.author.name} for {hourss} hours, {minutess} minutes, and {secondss} seconds.", color=0xFF5733)
            await ctx.send(embed=embed)
            if ctx.author.name in ft_users:
                if message != None:
                    ft_users[ctx.author.name] = [ft, ctx, message]
                else:
                    ft_users[ctx.author.name] = [ft, ctx]
            elif ctx.author.name not in ft_users:
                if message != None:
                    ft_users[ctx.author.name] = [ft, ctx, message]
                else:
                    ft_users[ctx.author.name] = [ft, ctx]
        else:
            print("Else Statement Compiled")
            if hourss == 'stop':
                ft_users[ctx.author.name] = [datetime.datetime.now(), ctx]
            elif hourss == "pause":
                await ctx.send("This is currently in the works.")
            else:
                print("Statement Failed")

@bot.command(name="funfact", help="Tells you a fun fact")
async def fact(ctx):

    fun_fact = [
        "Horrifying and Terrifying mean the same thing, but Terrific and Horrific mean completely different things.",
        "There is no telling whether or not life is a simulation, and whether or not that simulation is within a simulation. Life is mysterious",
        "Every 2 minutes, you could die, breathing just resets that timer.",
        "Somewhere, roughly every 12 seconds, someone dies.",
        "For every 60 seconds in africa, a minute passes.",
        "You can't move the top of your mouth",
        "You breathe and blink automatically until you hear, read, or even just think about it, then you do it all manually",
        "Theoretically, there's an alternate universe where you were the most successful person in the world. On that note, you could have also been the worst person to be known in all of mankind.",
        "We've known blackholes have existed for a while now, it's only til recently that we've been able to prove it.",
        "Scratching a scratch is just scratching that scratch so that scratch no longer feels scratchy",
        "Asking your friend a question you already know the answer to is the same thing as opening the fridge every 5 minutes expecting more food.",
        "Christmas is more of a deadline than a holiday.",
        "You park in the driveway and drive in a parkway.",
        "The fear of your own shadow is called *Sciaphobia*",
        "The word, *Tetraphobia*, means to practice avoiding any instance of the number 4.",
        "The lost city of Atlantis is a perplex mythological story, but theoretically, there are places where Atlantis could have been existential at some point, we just haven't had access to searching it yet.",
        "You don't technically 'have' money. You're just borrowing it. Then when you spend it, it moves on to someone else to borrow.",
        "People go to school to get an education, just to make minimum wage, yet, high school dropouts can still find a job and be millionaires before they hit their 30's",
        "If you think about it, your fingernails are just small, very dull razer blades.",
        "There's a school called Chute Middle School, which means they have a tab called *chute middle school staff*.",
        "There's a village in Austria named, Fucking, which was recently renamed to Fugging as of November 2020, due to the pronunciation of the village.",
        "A normal colony of ants can contain as little as 3,000 adult ants, but other colonies have shown to have over 100,000 ants in a single colony.",
        "None of the greek gods are interpreted as real *Gods* perse, but are known figures of the possibilities of actual Gods that run over their own *kingdom* of sorts.",
        "The phrase, 'Where are you?' was most likely not heard much until phones were invented.",
        "1 in every 100 people are considered a psychopath.",
        "Latin is one of the few languages that was very commonly used in society, and nowadays, nobody uses this language. In fact, roughly only 100 people in the world can speak the language fluently.",
        "Queen Elizibeth II is 94 years old as of Feb 1, 2021, and is indeed, invincible.",
        "If we buy expensive things to show how wealthy we are, are we really just showing how poor we are because we just spent all of our money?",
        "You can turn sand into glass, but you can never turn glass back into sand.",
        "A lethal amount for you average dog for the consumption of chocolate is roughly .5 oz of milk chocolate per lb of your dog's weight. Dark and/or semi-sweet chocolate is roughly .13 oz of chocolate per lb of your dog's weight.",
        "An Oak tree can produce at an average of 10,000 acorns in a year.",
        "Lysol was originally invented to help with the cholera pandemic in the late 19th century.",
        "It took 4 times longer to copper swords to steel than it took to go from steel to nuclear bombs",
        'Moths will vibrate their genitals as a way to prevent a bat from locating them.',
        'There’s an island near Mexico City filled with creepy old dolls',
        'Koala pee contains chlamydia',
        'When you\'re sick, the advice you get is to literally do drugs and stay out of school.',
        f'Psychopathy is defined as a mental (antisocial) disorder in which an individual manifests amoral and antisocial behavior, shows a lack of ability to love or establish meaningful personal relationships, expresses extreme egocentricity, and demonstrates a failure to learn from experience and other behaviors associated with the condition.\nCongratulations... {ctx.author.name}.',
        'Apollo 11 only had around 15-20 seconds of fuel left when it finally landed.',
        'Your mom gay lmao'
    ]

    yeet = random.choice(fun_fact)
    embed=discord.Embed(title="Fun Fact", description=yeet, color=0xFF5733)
    await ctx.send(embed=embed)

@bot.command(name='roll', help='*roll "# of sides" "# of dice"')
async def diceroll(ctx, sides, quantity=1):
    global total_rolls
    amount_of_dice = range(0, int(quantity))

    for i in amount_of_dice:
        random_roll = random.randint(1, int(sides))
        total_rolls += f"{random_roll}"
        total_rolls += "  "
    
    embed=discord.Embed(title="Dice:", description=total_rolls, color=0xFF5733)
    await ctx.send(embed=embed)
    total_rolls = ''

@bot.command(name="random", help='Gives you a random number between 0 and your number.')
async def random_thing(ctx, num=None, types=None, loop=None):
    num = int(num)
    if types == 'music':
        if num == 1:
            songs = [
                'youtu.be/YQRHrco73g4','youtu.be/HFuR8WJTkGM','youtu.be/j57OP141Gzs','youtu.be/yHLtE1wFeRQ',
                'youtu.be/4S0shEqJ8Vc','youtu.be/Hn4sfC2PbhI','youtu.be/uryVw968ZMM','youtu.be/A309fz7y65o',
                'youtu.be/s7dTBoW5H9k','youtu.be/EErSKhC0CZs','youtu.be/18JQUYgpOlw','youtu.be/2LOmFBBq4T0',
                'youtu.be/3Z1h2VE0hzs','youtu.be/xPfMb50dsOk','youtu.be/8pm_KoguqPM','youtu.be/XYKUeZQbMF0',
                'youtu.be/jrgO_9ey53M','youtu.be/zvq9r6R6QAY','youtu.be/Nla5XQGjgOI','youtu.be/dhYOPzcsbGM',
                'youtu.be/pTA0DSfrGZ0','youtu.be/9c2rW2Jd2DM','youtu.be/s7hMIHpQGGo','youtu.be/Oj18EikZMuU',
                'youtu.be/UgDD0C8QWL8','youtu.be/UgDD0C8QWL8','youtu.be/iY1eHL4KqA0','youtu.be/OflUhXR3cfE',
                'youtu.be/OflUhXR3cfE','youtu.be/3MnyyOY5ZTY','youtu.be/9Qmv8HUf37c','youtu.be/rlaG7gF7qeI',
                'youtu.be/ygI-2F8ApUM','youtu.be/ygI-2F8ApUM','youtu.be/GlUeW7IOSFc','youtu.be/oL5fbozc3kU',
                'youtu.be/oL5fbozc3kU','youtu.be/8GW6sLrK40k','youtu.be/TKfS5zVfGBc','youtu.be/hsXeFqj5p7Q',
                'youtu.be/2ziqtyseR3M','youtu.be/V0e7rFdVYxE'
                ]
            if loop != None:
                loop = int(loop)
                stringies = ''
                for i in range(0, loop):
                    answer = '!play '
                    answer += random.choice(songs)
                    stringies += answer
                    stringies += '\n'
                await ctx.send(stringies)
            else:
                answer = '!play '
                answer += random.choice(songs)
                await ctx.send(answer)

        elif num == 2:
            songs = [
                '!play your mom lmao'
                ]
            if loop != None:
                loop = int(loop)
                stringies = ''
                for i in range(0, loop):
                    answer = random.choice(songs)
                    stringies += answer
                    stringies += '\n'
                await ctx.send(stringies)

        elif num == 3:
            songs = [
                '!play your mom lmao'
                ]
            if loop != None:
                loop = int(loop)
                stringies = ''
                for i in range(0, loop):
                    answer = random.choice(songs)
                    stringies += answer
                    stringies += '\n'
                await ctx.send(stringies)

        else:
            await ctx.send('Please choose a playlist from the *music command. I.e.: *random 2 music 3 will give you 3 random songs from the second playlist.') 
    else:
        specific = random.randint(0, num)
        await ctx.send(f"The number is {specific}")

@bot.command(name="music", help="Gives a list of links of playlists to listen to.")
async def music(ctx):
    embed=discord.Embed(title="Music:", description='!play youtube.com/playlist?list=PLWOIV6PtMXoSYt2_hJ9XVUWFX_fb_Jv5z  ---  Discord Music To Vibe To\n!play youtube.com/playlist?list=PLWOIV6PtMXoT7jxzrxdWv0xQPPL-PlMD7  ---  Music To Set A Mood\n!play youtube.com/playlist?list=PLWOIV6PtMXoTL0pEEMKSKr-w9NbzGKo3K  ---  My Old Favorite Songs (Not Updated)', color=0xFF5733)
    await ctx.send(embed=embed)

# @bot.command(name="game?", help="/gameshelp for help")
# async def game(ctx, name=None, pingy=None, show_all=None):
#     username = ctx.author.name
#     if name != None:
#         with open('users_games.txt', 'rt') as file:
#             lists = []
#             # converts every line in the file to a list
#             for i in file:
#                 crap = i.split(',')
#                 lists.append(crap[0])
#                 # checks if they inputed a username
#                 if name != None:
#                     if crap[0] != '\n':
#                         ping = crap[1]
#                         # checks if the username is in the list
#                         if name in i:
#                             users_stuff = ''
#                             # puts every game a user has in their list into a string
#                             for x in range(2, len(crap)):
#                                 users_stuff += '\n'
#                                 users_stuff += crap[x]
#                             # checks if the user wants to ping the person
#                             if pingy != None:
#                                 # checks if the user wants to see everything, ping, games, etc.
#                                 if show_all != None:
#                                     await ctx.send(f'{name} has these games:\n{users_stuff}\n{ping}\n{username} wants to play a game with you in Vibin!')

#                                     try:
#                                         loud = ctx.author.name.upper()
#                                         vibin = bot.get_channel(757649192851210462)
#                                         member = ctx.author
#                                         await member.move_to(vibin)

#                                     except:
#                                         await ctx.send(f"{ctx.author.mention} Please Join Vibin'")
#                                 else:
#                                     await ctx.send(f'{ping}\n{username} wants to play a game with you in Vibin!')

#                                     try:
#                                         loud = ctx.author.name.upper()
#                                         vibin = bot.get_channel(757649192851210462)
#                                         member = ctx.author
#                                         await member.move_to(vibin)

#                                     except:
#                                         await ctx.send(f"{ctx.author.mention} Please Join Vibin'")
#                             else:
#                                 await ctx.send(f'{name} has these games:\n{users_stuff}')
            
#             # corrects a user for inputting an invalid name in the files.
#             if name not in lists:
#                 await ctx.send(f'Sorry, That user doesn\'t exist in our file.\nPlease refer to //gameshelp game? to view all valid users in our file.')

#     # pings everyone if nothing is specified,
#     else:
#         try:
#             loud = ctx.author.name.upper()
#             vibin = bot.get_channel(757649192851210462)
#             member = ctx.author
#             await member.move_to(vibin)
#             await ctx.send(f"{loud} is looking to game, <@&755135335905624155>, They'll be waiting in Vibin'")

#         except:
#             await ctx.send(f"{ctx.author.mention} Please Join Vibin'")
#             await ctx.send(f"{loud} is looking to game, <@&755135335905624155>, They'll be waiting in Vibin'")

# @bot.command(name="games", help="/gameshelp for help!")
# async def games(ctx, total_games=None, error=None):
#     final_information_list = []
#     if error != None:
#         await ctx.send("Please Use Correct Syntax.\n//games 'Example_Text'")
#     else:
#         username = ctx.author.name
#         with open('users_games.txt', 'r+') as file:
#             nameses = []
#             for i in file:
#                 check = i.strip()
#                 check = i.split(',')
#                 nameses.append(check[0])
#             all_data = []
#             writer_object = writer(file)

#             if username not in nameses:
#                 if total_games != None:
#                     new_list = total_games.split(" ")
#                     total = []
#                     for i in new_list:
#                         all_data.append(i)
#                     all_data.insert(0, username)
#                     all_data.insert(1, ctx.author.mention)
#                     await ctx.send("Response Recieved!")
#                 if all_data != []:
#                     writer_object.writerow(all_data)
            
#             else:
#                 num = 0
#                 generic = []
#                 new_items = []
#                 with open('users_games.txt', "r") as games_input:
#                     for i in games_input:
#                         generic.append(i)
#                     for i in range(len(generic)):
#                         try:
#                             generic.pop(i + 1)
#                         except:
#                             pass
                    
#                     for i in range(len(generic)):
#                         items = generic[i]
#                         item = items[:-1]
#                         new_items.append(item)

#                     # REMAKES THE ENTIER FILE INTO A LIST
#                     for i in new_items:

#                         if username in i:

#                             if total_games != None:
#                                 grand_total_games = total_games.split(" ")
                            
#                                 for x in range(len(grand_total_games)):

#                                     if grand_total_games[x] not in i:
#                                         i += ','
#                                         i += grand_total_games[x]

#                                     else:
#                                         await ctx.send(f"{grand_total_games[x]} is already in your list!")

#                                 new_items.pop(num)
#                                 new_items.append(i)
#                                 break
#                         num += 1
                    
#                     for i in new_items:
#                         final_information_list.append(i)
#         os.remove('users_games.txt')    
#         # CLEARS FILE AND WRITES NEW INFORMATION
        
#         with open('users_games.txt', 'w+') as jubber:
#             thingy = writer(jubber)
#             for i in final_information_list:
#                 new_list = i.split(',')
#                 thingy.writerow(new_list)
#             await ctx.send(f"Your games have been updated!")

# @bot.command(name="gameshelp", help="Shows how to use the games command.")
# async def gh(ctx, type=None):
#     with open('users_games.txt', 'rt') as file:
#         i = ''
#         next(file)
#         for x in file:
#             new_x = x.strip()
#             new_x = x.split(',')
#             i += new_x[0]
#         if type == None:
#             await ctx.send(f'To learn about all the game commands please use the syntax //gameshelp "type"\n TYPES:\ngame?\ngames')
#         else:
#             if type == 'game?':
#                 await ctx.send(f'the "//game?" command can be used 4 ways. if you just type //game? it will ping everyone that has the gamer tag.\n\nYou can use this function to see what games people have. People on this list include:\n{i}\n//game? "username" will check what games that specific user has.\n\n If you typed in //game? "username" ping, it will ping that user to play a game with you.\n\nTo see everything, just type //game? "username" ping SA (SA for See All)')

#             elif type == 'games':
#                 await ctx.send(f'//games is a command that will allow you to add games to your name so others can see what games you have.\nThis gives the chance for users to know whether or not they have the same games as you have.\nTo use the command, simply type //games "First_Game Second_Game Third_Game"\nMake sure to use proper Case Sensitivity, otherwise you may recieve duplicate games in your list!\nIf your game has a space, use underscores.\nIf you would like to add a game to your list that you don\'t already have, just use the //games "game_name" command again to add to your list.')

@bot.command(name='fizzbuzz', help='WARNING: This command is very spammy! Use with caution')
async def buzzlookanalien_whatWhere_BAH(ctx, num):
    string = ''
    num = int(num)
    if num <= 5:
        num = 5
    elif 50 <= num:
        num = 50
    for i in range(1, num + 1):
        divisible_by_3 = i % 3 == 0
        divisible_by_5 = i % 5 == 0
        if divisible_by_3 and divisible_by_5:
            string += 'FizzBuzz!\n'
        elif divisible_by_5:
            string += 'Buzz!\n'
        elif divisible_by_3:
            string += 'Fizz!\n'
        else:
            string += str(i) + '\n'

    embed=discord.Embed(title="Chess Board Help:", description=string, color=0xFF5733)
    await ctx.send(embed=embed)

@bot.command(name='chesshelp', help='Shows you everything you need to know about the chess command')
async def chess_help(ctx, type=None):
    if type == None:
        embed=discord.Embed(title="Chess Board Help:", description='It seems that you haven\'t specified what you want help with. Please type "*chesshelp options" to display a list of help commands', color=0xFF5733)
        await ctx.send(embed=embed)
    
    elif type.lower() == 'options':
        response = '''```Some commands are as follows:\n"*chesshelp board" Will display the moves you can make and how to make that move.\n"*chesshelp pieces" Will tell you how each piece can move\n"*chesshelp start" Will teach you how to officially start a game of chess with another user.\n"*chesshelp user_info" Will show you all the valid users that can play a game of chess with you!```'''
        embed=discord.Embed(title="Options:", description=response, color=0xFF5733)
        await ctx.send(embed=embed)
    
    elif type.lower() == 'board':
        board_help = 'a8 b8 c8 d8 e8 f8 g8 h8\na7 b7 c7 d7 e7 f7 g7 h7\na6 b6 c6 d6 e6 f6 g6 h6\na5 b5 c5 d5 e5 f5 g5 h5\na4 b4 c4 d4 e4 f4 g4 h4\na3 b3 c3 d3 e3 f3 g3 h3\na2 b2 c2 d2 e2 f2 g2 h2\na1 b1 c1 d1 e1 f1 g1 h1'
        how_to_make_moves = 'To make a valid move, first choose your piece that you would like to move.\nIf you would like to move a pawn for example, let\'s say your pawn is on space g2\nIf you want to move it up one space, the syntax would simply be "*chess move g2g3"'
        embed=discord.Embed(title="Chess Board Help:", description=f"""```{board_help}```\n```{how_to_make_moves}```""", color=0xFF5733)
        await ctx.send(embed=embed)

    elif type.lower() == 'pieces':
        knight = 'This is a white knight: ♞ | This is a black knight: ♘ | Knights are a bit tricky, however they are very nice once you understand their movement.\nKnights can move left, right, up, or down 2 spaces, and then from that second space, moving in the other direction 1 space.\nThink of it this way. You are on a block and you choose to move up two spaces. From there you must go right or left one space, that space is where you knight will go.'
        rook = 'This is a white rook: ♜ | This is a black rook: ♖ | Rooks are pieces you don\'t want to mess with.\n This piece can move any distance going horizontally and vertically, this is really useful when you want to limit the opponents movement distance.'
        bishop = 'This is a white bishop: ♝ | This is a black bishop: ♗ | Bishops can move any distance going diagonally.\nThe only set back for this is that they are always on a specific place, so if you lose a bishop, that could set you back for captures on another bishop. Spare them wisely'
        queen = 'This is a white queen: ♛ | This is a black queen: ♕ | Queens are the superior piece. It\'s like the bishop and rook had a baby.\nThe queen can move and distance diagonally, horizontally and vertically. It\'s just one of those pieces that whoops butt.'
        king = 'This is a white king: ♚ | This is a black king: ♔ | Kings are your main pieces that you want to guard. They can move one space in ANY direction.\nBe aware though, you can\'t move your king into a capturing position, or else that would place you in check, so you must move that piece in a valid space if you want to move it.'
        pawn = 'This is a white pawn: ♟ | This is a black pawn: ♙ | Pawns have one mode of direction, and that\'s straight.\nOn your pawns FIRST move, you can have them either move one or two spaces. In order to capture a piece with a pawn, it must be one space diagonally from that pawn.\nIn this instance, your pawn will have moved diagonally one piece, but only on a captured piece.'
        embed=discord.Embed(title="Chess Pieces", description=f"Pawns: {pawn}\n\nBishops: {bishop}\n\nKnights: {knight}\n\nRooks: {rook}\n\nKing: {king}\n\nQueen: {queen}", color=0xFF5733)
        await ctx.send(embed=embed)

    elif type.lower() == 'start':
        embed=discord.Embed(title="How to Play:", description='''```In order to start a game with someone, you and that user must have an account with us.\nTo create an account, simply type "//balance" and you will gain an account with Math Bot!\nIf you would like to start the game with that user, simply type "*chess start 'their user ID'".\nTo find out a user's ID, simply type "*chesshelp user_info".\nYou will only be able to play one game at a time, so if you would like to end a game, you can simply type "*chess end"```''', color=0xFF5733)
        await ctx.send(embed=embed)
    
    elif type.lower() == 'user_info':
        user_data = '\n'
        with open('casino_currency.csv') as file:
            await ctx.send('Some users in our file consist of:')
            for i in file:
                new_i = i.strip()
                new_i = new_i.split(',')
                if new_i != ['']:
                    user_data += '-'
                    user_data += new_i[0] + '\n'
            embed=discord.Embed(title="User Info:", description=f"""```{user_data}```""", color=0xFF5733)
            await ctx.send(embed=embed)

    else:
        embed=discord.Embed(title="Oops!", description='Oops! That\'s not a valid response! Please type "*chesshelp options" to display a list of help commands', color=0xFF5733)
        await ctx.send(embed=embed)

@bot.command(name='chess', help='Play a nice game of chess.')
async def chess_bot(ctx, command=None, other_user=None):
    if command == None:
        await ctx.send('Whoops! Looks like you didn\'t specify anything! Please type "*chesshelp options" for some help on the chess command!')
    else:
        user_valid = False
        opponent_valid = False
        user_in_match = False
        opponent_in_match = False
        game_can_start = False

        check_user_in_system

        if command.lower() == 'start':
            if ctx.author.name == other_user:
                await ctx.send('You can\'t play a game with yourself!')
                return False

            user_valid, opponent_valid = check_user_in_system(ctx, other_user, user_valid, opponent_valid)
            
            if opponent_valid:
                user_in_match, opponent_in_match = check_user_in_match(ctx, other_user, user_in_match, opponent_in_match)

            if user_valid:
                if user_in_match:
                    await ctx.send('You\'re currently playing a game right now!')
                elif opponent_valid:
                    game_can_start = True
                else:
                    if opponent_in_match:
                        await ctx.send('The opponent is currently in a match!')
                    else:
                        await ctx.send('The opponent could not be found! Have them look over "*chesshelp options!"')
            else:
                if user_in_match:
                    await ctx.send('You\'re currently playing a game right now!')
                else:
                    await ctx.send('You weren''t found on our records! Please type "//balance" or look through "*chesshelp options" to receive help!')
            
            if game_can_start:
                board = chess.Board()
                board.legal_moves
                board_value = []
                board_value.append(board)
                board_string = str(board_value)
                new_board = board_string.split("[Board('")
                new_board = new_board[1].strip("')]")
                start_new_chess_match(ctx, other_user, new_board)
                new_board = format_board(board)
                # await ctx.send(f"""```{new_board}```""")
                embed=discord.Embed(description=f'''```{new_board}```''', color=0xFF5733)
                await ctx.send(embed=embed)
                

        elif command.lower() == 'move':
            validity = check_whos_turn_chess(ctx)
            if validity:
                if len(other_user) >= 4:
                    new_board = chess_move(ctx, other_user)
                    if new_board == 'You must make a valid move!':
                        random_insult = [
                        "I can't believe you would move there sir, you should know that move isn't valid. You absolute freaking idiot. How about you actually give me a real move to work with.",
                        "That move isn't valid. Try again!",
                        "Man, didn't you know that move is illegal? Try again...",
                        "Ok, well I see that you tried moving to a spot. I admire that you tried, but you just can't simply make that move. It's an illegal move. Check the board again and try again. I got all the time in the world to make sure you make this move correct.",
                        "Whoops! Looks like that move is invalid! Check the board and try again.",
                        "Sir, that move is invalid, you dum-dum.",
                        "Well, I see you tried moving to that spot, but that simply won't work. Try again!",
                        "Bruh, that move ain't possible. Try again mate.",
                        "k that is an impossible move. You idiot.",
                        "Guess what? That move ain't valid. Try again.",
                        "That move was so wrong on so many levels that you broke the elevator to heaven. Try again, and don't be wrong!",
                        "Okay, so you tried moving but that move was invalid, so either get it right next time or I will go in your room and eat your carpet.",
                        "Sorry, that move is invalid!",
                        "Guess what? That move you just gave me? Yeah, it's invalid. Give me a better one or else i'll be unhappy with you.",
                        "Hey siri, how to make a valid move.\nSiri: Have you tried turning it on and off again?\nOk, you sir, make a move, but try that.",
                        "You sir are a psychopath. What on earth were you thinking when you gave me that move. It's invalid. Null. Incomplete. Impossible. Idiotic. Fix your mistakes.",
                        "Well, you tried, but clearly not hard enough. Try typing your move CORRECTLY next time please.",
                        "The heck is that. I don't even know what i'm looking at. That move just doesn't work.",
                        "How do you look at a piece and think, huh, I think I want to take my pawn and treat it like a queen. It just doesn't work. You bafoon.",
                        "Do you know the definition of a simpleton? Yeah. You're a simpleton. Try typing your move correctly this time.",
                        "That move is impossible. Next time when you make a move, actually use your brain.",
                        "Oh yeah, sure, you may think you can get away with that, but that's why i'm here to stop you from making that horribly obvious illegal move. I'm watching you.\nMAKE A VALID MOVE FOR PETES SAKE!",
                        "I'm just at a loss of words right now. I have no idea how you concocted this series of movements and what benefit it would give you, but this move you've given me just doesn't work.",
                        "Are you tired? Are you needing some caffeine in your system so that your brain actually functions properly? Look at the move you just did and see what's wrong with it.",
                        "Okay, either you seriously don't see what's wrong or you're just messing with me. Look VERY closely at the move you just did and see what's wrong there.",
                        "Have you ever had those moments where you're like, 'Where's my phone?' and it's in your hand? Yeah, except the concept here is that the move you just made is seriously wrong and you just don't know why. Check again mate.",
                        "What are you doing? Do you just think i'll let you get away with that move? You are so dumb if think that is the case. Try again, and make it RIGHT!",
                        "I don't know if you just don't know how the moves work. I'll be nice and give you the nice benefit of using '*chesshelp board' to actually see what spaces are equal to what and how to make those moves CORRECTLY.",
                        "I have given you ample opportunities to make right for what you've done wrong, but clearly you haven't learned your lesson. I'm going to continue pestering you for every wrong move you get, but just know, these will only get worse and worse the more impatient I grow."
                        ]
                        
                        response = random.choice(random_insult)
                        await ctx.send(response)
                        
                    else:
                        start_new_chess_match(ctx, other_user, new_board, True)
                        game_finished, statement = check_game_finish(new_board)
                        print_board = chess.Board(new_board)
                        player_number_one, player_number_two, current_player = chess_change_turns(ctx)
                        if game_finished:
                            if statement == "You're in checkmate":
                                if current_player == 'P1':
                                    await ctx.send(f'{statement}, {player_number_one}.\n{player_number_two} wins!')
                                else:
                                    await ctx.send(f'{statement}, {player_number_two}\n{player_number_one} wins!')
                                new_board = format_board(print_board)
                                embed=discord.Embed(description=f'''```{new_board}```''', color=0xFF5733)
                                await ctx.send(embed=embed)
                                chess_abandon(ctx)

                            elif statement == "You're in stalemate":
                                if current_player == 'P1':
                                    current_player = player_number_one
                                else:
                                    current_player = player_number_two

                                await ctx.send(f'{statement}, {current_player}')
                                new_board = format_board(print_board)
                                embed=discord.Embed(description=f'''```{new_board}```''', color=0xFF5733)
                                await ctx.send(embed=embed)
                                chess_abandon(ctx)
                            else:
                                if current_player == 'P1':
                                    current_player = player_number_one
                                else:
                                    current_player = player_number_two
                                await ctx.send(f'{statement}, {current_player}')
                                new_board = format_board(print_board)
                                embed=discord.Embed(description=f'''```{new_board}```''', color=0xFF5733)
                                await ctx.send(embed=embed)

                        else:
                            new_board = format_board(print_board)
                            embed=discord.Embed(description=f'''```{new_board}```''', color=0xFF5733)
                            await ctx.send(embed=embed)
                else:
                    await ctx.send('Your move must be 4 characters minimum! Ex: e2e4')
            else:
                await ctx.send('You are either not in a game, or it is not your turn! "*chesshelp options" for help!')
                
        elif command.lower() == 'current':
            board, thing = show_chess_board(ctx)
            new_board = format_board(board)
            embed=discord.Embed(description=f'''```{new_board}```''', color=0xFF5733)
            await ctx.send(embed=embed)

        elif command.lower() == 'end':
            check_ingame = chess_abandon(ctx)
            if check_ingame:
                await ctx.send('You have successfully abandoned your match!')
            else:
                await ctx.send('You can\'t end a game if you\'re not in one!')

        elif command.lower() == 'turn':
            is_it_your_turn = check_whos_turn_chess(ctx)
            if is_it_your_turn:
                placeholder_value = 'It is'
            else:
                placeholder_value = 'It is not'

            await ctx.send(f'{placeholder_value} currently your turn!')

def chess_abandon(ctx):
    temp_value = False
    placeholder_list = []
    with open('chess_match.csv', 'rt') as file:
        for i in file:
            new_i = i.strip()
            placeholder_list.append(new_i)

        for i in placeholder_list:
            index_value = placeholder_list.index(i)
            new_i = i.split(',')
            if new_i != ['']:
                if new_i[0] == ctx.author.name:
                    placeholder_list.pop(index_value)
                    temp_value = True
                    try:
                        placeholder_list.pop(index_value + 1)
                        break
                    except:
                        break

                elif new_i[1] == ctx.author.name:
                    placeholder_list.pop(index_value)
                    temp_value = True
                    try:
                        placeholder_list.pop(index_value + 1)
                        break
                    except:
                        break

    os.remove('chess_match.csv')
    
    with open('chess_match.csv', 'w+') as file:
        writer_obj = writer(file)
        for i in placeholder_list:
            temp_list = []
            new_i = i.split(',')
            if new_i != ['']:
                for i in new_i:
                    temp_list.append(i)
                writer_obj.writerow(temp_list)

    return temp_value

def check_whos_turn_chess(ctx):
    placeholder_list = []
    placeholder_value = False
    with open('chess_match.csv', 'rt') as file:
        for i in file:
            new_i = i.strip()
            placeholder_list.append(new_i)

        for i in placeholder_list:
            index_value = placeholder_list.index(i)
            new_i = i.split(',')
            if new_i != ['']:

                if new_i[0] == ctx.author.name and new_i[3] == 'P1':
                    placeholder_value = True

                elif new_i[1] == ctx.author.name and new_i[3] == 'P2':
                    placeholder_value = True

        return placeholder_value

def chess_change_turns(ctx):
    placeholder_list = []
    with open('chess_match.csv', 'rt') as file:
        for i in file:
            new_i = i.strip()
            placeholder_list.append(new_i)

        for i in placeholder_list:
            index_value = placeholder_list.index(i)
            new_i = i.split(',')
            if new_i != ['']:

                if new_i[0] == ctx.author.name:
                    if new_i[3] == 'P1':
                        new_i[3] = 'P2'
                    else:
                        new_i[3] = 'P1'
                    player_number_one = new_i[0]
                    player_number_two = new_i[1]
                    current_player = new_i[3]
                    placeholder_list.append(f'{ctx.author.name},{new_i[1]},{new_i[2]},{new_i[3]}')
                    placeholder_list.pop(index_value)
                    break

                elif new_i[1] == ctx.author.name:
                    if new_i[3] == 'P1':
                        new_i[3] = 'P2'
                    else:
                        new_i[3] = 'P1'
                    player_number_one = new_i[0]
                    player_number_two = new_i[1]
                    current_player = new_i[3]
                    index_value = placeholder_list.index(i)
                    placeholder_list.append(f'{new_i[0]},{ctx.author.name},{new_i[2]},{new_i[3]}')
                    placeholder_list.pop(index_value)
                    break

    os.remove('chess_match.csv')
    
    with open('chess_match.csv', 'w+') as file:
        writer_obj = writer(file)
        for i in placeholder_list:
            temp_list = []
            new_i = i.split(',')
            if new_i != ['']:
                for i in new_i:
                    temp_list.append(i)
                writer_obj.writerow(temp_list)

    return player_number_one, player_number_two, current_player

def check_game_finish(current_board):
    board = chess.Board(current_board)
    if board.is_checkmate():
        statement = 'You\'re in checkmate'
        return True, statement
            
    elif board.is_check():
        statement = 'You\'re in check'
        return True, statement

    elif board.is_stalemate():
        statement = 'You\'re in stalemate'
        return True, statement
    
    else:
        return False, 'E'

def chess_move(ctx, move):
    thing, current = show_chess_board(ctx)
    board = chess.Board(current)
    try:
        current_board = board.push_san(move)
        ip_thing = board.fen()
        return ip_thing
    except ValueError:
        return 'You must make a valid move!'

def start_new_chess_match(ctx, other_user, board, update=False):
    placeholder_list = []
    with open('chess_match.csv', 'rt') as file:
        for i in file:
            new_i = i.strip()
            placeholder_list.append(new_i)
        if not update:
            placeholder_list.append(f"{ctx.author.name},{other_user},{board},P1")

    if update:
        for i in placeholder_list:
            index_value = placeholder_list.index(i)
            new_i = i.split(',')
            if new_i != ['']:
                if new_i[0] == ctx.author.name:
                    placeholder_list.append(f'{ctx.author.name},{new_i[1]},{board},{new_i[3]}')
                    placeholder_list.pop(index_value)
                    break

                elif new_i[1] == ctx.author.name:
                    index_value = placeholder_list.index(i)
                    placeholder_list.append(f'{new_i[0]},{ctx.author.name},{board},{new_i[3]}')
                    placeholder_list.pop(index_value)
                    break

    os.remove('chess_match.csv')
    
    with open('chess_match.csv', 'w+') as file:
        writer_obj = writer(file)
        for i in placeholder_list:
            temp_list = []
            new_i = i.split(',')
            if new_i != ['']:
                for i in new_i:
                    temp_list.append(i)
                writer_obj.writerow(temp_list)

def show_chess_board(ctx):
    with open('chess_match.csv', 'rt') as file:
        for i in file:
            new_i = i.strip()
            new_i = new_i.split(',')
            if new_i != ['']:
                if new_i[0] == ctx.author.name or new_i[1] == ctx.author.name:
                    board = new_i[2]
                    final_board = chess.Board(board)
        return final_board, board

def check_user_in_match(ctx, other_user, user_in_match, opponent_in_match):
    with open('chess_match.csv', 'rt') as file:
        for i in file:
            new_i = i.split(',')
            if new_i != ['\n']:

                if new_i[0] == ctx.author.name:
                    user_valid = False
                    user_in_match = True
                
                elif new_i[1] == ctx.author.name:
                    user_valid = False
                    user_in_match = True

                elif new_i[0] == other_user:
                    opponent_in_match = True
                    opponent_valid = False

                elif new_i[1] == other_user:
                    opponent_in_match = True
                    opponent_valid = False

        return user_in_match, opponent_in_match

def check_user_in_system(ctx, other_user, user_valid, opponent_valid):
    with open('casino_currency.csv', 'rt') as file:
        for i in file:
            new_i = i.split(',')
            if new_i[0] == ctx.author.name:
                user_valid = True

            elif new_i[0] == other_user:
                opponent_valid = True
            
            elif opponent_valid and user_valid:
                break

        return user_valid, opponent_valid

def format_board(board):
    num = 0
    placeholder_board = ''
    placeholder_list = []
    for i in str(board):
        placeholder_list.append(i)
        if i == 'N':
            i = '♞'
        elif i == 'n':
            i = '♘'
        elif i == 'R':
            i = '♜'
        elif i == 'r':
            i = '♖'
        elif i == 'B':
            i = '♝'
        elif i == 'b':
            i = '♗'
        elif i == 'Q':
            i = '♛'
        elif i == 'q':
            i = '♕'
        elif i == 'K':
            i = '♚'
        elif i == 'k':
            i = '♔'
        elif i == 'P':
            i = '♟'
        elif i == 'p':
            i = '♙'
        elif num == 0 and i != '\n' and i != ' ':
            i = '▱'

        elif num == 1 and i != '\n' and i != ' ':
            i = '▱'

        if i != ' ':
            if num == 0:
                num = 1

            elif num == 1:
                num = 0

        placeholder_board += i
    return placeholder_board

async def check_user():
    global ft_users
    await bot.wait_until_ready()
    while not bot.is_closed():
        try:
            if ft_users != None:
                for i in ft_users:
                    if ft_users[i] != None:
                        data = ft_users[i]
                        entry = data[0]
                        point = data[1]
                        try:
                            timer_name = data[2]
                            if datetime.datetime.now() >= entry:
                                ft_users.pop(i)
                                if timer_name != None:
                                    embed=discord.Embed(title=timer_name, description=f"{point.author.mention}, your time has ended!", color=0xFF5733)
                                    await point.send(embed=embed)
                        except:
                            if datetime.datetime.now() >= entry:
                                ft_users.pop(i)
                                embed=discord.Embed(title="Timer", description=f"{point.author.mention}, your time has ended!", color=0xFF5733)
                                await point.send(embed=embed)  
            await asyncio.sleep(1)
        except Exception:
            print("Exception Failure")
            await asyncio.sleep(1)

bot.loop.create_task(check_user())
bot.run(TOKEN)