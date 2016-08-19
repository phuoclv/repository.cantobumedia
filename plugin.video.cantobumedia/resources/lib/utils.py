# -*- coding: utf-8 -*-

import xbmc, xbmcaddon, urllib2

#addon=addon()
addon= xbmcaddon.Addon()
profile=xbmc.translatePath(addon.getAddonInfo('profile'))
datapath=urllib2.os.path.join(profile,'data')
tempfolder=xbmc.translatePath('special://temp')
xsharefolder=urllib2.os.path.join(tempfolder,'xshare')
icon=urllib2.os.path.join(profile,'icon','icon.png')

hd={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/600.1.4 Gecko/20100101 Firefox/41.0'}	

class myaddon:
    def __init__(self):
		self.addon			= xbmcaddon.Addon()
		self.info			= self.addon.getAddonInfo
		self.name			= self.info('name')
		self.version		= self.info('version')
		self.get_setting	= self.addon.getSetting
		self.set_setting	= self.addon.setSetting

		self.src_path		= xbmc.translatePath(self.info('path'))
		self.data_path		= xbmc.translatePath(self.info('profile'))
		self.temp_path		= xbmc.translatePath('special://temp')

		self.data_folder	= urllib2.os.path.join(self.data_path,'data')
		self.icon_folder	= urllib2.os.path.join(self.data_path,'icon')
		self.icon			= urllib2.os.path.join(self.icon_folder,'icon.png')

def joinpath(p1,p2):
	try:p=os.path.join(p1,p2)
	except:p=os.path.join(p1,s2u(p2))
	return p		
		
def filetime(fn):#return hour
	fn=urllib2.os.path.join(xsharefolder,fn)
	t=urllib2.os.path.getmtime(fn) if urllib2.os.path.isfile(fn) else 0
	return int((urllib2.time.time()-t)/600)
	
def get_setting(name):return addon.getSetting(name)
def set_setting(name,value):addon.setSetting(name,value)
def mess(message='',title='',timeShown=5000):
	if not message:xbmc.executebuiltin("Dialog.Close(all, true)")
	else:
		title=': [COLOR blue]%s[/COLOR]'%title if title else ''
		s0='[COLOR green][B]Xshare[/B][/COLOR]'+title
		s1='[COLOR red]%s[/COLOR]'%message if '!' in message else u'[COLOR gold]%s[/COLOR]'%message
		#icon=addon.icon
		xbmc.executebuiltin((u'XBMC.Notification(%s,%s,%s,%s)'%(s0,s1,timeShown,icon)).encode("utf-8"))

def rsl(s):
	s=str(s).replace('HDG','').replace('HD','1080').replace('SD','640').replace('large','640').replace('medium','480')
	result=xsearch('(\d+)',s)
	return result if result else '240'

def ls(l):
	r=True if get_setting('resolut')=='Max' else False
	l=sorted(l, key=lambda k: int(k[1]),reverse=r)
	return l

def namecolor(name,c=''):return '[COLOR %s]%s[/COLOR]'%(c,name) if c else urllib2.re.sub('\[[^\[]+?\]','',name)
def xrw(fn,s=''):
	fn=urllib2.os.path.join(xsharefolder,fn)
	try:
		if s:f=open(fn,'w');f.write(s);s=fn
		else:f=open(fn);s=f.read()
		f.close()
	except:s=''
	return s

def xcookie(cookie=None):
	if cookie:ck=';'.join('%s=%s'%(i.name,i.value) for i in cookie.cookiejar)
	else:ck=urllib2.HTTPCookieProcessor();urllib2.install_opener(urllib2.build_opener(ck))
	return ck
	
def make_request(url,headers=hd,resp='b',maxr=0):
	try:
		if maxr==0:response=get(url,headers=headers)#,timeout=2)
		else:response=get(url,headers=headers,max_redirects=maxr)#,timeout=2)
		if resp=='o':resp=response
		else:
			if resp=='j':resp=response.json
			elif resp=='s':resp=response.status
			elif resp=='u':resp=response.text
			elif resp=='c':resp=response.cookiestring
			else:resp=response.body
			response.close()
	except:
		if resp=='j':resp=dict()
		elif resp=='s':resp=500
		else:resp=''
		if 'vaphim.com' not in url:
			link=xsearch('//(.{5,20}\.\w{2,3})',s2u(url))
			if not link:link=url
			mess(u'Lỗi kết nối tới: %s!'%xsearch('//(.{5,20}\.\w{2,3})',s2u(url)),'make_request')
		print 'Lỗi kết nối tới: %s!'%u2s(url);
	return resp#unicode:body=response.text

def make_post(url,headers=hd,data='',resp='o'):
	try:
		if data:response=post(url=url,headers=headers,data=data,timeout=10)
		else:response=post(url=url,headers=headers,timeout=10)
		if resp=='b':response=response.body
		elif resp=='j':response=response.json
	except:
		mess(u'Post link error: %s!'%s2u(url),'make_post');print 'Post link error: %s'%u2s(url)
		response={} if resp=='j' else ''
	return response

def xread(url,hd={'User-Agent':'Mozilla/5.0'},data=None):
	req=urllib2.Request(url,data,hd)
	try:res=urllib2.urlopen(req, timeout=20);b=res.read();res.close()
	except:b=''
	return b

def makerequest(file,body='',attr='r'):
	file=s2u(file)
	if attr=='r':
		try:f=open(file);body=f.read();f.close()
		except:body=''
	else:
		try:f=open(file,attr);f.write(body);f.close()
		except:mess(u'Lỗi ghi file: %s!'%s2u(os.path.basename(file)),'makerequest');body=''
	return body

def xget(url,data=None,timeout=30):#b.getcode();b.headers.get('Set-Cookie');b.geturl()
	try:b=urllib2.urlopen(url,data,timeout)
	except:b=None
	return b

def get_input(title=u"", default=u""):
	result = ''
	keyboard = xbmc.Keyboard(default, title)
	keyboard.doModal()
	if keyboard.isConfirmed():
		result = keyboard.getText()
	return result.strip()

def xsearch(pattern,string,group=1,flags=0,result=''):
	try:s=urllib2.re.search(pattern,string,flags).group(group)
	except:s=result
	return s

def fmn(n):
	try:s=format(int(n), "8,d").replace(',','.').strip()
	except:s=str(n)
	return s

def s2u(s):return s.decode('utf-8') if isinstance(s,str) else s
def u2s(s):return s.encode('utf-8') if isinstance(s,unicode) else s
def unescape(string):return ' '.join(urllib2.re.sub('&.+;',xsearch('&(\w).+;',s,1),s) for s in string.split())
def s2c(s):
	def sc(s):i=xsearch('&#(\d+);',s);return urllib2.re.sub('&#\d+;',d.get(i,''),s) if i else s
	d={'192':'À','193':'Á','194':'Â','195':'Ă','202':'Ê','204':'Ì','205':'Í','211':'Ó','212':'Ô','217':'Ù','218':'Ú','224':'à','225':'á','226':'â','227':'ă','232':'è','233':'é','234':'ê','235':'ẽ','236':'ì','237':'í','242':'ò','243':'ó','244':'ô','245':'ỏ','249':'ù','250':'ú','253':'ý'}
	return ' '.join(sc(i) for i in s.split())
def s2c1(s):
	return ' '.join(urllib2.re.sub('&#\d+;',unichr(int(xsearch('&#(\d+);',i))),i) if xsearch('&#(\d+);',i) else i for i in s.split())
