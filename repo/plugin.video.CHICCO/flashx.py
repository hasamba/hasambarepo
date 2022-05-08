#coding: utf-8
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#


import re,urllib2,urllib
import logging
from general_func import cPacker,cParser


class cRequestHandler:
    REQUEST_TYPE_GET = 0
    REQUEST_TYPE_POST = 1
      
    def __init__(self, sUrl):
        self.__sUrl = sUrl
        self.__sRealUrl = ''
        self.__cType = 0
        self.__aParamaters = {}
        self.__aParamatersLine = ''
        self.__aHeaderEntries = []
        self.removeBreakLines(True)
        self.removeNewLines(True)
        self.__setDefaultHeader()
        self.__timeout = 30
        self.__bRemoveNewLines = False
        self.__bRemoveBreakLines = False
        self.__sResponseHeader = ''

    def removeNewLines(self, bRemoveNewLines):
        self.__bRemoveNewLines = bRemoveNewLines

    def removeBreakLines(self, bRemoveBreakLines):
        self.__bRemoveBreakLines = bRemoveBreakLines

    def setRequestType(self, cType):
        self.__cType = cType
        
    def setTimeout(self, valeur):
        self.__timeout = valeur    

    def addHeaderEntry(self, sHeaderKey, sHeaderValue):
        for sublist in self.__aHeaderEntries:
            if sHeaderKey in sublist:
                self.__aHeaderEntries.remove(sublist)
        aHeader = {sHeaderKey : sHeaderValue}
        self.__aHeaderEntries.append(aHeader)

    def addParameters(self, sParameterKey, mParameterValue):
        self.__aParamaters[sParameterKey] = mParameterValue
        
    def addParametersLine(self, mParameterValue):
        self.__aParamatersLine = mParameterValue
        
    #egg addMultipartFiled('sess_id':sId,'upload_type':'url','srv_tmp_url':sTmp)
    def addMultipartFiled(self,fields ):
        mpartdata = MPencode(fields)
        self.__aParamaters = mpartdata[1]
        self.addHeaderEntry('Content-Type', mpartdata[0] )
        self.addHeaderEntry('Content-Length', len(mpartdata[1]))

    #Je sais plus si elle gere les doublons
    def getResponseHeader(self):
        return self.__sResponseHeader
        
    # url after redirects
    def getRealUrl(self):
        return self.__sRealUrl
        
    def GetCookies(self):
        if 'Set-Cookie' in self.__sResponseHeader:
            import re
            
            #cookie_string = self.__sResponseHeader.getheaders('set-cookie')
            #c = ''
            #for i in cookie_string:
            #    c = c + i + ', '
            c = self.__sResponseHeader.getheader('set-cookie')
            
            c2 = re.findall('(?:^|,) *([^;,]+?)=([^;,\/]+?);',c)
            if c2:
                cookies = ''
                for cook in c2:
                    cookies = cookies + cook[0] + '=' + cook[1]+ ';'
                return cookies
        return ''

    def request(self):
        self.__sUrl = self.__sUrl.replace(' ', '+')
        return self.__callRequest()

    def getRequestUri(self):
        return self.__sUrl + '?' + urllib.urlencode(self.__aParamaters)

    def __setDefaultHeader(self):
        self.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0')
        self.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        self.addHeaderEntry('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7')

    def __callRequest(self):
        if self.__aParamatersLine:
            sParameters = self.__aParamatersLine
        else:
            sParameters = urllib.urlencode(self.__aParamaters)

        if (self.__cType == cRequestHandler.REQUEST_TYPE_GET):
            if (len(sParameters) > 0):
                if (self.__sUrl.find('?') == -1):
                    self.__sUrl = self.__sUrl + '?' + str(sParameters)
                    sParameters = ''
                else:
                    self.__sUrl = self.__sUrl + '&' + str(sParameters)
                    sParameters = ''

        if (len(sParameters) > 0):
            oRequest = urllib2.Request(self.__sUrl, sParameters)
        else:
            oRequest = urllib2.Request(self.__sUrl)

        for aHeader in self.__aHeaderEntries:
            for sHeaderKey, sHeaderValue in aHeader.items():
                oRequest.add_header(sHeaderKey, sHeaderValue)

        sContent = ''
        try:
            oResponse = urllib2.urlopen(oRequest, timeout = self.__timeout)
            sContent = oResponse.read()
            
            self.__sResponseHeader = oResponse.info()
            
            #compressed page ?
            if self.__sResponseHeader.get('Content-Encoding') == 'gzip':
                import zlib
                sContent = zlib.decompress(sContent, zlib.MAX_WBITS|16)
            
            #https://bugs.python.org/issue4773
            self.__sRealUrl = oResponse.geturl()
            self.__sResponseHeader = oResponse.info()
        
            oResponse.close()
            
        except urllib2.HTTPError, e:
            if e.code == 503:
                
                #Protected by cloudFlare ?
                from resources.lib import cloudflare
                if cloudflare.CheckIfActive(e.read()):
 
                    cookies = self.GetCookies()

                    print 'Page protegee par cloudflare'
                    CF = cloudflare.CloudflareBypass()
                    sContent = CF.GetHtml(self.__sUrl,e.read(),cookies,sParameters,oRequest.headers)
                    self.__sRealUrl,self.__sResponseHeader = CF.GetReponseInfo()

            if not sContent:
                cConfig().error("%s (%d),%s" % (cConfig().getlanguage(30205), e.code , self.__sUrl))
                return ''
                
        except urllib2.URLError, e:
            cConfig().log(e.reason)
            cConfig().error("%s (%s),%s" % (cConfig().getlanguage(30205), e.reason , self.__sUrl))
            return ''           
        
        if (self.__bRemoveNewLines == True):
            sContent = sContent.replace("\n","")
            sContent = sContent.replace("\r\t","")

        if (self.__bRemoveBreakLines == True):
            sContent = sContent.replace("&nbsp;","")

        return sContent

    def getHeaderLocationUrl(self):        
        opened = urllib.urlopen(self.__sUrl)
        return opened.geturl()


