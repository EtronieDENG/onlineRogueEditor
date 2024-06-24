# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/claudiunderthehood https://github.com/JulianStiebler/
# Date of release: 13.06.2024
# Last Edited: 20.06.2024


"""
This script facilitates user login and session initialization for PokeRogue. It offers a menu-driven interface to 
perform various account and game data actions after a successful login using either requests or Selenium.

Features:
- User login through requests or Selenium.
- Various account and game data actions through a menu-driven interface.
- Custom logging and colored console output.

Modules:
- getpass: For securely obtaining the password from the user.
- requests: For handling HTTP sessions and requests.
- brotli: (Imported but not directly used in this script).
- loginLogic: Custom module for handling login logic using requests.
- Rogue: Custom module for initializing and interacting with the PokeRogue session.
- SeleniumLogic: Custom module for handling login using Selenium.
- cFormatter: Custom formatter for colored printing and logging.
- Color: Enumeration defining color codes for cFormatter.
- CustomLogger: Custom logging functionality.
- config: Custom module for configuration and update checking.
- datetime, timedelta: For date and time operations.
- colorama: For terminal text color formatting.
"""

import getpass
# Securely obtains the password from the user without echoing.

import requests
# Handles HTTP sessions and requests for logging in and maintaining session state.

import brotli  # noqa: F401
# Provides Brotli compression. Not directly used in this script but might be a dependency for other modules.

from modules import requestsLogic, Rogue,  SeleniumLogic, config
# requestLogic: Handles the login logic using requests.
# Rogue: Initializes and interacts with the PokeRogue session.
# SeleniumLogic: Handles login logic using Selenium for browser-based interactions.
# Config: Provides configuration settings and update checking functionality.

from colorama import Fore, Style, init
# Fore, Style: Used for terminal text color formatting.
# init: Initializes colorama for colored console output.

from utilities import cFormatter, Color, CustomLogger
# cFormatter: Custom formatter for colored printing and logging.
# Color: Enumeration defining color codes for cFormatter.
# Custom Logger: Provides custom logging functionality for the script.


from datetime import datetime, timedelta
# datetime, timedelta: For date and time operations, particularly for update checking.

init()
config.f_initFolders()
logger = CustomLogger()
config.f_checkForUpdates(requests, datetime, timedelta, Style)
config.f_printWelcomeText()

