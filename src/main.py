# Authors https://github.com/JulianStiebler/
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/claudiunderthehood 
# Date of release: 13.06.2024
# Last Edited: 28.06.2024
# Based on: https://github.com/pagefaultgames/pokerogue/

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

import pwinput
import requests
import brotli  # noqa: F401

from modules import requestsLogic, Rogue, SeleniumLogic, config
from modules.handler import OperationSuccessful, dec_handleOperationExceptions, OperationCancel, OperationSoftCancel
from colorama import Fore, Style, init
from utilities import cFormatter, Color, CustomLogger
from datetime import datetime, timedelta
from utilities import fh_printMessageBuffer
from sys import exit
init()
logger = CustomLogger()

if not config.debug:
    config.f_checkForUpdates(requests, datetime, timedelta, Style)


@dec_handleOperationExceptions
def m_executeOptions(choice_index, valid_choices):
    for idx, func in valid_choices:
        if idx == choice_index:
            func()
            break
        elif idx == 'exit':
            raise KeyboardInterrupt

@dec_handleOperationExceptions
def m_mainMenu(rogue, editOffline: bool = False):
    title = f'{config.title}>'
    useWhenDone = f'{Fore.LIGHTYELLOW_EX}(Use when Done)'
    reworked = f'{Fore.GREEN}(REWORKED)'

    term = [
        (title, 'title'),
        ('账号相关', 'category'),
        ((f'{Fore.YELLOW}创建备份', reworked), rogue.f_createBackup),
        ((f'{Fore.YELLOW}从备份中恢复', reworked), rogue.f_restoreBackup),
        (('加载服务器的数据', reworked), rogue.f_getGameData),
        # (('修改存档位', reworked), rogue.f_changeSaveSlot),
        # (('修改帐号状态', reworked), rogue.f_editAccountStats),

        ('修改', 'category'),
        ((f'{Fore.YELLOW}无中生有蛋蛋们', reworked), rogue.f_addEggsGenerator),
        ((f'改 {Fore.YELLOW}生蛋回合数', reworked), rogue.f_editHatchWaves),
        ((f'改 {Fore.YELLOW}扭蛋券', reworked), rogue.f_addTicket),
        ((f'改 {Fore.YELLOW}宝可梦', reworked), rogue.f_editStarter),
        ((f'改 {Fore.YELLOW}糖果{Style.RESET_ALL}', reworked), rogue.f_addCandies),

        ('解锁', 'category'),
        ((f'解锁 {Fore.YELLOW} 成就', reworked), rogue.f_unlockAchievements),
        ((f'解锁 {Fore.YELLOW} 挑战', reworked), rogue.f_unlockVouchers),
        ((f'解锁 {Fore.YELLOW} 全图鉴', reworked), rogue.f_unlockStarters),
        ((f'解锁 {Fore.YELLOW} 全模式', reworked), rogue.f_unlockGamemodes),
        ((f'解锁 {Fore.YELLOW} 全部', reworked), rogue.f_unlockAllCombined),

        ('修改存档', 'category'),
        ((f'改 {Fore.YELLOW}队伍', reworked), rogue.f_editParty),
        ((f'改 {Fore.YELLOW}钱', reworked), rogue.f_editMoney),
        ((f'改 {Fore.YELLOW}球', reworked), rogue.f_editPokeballs),
        ((f'改 {Fore.YELLOW}当前地图', reworked), rogue.f_editBiome),
        ((f'改 {Fore.YELLOW}道具', reworked), rogue.f_submenuItemEditor),

        ((f'{Fore.YELLOW}保存并更新至线上', useWhenDone), rogue.f_updateAllToServer),
        (('登出', ''), rogue.f_logout),
        (title, 'title')
    ]
    if editOffline or config.debug:
        # Filter entrys that would break offline
        term = [entry for entry in term if entry[1] != rogue.f_updateAllToServer]
        term = [entry for entry in term if entry[1] != rogue.f_getGameData]
        term = [entry for entry in term if entry[1] != rogue.f_logout]
        replaceEntry = ('离线修改器已加载', 'helper')
        term = [replaceEntry if entry == ('你也可以直接改json文件！', 'helper') else entry for entry in term]

    try:
        while True:
            validChoices = cFormatter.m_initializeMenu(term)
            fh_printMessageBuffer()
            userInput = input('Command: ').strip().lower()

            if userInput == 'exit':
                raise KeyboardInterrupt
            if userInput == 'lb':
                rogue.f_lb()

            if userInput.isdigit() and int(userInput) <= len(validChoices):
                choiceIndex = int(userInput)
                m_executeOptions(choiceIndex, validChoices)

    except OperationSuccessful as os:
        cFormatter.print(Color.DEBUG, f'Operation successful: {os}')
    except KeyboardInterrupt:
        cFormatter.print(Color.DEBUG, '\n程序已被用户终止.')
        exit()

@dec_handleOperationExceptions
def main():
    if config.debug:
        rogue = Rogue(requests.session(), 'Invalid Auth Token', config.debug)
        m_mainMenu(rogue)
    else:
        while True:
            try:
                config.f_printWelcomeText()
                loginChoice = int(input('在线还是离线？1:在线，2：离线 '))
                if loginChoice == 1:
                    username = input('用户名 ')
                    password = pwinput.pwinput(prompt='密码: ', mask='*')

                    session = requests.Session()
                    
                    login = requestsLogic(username, password)
                    try:
                        if login.login():
                            cFormatter.print(Color.INFO, f'登陆成功: {username}')
                            session.cookies.set('pokerogue_sessionId', login.sessionId, domain='pokerogue.net')
                            rogue = Rogue(session, login.token, login.sessionId)
                            break
                    except Exception as e:
                        cFormatter.print(Color.CRITICAL, f'Something went wrong. {e}', isLogging=True)
                
                elif loginChoice == 2:
                    rogue = Rogue(session, authToken='Invalid Auth Token', editOffline=True)
                    break
            except KeyboardInterrupt:
                exit()
        if loginChoice != 2:
            del username, password
        m_mainMenu(rogue, editOffline=(loginChoice == 2))

if __name__ == '__main__':
    while True:
        try:
            main()
        except OperationSuccessful as os:
            cFormatter.print(Color.DEBUG, f'操作成功: {os}')
        except KeyboardInterrupt:
            cFormatter.print(Color.DEBUG, '\n程序已被用户终止.')
            exit()
        except OperationCancel:
            cFormatter.print(Color.DEBUG, '\n程序已被用户终止.')
            exit()
        except OperationSoftCancel:
            cFormatter.print(Color.DEBUG, '\n程序已被用户终止.')
            exit()

    
