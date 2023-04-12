import getpass
import xbmcgui,xbmc,os,xbmcaddon
from generic import *
from resources.modules import log
log.warning("Starting login sequence1")
Addon = xbmcaddon.Addon()
import xbmcvfs
from urllib.parse import parse_qsl
xbmc_tranlate_path=xbmcvfs.translatePath

user_dataDir = xbmc_tranlate_path(Addon.getAddonInfo("profile")).decode("utf-8")
if not os.path.exists(user_dataDir):
     os.makedirs(user_dataDir)
logo_path=os.path.join(user_dataDir, 'logo')
if not os.path.exists(logo_path):
     os.makedirs(logo_path)
files_path=os.path.join(user_dataDir, 'files')
if not os.path.exists(files_path):
     os.makedirs(files_path)
db_path=os.path.join(user_dataDir, 'database')
if not os.path.exists(db_path):
     os.makedirs(db_path)
log.warning("Starting login sequence2")
def logout():
    loggging.warning('Logout')
    td_send({'@type': 'logOut'})

def wait_response(id,dp=''):
    while True:
        event = td_receive()
        
        
        
            
            
        log.warning('Alive wait')
        if event:
            if event.get('@type') =='error':
               
                xbmcgui.Dialog().ok('Error occurred',str(event.get('message')))
                break
            j_enent=(event)
           
            if '@extra' in j_enent :
               if j_enent['@extra']==id:
               
                break
        xbmc.sleep(1)
    return (event)

log.warning("Starting login sequence")
dp = xbmcgui . DialogProgress ( )
dp.create('Please Wait...','Login', '','')
dp.update(0, 'Please Wait...','Login', '' )


timeout=0
while True:
    
    try:
        event = (td_receive())
    except Exception as e:
        log.warning("Err in recive:"+str(e))
    
   
    if dp.iscanceled():
                      dp.close()
                     
                      break
    
    if event:
        if event.get('@type') =='error':
            answer=(str(event.get('message')))
            if 'Too Many' in answer:
               
                added_t=' Seconds'
            else:
                added_t=''
            xbmcgui.Dialog().ok('Error occurred',str(event.get('message'))+added_t)
            break
        if event.get('@type') == 'updateAuthorizationState':
            
            authtype = event.get('authorization_state').get('@type')
            if authtype == "authorizationStateWaitTdlibParameters":
                log.warning('send: setTdlibParameters')
                timeout=0
                dp.update(10, 'Please Wait...','Login', 'updateAuthorizationState' )
                td_send({'@type': 'setTdlibParameters',
                     'parameters': {'use_test_dc': False,
                                    'api_id':94575,
                                    'api_hash': 'a3406de8d171bb422bb6ddf3bbd800e2',
                                    'device_model': 'Desktop',
                                    'system_version': 'Unknown',
                                    'application_version': "0.0",
                                    'system_language_code': 'en',
                                    'database_directory': db_path,
                                    'files_directory': files_path,
                                    'use_file_database': False,
                                    'use_chat_info_database': False,
                                    'use_message_database': False,
                                    }
                     })
            elif authtype == 'authorizationStateWaitEncryptionKey':
                
                log.warning('send: checkDatabaseEncryptionKey')
                dp.update(20, 'Please Wait...','Login', 'checkDatabaseEncryptionKey' )
                td_send({'@type': 'checkDatabaseEncryptionKey', 'encryption_key': 'randomencryption'})
            elif authtype == "authorizationStateWaitPhoneNumber":
                #phone = input('Enter phone number:')
                dp.close()
                phone = xbmcgui.Dialog().input('Enter phone number:', '', xbmcgui.INPUT_NUMERIC)
                td_send({'@type': 'setAuthenticationPhoneNumber',
                         'phone_number': str(phone),
                         'allow_flash_call': False,
                         'is_current_phone_number': False}
                        )
            elif authtype == "authorizationStateWaitCode":
                #code = input('Enter code:')
                code = xbmcgui.Dialog().input('Enter code:', '', xbmcgui.INPUT_ALPHANUM)
                td_send({'@type': 'checkAuthenticationCode', 'code': str(code)})
            elif authtype == "authorizationStateWaitPassword":
                #password = getpass.getpass('Password:')
                password = xbmcgui.Dialog().input('Password:', '', xbmcgui.INPUT_ALPHANUM)
                td_send({'@type': 'checkAuthenticationPassword', 'password': password})
            elif authtype == "authorizationStateReady":
                break
            
    log.warning('Alive login')
    xbmc.sleep(100)

dp.close()
# more awesome stuff here

# td_json_client_destroy(client)
