# -*- coding: utf-8 -*-
import sys,logging,urllib2

import  re


UA = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0"
def VScreateDialogSelect(label,sTitle=''):
    oDialog = xbmcgui.Dialog()
    if sTitle:
        ret = oDialog.select(sTitle, label)
    else:
        ret = oDialog.select('Sélectionner une qualité', label)

    return ret
class Unbaser(object):
    """Functor for a given base. Will efficiently convert
    strings to natural numbers."""
    ALPHABET = {
        62: '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        95: (' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ'
             '[\]^_`abcdefghijklmnopqrstuvwxyz{|}~')
    }

    def __init__(self, base):
        self.base = base
        
        #Error not possible, use 36 by defaut
        if base == 0 :
            base = 36
        
        # If base can be handled by int() builtin, let it do it for us
        if 2 <= base <= 36:
            self.unbase = lambda string: int(string, base)
        else:
            if base < 62:
                self.ALPHABET[base] = self.ALPHABET[62][0:base]
            elif 62 < base < 95:
                self.ALPHABET[base] = self.ALPHABET[95][0:base]
            # Build conversion dictionary cache
            try:
                self.dictionary = dict((cipher, index) for index, cipher in enumerate(self.ALPHABET[base]))
            except KeyError:
                raise TypeError('Unsupported base encoding.')

            self.unbase = self._dictunbaser

    def __call__(self, string):
        return self.unbase(string)

    def _dictunbaser(self, string):
        """Decodes a  value to an integer."""
        ret = 0
        
        for index, cipher in enumerate(string[::-1]):
            ret += (self.base ** index) * self.dictionary[cipher]
        return ret

