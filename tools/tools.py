from proxyIp.proxy_ip import ProxiesIp
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
import configparser
from random import sample

def get_proxy():
  p = ProxiesIp()
  success_proxy_ips = p.run()

  return success_proxy_ips

def getDriver(proxy):
  print(f'\n\033[32;1m[+] Get Driver\033[0m')
  opts = ChromeOptions()
  if len(proxy)!=0:
    tar = sample(proxy, 1)[0]
    print('use ip: ', tar)
    opts.add_argument(f'--proxy-server={tar}')
  opts.add_argument("start-maximized")
  opts.add_argument("disable-infobars")
  opts.add_experimental_option("excludeSwitches", ["enable-automation"])
  opts.add_experimental_option('useAutomationExtension', False)
  ser = Service("./chromedriver.exe")
  driver = Chrome(service=ser, options=opts)

  stealth(driver,
          user_agent= 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
          languages= ["en-US", "en"],
          vendor=  "Google Inc.",
          platform=  "Win32",
          webgl_vendor=  "Intel Inc.",
          renderer=  "Intel Iris OpenGL Engine",
          fix_hairline= False,
          run_on_insecure_origins= False,
  )

  print('Window size: ', driver.get_window_size()) 

  return driver

def readConfig():
	print(f'\n\033[32;1m[+] Read Config\033[0m')
	config = configparser.ConfigParser()
	config.read('./config.cfg')

	return config