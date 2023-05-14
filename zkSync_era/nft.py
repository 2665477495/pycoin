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
    # # driver.get('chrome-extension://{}/home.html#unlock'.format('nkbihfbeogaeaoehlefnkodbefgpgknn'))
    # # driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")


    # driver.find_element(By.XPATH, '//*[@id="password-label"]').click()
    # try catch
    try:
        password = 'your_password'
        passworkdInput = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/div/form/div/div/input')
        passworkdInput.send_keys(password)
        driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div/button').click()
    except Exception as e:
        print("no need to unlock metamask")

    print("connected metamask")
    time.sleep(5)

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get('https://mintsquare.io/zksync')
    time.sleep(3)
    driver.find_element(By.XPATH, "(.//*[normalize-space(text()) and normalize-space(.)='Collections'])[1]/following::*[name()='svg'][2]");

    driver.quit()

runTest()