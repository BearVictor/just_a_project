import zipfile
import requests
import warnings
warnings.simplefilter("ignore")
from modules import *
from selenium import webdriver
from scraper_api import ScraperAPIClient

class MyResponse:
    def __init__(self, *, proxies=None, api=None):
        self.proxies = proxies
        self.api = api

    def get(self, url, *, timeout=45, stop=9, headers=None, cookies=None, sleep_times=None):
        func_name = inspect.stack()[0][3]
        retries = 0
        while retries < stop:
            try:
                user_agent = random_useragent()
                if headers is None:
                    headers = {
                        'User-Agent': user_agent,
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive',
                        'Pragma': 'no-cache',
                        'Upgrade-Insecure-Requests': '1',
                    }
                else:
                    headers['User-Agent'] = user_agent

                if sleep_times:
                    random_sec = random.choice(sleep_times)
                    print('[*] %s(sleep): %s' % (func_name, random_sec))
                    time.sleep(random_sec)

                kwargs = {'verify': False, 'headers': headers, 'timeout': timeout, }

                if self.proxies:
                    proxy = random.choice(self.proxies)
                    print(proxy)
                    kwargs['proxies'] = {"http": "http://" + proxy, "https": "http://" + proxy}

                if cookies:
                    kwargs['cookies'] = cookies

                response = requests.get(url, **kwargs)
                status = response.status_code
                if status in [200, 404, 500]:
                    print("[*] %s(%d): %s" % (func_name, status, url))
                    return response
                print("[*] %s(%d - retries%d): %s" % (func_name, status, retries, url))

            except requests.exceptions.Timeout:
                print("[*] %s(retries%d) Timeout %d: %s" % (func_name, retries, timeout, url))
            except requests.exceptions.TooManyRedirects:
                print("[*] %s(retries%d) TooManyRedirects: %s" % (func_name, retries, url))
            except requests.exceptions.RequestException:
                print("[*] %s(retries%d) RequestException: %s" % (func_name, retries, url))
            retries += 1

    def post(self, url, data, *, timeout=45, stop=9, headers=None, cookies=None, sleep_times=None):
        func_name = inspect.stack()[0][3]
        retries = 0
        while retries < stop:
            try:
                user_agent = random_useragent()
                if headers is None:
                    headers = {
                        'User-Agent': user_agent,
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive',
                        'Pragma': 'no-cache',
                        'Upgrade-Insecure-Requests': '1',
                    }
                else:
                    headers['User-Agent'] = user_agent

                if sleep_times:
                    random_sec = random.choice(sleep_times)
                    print('[*] %s(sleep): %s' % (func_name, random_sec))
                    time.sleep(random_sec)

                kwargs = {'verify': False, 'headers': headers, 'timeout': timeout, }

                if self.proxies:
                    proxy = random.choice(self.proxies)
                    print(proxy)
                    kwargs['proxies'] = {"http": "http://" + proxy, "https": "http://" + proxy}

                if cookies:
                    kwargs['cookies'] = cookies

                response = requests.post(url, data=data, **kwargs)
                status = response.status_code
                if status in [200, 404, 500]:
                    print("[*] %s(%d): %s" % (func_name, status, url))
                    return response
                print("%s(retries%d) %d: %s" % (func_name, retries, status, url))

            except requests.exceptions.Timeout:
                print("[*] %s(retries%d) Timeout %d: %s" % (func_name, retries, timeout, url))
            except requests.exceptions.TooManyRedirects:
                print("[*] %s(retries%d) TooManyRedirects: %s" % (func_name, retries, url))
            except requests.exceptions.RequestException:
                print("[*] %s(retries%d) RequestException: %s" % (func_name, retries, url))
            retries += 1

    def post_json(self, url, data, *, timeout=45, stop=9, headers=None, cookies=None, sleep_times=None):
        func_name = inspect.stack()[0][3]
        retries = 0
        while retries < stop:
            try:
                user_agent = random_useragent()
                if headers is None:
                    headers = {
                        'User-Agent': user_agent,
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive',
                        'Pragma': 'no-cache',
                        'Upgrade-Insecure-Requests': '1',
                    }
                else:
                    headers['User-Agent'] = user_agent

                if sleep_times:
                    random_sec = random.choice(sleep_times)
                    print('[*] %s(sleep): %s' % (func_name, random_sec))
                    time.sleep(random_sec)

                kwargs = {'verify': False, 'headers': headers, 'timeout': timeout, }

                if self.proxies:
                    proxy = random.choice(self.proxies)
                    print(proxy)
                    kwargs['proxies'] = {"http": "http://" + proxy, "https": "http://" + proxy}

                if cookies:
                    kwargs['cookies'] = cookies

                response = requests.post(url, json=data, **kwargs)
                status = response.status_code
                if status in [200, 404, 500]:
                    print("[*] %s(%d): %s" % (func_name, status, url))
                    return response
                print("%s(retries%d) %d: %s" % (func_name, retries, status, url))

            except requests.exceptions.Timeout:
                print("[*] %s(retries%d) Timeout %d: %s" % (func_name, retries, timeout, url))
            except requests.exceptions.TooManyRedirects:
                print("[*] %s(retries%d) TooManyRedirects: %s" % (func_name, retries, url))
            except requests.exceptions.RequestException:
                print("[*] %s(retries%d) RequestException: %s" % (func_name, retries, url))
            retries += 1

    def get_scraperapi(self, url, *, timeout=None, stop=9, headers=None, country_code=None):
        func_name = inspect.stack()[0][3]
        retries = 0
        while retries < stop:
            try:
                print(self.api)

                kwargs = {'url': url}
                if headers:
                    kwargs['headers'] = headers
                if timeout:
                    kwargs['timeout'] = timeout
                if country_code:
                    kwargs['country_code'] = country_code

                client = ScraperAPIClient(self.api)
                response = client.get(**kwargs)
                status = response.status_code
                if status in [200, 404, 500]:
                    print("[*] %s(%d): %s" % (func_name, status, url))
                    return response
                print("%s(retries%d) %d: %s" % (func_name, retries, status, url))

            except requests.exceptions.Timeout:
                print("[*] %s(retries%d) Timeout %d: %s" % (func_name, retries, timeout, url))
            except requests.exceptions.TooManyRedirects:
                print("[*] %s(retries%d) TooManyRedirects: %s" % (func_name, retries, url))
            except requests.exceptions.RequestException:
                print("[*] %s(retries%d) RequestException: %s" % (func_name, retries, url))
            retries += 1