class cPacker():
    def detect(self, source):
        """Detects whether `source` is P.A.C.K.E.R. coded."""
        return source.replace(' ', '').startswith('eval(function(p,a,c,k,e,')

    def unpack(self, source):
        """Unpacks P.A.C.K.E.R. packed js code."""
        payload, symtab, radix, count = self._filterargs(source)
        
        #correction pour eviter bypass
        if (len(symtab) > count) and (count > 0):
            del symtab[count:]
        if (len(symtab) < count) and (count > 0):
            symtab.append('BUGGED')   

        if count != len(symtab):
            raise UnpackingError('Malformed p.a.c.k.e.r. symtab.')
        
        try:
            unbase = Unbaser(radix)
        except TypeError:
            raise UnpackingError('Unknown p.a.c.k.e.r. encoding.')

        def lookup(match):
            """Look up symbols in the synthetic symtab."""
            word  = match.group(0)
            return symtab[unbase(word)] or word

        source = re.sub(r'\b\w+\b', lookup, payload)
        return self._replacestrings(source)

    def _cleanstr(self, str):
        str = str.strip()
        if str.find("function") == 0:
            pattern = (r"=\"([^\"]+).*}\s*\((\d+)\)")
            args = re.search(pattern, str, re.DOTALL)
            if args:
                a = args.groups()
                def openload_re(match):
                    c = match.group(0)
                    b = ord(c) + int(a[1])
                    return chr(b if (90 if c <= "Z" else 122) >= b else b - 26)

                str = re.sub(r"[a-zA-Z]", openload_re, a[0]);
                str = urllib2.unquote(str)

        elif str.find("decodeURIComponent") == 0:
            str = re.sub(r"(^decodeURIComponent\s*\(\s*('|\"))|(('|\")\s*\)$)", "", str);
            str = urllib2.unquote(str)
        elif str.find("\"") == 0:
            str = re.sub(r"(^\")|(\"$)|(\".*?\")", "", str);
        elif str.find("'") == 0:
            str = re.sub(r"(^')|('$)|('.*?')", "", str);

        return str

    def _filterargs(self, source):
        """Juice from a source file the four args needed by decoder."""
        
        source = source.replace(',[],',',0,')

        juicer = (r"}\s*\(\s*(.*?)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*\((.*?)\).split\((.*?)\)")
        args = re.search(juicer, source, re.DOTALL)
        if args:
            a = args.groups()
            try:
                return self._cleanstr(a[0]), self._cleanstr(a[3]).split(self._cleanstr(a[4])), int(a[1]), int(a[2])
            except ValueError:
                raise UnpackingError('Corrupted p.a.c.k.e.r. data.')

        juicer = (r"}\('(.*)', *(\d+), *(\d+), *'(.*)'\.split\('(.*?)'\)")
        args = re.search(juicer, source, re.DOTALL)
        if args:
            a = args.groups()
            try:
                return a[0], a[3].split(a[4]), int(a[1]), int(a[2])
            except ValueError:
                raise UnpackingError('Corrupted p.a.c.k.e.r. data.')

        # could not find a satisfying regex
        raise UnpackingError('Could not make sense of p.a.c.k.e.r data (unexpected code structure)')



    def _replacestrings(self, source):
        """Strip string lookup table (list) and replace values in source."""
        match = re.search(r'var *(_\w+)\=\["(.*?)"\];', source, re.DOTALL)

        if match:
            varname, strings = match.groups()
            startpoint = len(match.group(0))
            lookup = strings.split('","')
            variable = '%s[%%d]' % varname
            for index, value in enumerate(lookup):
                source = source.replace(variable % index, '"%s"' % value)
            return source[startpoint:]
        return source
        
    def detect(self, source):
        """Detects whether `source` is P.A.C.K.E.R. coded."""
        return source.replace(' ', '').startswith('eval(function(p,a,c,k,e,')

    def unpack(self, source):
        """Unpacks P.A.C.K.E.R. packed js code."""
        payload, symtab, radix, count = self._filterargs(source)
        
        #correction pour eviter bypass
        if (len(symtab) > count) and (count > 0):
            del symtab[count:]
        if (len(symtab) < count) and (count > 0):
            symtab.append('BUGGED')   

        if count != len(symtab):
            raise UnpackingError('Malformed p.a.c.k.e.r. symtab.')
        
        try:
            unbase = Unbaser(radix)
        except TypeError:
            raise UnpackingError('Unknown p.a.c.k.e.r. encoding.')

        def lookup(match):
            """Look up symbols in the synthetic symtab."""
            word  = match.group(0)
            return symtab[unbase(word)] or word

        source = re.sub(r'\b\w+\b', lookup, payload)
        return self._replacestrings(source)

    def _cleanstr(self, str):
        str = str.strip()
        if str.find("function") == 0:
            pattern = (r"=\"([^\"]+).*}\s*\((\d+)\)")
            args = re.search(pattern, str, re.DOTALL)
            if args:
                a = args.groups()
                def openload_re(match):
                    c = match.group(0)
                    b = ord(c) + int(a[1])
                    return chr(b if (90 if c <= "Z" else 122) >= b else b - 26)

                str = re.sub(r"[a-zA-Z]", openload_re, a[0]);
                str = urllib2.unquote(str)

        elif str.find("decodeURIComponent") == 0:
            str = re.sub(r"(^decodeURIComponent\s*\(\s*('|\"))|(('|\")\s*\)$)", "", str);
            str = urllib2.unquote(str)
        elif str.find("\"") == 0:
            str = re.sub(r"(^\")|(\"$)|(\".*?\")", "", str);
        elif str.find("'") == 0:
            str = re.sub(r"(^')|('$)|('.*?')", "", str);

        return str

def CheckCpacker(str):

    sPattern = '(\s*eval\s*\(\s*function(?:.|\s)+?{}\)\))'
    aResult = re.findall(sPattern,str)
    if (aResult):
        str2 = aResult[0]
        if not str2.endswith(';'):
            str2 = str2 + ';'
        try:
            str = cPacker().unpack(str2)
            print('Cpacker encryption')
        except:
            pass

    return str
