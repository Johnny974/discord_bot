# Kozák Discord Bot

A multifunctional Discord bot built with [discord.py](https://discordpy.readthedocs.io/), featuring jokes, polls, slot machine-style fruit game, NASA Astronomy Picture of the Day, and more.  

## Features

- 👋 Greets new members via DM  
- 🤣 Fetches random dad jokes (manual or daily at 20:00)  
- 🗳️ Creates interactive polls with up to 5 options  
- 🎰 "Ovocko" fruit slot machine game with a highscore system  
- 🌌 Shows NASA Astronomy Picture of the Day (APOD)  
- 🤖 Custom responses when someone mentions "kozák"  

## Commands

| Command | Description |
|---------|-------------|
| `/vtip` | Sends a random dad joke |
| `/setvtipkanal #channel` | (Admin only) Sets the channel for daily jokes at 20:00 |
| `/anketa question-option1-option2-...` | Creates a poll (max 5 options) |
| `/ovocko` | Plays the fruit slot machine game |
| `/ovocko_highscore` | Shows the highest score on the server |
| `/nasa` | Shows NASA’s Astronomy Picture of the Day |
| `/commands` | Displays the list of available commands |

## Deployment
I deployed the code on [Railway](https://railway.com/), so that the bot is up and running 24/7 on cloud servers.

## Future work
In the future, I want to discover many more funny or very cool APIs and this bot will interact with them!