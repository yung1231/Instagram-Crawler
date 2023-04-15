import os
import time
from tools.tools import get_proxy, getDriver, readConfig
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import getpass
import requests
import concurrent.futures



def requestDownload(url, save_pth, filename):
	with requests.get(url, stream=True) as r:	# The request will be processed as a stream rather than downloading the entire file at once
		r.raise_for_status()	# If the HTTP request status code is not 200, an exception will be raised, otherwise the call will be ignored
		with open(os.path.join(save_pth, filename+'.jpg'), 'wb') as f:
			for chunk in r.iter_content(chunk_size=8192):
				if chunk:
					f.write(chunk)


def downloadImg(img, save_pth):
	filename = img.split('/')[-1].split('.jpg')[0]

	try:
		requestDownload(img, save_pth, filename)
	except requests.exceptions.HTTPError as e:
		print(f'\n\033[31;1mHTTP error occurred\033[0m')


def downloadFile(img_urls, username):
	save_pth = '.\download_1'
	save_pth = os.path.join(save_pth, username)
	print('save_pth: ', save_pth)
	os.makedirs(save_pth, exist_ok=True)
	total_size = len(img_urls)

	with concurrent.futures.ThreadPoolExecutor() as executor:
		futures = list()
		futures = [executor.submit(downloadImg, img_url, save_pth) for img_url in img_urls]	# Submit the image download task to the threaded pool via the `executor.submit method`
		for idx, future in enumerate(concurrent.futures.as_completed(futures), start=1):	# Wait for all tasks to be completed
			try:
				future.result()	# When a picture is downloaded, the `future.result()` method will be called to get the result
				print(f'\r\033[36;1m({idx}/{total_size}), {(idx/total_size)*100:.2f}%, Download Successful\033[0m', end='')
			except Exception as e:
				print(f'\033[31;1mDownload failed: {e}\033[0m')
	print()


def login():
  global driver
  url = 'https://www.instagram.com/'  
  driver.get(url) 
  time.sleep(5)

  username_input = driver.find_elements(By.NAME, 'username')[0]
  password_input = driver.find_elements(By.NAME, 'password')[0]
  u = input("Your IG Account: ")
  p = getpass.getpass(prompt="Your IG password: ")
  username_input.send_keys(u)
  password_input.send_keys(p)
  login_click = driver.find_elements(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button[1]')[0]
  login_click.click() # login_click.send_keys(Keys.ENTER)
  time.sleep(5)

  # second_div = driver.find_elements(By.XPATH, '//body/div[2]')[0]
  # div_id = second_div.get_attribute("id")
  # print('div_id: ', div_id)

  store_click = driver.find_elements(By.XPATH, "//div[@role='button']")[0]
  store_click.click()
  time.sleep(5)  

def getImgUrls(username):
  url = f'https://instagram.com/{username}/'
  global driver
  driver.get(url) 
  time.sleep(5)    
  img_urls = set()
  pre_article_style = ""
  cnt = 0
  scroll_times = 1
  
  while True:
    time.sleep(3)    
    article_styles = driver.find_elements(By.XPATH, '//article[@class="x1iyjqo2"]/div[1]/div[1]')[0]
    article_style = article_styles.get_attribute('style')
    if article_style == pre_article_style:
      cnt+=1
    else:
      pre_article_style = article_style
      cnt = 0
    if cnt==4:
      break

    urls = driver.find_elements(By.XPATH, '//div[@class="_aagv"]/img[1]')
    total_size = len(urls)
    
    if total_size!=0:
      for idx, url in enumerate(urls, start=1):
        print(f'\r\033[36;1m---> scroll: {scroll_times}\tProcessing ({idx}/{total_size}), {(idx/total_size)*100:.2f}%\033[0m', end='')
        org_img = url.get_attribute('src')
        img_urls.add(org_img)
    driver.execute_script(f'window.scrollTo({scroll_times*2000}, {(scroll_times+1)*2000})')
    scroll_times+=1

  print()
  print('#img_urls: ', len(img_urls))

  return img_urls


def run(username):
  # url = 'https://www.instagram.com/'  
  # driver.get(url) 
  # time.sleep(5)

  # username_input = driver.find_elements(By.NAME, 'username')[0]
  # password_input = driver.find_elements(By.NAME, 'password')[0]
  # u = input("Your IG Account: ")
  # p = getpass.getpass(prompt="Your IG password: ")
  # username_input.send_keys(u)
  # password_input.send_keys(p)
  # login_click = driver.find_elements(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button[1]')[0]
  # login_click.click() # login_click.send_keys(Keys.ENTER)
  # time.sleep(5)
  
  # # second_div = driver.find_elements(By.XPATH, '//body/div[2]')[0]
  # # div_id = second_div.get_attribute("id")
  # # print('div_id: ', div_id)

  # store_click = driver.find_elements(By.XPATH, "//div[@role='button']")[0]
  # store_click.click()
  # time.sleep(5)   

  img_urls = getImgUrls(username)
  # input("Press enter to close the browser...")

  downloadFile(img_urls, username)


  return img_urls


if __name__=='__main__':
  config = readConfig()
  print(config['conf']['save_pth'])
  print(config['conf']['usernames'])
  save_pth = config['conf']['save_pth']
  usernames = config['conf']['usernames'].split(',')
  print('save_pth: ', save_pth)
  print('usernames: ', usernames)

  # success_proxy_ips = get_proxy()
  # print('success_proxy_ips: ', success_proxy_ips)

  success_proxy_ips = list()
  global driver
  driver = getDriver(success_proxy_ips)
  print('driver: ', driver)

  login()

  print(f'\n\033[32;1m[+] Run\033[0m')
  for username in usernames:
    print(f'\n\033[32;1m[+] Processing: {username}\033[0m')
    run(username)

  # print(f'\n\033[32;1m[+] download File\033[0m')
  # downloadFile(save_pth, img_urls)