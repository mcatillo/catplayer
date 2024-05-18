'''

catplayer: app for video player

Copyright (C) 2024 Marco Catillo

Distribuited under GPLv3 license
https://www.gnu.org/licenses/gpl-3.0.html

Functions for managing path across different operating systems

'''

import json

def get_past_settings(path):
    ''' Get the past settings saved on the previous application usage

    Returns:
        dict: dictionary of previous settings.
    '''
    with open(path.expand('rw_files','config','config.json'),'r') as f:
        latest_config = json.load(f)
    return latest_config