class cParser:

    def parseSingleResult(self, sHtmlContent, sPattern):     
	aMatches = re.compile(sPattern).findall(sHtmlContent)
	if (len(aMatches) == 1):
                aMatches[0] = self.__replaceSpecialCharacters(aMatches[0])
		return True, aMatches[0]
        return False, aMatches

    def __replaceSpecialCharacters(self, sString):
        return sString.replace('\\/','/').replace('&amp;','&').replace('\xc9','E').replace('&#8211;', '-').replace('&#038;', '&').replace('&rsquo;','\'').replace('\r','').replace('\n','').replace('\t','').replace('&#039;',"'").replace('&quot;','"').replace('&gt;','>').replace('&lt;','<').replace('&nbsp;','')

    def parse(self, sHtmlContent, sPattern, iMinFoundValue = 1):
        sHtmlContent = self.__replaceSpecialCharacters(str(sHtmlContent))
        aMatches = re.compile(sPattern, re.IGNORECASE).findall(sHtmlContent)
        if (len(aMatches) >= iMinFoundValue):                
            return True, aMatches
        return False, aMatches

    def replace(self, sPattern, sReplaceString, sValue):
         return re.sub(sPattern, sReplaceString, sValue)

    def escape(self, sValue):
        return re.escape(sValue)
    
    def getNumberFromString(self, sValue):
        sPattern = "\d+"
        aMatches = re.findall(sPattern, sValue)
        if (len(aMatches) > 0):
            return aMatches[0]
        return 0
        
    def titleParse(self, sHtmlContent, sPattern):
        sHtmlContent = self.__replaceSpecialCharacters(str(sHtmlContent))
        aMatches = re.compile(sPattern, re.IGNORECASE)
        try: 
            [m.groupdict() for m in aMatches.finditer(sHtmlContent)]              
            return m.groupdict()
        except:
            return {'title': sHtmlContent}

    def abParse(self,sHtmlContent,start,end,startoffset=''):
        #usage oParser.abParse(sHtmlContent,"start","end")
        #startoffset (int) décale le début pour ne pas prendre en compte start dans le résultat final si besoin
        #usage2 oParser.abParse(sHtmlContent,"start","end",6)
        #ex youtube.py
        if startoffset:
            return sHtmlContent[startoffset + sHtmlContent.find(start):sHtmlContent.find(end)]
        else:
            return sHtmlContent[sHtmlContent.find(start):sHtmlContent.find(end)]

def LoadLinks(htmlcode):
   

    sPattern ='[\("\'](https*:)*(\/[^,"\'\)\s]+)[\)\'"]'
    aResult = re.findall(sPattern, htmlcode, re.DOTALL)

    #xbmc.log(str(aResult))
    for http,urlspam in aResult:
        sUrl = urlspam
            
        if http:
            sUrl = http + sUrl
            
        sUrl = sUrl.replace('/\/','//')
        sUrl = sUrl.replace('\/','/')
        
        #filtrage mauvaise url
        if (sUrl.count('/') < 2) or ('<' in sUrl) or ('>' in sUrl) or (len(sUrl) < 15):
            continue
        if '[' in sUrl or ']' in sUrl:
            continue
        if '.jpg' in sUrl or '.png' in sUrl:
            continue
        
       
        
        if '\\x' in sUrl or '\\u' in sUrl:
            sUrl = ASCIIDecode(sUrl)
            if not sUrl:
                continue
        
        if sUrl.startswith('//'):
            sUrl = 'http:' + sUrl
            
        if sUrl.startswith('/'):
            host = 'https://thevideo.website'
            sUrl = host + sUrl
        
        #Url ou il ne faut pas aller
        if 'dok3v' in sUrl:
            continue
            
        #pour test
        if ('.js' not in sUrl) and ('.cgi' not in sUrl):
            continue
        #if 'flashx' in sUrl:
            #continue

        headers8 = {
        'User-Agent': UA
        #'Referer':'https://www.flashx.tv/dl?playthis'
        }

        try:
            logging.warning(sUrl)
            request = urllib2.Request(sUrl,None,headers8)
            reponse = urllib2.urlopen(request)
            sCode = reponse.read()
            reponse.close()
    
        except urllib2.HTTPError, e:

            if not e.geturl() == sUrl:
                
                
                try:
          
                    headers9 = {
                    'User-Agent': UA,
                    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language':'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
                    'Accept-Encoding':'gzip, deflate, br'
                    }
                    request = urllib2.Request(e.geturl().replace('https', 'http'), None, headers9)
                    reponse = urllib2.urlopen(request)
                    sCode = reponse.read()
                    reponse.close()
                
                except urllib2.HTTPError, e:
            
                    #xbmc.log(e.read())
                    logging.warning('Redirection Blocked ' + sUrl + ' Red ' + e.geturl())
                    pass
            else:
                logging.warning('Blocked ' + sUrl)
                logging.warning(str(e.code))
                logging.warning('>>' + e.geturl())
                #logging.warning(e.read())
    
    logging.warning('fin des unlock')