def main():
    while True:
        # Try loginChoice
        try:
            loginChoice = input('Please choose a method of logging in: ')
            loginChoice = int(loginChoice)  # Attempt to convert input to integer
            
            if loginChoice not in [1, 2, 3]:
                cFormatter.print(Color.DEBUG, 'Please choose a valid option.')
                continue  # Prompt user again if choice is not valid
        except KeyboardInterrupt:
            cFormatter.print(Color.DEBUG, '\nProgram interrupted by user.')
            exit()
        except ValueError:
            cFormatter.print(Color.DEBUG, 'Invalid input. Please enter a number.')
            continue  # Prompt user again for input

        # Try login
        try:
            username = input('Username: ')
            password = getpass.getpass('Password (password is hidden): ')

            session = requests.Session()
            # When using requests
            if loginChoice == 1:
                login = requestsLogic(username, password)
                try:
                    if login.login():
                        cFormatter.print(Color.INFO, f'Logged in as: {config.f_anonymizeName(username)}')
                        session.cookies.set('pokerogue_sessionId', login.session_id, domain='pokerogue.net')
                        rogue = Rogue(session, login.token, login.session_id)
                        break
                except Exception as e:
                    cFormatter.print(Color.CRITICAL, f'Something went wrong. {e}', isLogging=True)

            # When using browser
            elif loginChoice in [2, 3]:
                try:
                    if loginChoice == 3:
                        cFormatter.print(Color.INFO, 'Do not close your browser and do not browse in the game!')
                        cFormatter.print(Color.INFO, 'Do not close your browser and do not browse in the game!')
                        cFormatter.print(Color.INFO, 'Do not close your browser and do not browse in the game!')
                    selenium_logic = SeleniumLogic(username, password, 120, useScripts=(loginChoice == 3))
                    session_id, token, driver = selenium_logic.logic()

                    if session_id and token and driver:
                        cFormatter.print(Color.INFO, f'Logged in as: {username.capitalize()}')
                        session.cookies.set('pokerogue_sessionId', session_id, domain='pokerogue.net')
                        rogue = Rogue(session, auth_token=token, clientSessionId=session_id, driver=driver, useScripts=(loginChoice == 3))
                        break
                    else:
                        cFormatter.print(Color.CRITICAL, 'Failed to retrieve necessary authentication data from Selenium.')
                except Exception as e:
                    cFormatter.print(Color.CRITICAL, f'Something went wrong. {e}', isLogging=True)

            else:
                cFormatter.print(Color.CRITICAL, 'Invalid choice. Please choose a valid method.')
        except KeyboardInterrupt:
            cFormatter.print(Color.DEBUG, '\nProgram interrupted by user.')
            exit()

    # Define menu variables and our menu
    useWhenDone = f'{Fore.LIGHTYELLOW_EX}(Use when Done)'
    title = f'{config.title}>'

    # See cFormatter.initialize_menu() for more information
    term = [
        (title, 'title'),
        ('Account Actions', 'category'),
        (('Create a backup', ''), rogue.create_backup),
        (('Recover your backup', ''), rogue.restore_backup),
        (('Load Game-Data from server', ''), rogue.get_trainer_data),
        (('Change save-slot to edit', ''), rogue.f_changeSaveSlot),
        (('Edit account stats', ''), rogue.f_editAccountStats),

        ('Trainer Data Actions', 'category'),
        (('Edit a starter', ''), rogue.edit_starter_separate),
        (('Edit your egg-tickets', ''), rogue.add_ticket),
        (('Edit candies on a starter', ''), rogue.f_addCandies),
        (('Edit Egg-hatch durations', ''), rogue.f_editHatchWaves),
        (('Generate eggs', ''), rogue.f_addEggsGenerator),
        (('Unlock all vouchers', ''), rogue.f_editVouchers),
        (('Unlock all starters', ''), rogue.f_unlockStarters),
        (('Unlock all achievements', ''), rogue.f_editAchivements),
        (('Unlock all gamemodes', ''), rogue.f_editGamemodes),
        (('Unlock Everything', ''), rogue.f_unlockAllCombined),

        ('Session Data Actions', 'category'),
        (('Edit CURRENT Pokemon Party', ''), rogue.edit_pokemon_party),
        (('Edit money amount', ''), rogue.f_editMoney),
        (('Edit pokeballs amount', ''), rogue.f_editPokeballs),
        (('Edit current biome', ''), rogue.f_editBiome),
        (('Edit Items', f'{Fore.GREEN + Style.BRIGHT}NEW{Style.RESET_ALL}'), rogue.f_submenuItemEditor),

        ('Print game information', 'category'),
        (('Show all Pokemon ID', ''), rogue.print_pokedex),
        (('Show all Biome IDs', ''), rogue.print_biomes),
        (('Show all Move IDs', ''), rogue.print_moves),
        (('Show all Vouchers IDs', ''), rogue.print_vouchers),
        (('Show all Natures IDs', ''), rogue.print_natures),
        (('Show all NaturesSlot IDs', ''), rogue.print_natureSlot),

        ('You can always edit your JSON manually as well!', 'helper'),
        (('Save data and upload to the Server', useWhenDone), rogue.update_all),
        (('Print help and program information', ''), config.f_printHelp),
        (('Logout', ''), rogue.logout),
        (title, 'title'),
    ]

    try:

        while True:
            valid_choices = cFormatter.initialize_menu(term)
            user_input = input('Command: ').strip().lower()

            if user_input == 'exit':
                raise KeyboardInterrupt
            
            if user_input.isdigit():
                choice_index = int(user_input)
                for idx, func in valid_choices:
                    if idx == choice_index:
                        func()
                        break
                    elif idx == 'exit':
                        raise KeyboardInterrupt
                else:
                    cFormatter.print(Color.INFO, 'Invalid selection. Please choose a valid menu option.')
            else:
                cFormatter.print(Color.INFO, 'Invalid input. Please enter a number.')

    except KeyboardInterrupt:
        cFormatter.print(Color.DEBUG, '\nProgram interrupted by user.')
        exit()
if __name__ == '__main__':
    main()
