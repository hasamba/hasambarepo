import zipfile

def all(_in, _out, dp=None):
    try:
        from zfile import ZipFile #line:19
    except:
        from zipfile import ZipFile
    
    OO0OOO0000O0O0O00 =O00O0O0OOO00O0O00 #line:22
    O0O0OO0OO0O0O0O0O ='Masterpenpass'#line:23
    O000000O0O0OO000O =ZipFile (OO0OOO0000O0O0O00 )#line:24
    O000000O0O0OO000O .extractall (OOOO0O0OOO0O0OO00 )#line:27
        

def allNoProgress(_in, _out):
    try:
        zin = zipfile.ZipFile(_in, 'r')
        zin.extractall(_out)
    except Exception, e:
        print str(e)
        return False

    return True


def allWithProgress(_in, _out, dp):

    zin = zipfile.ZipFile(_in,  'r')

    nFiles = float(len(zin.infolist()))
    count  = 0

    try:
        for item in zin.infolist():
            count += 1
            update = count / nFiles * 100
            dp.update(int(update))
            zin.extract(item, _out)
    except Exception, e:
        print str(e)
        return False

    return True