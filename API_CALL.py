from __future__ import print_function
import time
import cfbd
from cfbd.rest import ApiException
from pprint import pprint
import API_KEYS

configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = API_KEYS.MY_API_KEY # Be sure to enter your API key here
configuration.api_key_prefix['Authorization'] = 'Bearer'

api_instance = cfbd.GamesApi(cfbd.ApiClient(configuration))
