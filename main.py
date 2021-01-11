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
    dr.find_element_by_xpath('//*[@id="exampleInputName"]').send_keys(username)
    dr.find_element_by_xpath('//*[@id="exampleInputPassword"]').send_keys(passwd)

    while(True):
        try:
            print('获取网页截图')

            dr.save_screenshot(screen)
            ele = dr.find_element_by_xpath('//*[@id="loginImgVcode"]')
            ele.screenshot(code)
            print('获取图形二维码截图')
            
            captcha = tools.ocrCap(code)
            print('解析后的图形二维码是：%s' % captcha)

            dr.find_element_by_xpath('//*[@id="loginVerifyCode"]').clear()
            dr.find_element_by_xpath('//*[@id="loginVerifyCode"]').send_keys(captcha)
            sleep(1)

            dr.find_element_by_xpath('//*[@id="loginBtn"]').click()
            sleep(1)
        except:
            continue
        
        try:
            error = dr.find_element_by_xpath('//*[@id="Login"]/div/p[3]').text
            print(error)

            if error != '验证码填写错误':
                break
            sleep(3)
        except:
            break
        

    print('图形二维码验证通过!')

    try:
        dr.find_element_by_xpath('//*[@id="Login"]/div/p[3]').click()
        sleep(1)
        dr.find_element_by_xpath('//*[@id="theNewestModalLabel"]/div[2]/div/div[3]/button').click()
        sleep(1)
        dr.find_element_by_xpath('//*[@id="theNewestModalLabel"]/div[2]/div/div[3]/button').click()
        sleep(1)
    except:
        pass
else:
    # 手动登录后，可设置如下cookie值 is_auto_login = False
    dr.add_cookie({'name': '_ati', 'value': '7167890117748'})
    dr.add_cookie({'name': 'Hm_lvt_f8001a3f3d9bf5923f780580eb550c0b', 'value': '1608774615,1608887048,1609121740,1609136565'})
    dr.add_cookie({'name': 'dxm_i', 'value': 'NzkxMjE4IWFUMDNPVEV5TVRnITAxNjA5MTQzMmM1MTE4MzUyYjFkZGQwY2Y0Nzc1MDM2'})
    dr.add_cookie({'name': 'dxm_t', 'value': 'MTYwOTE0NTk4MiFkRDB4TmpBNU1UUTFPVGd5IWI5ZmE3MDA4YTg0NWVhYjM2ZTRhYWJhNThmNjkwMzg4'})
    dr.add_cookie({'name': 'dxm_c', 'value': 'VG0wQmtEUkchWXoxVWJUQkNhMFJTUnchNDZlNzcyYjYwYmQ4N2RmMTFhYjE2MTc4ODBhZmRiYzc'})
    dr.add_cookie({'name': 'dxm_w', 'value': 'NDQwYTgzOWE0ZTBiMzAyM2FmMjc5ZmViOTMxOTc0NzEhZHowME5EQmhPRE01WVRSbE1HSXpNREl6WVdZeU56bG1aV0k1TXpFNU56UTNNUSE3MDcwMTY0NjJiYjlkNjJmN2Y4YjM0Y2E2MWU4YWRlNg'})
    dr.add_cookie({'name': 'dxm_s', 'value': '29yrYuCI2-1i8WiKV8PR-Aee6zBzcqdYFGP3iMtyGCs'})
    dr.add_cookie({'name': 'Hm_lpvt_f8001a3f3d9bf5923f780580eb550c0b', 'value': '1609145976'})
    dr.add_cookie({'name': 'JSESSIONID', 'value': '1EE1303D0B1F164797C24AEE6F3FCDFF'})


dr.get('https://www.dianxiaomi.com/bannedWord/index.htm')

try:
    dr.find_element_by_xpath('//*[@id="theNewestModalLabel"]/div[2]/div/div[3]/button').click()
    sleep(1)
    dr.find_element_by_xpath('//*[@id="theNewestModalLabel"]/div[2]/div/div[3]/button').click()
    sleep(1)
except:
    pass

dr.find_element_by_xpath('//*[@id="rightBody"]/div[2]/div/div/div/ul/li[2]').click()
sleep(1)

sel = dr.find_element_by_xpath('//*[@id="downPage"]/li[1]/a/select')
Select(sel).select_by_value('100')
sleep(2)

totalStr = dr.find_element_by_xpath('//*[@id="upPage"]/li[7]/a').text
total = int(totalStr[totalStr.rfind('/')+1 : len(totalStr)])

for i in trange(total): 
    sleep(2)
    dr.find_element_by_xpath('//*[@id="downPage"]/li[5]/a').click()

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
