# Frog of the week discord bot
_Discord bot to choose a random frog and display information about it once every week. Information 
is german as this is based on a german meme._

## installation
There are no PyPI releases. Neither are they planned.

### manual
For installation with pip directly from this GitHub repository simply open a terminal and type
```
pip install git+ssh://git@github.com/rlipperts/python_package_template.git
```

## usage

_To use the bot you have to host it on a server and then add it ot your Discord server._

### setup the bot on with docker

1. Clone the GitHub repository onto your server
   ```
   git clone git@github.com:rlipperts/frog-of-the-week.git
   ```
2. Build the docker image
   ```
   cd frog-of-the-week
   docker build -t frog-of-the-week-discord-bot .
   ```
3. Execute the container
   ```
   docker run -d frog-of-the-week-discord-bot
   ```
