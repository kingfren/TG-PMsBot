<h1 align="center">Telegram PM-Bot</h1>
<p align="center">
    <a herf="https://github.com/libgnu/TG-PMsBot">
        <img src="https://graph.org/file/5b08963ece50cfdbe7a2a.jpg" alt="Bot Logo">
    </a>
</p>

This Bot can forward Messages between the Owner and other Users of Bot.

##  Functions of this Bot:
```
• It can Forward Messages or any Media file.
• It Can be Used to hold Giveaways.
• It acts as a Feedback Bot.
• It can be Used for Announcement with Broadcast feature.
• It can be used to chat with Spam-Reported guys as well.
• Owner can Block/Unblock any User(s).
• Owner can Broadcast Message to all Users.
```
---

## Deployment

#### This Bot can be Deployed easily using Dockerfile.

### Compulsory Variables
`API_ID` : Get it from [my.telegram.org](https://my.telegram.org).

`API_HASH` : Get it from [my.telegram.org](https://my.telegram.org).

`BOT_TOKEN` : Get the bot token from [@BotFather](https://telegram.dog/BotFather).

`OWNER_ID` : Your Telegram User ID. Get it from [@MissRose_Bot](https://telegram.dog/MissRose_Bot).

`REDIS_URI` : Your Redis Endpoint URI, Get it from [redislabs.com](https://redislabs.com).

`REDIS_PASSWORD` : Your Redis Endpoint Password, Get it from [redislabs.com](https://redislabs.com).

### Optional Vars
`FORCE_SUBSCRIBE` : Your Channel/Group id or username. If you don't Want this, Keep this Empty.

`TZ` : Your TimeZone; Default is Asia/Kolkata.

### Deploying on Heroku
[![Deploy To Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/libgnu/TG-PMsBot)

### Deploying on VPS
```sh
git clone https://github.com/libgnu/TG-PMsBot pmbot
cd pmbot
cp .env.sample .env
nano .env # fill your credentials here
screen -S pmbot
python -m pmbot
```
• PRESS - CTRL + A then CTRL + D to detach from screen.

## Credits and Inspiration
- [TeamYukki](https://github.com/TeamYukki) for [Yukki](https://github.com/TeamYukki/YukkiMusicBot)
- [TeamUltroid](https://github.com/TeamUltroid) for [Ultroid](https://github.com/TeamUltroid/Ultroid)
- [Lonami](https://github.com/LonamiWebs) for [Telethon](https://github.com/LonamiWebs/Telethon)
