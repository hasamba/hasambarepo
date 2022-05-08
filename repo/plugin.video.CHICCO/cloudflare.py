# -*- coding: utf-8 -*-

'''
    Genesis Add-on
    Copyright (C) 2015 lambda

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import re,urllib,urlparse,time
import cache,logging,requests
import xbmcaddon, xbmc, xbmcplugin, xbmcgui


user_agent ='Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'

def request(url, post=None, headers=None, mobile=False, safe=False, timeout=30):
    #try:
        user_agent ='Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
        headers = {'User-Agent': user_agent}
      
        import cfscrape
        
        try:
          tokens, user_agent = cache.get(cfscrape.get_tokens,3,url,timeout, table='cookies')
        except Exception as e:
          
       
          try:
            result = requests.get(url,headers=headers,timeout=timeout)
          except:
            return ' ','OK'
          
          return result.content,'ok'
        headers = {'User-Agent': user_agent}

        result = requests.get(url,headers=headers,cookies=tokens,timeout=timeout)
        if post!=None:
          result = requests.post(url,headers=headers,cookies=tokens,data=post)
       
        if 'jschl-answer' in result.content:
            
            tokens, user_agent = cache.get(cfscrape.get_tokens,0,url,timeout, table='cookies')
            headers = {'User-Agent': user_agent}
            result = requests.get(url,headers=headers,cookies=tokens,timeout=timeout)
            if post!=None:
              result = requests.post(url,headers=headers,cookies=tokens,data=post)

        #scraper = cfscrape.create_scraper()
        #r = scraper.get(url).content
        content=[]
        content.append(tokens)
        content.append(headers)
        return result.content,content
        if headers is None:
            headers = {'User-Agent': userAgent}
        else:
            headers['User-Agent'] = userAgent
        u = '%s://%s' % (urlparse.urlparse(url).scheme, urlparse.urlparse(url).netloc)
        #cookie = cache.get(cloudflare, 3, u, post, {'User-Agent': userAgent}, mobile, safe, timeout, table='cookies')
        cookie = cloudflare( u, post, {'User-Agent': userAgent}, mobile, safe, timeout)
        result = client.request(url, cookie=cookie, post=post, headers=headers, mobile=mobile, safe=safe, timeout=timeout, output='response', error=True)
        
        if 'HTTP Error 503' in result[0]:
            cookie = cache.get(cloudflare, 0, u, post, {'User-Agent': userAgent}, mobile, safe, timeout, table='cookies')
            #cookie = cloudflare( u, post, {'User-Agent': userAgent}, mobile, safe, timeout)

            cookies={'__cfduid':cookie.split('=')[1],
                     'cf_clearance':'4b092a6ad0892d7c71bb89e1d2287798fc82c67f-1523195257-3600'}
            #result=requests.get(url,headers=headers,cookies=cookies).content
            result = client.request(url, cookie=cookies, post=post, headers=headers, mobile=mobile, safe=safe, timeout=timeout)
     
        else:
            result= result[1]

        return result, cookie
    #except:
    #    return


def source(url, post=None, headers=None, mobile=False, safe=False, timeout='60'):
    result, cookie = request(url, post, headers, mobile, safe, timeout)
    return result


def cloudflare(url, post, headers, mobile, safe, timeout):
    #try:
        result = client.request(url, post=post, headers=headers, mobile=mobile, safe=safe, timeout=timeout, error=True)

        jschl = re.compile('name="jschl_vc" value="(.+?)"/>').findall(result)[0]
        init = re.compile('setTimeout\(function\(\){\s*.*?.*:(.*?)};').findall(result)[0]
        builder = re.compile(r"challenge-form\'\);\s*(.*)a.v").findall(result)[0]
        decryptVal = parseJSString(init)
        lines = builder.split(';')

        
        for line in lines:
            if len(line)>0 and '=' in line:
                sections=line.split('=')
                line_val = parseJSString(sections[1])
                decryptVal = int(eval(str(decryptVal)+sections[0][-1]+str(line_val)))

        answer = decryptVal + len(urlparse.urlparse(url).netloc)

        query = '%s/cdn-cgi/l/chk_jschl?jschl_vc=%s&jschl_answer=%s' % (url, jschl, answer)

        if 'type="hidden" name="pass"' in result:
            passval = re.compile('name="pass" value="(.*?)"').findall(result)[0]
            query = '%s/cdn-cgi/l/chk_jschl?pass=%s&jschl_vc=%s&jschl_answer=%s' % (url, urllib.quote_plus(passval), jschl, answer)
            time.sleep(5)
        
        cookie = client.request(query, post=post, headers=headers, mobile=mobile, safe=safe, timeout=timeout, output='cookie', error=True)
  

        
        return cookie
    #except:
    #    pass


def parseJSString(s):
    #try:
        offset=1 if s[0]=='+' else 0
        val = int(eval(s.replace('!+[]','1').replace('!![]','1').replace('[]','0')[offset:]))
        return val
    #except:
    #    pass

