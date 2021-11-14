# bot.py
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
from discord.ext.commands.core import check
import pandas as pd
from discord.utils import get
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN1')

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

bot = commands.Bot(command_prefix='//')

@bot.event
async def on_ready():
    print('Math bot Has Connected!')

class NewHelpName(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page)
            await destination.send(embed=emby)

bot.help_command = NewHelpName()

# @bot.command(name='help', help='Provides each command and its help section.')
# async def help(ctx):
#     commands = ['']
#     await ctx.send()

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

@bot.command(name='creditshelp', help='Teaches you how you earn credits using my bot!')
async def help_center(ctx):
    await ctx.send(f'It is very simple to earn credits using my bot, it is also very abusable, but I don\'t care, that\'s the reward!\nTo gain credits to your name, you simply just use commands on my bot, and a random amount of credits will be rewarded!\n\nThese credits can be used to gamble, unlock cool things, such as ranks, and much more!\nOther commands to claim mChips inclide //daily, //weekly, and //monthly. As in their names, you must wait that long to claim it again.\nTo see what commands we have to offer, use the //help command.')
    gain_credits(ctx)

@bot.command(name='rps', help="//rps 'credits' 'rock,paper, or scissors'")
async def rps(ctx, credits, rps_input):
    username = ctx.author.name
    if credits.isdecimal:
        credits = int(credits)
        if int(credits) > 0:
            truth = check_bal(ctx, credits)
            
            if truth:
                
                if rps_input.lower() == 'scissors' or rps_input.lower() == 'rock' or rps_input.lower() == 'paper':
                    result = ['rock', 'paper', 'scissors']
                    
                    if rps_input.lower() == 'rock':
                        final_result = random.choice(result)
                        
                        if final_result == rps_input.lower():
                            await ctx.send(f'{username}: {rps_input.capitalize()}!\nMath Bot: {final_result}!\nYou Tied!\n\nYour new balance is {display_current_balance(ctx)}.')
                        
                        elif final_result == 'scissors':
                            balance = credit_dedux(ctx, credits)
                            balance = roulette_x_win(ctx, credits, 2)
                            await ctx.send(f'{username}: {rps_input.capitalize()}!\nMath Bot: {final_result}!\nYou Win!\n\nYour new balance is {balance}.')
                        
                        else:
                            balance = credit_dedux(ctx, credits)
                            await ctx.send(f'{username}: {rps_input.capitalize()}!\nMath Bot: {final_result}!\nYou Lost!\n\nYour new balance is {balance}.')
                    
                    elif rps_input.lower() == 'paper':
                        final_result = random.choice(result)
                        
                        if final_result == rps_input.lower():
                            await ctx.send(f'{username}: {rps_input.capitalize()}!\nMath Bot: {final_result}!\nYou Tied!\n\nYour new balance is {display_current_balance(ctx)}.')
                        
                        elif final_result == 'rock':
                            balance = credit_dedux(ctx, credits)
                            balance = roulette_x_win(ctx, credits, 2)
                            await ctx.send(f'{username}: {rps_input.capitalize()}!\nMath Bot: {final_result}!\nYou Win!\n\nYour new balance is {balance}.')
                        
                        else:
                            balance = credit_dedux(ctx, credits)
                            await ctx.send(f'{username}: {rps_input.capitalize()}!\nMath Bot: {final_result}!\nYou Lost!\n\nYour new balance is {balance}.')
                    else:
                        final_result = random.choice(result)
                        
                        if final_result == rps_input.lower():
                            await ctx.send(f'{username}: {rps_input.capitalize()}!\nMath Bot: {final_result}!\nYou Tied!\n\nYour new balance is {display_current_balance(ctx)}.')
                        
                        elif final_result == 'paper':
                            balance = credit_dedux(ctx, credits)
                            balance = roulette_x_win(ctx, credits, 2)
                            await ctx.send(f'{username}: {rps_input.capitalize()}!\nMath Bot: {final_result}!\nYou Win!\n\nYour new balance is {balance}.')
                        
                        else:
                            balance = credit_dedux(ctx, credits)
                            await ctx.send(f'{username}: {rps_input.capitalize()}!\nMath Bot: {final_result}!\nYou Lost!\n\nYour new balance is {balance}.')
                else:
                    await ctx.send('Please leave a valid response! i.e. "Rock", "Paper", "Scissors".')
            else:
                await ctx.send(f'You have insufficient funds! Please check your balance by using //balance!')
        else:
            await ctx.send('Please type a positive amount of credits!')
    else:
        await ctx.send('Please type a valid input for your credits! Ex. "//rps \'12\' \'rock\'"\nThis will place a 12 mChip bet on rock!')

