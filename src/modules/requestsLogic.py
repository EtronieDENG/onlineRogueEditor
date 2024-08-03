# Authors https://github.com/JulianStiebler/
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/claudiunderthehood 
# Date of release: 13.06.2024 
# Last Edited: 28.06.2024

"""
This script provides functionality for handling HTTP requests, including error handling and login logic.

Features:
- Sends HTTP POST requests to a specified login URL.
- Handles various HTTP response status codes and logs corresponding messages.
- Generates random user agent headers for requests.
- Implements rate limiting to prevent excessive requests.

Modules:
- requests: Sends HTTP requests and handles responses.
- random: Generates random integers for implementing rate limiting and adding delays.
- typing: Provides support for type hints.
- time.sleep: Introduces delays between requests to simulate human behavior.
- utilities.limiter.Limiter: Limits the frequency of requests to avoid rate limiting issues.
- utilities.cFormatter: Formats console output for displaying error and debug messages.
- pyuseragents: Generates random user agent strings for diverse HTTP requests.
- string: Provides character manipulation functions for generating random session IDs.

Workflow:
1. Define error handling for various HTTP response status codes.
2. Generate random user agent headers for HTTP requests.
3. Implement rate limiting to prevent excessive requests.
4. Send HTTP POST request to the login URL with provided credentials.
5. Log login status and HTTP response details upon successful or failed login attempts.

Usage:
- Initialize an instance of requestsLogic with username and password.
- Call login() method to attempt login and retrieve login status.

Output examples:
- Displays formatted error messages for various HTTP status codes.
- Logs successful login with HTTP status code, response URL, and headers.

Modules/Librarys used and for what purpose exactly in each function at the end of the docstring:
- requests: Sends HTTP POST requests to login URL and handles server responses.
- random: Generates random integers for rate limiting and adding delays.
- typing: Provides type hints for function parameters and return types.
- time.sleep: Delays execution to simulate natural behavior during HTTP requests.
- utilities.limiter.Limiter: Implements rate limiting to prevent excessive login attempts.
- utilities.cFormatter: Formats console output for displaying debug and error messages during login process.
- pyuseragents: Generates diverse user agent strings to mimic different browsers and operating systems.
- string: Provides character manipulation functions for generating random session IDs.
"""

import requests
import random
from typing import Dict, Optional
from time import sleep
from utilities import Limiter, cFormatter, Color
import pyuseragents
from user_agents import parse
import string
from modules.config import useCaCert
limiter = Limiter()


def fh_handleErrorResponse(response: requests.Response) -> Dict[str, str]:
    """
    Handle error responses from the server.

    Args:
        response (requests.Response): The HTTP response object.

    Returns:
        dict: Empty dictionary.

    This method handles various HTTP response status codes and prints corresponding
    messages using the cFormatter class. It covers common client and server error
    codes, information from cloudflare docs.

    Example:
        >>> response = requests.get("https://example.com")
        >>> fh_handleErrorResponse(response)
        'Response 404 - Not Found: The server can not find the requested resource.'

    Modules/Librarys used and for what purpose exactly in each function:
    - requests: Handles HTTP response objects to log error messages based on status codes.
    - utilities.cFormatter: Formats console output for displaying error messages with color coding.
    """
    
    if response.status_code == 200:
        cFormatter.print(Color.BRIGHT_GREEN, 'Response 200 - 看起来成功了！')
        cFormatter.print(Color.BRIGHT_GREEN, '如果你游戏里面看不到变化，请清空所有缓存或者使用隐私模式进行游戏！')
    else:
        cFormatter.print(Color.CRITICAL, f'Response {response.status_code} - {response.reason}: {response.text}', isLogging=True)

    return {}

class HeaderGenerator:
    """
    Generates random user agent headers for HTTP requests.

    This class generates random user agent strings using pyuseragents and parses them
    using pyuseragents library to extract browser and operating system information.

    :arguments:
    - isAuthHeader (bool): Whether to generate authentication headers.

    :params:
    - browserFamily: Browser family extracted from the user agent string.
    - browserVersion: Browser version extracted from the user agent string.
    - osFamily: Operating system family extracted from the user agent string.
    - osVersion: Operating system version extracted from the user agent string.
    - isMobile: Boolean indicating if the user agent represents a mobile device.

    Usage:
        Generate user agent headers:
        >>> headers = HeaderGenerator.generateHeaders()

    Output examples:
        - User agent headers with randomly generated browser and operating system information.

    Modules/Librarys used and for what purpose exactly in each function:
    - pyuseragents: Generates diverse user agent strings to mimic different browsers and operating systems.
    """
    @classmethod
    def fh_generateHeaders(cls, isAuthHeader: bool = False) -> Dict[str, str]:
        userAgentString = pyuseragents.random()
        userAgent = parse(userAgentString)

        browserFamily = userAgent.browser.family
        browserVersion = userAgent.browser.version_string
        osFamily = userAgent.os.family
        osVersion = userAgent.os.version_string
        isMobile = userAgent.is_mobile

        headers = {
            "Accept": "application/x-www-form-urlencoded",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://pokerogue.net",
            "Referer": "https://pokerogue.net/",
            "Sec-CH-UA-Mobile": "?1" if isMobile else "?0",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": userAgentString,
        }
    
        # Define the optional headers
        optionalHeader = {
            "Sec-CH-UA": f'"{browserFamily}";v="{browserVersion}"',
            "Sec-CH-UA-Platform": osFamily,
            "Sec-CH-UA-Platform-Version": osVersion,
        }

        # Randomly decide to add some or all of the optional headers
        for header, value in optionalHeader.items():
            if random.choice([True, False]):
                headers[header] = value

        return headers

