import os
import random
from datetime import datetime
from csv import writer
from typing import Sized
import discord
from discord.ext import commands
from discord.ext.commands.core import check
from discord.ext.commands.errors import MissingRole
from discord.utils import get
from dotenv import load_dotenv
from pymongo import MongoClient
from discord_slash import SlashCommand, SlashContext
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import numpy as np

load_dotenv()
TOKEN = os.getenv('MATHBOT_TOKEN')
cluster = MongoClient('MONGO_TOKEN')

amount = 0

bot = commands.Bot(command_prefix='//')
slash = SlashCommand(bot, sync_commands=True) 

@slash.slash(name='help', description='', guild_ids=[755112397454180443])
async def help(ctx:SlashContext, option=None):
    options = ['credits', 'rps', 'roulette', 'cointoss', 'slots', 'oasis', 'levels', 'shop', 'color', 'info','font']
    if option in options:
        if option == 'credits':
            embed=discord.Embed(title = 'Credits', description='To gain credits using mathbot, you much gamble! Other ways you may gain credits \
                                         is by using /daily, /weekly, and /monthly. These commands give a random amount of credits to you, and multiplies \
                                         based on your level.', color=0xF4513B)
            await ctx.send(embed=embed)
        elif option == 'rps':
            await ctx.send('E')
        elif option == 'roulette':
            red_numbers = str("""```diff\n-1 3 5 7 9 12 14 16 18 21 23 25 27 28 30 32 34 36```""")
            green_numbers = str("""```css\n0 00```""")
            black_numbers = str("""```2 4 6 8 10 11 13 15 17 19 20 22 24 26 29 31 33 35```""")
            roulette_command = "```/roulette bid: '# of credits' color: (R G B N) number: 'Number Relating to Color'```"
            embed=discord.Embed(title = 'Roulette Help', description=f'To properly use the /roulette command, you must know the board and the format of \
                the command to place your bet.\n\nThe command should go something like this, {roulette_command}\nEach color letter corresponds to a certain \
                color. G = Green, R = Red, B = Black, and N = No Color\nNo color is usually used when you are bidding on a number rather than a color,\
                however it does not matter what you put, just so long that you place in a valid color.\nYou DO NOT need to place something in the number \
                slot. The only slots that require input is the Credits, and Color.\nIf you place a bet in the number, it will place your outcome very high \
                but chances of you winning are very low, so keep that in mind.\n\nIf you need access to the roulette board, you can always type, \
                /help roulette,\nHere\'s the board for reference.\n{red_numbers} {green_numbers} {black_numbers}', color=0xF4513B)
            await ctx.send(embed=embed)
        elif option == 'cointoss':
            await ctx.send('E')
        elif option == 'slots':
            await ctx.send('E')
        elif option == 'oasis':
            await ctx.send('E')
        elif option == 'levels':
            embed=discord.Embed(title = 'Levels', description='To view what level you have and how much it will cost to levelup, type ```/levelup```\n If you would just like to view you level, type ```/level```\nTo levelup, type ```/levelup confirm: confirm```', color=0xF4513B)
            await ctx.send(embed=embed)
        elif option == 'shop':
            await ctx.send('E')
        elif option == 'color':
            colors =['white',     'light_grey',    'dark_grey', 'black',
                     'red',       'blue',          'scarlet',   'blue_green',
                     'orange',    'purple',        'tangerine', 'golden_brown',
                     'yellow',    'pink',          'teal',      'hazelnut',
                     'green',     'brown',         'turquoise', 'lime',
                     'sunflower', 'sea_green',     'sky_blue',  'periwinkle', 
                     'amber',     'grass_green',   'indigo',    'azure_blue', 
                     'caramel',   'carrot_orange', 'warm_white']

            allColors = ''
            colors.sort()
            for i in colors:
                allColors += i + ' '
            embed=discord.Embed(title = 'Colors', description=f'The color command is quite easy! This is used to choose what color you would like your information to be viewed as in the "/info" command!\nSimply type ```/color color: "name of color"``` and your text will show up in the chosen color.\nHere are all the color names in correct format ```{allColors}```', color=0xF4513B)
            await ctx.send(embed=embed)
        elif option == 'info':
            await ctx.send('E')
        elif option == 'font':
            allFonts = ''
            fonts = ['arial', 'comic', 'bahnschrift', 'consola', 'impact' , 'segoesc']
            for i in fonts:
                allFonts += i + ' '
            embed=discord.Embed(title = 'Colors', description=f'The font command is very neat. This allows you to change the font of which you see in the /info command! To change your font, you want to type ```/font "font_name"``` These font names include: ```{allFonts}```', color=0xF4513B)
            await ctx.send(embed=embed)
    else:
        allOptions = ''
        for i in options: allOptions += i + ' \n'
        embed=discord.Embed(title = 'Options:', description=allOptions, color=0xF4513B)
        await ctx.send(embed=embed)

@slash.slash(name='setup', description='Sets you up in our system!', guild_ids=[755112397454180443])
async def balance(ctx: SlashContext):

    await ctx.defer()
    username = ctx.author.name
    userFound = False

    # Searches the MathBot Database and grabs all users
    userDB = cluster['MathBot']
    userCollection = userDB['users']
    users = userCollection.find()

    for user in users:
        if user['_id'] == username:
            userFound = True

    if not userFound:
        '''
            _id = username of the player
            balance = The user's balance
            daily, weekly, monthly = Datetime objects determining time based money claims
            nicknames = A list of nicknames the user has
            level = The user's current level
            backgrounds = A list of backgrounds the user has purchased. 1st index is the one they want to view
            text_color = The color the user wants the text to show up as in /info
        '''
        post = {'_id': username, 'balance': 1000, 'daily': 0, 'weekly': 0, 'monthly': 0, 'nicknames': [], 'level': 1, 'background': 'red_basic.png', 'text_color': (0, 0, 0), 'font': 'arial.ttf'}
        userCollection.insert_one(post)
        await ctx.send("You have been successfully added to the system!")
    else:
        await ctx.send("You are already registered in our system!")