class iHoster:

    def getDisplayName(self):
        raise NotImplementedError()

    def setDisplayName(self, sDisplayName):
        raise NotImplementedError()

    def setFileName(self, sFileName):
	raise NotImplementedError()

    def getFileName(self):
	raise NotImplementedError()

    def getPluginIdentifier(self):
        raise NotImplementedError()

    def isDownloadable(self):
        raise NotImplementedError()

    def isJDownloaderable(self):
        raise NotImplementedError()

    def getPattern(self):
        raise NotImplementedError()

    def setUrl(self, sUrl):
        raise NotImplementedError()

    def checkUrl(self, sUrl):
        raise NotImplementedError()

    def getUrl(self):
        raise NotImplementedError()

    def getMediaLink(self):
        raise NotImplementedError()
#Remarque : meme code que vodlocker

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
#UA = 'Nokia7250/1.0 (3.14) Profile/MIDP-1.0 Configuration/CLDC-1.0'

def ASCIIDecode(string):
    
    i = 0
    l = len(string)
    ret = ''
    while i < l:
        c =string[i]
        if string[i:(i+2)] == '\\x':
            c = chr(int(string[(i+2):(i+4)],16))
            i+=3
        if string[i:(i+2)] == '\\u':
            cc = int(string[(i+2):(i+6)],16)
            if cc > 256:
                #ok c'est de l'unicode, pas du ascii
                return ''
            c = chr(cc)
            i+=5
        ret = ret + c
        i = i + 1

    return ret

def GetHtml(url,headers):
    request = urllib2.Request(url,None,headers)
    reponse = urllib2.urlopen(request)
    sCode = reponse.read()
    reponse.close()
    
    return sCode

def UnlockUrl(url2=None):
    headers9 = {
    'User-Agent': UA,
    'Referer':'https://www.flashx.ws/dl?playthis'
    }
    
    url1 = 'https://www.flashx.ws/js/code.js'
    if url2:
        url1 = url2
        
    if not url1.startswith('http'):
        url1 = 'https:' + url1


    
    oRequest = cRequestHandler(url1)
    oRequest.addParameters('User-Agent', UA)
    
    #oRequest.addParameters('Accept', '*/*')
    #oRequest.addParameters('Accept-Encoding', 'gzip, deflate, br')
    #oRequest.addParameters('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequest.addParameters('Referer','https://www.flashx.ws/dl?playthis')
    code = oRequest.request()
    
    url = ''
    if not code:
        url = oRequest.getRealUrl()
  
    else:
        #logging.warning(code)
        aResult = re.search("!= null\){\s*\$.get\('([^']+)', *{(.+?)}", code, re.DOTALL)
        if aResult:
            dat = aResult.group(2)
            dat = dat.replace("'",'')
            dat = dat.replace(" ",'')

            dat2 = dict(x.split(':') for x in dat.split(','))

            dat3 = aResult.group(1) + '?'
            for i,j in dat2.items():
                dat3 = dat3 + str(i)+ '=' + str(j) + '&'
            
            url = dat3[:-1]
            
    #url = 'https://www.flashx.tv/flashx.php?fxfx=6'
    
    if url:
        logging.warning('Good Url :' + url1)
        logging.warning(url)
        GetHtml(url,headers9)
        return True
        
    logging.warning('Bad Url :' + url1)
        
    return False

