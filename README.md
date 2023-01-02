<h1 align="center">Telegram PM-Bot</h1>

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
This Bot can be Deployed anywhere easily with Dockerfile

### Deploying on Heroku

### Deploying Via Dockerfile
```sh
sudo apt update
sudo apt install -y docker.io
sudo docker build . -t pmbot
sudo docker run -it pmbot --name pmbot
```
Follow the VPS guide after this 

### Deploying on VPS
```sh
git clone https://github.com/LibGnu/TG-PMsBot pmbot
cd pmbot
cp .env.sample .env
nano .env  # fill your credentials here
screen -S pmbot
python -m pmbot
```
PRESS - CTRL + A then CTRL + D to detach from screen.
If you're in Docker Container, Press CTRL + P then CTRL + Q to detach.
