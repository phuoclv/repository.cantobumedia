# -*- coding: utf-8 -*-
import urllib,urllib2,urlfetch, re, os, json
from utils import *
from urlfetch import get,post

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
		try:j=json.loads(xsearch('\((\{.+?\})\)',xread(url)))
		except:j={}
		if not j.get('results',{}):
			mess(u'Tìm gần đúng','i-max.vn')
			try:j=json.loads(xsearch('\((\{.+?\})\)',xread(url.replace('%22',''))))
			except:j={}
			if not j:return []
		
		def detail(l):
			title=l.get('titleNoFormatting','').encode('utf-8')
			href=l.get('unescapedUrl','').encode('utf-8')
			try:img=l['richSnippet']['cseImage']['src'].encode('utf-8')
			except:img=''
			return title,href,img
		l=[detail(i) for i in j.get('results',{}) if i.get('titleNoFormatting') and i.get('unescapedUrl')]
		
		cursor=j.get('cursor',{});currentPage=cursor.get('currentPageIndex',1000);pages=cursor.get('pages',{})
		start=''.join(i.get('start','') for i in pages if i.get('label',0)==cursor.get('currentPageIndex')+2)
		if start:
			title='[COLOR lime]Page next: %d[/COLOR]'%(cursor.get('currentPageIndex')+2)
			l.append((title,start,''))
		return l