@bot.command(name='roulette', help='//roulettehelp to learn how to use this command properly.')
async def gamble(ctx, credits=None, color=None, number=None):
    chosen_color = ''
    try:
        if credits != None:
            if credits.isdecimal():
                positive = check_bal(ctx, credits)
                if positive:
                    credits = int(credits)
                    if color == 'R' or color == 'G' or color == 'B' or color == 'N':
                        roulette_numbers = ['00', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]
                        red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 21, 23, 25, 27, 28, 30, 32, 34, 36]
                        black_numbers = [2, 4, 6, 8, 10, 11, 13, 15, 17, 19, 20, 22, 24, 26, 29, 31, 33, 35]
                        chosen_number = random.choice(roulette_numbers)
                        if number != None:
                            if number == number:
                                balance = credit_dedux(ctx, credits)
                                chosen_number = random.choice(roulette_numbers)

                                if chosen_number == int(number):
                                    response = f'The ball landed on {chosen_number}, Congratulations!'
                                    balance = roulette_x_win(ctx, credits, 36)
                                    total_balance = final_balance(balance)
                                    await ctx.send(f'{response}\nYour New Balance is: {total_balance}')
                                elif chosen_number == str(number):
                                    response = f'The ball landed on {chosen_number}, Congratulations!'
                                    balance = roulette_x_win(ctx, credits, 36)
                                    total_balance = final_balance(balance)
                                    await ctx.send(f'{response}\nYour New Balance is: {total_balance}')

                                else:
                                    total_balance = final_balance(balance)
                                    response = f'The ball landed on {chosen_number}, better luck next time!'
                                    await ctx.send(f'{response}\nYour New Balance is: {total_balance}')
                            else:
                                await ctx.send('Woah there! You\'re bidding on a non-existent number! //roulettehelp to view the board!')
                        else:
                            balance = credit_dedux(ctx, credits)
                            if color == 'R':
                                if chosen_number in red_numbers:
                                    chosen_color = 'Red'
                                elif chosen_number in black_numbers:
                                    chosen_color = 'Black'
                                else:
                                    chosen_color = 'Green'

                                if chosen_number in red_numbers:
                                    response = f'The ball landed on {chosen_number} {chosen_color}, Congratulations!'
                                    balance = roulette_x_win(ctx, credits, 2)
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
                                    balance = roulette_x_win(ctx, credits, 14)
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
                                    balance = roulette_x_win(ctx, credits, 2)
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