@slash.slash(name='rps', description="//rps 'credits' 'rock,paper, or scissors'", guild_ids=[755112397454180443])
async def rps(ctx:SlashContext, credits, rps_input):
    username = ctx.author.name
    if credits.isdecimal:
        credits = int(credits)
        if int(credits) > 0:
            truth = check_bal(username, credits)
            
            if truth:
                
                if rps_input.lower() == 'scissors' or rps_input.lower() == 'rock' or rps_input.lower() == 'paper':
                    result = ['rock', 'paper', 'scissors']
                    
                    if rps_input.lower() == 'rock':
                        final_result = random.choice(result)
                        
                        if final_result == rps_input.lower():
                            await ctx.send(f'{username}: {rps_input.capitalize()}!\nMath Bot: {final_result}!\nYou Tied!\n\nYour new balance is {display_current_balance(username)}.')
                        
                        elif final_result == 'scissors':
                            balance = credit_dedux(username, credits)
                            balance = roulette_x_win(username, credits, 2)
                            await ctx.send(f'{username}: {rps_input.capitalize()}!\nMath Bot: {final_result}!\nYou Win!\n\nYour new balance is {balance}.')
                        
                        else:
                            balance = credit_dedux(username, credits)
                            await ctx.send(f'{username}: {rps_input.capitalize()}!\nMath Bot: {final_result}!\nYou Lost!\n\nYour new balance is {balance}.')
                    
                    elif rps_input.lower() == 'paper':
                        final_result = random.choice(result)
                        
                        if final_result == rps_input.lower():
                            await ctx.send(f'{username}: {rps_input.capitalize()}!\nMath Bot: {final_result}!\nYou Tied!\n\nYour new balance is {display_current_balance(username)}.')
                        
                        elif final_result == 'rock':
                            balance = credit_dedux(username, credits)
                            balance = roulette_x_win(username, credits, 2)
                            await ctx.send(f'{username}: {rps_input.capitalize()}!\nMath Bot: {final_result}!\nYou Win!\n\nYour new balance is {balance}.')
                        
                        else:
                            balance = credit_dedux(username, credits)
                            await ctx.send(f'{username}: {rps_input.capitalize()}!\nMath Bot: {final_result}!\nYou Lost!\n\nYour new balance is {balance}.')
                    else:
                        final_result = random.choice(result)
                        
                        if final_result == rps_input.lower():
                            await ctx.send(f'{username}: {rps_input.capitalize()}!\nMath Bot: {final_result}!\nYou Tied!\n\nYour new balance is {display_current_balance(username)}.')
                        
                        elif final_result == 'paper':
                            balance = credit_dedux(username, credits)
                            balance = roulette_x_win(username, credits, 2)
                            await ctx.send(f'{username}: {rps_input.capitalize()}!\nMath Bot: {final_result}!\nYou Win!\n\nYour new balance is {balance}.')
                        
                        else:
                            balance = credit_dedux(username, credits)
                            await ctx.send(f'{username}: {rps_input.capitalize()}!\nMath Bot: {final_result}!\nYou Lost!\n\nYour new balance is {balance}.')
                else:
                    await ctx.send('Please leave a valid response! i.e. "Rock", "Paper", "Scissors".')
            else:
                await ctx.send(f'You have insufficient funds! Please check your balance by using /balance!')
        else:
            await ctx.send('Please type a positive amount of credits!')
    else:
        await ctx.send('Please type a valid input for your credits! Ex. "//rps \'12\' \'rock\'"\nThis will place a 12 mChip bet on rock!')

