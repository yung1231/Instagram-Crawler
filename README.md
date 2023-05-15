# Instagram Crawler
This program is a crawler that can be used to download all images from a given set of Instagram accounts.

## Installation
1. Clone the repository & Install the required dependencies

```bash
git clone https://github.com/yung1231/Instagram-Crawler.git

pip install -r requirements.txt
```

2. chromedriver
   - Download the Chrome Driver from [official website](https://chromedriver.chromium.org/downloads). Make sure to download the version that matches your Chrome browser version.

## Usage
1. Fill in the information in `config.cfg`, including the usernames of the Instagram accounts you want to download images from.
   - Note: You can enter multiple usernames in the `usernames` field by separating them with commas.
   ```bash
   [conf]
   save_pth = .\download_1
   usernames = username_1,username_2,username_3,username_4,username_5...
   ```
2. Run `main.py`.
3. Enter your `username` and `password` to login.
4. Alternatively, you can use `cookies` for login. If it's your first time using the program, you will need to login with your username and password. Afterwards, you can use cookies to login directly.
   - Note: If you encounter any issues with your cookies, please delete the `cookies.json` file and re-capture the cookies.