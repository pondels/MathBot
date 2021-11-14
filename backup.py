import os
import random
from datetime import datetime
from csv import writer
import discord
from discord.ext import commands
from discord.ext.commands.core import check
from discord.utils import get
from dotenv import load_dotenv
from pymongo import MongoClient
from discord_slash import SlashCommand, SlashContext

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN1')
cluster = MongoClient('mongodb+srv://mathidiot:sparky123592n600@character-creation-shee.pqgon.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')

amount = 0

bot = commands.Bot(command_prefix='//')
slash = SlashCommand(bot, sync_commands=True) 

@slash.slash(name='balance', description='Checks your current balance.', guild_ids=[755112397454180443])
async def balance(ctx: SlashContext):

    await ctx.defer()
    username = ctx.author.name
    balanceFound = False

    # Searches the MathBot Database and grabs all users
    userDB = cluster['MathBot']
    userCollection = userDB['users']
    users = userCollection.find()
    
    response = f'You did not have an account with us so we opened up an account for you, {username}! \
                    \nPlease type //balance again to view your balance!\nTo learn more about how you earn credits, type //creditshelp!'

    # Searches the user until it finds the player who ran the command
    for user in users:
        if user['_id'] == username:
            embed=discord.Embed(title = f'{ctx.author.name.capitalize()}\'s Balance', description=f'Balance: {user["balance"]} mChips!', color=0xF4513B)
            await ctx.send(embed=embed)
            balanceFound = True

    # If No one was found, place them into the database
    if not balanceFound:
        post = {'_id': username, 'balance': 1000, 'daily': 0, 'weekly': 0, 'monthly': 0}
        userCollection.insert_one(post)
        await ctx.send(response)

@slash.slash(name='creditshelp', description='Teaches you how you earn credits using my bot!', guild_ids=[755112397454180443])
async def help_center(ctx:SlashContext):
    await ctx.send(f'It is very simple to earn credits using my bot, it is also very abusable, but I don\'t care, that\'s the reward!\nTo gain credits to your name, you simply just use commands on my bot, and a random amount of credits will be rewarded!\n\nThese credits can be used to gamble, unlock cool things, such as ranks, and much more!\nOther commands to claim mChips inclide //daily, //weekly, and //monthly. As in their names, you must wait that long to claim it again.\nTo see what commands we have to offer, use the //help command.')

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
                await ctx.send(f'You have insufficient funds! Please check your balance by using //balance!')
        else:
            await ctx.send('Please type a positive amount of credits!')
    else:
        await ctx.send('Please type a valid input for your credits! Ex. "//rps \'12\' \'rock\'"\nThis will place a 12 mChip bet on rock!')

@slash.slash(name='roulette', description='//roulettehelp to learn how to use this command properly.', guild_ids=[755112397454180443])
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
                                await ctx.send('Woah there! You\'re bidding on a non-existent number! //roulettehelp to view the board!')
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
                    await ctx.send(f'Please input a valid number of credits! //balance to see how much money you have!')
            else:
                await ctx.send('Please enter a valid integer as a bid')
        else:
            await ctx.send('You have to enter a bid! //roulette "Bid" "Color". //roulettehelp for more info')
    except:
        await ctx.send('We do not see you in our system. Please type //balance to create an account with us!')

@slash.slash(name='roulettehelp', description='Helps you properly use the roulette command.', guild_ids=[755112397454180443])
async def rhelp(ctx:SlashContext):
    red_numbers = str("""```diff\n- RED NUMBERS\n``````1 3 5 7 9 12 14 16 18 21 23 25 27 28 30 32 34 36```""")
    stragnt = '00 0'
    green_numbers = str(f"""```css\nGREEN COLORS\n``````css\n{stragnt}```""")
    black_numbers = str("""```BLACK COLORS\n``````2 4 6 8 10 11 13 15 17 19 20 22 24 26 29 31 33 35```""")
    roulette_command = str("""```css\n//roulette "Credits" "Color (R G B N)" "Number Relating to Color"```""")
    await ctx.send(f'To properly use the //roulette command, you must know the board and the format of the command to place your bet.\n\nThe command should go something like this, {roulette_command}\nEach color letter corresponds to a certain color. G = Green, R = Red, B = Black, and N = No Color\nNo color is usually used when you are bidding on a number rather than a color, however it does not matter what you put, just so long that you place in a valid color.\nYou DO NOT need to place something in the number slot. The only slots that require input is the Credits, and Color.\nIf you place a bet in the number, it will place your outcome very high but chances of you winning are very low, so keep that in mind.\n\nIf you need access to the roulette board, you can always type, //roulettehelp,\nHere\'s the board for reference.\n{red_numbers} {green_numbers} {black_numbers}')

