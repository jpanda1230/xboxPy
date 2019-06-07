import os
import sys
import time

import xbox.webapi.scripts.authenticate as auth

from xbox.webapi.api.client import XboxLiveClient
from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.common.exceptions import AuthenticationException



def load_password():
    return  "Celeste1"

def read_file(path):
    with open(path, 'r') as f:
        return f.read().split()

def update_log(tag):
    global current_account
    with open("C:/Users/tellg/OneDrive/Desktop/Cuba's Turbo/claim_log",'a') as f:
        f.write("Email: {} Tag: {} \n".format(name, tag))
     
    
def initiate_turbo(name,accounts,gamertags):

    counter = 0
    
    password = load_password()
    
    auth.main(name, password)

    try:
            auth_mgr = AuthenticationManager.from_file('C:/Users/tellg/AppData/Local/OpenXbox/xbox/tokens.json')
    except FileNotFoundError as e:
            print( 'Failed to load tokens from \'{}\'.\n'
            'ERROR: {}'.format(e.filename, e.strerror) )
            sys.exit(-1)

    try:
        auth_mgr.authenticate(do_refresh=True)
    except AuthenticationException as e:
        print('Authentication failed! Err: %s' % e)
        sys.exit(-1)

    xbl_client = XboxLiveClient(auth_mgr.userinfo.userhash, auth_mgr.xsts_token.jwt, auth_mgr.userinfo.xuid)

    
    while True:
        
        for tag in gamertags:
            
            time.sleep(0.15)
            if xbl_client.profile.get_profile_by_gamertag(tag).status_code == 200:
                print(tag + ': Not available for claiming')

            else:
                response = xbl_client.accounts.change_gamertag(str(xbl_client.xuid), tag)
                
                if response.status_code == 200:
                    update_log(tag)
                    print("Tag: "+ tag +" has been claimed!")
                    try:
                        name = accounts.pop(0)
                        gamertags.remove(tag)
                    except:
                        print("No more accounts available to claim!")
                        sys.exit(0)
                    initiate_turbo(name, accounts, gamertags)
                    
                elif response.status_code == 403:
                    os.remove("C:/Users/tellg/AppData/Local/OpenXbox/xbox/tokens.json")
                    print("Tag is not yet out in wild")
                    print("Refreshing tokens.json")
                    initiate_turbo(name, accounts, gamertags)
                    

                elif response.status_code == 429:
                    time.sleep(15)

                elif response.status_code == 1020:
                    print('Changing gamertag failed - You are out of free changes')

                else:
                    time.sleep(0.5)
                    os.remove("C:/Users/tellg/AppData/Local/OpenXbox/xbox/tokens.json")
                    print("Refreshing tokens.json")
                    initiate_turbo(name, accounts, gamertags)

            counter += 1

            if counter%298 == 0:
                cls = lambda: os.system('cls')
                cls()
                time.sleep(1)

            if counter%600 == 0:
                return
                
    


def main():
      
      gamertags = read_file("C:/Users/tellg/OneDrive/Desktop/Cuba's Turbo/gamertags.txt")
      accounts = read_file("C:/Users/tellg/OneDrive/Desktop/Cuba's Turbo/accounts.txt")
      name = accounts.pop(0)

      initiate_turbo(name, accounts, gamertags)         
  
