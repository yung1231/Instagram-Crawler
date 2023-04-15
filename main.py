import os
import time
from tools.tools import get_proxy, getDriver, readConfig
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from i_crawler import ICrawler


if __name__=='__main__':
  config = readConfig()
  save_pth = config['conf']['save_pth']
  usernames = config['conf']['usernames'].split(',')
  print('save_pth: ', save_pth)
  print('usernames: ', usernames)

  # success_proxy_ips = get_proxy()
  # print('success_proxy_ips: ', success_proxy_ips)

  success_proxy_ips = list()
  driver = getDriver(success_proxy_ips)

  i = ICrawler(usernames, driver)
  i.startSearch()