from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from time import sleep
from lxml import etree
from tqdm import trange
import json
import tools
import write_sql
import platform
import config


username = config.username # 登录账户名
passwd = config.passwd # 登录密码
screen = config.screen # 截取全屏
code = config.code # 截取图片验证二维码
words_path = config.words_path # 文本保存路径

# chromedriver驱动
executable_path = config.chromedriver_win
if(platform.system() == "Linux"):
    executable_path = config.chromedriver_linux


home_page = config.home_page # 官网URL
res = [] # 最终结果
is_auto_login = True # 是否自动登录


options = Options()
options.add_argument('--headless')
dr = webdriver.Chrome(executable_path=executable_path, options=options)
dr.maximize_window()

dr.get(home_page)

if is_auto_login:
    dr.find_element_by_xpath('//*[@id="login_container"]/ul[1]/li[1]/div/input').send_keys(username)
    
    while(True):
        try:
            print('获取网页截图')

            dr.save_screenshot(screen)
            ele = dr.find_element_by_xpath('//*[@id="captcha"]')
            ele.screenshot(code)
            print('获取图形二维码截图')
            
            captcha = tools.ocrCap(code)
            print('解析后的图形二维码是：%s' % captcha)

            dr.find_element_by_xpath('//*[@id="login_container"]/ul[1]/li[2]/div/input').clear()
            dr.find_element_by_xpath('//*[@id="login_container"]/ul[1]/li[2]/div/input').send_keys(passwd)

            dr.find_element_by_xpath('//*[@id="login_container"]/ul[1]/li[3]/div/input').clear()
            dr.find_element_by_xpath('//*[@id="login_container"]/ul[1]/li[3]/div/input').send_keys(captcha)
            sleep(1)

            dr.find_element_by_xpath('//*[@id="login_container"]/input').click()
            sleep(1)
        except:
            continue
        
        try:
            error = dr.find_element_by_xpath('//*[@id="login_container"]/div[2]').text
            print(error)

            if error != '!验证码输入错误':
                break
            sleep(3)
        except:
            break
        

    print('图形二维码验证通过!')

else:
    # 手动登录后，可设置如下cookie值 is_auto_login = False
    dr.add_cookie({'name': 'JSESSIONID', 'value': 'A7718F554D2FD52E56C0A3D8EE4ED5AD'})
    dr.add_cookie({'name': 'route_srv_id', 'value': 'e6010b755650ba73faa9f09ff40d68cc'})
    dr.add_cookie({'name': '_ati', 'value': '9654480104297'})



dr.get(config.data_page)

sleep(1)
try:
    dr.find_element_by_xpath('//*[@id="announcementsWin"]/div[2]/a[1]').click()
except:
    pass

sel = dr.find_element_by_xpath('//*[@id="tableDiv"]/div/div/div[2]/table/tbody/tr/td[1]/select')
Select(sel).select_by_visible_text('50')
sleep(2)

totalStr = dr.find_element_by_xpath('//*[@id="tableDiv"]/div/div/div[2]/table/tbody/tr/td[8]/span').text
total = int(totalStr[1:-1])

for i in trange(total): 
    sleep(2)
    dr.find_element_by_xpath('//*[@id="tableDiv"]/div/div/div[2]/table/tbody/tr/td[10]/a/span/span[2]').click()

    htmlSource = dr.page_source
    html = etree.HTML(htmlSource)
    res += tools.pageData(html)

jsonData = json.dumps(res)
with open(words_path, "w") as f:
    f.write(jsonData)

print('爬取数据完成')

print('开始写入数据库')
write_sql.write_into_db(words_path)
print('写入数据库完成')

dr.quit()
