import os
import time
import requests
from selenium.webdriver.common.by import By
import concurrent.futures
import getpass
import json

class ICrawler:
  def __init__(self, usernames, driver):
    print(f'\n\033[32;1m[+] Start Instagram Crawler\033[0m')
    self.usernames = usernames
    self.driver = driver
    self.url = 'https://www.instagram.com/' 
    self.cookies = './cookies.json'
    

  def login(self):
    print(f'\n\033[32;1m[+] Login\033[0m')
    self.driver.get(self.url) 
    time.sleep(5)

    username_input = self.driver.find_elements(By.NAME, 'username')[0]
    password_input = self.driver.find_elements(By.NAME, 'password')[0]
    u = input("Your IG Account: ")
    p = getpass.getpass(prompt="Your IG password: ")
    username_input.send_keys(u)
    password_input.send_keys(p)
    login_click = self.driver.find_elements(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button[1]')[0]
    login_click.click() # login_click.send_keys(Keys.ENTER)
    time.sleep(5)

    # second_div = self.driver.find_elements(By.XPATH, '//body/div[2]')[0]
    # div_id = second_div.get_attribute("id")
    # print('div_id: ', div_id)

    store_click = self.driver.find_elements(By.XPATH, "//div[@role='button']")[0]
    store_click.click()
    print(f'\n\033[35;1m[~] Waiting......\033[0m')
    time.sleep(10)  

    self.getCookie()


  def getImgUrls(self, username):
    # url = f'https://instagram.com/{username}/'
    self.driver.get('{}{}/'.format(self.url, username)) 
    time.sleep(5)    
    img_urls = set()
    pre_article_style = ""
    cnt = 0
    scroll_times = 1
    
    while True:
      time.sleep(3)    
      article_styles = self.driver.find_elements(By.XPATH, '//article[@class="x1iyjqo2"]/div[1]/div[1]')[0]
      article_style = article_styles.get_attribute('style')
      if article_style == pre_article_style:
        cnt+=1
      else:
        pre_article_style = article_style
        cnt = 0
      if cnt==4:
        break

      urls = self.driver.find_elements(By.XPATH, '//div[@class="_aagv"]/img[1]')
      total_size = len(urls)
      
      if total_size!=0:
        for idx, url in enumerate(urls, start=1):
          print(f'\r\033[36;1m---> scroll: {scroll_times}\tProcessing ({idx}/{total_size}), {(idx/total_size)*100:.2f}%\033[0m', end='')
          org_img = url.get_attribute('src')
          img_urls.add(org_img)
      self.driver.execute_script(f'window.scrollTo({scroll_times*2000}, {(scroll_times+1)*2000})')
      scroll_times+=1

    print()
    print('#img_urls: ', len(img_urls))

    return img_urls


  def requestDownload(self, url, save_pth, filename):
    with requests.get(url, stream=True) as r:	# The request will be processed as a stream rather than downloading the entire file at once
      r.raise_for_status()	# If the HTTP request status code is not 200, an exception will be raised, otherwise the call will be ignored
      with open(os.path.join(save_pth, filename+'.jpg'), 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
          if chunk:
            f.write(chunk)


  def downloadImg(self, img, save_pth):
    filename = img.split('/')[-1].split('.jpg')[0].split('.webp')[0]

    try:
      self.requestDownload(img, save_pth, filename)
    except requests.exceptions.HTTPError as e:
      print(f'\n\033[31;1mHTTP error occurred\033[0m')


  def downloadFile(self, img_urls, username):
    save_pth = '.\download_1'
    save_pth = os.path.join(save_pth, username)
    print('save_pth: ', save_pth)
    os.makedirs(save_pth, exist_ok=True)
    total_size = len(img_urls)
    fail_cnt = 0

    with concurrent.futures.ThreadPoolExecutor() as executor:
      futures = list()
      futures = [executor.submit(self.downloadImg, img_url, save_pth) for img_url in img_urls]	# Submit the image download task to the threaded pool via the `executor.submit method`
      for idx, future in enumerate(concurrent.futures.as_completed(futures), start=1):	# Wait for all tasks to be completed
        try:
          future.result()	# When a picture is downloaded, the `future.result()` method will be called to get the result
          print(f'\r\033[36;1m({idx}/{total_size}), {(idx/total_size)*100:.2f}%, Downloading...\033[0m', end='')
        except Exception as e:
          # print(f'\033[31;1mDownload failed: {e}\033[0m')
          fail_cnt+=1
    print()
    print(f'#Download Success: {total_size - fail_cnt} | #Download Fail: {fail_cnt} |')
    print(f'\n\033[32;1m[+] Finish\033[0m')
  
  def getCookie(self):
    print(f'\n\033[34;1m[~] Get Cookies\033[0m')
    cookie_items = self.driver.get_cookies()
    cookies = dict()
    for idx, item_cookie in enumerate(cookie_items):
      print(f'{idx}: {item_cookie}')
      cookies[item_cookie["name"]] = item_cookie["value"]
    with open(self.cookies, 'w') as f:
      json.dump(cookies, f)
    print('cookies:', cookies)

  def loadCookie(self):
    print(f'\n\033[32;1m[+] Load Cookies\033[0m')
    self.driver.get(self.url) 
    time.sleep(5)
    self.driver.delete_all_cookies()
    with open(self.cookies, 'r') as f:
      cookies = json.load(f)
    for k, v in cookies.items():
      cookie = {'name':k, 'value':v}
      self.driver.add_cookie(cookie)

  def run(self, username):
    img_urls = self.getImgUrls(username)
    # input("Press enter to close the browser...")

    self.downloadFile(img_urls, username)


  def startSearch(self):
    print(f'\n\033[32;1m[+] Init\033[0m')

    if not os.path.exists(self.cookies):
      print(f'\n\033[34;1m[~] {self.cookies} not exists, please login \033[0m')
      self.login()
    else:
      print(f'\n\033[34;1m[~] {self.cookies} exists \033[0m')
      self.loadCookie()

    print(f'\n\033[32;1m[+] Start Search\033[0m')
    for username in self.usernames:
      print(f'\n\033[34;1m[~] Processing: {username}\033[0m')
      self.run(username)

    self.driver.quit()