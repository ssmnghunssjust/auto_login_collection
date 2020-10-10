import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

"""
运行前必须要做的事情：
如果直接使用webdriver，不做任何修改的话，淘宝可以断定启动的浏览器是“机器人”，而不是“死的机器”。
如果想让淘宝错误地认为启动的浏览器是"死的机器"，那么就需要修改webdriver。
我使用的是chromedriver，"perl -pi -e 's/cdc_/dog_/g' /usr/local/bin/chromedriver"是修改chromedriver的代码，直接在Terminal执行即可。执行完在运行此脚本，则可以成功登录。

这里我解释一下"perl -pi -e 's/cdc_/dog_/g' /usr/local/bin/chromedriver"，这段代码其实就是全局修改/usr/local/bin/chromedriver中的cdc_为dog_，"/usr/local/bin/chromedriver"是chromedriver所在的文件路径。
感谢https://www.jianshu.com/p/368be2cc6ca1这篇文章的作者。

######################################
- 已经修改的 webdriver 在仓库中请自行下载
- 不保证所有的版本都可用，以下是我用的版本，如果不适应，请下载对应的版本自行修改
- 另外感谢提供思路--
version: 版本 76.0.3809.100（正式版本） （64 位）
######################################
"""


class TaobaoSpider:

    def __init__(self, username, password):
        chrome_options = webdriver.ChromeOptions()
        # 不加载图片，加快访问速度
        chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        # 设置为开发者模式，避免被识别
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # self.web_driver = webdriver.Chrome(executable_path=r'D:\myWorkspace\awesome-python-login-model\taobao\windows_driver\chromedriver.exe',options=chrome_options)
        self.web_driver = webdriver.Chrome(executable_path=r'C:\Users\Administrator\Desktop\chromedriver.exe',
                                           options=chrome_options)
        self.web_driver_wait = WebDriverWait(self.web_driver, 10)

        # self.url = 'https://login.taobao.com/member/login.jhtml'
        self.url = 'https://main.m.taobao.com/mytaobao/index.html'
        self.username = username
        self.password = password

    def login(self):
        self.web_driver.get(self.url)
        try:
            # 切换为帐号密码登录
            # login_method_switch = self.web_driver_wait.until(
            #     expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="login"]/div[1]/i[contains(@class,"icon-password")]')))
            # login_method_switch.click()

            # 找到用户名输入框并输入
            # username_input = self.web_driver_wait.until(
            #     expected_conditions.presence_of_element_located((By.ID, 'fm-login-id')))
            # username_input.send_keys(self.username)
            time.sleep(3)
            iframe = self.web_driver_wait.until(
                expected_conditions.presence_of_element_located((By.TAG_NAME, 'iframe'))
            )
            self.web_driver.switch_to.frame(iframe)
            # self.web_driver.find_element_by_id('fm-login-id').send_keys('13126335602')
            username_input = self.web_driver_wait.until(
                expected_conditions.presence_of_element_located((By.ID, 'fm-login-id')))
            username_input.send_keys(self.username)

            # 找到密码输入框并输入
            password_input = self.web_driver_wait.until(
                expected_conditions.presence_of_element_located((By.ID, 'fm-login-password')))
            password_input.send_keys(self.password)
            time.sleep(1)

            # 拖动滑块完成验证码
            try:
                bar_drag = self.web_driver_wait.until(
                    expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="nc_1_n1z"]'))
                )
                bar_drag_size = bar_drag.size
                bar_drag_width = bar_drag_size.get('width')
                bar_size = self.web_driver.find_element_by_xpath('//*[@id="nc_1__scale_text"]/span').size
                bar_width = bar_size.get('width')
                print('bar_drag_width: %s' % bar_drag_width)
                print('move_offset: %s' % int(bar_width - bar_drag_width))
                action = ActionChains(self.web_driver)
                action.click_and_hold(bar_drag).perform()
                action.move_by_offset(int(bar_width - bar_drag_width), 0)
                action.release().perform()
                time.sleep(0.5)

            # 找到登录按钮并点击
            finally:
                login_button = self.web_driver_wait.until(
                    expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="login-form"]/div[5]/button')))
                login_button.click()
                time.sleep(2)

                # 找到名字标签并打印内容
                # taobao_name_tag = self.web_driver_wait.until(expected_conditions.presence_of_element_located(
                #     (By.XPATH, '//*[@id="J_Col_Main"]/div/div[1]/div/div[1]/div[1]/div/div[1]/a/em')))
                # print(f"登陆成功：{taobao_name_tag.text}")

                # 找到'查看全部订单'，则说明登录成功
                check_order = self.web_driver_wait.until(
                    expected_conditions.presence_of_element_located(
                        (By.XPATH, '/html/body/div[1]/div[1]/div[3]/div/div[2]/div[1]/div[2]/span'))
                )
                print('登录成功')
                cookie = self.web_driver.get_cookies()
                print(f'cookie：{cookie}')

                # 休息5秒钟，然后关闭浏览器
                time.sleep(5)
                self.web_driver.close()
                return cookie

        except Exception as e:
            print(e)
            self.web_driver.close()
            print("登陆失败")

    def login_test(self):
        self.web_driver.get(self.url)


if __name__ == "__main__":
    # username = input("请输入用户名：")
    # password = input("请输入密码：")
    spider = TaobaoSpider(username='', password='')
    spider.login()
    # spider.login_test()