def LoadLinks(htmlcode):

    
        host = 'https://www.flashx.tv'
        sPattern ='[\("\'](https*:)*(\/[^,"\'\)\s]+)[\)\'"]'
        aResult = re.findall(sPattern, htmlcode, re.DOTALL)

       
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
                sUrl = host + sUrl
            
            #Url ou il ne faut pas aller
            if 'dok3v' in sUrl:
                continue
                
            #pour test
            if ('.js' not in sUrl) or ('.cgi' not in sUrl):
                continue
            #if 'flashx' in sUrl:
                #continue

            headers8 = {
            'User-Agent': UA,
            'Referer':'https://www.flashx.tv/dl?playthis'
            }
            
            try:
                request = urllib2.Request(sUrl,None,headers8)
                reponse = urllib2.urlopen(request)
                sCode = reponse.read()
                reponse.close()
                #logging.warning('Worked ' + sUrl)
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
                        #logging.warning('Worked ' + sUrl)
                    except urllib2.HTTPError, e:
                       
                        logging.warning('Redirection Blocked ' + sUrl + ' Red ' + e.geturl())
                        pass
                
                
        
        

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'FlashX'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR] [COLOR khaki]' + self.__sHD + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'flashx'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''

    



    def setUrl(self, sUrl):
        self.__sUrl = 'http://' + self.GetHost(sUrl) + '/embed.php?c=' + self.__getIdFromUrl(sUrl)

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return ''

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def CheckGoodUrl(self,url):
        
      
        headers = {'User-Agent': UA
                   #'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   #'Accept-Language':'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
                   #'Accept-Encoding':'gzip, deflate, br',
                   #'Host':'openload.co',
                   #'Referer':referer
        }

        req = urllib2.Request(url)#,None,headers)
        res = urllib2.urlopen(req)
        #pour afficher contenu
    
        #pour afficher header
       
        #Pour afficher redirection

        
        if 'embed' is res.geturl():
            return false
            
        html = res.read()
        
        res.close()

        return res
def GetRedirectHtml(web_url,sId,NoEmbed = False):
        
        headers = {
        #'Host' : 'www.flashx.tv',
        'User-Agent': UA,
        #'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        #'Accept-Language':'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer':'http://embed.flashx.tv/embed.php?c=' + sId,
        'Accept-Encoding':'identity'
        }
        
        MaxRedirection = 3
        while MaxRedirection > 0:
            
            #generation headers
            #headers2 = headers
            #headers2['Host'] = self.GetHost(web_url)
            
          
            request = urllib2.Request(web_url,None,headers)
      
            redirection_target = web_url
        
            try:
                #ok ca a enfin marche
                reponse = urllib2.urlopen(request)
                sHtmlContent = reponse.read()
                reponse.close()

                if not (reponse.geturl() == web_url) and not (reponse.geturl() == ''):
                    redirection_target = reponse.geturl()
                else:
                    break
            except urllib2.URLError, e:
                if (e.code == 301) or  (e.code == 302):
                    redirection_target = e.headers['Location']
                else:
                    #logging.warning(str(e.code))
                    #logging.warning(str(e.read()))
                    return False
                
            web_url = redirection_target
            
            if 'embed' in redirection_target and NoEmbed:
                #rattage, on a pris la mauvaise url
                logging.warning('2')
                return False
            
            MaxRedirection = MaxRedirection - 1
            
        return sHtmlContent
def __getIdFromUrl( sUrl):
    sPattern = "https*:\/\/((?:www.|play.)?flashx.tv)\/(?:playvid-)?(?:embed-)?(?:embed.+?=)?(-*[0-9a-zA-Z]+)?(?:.html)?"
    oParser = cParser()
    aResult = oParser.parse(sUrl, sPattern)
    if (aResult[0] == True):
        return aResult[1][0][1]

    return ''

def GetHost(sUrl):
    oParser = cParser()
    sPattern = 'https*:\/\/(.+?)\/'
    aResult = oParser.parse(sUrl, sPattern)
    if aResult[0]:
        return aResult[1][0]
    return ''