class fshare:#https://www.fshare.vn/home/Mục chia sẻ của thaitni/abc?pageIndex=1
    
	def __init__(self, username='', password='', id=''):
		self.url_id=id
		self.myFavourite_id=''
		self.token=''
		self.logged=None
		self.hd={'User-Agent':'Mozilla/5.0 Gecko/20100101 Firefox/44.0','x-requested-with':'XMLHttpRequest'}
		if username:
			self.login(username,password)
			if self.logged=='success':
				myfolder=self.get_myFolder()
				self.myFavourite_id=''.join(xsearch('(\w{10,})',s[1]) for s in myfolder if s[0]=='xshare_favourite')
				if not self.myFavourite_id:
					self.myFavourite_id=self.add_folder(folder_name='xshare_favourite',in_dir_id='0')

	def fetch(self,url,data=None):
		try:response=urlfetch.fetch(url,headers=self.hd,data=data)
		except:response= None
		return response
	
	def login(self,username,password):
		response = self.fetch('https://www.fshare.vn/login')
		if not response or response.status!=200:mess('Connect to fshare.vn fails','Fshare.vn')
		else:
			fs_csrf=xsearch('value="(.+?)" name="fs_csrf"',response.body)
			data={"LoginForm[email]":username,"LoginForm[password]":password,"fs_csrf":fs_csrf}
			self.hd['Cookie']=response.cookiestring
			response = self.fetch('https://www.fshare.vn/login',data)
			if response and response.status==302:
				self.hd['Cookie']=response.cookiestring;self.logged='success'
				mess(u'Login thành công','Fshare.vn')
			else:mess(u'Login không thành công!','Fshare.vn')
	
	def logout(self):
		if self.logged:
			response = self.fetch('https://www.fshare.vn/logout')
			if response and response.status==302:self.logged=None;mess(u'Logout thành công','Fshare.vn')
			else:mess(u'Logout không thành công!','Fshare.vn')
	
	def get_maxlink(self,url):
		response=self.fetch(url);result=pw=None
		if not response:print 'Not response'
		elif response.status==302:result=response.headers['location']
		elif response.status==200:
			if re.search('<title>.*Lỗi 404.*</title>|"index-404"',response.body):
				mess(u'Tập tin quý khách yêu cầu không tồn tại!','Fshare.vn');result='fail'
			elif 'sử dụng nhiều địa chỉ IP' in response.body:
				mess(u'Quý khách đang sử dụng nhiều địa chỉ IP để tải xuống!','Fshare.vn',10000)
				result='fail'
			elif re.search('<i class="fa fa-star">',response.body):mess('Your Fshare acc is FREE','Fshare.vn')
			
			if re.search('class="fa fa-lock"',response.body):
				pw=get_input(u'Hãy nhập: Mật khẩu tập tin')
				if pw:
					try:
						data={'fs_csrf':xsearch('value="(.+?)" name="fs_csrf"',response.body),
						'DownloadForm[pwd]':pw,'ajax':'download-form','DownloadForm[linkcode]':url.split('/')[4]}
						response=self.fetch('https://www.fshare.vn/download/get',data).json
					except:response={}

					if not response:mess(u'Get maxspeed link fail!','Fshare.vn');result='fail'
					elif response.get('url'):result=response.get('url')
					elif response.get('DownloadForm_pwd'):mess(u'Mật khẩu không chính xác!','Fshare.vn')
					else: print response
			elif re.search('action="/download/get"',response.body):
				href='https://www.fshare.vn'+xsearch('action="(/download/get)"',response.body)
				fs_csrf=xsearch('value="(.+?)" name="fs_csrf"',response.body)
				downloadForm=xsearch('id="DownloadForm_linkcode" type="hidden" value="(.+?)"',response.body)
				data={'fs_csrf':fs_csrf,'DownloadForm[pwd]':'','DownloadForm[linkcode]':downloadForm,
						'ajax':'download-form','undefined':'undefined'}
				response=self.fetch(href,data)
				try:result=response.json.get('url')
				except:pass
		return result
	
	def get_token(self,url='https://www.fshare.vn/home'):
		self.hd['x-pjax']='true'
		response=self.fetch(url)
		if not response or response.status!=200:mess(u'Get home page fail!','Fshare.vn');return ''
		self.token=xsearch('data-token="(.+?)"',response.body)
		return self.token
	
	def get_folder(self,url):
		if '/file/' in url:return {'pagename':'','items':[]}
		response=self.fetch(url)
		body=response.body if response and response.status==200 else ''
		pagename=xsearch('<title>(.+?)</title>',body).replace('Fshare - ','')
		items=list()
		for content in re.findall('<div class="pull-left file_name(.+?)<div class="clearfix"></div>',body,re.S):
			item=re.search('data-id="(.+?)".+?href="(.+?)".+?title="(.+?)"',content)
			if item:
				size=xsearch('<div class="pull-left file_size align-right">(.+?)</div>',content).strip()
				id=item.group(1);type='file' if 'file' in item.group(2) else 'folder';title=item.group(3)
				if type=='file':link='https://www.fshare.vn/file/%s'%id
				elif re.search('(\w{10,20} )',title):
					iD=xsearch('(\w{10,20} )',title)
					if 'FOLDER' in iD:link='https://www.fshare.vn/folder/%s'%iD.replace('FOLDER','')
					elif 'FILE' in iD:link='https://www.fshare.vn/file/%s'%iD.replace('FILE','')
					else:
						link='https://www.fshare.vn/folder/%s'%iD
						try:
							if self.fetch(link).status!=200:link='https://www.fshare.vn/file/%s'%iD
						except:pass
					title=' '.join(s for s in title[title.find(' '):].split())
				else:link='https://www.fshare.vn/folder/%s'%id;title=' '.join(s for s in title.split())
				date=xsearch('"pull-left file_date_modify align-right">(.+?)</div>',content).strip()
				items.append((title,link,id,size,date))
		return {'pagename':pagename,'items':items}
	
	def myFshare_add(self,url,name):
		if not self.url_id:mess(u'Hãy set "Thư mục chia sẻ của tôi trên Fshare!"','myFshare');return
		id=url.split('/')[4]
		if [s for s in self.get_folder('https://www.fshare.vn/folder/'+self.url_id)['items'] if id in s[0]]:
			mess(u'This item already in MyFshare!','Fshare.vn');return
		token=self.get_token();name=id+('FOLDER ' if 'folder' in url else 'FILE ')+name
		data='{"token":"%s","name":"%s","in_dir":"%s"}'%(token,name,self.url_id)
		response=self.fetch('https://www.fshare.vn/api/fileops/createFolder',data)
		if response and response.status==200:mess(u'Add a item to MyFshare success','Fshare.vn')
		else:mess(u'Add a item to MyFshare fail!','Fshare.vn')
	
	def myFshare_remove(self,url):
		id=[s[2] for s in self.get_folder('https://www.fshare.vn/folder/'+self.url_id)['items'] if url==s[1]]
		id=id[0] if id else '';data='{"token":"%s","items":["%s"]}'%(self.get_token(),id.strip())
		response=self.fetch('https://www.fshare.vn/api/fileops/delete',data)
		if response and response.status==200:result=True;mess(u'Remove a item from MyFshare success','Fshare.vn')
		else:result=False;mess(u'Remove a item from MyFshare fail!','Fshare.vn')
		return result
	
	def myFshare_rename(self,url,new_name):
		id=[s[2] for s in self.get_folder('https://www.fshare.vn/folder/'+self.url_id)['items'] if url==s[1]]
		id=id[0] if id else '';data='{"token":"%s","new_name":"%s","file":"%s"}'%(self.get_token(),new_name,id)
		response=self.fetch('https://www.fshare.vn/api/fileops/rename',data)
		if response and response.status==200:result=True;mess(u'Rename a item in MyFshare success','Fshare.vn')
		else:result=False;mess(u'Rename a item in MyFshare fail!','Fshare.vn')
		return result
	
	def myFshare_upload(self,name,size,content):
		response=self.fetch('https://www.fshare.vn/home');result=False
		if not response or response.status!=200:
			response=self.fetch('https://www.fshare.vn/home')
			if not response or response.status!=200:mess(u'Get home page fail!','Fshare.vn');return result
		token=xsearch('data-token="(.+?)"',response.body)
		path=xsearch('data-id="%s" path-origin = "" data-path="(.+?)"'%self.url_id,response.body)
		SESSID=xsearch('session_id=(.+?)\W',str(self.hd))
		data='{"SESSID":"%s","name":"%s","size":"%s","path":"%s","token":"%s","secured":1}'%(
			SESSID,name,size,path,token)#;print data
		response=self.fetch('https://www.fshare.vn/api/session/upload',data)
		if response and response.status==200:
			response=self.fetch(response.json['location'],content)
			if response and response.status==200:result=True;mess(u'Upload file to MyFshare success','Fshare.vn')
		if result is False:mess(u'Upload file to MyFshare fail!','Fshare.vn')#;print response.status
		return result
	
	def Favorite_add(self,url):
		data='{"token":"%s","link":"%s"}'%(self.get_token(),url)
		response=self.fetch('https://www.fshare.vn/api/fileops/AddFavorite',data)
		if response and response.status==200:
			result=True;mess(u'Add a item to MyFshare Favorite success','Fshare.vn')
		else:result=False;mess(u'Add a item to MyFshare Favorite fail!','Fshare.vn')
		return result
	
	def Favorite_remove(self,name):
		data='{"token":"%s","items":["%s"],"status":0}'%(self.get_token(),name)
		response=self.fetch('https://www.fshare.vn/api/fileops/ChangeFavorite',data)
		if response and response.status==200:
			result=True;mess(u'Remove a item from MyFshare Favorite success','Fshare.vn')
		else:result=False;mess(u'Remove a item from MyFshare Favorite fail!','Fshare.vn')
		return result
	
	def add_folder(self,folder_name,in_dir_id='0'):
		token=self.get_token()
		#{"token":"49e3b84c0e4f1353491fed40eb964f485d091574","name":"abc","in_dir":"8NDKF9NA7T9I"}
		data='{"token":"%s","name":"%s","in_dir":"%s"}'%(token,folder_name,in_dir_id)
		response=self.fetch('https://www.fshare.vn/api/fileops/createFolder',data)
		try:result=response.json;result_code=result.get('code')
		except:result_code=0
		if result_code==200:
			#mess(result.get('msg')+' - '+result.get('folder',{}).get('name'),'Fshare.vn')
			result=result.get('folder',{}).get('linkcode')
		else:mess(u'Add folder fail !','Fshare.vn');result=''
		return result #folder ID created, empty if fail
	
	def remove_folder(self,parent_folder,folder_id):
		data='{"token":"%s","items":["%s"]}'%(self.get_token(),folder_id)
		self.hd['Referer']='https://www.fshare.vn/home/xshare_favourite'
		response=self.fetch('https://www.fshare.vn/api/fileops/delete',data)
		try:result=response.json;result_code=result.get('code')
		except:result_code=0
		if result_code==200:result=result.get('msg')
		else:result=''
		return result
	
	def get_myFolder(self,folder_name=''):
		self.hd['x-pjax']='true'
		url='https://www.fshare.vn/home/'+folder_name+'?_pjax=%23pjax_content'
		response=self.fetch(url)
		if response and response.status==200:
			items=re.findall('dl="(.+?)".+?f-name= "(.+?)"',response.body)
			items=[(s[1],'https://www.fshare.vn'+s[0]) for s in items]
		else:items=[]
		return items #(folder name,public url)
	
	def upload_file(self,fn):#Chua xong
		size=os.path.getsize(fn);name=os.path.basename(fn);path='/'
		session_id=xsearch('session_id=(.+?)\W',str(self.hd))
		data='{"SESSID":"%s","name":"%s","path":"%s","secured":"1","size":"%d","token":"%s"}'%(session_id,name,path,size,self.get_token())
		response=self.fetch('https://www.fshare.vn/api/session/upload',data)
		
		if response and response.status==200:
			try:response=urlfetch.fetch(response.json['location'].replace('http:','https:'),headers=self.hd,data=data)
			except:response= None
			if response and response.status==200:
				result=True;mess(u'Upload file to MyFshare success','Fshare.vn')
		#print response.status

	def remove_file(self,id):
		data='{"token": "%s", "items":["%s"]}'%(self.get_token(),id)
		response=self.fetch('https://www.fshare.vn/api/fileops/delete',data)
		
	def myFavourites_add(self,s):
		result=[]
		if not self.myFavourite_id:mess('Your Fshare Favourite ID not found!')
		else:
			import time
			loop=True;prefix=int(time.time());count=0;s=urllib2.base64.urlsafe_b64encode(s)
			while loop:
				folder_name='%d.%d.'%(prefix,count)+s[:230]
				if len(s)>230:s=s[230:];count+=1
				else:loop=False
				i=self.add_folder(folder_name,self.myFavourite_id)
				if i:result.append(i)
				else:loop=False#Chua xu ly delete neu that bai
		return result # list of folders ID created
	
	def myFavourites_loads(self):
		#(folder name,public url)
		myFolder=self.get_myFolder('xshare_favourite')
		f=[i[0] for i in myFolder if re.search('\d{10,}',i[0])]
		s=sorted([i.split('.') for i in f], key=lambda m:(m[0],m[1]))
		k=[]
		for i in list(set([i[0] for i in s])):
			try:m=urllib2.base64.urlsafe_b64decode(''.join(j[2] for j in s if j[0]==i))
			except:m=''
			if m:k.append(m+','+'-'.join(xsearch('(\w{10,})',j[1]) for j in myFolder if i in j[0]))
		return k
		
	def myFavourites_remove(self,ids):
		result=True
		for i in ids.split('-'):
			if not self.remove_folder('xshare_favourite',i):result=False
		return result

