# -*- coding: utf-8 -*-
import urllib,urllib2,urlfetch, re, os, json
from time import sleep
from utils import *
from urlfetch import get,post


from setting import notify, alert, myaddon
import random
import xbmc

def fixString(string):
	try:		
		for a, b in {'&#39;':'','&amp;':'','&':'',' ':'-','+':'-'}.iteritems():
			string = string.replace(a, b)
	except:string=''		
	return string.lower().strip()



color={'trangtiep':'[COLOR lime]','cat':'[COLOR green]','search':'[COLOR red]','phimbo':'[COLOR tomato]','phimle':'[COLOR yellow]','imdb':'[COLOR yellow]','namphathanh':'[COLOR yellow]','theloai':'[COLOR green]','quocgia':'[COLOR blue]'}

hd={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/600.1.4 Gecko/20100101 Firefox/41.0'}		
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
			notify(u'Lỗi kết nối tới: %s!'%xsearch('//(.{5,20}\.\w{2,3})',s2u(url)),'make_request')
		print 'Lỗi kết nối tới: %s!'%u2s(url);
	return resp#unicode:body=response.text		
		
def json_rw(file,dicts={},key=''):
	if dicts:makerequest(joinpath(datapath,file),json.dumps(dicts),'w')
	else:
		try:dicts=json.loads(makerequest(joinpath(datapath,file)))
		except:dicts={}
		if key:dicts=dicts.get(key,())
	return dicts

class serversList:
	def __init__(self):
		self.servers=[('anime47.com', '37'), ('tvhay.org', '41'), ('hdviet.com', '22'), ('fptplay.net', '07'), ('hayhaytv.vn', '23'), ('bilutv.com', '36'), ('phimmoi.net', '24'), ('hdonline.vn', '30'), ('megabox.vn', '17'), ('phim3s.net', '32'), ('phim14.net', '39'), ('kenh88.com', '26'), ('phimdata.com', '27'), ('phimsot.com', '29'), ('phim47.com', '28'), ('phimbathu.com', '43'), ('kphim.tv', '33'), ('phimnhanh.com', '35'), ('dangcaphd.com', '18'), ('phim.media', '40'), ('hdsieunhanh.com', '44'), ('imovies.vn', '48'), ('vuahd.tv', '21'), ('pubvn.tv', '19'), ('vietsubhd.com', '54'), ('mphim.net', '55')]
		try:self.ordinal=[int(i) for i in xrw('free_servers.dat').split(',')]
		except:self.ordinal=[]
		l=len(self.servers);update=False
		for i in range(l):
			if i not in self.ordinal:self.ordinal.append(i);update=True
		for i in self.ordinal:
			if i >= l:self.ordinal.remove(i);update=True
		if update:xrw('free_servers.dat',','.join(str(i) for i in self.ordinal))
		
	def mylist(self):
		return [self.servers[i] for i in self.ordinal]

	def move(self,server,step):#sl:server location, ol: ordinal location, step:up=-1,down=+1
		sl=self.servers.index([i for i in self.servers if i[0]==server][0])
		ol=self.ordinal.index([i for i in self.ordinal if i==sl][0])
		temp=self.ordinal[ol+step];self.ordinal[ol+step]=sl;self.ordinal[ol]=temp
		xrw('free_servers.dat',','.join(str(i) for i in self.ordinal))

	def moveDown(self,server):
		sl=self.servers.index([i for i in self.servers if i[0]==server][0])
		ol=self.ordinal.index([i for i in self.ordinal if i==sl][0])
		temp=self.ordinal[ol+1];self.ordinal[ol+1]=sl;self.ordinal[ol]=temp
		xrw('free_servers.dat',','.join(str(i) for i in self.ordinal))

	def search(self,url):
		print xread(url)
		try:j=json.loads(xsearch('\((\{.+?\})\)',xread(url)))
		except:j={}
#		if not j.get('results',{}):
#			notify(u'Tìm gần đúng','i-max.vn')
#			try:j=json.loads(xsearch('\((\{.+?\})\)',xread(url.replace('%22',''))))
#			except:j={}
#			if not j:return []
		
		def detail(l):
			title=l.get('titleNoFormatting','').encode('utf-8')
			href=l.get('unescapedUrl','').encode('utf-8')
			try:img=l['richSnippet']['cseImage']['src'].encode('utf-8')
			except:img=''
			return title,href,img
		l=[detail(i) for i in j.get('results',{}) if i.get('titleNoFormatting') and i.get('unescapedUrl')]
		
		cursor=j.get('cursor',{});currentPage=cursor.get('currentPageIndex',100);pages=cursor.get('pages',{})
		start=''.join(i.get('start','') for i in pages if i.get('label',0)==cursor.get('currentPageIndex')+2)
		if start:
			title='[COLOR lime]Page next: %d[/COLOR]'%(cursor.get('currentPageIndex')+2)
			l.append((title,start,''))
		return l

			
class fshare:
    
	def __init__(self):
		self.hd={'User-Agent':'Mozilla/5.0 Gecko/20100101 Firefox/44.0','x-requested-with':'XMLHttpRequest'}

	def fetch_data2(self,url,headers='',data=None):
		try:response=urlfetch(url,headers=self.hd,data=data)
		except:response= None
		return response

	def fetch_data(self,url, headers=None, data=None):
		if headers is None:
			headers = self.hd
		try:
			if data:
				response = urlfetch.post(url, headers=headers, data=data)
			else:
				response = urlfetch.get(url, headers=headers)
			return response
		except:return None
			
	def getLink(self,url,username='', password=''):
		login_url = 'https://www.fshare.vn/login'
		logout_url = 'https://www.fshare.vn/logout'
		download_url = 'https://www.fshare.vn/download/get'

		#username = myaddon.getSetting('usernamef')
		#password = myaddon.getSetting('usernamef')

		try:
			url_account = 'http://www.aku.vn/linksvip'
			headers = { 
				'Referer'			: 'http://aku.vn/linksvip',
				'User-Agent'		: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
			}
			response = self.fetch_data('http://www.aku.vn/linksvip',headers=headers,data={ 'url_download' : url })
			if response.status==404:response = self.fetch_data('http://aku.vn/linksvip',headers=headers,data={ 'url_download' : url })
			link_match=re.search("<a href=http://download(.*?)\starget=_blank", response.body)
			if link_match:
				return 'http://download' + link_match.group(1)

		except Exception as e:
			pass


		#print 'username: '+username
		#print 'password: '+password
			
		if len(username) == 0  or len(password) == 0:
			alert(u'Bạn chưa nhập tài khoản fshare'.encode("utf-8"))
			return
		

		
		response = self.fetch_data(login_url)
		if not response:
			return
		
		csrf_pattern = '\svalue="(.+?)".*name="fs_csrf"'

		csrf=re.search(csrf_pattern, response.body)
		fs_csrf = csrf.group(1)

		headers = { 
					'User-Agent' 	: 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36 VietMedia/1.0',
					'Cookie'		: response.cookiestring
				}
		
		data = {
				"LoginForm[email]"		: username,
				"LoginForm[password]"	: password,
				"fs_csrf"				: fs_csrf
			}

		response = self.fetch_data(login_url, headers, data)
		headers['Cookie'] = response.cookiestring
		headers['Referer'] = url
		direct_url = ''
		attempt = 1
		MAX_ATTEMPTS = 5
		file_id = os.path.basename(url)
		if response and response.status == 302:
			notify (u'Đăng nhập fshare thành công'.encode("utf-8"))
			while attempt < MAX_ATTEMPTS:
				if attempt > 1: sleep(2)
				notify (u'Lấy link lần thứ #%s'.encode("utf-8") % attempt)
				attempt += 1

				response = self.fetch_data(url, headers, data)
				print response.status
				if response.status == 200:
					csrf=re.search(csrf_pattern, response.body)
					fs_csrf = csrf.group(1)
					data = {
							'fs_csrf'					: fs_csrf,
							'ajax'						: 'download-form',
							'DownloadForm[linkcode]'	: file_id
						}
					
					response=self.fetch_data(download_url, headers, data);
					
					json_data = json.loads(response.body)
					
					if json_data.get('url'):
						direct_url = json_data['url']
						break
					elif json_data.get('msg'):
						notify(json_data['msg'].encode("utf-8"))
				elif response.status == 302:
					direct_url = response.headers['location']
					break
				else:
					notify (u'Lỗi khi lấy link, mã lỗi #%s. Đang thử lại...'.encode("utf-8") % response.status) 

			response = self.fetch_data(logout_url, headers)
			if response.status == 302:
				notify (u'Đăng xuất fshare thành công'.encode("utf-8"))
		else:
			notify (u'Đăng nhập không thành công, kiểm tra lại tài khoản'.encode("utf-8"))
		if len(direct_url) > 0:
			notify (u'Đã lấy được link'.encode("utf-8"))
		else:
			notify (u'Không được link, bạn vui lòng kiểm tra lại tài khoản'.encode("utf-8"))
			
		return direct_url
	


class fptPlay:#from resources.lib.servers import fptPlay;fpt=fptPlay(c)
	def __init__(self):
		self.hd={'User_Agent':'Mozilla/5.0','X-Requested-With':'XMLHttpRequest'}
		self.hd['referer']='https://fptplay.net/fptplay/gioi-thieu'
		self.hd['Cookie']=xrw('fptplay.cookie') if filetime('fptplay.cookie')<30 else self.login()
		
	def fpt2s(self,s):return ' '.join(re.sub('&.+;',xsearch('&(\w).+;',i),i) for i in s.split())
	
	def login(self):
		email=get_setting('mail_fptplay');password=get_setting('pass_fptplay')
		if not email:
			notify(u'Bạn đang sử dụng account Fptplay của xshare')
			email,password=urllib2.base64.b64decode('eHNoYXJlQHRoYW5odGhhaS5uZXQ6YWRkb254c2hhcmU=').split(':')
		data=urllib.urlencode({'email':email,'password':password})
		cookie=urllib2.HTTPCookieProcessor();opener=urllib2.build_opener(cookie);urllib2.install_opener(opener)
		#try:b=opener.open(self.hd['referer'])
		#except:pass
		opener.addheaders=self.hd.items();url='https://fptplay.net/user/login'
		req=urllib2.Request('https://fptplay.net/user/login',data)
		try:b=urllib2.urlopen(req,timeout=30)
		except:pass
		cookie=xcookie(cookie);print cookie
		if 'laravel_id' in cookie:notify(u'Login thành công','fptplay.net');xrw('fptplay.cookie',cookie)
		else:notify(u'Login không thành công!','fptplay.net')
		return cookie
	
	def login5(self):
		email=get_setting('mail_fptplay');password=get_setting('pass_fptplay')
		if not email:
			notify(u'Bạn đang sử dụng account Fptplay của xshare')
			email,password=urllib2.base64.b64decode('eHNoYXJlQHRoYW5odGhhaS5uZXQ6YWRkb254c2hhcmU=').split(':')
		data=urllib.urlencode({'email':email,'password':password})
		cookie=urllib2.HTTPCookieProcessor();opener=urllib2.build_opener(cookie)
		opener.addheaders=self.hd.items();url='https://fptplay.net/user/login'
		try:
			opener.open(self.hd['referer'])
			urllib2.install_opener(opener)
			urllib2.urlopen(url,data)
		except:pass
		cookie=xcookie(cookie)
		if 'laravel_id' in cookie:notify(u'Login thành công','fptplay.net');xrw('fptplay.cookie',cookie)
		else:notify(u'Login không thành công!','fptplay.net')
		return cookie
	
	def login0(self):
		email=get_setting('mail_fptplay');password=get_setting('pass_fptplay')
		if not email:
			notify(u'Bạn đang sử dụng account Fptplay của xshare')
			email,password=urllib2.base64.b64decode('eHNoYXJlQHRoYW5odGhhaS5uZXQ6YWRkb254c2hhcmU=').split(':')
		data={'email':email,'password':password}
		response=urlfetch.get('https://fptplay.net/tai-khoan');self.hd['Cookie']=response.cookiestring
		response=urlfetch.post('https://fptplay.net/user/login',headers=self.hd,data=data)
		cookie=response.cookiestring
		if 'laravel_id' in cookie:notify(u'Login thành công','fptplay.net')#;xrw('fptplay.cookie',cookie)
		else:notify(u'Login không thành công!','fptplay.net')
		return cookie
	
	def detail(self,s):
		title=self.fpt2s(xsearch('title="([^"]+?)"',s))
		if not title:title=self.fpt2s(xsearch('alt="([^"]+?)"',s))
		label=' '.join(re.findall('<p[^<]*?>(.+?)</p>',s))+title
		dir=True if 'tập' in (title+label).lower() else False
		if xsearch('(\d+/\d+)',label):dir=True;title+=' [COLOR blue]%s[/COLOR]'%xsearch('(\d+/\d+)',label)
		if 'thuyếtminh' in (title+label).replace(' ','').lower():title='[COLOR blue]TM[/COLOR] '+title
		if 'phụđề' in (title+label).replace(' ','').lower():title='[COLOR green]PĐ[/COLOR] '+title
		href=xsearch('href="([^"]+?)"',s)
		if not href:href=xsearch('data-href="(.+?)"',s)
		if 'Đang diễn ra' in s:dir=None
		img=xsearch('src="([^"]+?\.jpg)',s)
		if not img:img=xsearch('data-original="([^"]+?\.jpg)',s)
		if not img:img=xsearch('data-original="([^"]+?\.png)',s)
		return title,href,img,dir
	
	def eps(self,url,page):
		data='film_id=%s&page=%d'%(xsearch('(\w{20,30})',url),page);items=[]
		b=xread('https://fptplay.net/show/episode',self.hd,data)
		for s in [i for i in re.findall('(<li.+?/li>)',b,re.S) if '"title_items"' in i]:
			title=xsearch('title="(.+?)"',s)
			epi=xsearch('<p class="title_items">.+? (\d+)',s)
			if epi:title=epi+'-'+title
			if 'phụđề' in title.replace(' ','').lower():title='[COLOR green]PĐ[/COLOR] '+title
			elif 'thuyếtminh' in title.replace(' ','').lower():title='[COLOR blue]TM[/COLOR] '+title
			href=xsearch('(\w{20,30})',xsearch('href="(.+?)"',s))+'?'+xsearch('id="episode_(\d{1,4})"',s)
			items.append((self.fpt2s(title),href))

		if '&rsaquo;&rsaquo;' in b:items.append(('[COLOR lime]Các tập tiếp theo ...[/COLOR]',''))
		return items
	
	def liveChannals(self):
		b=xread('https://fptplay.net/livetv').split('"col-xs-6 col-sm-5 col-md-4">')
		items=[]
		for s in [i for i in b if ' class="livetv_header' in i]:
			i=xsearch('<span class="livetv_header Regular pull-left"[^>]*>(.+?)</span>',s)
			items.append((self.fpt2s(i),'sep',''))
			for title,href,img,dir in [self.detail(i) for i in re.findall('(<a class="tv_channel.+?/a>)',s,re.S)]:
				items.append((title,href,img))
		return items
		
	def liveChannals1(self):
		b=xread('https://fptplay.net/livetv')
		items=[]
		for s in re.findall('(<a class="tv_channel.+?/a>)',b,re.S):
			title=xsearch('title="(.+?)"',s)
			href=xsearch('data-href="(.+?)"',s)
			img=xsearch('data-original="(.+?)\?',s)
			items.append((self.fpt2s(title),href,img))
		return items
		
	def liveLink(self,url):
		id=urllib2.os.path.basename(url)
		if not id:id='vtv3-hd'
		data='mobile=web&quality=3&type=newchannel&id=%s'%id
		b=xread('https://fptplay.net/show/getlinklivetv',self.hd,data)
		try:link=json.loads(b).get('stream')
		except:link=''
		return link

class hayhayvn:
	def __init__(self):
		self.hd={'User-Agent':'Mozilla/5.0','Referer':'http://www.hayhaytv.vn/dieu-khoan-su-dung.html'}
		
	def getLink(self,url):
		b=xread(url)
		link=xsearch('file.{,5}"(.+?)"',b);sub=''
		if link:sub=xsearch("var track.{,5}'(.+?)'",b)
		else:
			url='http://www.hayhaytv.vn/getsource/%s'%xsearch("FILM_KEY = '(.+?)'",b)
			b=xread(url,self.hd)
			try:j=eval(b)
			except:j=[]
			links=[(i.get('file').replace('\\',''),i.get('label')) for i in j]
			for href,r in ls([(i[0],rsl(i[1])) for i in links]):
				g=xget(href)
				if g:link=g.geturl();break
		return link,sub
		
class hdonline:
	def __init__(self):
		self.home='http://hdonline.vn'

	def additems(self,body,mode):
		items=[]
		for content in re.findall('<li>\s*<div class="tn-bxitem">(.+?)</li>',body,re.S):
			titleVn=xsearch('<p class="name-en">(.+?)</p>',content).strip()
			titleEn=xsearch('<p class="name-vi">(.+?)</p>',content).strip()
			href=xsearch('<a href="(.+?)"',content).strip()

			#thoiluong = xsearch('Thời lượng:</strong> (.+?)</li>',content)
			IMDb=xsearch('<p>Đánh giá:(.+?)</p>',content)
			year=xsearch('<p>Năm sản xuất:(.+?) </p>',content).strip()
			#quocgia=xsearch('Quốc gia:</strong> (.+?)</li>',content)
			theloai=xsearch('<span class="tn-pcolor1">(.+?)</span>',content)
			desc=xsearch('<div class="tn-contentdecs mb10">(.+?)</div>',content)											
			
			href='http://hdonline.vn'+href
			img=xsearch('<img src="(.+?)"',content).strip()
			
			title = titleVn + ' - ' + titleEn
			if year:title = title + ' [B]' + str(year) + '[/B]'
			if IMDb:title+=color['imdb']+' IMDb: '+IMDb+'[/COLOR]'					
			
			if 'moicapnhat' in mode:
				#title+='[B]'+quocgia+'[/B] '
				title+=' '+color['theloai']+theloai+'[/COLOR]'
			
			esp = xsearch('Số Tập: (.+?) </p>',content)
			
			isFolder=True
			if 'episodes' in content:
				title = '(' + esp + ') ' + title
			
				v_mode='episodes'
				if 'serverlist' in mode:							
					title = '[HDO] ' + title
				elif 'search' in mode:							
					v_mode='serverlist_phim-bo'												
			else:
				if 'serverlist' in mode:
					title = '[HDO] ' + title
					v_mode='stream';isFolder=False					
					
					filmid = xsearch('-(\d+?).html',href)
					plg='plugin://plugin.video.hkn.hdonline/?action=ListEpisodes&filmid='
					href = plg + str(filmid)											
				elif 'search' in mode:
					v_mode='serverlist_phim-le'
				elif 'moicapnhat' in mode:
					v_mode='stream';isFolder=False
					
					
			items.append((title,href,'%s&query=%s'%(v_mode,titleVn+'[]'+titleEn+'[]'+str(year)),img,isFolder))
			
		return items
		
	def eps(self,id,page):
		b=xread('http://hdonline.vn/episode/ajax?film=%s&episode=&page=%d&search='%(id,page))
		items=[('http://hdonline.vn'+j[0],j[1]) for j in re.findall('href="(.+?)"[^>]+>(\d+)</a>',b)]
		
		pn=xsearch('<a class="active"[^<]+>\d+</a><[^<]+>(\d+)</a>',b)
		if pn:items.append(('[COLOR lime]Các tập tiếp theo...[/COLOR]',pn))
		return items		
		
class hdviet:
	def __init__(self):
		self.hd={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/600.1.4 Gecko/20100101 Firefox/41.0'}
		
	def additems(self,body,mode):
		items=[]
	
		pattern='<li class="mov-item".+?href="(.+?)".+?src="(.+?)".+?title="Phim (.+?)".+?<span(.+?) data-id="(.+?)">'	
		data=re.findall(pattern,body,re.DOTALL);listitems=list()
		for href,img,title,detail,id_film in data:
			epi=xsearch('"labelchap2">(\d{1,3})</span>',detail);title=unescape(title)
			res=xsearch('id="fillprofile" class="icon-(.+?)11">',detail)
			res='[COLOR gold]SD[/COLOR]' if 'SD' in res else '[COLOR gold]HD[/COLOR]%s'%res
			phim18=xsearch('class="children11".+?>(.+?)</label></span>',detail)
			TM=xsearch('id="fillaudio" class="icon-(.+?)">',detail)
			TM='%s[COLOR green]%s[/COLOR][COLOR red]%s[/COLOR]'%(res,TM,phim18)
			plot=xsearch('<span class="cot1">(.+?)</span>',detail)
			year=xsearch('<span class="chil-date".+?>(.*?)</label></span>',detail)
			act=', '.join(s for s in re.findall('<a href="http://movies.hdviet.com/dien-vien/.+?">(.+?)</a>',detail))
			drt=', '.join(s for s in re.findall('<a href="http://movies.hdviet.com/dao-dien/.+?">(.+?)</a>',detail))
			IMDb=xsearch('<span class="fl-left">.+?<span>(.+?)</span>',detail)
			upl=xsearch('<span class="fl-right">.+?<span>(.+?)</span>',detail)

			if '(' in title and ')' in title:title=title.replace('(','[B]').replace(')','[/B]')
			if IMDb:title+=color['imdb']+' IMDb: '+IMDb+'[/COLOR]'			
			
			href='hdviet.com|'+str(id_film)
			
			#if 'moicapnhat' in mode:
				#title+='[B]'+quocgia+'[/B] '
				#title+=color['theloai']+theloai+'[/COLOR]'

			
			isFolder=True
			v_mode=''
			titleVn=title
			titleEn=title
			if epi:
				title = '(' + epi + ') ' + title
				v_mode='episodes';
				if 'serverlist' in mode:							
					title = '[HDViet] ' + title
					title = color['phimbo'] + title + '[/COLOR]'							
				elif 'category' in mode or 'search' in mode:
					v_mode='serverlist_phim-bo'	
			else:
				if 'serverlist' in mode:
					title = '[HDViet] ' + title
					v_mode='stream';isFolder=False					
					titleEn=href
					href='hdviet.com'						
				elif 'search' in mode:
					v_mode='serverlist_phim-le'
				elif 'moicapnhat' in mode:
					v_mode='stream';isFolder=False
					
			items.append((title,href,'%s&query=%s'%(v_mode,titleVn+'[]'+titleEn+'[]'+str(year)),img,isFolder))					
			
		return items
		
	def getResolvedUrl(self,id_film,loop=0):#Phim le/phim chieu/ke doi dau thien ac		
		data=json_rw('hdviet.cookie')
		token = data.get('access_token')
		#token = '22bb07a59d184383a3c0cd5e3db671fc'
		#id_film=id_film.replace('_e','&ep=')
		direct_link='https://api-v2.hdviet.com/movie/play?accesstokenkey=%s&movieid=%s'%(token,id_film)		
				
		result=xread(direct_link)
		try:links=json.loads(result)["r"]
		except:links=dict()
		
		try:print json.dumps(links,indent=2,ensure_ascii=True)
		except:pass			
		
		link=links.get('LinkPlay')
		#if not link:return '',''
		#elif '0000000000000000000000' in link:
			#data=login_hdviet();links=getlinkhdviet(data.get('access_token'),id_film);link=links.get('LinkPlay')	
		
		if link:
			#max_resolution='_1920_' if myaddon.getSetting('hdvietresolution')=='1080' else '_1280_'
			max_resolution='_1920_'
			resolutions=['_1920_','_1885_','_1876_','_1866_','_1792_','_1280_','_1024_','_800_','_640_','_480_']
			if '_e' in id_film:link=re.sub('%s_e\d{1,3}_'%id_film.split('_')[0],'%s_'%id_film,link)
			
			r=''.join([s for s in resolutions if s in link]);response=''
			if r:
				href=link[:link.rfind(r)]+link[link.rfind(r):].replace(r,'%s')
				for i in resolutions:
					if i>max_resolution:continue
					response=make_request(href%i)
					if len(response)>0:link=href%i;break
			else:
				href=link.replace('playlist.m3u8','playlist_h.m3u8')
				response=make_request(href)
				if not response or '#EXT' not in response:
					for s in range(1,6):
						#print re.sub('http://n0\d.vn-hd.com','http://n0%d.vn-hd.com'%s,href)
						if 'http://n0%d'%s in href:continue
						elif re.search('http://n0\d.vn-hd.com',href):
							response=make_request(re.sub('http://n0\d.vn-hd.com','http://n0%d.vn-hd.com'%s,href))
						if response and  '#EXT' in response:break
				if not response:response=make_request(link)
			
			if response and '#EXT' in response:
				items=re.findall('RESOLUTION=(\d+?)x.*\s(.+m3u8)',response)
				if items:
					res=0;hr=''
					for r,h in items:
						#print r,h
						if int(r)>res:res=int(r);hr=h
					if hr and 'http://' in hr:link=hr
					else:link=os.path.dirname(link)+'/'+hr
				else:
					items=re.findall('(.+m3u8)',response)
					if items and 'http://' in items[0]:link=items[len(items)-1]#;print items[0]
					elif items:link=os.path.dirname(link)+'/'+items[0]
				
			else:link=''
		if not link:return '',''
		audio=links.get('AudioExt',list());audioindex=-1;linksub=''
		if not audio:pass
		elif len(audio)>1:
			#audio_choice=myaddon.getSetting('hdvietaudio')
			audio_choice='Hỏi khi xem-'
			if audio_choice=='Hỏi khi xem':
				title=u'[COLOR green]Chọn Audio[/COLOR]';line1= u'[COLOR yellow]Vui lòng chọn Audio[/COLOR]'
				audioindex=notify_yesno(title,line1,'',audio[0].get("Label",'0'),audio[1].get("Label",'1'))
			else:audioindex=0 if u2s(audio[0].get("Label")) in audio_choice else 1
			if 'Thuyết' not in u2s(audio[audioindex].get("Label")):linksub='yes'#bật cờ download sub
			try:link=link+'?audioindex=%d'%(int(audio[audioindex].get("Index",'0'))-1)
			except:pass
		elif u2s(audio[0].get("Label"))=='Thuyết Minh':audioindex=0
		if audioindex<0 or linksub:
			for source in ['Subtitle','SubtitleExt','SubtitleExtSe']:
				try:linksub=links[source]['VIE']['Source']
				except:linksub=''
				if linksub:break
		#print 'getResolvedUrl: %s - %s'%(link,linksub)
		return link,linksub		
		
class phimmoi:		
	def additems(self,body,mode):
		items=[]
		
		for s in re.findall('(<li class="movie-item">.+?</li>)',body,re.DOTALL):
			#title=xsearch('title="(.+?)"',s)
			titleVn=xsearch('<span class="movie-title-1">(.+?)</span>',s)
			titleEn=xsearch('<span class="movie-title-2">(.+?)</span>',s)
			#duration=xsearch('>(\d{1,3}.?phút)',s)
			#label=xsearch('"ribbon">(.+?)</span>',s)
			#if label:title+=' [COLOR green]%s[/COLOR]'%label
			href=xsearch('href="(.+?)"',s)
			img=xsearch('url=(.+?)%',s)
			
			b=xread('http://www.phimmoi.net/'+href)
			thoiluong = xsearch('Thời lượng:</dt><dd class="movie-dd">(.+?)</dd>',b)
			IMDb = xsearch('<dd class="movie-dd imdb">(.+?)</dd>',b)			
			quocgia=xsearch('Quốc gia:</strong> (.+?)</li>',b)
			theloais=xsearch('Thể loại:</dt><dd class="movie-dd dd-cat">(.+?)</dd>',b)
			
			theloai=''
			i=1
			theloais=re.findall('<a class="category" href=".+?" title=".+?">(.+?)</a>',theloais,re.DOTALL)
			for item in theloais:				
				if item!='Phim lẻ' and item!='Phim bộ':
					theloai+=item
					if i<len(theloais)-1:theloai+=', '
				i+=1
			
			#desc=xsearch('<div class=\'des\'>(.+?)</div>',b)

			if 'Năm:</dt><dd class="movie-dd">' in b:
				year = xsearch('Năm:</dt><dd class="movie-dd">.+?(\d{1,4})</a>',b,1,re.DOTALL)
			elif 'Ngày phát hành:</dt><dd class="movie-dd">' in b:
				year = xsearch('Ngày phát hành:</dt><dd class="movie-dd">.+?/.+?/(.+?)</dd>',b,1,re.DOTALL)
			else:
				year = xsearch('Ngày ra rạp:</dt><dd class="movie-dd">.+?/.+?/(.+?)</dd>',b,1,re.DOTALL)			
				
			title = titleVn + ' - ' + titleEn
			if year:title = title + ' [B]' + str(year) + '[/B]'
			if IMDb:title+=color['imdb']+' IMDb: '+IMDb+'[/COLOR]'			
				
			if 'moicapnhat' in mode:
				#title+='[B]'+quocgia+'[/B] '
				title+=' '+color['theloai']+theloai+'[/COLOR]'
			
			
				
			eps=xsearch('Tập ?(\d{,4}/\d{,4}|\?/\d{,4}|\d{,4})',s)
			if not eps:
				epi=xsearch('class="eps">Trọn bộ ?(\d{1,4}) ?tập</div>',s)
				if epi:eps='%s/%s'%(epi,epi)
			else:epi=eps.split('/')[0]
			try:epi=int(epi)
			except:epi=0
			
			if xsearch('<dd class="movie-dd status">Trailer',b,0):continue
					
			isFolder=True;v_mode=''
			if epi>1 or 'phút/tập' in s:
				title = '(' + eps + ') ' + title
				
				v_mode='episodes'
				if 'serverlist' in mode:							
					title = '[PhimMoi] ' + title
				elif 'search' in mode:
					v_mode='serverlist_phim-bo'	
			else:
				if 'serverlist' in mode:
					title = '[PhimMoi] ' + title
					v_mode='stream';isFolder=False					
				elif 'search' in mode:
					v_mode='serverlist_phim-le'	
				elif 'moicapnhat' in mode:
					v_mode='stream';isFolder=False
			
			isFolder=True
			#href='http://www.phimmoi.net/'+href
			items.append((title,href,'%s&query=%s'%(v_mode,titleVn+'[]'+titleEn+'[]'+str(year)),img,isFolder))
											
		return items		

class megabox:		
	def __init__(self):
		self.hd={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/600.1.4 Gecko/20100101 Firefox/41.0'}
		
	def additems(self,body,mode):
		items=[]
		
		for content in re.findall('<div class="item">(.+?)</div><!--',body,re.S):
			item=re.search('src="(.+?)">\s*.*<span class="features">\s*</span>\s*</a>\s*<div class="meta">\s*<h3 class="H3title">\s*<a href="(.+?)">(.+?)</a>',content)
			if item:
				#title=item.group(3)
				href=item.group(2)
				img=item.group(1)
				
				thoiluong = xsearch('Thời lượng:</strong> (.+?)</li>',content)
				IMDb = xsearch('<span class=\'rate\'>(.+?)</span>',content)
				year = xsearch('Năm phát hành:</strong> .+?-.+?-(.+?)</li>',content)
				title=xsearch('<h3 class=\'H3title\'>(.+?)</h3>',content).replace(' '+year, '')
				quocgia=xsearch('Quốc gia:</strong> (.+?)</li>',content)
				theloai=xsearch('Thể loại:</strong> (.+?)</li>',content)
				desc=xsearch('<div class=\'des\'>(.+?)</div>',content)

				try:					
					titleVn = title.split(" (")[0]
					titleEn = title.split(" (")[1].replace(')','')
					title = titleVn + ' - ' + titleEn
					if year:title = title + ' [B]' + str(year) + '[/B]'
				except:titleVn='';titleEn=title
				if IMDb:title+=color['imdb']+' IMDb: '+IMDb+'[/COLOR]'
				
				if 'moicapnhat' in mode:					
					title+=' [B]'+quocgia+'[/B]'
					title+=' '+color['theloai']+theloai+'[/COLOR]'
				
				esp = xsearch('class=.esp.><i>(.+?)</span>',content).replace('</i>','')				
				#count-view=xsearch('<span class=\'count-view\'><i></i>(.+?)</span>',content).strip()
							
				isFolder=True
				v_mode=''
				if esp:
					title = '(' + esp + ') ' + title
					
					v_mode='episodes'
					if 'serverlist' in mode:							
						title = '[MegaBox] ' + title					
					elif 'search' in mode:
						v_mode='serverlist_phim-bo'	
				else:
					if 'serverlist' in mode:
						title = '[MegaBox] ' + title
						v_mode='stream';isFolder=False					
					elif 'search' in mode:
						v_mode='serverlist_phim-le'
					elif 'moicapnhat' in mode:
						v_mode='stream';isFolder=False
				
				v_query=fixString(titleEn+'[]'+titleVn+'[]'+str(year))
				items.append((title,href,'%s&query=%s'%(v_mode,v_query),img,isFolder))
											
		return items		
		
	def getLink(self,url):		
		content = make_request(url)
		links = re.compile('var iosUrl = "(.+?)";').findall(content)
		  
		link=''
		if len(links) > 0:
			link = links[0]
		if 'youtube' in link:
			link = url.replace('https://www.youtube.com/watch?v=', 'plugin://plugin.video.youtube/?action=play_video&videoid=')
		else:
			link = link.replace('media21.megabox.vn', '113.164.28.47')
			link = link.replace('media22.megabox.vn', '113.164.28.48')		
			link = link+'|'+urllib.urlencode(hd)
		return link
		
class phimnhanh:				
	def __init__(self):
		self.hd={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/600.1.4 Gecko/20100101 Firefox/41.0'}
		
	def additems(self,body,mode):
		items=[]

		hrefs=[]
		for  s in re.findall('(<li  class="serial">.+?</li>)',body,re.DOTALL):
			href=xsearch('href="(.+?)"',s)
			if href not in hrefs:hrefs.append(href)
			else:continue
			#title=xsearch('title="(.+?)"',s)
			titleVn=xsearch('<span class="title display">(.+?)</span>',s)
			titleEn=xsearch('<span class="title real">(.+?) \(',s)
			year=xsearch('<span class="title real">.+? \((.+?)\)</span>',s)
			img=xsearch('data-original=="(.+?)"',s)
			label=xsearch('<span class="m-label q">(.+?)</span>',s)
			lang=xsearch('<span class="m-label lang">(.+?)</span>',s)
			IMDb=xsearch('<span class="m-label imdb"><span class="rate">(.+?)</span>',s)
			ep=xsearch('<span class="m-label ep">(.+?)</span>',s)
			if 'tập' in ep:esp=ep;thoiluong=''
			else:thoiluong=ep;esp=''
			
			title = titleVn + ' - ' + titleEn
			if year:title = title + ' [B]' + str(year) + '[/B]'
			if IMDb:title+=color['imdb']+' IMDb: '+IMDb+'[/COLOR]'
			

			#if 'moicapnhat' in mode:
				#title+='[B]'+quocgia+'[/B] '
				#title+=color['theloai']+theloai+'[/COLOR]'

			
			isFolder=True
			v_mode=''
			if esp:
				title = '(' + esp + ') ' + title
				
				v_mode='episodes'
				if 'serverlist' in mode:							
					title = '[PhimNhanh] ' + title					
				elif 'search' in mode:
					v_mode='serverlist_phim-bo'	
			else:
				if 'serverlist' in mode:
					title = '[PhimNhanh] ' + title
					v_mode='stream';isFolder=False					
				elif 'search' in mode:
					v_mode='serverlist_phim-le'
				elif 'moicapnhat' in mode:
					v_mode='stream';isFolder=False
						
			items.append((title,href,'%s&query=%s'%(v_mode,titleVn+'[]'+titleEn+'[]'+str(year)),img,isFolder))
		return items	
			
		np=xsearch('<a href="([^>]+?)" rel="next">',body)
		if np:
			np=np.replace('amp;','');pn=xsearch('page=(\d+?)\Z',np)
			ps=xsearch('<a href="[^>]+?">(\d+?)</a></li> <li><a href="[^>]+?" rel="next">',body)
			t=color['trangtiep']+' Trang tiep theo...trang %s/%s[/COLOR]'%(pn,ps)
			#addir_info(t,np,ico,'',mode,page+1,query,True)
			
	def getLink(self,url):					
		
		a=make_request(url.replace('/phim/','/xem-phim/'))
		link=xsearch('playlist: "(.+?)"',a);a=make_request(link)
		for s in re.findall('(label="\d+p")',a):a=re.sub(s,'label="'+xsearch('label="(\d+)p"',s)+'"',a)
		a=a.replace('hd1080','1080').replace('hd720','720').replace('large','640').replace('medium','480')
		items=re.findall('file[^"]+"(.+?)"[^"]+"(\d+)"',a)
		items=sorted(items, key=lambda k: int(k[1]),reverse=True)		
		if items:
			link=''
			for href,label in items:
				response=make_request(href.replace('amp;',''),resp='o')
				if response and response.status==302:
					href=response.headers.get('location')
					if make_request(href,resp='s')==200:link=href;break
				if not link:xbmc.sleep(1000)
		else:
			link=xsearch('file="(.+?)"',a).replace('amp;','')
			if link and '.youtube.com' in link:
				link = link.replace('https://www.youtube.com/watch?v=', 'plugin://plugin.video.youtube/?action=play_video&videoid=')
		
		return link