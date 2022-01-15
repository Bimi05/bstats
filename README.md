![Size](https://img.shields.io/github/languages/code-size/Bimi05/bstats)
![Package-Version](https://img.shields.io/pypi/v/bstats)
![Python-Version](https://img.shields.io/pypi/pyversions/bstats)
![License](https://img.shields.io/pypi/l/bstats)
![Downloads](https://img.shields.io/pypi/dm/bstats)

# BStats

- This library has both a sync and an async client
- Python 3.8 or later is required

# Features

- Easy to use module with an object oriented design.
- Get a player's profile.
   - You can also get their 25 most recent battles using the player's tag!
- Get a club's statistics.
   - You are also able to access its members and their individual statistics!
- Get the top 200 rankings for players, clubs, or a specific brawler.
- Get information about all currently available brawlers.
- Get the current ongoing event rotation.

# Installation

Install the latest build:

> `pip install bstats`


# Examples

### Sync example
```py
import bstats

client = bstats.SyncClient("token") # Never post any of your tokens for APIs on a public github!

player = client.get_player("80V2R98CQ")
print(player.trophies)
print(player.solo_victories)

club = player.club
if club:
    print(club.tag)
    members = club.members

    for player in members[:5]: # Get the top 5 club members
       print(player.name, player.trophies) # Show their name and their trophies

# Get the top 5 players in the world
best_players = client.get_leaderboards(mode="players", limit=5)
for player in best_players:
    print(player.name, player.rank) # Show their name and their rank on the leaderboard

# Get the top 5 Meg players in the United Kingdom
top_meg_players = client.get_leaderboards(
    mode="brawlers",
    country="GB",
    limit=5,
    brawler="Meg"
)
for player in top_meg_players:
    print(player.name, player.rank)

# Get a player's 25 most recent battles
battles = client.get_battlelogs("80V2R98CQ")
print(battles[0].mode_name) # Show the last mode the player battled in

rotation = client.get_event_rotation()
for event in rotation:
    print(event.start, event.end)
```

### Async example
```py
import asyncio
import bstats

client = bstats.AsyncClient("token") # Never post any of your tokens for APIs on a public github!

# to use the async client, we'll need an async function
async def main():
    player = await client.get_player("80V2R98CQ")
    print(player.trophies)
    print(player.solo_victories)

    club = player.club
    if club:
       print(club.tag)
       members = club.members

       for player in members[:5]: # Get the top 5 club members
          print(player.name, player.trophies) # Show their name and their trophies

    # Get the top 5 players in the world
    best_players = await client.get_leaderboards(mode="players", limit=5)
    for player in best_players:
       print(player.name, player.rank) # Show their name and their rank on the leaderboard

    # Get the top 5 Meg players in the United Kingdom
    top_meg_players = await client.get_leaderboards(
       mode="brawlers",
       country="GB",
       limit=5,
       brawler="Meg"
    )
    for player in top_meg_players:
       print(player.name, player.rank)

    # Get a player's 25 most recent battles
    battles = await client.get_battlelogs("80V2R98CQ")
    print(battles[0].mode_name) # Show the last mode the player battled in

    rotation = await client.get_event_rotation()
    for event in rotation:
       print(event.start, event.end)

# we now create a loop to send us the data from the async client
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

# Miscellaneous

- Please star this repository if you're satisfied with the wrapper 😊
- Have you come across an issue in the wrapper? No worries! Just [create an issue](https://github.com/Bimi05/bstats/issues)!
- If you need an API key, visit the [Brawl Stars API](https://developer.brawlstars.com/#/) page.
   - You must create an account in order to create and use an API key.
