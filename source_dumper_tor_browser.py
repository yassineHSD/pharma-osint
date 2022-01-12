import tbselenium.common as cm
from bs4 import BeautifulSoup
from tbselenium.tbdriver import TorBrowserDriver
from tbselenium.utils import launch_tbb_tor_with_stem
import time

'''
tbb_dir = "/home/sudoer/tor-browser/tor-browser_en-US/"
tor_process = launch_tbb_tor_with_stem(tbb_path=tbb_dir)
with TorBrowserDriver(tbb_dir, tor_cfg=cm.USE_STEM) as driver:
    driver.load_url("https://duckduckgo.com/?q=site%3Areddit.com+AND+intitle%3ANovartis&t=h_&ia=web")
'''
with TorBrowserDriver("/home/sudoer/tor-browser/tor-browser_en-US/") as driver:
    driver.get('https://check.torproject.org')
time.sleep(10)
html_source = driver.page_source
soup = BeautifulSoup(html_source,'lxml')
f = open("soup.html", "w")
f.write(soup)
f.close()
print(soup)
#tor_process.kill()