@bot.command(name='roulettehelp', help='Helps you properly use the roulette command.')
async def rhelp(ctx):
    red_numbers = str("""```diff\n- RED NUMBERS\n``````1 3 5 7 9 12 14 16 18 21 23 25 27 28 30 32 34 36```""")
    stragnt = '00 0'
    green_numbers = str(f"""```css\nGREEN COLORS\n``````css\n{stragnt}```""")
    black_numbers = str("""```BLACK COLORS\n``````2 4 6 8 10 11 13 15 17 19 20 22 24 26 29 31 33 35```""")
    roulette_command = str("""```css\n//roulette "Credits" "Color (R G B N)" "Number Relating to Color"```""")
    await ctx.send(f'To properly use the //roulette command, you must know the board and the format of the command to place your bet.\n\nThe command should go something like this, {roulette_command}\nEach color letter corresponds to a certain color. G = Green, R = Red, B = Black, and N = No Color\nNo color is usually used when you are bidding on a number rather than a color, however it does not matter what you put, just so long that you place in a valid color.\nYou DO NOT need to place something in the number slot. The only slots that require input is the Credits, and Color.\nIf you place a bet in the number, it will place your outcome very high but chances of you winning are very low, so keep that in mind.\n\nIf you need access to the roulette board, you can always type, //roulettehelp,\nHere\'s the board for reference.\n{red_numbers} {green_numbers} {black_numbers}')
    gain_credits(ctx)

def gain_credits(ctx):
    final_information = {}
    global_balance = 0
    with open('casino_currency.csv', 'r+') as gan:
        un = ctx.author.name
        # Saves the file into a list
        base_string = ''
        name_file = []
        grab_money = {}
        for i in gan:
            new_list = i.strip()
            if new_list != '':
                name_file.append(new_list)
        # Makes a list so that you can access your balance in the future
        for i in name_file:
            naim = i.split(',')
            grab_money[naim[0]] = naim[1]
        # Adds you to the file if you are not currently on it and gives a base balance of 1000 Credits
        if un in grab_money:
            rand_amt = random.randint(10, 25)
            jackpot_bonus = random.randint(1, 100)
            if jackpot_bonus == 2:
                rand_amt = random.randint(5000, 25000)

            currency = int(grab_money[un])
            final_balance = currency + rand_amt
            grab_money[un] = final_balance

            stronk = ''
            stronk += str(un)
            stronk += ','
            stronk += f'{final_balance}'

        final_information = grab_money
        global_balance = final_balance
    os.remove('casino_currency.csv')

    with open('casino_currency.csv', 'w+') as genius:
        dos = writer(genius)
        temp_list = []
        temp_values = []
        prog = 0
        for i in list(final_information.values()):
            temp_values.append(i)

        for x in list(final_information.keys()):
            temp_list = []
            temp_list.append(x)
            temp_list.append(temp_values[prog])
            prog += 1
            dos.writerow(temp_list)

    return global_balance

@bot.command(name='daily', help='Use this to claim your daily reward!')
async def daily(ctx):
    global daily_hour
    global daily_minute
    global daily_second
    current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    current_date = datetime.datetime.strptime(current_date, '%Y-%m-%d %H:%M:%S')
    create = daily_user_claim(ctx, current_date, 'daily_user_claim.csv', 1, 'daily')
    if create == True:
        random_creds = random.randint(125, 175)
        balance = roulette_x_win(ctx, random_creds, 2)
        future_date = current_date + datetime.timedelta(days=1)
        await ctx.send('Daily reward claimed!')
    elif create == False:
        if daily_hour == 0:
            if daily_minute == 0:
                await ctx.send(f'You need to wait {daily_second} seconds to claim your daily!')
            else:
                await ctx.send(f'You need to wait {daily_minute} Minutes, and {daily_second} seconds to claim your daily!')
        else:
            await ctx.send(f'You need to wait {daily_hour} Hours, {daily_minute} Minutes, and {daily_second} seconds to claim your daily!')