@slash.slash(name='Daily', description='Your Daily Claim!', guild_ids=[755112397454180443])
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
                userInfo.update_one({"_id": username}, {"$set": {'balance': user['balance'] + rewardChoice}}) # Updates the Balance of the User
                userInfo.update_one({"_id": username}, {"$set": {time: datetime.now()}}) # Updates the Daily Timer
                return f"+{rewardChoice}$ Your New Balance: ${user['balance'] + rewardChoice}" # Returns a string formatted balance to the user
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
                    userInfo.update_one({"_id": username}, {"$set": {'balance': user['balance'] + rewardChoice}}) # Updates the Balance of the User
                    userInfo.update_one({"_id": username}, {"$set": {time: datetime.now()}}) # Updates the x Timer
                    return f"+{rewardChoice}$ Your New Balance: ${user['balance'] + rewardChoice}" # Returns a string formatted balance to the user
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
    userDB = cluster['MathBot']
    userCollection = userDB['users']
    users = userCollection.find()

    for user in users:
        if user["_id"] == username:
            userCollection.update_one({"_id": username}, {"$set": {'balance': user['balance'] - (bid)}})
            return user['balance'] - bid

def final_balance(end_balance):
    final_balance = f"{end_balance} mChips"
    return final_balance

def roulette_x_win(username, credits, multiplier):
    '''
        Take the balance of the user and update it to their 
        balance + the multiplier * credits
    '''
    userDB = cluster['MathBot']
    userCollection = userDB['users']
    users = userCollection.find()

    for user in users:
        if user["_id"] == username:
            userCollection.update_one({"_id": username}, {"$set": {'balance': user['balance'] + (credits*multiplier)}})
            return user['balance'] + credits * multiplier

def check_bal(username, bid):
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
                coinflip = ['Heads', 'Tails']
                coin = random.choice(coinflip)
                balance = credit_dedux(username, int(bid))
                if call.lower() == coin.lower():
                    balance = roulette_x_win(ctx, bid, 2)
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
@commands.has_role("Owner") # This must be exactly the name of the appropriate role
async def give_creds(ctx:SlashContext, member: discord.Member, credits):
    username = (str(member)).split('#')[0]
    roulette_x_win(username, int(credits), 1)
    balance = display_current_balance(username)
    embed=discord.Embed(title = f'{ctx.author.name.capitalize()}\'s Balance', description=f'Your new balance is {balance}', color=0xF4513B)
    await ctx.send(embed=embed)

@slash.slash(name='take', description='Owner can take credits away this way!', guild_ids=[755112397454180443])
@commands.has_role("Owner") # This must be exactly the name of the appropriate role
async def give_creds(ctx:SlashContext, member: discord.Member, credits):
    username = (str(member)).split('#')[0]
    roulette_x_win(username, int(credits), -1)
    balance = display_current_balance(username)
    embed=discord.Embed(title = f'{username.capitalize()}\'s Balance', description=f'Your new balance is {balance}', color=0xF4513B)
    await ctx.send(embed=embed)



# FIX OASIS COMMAND, TEMPORTARILY DISABLED

@slash.slash(name='oasis', description='//oasishelp for more help', guild_ids=[755112397454180443])
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

# @bot.command(name='oasishelp', help='Teaches you how to use the oasis command')
# async def helpoasis(ctx):
#     pass

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

