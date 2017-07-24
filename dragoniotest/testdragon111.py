# coding: utf-8
import atx
import time
import math

HUAWEI = 'FUH7N16921000491'
LG = 'LGAS33029f6c42c'
HTC = 'HT5BCJT00021'
PINKSAMSUNG = '330060b91193138f'
d = atx.connect(PINKSAMSUNG)

d.start_app('com.newstart.dragonio',"com.zentertain.newstart.Main")

def isCircle(targetPt,r):
	#圆心坐标
	cCenterPtX=0
	cCenterPtY=0
	#点击位置x坐标与圆心的x坐标的距离
	distanceX =	math.fabs(cCenterPtX - targetPt[0]);
	#点击位置y坐标与圆心的y坐标的距离
	distanceY =	math.fabs(cCenterPtY - targetPt[1]);
	#点击位置与圆心的直线距离
	distanceLen = math.sqrt(math.pow(distanceX,2) + math.pow(distanceY,2));

	#如果点击位置与圆心的距离大于圆的半径，证明点击位置没有在圆内
	if distanceLen > r :
		print (targetPt[0],targetPt[1])
		d.touch(-targetPt[0]/2,-targetPt[1]/2)
		print "掉头"+str(-targetPt[0]/2),str(-targetPt[1]/2)
	# elif distanceLen < r:
	# 	print "在圆内"
	else:
		pass

def ssdsd(d):
	pass
	#1.通过d.exists获取龙头位置
	#2.调用isCircle检测龙头是否在边缘
	#3.调用d.touch传入龙头的反方向位置

def dragonIO(d):
	if d.exists('dragonhead.1920x1080.png'):
		dragonhead = d.exists('dragonhead.1920x1080.png')
		print "dragonHead:"+str(dragonhead)
		# drx = str(drhead[0])
		# dry = str(drhead[1])
		r = 1000
		d.touch(d.info["displayHeight"]/3,d.info["displayWidth"]/3)
		print "掉头"
		#isCircle(dragonhead.pos,r)
	else:
		print "Not exits Dragon"
	return 0

def checkerror(d):
	d.exists(u'sysok.1920x1080.png')
	print "********"
	if d.exists(u'sysok.1920x1080.png'):
		d.touch(10,10)
		print "11111111111111111"
		return 1
	else:
		print "not found"
		return 0

def checklogin(d):
	if d.exists('enterplay.1920x1080.png'):
		debug(d)
		login(d)
		return 1
	else:
		print "2222"
		return  0

def debug(d):
	d.click_image('debugbutton.1920x1080.png')
	# d.click_image('opentouch.1920x1080.png')
	if(d.exists('offtouch.1920x1080.png')):
		d.click_image('closedebug.1920x1080.png',safe=True)
	else:
		d.click_image('opentouch.1920x1080.png',safe=True)
		d.click_image('closedebug.1920x1080.png',safe=True)
		print"*****************"
	
	return 0

def login(d):
	d.click_image('inputname.1920x1080.png')
	d.type('hello world')
	d.click_image('textspace.1920x1080.png',safe=True)
	d.click_image('closetext.1920x1080.png',safe=True)
	d.click_image('enterplay.1920x1080.png',safe=True)
	return 1


while 1:
	dragonIO(d)
	if(checkerror(d)):
		d.sleep(1)
		d.screenshot('screenshot.png')
		print "55555555555"
	elif(checklogin(d)):
	  	d.sleep(3)
	else:
		print "00000000000000"
		print "has entry"
		d.click_image('pinkfoods.1920x1080.png',safe=True)
		print "pink Map found"

		d.click_image('greenfoods.1920x1080.png',safe=True)
		print('green found')
		d.click_image('bluefoods.1920x1080.png',safe=True)
		print('blue found')
		print('HAHAHA')
		if (d.exists('recover.1920x1080.png')):
			d.click_image('recover.1920x1080.png',safe=True)
		elif(d.exists('savelog.1920x1080.png')):
			adb_cmd('logcat -d','dragon.log')

		d.sleep(1)
		# dragonIO(d)

		# d.click_image('inputname.1920x1080.png')
		# d.type('hello world')
		# d.click_image('textspace.1920x1080.png')
		# d.click_image('closetext.1920x1080.png')
		# d.click_image('enterplay.1920x1080.png')

# d.sleep(60)
# d.clear_text()


# if d.exists(u'cooking2new.1920x1080.png'):  # 判断截图是否在屏幕中出现, 反馈查找到的坐标
#    print 'founded'
#    d.click_image(u"cooking2new.1920x1080.png")
# print "11111"
# # d.screenshot()
# # d.print()

#d.click_image('guest_login.1920x1080.png')
# d.screenshot('screen.png')  # 截图