@slash.slash(name='roulette', description='"/help roulette" to learn how to use this command properly.', guild_ids=[755112397454180443])
async def gamble(ctx:SlashContext, bid=None, color=None, number=None):
    username = ctx.author.name
    chosen_color = ''
    try:
        if bid != None:
            if bid.isdecimal():
                positive = check_bal(username, bid)
                if positive:
                    bid = int(bid)
                    if color == 'R' or color == 'G' or color == 'B' or color == 'N':
                        roulette_numbers = ['00', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]
                        red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 21, 23, 25, 27, 28, 30, 32, 34, 36]
                        black_numbers = [2, 4, 6, 8, 10, 11, 13, 15, 17, 19, 20, 22, 24, 26, 29, 31, 33, 35]
                        chosen_number = random.choice(roulette_numbers)
                        if number != None:
                            if number == number:
                                balance = credit_dedux(username, credits)
                                chosen_number = random.choice(roulette_numbers)

                                if chosen_number == int(number):
                                    response = f'The ball landed on {chosen_number}, Congratulations!'
                                    balance = roulette_x_win(username, bid, 36)
                                    total_balance = final_balance(balance)
                                    await ctx.send(f'{response}\nYour New Balance is: {total_balance}')
                                elif chosen_number == str(number):
                                    response = f'The ball landed on {chosen_number}, Congratulations!'
                                    balance = roulette_x_win(username, bid, 36)
                                    total_balance = final_balance(balance)
                                    await ctx.send(f'{response}\nYour New Balance is: {total_balance}')

                                else:
                                    total_balance = final_balance(balance)
                                    response = f'The ball landed on {chosen_number}, better luck next time!'
                                    await ctx.send(f'{response}\nYour New Balance is: {total_balance}')
                            else:
                                await ctx.send('Woah there! You\'re bidding on a non-existent number! "/help roulette" to view the board!')
                        else:
                            balance = credit_dedux(username, bid)
                            if color == 'R':
                                if chosen_number in red_numbers:
                                    chosen_color = 'Red'
                                elif chosen_number in black_numbers:
                                    chosen_color = 'Black'
                                else:
                                    chosen_color = 'Green'

                                if chosen_number in red_numbers:
                                    response = f'The ball landed on {chosen_number} {chosen_color}, Congratulations!'
                                    balance = roulette_x_win(username, bid, 2)
                                    total_balance = final_balance(balance)
                                    await ctx.send(f'{response}\nYour New Balance is: {total_balance}')
                                else:
                                    total_balance = final_balance(balance)
                                    response = f'The ball landed on {chosen_number} {chosen_color}, better luck next time!'
                                    await ctx.send(f'{response}\nYour New Balance is: {total_balance}')

                            elif color == "G":
                                if chosen_number in red_numbers:
                                    chosen_color = 'Red'
                                elif chosen_number in black_numbers:
                                    chosen_color = 'Black'
                                else:
                                    chosen_color = 'Green'

                                if chosen_number == 0 or chosen_number == '00':
                                    response = f'The ball landed on {chosen_number} {chosen_color}, Congratulations!'
                                    balance = roulette_x_win(username, bid, 14)
                                    total_balance = final_balance(balance)
                                    await ctx.send(f'{response}\nYour New Balance is: {total_balance}')
                                else:
                                    total_balance = final_balance(balance)
                                    response = f'The ball landed on {chosen_number} {chosen_color}, better luck next time!'
                                    await ctx.send(f'{response}\nYour New Balance is: {total_balance}')
                            else:
                                if chosen_number in red_numbers:
                                    chosen_color = 'Red'
                                elif chosen_number in black_numbers:
                                    chosen_color = 'Black'
                                else:
                                    chosen_color = 'Green'

                                if chosen_number in black_numbers:
                                    response = f'The ball landed on {chosen_number} {chosen_color}, Congratulations!'
                                    balance = roulette_x_win(username, bid, 2)
                                    total_balance = final_balance(balance)
                                    await ctx.send(f'{response}\nYour New Balance is: {total_balance}')
                                else:
                                    total_balance = final_balance(balance)
                                    response = f'The ball landed on {chosen_number} {chosen_color}, better luck next time!'
                                    await ctx.send(f'{response}\nYour New Balance is: {total_balance}')
                    else:
                        await ctx.send('Please type a valid color! (R=Red, G=Green, B=Black N=None) //roulettehelp for more info.')
                else:
                    await ctx.send(f'Please input a valid number of credits! /balance to see how much money you have!')
            else:
                await ctx.send('Please enter a valid integer as a bid')
        else:
            await ctx.send('You have to enter a bid! //roulette "Bid" "Color". //roulettehelp for more info')
    except:
        await ctx.send('We do not see you in our system. Please type //balance to create an account with us!')

@slash.slash(name='daily', description='Your Daily Claim!', guild_ids=[755112397454180443])
async def monthly(ctx: SlashContext):

    daily = [250, 275, 300, 325]

    claim = xClaim(daily, ctx.author.name, 'daily')
    await ctx.send(claim)

@slash.slash(name='weekly', description='Your Weekly Claim!', guild_ids=[755112397454180443])
async def monthly(ctx: SlashContext):

    weekly = [2000, 2250, 2500, 2750, 3000]

    claim = xClaim(weekly, ctx.author.name, 'weekly')
    await ctx.send(claim)

@slash.slash(name='monthly', description='Your Monthly Claim!', guild_ids=[755112397454180443])
async def monthly(ctx: SlashContext):

    monthly = [8000, 8500, 9000, 9500, 10000]

    claim = xClaim(monthly, ctx.author.name, 'monthly')
    await ctx.send(claim)

def xClaim(rewards, username, time):
    '''
        Adaptively update the x claim functions

        rewards = array of random rewards for the given time
        ctx = username of the user who ran the command
        time = string of which function was ran
    '''
    nameDB = cluster['MathBot']
    userInfo = nameDB['users']
    users = userInfo.find()

    rewardChoice = random.choice(rewards)

    for user in users:
        if user["_id"] == username:
            if user[time] == 0:
                userInfo.update_one({"_id": username}, {"$set": {'balance': user['balance'] + ((1+(user['level']*.05)) * rewardChoice)}}) # Updates the Balance of the User
                userInfo.update_one({"_id": username}, {"$set": {time: datetime.now()}}) # Updates the Daily Timer
                return f"+{rewardChoice * (1+(user['level']*.05))}$ Your New Balance: ${user['balance'] + ((1+(user['level']*.05)) * rewardChoice)}" # Returns a string formatted balance to the user
            else:
                datetimeObject =  datetime.now() - user[time]
                days, hours, minutes = datetimeObject.days, datetimeObject.seconds//3600, (datetimeObject.seconds//60)%60
                if time == 'monthly':
                    days_left = 30 - days
                    verify = 'month'
                elif time == 'weekly':
                    days_left = 6 - days
                    verify = 'week'
                else:
                    days_left = 0
                    verify = 'day'
                hours_left = 23 - hours
                minutes_left = 59 - minutes
                if (days >= 1 and verify == 'day') or (days >= 7 and verify == 'week') or (days >= 31 and verify == 'month'):
                    userInfo.update_one({"_id": username}, {"$set": {'balance': user['balance'] + ((1+(user['level']*.05)) * rewardChoice)}}) # Updates the Balance of the User
                    userInfo.update_one({"_id": username}, {"$set": {time: datetime.now()}}) # Updates the x Timer
                    return f"+{rewardChoice * (1+(user['level']*.05))}$ Your New Balance: ${user['balance'] + ((1+(user['level']*.05)) * rewardChoice)}" # Returns a string formatted balance to the user
                return f"Sorry! Looks like it hasn't quite been a {verify} yet!\nCome back in {days_left} days, {hours_left} hours and {minutes_left} minutes!"
    return "Whoops! Looks like you're not showing up in our system!\nPlease use '/setup' to be registered in our system!"

