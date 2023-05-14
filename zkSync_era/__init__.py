from selenium.webdriver.common.by import By
import requests,time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

def changeMetamaskNetwork(driver, networkName):
    # opening network
    print("Changing network")
    driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[1]/div/div[2]/div[1]/div/span').click()
    print("opening network dropdown")
    time.sleep(2)
    # 以太坊 Ethereum 主网络
    # Ropsten 测试网络
    # Kovan 测试网络
    # Rinkeby 测试网络
    # Goerli 测试网络
    all_li = driver.find_elements(By.TAG_NAME, 'li')

    for li in all_li:
        text = li.text
        if text == networkName:
            li.click()
            print(text, "is selected")
            return
    print("Please provide a valid network name")
    # driver.close()
    # driver.switch_to.window(driver.window_handles[0])
    # time.sleep(3)


def launchSeleniumWebdriver(resp):
    chrome_driver = resp["data"]["webdriver"]
    print('web driver path: ', chrome_driver)
    # print('path', EXTENSION_PATH)
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--lang=zh-cn')
    chrome_options.add_argument('--disable-lava-moat')
    # chrome_options.add_extension(EXTENSION_PATH)
    chrome_options.add_experimental_option("debuggerAddress", resp["data"]["ws"]["selenium"])
    driver = webdriver.Chrome(chrome_driver, options=chrome_options)
    print("Extension has been loaded")
    return driver
