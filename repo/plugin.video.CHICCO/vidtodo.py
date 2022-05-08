# -*- coding: utf-8 -*-
import  time
import re,logging,requests
from flashx import cRequestHandler
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

def VidToDoResolver(web_url,c_head=None):
        UA = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0"
        headers8 = {
        'User-Agent': UA
        #'Referer':'https://www.flashx.tv/dl?playthis'
        }

        
        api_call = ''
        if c_head!=None:
          logging.warning(c_head)
          sHtmlContent =requests.get(web_url,headers=c_head).content
        else:
          sHtmlContent = requests.get(web_url,headers=headers8).content
        #logging.warning(sHtmlContent)
        oParser = cParser()

  
        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        logging.warning(aResult)
        if (aResult[0] == True):
            sHtmlContent = cPacker().unpack(aResult[1][0])

            sPattern = '{file: *"([^"]+smil)"}'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                api_call = self.extractSmil(aResult[1][0])
            else:
                sPattern = '{file: *xpro\("(.+?)"'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if (aResult[0] == True):
                    api_call = aResult[1][0].decode('rot13')

  
        if (api_call):
            return True, api_call
            
        return False, False
def __get_vidto(__sUrl):

        oRequest = cRequestHandler(__sUrl)
        sHtmlContent = oRequest.request()

        sPattern =  '<input type="hidden" name="([^"]+)" value="([^"]+)"'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        
        if (aResult[0] == True):
            time.sleep(7)
            oRequest = cRequestHandler(__sUrl)
            oRequest.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
            for aEntry in aResult[1]:
                oRequest.addParameters(aEntry[0], aEntry[1])

            oRequest.addParameters('referer', __sUrl)
            sHtmlContent = oRequest.request()
            sHtmlContent = sHtmlContent.replace('file:""','')
            
            sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                sHtmlContent = cPacker().unpack(aResult[1][0])
                sPattern =  ',file:"([^"]+)"}'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if (aResult[0] == True):
                    return True, aResult[1][0]
            else:
                sPattern = '{file:"([^"]+)",label:"(\d+p)"}'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if (aResult[0] == True):
                    url=[]
                    qua=[]
                for i in aResult[1]:
                    url.append(str(i[0]))
                    qua.append(str(i[1]))
      
                if len(url) == 1:
                    return True,url[0]

                elif len(url) > 1:
                    return True, url[0] #240p de nos jours serieux dialog choix inutile max vue 360p pour le moment

        return False, False
def get_thevid(url): 
        headers = {
        'Pragma': 'no-cache',
        'Accept-Encoding': 'utf-8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        }   
        sHtmlContent,cook = requests.get(url,headers=headers).content
        
        oParser = cParser()
              
        #Dean Edwards Packer
        sPattern = "(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            sUnpacked = cPacker().unpack(aResult[1][0])
        
        #fh = open('c:\\test.txt', "w")
        #fh.write(sUnpacked)
        #fh.close()
        
        if (sUnpacked):

            sPattern ='var vurl2 *= *"([^"]+?)";'
            aResult = oParser.parse(sUnpacked, sPattern)
            
            #print aResult
            
            if (aResult[0] == True):
                return True , aResult[1][0]
        
        cGui().showInfo(self.__sDisplayName, 'Fichier introuvable' , 5)
        
        return False, False