def display_current_balance(username):
    userDB = cluster['MathBot']
    userCollection = userDB['users']
    users = userCollection.find()

    for user in users:
        if user['_id'] == username:
            return user['balance']

def credit_dedux(username, bid):
    '''
        Removes x amount of money from a user's account

        bid = amount of money to remove

        returns: the end balance
    '''
    userDB = cluster['MathBot']
    userCollection = userDB['users']
    users = userCollection.find()

    for user in users:
        if user["_id"] == username:
            userCollection.update_one({"_id": username}, {"$set": {'balance': user['balance'] - (bid)}})
            return user['balance'] - bid

def final_balance(end_balance):
    # Formats the balance to mChips
    # returns: the formatted string
    final_balance = f"{end_balance} mChips"
    return final_balance

def roulette_x_win(username, credits, multiplier):
    '''
        Updates a user's balance with the credits * multiplier

        username = ctx.author.name
        credits = # of credits to add to balance
        multiplier = modifier for the credits

        returns: the end balance
    '''
    userDB = cluster['MathBot']
    userCollection = userDB['users']
    users = userCollection.find()

    for user in users:
        if user["_id"] == username:
            userCollection.update_one({"_id": username}, {"$set": {'balance': user['balance'] + (credits*multiplier)}})
            return user['balance'] + credits * multiplier

def check_bal(username, bid):
    '''
        Checks if a user has enough money for a bid

        bid = amount of the desired bid

        returns: True/False
    '''
    userDB = cluster['MathBot']
    userCollection = userDB['users']
    users = userCollection.find()

    for user in users:
        if user["_id"] == username:
            if user['balance'] >= int(bid):
                return True
    return False

def check_win_slots(winner, types, bid):
    check_consec = winner.split(' ')
    check_consec.pop()

    test, amount = check_threeinarow(check_consec, types, int(bid))
    if test:
        return amount

    test, amount = check_twoinarow(check_consec, types, int(bid))
    if test:
        return amount

    return 0

def check_threeinarow(slots, types, bid):
    if slots[0] == slots[1] == slots[2]:
        if 1 in types:
            amount = 15 * bid # Changed base to 15
        if 2 in types:
            amount = 18.75 * bid
        if 3 in types:
            amount = 19.4 * bid
        if 4 in types:
            amount = 24 * bid
        if 5 in types:
            amount = 24 * bid
        if 6 in types:
            amount = 30 * bid
        if 7 in types:
            amount = 40 * bid
        if 8 in types:
            amount = 60 * bid
        if 9 in types:
            amount = 300 * bid
        return True, amount
    else:
        return False, 0

def check_twoinarow(slots, types, bid):
    amount = 0
    if ((slots[0] == slots[1]) or (slots[1] == slots[2])):
        if ((1 in types) and ((types[0] == 1 == types[1]) or (types[1] == 1 == types[2]))):
            amount = bid * 4 # Changed base to 4
        if ((2 in types) and ((types[0] == 2 == types[1]) or (types[1] == 2 == types[2]))):
            amount = bid * 5
        if ((3 in types) and ((types[0] == 3 == types[1]) or (types[1] == 3 == types[2]))):
            amount = bid * 5.2
        if ((4 in types) and ((types[0] == 4 == types[1]) or (types[1] == 4 == types[2]))):
            amount = bid * 6.4
        if ((5 in types) and ((types[0] == 5 == types[1]) or (types[1] == 5 == types[2]))):
            amount = bid * 6.4
        if ((6 in types) and ((types[0] == 6 == types[1]) or (types[1] == 6 == types[2]))):
            amount = bid * 8
        if ((7 in types) and ((types[0] == 7 == types[1]) or (types[1] == 7 == types[2]))):
            amount = bid * 10.6
        if ((8 in types) and ((types[0] == 8 == types[1]) or (types[1] == 8 == types[2]))):
            amount = bid * 16
        if ((9 in types) and ((types[0] == 9 == types[1]) or (types[1] == 9 == types[2]))):
            amount = bid * 40
        return True, amount
    else:
        return False, amount

@slash.slash(name='cointoss', description='Makes a coin toss', guild_ids=[755112397454180443])
async def toss(ctx:SlashContext, bid=None, call='nocall'):
    dice_away = False
    no_call = False
    username = ctx.author.name
    if bid == None:
        coinflip = ['Heads', 'Tails']
        coin = random.choice(coinflip)
        await ctx.send(f'The coin landed on {coin}!')
        no_call = True
    elif (str(call.lower()) == 'heads') or (call.lower() == 'tails'):
        dice_away = True
    if dice_away:
        thingy = check_bal(username, bid)
        if thingy:
            coinflip = ['heads', 'tails']
            coin = random.choice(coinflip)
            balance = credit_dedux(username, int(bid))
            if call.lower() == coin:
                balance = roulette_x_win(username, int(bid), 2)
                total_balance = final_balance(balance)
                await ctx.send(f'The coin landed on {coin}!\nYour New Balance is {total_balance}')
            else:
                total_balance = final_balance(balance)
                await ctx.send(f'The coin landed on {coin}!\nYour New Balance is {total_balance}')
        else:
                await ctx.send("You do not have enough money to make that bid!")
    else:
        if not no_call:
            await ctx.send('You must make a valid call! //cointoss (amount) ("Heads" or "Tails").')        