def __getMediaLinkForGuest(__sUrl):
        
        oParser = cParser()
        
        #on recupere le host atuel
        HOST = GetHost(__sUrl)
 
        #on recupere l'ID
        sId = __getIdFromUrl(__sUrl)
        if sId == '':
            logging.warning("Id prb")
            return False,False
        
        #on ne garde que les chiffres
        #sId = re.sub(r'-.+', '', sId)
        
        #on cherche la vraie url
        sHtmlContent = GetRedirectHtml(__sUrl, sId)
        
        #fh = open('c:\\test.txt', "w")
        #fh.write(sHtmlContent)
        #fh.close()

        sPattern = 'href=["\'](https*:\/\/www\.flashx[^"\']+)'
        AllUrl = re.findall(sPattern,sHtmlContent,re.DOTALL)
        logging.warning(str(AllUrl))

        #Disabled for the moment
        if (False):
            if AllUrl:
                # Need to find which one is the good link
                # Use the len don't work
                for i in AllUrl:
                    if i[0] == '':
                        web_url = i[1]
            else:
                return False,False
        else:
            web_url = AllUrl[0]
            
        web_url = AllUrl[0]
        
        #Requests to unlock video
        #unlock fake video
        LoadLinks(sHtmlContent)
        #unlock bubble
        unlock = False
        url2 = re.findall('["\']([^"\']+?\.js\?cache.+?)["\']', sHtmlContent, re.DOTALL)
        if not url2:
            logging.warning('No special unlock url find')
        for i in url2:
            unlock = UnlockUrl(i)
            if unlock:
                break
                
        if not unlock:
            logging.warning('No special unlock url working')
            return False,False
               
        #get the page
        sHtmlContent = GetRedirectHtml(web_url, sId, True)
        
        if sHtmlContent == False:
            logging.warning('Passage en mode barbare')
            #ok ca a rate on passe toutes les url de AllUrl
            for i in AllUrl:
                if not i == web_url:
                    sHtmlContent = GetRedirectHtml(i, sId, True)
                    if sHtmlContent:
                        break

        if not sHtmlContent:
            return False,False

        #fh = open('c:\\test2.txt', "w")
        #fh.write(sHtmlContent)
        #fh.close()
        
        logging.warning('Page obtenue')

        if 'reload the page!' in sHtmlContent:
            logging.warning("page bloquée")
            
            #On recupere la bonne url
            sGoodUrl = web_url

            #on recupere la page de refresh
            sPattern = 'reload the page! <a href="([^"]+)">!! <b>'
            aResult = re.findall(sPattern,sHtmlContent)
            if not aResult:
                return False,False
            sRefresh = aResult[0]
            
            #on recupere le script de debloquage
            sPattern = '<script async class.+?src="([^"]+)"><\/script>'
            aResult = re.findall(sPattern,sHtmlContent)
            if not aResult:
                return False,False
            
            #on debloque la page (en test ca a l'air inutile)
            sHtmlContent = GetRedirectHtml(aResult[0],sId)
            
            #lien speciaux ?
            if sRefresh.startswith('./'):
                sRefresh = 'http://' + GetHost(sGoodUrl) + sRefresh[1:]
            
            #on rafraichit la page
            sHtmlContent = GetRedirectHtml(sRefresh,sId)
            
            #et on re-recupere la page
            sHtmlContent = GetRedirectHtml(sGoodUrl,sId)
            
        if (False):
         
            #A t on le lien code directement?
            sPattern = "(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>"
            aResult = re.findall(sPattern,sHtmlContent)
                    
            if (aResult):
                logging.warning( "lien code")
                
                AllPacked = re.findall('(eval\(function\(p,a,c,k.*?)\s+<\/script>', sHtmlContent, re.DOTALL)
                if AllPacked:
                    for i in AllPacked:
                        sUnpacked = cPacker().unpack(i)
                        sHtmlContent = sUnpacked
                       
                        if "file" in sHtmlContent:
                            break
                else:
                    return False,False
  
        #decodage classique
        sPattern = '{file:"([^",]+)",label:"([^"<>,]+)"}'
        sPattern = '{src: *\'([^"\',]+)\'.+?label: *\'([^"<>,\']+)\''
        aResult = oParser.parse(sHtmlContent, sPattern)

        api_call = ''
        
     

        if (aResult[0] == True):
            #initialisation des tableaux
            url=[]
            qua=[]
        
            #Remplissage des tableaux
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))
                
            #Si une seule url
            if len(url) == 1:
                api_call = url[0]
            #si plus de une
            elif len(url) > 1:
            #Affichage du tableau
                
                 api_call = url[0]

        #print api_call
        
        if (api_call):
            return True, api_call
            
        return False, False
