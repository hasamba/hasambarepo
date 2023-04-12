from ctypes import CDLL, c_void_p, c_char_p, c_double, c_int, c_longlong,c_long, CFUNCTYPE,c_int64
from ctypes.util import find_library
import os,logging,sys,xbmc
from shutil import copyfile
import imp,xbmcaddon
Addon = xbmcaddon.Addon()

user_dataDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
if not os.path.exists(user_dataDir):
     os.makedirs(user_dataDir)
import json
print 'Start'
import platform
platform= (platform.architecture())
logging.warning(platform)

cur=os.path.dirname(os.path.abspath(__file__))
cur=os.path.join(cur,'resources')
if platform[0]=='32bit':
        logging.warning('32bit')




if sys.platform.lower().startswith('linux'):
    plat = 'linux'
    if 'ANDROID_DATA' in os.environ:
        plat = 'android'
elif sys.platform.lower().startswith('win'):
    plat = 'windows'
elif sys.platform.lower().startswith('darwin'):
    plat = 'darwin'
else:
    plat = None
logging.warning('Platform:'+plat)
if plat == 'android':
    if platform[0]=='32bit':
        logging.warning('32bit')
        f_name='libtdjsonjava32'
    else:
        f_name='libtdjsonjava64'
    #loc1=os.path.join(xbmc.translatePath('special://temp'),'libtdjni.so')

    loc1=os.path.join(xbmc.translatePath('special://xbmc'),'libtdjsonjava.so')

    #loc1=os.path.join(os.path.dirname(os.path.abspath(__file__)),'libtdjni.so')

    #loc4=os.path.join(xbmc.translatePath('special://temp'),'libtdjson.so')

    loc4=os.path.join(xbmc.translatePath('special://xbmc'),'libtdjson.so')

    #loc4=os.path.join(os.path.dirname(os.path.abspath(__file__)),'libtdjson.so')
    #if not os.path.exists(loc1):
    copyfile(os.path.join(cur,'lib','%s.so'%f_name),loc1)

    #all_option=[loc1,loc2,loc3]#,os.path.join(cur,'lib','libtdjni.so'),os.path.join(cur,'lib','libtdjsonjava_armv7.so'),os.path.join(cur,'lib','libtdjsonjava_arm64.so'),os.path.join(cur,'lib','libtdjsonjava_and_x86.so'),os.path.join(cur,'lib','libtdjsonjava_and_64.so')]
    #all_option2=[loc4,loc5,loc6]
  
    if 1:#for items in all_option:
        try:
            logging.warning('CDLL:'+loc1)
            tdjson=CDLL(loc1)
         
          
            cwd=xbmc.translatePath('special://xbmc')
            logging.warning('Imp:'+loc1)
           
    
            #break
        except Exception as e:
            logging.warning(e)
            pass
    td_json_client_create = tdjson._td_json_client_create
    td_json_client_create.restype = c_void_p
    td_json_client_create.argtypes = []

    td_json_client_receive = tdjson._td_json_client_receive
    td_json_client_receive.restype = c_char_p
    td_json_client_receive.argtypes = [c_void_p, c_double]

    td_json_client_send = tdjson._td_json_client_send
    td_json_client_send.restype = None
    td_json_client_send.argtypes = [c_void_p, c_char_p]

    td_json_client_execute = tdjson._td_json_client_execute
    td_json_client_execute.restype = c_char_p
    td_json_client_execute.argtypes = [c_void_p, c_char_p]

    td_json_client_destroy = tdjson._td_json_client_destroy
    td_json_client_destroy.restype = None
    td_json_client_destroy.argtypes = [c_void_p]
    logging.warning('Done Define')
    
else:
    ph=os.path.join(cur,'lib','libeay32.dll')
    logging.warning(ph)
    CDLL(ph)


    ph=os.path.join(cur,'lib','ssleay32.dll')
    logging.warning(ph)
    CDLL(ph)


    ph=os.path.join(cur,'lib','zlib1.dll')

    CDLL(ph)

    ph=os.path.join(cur,'lib','tdjson32.dll')
    print ph
    tdjson = CDLL(ph)

    # tdjson = CDLL(tdjson_path)

    td_json_client_create = tdjson.td_json_client_create
    td_json_client_create.restype = c_void_p
    td_json_client_create.argtypes = []

    td_json_client_receive = tdjson.td_json_client_receive
    td_json_client_receive.restype = c_char_p
    td_json_client_receive.argtypes = [c_void_p, c_double]

    td_json_client_send = tdjson.td_json_client_send
    td_json_client_send.restype = None
    td_json_client_send.argtypes = [c_void_p, c_char_p]

    td_json_client_execute = tdjson.td_json_client_execute
    td_json_client_execute.restype = c_char_p
    td_json_client_execute.argtypes = [c_void_p, c_char_p]

    td_json_client_destroy = tdjson.td_json_client_destroy
    td_json_client_destroy.restype = None
    td_json_client_destroy.argtypes = [c_void_p]

    td_set_log_file_path = tdjson.td_set_log_file_path
    td_set_log_file_path.restype = c_int
    td_set_log_file_path.argtypes = [c_char_p]

    td_set_log_max_file_size = tdjson.td_set_log_max_file_size
    td_set_log_max_file_size.restype = None
    td_set_log_max_file_size.argtypes = [c_longlong]

    td_set_log_verbosity_level = tdjson.td_set_log_verbosity_level
    td_set_log_verbosity_level.restype = None
    td_set_log_verbosity_level.argtypes = [c_int]

    fatal_error_callback_type = CFUNCTYPE(None, c_char_p)

    td_set_log_fatal_error_callback = tdjson.td_set_log_fatal_error_callback
    td_set_log_fatal_error_callback.restype = None
    td_set_log_fatal_error_callback.argtypes = [fatal_error_callback_type]
    td_set_log_verbosity_level(2)
    def on_fatal_error_callback(error_message):
        print('TDLib fatal error: ', error_message)
    c_on_fatal_error_callback = fatal_error_callback_type(on_fatal_error_callback)
    td_set_log_fatal_error_callback(c_on_fatal_error_callback)







def td_send(query):
    query = json.dumps(query).encode('utf-8')
    td_json_client_send(client, query)


def td_receive():
    logging.warning('td_json_client_receive')
    logging.warning(client)
    
    result = td_json_client_receive(client, 1.0)
    logging.warning('Done td_json_client_receive')
    if result:
        result = json.loads(result.decode('utf-8'))
        #result = (result.decode('utf-8'))
        
    return result

def td_close():
    td_json_client_destroy(client)
def td_execute(query):
    query = json.dumps(query).encode('utf-8')
    result = td_json_client_execute(client, query)
    if result:
        result = json.loads(result.decode('utf-8'))
        
    return result
file = open(os.path.join(user_dataDir, 'c_id.txt'), 'r')  
file_data= file.read()
file.close()
logging.warning('client_create')
client = int(file_data)
'''
try:
    client=long(Addon.getSetting("client_id"))
except:
    client = td_json_client_create()
    Addon.setSetting('client_id',str(client))
'''
logging.warning('Done client_create')
