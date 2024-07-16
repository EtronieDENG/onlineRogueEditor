import logging
import getpass
from modules.loginLogic import loginLogic
from modules.rogueClass import Rogue  # Importing the Rogue class

# Configure logging to display debug messages
logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    
    while True:
        print("\n<Login>")
        username = input("Username: ")
        password = getpass.getpass("Password (password is hidden): ")

        login = loginLogic(username, password)

        try:
            if login.login():
                print(f"Logged in as: {username.capitalize()}")
                rogue = Rogue(login.token, login.session_id)
                rogue = Rogue.dump_data()
                break
            else:
                print("Incorrect credentials")
        except Exception as e:
            print("An error occurred during login.")
            logging.exception(e)
            
    func = {
        "1": rogue.update_all,
        "2": rogue.starter_edit,
        "3": rogue.unlock_all_starters,
        "4": rogue.egg_gacha,
        "5": rogue.edit_pokemon_party,
        "6": rogue.unlock_all_achievements,
        "7": rogue.unlock_all_gamemodes,
        "8": rogue.unlock_all_vouchers,
        "9": rogue.add_candies,
        "10": rogue.edit_money,
        "11": rogue.edit_pokeballs,
        "12": rogue.edit_biome,
        "13": rogue.generate_eggs,
        "14": rogue.edit_account_stats,
        "15": rogue.max_account,
        "16": rogue.restore_backup,
        "17": rogue.pokedex,
        "18": rogue.biomes,
        "19": rogue.moves,
    }

    term = [
        "**************************** ONLINE EDITOR ****************************",
        "1: Update all Data on the Server (Working)",
        "2: Edit a starter (Working)",
        "3: Unlock all starters (Working)",
        "4: Edit your egg-tickets (Working)",
        "5: Edit CURRENT Pokemon Party (Working)",
        "6: Unlock all achievements (Working)",
        "7: Unlock all gamemodes (Working)",
        "8: Unlock all vouchers (Working)",
        "9: Add candies to a pokemon (Working)",
        "10: Edit money amount (Working)",
        "11: Edit pokeballs amount (Working)",
        "12: Edit biome (Working)",
        "13: Generate eggs (Working)",
        "14: Edit account stats (Working)",
        "15: Unlock Everything (Working)",
        "--------------------------------------------------------------------",
        "16: Recover your backup (Working)",
        "17: Show all Pokemon ID (Working)",
        "18: Show all Biome IDs (Working)",
        "19: Show all Move IDs (Working)",
        "--------------------------------------------------------------------"
    ]

    while True:
        print("\n".join(term))
        command = input("Command: ")

        if command in func:
            func[command]()
        elif command == "exit":
            quit()
        else:
            print("Command not found")