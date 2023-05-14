import zkSync2_auto
from config import global_config
from selenium.webdriver.common.by import By
import requests,time
import sys

from zkSync_era import launchSeleniumWebdriver


def runTest():
    # 指定chromedriver路径
    # driver_path = global_config.get('path', 'driver_path').strip()
    # driver_path = global_config.get('path', 'driver_path').strip()
    open_url = "http://local.adspower.net:50325/api/v1/browser/start?user_id=j5wkcl8"
    close_url = "http://local.adspower.net:50325/api/v1/browser/stop?user_id=j5wkcl8"

    resp = requests.get(open_url).json()
    if resp["code"] != 0:
        print(resp["msg"])
        print("please check ads_id")
        sys.exit()

    chrome_driver = resp["data"]["webdriver"]
    print('web driver' + chrome_driver)

    driver = launchSeleniumWebdriver(resp)
    # 打开zkSync2.0测试网
    wait_time = global_config.get('config', 'time')
    driver.implicitly_wait(wait_time)

    # close all tabs except the first one
    window_handles = driver.window_handles

    # 循环遍历所有窗口句柄
    for handle in window_handles:
        # 切换到该窗口
        driver.switch_to.window(handle)
        driver.close()
        if len(driver.window_handles) == 1:
            break
        # # 如果该窗口不是当前窗口，就关闭它
        # if handle != driver.current_window_handle:


    driver.switch_to.window(driver.window_handles[0])

    driver.maximize_window()

    driver.get('chrome-extension://{}/home.html'.format('jggokpgddphmogakajaeedjdmfoacona'))

    try:
        password = 'your_password'
        passworkdInput = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/div/form/div/div/input')
        passworkdInput.send_keys(password)
        driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div/button').click()
    except Exception as e:
        print("no need to unlock metamask")

    print("connected metamask")

    zkSync2_auto.changeMetamaskNetwork(driver, 'zkSync Era')

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get('https://swap-zksync.spacefi.io/#/swap')
    time.sleep(5)

    try:
        driver.find_element(By.XPATH, "//button[@id='connect-wallet']/p").click()
        driver.find_element(By.XPATH, "connect-METAMASK").click()

        driver.switch_to.window(driver.window_handles[0]) # go to metamask
        for i in range(0, 2):
            driver.refresh()
            time.sleep(2)
        driver.find_element(By.XPATH, '//button[text()="Next"]').click()
        driver.find_element(By.XPATH, '//button[text()="Connect"]').click()
        driver.switch_to.window(driver.window_handles[1]) # go to mute
        driver.refresh()
    except Exception as e:
        print("already connected")

    # input amount
    driver.find_element(By.XPATH, '//*[@id="swap-currency-input"]/div/div[2]/input').send_keys('0.01')
    driver.find_element(By.XPATH,
        u"(.//*[normalize-space(text()) and normalize-space(.)='选择通证'])[1]/following::*[name()='svg'][1]").click()
    driver.find_element(By.XPATH,
        "(.//*[normalize-space(text()) and normalize-space(.)='SPACE'])[3]/following::div[6]").click()
    driver.find_element(By.XPATH, "//button[@id='swap-button']/div").click()

    # confirm in metamask


runTest()