@bot.command(name='weekly', help='Use this to claim your weekly reward!')
async def daily(ctx):
    global daily_hour
    global daily_minute
    global daily_second
    global daily_days
    current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    current_date = datetime.datetime.strptime(current_date, '%Y-%m-%d %H:%M:%S')
    create = daily_user_claim(ctx, current_date, 'weekly_user_claim.csv', 7, 'weekly')
    if create == True:
        random_creds = random.randint(500, 1250)
        balance = roulette_x_win(ctx, random_creds, 2)
        future_date = current_date + datetime.timedelta(days=7)
        await ctx.send('Weekly reward claimed!')
    elif create == False:
        if daily_days != 0:
            await ctx.send(f'You need to wait {daily_days}, {daily_hour} Hours, {daily_minute} Minutes, and {daily_second} seconds to claim your Weekly!')
        else:
            if daily_hour == 0:
                if daily_minute == 0:
                    await ctx.send(f'You need to wait {daily_second} seconds to claim your weekly!')
                else:
                    await ctx.send(f'You need to wait {daily_minute} Minutes, and {daily_second} seconds to claim your weekly!')
            else:
                await ctx.send(f'You need to wait {daily_hour} Hours, {daily_minute} Minutes, and {daily_second} seconds to claim your Weekly!')
    daily_days = 0

@bot.command(name='monthly', help='Use this to claim your monthly reward!')
async def daily(ctx):
    global daily_hour
    global daily_minute
    global daily_second
    global daily_days
    current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    current_date = datetime.datetime.strptime(current_date, '%Y-%m-%d %H:%M:%S')
    create = daily_user_claim(ctx, current_date, 'monthly_user_claim.csv', 31, 'monthly')
    if create == True:
        random_creds = random.randint(5000, 6250)
        balance = roulette_x_win(ctx, random_creds, 2)
        future_date = current_date + datetime.timedelta(days=31)
        await ctx.send('Monthly reward claimed!')
    elif create == False:
        if daily_days != 0:
            await ctx.send(f'You need to wait {daily_days}, {daily_hour} Hours, {daily_minute} Minutes, and {daily_second} seconds to claim your Monthly!')
        else:
            if daily_hour == 0:
                if daily_minute == 0:
                    await ctx.send(f'You need to wait {daily_second} seconds to claim your Monthly!')
                else:
                    await ctx.send(f'You need to wait {daily_minute} Minutes, and {daily_second} seconds to claim your Monthly!')
            else:
                await ctx.send(f'You need to wait {daily_hour} Hours, {daily_minute} Minutes, and {daily_second} seconds to claim your Monthly!')
    daily_days = 0

def daily_user_claim(ctx, current_time, file_name, day_time, claim):
    new_list = []
    info_list = []
    check = False
    username = ctx.author.name
    global daily_hour
    global daily_minute
    global daily_second
    global daily_days
    with open(file_name, 'r+') as file:
        flub = writer(file)
        for i in file:
            new_i = i.strip()
            new_i = new_i.split(',')
            if new_i != ['']:
                new_list.append(new_i[0])
                info_list.append(new_i)
        if username not in new_list:
            placeholder_list = []
            placeholder_list.append(username)
            placeholder_list.append(current_time)
            flub.writerow(placeholder_list)
            return True
        else:
            for i in info_list:
                if username == i[0]:
                    users_time = datetime.datetime.strptime(i[1], '%Y-%m-%d %H:%M:%S')
                    future_date = users_time + datetime.timedelta(days=day_time)
                    if current_time <= future_date:
                        time_waited = current_time - users_time
                        day_1 = future_date - users_time
                        wait_this_long = day_1 - time_waited
                        wait_this_long = str(wait_this_long)
                        test_days = wait_this_long.split(',')
                        if 'day' in test_days[0]:
                            fixed_time = test_days[1].strip(' ')
                            final_time = datetime.datetime.strptime(fixed_time, '%H:%M:%S')
                            daily_days = test_days[0]
                        else:
                            final_time = datetime.datetime.strptime(wait_this_long, '%H:%M:%S')
                        daily_hour = final_time.hour
                        daily_minute = final_time.minute
                        daily_second = final_time.second
                        return False
                    else:
                        check = True

    if check:
        os.remove(file_name)
        with open(file_name, 'w+') as file:
            writer_object = writer(file)
            for i in info_list:
                if username == i[0]:
                    placeheld_list = []
                    placeheld_list.append(username)
                    placeheld_list.append(current_time)
                    writer_object.writerow(placeheld_list)
                else:
                    writer_object.writerow(i)
        return True