def __getIdFromUrl(sUrl):
    """ URL trouvées:
        https://thevideo.me/1a2b3c4e5d6f
        https://thevideo.me/embed-1a2b3c4e5d6f.html
        http(s)://thevideo.me/embed-1a2b3c4e5d6f-816x459.html
    """
    sPattern = '\/(?:embed-)?(\w+)(?:-\d+x\d+)?(?:\.html)?$' 
    aResult = cParser().parse( sUrl, sPattern )
    if (aResult[0] == True):
        return aResult[1][0]
    return ''

def __getIdFromUrl_vidup( sUrl):
        sPattern = 'https*://vidup.me/([^<]+)'
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''
        
def __getKey(sHtmlContent):
        '''
        import requests


        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'vidup.tv',
            'Pragma': 'no-cache',
            'Referer': __sUrl,
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
        }

        response = requests.get(__sUrl, headers=headers).content
        regex="'_vhash', value: '(.+?)'"
        _vhash=re.compile(regex).findall(response)[0]
        
        regex="'gfk', value: '(.+?)'"
        gfk=re.compile(regex).findall(response)[0]
        
        regex='name="id" value="(.+?)"'
        id=re.compile(regex).findall(response)[0]
        
        regex='name="fname" value="(.+?)"'
        fname=re.compile(regex).findall(response)[0]
        
        regex='name="hash" value="(.+?)"'
        hash=re.compile(regex).findall(response)[0]
        
        
        regex='name="inhu" value="(.+?)"'
        inhu=re.compile(regex).findall(response)[0]
        data={'_vhash':_vhash,
        'gfk':gfk,
        'op':'download1',
        'usr_login':'',
        'id':id,
        'fname':fname,
        'referer':'',
        'hash':hash,
        'inhu':inhu,
        'imhuman':''}
        data={'gfk': 'i22abd2449', 'imhuman': '', 'referer': '', 'inhu': 'foff', 'fname': 'Guardians.of.the.Galaxy.2014.720p.BluRay.H264.AAC-RARBG.mp4', 'id': 'v2t9h5sl3inf', '_vhash': 'i1102394cE', 'usr_login': '', 'hash': '8200264-85-250-1522780048-ae8dcfe4e7afc61d525fe8c289963b17', 'op': 'download1'}
        headers1 = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'vidup.tv',
            'Pragma': 'no-cache',
            'Referer': __sUrl.replace('.me','.tv'),
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
        }
       
        
        sHtmlContent = requests.post(__sUrl, headers=headers1, data=data).content
        '''
        sPattern= "var thief='(.+?)';"
        match=re.compile(sPattern).findall(sHtmlContent)

       
        return match[0]
            
      
def setUrl( sUrl):
    sId = __getIdFromUrl( sUrl )
    return( 'https://thevideo.me/embed-' + sId + '.html')
def setUrl_vidup( sUrl):
    sId = __getIdFromUrl( sUrl )
    return( 'https://vidup.me/embed-' + sId + '.html')