@slash.slash(name='give', description='Owner can give credits this way!', guild_ids=[755112397454180443])
@commands.has_role("Owner")
async def give_creds(ctx:SlashContext, member: discord.Member, credits):
    username = (str(member)).split('#')[0]
    roulette_x_win(username, int(credits), 1)
    balance = display_current_balance(username)
    embed=discord.Embed(title = f'{username.capitalize()}\'s Balance', description=f'Your new balance is {balance}', color=0xF4513B)
    await ctx.send(embed=embed)

@slash.slash(name='take', description='Owner can take credits away this way!', guild_ids=[755112397454180443])
@commands.has_role("Owner")
async def give_creds(ctx:SlashContext, member: discord.Member, credits):
    username = (str(member)).split('#')[0]
    roulette_x_win(username, int(credits), -1)
    balance = display_current_balance(username)
    embed=discord.Embed(title = f'{username.capitalize()}\'s Balance', description=f'Your new balance is {balance}', color=0xF4513B)
    await ctx.send(embed=embed)



# FIX OASIS COMMAND, TEMPORTARILY DISABLED

@slash.slash(name='oasis', description='"/help oasis" for more information', guild_ids=[755112397454180443])
async def oasis(ctx:SlashContext):
    cards = ['A♤', '2♤', '3♤', '4♤', '5♤', '6♤', '7♤', '8♤', '9♤', '10♤', 'J♤', 'Q♤', 'K♤',
             'A♡', '2♡','3♡', '4♡', '5♡', '6♡', '7♡', '8♡', '9♡', '10♡', 'J♡', 'Q♡', 'K♡',
             'A♢', '2♢', '3♢', '4♢', '5♢', '6♢', '7♢', '8♢', '9♢', '10♢', 'J♢', 'Q♢', 'K♢',
             'A♧', '2♧', '3♧', '4♧', '5♧', '6♧', '7♧', '8♧', '9♧', '10♧', 'J♧', 'Q♧', 'K♧'
            ]

    test_string = ''
    test_string2 = ''
    for i in range(10):
        if i > 4:
            value = random.choice(cards)
            index = cards.index(value)
            cards.pop(index)
            test_string2 += f'{value}   '
        else:
            value = random.choice(cards)
            index = cards.index(value)
            cards.pop(index)
            test_string += f'{value}   '

    embed=discord.Embed(color=0xF4513B)
    embed.add_field(name="Dealer's Hand", value=test_string2, inline=False)
    embed.add_field(name="Your Hand", value=test_string, inline=False)
    msg = await ctx.send(embed=embed)

    await msg.add_reaction(':one:847211700147191848')
    await msg.add_reaction(':one:847211700147191848')
    await msg.add_reaction('<:two:847212663570432001>')
    await msg.add_reaction('<:three:847216300022562816>')
    await msg.add_reaction('<:four:847214057153101864>')
    await msg.add_reaction('<:five:847215039856508980>')
    await msg.add_reaction('<:next:847215688933179403>')

@slash.slash(name='slots', description='It\'s a slot machine...', guild_ids=[755112397454180443])
async def slot_machine(ctx:SlashContext, bid):
    credits = int(bid)
    username = ctx.author.name
    if credits == None:
        await ctx.send('Please specify an amount of credits!')
    else:
        check_balance = check_bal(username, credits)
        if check_balance:
            credit_dedux(username, credits)
            random_slot_item = {
                1: ['🍌 ', 20], # 20% chance
                2: ['🐿️ ', 36], # 16 % chance
                3: ['🐬 ', 51.5], # 15.5% chance
                4: ['<:plush:798711975776354306> ', 64], # 12.5 % chance
                5: ['🎲 ', 76.5], # 12.5 % chance
                6: ['⚠️ ', 86.5], # 10 % chance
                7: ['🅱️ ', 94], # 7.5 % chance
                8: ['🎱 ', 99], # 5 % chance
                9:  ['<:yesmoney:559875535262580758> ', 100] # 1 % chance
            }
            slots = ''
            types = []
            for _ in range(3):
                percent = random.random()
                percent *= 100
                if 0 <= percent <= random_slot_item[1][1]:
                    slots += random_slot_item[1][0]
                    types.append(1)
                elif random_slot_item[1][1] < percent <= random_slot_item[2][1]:
                    slots += random_slot_item[2][0]
                    types.append(2)
                elif random_slot_item[2][1] < percent <= random_slot_item[3][1]:
                    slots += random_slot_item[3][0]
                    types.append(3)
                elif random_slot_item[3][1] < percent <= random_slot_item[4][1]:
                    slots += random_slot_item[4][0]
                    types.append(4)
                elif random_slot_item[4][1] < percent <= random_slot_item[5][1]:
                    slots += random_slot_item[5][0]
                    types.append(5)
                elif random_slot_item[5][1] < percent <= random_slot_item[6][1]:
                    slots += random_slot_item[6][0]
                    types.append(6)
                elif random_slot_item[6][1] < percent <= random_slot_item[7][1]:
                    slots += random_slot_item[7][0]
                    types.append(7)
                elif random_slot_item[7][1] < percent <= random_slot_item[8][1]:
                    slots += random_slot_item[8][0]
                    types.append(8)
                elif random_slot_item[8][1] < percent <= random_slot_item[9][1]:
                    slots += random_slot_item[9][0]
                    types.append(9)
                else:
                    slots += 'Execution Error!\n'

            win_value = check_win_slots(slots, types, credits)
            if win_value > 0:
                delimiter = '+'
                roulette_x_win(username, win_value, 1)
            else:
                delimiter = '-'
                win_value = credits

            await ctx.send(f'{slots} < | {delimiter} {win_value:.0f}')

        else:
            await ctx.send('You need more money to make that bid!')

