import logging
from argparse import ArgumentParser
from seleniumwire import webdriver
from os import path, mkdir
from urllib.parse import urlparse
from time import sleep
from secrets import SystemRandom
from selenium.webdriver.chrome.options import Options

from pyvirtualdisplay import Display

base_dir = path.dirname(path.abspath(__file__))
log_dir = path.join(base_dir, 'log')
driver_path = path.join(base_dir, 'chromedriver')
GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

parser = ArgumentParser(description="The URL of the webpage to visit.")
parser.add_argument('url', nargs='*', metavar='url', type=str, help='URL to visit.', default='test')

args = parser.parse_args()

u_a_list = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4209.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 "
    "Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.26 "
    "Safari/537.36 OPR/71.0.3770.0 (Edition developer)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 "
    "Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.3538.77 "
    "Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4215.0 "
    "Safari/537.36 Edg/86.0.597.0",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
            ]


referrer_list = [
    'https://www.google.com/', 'https://www.google.co.in/', 'https://duckduckgo.com/', 'https://www.bing.com/',
    'https://yandex.com/', 'https://en.wikipedia.org/', 'https://www.quora.com/', 'https://www.facebook.com/',
    'https://www.feedspot.com/', 'https://www.reddit.com', 'https://medium.com/', 'https://www.youtube.com/',
    'https://in.pinterest.com/', 'https://pinterest.com/'
]

random_generator = SystemRandom()


class HaxBot(object):
    def __init__(self, log_level_file=logging.DEBUG, log_level_stream=logging.INFO):
        self.logger = logging.getLogger("Hits Bot")
        self.logger.setLevel(logging.DEBUG)

        if not path.isdir(log_dir):
            mkdir(log_dir)

        log_filename: str = path.join(log_dir, 'hits_bot.log')
        fh = logging.FileHandler(filename=log_filename)
        fh.setLevel(log_level_file)
        fh.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s (%(module)s %(pathname)s:%(lineno)s) - %(levelname)s - %(message)s"
            )
        )

        self.logger.addHandler(fh)

        ch = logging.StreamHandler()
        ch.setLevel(log_level_stream)
        ch.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        self.logger.addHandler(ch)

        self.logger.info('------------- Init HitsBot -------------')

        self.user_agent = random_generator.choice(u_a_list)
        default_header = {
            'User-Agent': self.user_agent,
            'Referer': random_generator.choice(referrer_list)
        }

        options = webdriver.ChromeOptions()
        options.add_argument(f"user-agent={self.user_agent}")
        options.add_argument("--disable-web-security")
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.binary_location = GOOGLE_CHROME_PATH
        self.driver = webdriver.Chrome(execution_path=CHROMEDRIVER_PATH, options=options)
        self.driver.header_overrides = default_header

    def send_request(self, endpoint: str) -> None:
        try:
            self.logger.info(f"Trying to get - {endpoint}")
            self.driver.get(endpoint)

        except Exception as e:
            self.logger.info('Error occurred!')
            self.logger.info(e)
            raise SystemExit(0)

        for request in self.driver.requests:
            resp = request.response
            if resp:
                if urlparse(request.url).netloc == urlparse(endpoint).netloc:
                    self.logger.info(f"Response: [{resp.status_code}] {resp.reason}")

    def get_url(self, link: str):
        self.send_request(link)

    def sleep(self, t: int):
        self.logger.info(f'Waiting {t} seconds.')
        sleep(t)

    def close(self):
        self.driver.quit()
        self.logger.info("Finished!")


if __name__ == "__main__":
    display = Display(visible=0, size=(800, 600))
    display.start()
    bot = HaxBot()
    urls = args.url
    for n, u in enumerate(urls):
        o = urlparse(u)
        if o.scheme:
            bot.get_url(u)
        if n != (len(urls) - 1):
            bot.sleep(random_generator.randint(20, 32))
        else:
            bot.sleep(random_generator.randint(3, 8))
    bot.close()
    display.stop()
