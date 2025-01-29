r"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module provides routines for webscraping.
"""

import lib.fct as fct
import common
import sys
import requests

from lib.decorators import metrics, log

@metrics
def web_request(morPy_trace: dict, app_dict: dict, URL: str, req_dict: dict) -> dict:

    r"""
    Connects to a URL and delivers the requested responses. Data from web pages,
    such as spreadsheets or other media, can be extracted using this method.

    :param morPy_trace: Operation credentials and tracing information.
    :param app_dict: The morPy global dictionary containing app configurations.
    :param URL: The link to the webpage.
    :param req_dict: Dictionary specifying which responses are requested. Example:
        req_dict = {
            'apparent_encoding': False,
            'content': False,
            'cookies': False,
            'elapsed': False,
            'encoding': False,
            'headers': False,
            'history': False,
            'is_permanent_redirect': False,
            'is_redirect': False,
            'links': False,
            'next': False,
            'ok': False,
            'reason': False,
            'request': False,
            'status_code': False,
            'text': False,
            'url': False
        }

    :return: dict
        morPy_trace: Operation credentials and tracing.
        check: Indicates whether the function executed successfully (True/False).
        html_code: The 3-digit HTTP response code.
        response_dict: Returns the requested responses. Includes the same keys as the provided `req_dict`.

    :example:
        web_request(morPy_trace, app_dict, "https://example.com", {'content': True, 'status_code': True})

    TODO finish the function
    """

    # Define operation credentials (see init.init_cred() for all dict keys)
    module = 'web'
    operation = 'web_request(~)'
    morPy_trace = fct.tracing(module, operation, morPy_trace)

    # Preparing parameters
    check = False

    try:

        # Apply standard formats
        URL = f'{URL}'
        requests_log = ''
        html_code = 'VOID'
        response_dict = {'apparent_encoding' : 'VOID' , \
                        'content' : 'VOID' , \
                        'cookies' : 'VOID' , \
                        'elapsed' : 'VOID' , \
                        'encoding' : 'VOID' , \
                        'headers' : 'VOID' , \
                        'history' : 'VOID' , \
                        'is_permanent_redirect' : 'VOID' , \
                        'is_redirect' : 'VOID' , \
                        'links' : 'VOID' , \
                        'next' : 'VOID' , \
                        'ok' : 'VOID' , \
                        'reason' : 'VOID' , \
                        'request' : 'VOID' , \
                        'status_code' : 'VOID' , \
                        'text' : 'VOID' , \
                        'url' : 'VOID'
                        }

        # TODO Localization
        log(morPy_trace, app_dict, "info",
            lambda: f'Fetching a webpage.\n'
                      f'URL: {URL}')

        # Fetch the webpage requested
        response = requests.get(URL)

        # Get and format the response code
        html_code = f'{response}'
        html_code = common.regex_findall(morPy_trace, app_dict, html_code, '[0-9]{3}')['result']

        # Evaluate the request and get responses
        # Loop through requests to show up in logging
        for key, value in req_dict.items():

            # Select only the activated requests
            if value:
                response_dict[key] = f'response.{key}'

                # Prepare log message of requested items
                if not requests_log:
                    requests_log = f'> {key}'
                else:
                    requests_log = f'{requests_log}\n> {key}'

        # TODO Localization
        log(morPy_trace, app_dict, "debug",
            lambda: f'Webpage data requested successfully.\n'
                      f'HTML Response Code: {html_code}\n'
                      f'Requests:\n{requests_log}')

        check = True

    except Exception as e:
        log(morPy_trace, app_dict, "error",
            lambda: f'{app_dict["loc"]["morPy"]["err_line"]}: {sys.exc_info()[-1].tb_lineno}\n'
                f'{type(e).__name__}: {e}')

    return{
        'morPy_trace' : morPy_trace, \
        'check' : check, \
        'html_code' : html_code, \
        'response_dict' : response_dict
        }