class fptPlay:#from resources.lib.servers import fptPlay;fpt=fptPlay(c)
	def __init__(self):
		self.hd={'User_Agent':'Mozilla/5.0','X-Requested-With':'XMLHttpRequest'}
		self.hd['referer']='https://fptplay.net/fptplay/gioi-thieu'
		self.hd['Cookie']=xrw('fptplay.cookie') if filetime('fptplay.cookie')<30 else self.login()
		
	def fpt2s(self,s):return ' '.join(re.sub('&.+;',xsearch('&(\w).+;',i),i) for i in s.split())
	
	def login(self):
		email=get_setting('mail_fptplay');password=get_setting('pass_fptplay')
		if not email:
			mess(u'Bạn đang sử dụng account Fptplay của xshare')
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
		if 'laravel_id' in cookie:mess(u'Login thành công','fptplay.net');xrw('fptplay.cookie',cookie)
		else:mess(u'Login không thành công!','fptplay.net')
		return cookie
	
	def login5(self):
		email=get_setting('mail_fptplay');password=get_setting('pass_fptplay')
		if not email:
			mess(u'Bạn đang sử dụng account Fptplay của xshare')
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
		if 'laravel_id' in cookie:mess(u'Login thành công','fptplay.net');xrw('fptplay.cookie',cookie)
		else:mess(u'Login không thành công!','fptplay.net')
		return cookie
	
	def login0(self):
		email=get_setting('mail_fptplay');password=get_setting('pass_fptplay')
		if not email:
			mess(u'Bạn đang sử dụng account Fptplay của xshare')
			email,password=urllib2.base64.b64decode('eHNoYXJlQHRoYW5odGhhaS5uZXQ6YWRkb254c2hhcmU=').split(':')
		data={'email':email,'password':password}
		response=urlfetch.get('https://fptplay.net/tai-khoan');self.hd['Cookie']=response.cookiestring
		response=urlfetch.post('https://fptplay.net/user/login',headers=self.hd,data=data)
		cookie=response.cookiestring
		if 'laravel_id' in cookie:mess(u'Login thành công','fptplay.net')#;xrw('fptplay.cookie',cookie)
		else:mess(u'Login không thành công!','fptplay.net')
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
			rate=xsearch('<p>Đánh giá:(.+?)</p>',content).strip()
			href=xsearch('<a href="(.+?)"',content).strip()
			#href='m.hdonline.vn'+href
			href='http://hdonline.vn'+href
			img=xsearch('<img src="(.+?)"',content).strip()
			year=xsearch('<p>Năm sản xuất:(.+?)</p>',content).strip()
			title = titleVn + ' - ' + titleEn + ' (' + year + ')'
			q=''
			isFolder=True
			if 'episodes' in content and ('phim-bo' in mode):					
				v_mode='episodes'
				if 'serverlist' in mode:							
					title = '[HDO] ' + title
					title = color['phimbo'] + title + '[/COLOR]'							
				elif 'category' in mode or 'search' in mode:
							
					v_mode='serverlist_phim-bo'							
					
				if 'search' in mode: title = '[B]' + title + '[/B]'	
				#addItem(title, href, v_mode+'&query='+titleEn, img, isFolder)
			elif ('phim-le' in mode):
				if 'serverlist' in mode:
					title = '[HDO] ' + title
					v_mode='stream';isFolder=False					
				elif 'category' in mode or 'search' in mode:
					#title = '[B]' + title + '[/B]'
					v_mode='serverlist_phim-le'
				else:							
					v_mode='stream';isFolder=False
					
			filmid = xsearch('-(\d+?).html',href)
			plg='plugin://plugin.video.hkn.hdonline/?action=ListEpisodes&filmid='
			href = plg + str(filmid)						

			items.append((title,href,'%s&query=%s&page=%s'%(v_mode,titleVn+'[]'+titleEn,year),img,isFolder))							
			
		return items


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
			mess(u'Lỗi kết nối tới: %s!'%xsearch('//(.{5,20}\.\w{2,3})',s2u(url)),'make_request')
		print 'Lỗi kết nối tới: %s!'%u2s(url);
	return resp#unicode:body=response.text		
		
