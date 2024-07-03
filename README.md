# pyRogue
> ## **pyRogue** is a **educational** project. 
<img src="https://img.shields.io/badge/Make_sure_to_mark_with_a-Star-yellow"> <a href="https://discord.gg/9ZsnGDmGk2"><img src="https://img.shields.io/badge/Join_our_News-Discord-blue
"></a>

[Based on the Source Code of pokerogue.net](https://github.com/pagefaultgames/pokerogue)
> In compliance with Pokerogue's License this project here is also released under AGPL3.

![Preview Image](.github/previews/main.png)
![Preview Image](.github/previews/tool.png)

# List of content
- [Important Foreword](https://github.com/RogueEdit/onlineRogueEditor?tab=readme-ov-file#important-foreword)
- [FAQ](https://github.com/RogueEdit/onlineRogueEditor?tab=readme-ov-file#faq)
- [How to run from code](https://github.com/RogueEdit/onlineRogueEditor?tab=readme-ov-file#how-to-run-from-code)
- [License](https://github.com/RogueEdit/onlineRogueEditor?tab=readme-ov-file#license)
- [Features](https://github.com/RogueEdit/onlineRogueEditor?tab=readme-ov-file#editor-features)
- [Regarding Bans and Limited Accounts](https://github.com/RogueEdit/onlineRogueEditor?tab=readme-ov-file#regarding-bans-and-limited-accounts) !! IMPORTANT !!

## Important foreword

We learned enough about freezing python to binarys so from here on out it will be source code only.

We will not sent you any files or contact you about anything. You can see who contributed and everything regarding us will be only done on GitHub. We will not contact you in any matter or will send you files. There are scammers out there. Here you can read the full source code, compile it from scratch and such or download a VT-checked official release.

Attention: When ever this tool detects you are trying to manipulate a daily seeded run it will abort. We only do this for educating us and provide the source code opensource in compliance with PokeRogue's License.

- We take no responsibility for your actions when using this tool.  Whenever you startup tho a backup is created and stand: 03.07.2024 - they are applicable no matter created when.

## FAQ

- How do i revert my changes?
  - The programm will always create backups everytime you login! When you load the first time it will create a `base_gameData(trainerID)_03.07.2024_18.03.22.json` unique based on your trainerID coupled with a timestamp. This applies for slot' data aswell; `backup_slotData(slotNumber_trainerID)_03.07.2024_18.03.22.json`. All subsequent backups will be prefixed with `backup_` and you can restore to any file back in time.

  ![Preview Image](.github/previews/backup.png)

- Will this get me banned?
  - See [Regarding Bans and Limited Accounts](https://github.com/RogueEdit/onlineRogueEditor?tab=readme-ov-file#regarding-bans-and-limited-accounts)

- Where can i donate?
  - We will not accept any money or any form of payment. If you want to help then only by contributing. We do it for education only, any critique welcome.

## How to run from code
- Install python
- Download the source code
- Extract the source code
- Open a terminal, navigate into your `[extracted_folder]/src/`
- Install all the requirements using python according to setup
  - `python3 -m pip install -r requirements.txt`
- Now you should be able to run main.py
  - `python3 main.py`


## License

- See license document and credit headers. 
 
## Editor Features
- Extensive logging for easy debug in a log file
---
- Autocomplete recomendations

![Preview Image](.github/previews/autocomplete.png)

---

- Checks for updates (new Commits to this repo) on startup

![Preview Image](.github/previews/updateChecker.png)

---
- Four login methods, three for online, one for offline

![Preview Image](.github/previews/loginMethods.png)

---
- When logging in it will automatically create backups for you.
  - You can restore backups easily see preview above
---
- Change selected slot
  - This will fetch the chosen new slot_x.json containing your session save data
---
- Edit a starter - This will ask you to take any input:

![Preview Image](.github/previews/editStarter.png)

---
- Unlock all starters | same as above but for all pokemons
  - This will unlock every single Pokemon depending on your choosings like above
---
- Modify the number of egg-tickets you have
  - This allows you to set the amount of egg gacha tickets you have of every tier
---
- Edit a pokemon in your party
  - Let's you edit g-max, fusions, moves, species, level, luck, fusion etc...

![grafik](.github/previews/editParty.png)

---
- Item Editor

![Preview Image](.github/previews/itemEditor.png)

---
- Unlock all game modes
  - Unlocks: classic, endless, spliced endless
- Add one or unlock all
  - Vouchers
  - Achievements

![Preview Image](.github/previews/editAchievementsMin.png)

---
- Edit candies on a pokemon
- Edit amount of money
- Edit pokeballs amount
- Edit biome
---
- Generate eggs
  - Depending on your liking, whatever rarity - gacha type and such
- Set your eggs to hatch
- Edit account stats
  - Randomize all
  - Set specific ones
  - Set all in a loop
---
- Unlock everything
  - Just calls mulitiple features from above
  - Will also edit account stats with "legit" constraints. Based on your seen variables and such and randomized between reasonable values.
---
- Display all Pokemon with their names and id
- Display all Biomes IDs
- Display all Moves IDs
- Display all Voucher IDs
- Display all Natures
- Display all Nature Slot IDs
- Save data to server via open accesible API calls



## Regarding Bans and Limited Accounts
https://www.reddit.com/r/pokerogue/comments/1d8hncf/cheats_and_exploits_post_followup_bannable/

https://www.reddit.com/r/pokerogue/comments/1d8ldlw/a_cheating_and_account_deletionwipe_followup/

<meta name="keywords" content="pokerogue, pokerogue save editor, pokerogue, rogueEditor, free, gacha, ticket, tickets, egg, eggs, shiny, save, edit, pokemon, unlimited, hack, hacks, cheat, cheats, trainer, table, pokedex, dex, wave, money, level, levels, iv, ivs, stat, stats, item, items, api, mod, mods, tool, tools, education, python">
