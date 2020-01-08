#!/usr/bin/python3
# -*- coding:UTF-8 -*-

from datetime import datetime

import pyperclip
import requests
import yagmail as email

# 邮箱参数（务必填写以下参数）
# 邮箱用户名
user = ''
# 邮箱密码
password = ''
# 邮箱服务器地址
host = ''
# 邮箱服务器端口
port = 465
# 收件人列表
mail_ls = ['']

# key 注册地址：https://www.tianapi.com/apiview/26
# 替换26为：26，72，117
key_ls = ['']

# 天气预报
city_name = '上海'


# 剪贴板操作
def addToClipBoard(text):
	pyperclip.copy(text)


# 时间戳操作
def get_timestamp():
	return datetime.now().strftime("%Y%m%d")


# 发送邮件
def sendMail(to=None, subject=None, contents=None, attachments=None, cc=None, bcc=None, preview_only=False, headers=None, newline_to_break=True):
	try:
		with email.SMTP(user=user, password=password, host=host, port=port) as m:
			m.send(to=to, subject=subject, contents=contents, attachments=attachments, cc=cc, bcc=bcc, preview_only=preview_only, headers=headers, newline_to_break=newline_to_break)
			print(f'邮件发送成功！to：{to}')
	except Exception as ex:
		print(ex)


# 获取天气，渠道：天行api 72
def get_weather():
	for key in key_ls:
		res = requests.get(url=f'http://api.tianapi.com/txapi/tianqi/index?key={key}&city={city_name}').json()
		if res['code'] == 200 and res['msg'] == 'success':
			return res['newslist'][0]
		else:
			print(res)
	print(f'无可用的key！')
	return None


# 获取新闻，渠道：天行api 117
def get_news():
	for key in key_ls:
		res = requests.get(url=f'http://api.tianapi.com/bulletin/index?key={key}').json()
		if res['code'] == 200 and res['msg'] == 'success':
			return res['newslist']
		else:
			print(res)
	print(f'无可用的key！')
	return None


# 获取名人名言，渠道：天行api 26
def get_word_of_famous_people():
	for key in key_ls:
		res = requests.get(url=f'http://api.tianapi.com/txapi/dictum/index?key={key}&num=1').json()
		if res['code'] == 200 and res['msg'] == 'success':
			return res['newslist'][0]
		else:
			print(res)
	print(f'无可用的key！')
	return None


# 获取日报
# show_digest: bool = False, 是否显示简介，默认为否
# show_url: bool = False, 是否显示超链接，默认为否
# show_image: bool = False, 是否显示图片，默认为否
# send_to_clidBoard: bool = False, 是否复制到剪贴板，默认为否
# send_mail: bool = True，是否发送邮件，默认为是
# 默认返回daily到控制台
def get_daily(show_digest: bool = False, show_url: bool = False, show_image: bool = False, send_to_clidBoard: bool = False, send_mail: bool = True):
	daily = list()
	# 获取天气预报
	res = get_weather()
	if res:
		daily.append(f'****************************************')
		daily.append(f"天气预报：[ 城市：{city_name} ]")
		daily.append(f'****************************************')
		daily.append(f"日期：{res['date']}")
		daily.append(f"星期：{res['week']}")
		daily.append(f"天气：{res['weather']}")
		daily.append(f"当前温度：{res['real']}")
		daily.append(f"最低温度：{res['lowest']}")
		daily.append(f"最高温度：{res['highest']}")
		daily.append(f"风向：{res['wind']}")
		daily.append(f"风速：{res['windspeed']}")
		daily.append(f"湿度：{res['humidity']}")
		daily.append(f"空气质量指数：{res['air']}")
		daily.append(f"空气质量等级：{res['air_level']}")
		daily.append(f"天气状况提示：{res['tips']}")

	# 今日热点
	res = get_news()
	if res:
		daily.append(f'****************************************')
		daily.append(f'今日热点：')
		daily.append(f'****************************************')
		for idx, news in enumerate(res, 1):
			daily.append(f"{idx}、{news['title']}")
			if show_digest and news['digest']:
				daily.append(f"--> {news['digest']}")
			if show_url and news['url']:
				daily.append(f"--> {news['url']}")
			if show_image and news['imgsrc']:
				daily.append(f"<img src='{news['imgsrc']}' alt='{news['title']}'>")
			# if show_url:
			# 	if news['url']:
			# 		daily.append(f"{idx}、<a href='{news['url']}'>{news['title']}</a>")
			# 	else:
			# 		daily.append(f"{idx}、{news['title']}")
			# 	if show_image:
			# 		if news['imgsrc']:
			# 			if news['url']:
			# 				daily.append(f"<a href='{news['url']}'><img src='{news['imgsrc']}' alt='{news['title']}'></a>")
			# 			else:
			# 				daily.append(f"<img src='{news['imgsrc']}' alt='{news['title']}'>")
			# else:
			#
			# 	if show_digest:
			# 		daily.append(f"--> {news['digest']}")

	# 每日一句
	res = get_word_of_famous_people()
	if res:
		daily.append(f'****************************************')
		daily.append(f'每日一句：')
		daily.append(f'****************************************')
		daily.append(f"{res['content']} —— {res['mrname']}")
	if len(daily) > 0:
		content = '\n'.join(daily)
		if send_to_clidBoard:
			addToClipBoard(content)
		if send_mail:
			# 发送邮件
			sendMail(to=mail_ls, subject=f'{get_timestamp()}日报', contents=content)
		return content


if __name__ == '__main__':
	# 请在配置顶部参数后，根据实际情况修改传入的参数
	# show_digest: bool = False, 是否显示简介，默认为否
	# show_url: bool = False, 是否显示超链接，默认为否
	# send_to_clidBoard: bool = False, 是否复制到剪贴板，默认为否
	# send_mail: bool = True，是否发送邮件，默认为是
	# 默认返回daily到控制台
	print(get_daily(show_digest=False, show_url=False, show_image=False, send_to_clidBoard=True, send_mail=False))
	pass