def json_rw(file,dicts={},key=''):
	if dicts:makerequest(joinpath(datapath,file),json.dumps(dicts),'w')
	else:
		try:dicts=json.loads(makerequest(joinpath(datapath,file)))
		except:dicts={}
		if key:dicts=dicts.get(key,())
	return dicts
		
		
class hdviet:
	def __init__(self):
		self.hd={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/600.1.4 Gecko/20100101 Firefox/41.0'}
		
	def additems(self,body,mode):
		items=[]
	
		pattern='<li class="mov-item".+?href="(.+?)".+?src="(.+?)".+?title="Phim (.+?)".+?<span(.+?) data-id="(.+?)">'	
		data=re.findall(pattern,body,re.DOTALL);listitems=list()
		for href,img,title,detail,id_film in data:
			epi=xsearch('"labelchap2">(\d{1,3})</span>',detail);#title=unescape(title)
			res=xsearch('id="fillprofile" class="icon-(.+?)11">',detail)
			res='[COLOR gold]SD[/COLOR]' if 'SD' in res else '[COLOR gold]HD[/COLOR]%s'%res
			phim18=xsearch('class="children11".+?>(.+?)</label></span>',detail)
			TM=xsearch('id="fillaudio" class="icon-(.+?)">',detail)
			TM='%s[COLOR green]%s[/COLOR][COLOR red]%s[/COLOR]'%(res,TM,phim18)
			plot=xsearch('<span class="cot1">(.+?)</span>',detail)
			year=xsearch('<span class="chil-date".+?>(.*?)</label></span>',detail)
			act=', '.join(s for s in re.findall('<a href="http://movies.hdviet.com/dien-vien/.+?">(.+?)</a>',detail))
			drt=', '.join(s for s in re.findall('<a href="http://movies.hdviet.com/dao-dien/.+?">(.+?)</a>',detail))
			rat=xsearch('<span class="fl-left">.+?<span>(.+?)</span>',detail)
			upl=xsearch('<span class="fl-right">.+?<span>(.+?)</span>',detail)
			if not epi:title=TM+' '+title;query='hdvietplay'
			elif epi=='1':query='hdvietfolder'
			else:title=TM+' '+title+' [COLOR green](%s)[/COLOR]'%epi;query='hdvietfolder'
			#listItem = xbmcgui.ListItem(label=title,iconImage=img,thumbnailImage=img)
			if rat:rat='[COLOR tomato]IMDb:[/COLOR] %s, '%rat
			if upl:upl='[COLOR tomato]Uploader:[/COLOR] %s, '%upl
			if act:act='[COLOR tomato]Diễnviên:[/COLOR] %s, '%act
			if drt:drt='[COLOR tomato]Đạodiễn:[/COLOR] %s, '%drt
			plot=rat+upl+act+drt+'\n'+plot
			#info={'title':title,'year':year,'rating':xsearch('(\d\.\d{1,2})',rat),'plot':plot,'episode':epi,'director':drt,'writer':act}			
			
			href='hdviet.com|'+str(id_film)
			
			isFolder=True
			v_mode=''
			titleVn=title
			titleEn=title
			if epi and ('phim-bo' in mode):
				v_mode='episodes';
				if 'serverlist' in mode:							
					title = '[HDViet] ' + title
					title = color['phimbo'] + title + '[/COLOR]'							
				elif 'category' in mode or 'search' in mode:
					#title = '[B]' + title + '[/B]'			
					v_mode='serverlist_phim-bo'	

				if 'search' in mode: title = '[B]' + title + '[/B]'	

			elif 'phim-le' in mode:
				if 'serverlist' in mode:
					title = '[HDViet] ' + title
					v_mode='stream';isFolder=False					
					titleEn=href
					href='hdviet.com'						
				elif 'category' in mode or 'search' in mode:
					#title = '1' + title + ''
					v_mode='serverlist_phim-le'
				else:							
					v_mode='stream';isFolder=False					
			items.append((title,href,'%s&query=%s&page=%s'%(v_mode,titleVn+'[]'+titleEn,year),img,isFolder))							
			
		return items
		
	def getResolvedUrl(self,id_film,loop=0):#Phim le/phim chieu/ke doi dau thien ac		
		data=json_rw('hdviet.cookie')
		token = data.get('access_token')
		#token = '22bb07a59d184383a3c0cd5e3db671fc'
		print 'id_film:'+id_film
		#id_film=id_film.replace('_e','&ep=')
		direct_link='https://api-v2.hdviet.com/movie/play?accesstokenkey=%s&movieid=%s'%(token,id_film)		
				
		result=xread(direct_link)
		print direct_link
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
				audioindex=mess_yesno(title,line1,'',audio[0].get("Label",'0'),audio[1].get("Label",'1'))
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
				year = xsearch('Năm phát hành:</strong> .+?-.+?-(.+?)</li>',content)								
				title=xsearch('<h3 class=\'H3title\'>(.+?)</h3>',content).strip()
				try:					
					titleVn = title.split(" (")[0]
					titleEn = title.split(" (")[1].replace(')','')				
					title = title + ' - ' + str(year)
				except:titleVn='';titleEn=title
				
				esp = xsearch('class=.esp.><i>(.+?)</span>',content).replace('</i>','')				
				#count-view=xsearch('<span class=\'count-view\'><i></i>(.+?)</span>',content).strip()
							
				isFolder=True
				v_mode=''
				if esp and ('phim-bo' in mode):
					v_mode='episodes'
					if 'serverlist' in mode:							
						title = '[MegaBox] ' + title
						title = color['phimbo'] + title + '[/COLOR]'							
					elif 'category' in mode or 'search' in mode:
						#title = '[B]' + title + '[/B]'			
						v_mode='serverlist_phim-bo'	

					if 'search' in mode: title = '[B]' + title + '[/B]'	
				elif 'phim-le' in mode:
					if 'serverlist' in mode:
						title = '[MegaBox] ' + title
						v_mode='stream';isFolder=False					
					elif 'category' in mode or 'search' in mode:
						#title = '1' + title + ''
						v_mode='serverlist_phim-le'
					else:							
						v_mode='stream';isFolder=False
						
				items.append((title,href,'%s&query=%s'%(v_mode,titleVn+'[]'+titleEn+'[]'+str(year)),img,isFolder))							
											
		return items		
		
	def getLink(self,url):
		#content = GetUrl(url)				        
		#try:
		#	try:
		#		link = re.compile('var iosUrl = "(.+?)"').findall(content)[0].replace('http://media21.megabox.vn','http://113.164.28.46').replace('http://media22.megabox.vn','http://113.164.28.46') + reg
		#	except:
		#		link = re.compile('var iosUrl = "(.+?)"').findall(content)[0].replace('http://media21.megabox.vn','http://113.164.28.47').replace('http://media22.megabox.vn','http://113.164.28.47') + reg
		#except:
		#	link = re.compile('var iosUrl = "(.+?)"').findall(content)[0].replace('http://media21.megabox.vn','http://113.164.28.48').replace('http://media22.megabox.vn','http://113.164.28.48') + reg		
		
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
		return link,''