import os

from rich.console import Console
from rich.traceback import install

from config.selenium_config import config_selenium
from downloader import dl_litmos

if __name__ == '__main__':
    cwd = os.getcwd()
    console = Console()
    install()
    download_dir = cwd + '\\data'
    driver_dir = cwd + r'\driver\chromedriver.exe'
    chrome_dir = r'..\chrome-win_89\chrome.exe'
    driver = config_selenium(driver_dir, chrome_dir, download_dir)

    try:
        dl_litmos(driver, download_dir, web_timeout=340, dl_timeout=340)
    finally:
        driver.quit()
        console.log('finalizando driver', style='green')