@slash.slash(name='placeholder', description='This is just a placeholder command for me to brainstorm new ideas', guild_ids=[755112397454180443])
async def brainstorm(ctx:SlashContext):
    await ctx.send(f'You don\'t get to see my ideas because they\'re commented out >:D')
    # Monopoly?????? (Its own bot)
    # Checkers 
    # Uno? // Problems with personal hands and spamming DM's // Maybe find a workaround?
    # Oasis Poker // Also known as the LUIGI POKER GAME FROM MY MARIO DS THINGY, yeah that game
    # Coin Toss against other people
    # Have a shop command that allows you to gain access to ranks and other things.

# @slash.slash(name='testEmbeds', description='E', guild_ids=[755112397454180443])
# async def embed(ctx:SlashContext):
    # embed=discord.Embed(title="Sample Embed", url="https://realdrewdata.medium.com/", help="This is an embed that will show how to build an embed and the different components", color=0xFF5733)
    # await ctx.send(embed=embed)

@slash.slash(name='shop', description='Displays commands and prices for items to purchase', guild_ids=[755112397454180443])
async def shop(ctx:SlashContext, option=None, number=None):
    username = ctx.author.name
    nicknames = {1: ['( ͡° ͜ʖ ͡°)', 150000],
                 2: ['(∩ȍ ʖ̯ȍ)⊃━☆ﾟ.*', 200000],
                 3: ['(っ^‿^)っ', 250000],
                 4: ['(╯✧≖ᨓ≖）╯︵ ┻━┻', 1500000],
                 5: ['ḑ̷̧̬̞͔̺̥͉̠͍͙͓̳̲̘͍̤̲̀͊̌̂͂̈́͑̉́̇̇̄̇̈́́̈́͂̂̾͑̄͘͝͝ę̴͖̥̟͙̺̩̹̣̱̣̤̌̈́͐̓͌̽̾̀̊̄̆̓̐̿͒̏̄̿͒̓͐̑̈̀̂̔̇̋̅̽͑̆̃̿͗́͑͂̉̕̕͠͝͝ą̴̭̼̹͍̩͔͎̞̜͙͈̆̋̍̓̋̈́̎͂̎̍̀̄̒̂͑̐̈́̋̈̈́̐̌̏̀̊͑́̎́̎̒̚͘̕̕͘͝͠͠͝͝t̷̨̬͈͍̝̱̀̇̎̈́̃̏̑͘̕ḩ̸̧̨̡̢̛̛͖̜̱͎̙͇̜̩͚̖̦̠̤͔̥̬͈̙̰̘͙͗͛̃̃͂́͑͋̅̉̌͑͑̽̊̏͛̆̓̂͒̉̑̃̏̌̐́͋͋̈́̈́̒͒̆̕̕͘̕͜͜͝', 2750000],
                 6: ['s̷͈̎a̸͙͐n̵̦̾v̵̗̐i̵̘̚č̷̯h̴̥͒', 3250000],
                 7: ['товарищ', 4250000],
                 8: ['─=≡Σᕕ( ﾟᗜ ﾟ)ᕗ', 9500000],
                 9: ['ウィーブ', 100000000]}
    if option == None:
        nickname_format = ''
        count = 1
        for i in nicknames.keys():
            nickname_format += f"{i}) {nicknames[i][0]}--- ${nicknames[i][1]:,.2f}\n".format(amount)
            count += 1
        embed=discord.Embed(title="Shop", help="This is an embed that will show how to build an embed and the different components", color=0xFF5733)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name="Nicknames", value=nickname_format, inline=False)
        embed.set_footer(text=f"Request made by: {username}")
        # embed.add_field(name="Your Hand", value=test_string, inline=False)
        await ctx.send(embed=embed)
    else:
        if option == 'nicknames':
            if number.isdecimal:
                number = int(number)
                if number in nicknames:
                    valid_balance = check_bal(username, nicknames[number][1])
                    if valid_balance:
                        credit_dedux(username, nicknames[number][1])
                        await ctx.author.edit(nick=nicknames[number][0])
                        await ctx.send(f'Your name has been updated to {nicknames[number][0]}')
                    else:
                        await ctx.send(f"You do not have enough money to purchase that item, {username}!")
            else: await ctx.send("Please enter a valid number!")

bot.run(TOKEN)