class MyBrowser:
    def __init__(self, *, proxies=None):
        self.proxies = proxies
        self.width = 1920
        self.height = 1080

    def chrome(self, url, *, timeout=45, stop=9, headless=True, session_dir=None, download_dir=None, sleep_times=None):
        func_name = inspect.stack()[0][3]
        retries = 0
        while retries < stop:
            if sleep_times:
                random_sec = random.choice(sleep_times)
                print('[*] %s(sleep): %s' % (inspect.stack()[0][3], random_sec))
                time.sleep(random_sec)

            options = webdriver.ChromeOptions()
            options.add_argument("--window-size=%s,%s" % (self.width, self.height))
            options.add_argument(f'user-agent={random_chome_useragent()}')

            if headless:
                options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-gpu')

            proxy = ''
            if self.proxies:
                proxy = random.choice(self.proxies)
                print(proxy)
                options.add_argument('--proxy-server=%s' % proxy)

            if session_dir:
                create_dir(session_dir)
                if self.proxies:
                    options.add_argument("user-data-dir=%s/%s" % (session_dir, hash_name(random.choice(self.proxies))))
                else:
                    options.add_argument("user-data-dir=%s/%s" % (session_dir, "local"))

            if download_dir:
                create_dir(download_dir)
                prefs = {
                    "download.default_directory": download_dir,
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True,
                    "safebrowsing_for_trusted_sources_enabled": False,
                    "safebrowsing.enabled": False
                }
                options.add_experimental_option("prefs", prefs)

            kawargs = {'chrome_options': options}
            if os.path.exists('./chromedriver') and os.name != 'nt':
                kawargs['executable_path'] = "./chromedriver"
            if os.path.exists('./chromedriver.exe') and os.name == 'nt':
                kawargs['executable_path'] = "./chromedriver.exe"
            driver = webdriver.Chrome(**kawargs)
            driver.set_page_load_timeout(timeout)

            if download_dir and headless:
                create_dir(download_dir)
                driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
                params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
                driver.execute("send_command", params)

            try:
                driver.get(url)
                print('[*] %s(opened): %s' % (func_name, url))
                return driver
            except:
                print("%s\n [*] %s(retries%d%s): %s"
                      % (traceback.format_exc().strip(), func_name, retries, ' %s' % proxy, url))
            driver.quit()
            retries += 1

    def chrome_dowload_PDFViewer(self, url, *, timeout=45, stop=9, headless=True, session_dir=None, download_dir=None, sleep_times=None):
        func_name = inspect.stack()[0][3]
        retries = 0
        while retries < stop:
            if sleep_times:
                random_sec = random.choice(sleep_times)
                print('[*] %s(sleep): %s' % (inspect.stack()[0][3], random_sec))
                time.sleep(random_sec)

            options = webdriver.ChromeOptions()
            options.add_argument("--window-size=%s,%s" % (self.width, self.height))
            options.add_argument(f'user-agent={random_chome_useragent()}')

            if headless:
                options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-gpu')

            proxy = ''
            if self.proxies:
                proxy = random.choice(self.proxies)
                print(proxy)
                options.add_argument('--proxy-server=%s' % proxy)

            if session_dir:
                create_dir(session_dir)
                if self.proxies:
                    options.add_argument("user-data-dir=%s/%s" % (session_dir, hash_name(random.choice(self.proxies))))
                else:
                    options.add_argument("user-data-dir=%s/%s" % (session_dir, "local"))

            if download_dir:
                create_dir(download_dir)
                prefs = {
                    "plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],
                    "download.default_directory": download_dir, "download.extensions_to_open": "applications/pdf"
                }
                options.add_experimental_option("prefs", prefs)

            kawargs = {'chrome_options': options}
            if os.path.exists('./chromedriver') and os.name != 'nt':
                kawargs['executable_path'] = "./chromedriver"
            if os.path.exists('./chromedriver.exe') and os.name == 'nt':
                kawargs['executable_path'] = "./chromedriver.exe"
            driver = webdriver.Chrome(**kawargs)
            driver.set_page_load_timeout(timeout)

            if download_dir and headless:
                create_dir(download_dir)
                driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
                params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
                driver.execute("send_command", params)

            try:
                driver.get(url)
                print('[*] %s(opened): %s' % (func_name, url))
                return driver
            except:
                print("%s\n [*] %s(retries%d%s): %s"
                      % (traceback.format_exc().strip(), func_name, retries, ' %s' % proxy, url))
            driver.quit()
            retries += 1

    def chrome_auth(self, url, *, timeout=45, stop=9):
        func_name = inspect.stack()[0][3]
        retries = 0
        while retries < stop:
            print(self.proxies)
            proxy_host, proxy_post, proxy_user, proxy_pass = extract_host_port_user_pass(random.choice(self.proxies))
            manifest_json = """
            {
                "version": "1.0.0",
                "manifest_version": 2,
                "name": "Chrome Proxy",
                "permissions": [
                    "proxy",
                    "tabs",
                    "unlimitedStorage",
                    "storage",
                    "<all_urls>",
                    "webRequest",
                    "webRequestBlocking"
                ],
                "background": {
                    "scripts": ["background.js"]
                },
                "minimum_chrome_version":"22.0.0"
            }
            """

            background_js = """
            var config = {
                    mode: "fixed_servers",
                    rules: {
                    singleProxy: {
                        scheme: "http",
                        host: "%s",
                        port: parseInt(%s)
                    },
                    bypassList: ["localhost"]
                    }
                };
    
            chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
    
            function callbackFn(details) {
                return {
                    authCredentials: {
                        username: "%s",
                        password: "%s"
                    }
                };
            }
    
            chrome.webRequest.onAuthRequired.addListener(
                        callbackFn,
                        {urls: ["<all_urls>"]},
                        ['blocking']
            );
            """ % (proxy_host, proxy_post, proxy_user, proxy_pass)

            options = webdriver.ChromeOptions()
            pluginfile = 'proxy_auth_plugin.zip'
            with zipfile.ZipFile(pluginfile, 'w') as zp:
                zp.writestr("manifest.json", manifest_json)
                zp.writestr("background.js", background_js)
            options.add_extension(pluginfile)
            options.add_argument(f'user-agent={random_chome_useragent()}')
            path = os.path.dirname(os.path.abspath(__file__))
            driver = webdriver.Chrome(os.path.join(path, 'chromedriver'), options=options)
            driver.set_page_load_timeout(timeout)

            try:
                driver.get(url)
                print('[*] %s(opened): %s' % (func_name, url))
                return driver
            except:
                print(traceback.format_exc())
            driver.quit()
            retries += 1

    def firefox(self, url, *, timeout=45, stop=9, headless=True):
        func_name = inspect.stack()[0][3]
        retries = 0
        while retries < stop:
            kwargs = {}
            profile = webdriver.FirefoxProfile()
            profile.set_preference("general.useragent.override", random_firefox_useragent())

            options = webdriver.FirefoxOptions()
            if headless:
                options.add_argument("--headless")

            proxy = ''
            if self.proxies:
                proxy = random.choice(self.proxies)
                print(proxy)
                capabilities = webdriver.DesiredCapabilities.FIREFOX
                capabilities['proxy'] = {"proxyType": "MANUAL", "httpProxy": proxy, "ftpProxy": proxy, "sslProxy": proxy}
                kwargs['capabilities'] = capabilities

            kwargs['firefox_profile'] = profile
            kwargs['options'] = options
            if os.path.exists('./geckodriver') and os.name != 'nt':
                kwargs['executable_path'] = './geckodriver'
            if os.path.exists('./geckodriver.exe') and os.name == 'nt':
                kwargs['executable_path'] = './geckodriver.exe'
            driver = webdriver.Firefox(**kwargs)
            driver.set_page_load_timeout(timeout)
            driver.set_window_size(self.width, self.height)
            try:
                driver.get(url)
                print('[*] %s(opened): %s' % (func_name, url))
                return driver
            except:
                print("%s\n [*] %s(retries%d%s): %s"
                      % (traceback.format_exc().strip(), func_name, retries, ' %s' % proxy, url))
            driver.quit()
            retries += 1

    def firefox_luminati(self, url, *, timeout=45, stop=9, headless=True):
        func_name = inspect.stack()[0][3]
        retries = 0
        while retries < stop:
            kwargs = {}
            profile = webdriver.FirefoxProfile()
            profile.set_preference("general.useragent.override", random_firefox_useragent())

            options = webdriver.FirefoxOptions()
            if headless:
                options.add_argument("--headless")

            proxy = ''
            if self.proxies:
                proxy = random.choice(self.proxies)
                print(proxy)
                capabilities = webdriver.DesiredCapabilities.FIREFOX
                capabilities['proxy'] = {
                    "proxyType": "MANUAL",
                    "httpProxy": proxy,
                    "ftpProxy": proxy,
                    "sslProxy": proxy,
                    "socksVersion": 4
                }
                kwargs['capabilities'] = capabilities

            kwargs['firefox_profile'] = profile
            kwargs['options'] = options
            if os.path.exists('./geckodriver') and os.name != 'nt':
                kwargs['executable_path'] = './geckodriver'
            if os.path.exists('./geckodriver.exe') and os.name == 'nt':
                kwargs['executable_path'] = './geckodriver.exe'
            driver = webdriver.Firefox(**kwargs)
            driver.set_page_load_timeout(timeout)
            driver.set_window_size(self.width, self.height)
            try:
                driver.get(url)
                print('[*] %s(opened): %s' % (func_name, url))
                return driver
            except:
                print("%s\n [*] %s(retries%d%s): %s"
                      % (traceback.format_exc().strip(), func_name, retries, ' %s' % proxy, url))
            driver.quit()
            retries += 1

    def firefox_pdf(self, url, *, timeout=45, stop=9, headless=True, download_dir=None):
        func_name = inspect.stack()[0][3]
        retries = 0
        while retries < stop:
            kwargs = {}
            profile = webdriver.FirefoxProfile()

            if download_dir:
                create_dir(download_dir)
                profile.set_preference("general.useragent.override", random_firefox_useragent())
                profile.set_preference("browser.download.folderList", 2)
                profile.set_preference("browser.download.manager.showWhenStarting", False)
                profile.set_preference("browser.download.dir", download_dir)
                profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")

                profile.set_preference("pdfjs.disabled", True)
                profile.set_preference("plugin.scan.Acrobat", "99.0")
                profile.set_preference("plugin.scan.plid.all", False)

            options = webdriver.FirefoxOptions()
            if headless:
                options.add_argument("--headless")

            proxy = ''
            if self.proxies:
                proxy = random.choice(self.proxies)
                print(proxy)
                capabilities = webdriver.DesiredCapabilities.FIREFOX
                capabilities['proxy'] = {"proxyType": "MANUAL", "httpProxy": proxy, "ftpProxy": proxy, "sslProxy": proxy}
                kwargs['capabilities'] = capabilities

            kwargs['firefox_profile'] = profile
            kwargs['options'] = options
            if os.path.exists('./geckodriver') and os.name != 'nt':
                kwargs['executable_path'] = './geckodriver'
            if os.path.exists('./geckodriver.exe') and os.name == 'nt':
                kwargs['executable_path'] = './geckodriver.exe'


            driver = webdriver.Firefox(**kwargs)
            driver.set_page_load_timeout(timeout)
            driver.set_window_size(self.width, self.height)
            try:
                driver.get(url)
                print('[*] %s(opened): %s' % (func_name, url))
                return driver
            except:
                print("%s\n [*] %s(retries%d%s): %s"
                      % (traceback.format_exc().strip(), func_name, retries, ' %s' % proxy, url))
            driver.quit()
            retries += 1

    def phantomjs(self, url, *, timeout=45, stop=9):
        func_name = inspect.stack()[0][3]
        retries = 0
        while retries < stop:
            kwargs = {}
            capabilities = webdriver.DesiredCapabilities.PHANTOMJS
            capabilities["phantomjs.page.settings.userAgent"] = random_useragent()
            kwargs['desired_capabilities'] = capabilities

            proxy = ''
            if self.proxies:
                proxy = random.choice(self.proxies)
                print(proxy)
                if '@' in proxy:
                    proxy_host, proxy_post, proxy_user, proxy_pass = extract_host_port_user_pass(proxy)
                    service_args = [
                        '--proxy=http://{}:{}'.format(proxy_host, proxy_post),
                        '--proxy-type=http',
                        '--proxy-auth={}:{}'.format(proxy_user, proxy_pass)
                    ]
                else:
                    service_args = [
                        '--proxy=http://{}'.format(proxy),
                        '--proxy-type=http',
                    ]
                kwargs['service_args'] = service_args

            driver = webdriver.PhantomJS(**kwargs)
            driver.set_page_load_timeout(timeout)
            driver.set_window_size(self.width, self.height)
            try:
                driver.get(url)
                print('[*] %s(opened): %s' % (func_name, url))
                return driver
            except:
                print("%s\n [*] %s(retries%d%s): %s"
                      % (traceback.format_exc().strip(), func_name, retries, ' %s' % proxy, url))
            driver.quit()
            retries += 1


if __name__ == "__main__":
    print('test...')