def getMediaLinkForGuest_vidup(__sUrl):
    

        stream_url = ''
        __sUrl=setUrl_vidup(__sUrl)

        sHtmlContent,cook = cloudflare.request(__sUrl)
        key = __getKey(sHtmlContent)
        
        getCode = 'http://vidup.me/jwv/' + key
        
        sHtmlContent2,cook = cloudflare.request(getCode)

        unPacked = cPacker().unpack(sHtmlContent2)
    
        oParser = cParser()
        

        
        


        sPattern='vt=(.+?)"'
        match=re.compile(sPattern).findall(unPacked)
        
        aResult = oParser.parse(unPacked, sPattern)
        
        if (aResult[0] == True):
            code = aResult[1][0]
            url=[]
            qua=[]
        
            sPattern =  "label: '([0-9]+)p', file: '([^']+)'"
            aResult = oParser.parse(sHtmlContent, sPattern)
            
            if (aResult[0]):
                for aEntry in aResult[1]:
                    url.append(aEntry[1])
                    qua.append(aEntry[0])
            else:
                sPattern = '"file":"([^"]+)","label":"([0-9]+)p"'
                aResult = oParser.parse(sHtmlContent, sPattern)
            
                if (aResult[0]):
                    for aEntry in aResult[1]:
                        url.append(aEntry[0])
                        qua.append(aEntry[1])            
                
            #Si une seule url
            if len(url) == 1:
                stream_url = url[0]
            #si plus de une
            elif len(url) > 1:
            #Afichage du tableau
                ret = VScreateDialogSelect(qua)
                if (ret > -1):
                    stream_url = url[ret]

        if (stream_url):
            return True, stream_url + '?direct=false&ua=1&vt=' + code
def getMediaLinkForGuest_vidlox(url):
        sHtmlContent,cook = cloudflare.request(url)
    
        
        sPattern =  '([^"]+\.mp4)'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            #initialisation des tableaux
            url=[]
            qua=["HD","SD"] #bidouille evite m3u8
            api_call = ''

            #Replissage des tableaux
            for i in aResult[1]:
                url.append(str(i))

            #Si une seule url
            if len(url) == 1:
                api_call = url[0]
            #si plus de une
            elif len(url) > 1:
                #Afichage du tableau
                ret = util.VScreateDialogSelect(qua)
                if (ret > -1):
                    api_call = url[ret]
  
        if (api_call):
            return True, api_call 

        return False, False
def getMediaLinkForGuest_vshare(url):

   
    import requests

 

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'vshare.eu',
        'Pragma': 'no-cache',
        'Referer': url,
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
    }
    xx=requests.get(url, headers=headers).content
    regex='type="hidden" name="fname" value="(.+?)"'
    fname=re.compile(regex).findall(xx)[0]
    regex='type="hidden" name="id" value="(.+?)"'
    id=re.compile(regex).findall(xx)[0]
    data={'fname':fname,
            'id':id,
            'method_free':'Proceed+to+video',
            'op':'download1',
            'referer':'',
            'usr_login':''}


    sHtmlContent = requests.post(url, headers=headers,data=data).content
    regex='source src="(.+?)"'
    match=re.compile(regex).findall(sHtmlContent)
    return match[0]
    

