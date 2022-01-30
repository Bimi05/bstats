# Welcome
<a href="https://pypi.org/project/brawlstats/"><img src="https://img.shields.io/pypi/v/bstats"></a>
<a href="https://pypi.org/project/brawlstats/"><img src="https://img.shields.io/pypi/pyversions/bstats"></a>
<a href="https://github.com/Bimi05/bstats/blob/main/LICENSE"><img src="https://img.shields.io/pypi/l/bstats"></a>
<a href="https://pypi.org/project/brawlstats/"><img src="https://img.shields.io/pypi/dm/bstats"></a>

* This wrapper supports both sync and async requests to the Brawl Stars API
* Required Python versions: 3.8 and higher

## Features

* Easy to use with an object oriented design.
* Get a player's profile as well as their 25 most recent battles.
* Get a club's statistics as well as its members and their individual statistics.
* Get the top 200 rankings for players, clubs, or a specific brawler.
* Get information about all currently available brawlers.
* Get the current ongoing event rotation.

## Installation

```sh
# Stable
pip install bstats

# Development
pip install git+https://github.com/Bimi05/bstats
```

## Examples

### Sync

```Python
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

### Async

```Python
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

## Miscellaneous

* Please star this repository if you're satisfied with the wrapper 😊
* Have you come across an issue in the wrapper? No worries! Just create an issue!
* If you need an API key, visit the Brawl Stars API page.

(You must create an account in order to create and use an API key)