def display_current_balance(ctx):
    with open('casino_currency.csv', 'rt') as file:
        username = ctx.author.name
        for i in file:
            if username in i:
                new_i = i.strip()
                new_i = new_i.split(',')
                return new_i[1]

def credit_dedux(ctx, credits):
    final_information = {}
    global_balance = 0
    with open('casino_currency.csv', 'r+') as gan:
        un = ctx.author.name
        # Saves the file into a list
        base_string = ''
        name_file = []
        grab_money = {}
        for i in gan:
            new_list = i.strip()
            if new_list != '':
                name_file.append(new_list)
        # Makes a list so that you can access your balance in the future
        for i in name_file:
            naim = i.split(',')
            grab_money[naim[0]] = naim[1]

        # Adds you to the file if you are not currently on it and gives a base balance of 1000 Credits
        if un in grab_money:
            currency = int(grab_money[un])
            final_balance = currency - credits
            grab_money[un] = final_balance

            stronk = ''
            stronk += str(un)
            stronk += ','
            stronk += f'{final_balance}'
        final_information = grab_money
        global_balance = final_balance
    os.remove('casino_currency.csv')

    with open('casino_currency.csv', 'w+') as genius:
        dos = writer(genius)
        temp_list = []
        temp_values = []
        prog = 0
        for i in list(final_information.values()):
            temp_values.append(i)

        for x in list(final_information.keys()):
            temp_list = []
            temp_list.append(x)
            temp_list.append(temp_values[prog])
            prog += 1
            dos.writerow(temp_list)

    return global_balance

def final_balance(end_balance):
    final_balance = f"{end_balance} mChips"
    return final_balance

def roulette_x_win(ctx, credits, multiplier):
    final_information = {}
    global_balance = 0
    with open('casino_currency.csv', 'r+') as gan:
        un = ctx.author.name
        # Saves the file into a list
        base_string = ''
        name_file = []
        grab_money = {}
        for i in gan:
            new_list = i.strip()
            if new_list != '':
                name_file.append(new_list)

        # Makes a list so that you can access your balance in the future
        for i in name_file:
            naim = i.split(',')
            grab_money[naim[0]] = naim[1]

        # Adds you to the file if you are not currently on it and gives a base balance of 1000 Credits
        if un in grab_money:
            currency = int(grab_money[un])
            winnings = int(credits) * multiplier
            final_balance = currency + winnings
            grab_money[un] = final_balance

            stronk = ''
            stronk += str(un)
            stronk += ','
            stronk += f'{final_balance}'

        final_information = grab_money
        global_balance = final_balance
    os.remove('casino_currency.csv')

    with open('casino_currency.csv', 'w+') as genius:
        dos = writer(genius)
        temp_list = []
        temp_values = []
        prog = 0
        for i in list(final_information.values()):
            temp_values.append(i)

        for x in list(final_information.keys()):
            temp_list = []
            temp_list.append(x)
            temp_list.append(temp_values[prog])
            prog += 1
            dos.writerow(temp_list)

    return global_balance

def check_bal(ctx, credits):
    with open('casino_currency.csv', 'r+') as gan:
        un = ctx.author.name
        # Saves the file into a list
        base_string = ''
        name_file = []
        grab_money = {}
        for i in gan:
            new_list = i.strip()
            if new_list != '':
                name_file.append(new_list)
        # Makes a list so that you can access your balance in the future
        for i in name_file:
            naim = i.split(',')
            grab_money[naim[0]] = naim[1]

        # Adds you to the file if you are not currently on it and gives a base balance of 1000 Credits
        if un in grab_money:
            currency = int(grab_money[un])
            if int(credits) > currency:
                positive = False
            else:
                positive = True

    return positive

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