def getMediaLinkForGuest_thevid(url):
        import requests
        headers8 = {
        'User-Agent': UA
        
        }
        logging.warning('THVID')
        api_call = False
        my_url=setUrl(url)
        logging.warning(url)
        sHtmlContent = requests.get(url,headers=headers8, verify=False).content
        sHtmlContent3 = sHtmlContent
        maxboucle = 3
        while (maxboucle > 0):
            
            sHtmlContent3 = CheckCpacker(sHtmlContent3)
            #sHtmlContent3 = CheckJJDecoder(sHtmlContent3)           
            #sHtmlContent3 = CheckAADecoder(sHtmlContent3)
            
            maxboucle = maxboucle - 1   
         
        sHtmlContent = sHtmlContent3
        logging.warning(sHtmlContent)
        #fh = open('c:\\test.txt', "w")
        #fh.write(sHtmlContent)
        #fh.close()

        #LoadLinks(sHtmlContent)
        
        oParser = cParser()
        
        sPattern = "var thief='([^']+)';"
        aResult = oParser.parse(sHtmlContent, sPattern)
        logging.warning(aResult)
        if not (aResult[0]):
            return False , False
        key = aResult[1][0].replace('+','')
        
            
        sPattern = "'rc=[^<>]+?\/(.+?)'\.concat"
        aResult = oParser.parse(sHtmlContent, sPattern)
        logging.warning(aResult)
        if not (aResult[0]):
            return False , False
            
        ee = aResult[1][0]
            
        url2 = 'https://thevideo.me/' + ee + '/' + key
        logging.warning(url2)
        sHtmlContent2 = requests.get(url2,headers=headers8).content
         
        
        code = cPacker().unpack(sHtmlContent2)
        sPattern = '"vt=([^"]+)'
        r2 = re.search(sPattern,code)
        if not (r2):
            return False,False
            
        #Unlock url
        url1 = re.search(r'async src="([^"]+)">', sHtmlContent,re.DOTALL).group(1)

        logging.warning(url1)
        sHtmlContenttmp1 = requests.get(url1,headers=headers8).content

        
        sId = __getIdFromUrl( url )
        url2 = 'https://thevideo.website/api/slider/' + sId
 
        logging.warning(url2)
        
        sHtmlContenttmp2= requests.get(url2,headers=headers8).content

        url3 = re.search(r'"src":"([^"]+)"', sHtmlContenttmp2,re.DOTALL).group(1)
      
        logging.warning(url3)
   
        sHtmlContenttmp3 = requests.get(url3,headers=headers8).content
  
        
        xbmc.sleep(1000)
            
        sPattern = '{"file":"([^"]+)","label":"(.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        logging.warning(aResult)
        if (aResult[0] == True):
            #initialisation des tableaux
            url=[]
            qua=[]
        
            #Remplissage des tableaux
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))
                
            #Si  1 url
            if len(url) == 1:
                api_call = url[0]
            #Affichage du tableau
            elif len(url) > 1:
                ret = VScreateDialogSelect(qua)
                if (ret > -1):
                    api_call = url[ret]

        #xbmc.sleep(5000)
                    
        #api_call ='https://n4081.thevideo.me:8777/ivcgn7pgt23xu37wrbrovparhhdg6yozy42ehjynz3p3lxyt2da7ibbxyhzjgbcxf5vtsutqndvnbfcpxvelknwgfy3pbkml7ff3s2baxyzssn7o6rw66s2gcnlmzejg75pcbw2io7vdcqkg3o2ggpduysgsbybagh434jamjp3pc5gdvqc7tpfd7hxn4hdx5p2klae7mrjecghepspd6jezziuqi4xrfsbg5hldgqfirxevcaaurglqznpxivy5wndsnvedx4xokoonky77bi4mjzzq/v.mp4?direct=false&ua=1&vt=pw42hcaoyjkxkx3qfwd4gdyoc775sk55pq7sqsr7rsv4rp3qk4huxuitpwqolirqnsmcyomiwarevrb4mt4lgbouyzxvtx3z4i3it6m3gr4lke7tske5sljujqarhotsraukqq4nqwkzoqdqw5qo7zjmobw5vzwd6r5oudfvp3deh2xo3boy75pkrzybt2mftelbbbqcifmoezvqw3cqeanck5lmzhshcph2qtseoakvw26bscztw44didbp63qrmc56j3wu7kmg6bhpiidfstx57m'
        
        if (api_call):
            api_call = api_call + '?direct=false&ua=1&vt=' + r2.group(1)
            return True, api_call
            
        return False, False
        