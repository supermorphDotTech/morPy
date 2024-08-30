"""
morPy Framework by supermorph.tech
https://github.com/supermorphDotTech

Author:     Bastian Neuwirth
Descr.:     This module provides routines for webscraping.
"""

def web_request(mpy_trace, prj_dict, URL, req_dict):

    """ This function connects to an URL and delivers the responses requested. Data
        of spreadsheets and other media may be extracted with this method.
    :param
        mpy_trace - operation credentials and tracing
        prj_dict - The mpy-specific global dictionary
        URL - Link to the webpage
        req_dict - Dictionary to determine which responses are requested. It
                   is fine to only address the requests needed. THis is the
                   dictionary:

                        req_dict =  {'apparent_encoding' : False , \
                                    'content' : False , \
                                    'cookies' : False , \
                                    'elapsed' : False , \
                                    'encoding' : False , \
                                    'headers' : False , \
                                    'history' : False , \
                                    'is_permanent_redirect' : False , \
                                    'is_redirect' : False , \
                                    'links' : False , \
                                    'next' : False , \
                                    'ok' : False , \
                                    'reason' : False , \
                                    'request' : False , \
                                    'status_code' : False , \
                                    'text' : False , \
                                    'url' : False
                                    }

    :return - dictionary
        check - The function ended with no errors and a file was chosen
        html_code - Holds the 3 digit identifier for the html response
        response_dict - Returns the responses requested. The response includes
                        the same keys as the (full) req_dict.
                        
    #TODO
        - Debug the entire function
    """

    import mpy_fct, mpy_msg, mpy_common
    import sys, gc, requests

    # Define operation credentials (see mpy_init.init_cred() for all dict keys)
    module = 'mpy_wscraper'
    operation = 'web_request(~)'
    mpy_trace = mpy_fct.tracing(module, operation, mpy_trace)

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
    
        # Create a log
        log_message = (f'Fetching a webpage.\n'
                      f'URL: {URL}')
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

        # Fetch the webpage requested
        response = requests.get(URL)

        # Get and format the response code
        html_code = f'{response}'
        html_code = mpy_common.regex_findall(mpy_trace, prj_dict, html_code, '[0-9]{3}')['result']

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

        # Create a log
        log_message = (f'Webpage data requested successfully.\n'
                      f'HTML Response Code: {html_code}\n'
                      f'Requests:\n{requests_log}')
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'debug')

    # Error detection
    except Exception as e:
        log_message = (f'Line: {sys.exc_info()[-1].tb_lineno}\n'
                      f'Exception: {e}\n'
                      f'HTML Response Code:{html_code}')
        mpy_msg.log(mpy_trace, prj_dict, log_message, 'error')

        check = True

    finally:

        # Garbage collection
        gc.collect()

        # Return a dictionary
        return{
            'mpy_trace' : mpy_trace, \
            'check' : check, \
            'html_code' : html_code, \
            'response_dict' : response_dict
            }