# @slash.slash(name='testEmbeds', description='E', guild_ids=[755112397454180443])
# async def embed(ctx:SlashContext):
    # embed=discord.Embed(title="Sample Embed", url="https://realdrewdata.medium.com/", help="This is an embed that will show how to build an embed and the different components", color=0xFF5733)
    # await ctx.send(embed=embed)

@slash.slash(name='levelup', description='Use this to level up!', guild_ids=[755112397454180443])
async def levelup(ctx:SlashContext, confirm=None):
    '''
        Give's level information and levels up the user

        ctx = user info
        confirm = confirms the user wants to level up
    '''
    await ctx.defer()
    username = ctx.author.name
    userFound = False

    # Grabs all information from a database
    userDB = cluster['MathBot']
    userCollection = userDB['users']
    users = userCollection.find()

    for user in users:
        if user['_id'] == username: # user found in database
            userFound = True
            level_price = round(100 * (user['level'] + 1) + ((user['level'] + 1) ** 3), 0) # Mathematically increases the price of a levelup
            if confirm == None:
                await ctx.send(f'The price to level up will be ${level_price:,.2f}.'.format(amount))
            elif user['balance'] >= level_price: # User wants to level up and CAN level up
                userCollection.update_one({"_id": username}, {"$set": {'level': user['level'] + 1}})
                userCollection.update_one({"_id": username}, {"$set": {'balance': user['balance'] - level_price}})
                await ctx.send(f'You have successfully leveled up to level {user["level"] + 1}')
    if not userFound:
        await ctx.send("You were either not found in our database! Please type /balance to create an account with us!")

@slash.slash(name='level', description='Use this to level up!', guild_ids=[755112397454180443])
async def levelup(ctx:SlashContext):
    '''
        Displays the current level of the user
    '''
    username = ctx.author.name
    userFound = False

    userDB = cluster['MathBot']
    userCollection = userDB['users']
    users = userCollection.find()

    for user in users:
        if user['_id'] == username:
            userFound = True
            await ctx.send(f"Your current level is {user['level']}")
    if not userFound:
        await ctx.send("You weren't found in the database! Please type /balance to be placed in the system!")

