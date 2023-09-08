# Author: Rainsblue.chan
# Create: 2023/7/20
# FileName: powered by pyppeteer
import asyncio
import time
import logging
from pyppeteer import launch
from pyquery import PyQuery as pq

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s-%(levelname)s:%(message)s')

# 根网页
global url
print('url like: https://www.kaoshibao.com/online/?paperId=xxxxx')
url = input('print url:')
print('meow.')
time.sleep(0.2)
width,height = 1200,768

async def main():
    browser = await launch(headless=True, args=['--disable-infobars',f'--window-size={width},{height}'])
    context = await browser.createIncogniteBrowserContext()  # 开启无痕模式
    page = await context.newPage()
    await page.setViewport({'width':width,'height':height})
    await page.goto(url)
    element = await page.waitForXPath('//*[@id="body"]/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]/p[2]/span[2]/div')
    await element.click()
    # 全题型
    num = input('题目从哪里到哪里？（比如第1题到第5题，就输1 5，用空格隔开）：')
    sb = num.split(' ')
    for i in range(int(sb[0]), int(sb[1])):
        try:
            xp = '//*[@id="body"]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/span[' + str(i) + ']'
            element = await page.waitForXPath(xp)
            # 调试
            # print(bt)
            await element.click()
        except ElementClickInterceptedException:
            element = await page.waitForXPath('/html/body/div[4]/div/div[3]/button[1]')
            await element.click()
            xp = '//*[@id="body"]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/span[' + str(i) + ']'
            element = await page.waitForXPath(xp)
            await element.click()
        # 题目
        async def get_question():
            question = await page.waitForSelector('.qusetion-box')
            doc = pq(await page.content())
            names = [item.text() for item in doc('.qusetion-box').items()]
            print('Names:', names)
        # 选项
        async def get_options():
            option = await page.waitForSelector('.option')
            doc = pq(await page.content())
            names = [item.text() for item in doc('.option').items()]
            print('Options:', names)
        # 正确选项
        async def get_right_option():
            option = await page.waitForSelector('.right')
            doc = pq(await page.content())
            names = [item.text() for item in doc('.right').items()][0]
            print('Right option:', names)
        async def get_right_options():
            option = await page.waitForSelector('.right3')
            doc = pq(await page.content())
            names = [item.text() for item in doc('.right3').items()]
            print('Right options:', names)
        # 留足渲染时间
        time.sleep(0.1)
        await get_question()
        await get_options()
        # 改成XPath就果然没问题...
        option = await page.waitForXPath('//*[@id="body"]/div[2]/div[1]/div[2]/div[1]/div/div[1]/div/div[1]/div/span[1]')
        doc = pq(await page.content())
        names = [item.text() for item in doc('.topic-type').items()][0]
        if names != '多选题':
            await get_right_option()
        else:
            await get_right_options()
        time.sleep(0.1)
    time.sleep(5)
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())