# Overview

## NOTICE - THIS PROJECT IS MAPPED AROUND MATHBOT.PY AND NOT MATHBOT2.PY THE SECOND FILE IS CURRENTLY IN THE WORKS FOR THE SAME REASONS OF MATHBOT.PY

This was a project I started a year ago to test my coding skills as a way to learn new things, (*ahem* hence the lack of classes). However, this bot had no database, and the lack of storing information just rubbed me the wrong way.

This is a discord bot API that allows you to gamble with fake currency, and earn prizes based on your good luck.

This was a project formed by me to clean up the project and have a much nicer User Interface and better information storage by me for the user.

This includes having daily, weekly, and monthly credit claims to reward the user with extra points to keep them motivated using the bot.

This project used to have a lack of information storage which I found unacceptable, so I imported a shop system and a levelup system for the user to gain levels as they use the bot and earn money, while also being able to use their hard earned cash towards fun rewards, which in this case as of now is nicknames.

My project can be viewed in the following link below labeled "Software Demo Video."

[Software Demo Video](http://youtube.link.goes.here)

# Cloud Database
I am using mongoDB for my database. It is using a direct link through python code to direct the cluster (aka the database itself) and allow for creating, modifying, and inserting data into the database.

# Development Environment

- MongoDB
- VSCode
- Python 3.9.4
        
        libraries:
            dotenv
            os
            random
            datetime
            csv
            discord - commands // check // get // SlashCommand and Slash Context
            pymongo

# Useful Websites

{Make a list of websites that you found helpful in this project}
* [Tech With Tim // MongoDB In Python](https://www.youtube.com/watch?v=rE_bJl2GAY8)

# Future Work
- More Accessibility with the shop feature and leveling
- Custom names by the user by utilizing inputs
- More friendly UI
- Have benefits to users with higher levels. (I.E. Higher Daily/Weekly Claims the higher the level)