@slash.slash(name='shop', description='Displays commands and prices for items to purchase', guild_ids=[755112397454180443])
async def shop(ctx:SlashContext, option=None, number=None):
    username = ctx.author.name
    nicknames = {1: ['( ͡° ͜ʖ ͡°)', 150000],
                 2: ['(∩ȍ ʖ̯ȍ)⊃━☆ﾟ.*', 200000],
                 3: ['(っ^‿^)っ', 250000],
                 4: ['(╯✧≖ᨓ≖）╯︵ ┻━┻', 1500000],
                 5: ['ḑ̷̧̬̞͔̺̥͉̠͍͙͓̳̲̘͍̤̲̀͊̌̂͂̈́͑̉́̇̇̄̇̈́́̈́͂̂̾͑̄͘͝͝ę̴͖̥̟͙̺̩̹̣̱̣̤̌̈́͐̓͌̽̾̀̊̄̆̓̐̿͒̏̄̿͒̓͐̑̈̀̂̔̇̋̅̽͑̆̃̿͗́͑͂̉̕̕͠͝͝ą̴̭̼̹͍̩͔͎̞̜͙͈̆̋̍̓̋̈́̎͂̎̍̀̄̒̂͑̐̈́̋̈̈́̐̌̏̀̊͑́̎́̎̒̚͘̕̕͘͝͠͠͝͝t̷̨̬͈͍̝̱̀̇̎̈́̃̏̑͘̕ḩ̸̧̨̡̢̛̛͖̜̱͎̙͇̜̩͚̖̦̠̤͔̥̬͈̙̰̘͙͗͛̃̃͂́͑͋̅̉̌͑͑̽̊̏͛̆̓̂͒̉̑̃̏̌̐́͋͋̈́̈́̒͒̆̕̕͘̕͜͜͝', 2750000],
                 6: ['s̷͈̎a̸͙͐n̵̦̾v̵̗̐i̵̘̚č̷̯h̴̥͒ 🥪', 3250000],
                 7: ['товарищ', 4250000],
                 8: ['─=≡Σᕕ( ﾟᗜ ﾟ)ᕗ', 9500000],
                 9: ['ウィーブ', 10000000],
                 10: ['ヽ༼ຈل͜ຈ༽ﾉ', 10000001],
                 11: ['Problematic', 12500000],
                 12: ['True Gamer', 22500000],
                 13: ['ლ(▰෴▰ლ)', 25000000],
                 14: [" ̿ ̿'̿'\̵͇̿̿\з=(•_•)=ε/̵͇̿̿/'̿'̿ ̿", 27500000],
                 15: ['□ᨎ□', 30000000],
                 16: ['Steev Jahbz', 45500000],
                 17: ['(╭☞ ͡⎚ロ ͡⎚)╭☞', 52500000],
                 18: ['♋︎', 694201337],
                 19: ['DeLimiter', 99999999],
                 20: ['(っ◔◡◔)っ ♥ Cannibalism ♥', 100000000],
                 21: ['🍌', 500000000],
                 22: ['Bit Boi', 2147483647],
                 23: ['ງค๓๖liຖງ ค໓໓i¢t', 10000000000]}

    backgrounds = ['[Beach](https://www.worldsbestbars.com/wp-content/uploads/2021/11/South-africa-tracks-on-the-rocks-1920x720.jpg)',
                   '[Bubbly](https://gmedia.playstation.com/is/image/SIEPDC/SummerDeals-kv-main-01-20210709-pc-1920x720?$native$)',
                   '[Circuit](https://www.incoproip.com/wp-content/uploads/2020/06/Evolution-of-counterfeiting_banner-992x0-c-default.jpg)',
                   '[Dots]()',
                   '[Ducks]()',
                   '[Flame](https://www.phdmedia.com/nicaragua/wp-content/uploads/sites/96/2017/03/banner-583.jpg)',
                   '[Forest]()',
                   '[Hue_Arrows](https://cdn.wallpapersafari.com/75/77/x4j1Rb.jpg)',
                   '[Landscape](https://photos.tripsite.com/assets/files/1380/sunset-5371719.1920x720.jpg)',
                   '[Map](https://excelsiorclasses.com/wp-content/uploads/2019/04/banner-3544296_1920.jpg)',]

    backgrounds2 = ['[Node](https://www.microsoft.com/en-us/research/uploads/prod/2012/12/NYCAGTImage-1920x720.jpg)',
                    '[One_Piece](https://wallpaperaccess.com/full/4205679.jpg)',
                    '[Plasma](https://wp.biologos.org/wp-content/uploads/2018/11/science-and-god-1920x720.jpg)',
                    '[Polyhedral](https://wallpaperaccess.com/full/1615368.jpg)',
                    '[Red_Basic](https://images.squarespace-cdn.com/content/v1/5e1a8289c429c302ddea1459/1596503590491-UUJNM80B7C2QAADHZ5U6/Web+Banner6.jpg?format=2500w)',
                    '[Sky](https://wp.biologos.org/wp-content/uploads/2019/10/sunset-WEB-1920x720.jpg)',
                    '[Waifu](https://static.zerochan.net/Cocoro%40Function%21.full.1812576.jpg)',
                    '[Waterfall](https://wallpaperaccess.com/full/4205645.jpg)',
                    '[Wave](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSNE-EhuylARyoTZ_lH6Epg2BYVQF4aEY5cUw&usqp=CAU)',
                    '[Zendikar](https://images.ctfassets.net/s5n2t79q9icq/2Pa7QHLWU1h7fn0uSp78OU/f96c13fc30647c976354e549ea423e24/backdrop-red-mountain.jpg?q=70)']

    if option == None: # User is browsing the shop
        nickname_format = ''
        backgrounds_format = ''
        backgrounds2_format = ''
        for i in nicknames.keys():
            nickname_format += f"{i}) {nicknames[i][0]} ${nicknames[i][1]:,.2f}\n".format(amount)
        for i in backgrounds:
            backgrounds_format += i + '\n'
        for i in backgrounds2:
            backgrounds2_format += i + '\n'

        embed=discord.Embed(title="Shop", help="This is an embed that will show how to build an embed and the different components", color=0xFF5733)
        # embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name="Nicknames", value=nickname_format, inline=True)
        embed.add_field(name="Backgrounds", value = backgrounds_format, inline=True) # FUTURE PURCHASABLES
        embed.add_field(name="More Backgrounds", value = backgrounds2_format, inline=True) # FUTURE PURCHASABLES
        embed.set_footer(text=f"Request made by: {username}")
        embed.set_author(name=username, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    else: # User wants to buy something
        if option == 'nicknames':
            if number.isdecimal:
                number = int(number)
                if number in nicknames:
                    valid_balance = check_bal(username, nicknames[number][1])
                    if valid_balance:
                        userDB = cluster['MathBot']
                        userCollection = userDB['users']
                        users = userCollection.find()

                        for user in users:
                            if user['_id'] == username:
                                if nicknames[number][0] not in user['nicknames']:
                                    userCollection.update_one({"_id": username}, {"$set": {'nicknames': user['nicknames'] + [nicknames[number][0]]}})
                                    credit_dedux(username, nicknames[number][1])
                                    await ctx.author.edit(nick=nicknames[number][0])
                                    await ctx.send(f'Your name has been updated to {nicknames[number][0]}')
                                else:
                                    await ctx.author.edit(nick=nicknames[number][0])
                                    await ctx.send(f'You already have that nickname! Don\'t worry though, we went ahead and updated your name to {nicknames[number][0]}')
                    else:
                        await ctx.send(f"You do not have enough money to purchase that item, {username}!")
            else: await ctx.send("Please enter a valid number!")

@slash.slash(name='color', description='Shows your stats!', guild_ids=[755112397454180443])
async def test(ctx: SlashContext, color):
    username = ctx.author.name
    userFound = False
    color = color.lower()

    color_names = {'white': (255, 255, 255),    'light_grey': (132, 132, 130),   'dark_grey': (85, 85, 85),   'black': (0, 0, 0),
                    'red': (255, 0, 0),          'blue': (0, 0, 255),             'scarlet': (255, 36, 0),     'blue_green': (13, 152, 186),
                    'orange': (255, 127, 0),     'purple': (96, 0, 128),          'tangerine': (242, 133, 0),  'golden_brown': (184, 134, 11),
                    'yellow': (255, 255, 0),     'pink': (255, 192, 203),         'teal': (0, 128, 128),       'Hazelnut': (133, 117, 78),
                    'green': (0, 255, 0),        'brown': (136, 84, 11),          'turquoise': (64, 224, 208), 'lime': (50, 205, 50),
                    'sunflower': (227, 171, 87), 'sea_green': (46, 139, 87),      'sky_blue': (135, 206, 235), 'periwinkle': (204, 204, 255), 
                    'amber': (255, 191, 0),      'grass_green': (19, 136, 8),     'indigo': (75, 0, 130),      'azure_blue': (0, 127, 255), 
                    'caramel': (153, 101, 21),   'carrot_orange': (237, 145, 33), 'warm_white': (255, 222, 173)}
    userDB = cluster['MathBot']
    userCollection = userDB['users']
    users = userCollection.find()

    for user in users:
        if user['_id'] == username:
            if color in color_names:
                color_chosen = color_names[color]
                userCollection.update_one({"_id": username}, {"$set": {'text_color': color_chosen}})
                userFound = True
                await ctx.send("Color Updated! Use '/info' to see your new color!")
    if not userFound:
        await ctx.send("Looks like you're not in our database! Please use '/setup' to be placed in the database")

@slash.slash(name='background', description='Choose which background to view when using /info!', guild_ids=[755112397454180443])
async def test(ctx: SlashContext, background):
    username = ctx.author.name
    userFound = False

    background_names = ['beach', 'bubbly', 'circuit', 'dots', 'ducks', 'flame', 'forest', 'hue_arrows',
                        'landscape', 'map', 'node', 'one_piece', 'plasma', 'polyhedral', 'red_basic', 'sky',
                        'waifu', 'waterfall', 'wave', 'zendikar']
            
    userDB = cluster['MathBot']
    userCollection = userDB['users']
    users = userCollection.find()

    for user in users:
        if user['_id'] == username:
            userFound = True
            if background in background_names:
                userCollection.update_one({"_id": username}, {"$set": {'background': f'{background}.png'}})
                await ctx.send("Background Updated! Use '/info' to see your new color!")
            else:
                await ctx.send('That background isn\'t in our database! Please refer to "/shop" to view our backgrounds! Although they are in the shop, the backgrounds are entirely free!')
    if not userFound:
        await ctx.send("Looks like you're not in our database! Please use '/setup' to be placed in the database")

@slash.slash(name='font', description='Choose which font to view when using /info!', guild_ids=[755112397454180443])
async def test(ctx: SlashContext, font):
    username = ctx.author.name
    userFound = False

    font_names = ['arial', 'comic', 'bahnschrift', 'consola', 'impact' , 'segoesc']
            
    userDB = cluster['MathBot']
    userCollection = userDB['users']
    users = userCollection.find()

    for user in users:
        if user['_id'] == username:
            userFound = True
            if font in font_names:
                userCollection.update_one({"_id": username}, {"$set": {'font': f'{font}.ttf'}})
                await ctx.send("Font Updated! Use '/info' to see your new color!")
            else:
                await ctx.send('That background isn\'t in our database! Please refer to "/shop" to view our backgrounds! Although they are in the shop, the backgrounds are entirely free!')
    if not userFound:
        await ctx.send("Looks like you're not in our database! Please use '/setup' to be placed in the database")

@slash.slash(name='info', description='Shows your stats!', guild_ids=[755112397454180443])
async def test(ctx: SlashContext):
    await ctx.defer()
    username = ctx.author.name

    userFound = False

    userDB = cluster['MathBot']
    userCollection = userDB['users']
    users = userCollection.find()

    for user in users:
        if user['_id'] == username:
            userFound = True
            level = user['level']
            balance = user['balance']
            image = user['background'] # Background of the image
            userFont = user['font'] # Font the user chooses
            font_color = (user['text_color'][0], user['text_color'][1], user['text_color'][2]) # RGB Tuple defining the color of the text
    if userFound:
        with Image.open(f"banners/{image}") as img:
            draw = ImageDraw.Draw(img) # Initializes the background
            # Font for text and set's information on background
            fontsize = 80
            font = ImageFont.truetype(userFont, fontsize)
            draw.text((675, 160), username.title(), font_color, font=font)
            draw.text((675, 320), f"Level: {level}", font_color, font=font)
            draw.text((675, 480), f"Balance: ${balance:,.2f}".format(amount), font_color, font=font)
            # Grabs user's avatar and saves it to avatar.png
            avatar = ctx.author.avatar_url
            response = requests.get(avatar)
            img2 = Image.open(BytesIO(response.content))
            img2 = img2.resize([480, 480])
            img2.save('avatar.png')
            # # ^^^ # GRABS THE USER'S AVATAR AND SAVES IT TO A FILE # ^^^ #
            # # vvv # GRABS THE AVATAR AND CONVERTS IMAGE TO CIRCLE # vvv #
            # img2=Image.open("avatar.png").convert("RGB") # COMMENTED OUT RIGHT NOW DUE TO CIRCLE BEING DUMBDUMB
            # npImage=np.array(img2)
            # h,w=img2.size
            # alpha = Image.new('L', img2.size,0)
            # draw = ImageDraw.Draw(alpha)
            # draw.pieslice([0,0,h,w],0,360,fill=255)
            # npAlpha=np.array(alpha)
            # npImage=np.dstack((npImage,npAlpha))
            # Image.fromarray(npImage).save('avatar.png')
            # ^^^ # CONVERTS THE IMAGE TO A CIRCLE # ^^^ #
            avatar = Image.open('avatar.png')
            img.paste(avatar, (120, 120))
            img.save('placeholder.png')
            picture = discord.File('placeholder.png')
            await ctx.send(file=picture)
    else:
        await ctx.send("Looks like you weren't found in the database! Please use /setup to do so and try again!")
bot.run(TOKEN)