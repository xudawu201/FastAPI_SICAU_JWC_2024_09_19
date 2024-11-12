'''
Author: xudawu
Date: 2022-08-26 13:39:48
LastEditors: xudawu
LastEditTime: 2024-11-10 18:21:12
'''

# Selenium 是一个自动化测试工具，利用它可以驱动浏览器执行特定的行为，最终帮助爬虫开发者获取到网页的动态内容。
# selenium 库是模拟人工操作浏览器的，优点可见即可爬
import random
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys # Keys 类提供键盘按键的支持
from selenium.webdriver.support.wait import WebDriverWait # 设置显示等待
from selenium.webdriver.support import expected_conditions as EC # 设置显示等待，找到特定标签后开始操作
'''
1.有一些网站专门针对 Selenium 设置了反爬措施，因为使用 Selenium 驱动的浏览器，
在控制台中可以看到如下所示的webdriver属性值为true，如果要绕过这项检查，
可以在加载页面之前，先通过执行 JavaScript 代码将其修改为undefined。
2.将浏览器窗口上的“Chrome正受到自动测试软件的控制”隐藏掉
'''

# 获得浏览器对象
def getBrowser(url):
    # 创建Chrome参数对象
    options = webdriver.ChromeOptions()
    # 添加试验性参数
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    # 不需要显示浏览器窗口
    # options.add_argument('--headless')
    # 创建Chrome浏览器对象并传入参数
    browser_WebDriver = webdriver.Chrome(options=options)
    # 执行Chrome开发者协议命令（在加载页面时执行指定的JavaScript代码）
    browser_WebDriver.execute_cdp_cmd(
        'Page.addScriptToEvaluateOnNewDocument',
        {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'}
    )
    browser_WebDriver.get(url)
    return browser_WebDriver

# 获取文本内容
def getContent(tagType_str,tagName_str):
    searchElementContent_WebDriver = browser_WebDriver.find_element(tagType_str,tagName_str)
    # searchElementContent_WebDriver = browser_WebDriver.find_element('class name',tagName_str)
    return searchElementContent_WebDriver.text

# 进入下一页/章
def nextPage(tagName_str):
    searchNextUrlContent_WebDriver = browser_WebDriver.find_element('id',tagName_str)
    searchNextUrlContent_WebDriver.click()

# 获取网络资源
def getNetFile(url_str):
    # 头部伪装
    # 如果不设置HTTP请求头中的User-Agent，网页会检测出不是浏览器而阻止我们的请求。
    # 通过get函数的headers参数设置User-Agent的值，具体的值可以在浏览器的开发者工具查看到。
    # 用爬虫访问大部分网站时，将爬虫伪装成来自浏览器的请求都是非常重要的一步。
    headers={
        'User-Agent': 
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6045.105 Safari/537.36'
        }
    #请求服务器,获取网络资源
    response = requests.get(url_str, headers=headers)
    # 获取网络资源的内容
    content=response.content
    return content

# 存储为txt文件，以追加方式
def saveInTxtFileByAppend_txt(fileName, content_str):
    fileNovel_txt = open(fileName, mode='a', encoding='utf-8')
    fileNovel_txt.write(content_str)  # write 写入
    fileNovel_txt.write('\r\n') # 写完一次换行
    fileNovel_txt.close()  # 关闭文件,如果用with open("f.txt", "a") as f:方式打开文件，会自动执行close()
    
# 等待页面加载完成
def waitPageLoaded(pageLocator_str):
    WebDriverWait(browser_WebDriver,10,0.5).until(EC.presence_of_element_located(pageLocator_str))

# 定位元素返回列表
def get_elements_list(browser_WebDriver,tagType_str,tagName_str):

    # 定位到父元素
    Element = WebDriverWait(browser_WebDriver, 10,0.5).until(
        EC.presence_of_element_located((tagType_str, tagName_str))  # 将 dl_id 替换为实际的 id
    )

    # 找到子元素
    element_list = Element.find_elements('tag name', 'dt')  # 替换为实际的标签名称

    # 定位元素并点击
    return element_list

# 点击元素
def click_element(element_webDriver):
    element_webDriver.click()

# 登录网站
def login_web(browser_WebDriver):
    
    # 用户名
    username_str='73294'
    # 密码
    password_str='Aimer1x@@'
    # 用户名输入框id
    usernameId_str='txtUser'
    # 密码输入框id
    passwordId_str='Userpwd'
    # 身份类别选择框id
    identityType_str='lb'
    # 登录按钮id
    loginButtonId_str='btn-primary'

    # 定位用户名和密码输入框,获取第一个元素
    username_input = browser_WebDriver.find_elements('id', usernameId_str)[0]
    password_input = browser_WebDriver.find_elements('id', passwordId_str)[0]

    # 输入用户名和密码
    username_input.send_keys(username_str)
    password_input.send_keys(password_str)

    # 定位身份类别选择框并点击,选择第二个标签
    identity_type = browser_WebDriver.find_elements('id', identityType_str)[1]
    identity_type.click()

    # 定位登录按钮并点击
    login_button = browser_WebDriver.find_elements('class name', loginButtonId_str)[0]  # 根据实际情况更改ID或定位方式
    login_button.click()


#主函数
if __name__ == '__main__':
    # 加载指定的页面
    url='https://jiaowu.sicau.edu.cn/web/web/web/index.asp'
    # 加载指定 URL 的页面到浏览器中
    browser_WebDriver=getBrowser(url)
    # 窗口最大化
    # browser_WebDriver.maximize_window()
    # 当前标签页浏览器渲染之后的网页源代码,包括动态内容
    # html=browser_WebDriver.page_source
    # print(html)
    # 设置隐式等待时间
    browser_WebDriver.implicitly_wait(5)
    
    # 用户登录
    login_web(browser_WebDriver)

    # 定位菜单标签
    tag_type_str='id'
    tag_name_str='menu-article'
    element_list = get_elements_list(browser_WebDriver,tag_type_str,tag_name_str)

    # 师资管理索引13
    element_list[13].click()

    # 存入的章节数
    targetChapterNumber_int=700
    # 当前章节数
    currentChapterNumber_int=1
    # 判断是否是下一页内容，0表示不是
    isNextPageContentFlag_int=0
    # 当前章节数小于等于目标章节数则继续存储
    while currentChapterNumber_int<=targetChapterNumber_int:
    # for chapter in range(1,chapterNumber_int):
        # 等待页面加载完成
        # pageLocator_str=('id','content')
        pageLocator_str=('class name','footer')
        # pageLocator_str=('tag name','footer')
        waitPageLoaded(pageLocator_str)
        # 显示页面标题
        title_str=browser_WebDriver.title
        # print('page:',title_str,'loaded')
        # 如果不是章节未完的下一页内容，则存储标题
        if isNextPageContentFlag_int==0:
            # 存储标题
            fileName='text.txt'
            saveInTxtFileByAppend_txt(fileName,title_str)

        # 文本内容tag
        tagType_str='id'
        searchContentId_str='content'
        # 获取元素中的文本
        ElementContent01_str=getContent(tagType_str,searchContentId_str)
        # print(ElementContent01_str)

        # 存储文本
        saveInTxtFileByAppend_txt(fileName,ElementContent01_str)
        # 存储完成
        print(title_str,'saved successful')

        # 查看有没有下一页
        searchNextPageUrlText_str='下一页'
        # 返回元素列表
        nextPageTag_list=browser_WebDriver.find_elements('link text',searchNextPageUrlText_str)
        # 如果不是空列表
        if nextPageTag_list!=[]:
            # 选择列表第一个下一页标签，点击进入下一页
            nextPageTag_list[0].click()
            # 设置下一页标签为1
            isNextPageContentFlag_int=1
            # 随机休眠，避免爬取页面过于频繁被封IP
            # time.sleep(random.randint(1, 3))
            # 跳过进入下一章
            continue
            # print(nextPageTag_list)
        
        # 设置下一页标签为0
        isNextPageContentFlag_int=0
        # 下一章tag
        searchNextChapterUrlText_str='下一章'
        # link text通过标签页面显示文本找到元素
        nextChapter_tag=browser_WebDriver.find_element('link text',searchNextChapterUrlText_str)
        # 点击进入下一章
        nextChapter_tag.click()
        # 章节数加一
        currentChapterNumber_int=currentChapterNumber_int+1
        # 随机休眠，避免爬取页面过于频繁被封IP
        # time.sleep(random.randint(1, 3))

    # 关闭浏览器
    browser_WebDriver.quit()
    print('all download successfully')