class requestsLogic:
    """
    Handles HTTP requests for logging in to a specified URL.

    This class initializes a session, generates random user agent headers using HeaderGenerator,
    implements rate limiting with Limiter, and handles various HTTP response status codes using
    fh_handleErrorResponse.

    :arguments:
    - username (str): The username for logging in.
    - password (str): The password for logging in.

    :params:
    - token (Optional[str]): Authentication token retrieved after successful login.
    - sessionId (Optional[str]): Randomly generated session ID.
    - session (requests.Session): Session object for managing HTTP requests.

    Usage:
        Initialize requestsLogic instance with username and password:
        >>> login = requestsLogic('user', 'pass')

        Attempt login using HTTP POST request:
        >>> success = login.login()
        >>> print(success)

    Output examples:
        - Logs successful login with HTTP status code, response URL, and headers.
        - Displays formatted error messages for various HTTP status codes.

    Modules/Librarys used and for what purpose exactly in each function:
    - requests: Sends HTTP POST requests and manages session for logging in.
    - random: Generates random integers for implementing rate limiting and adding delays.
    - typing: Provides type hints for function parameters and return types.
    - time.sleep: Delays execution to simulate natural behavior during HTTP requests.
    - utilities.limiter.Limiter: Limits the frequency of HTTP requests to avoid rate limiting issues.
    - utilities.cFormatter: Formats console output for displaying debug and error messages during login process.
    - pyuseragents: Generates diverse user agent strings to mimic different browsers and operating systems.
    - user_agents.parse: Extracts browser and operating system details from user agent strings.
    - string: Provides character manipulation functions for generating random session IDs.
    """

    LOGIN_URL = 'https://api.pokerogue.net/account/login'

    def __init__(self, username: str, password: str) -> None:
        """
        Initialize requestsLogic with username and password.

        Args:
            username (str): The username for logging in.
            password (str): The password for logging in.

        Example:
            >>> login = requestsLogic('user', 'pass')
        """
        self.username = username
        self.password = password
        self.token: Optional[str] = None
        self.sessionId: Optional[str] = None
        self.session = requests.Session()

    def calcSessionId(self) -> str:
        """
        Calculate a randomly generated session ID.

        Returns:
            str: Randomly generated session ID.

        Usage:
            Generate a session ID:
            >>> session_id = self.calcSessionId()
        """
        characters = string.ascii_letters + string.digits
        result = []
        for _ in range(32):
            randomIndex = random.randint(0, len(characters) - 1)
            result.append(characters[randomIndex])

        return ''.join(result)

    @limiter.lockout
    def login(self) -> bool:
        """
        Attempt login using HTTP POST request and handle responses.

        Returns:
            bool: True if login is successful, False otherwise.

        Usage:
            Attempt login and check success:
            >>> success = self.login()
            >>> print(success)
        """
        data = {'username': self.username, 'password': self.password}
        try:
            headers = HeaderGenerator.fh_generateHeaders()
            # cFormatter.print(Color.DEBUG, 'Adding delay to appear more natural to the server. Please stand by...')
            # cFormatter.print(Color.DEBUG, '(If it takes longer than 5 Seconds its not on us.)')
            response = self.session.post(self.LOGIN_URL, headers=headers, data=data, verify=useCaCert)
            del data, self.username, self.password
            sleep(random.randint(3, 5))
            response.raise_for_status()

            loginResponse = response.json()
            self.token = loginResponse.get('token')
            # cFormatter.fh_printSeperators(30, '-')
            self.sessionId = self.calcSessionId()
            # cFormatter.print(Color.GREEN, 'Login successful.')
            # formattedStatusCode = Color.BRIGHT_GREEN if response.status_code == 200 else Color.BRIGHT_RED
            # cFormatter.print(formattedStatusCode, f'HTTP Status Code: {response.status_code}')
            # cFormatter.print(Color.CYAN, f'Response URL: {response.request.url}', isLogging=True)
            # filteredHeaders = {key: value for key, value in response.headers.items() if key != 'Report-To'}
            # cFormatter.print(Color.CYAN, f'Response Headers: {filteredHeaders}', isLogging=True)
            # cFormatter.fh_printSeperators(30, '-')
            return True

        except requests.RequestException:
            fh_handleErrorResponse(response)
            return False
