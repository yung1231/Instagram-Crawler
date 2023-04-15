import requests
import re
import concurrent.futures

class ProxiesIp:
  def __init__(self):
    pass

  def get_proxy_ip(self):
    response = requests.get("https://www.us-proxy.org")
    proxy_ips = re.findall('\d+\.\d+\.\d+\.\d+:\d+', response.text) # \d 代表任何一個數字字符     + 代表前面的模式出現一次或多次      
    return proxy_ips

  def check_proxy(self, proxy_ip, site_to_check):
    try:
      res = requests.get(site_to_check, 
                          proxies={'http': proxy_ip, 'https': proxy_ip}, 
                          timeout=5)
      if res.status_code == 200:
        return proxy_ip
    except:
      pass
    
    return None

  def check_proxies(self, proxy_ips, site_to_check='http://ipinfo.io/json'):
    print('site_to_check: ', site_to_check)
    valid_proxy_ips = list()

    with concurrent.futures.ThreadPoolExecutor() as executor:
      futures = [executor.submit(self.check_proxy, proxy_ip, site_to_check) for proxy_ip in proxy_ips]
      total_size = len(futures)
      for idx, future in enumerate(concurrent.futures.as_completed(futures), start=1):
        valid_proxy_ip = future.result()
        print(f'\r\033[36;1m({idx}/{total_size}), {(idx/total_size)*100:.2f}%, Checking Proxy\033[0m', end='')
        if valid_proxy_ip is not None:
          valid_proxy_ips.append(valid_proxy_ip)
    print()

    return valid_proxy_ips
  
  def run(self):
    print(f'\n\033[32;1m[+] Get Proxy Ip\033[0m')
    proxy_ips = self.get_proxy_ip()
    print('#proxy_ips: ', len(proxy_ips))

    # print(f'\n\033[32;1m[+] Check Proxies\033[0m')
    # valid_proxy_ips = self.check_proxies(proxy_ips)
    # print(f'#valid_proxy_ips: {len(valid_proxy_ips)}')

    print(f'\n\033[32;1m[+] Check Use Proxies\033[0m')
    site_to_check = 'https://www.instagram.com/hahahaleopard/'
    success_proxy_ips = self.check_proxies(proxy_ips, site_to_check)
    print(f'#success_proxy_ips: {len(success_proxy_ips)}')



    # success_proxy_ips = self.check_valid_proxies(valid_proxy_ips)
    # print(success_proxy_ips)

    return success_proxy_ips