@bot.command(name='cointoss', help='Makes a coin toss')
async def toss(ctx, bid=None, call='nocall'):
    dice_away = False
    no_call = False
    if bid == None:
        coinflip = ['Heads', 'Tails']
        coin = random.choice(coinflip)
        await ctx.send(f'The coin landed on {coin}!')
        no_call = True
    elif (str(call.lower()) == 'heads') or (call.lower() == 'tails'):
        dice_away = True
    if dice_away:
            thingy = check_bal(ctx, bid)
            if thingy:
                coinflip = ['Heads', 'Tails']
                coin = random.choice(coinflip)
                balance = credit_dedux(ctx, int(bid))
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

@bot.command(name='give', help='Owner can give credits this way!')
@commands.has_role("Owner") # This must be exactly the name of the appropriate role
async def give_creds(ctx, credits):
    roulette_x_win(ctx, credits, 1)
    balance = display_current_balance(ctx)
    embed=discord.Embed(title = f'{ctx.author.name.capitalize()}\'s Balance', description=f'Your new balance is {balance}', color=0xF4513B)
    await ctx.send(embed=embed)

@bot.command(name='take', help='Owner can take credits away this way!')
@commands.has_role("Owner") # This must be exactly the name of the appropriate role
async def give_creds(ctx, credits):
    roulette_x_win(ctx, credits, -1)
    balance = display_current_balance(ctx)
    embed=discord.Embed(title = f'{ctx.author.name.capitalize()}\'s Balance', description=f'Your new balance is {balance}', color=0xF4513B)
    await ctx.send(embed=embed)



# FIX OASIS COMMAND, TEMPORTARILY DISABLED

@bot.command(name='oasis', help='//oasishelp for more help')
async def oasis(ctx):
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

@bot.command(name='slots', help='It\'s a slot machine...')
async def slot_machine(ctx, credits=None):
    credits = int(credits)
    if credits == None:
        await ctx.send('Please specify an amount of credits!')
    
    else:
        check_balance = check_bal(ctx, credits)
        if check_balance:
            credit_dedux(ctx, credits)
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
                roulette_x_win(ctx, win_value, 1)
            else:
                delimiter = '-'
                win_value = credits

            await ctx.send(f'{slots} < | {delimiter} {win_value:.0f}')

        else:
            await ctx.send('You need more money to make that bid!')

@bot.command(name='placeholder', help='This is just a placeholder command for me to brainstorm new ideas')
async def brainstorm(ctx):
    await ctx.send(f'You don\'t get to see my ideas because they\'re commented out >:D')
    # Monopoly?????? (Its own bot)
    # Checkers 
    # Uno? // Problems with personal hands and spamming DM's // Maybe find a workaround?
    # Oasis Poker // Also known as the LUIGI POKER GAME FROM MY MARIO DS THINGY, yeah that game
    # Coin Toss against other people
    # Have a shop command that allows you to gain access to ranks and other things.

@bot.command(name='testEmbeds', help='E')
async def embed(ctx):
    await ctx.send('This is a command to help me with embeds. Everything is commented out, so you are seeing this response.')
    # embed=discord.Embed(title="Sample Embed", url="https://realdrewdata.medium.com/", description="This is an embed that will show how to build an embed and the different components", color=0xFF5733)
    # await ctx.send(embed=embed)

@bot.command(name='shop', help='Displays commands and prices for items to purchase')
async def shop(ctx):
    await ctx.send('This command is currently under development. Please be patient as it is being worked on.')

'''
@bot.event
async def on_message(message):
    if not message.content.startswith("-"):
        if message.author != bot.user:
            ctx = message.author.name
            if message.content.startswith('69'):
                channel = message.channel
                await channel.send('nice')

            elif message.content.startswith('bet'):
                channel = message.channel
                await channel.send('bet')

            elif message.content.startswith('<:POGGERS:798741856337920030>'):
                channel = message.channel
                await channel.send('<:POGGERS:798741856337920030>')

            elif message.content.startswith('e'):
                channel = message.channel
                await channel.send('e')
'''
bot.run(TOKEN)