__author__ = 'thaitni'
# -*- coding: utf-8 -*-
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,urllib,re,os,unicodedata,datetime,random,json,sys

myaddon=xbmcaddon.Addon()
home=xbmc.translatePath(myaddon.getAddonInfo('path'))
datapath=xbmc.translatePath(os.path.join( xbmc.translatePath(myaddon.getAddonInfo('profile')),'data'))
iconpath=xbmc.translatePath(os.path.join( xbmc.translatePath(myaddon.getAddonInfo('profile')),'icon'))
sys.path.append(os.path.join(home,'resources','lib'));from urlfetch import get,post
#import urlfetch

search_file=os.path.join(datapath,"search.xml");data_path=os.path.join(home,'resources','data')

myfolder= myaddon.getSetting('thumuccucbo').decode('utf-8');copyxml=myaddon.getSetting('copyxml')
if not os.path.exists(myfolder):myfolder=os.path.join(datapath,'myfolder')
subsfolder=os.path.join(myfolder,'subs');tempfolder=os.path.join(myfolder,'temp')
rows=int(myaddon.getSetting('sodonghienthi')) #Số dòng hiển thị cho 1 trang


media_ext=['aif','iff','m3u','m4a','mid','mp3','mpa','ra','wav','wma','3g2','3gp','asf','asx','avi','flv','mov','mp4','mpg','mkv','m4v','rm','swf','vob','wmv','bin','cue','dmg','iso','mdf','toast','vcd','ts','flac']
color={'trangtiep':'[COLOR lime]','search':'[COLOR lime]','phimbo':'[COLOR tomato]','phimle':'[COLOR yellow]'};icon={}
for hd in ['xshare','4share', 'dangcaphd', 'downsub', 'favorite', 'fptplay', 'fshare', 'gsearch', 'hdvietnam', 'icon', 'id', 'ifiletv', 'isearch', 'khophim', 'maxspeed', 'megabox', 'movie', 'msearch', 'myfolder', 'myfshare', 'phimfs', 'serverphimkhac', 'setting', 'tenlua', 'vaphim']:
	icon.setdefault(hd,os.path.join(iconpath,'%s.png'%hd))
hd = {'User-Agent' : 'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'}

def mess(message, timeShown=10000,title=''):
	xbmc.executebuiltin((u'XBMC.Notification(%s,%s,%s,%s)'%('Xshare [COLOR green]%s[/COLOR]'%title,message,timeShown,icon['icon'])).encode("utf-8"))

def mess_yesno(title='[COLOR green]Xshare[/COLOR]', line1='', line2=''):
	dialog=xbmcgui.Dialog()#dialog.yesno(heading, line1[, line2, line3,nolabel,yeslabel])
	return dialog.yesno(title,line1,line2)

def no_accent(s):
	s=re.sub(u'Đ','D',str2u(s));s=re.sub(u'đ','d',s)
	return unicodedata.normalize('NFKD', unicode(s)).encode('ASCII', 'ignore')

def str2u(s):
	if type(s)==str:
		try:s=s.decode('utf-8','ignore')
		except:pass
	return s

def clean_string(string):
	return ' '.join(s for s in re.sub('Fshare|4share|Tenlua|&.+?;','',string).split())

def joinpath(p1,p2):
	try:p=os.path.join(p1,p2)
	except:p=os.path.join(p1,str2u(p2))
	return p

def init_file():
	datafolder=xbmc.translatePath(myaddon.getAddonInfo('profile'))
	for folder in (datafolder,datapath,iconpath,myfolder,subsfolder,tempfolder):
		if not os.path.exists(folder):os.mkdir(folder)
	#xmlheader='<?xml version="1.0" encoding="utf-8">\n';p=datapath;q=myfolder
	#for i in [(p,'search.xml'),(p,'hdvietnam.xml'),(p,'favourites.xml'),(p,'phimmoi.xml'),(p,'fpt.xml'),(q,'mylist.xml')]:
		#file=joinpath(i[0],i[1])
		#if not os.path.isfile(file):makerequest(file,xmlheader,'w')
	
def xshare_group(object,group):
	return object.group(group) if object else ''

def delete_files(folder,mark='',temp='ok'):
	for file in os.listdir(folder):
		if os.path.isfile(joinpath(folder,file)) and (not mark or mark in file):
			try:os.remove(joinpath(folder,file))
			except:temp='';pass
	return temp

def endxbmc():
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def xbmcsetResolvedUrl(url,name=''):
	item=xbmcgui.ListItem(path=url)
	if 'Maxlink' in name:
		if name!='Maxlink':name=name.replace('Maxlink','');item.setInfo('video', {'Title':name})
		else:item.setInfo('video', {'Title':os.path.basename(url)})
		name=''
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item);endxbmc()
	if myaddon.getSetting('autoload_sub')=='true' and name!='xshare':
		if name:url=name
		urltitle=urllib.unquote(os.path.splitext(os.path.basename(url))[0]).lower()
		urltitle='.'+'.'.join(s for s in re.sub('_|\W+',' ',re.split('\d\d\d\d',urltitle)[0]).split())+'.'
		subfile='';items=[]
		for file in os.listdir(subsfolder):
			filefullpath=joinpath(subsfolder,file).encode('utf-8')
			filename=re.sub('vie\.|eng\.','',os.path.splitext(file)[0].lower().encode('utf-8'))
			filename=re.split('\d\d\d\d',filename)[0];count=0
			for word in re.sub('_|\W+',' ',filename).split():
				if '.%s.'%word in urltitle:count+=1
			if count:items.append((count,filefullpath))
		for item in items:
			if item[0]>=count:count=item[0];subfile=item[1]
		if subfile:
			xbmc.sleep(1000);xbmc.Player().setSubtitles(subfile)
			mess(u'[B][COLOR green]%s[/B][/COLOR]'%str2u(os.path.basename(subfile)),20000,'Auto load sub')

def addir(name,link,img='',fanart='',mode=0,page=0,query='',isFolder=False):
	#if '18+' in name and myaddon.getSetting('phim18')=="false":return
	ok=True;name=re.sub(',|\|.*\||\||\<.*\>','',name)
	item=xbmcgui.ListItem(name,iconImage=img,thumbnailImage=img)
	query=menuContext(name,link,img,fanart,mode,query,item)
	item.setInfo(type="Video", infoLabels={"title":name})
	item.setProperty('Fanart_Image',fanart)
	u=sys.argv[0]+"?url="+urllib.quote_plus(link)+"&img="+urllib.quote_plus(img)+"&fanart="+urllib.quote_plus(fanart)+"&mode="+str(mode)+"&page="+str(page)+"&query="+query+"&name="+name
	if not isFolder:item.setProperty('IsPlayable', 'true')
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=isFolder)
	return ok

def menuContext(name,link,img,fanart,mode,query,item):
	if query.split('?')[0]=='Search':
		query=query.split('?')[1]
		item.addContextMenuItems(searchContext(name,link,img,fanart,mode))
	elif query.split('?')[0]=='ID':
		query=query.split('?')[1]
		command=searchContext(name,link,img,fanart,15)
		command+=favouritesContext(name,link,img,fanart,mode)
		item.addContextMenuItems(command)
	elif 'fshare.vn' in link or '4share.vn' in link or 'tenlua.vn' in link:#mode in (3,38,90,95):
		item.addContextMenuItems(favouritesContext(name,link,img,fanart,mode))
	elif myfolder in str2u(link):
		item.addContextMenuItems(make_myFile(name,link,img,fanart,mode,query))
	elif query in 'hdvietfolder-hdvietplay':
		item.addContextMenuItems(hdvietContext(name,link,img,fanart,mode))
	return query

def makeContext(name,link,img,fanart,mode,query):
	if query=='Add to MyFshare favorite':make='AddFavorite'
	elif query=='Remove from MyFshare favorite':make='RemoveFavorite'
	else:make=query.split()[0]
	if 'Rename' in make:colo=color['fshare']
	elif 'Remove' in make:colo=color['hdvietnam']
	else:colo=color['trangtiep']
	context=colo+query+'[/COLOR]'
	p=(myaddon.getAddonInfo('id'),mode,name,link,img,fanart,make)
	cmd='RunPlugin(plugin://%s/?mode=%s&name=%s&url=%s&img=%s&fanart=%s&query=%s)'%(p)
	return context,cmd

def hdvietContext(name,link,img,fanart,mode):
	context=color['trangtiep']+'Thêm vào phim yêu thích[/COLOR]'
	p=(myaddon.getAddonInfo('id'),mode,name,link.split('_')[0],img,fanart,'Themmucyeuthich')
	cmd='RunPlugin(plugin://%s/?mode=%s&name=%s&url=%s&img=%s&fanart=%s&query=%s)'%(p)
	command=[(context,cmd)]
	return command

def searchContext(name,link,img,fanart,mode):
	command=[(makeContext(name,link,img,fanart,9,'Rename item'))]
	command.append((makeContext(name,link,img,fanart,9,'Remove item')))
	return command

def favouritesContext(name,link,img,fanart,mode):
	command=[];
	if type(link)==unicode:link=link.encode('utf-8')
	if link in makerequest(joinpath(datapath,"favourites.xml")):
		command.append((makeContext(name,link,img,fanart,98,'Rename in MyFavourites')))
		command.append((makeContext(name,link,img,fanart,98,'Remove from MyFavourites')))
	else:
		command.append((makeContext(name,link,img,fanart,98,'Add to MyFavourites')))
	if 'www.fshare.vn' in link:
		if query=='MyFshare':
			command.append((makeContext(name,link,img,fanart,11,'Remove from MyFshare')))
			command.append((makeContext(name,link,img,fanart,11,'Rename from MyFshare')))
		else:
			command.append((makeContext(name,link,img,fanart,11,'Add to MyFshare')))
	if link in makerequest(joinpath(myfolder,'mylist.xml')):
		command.append((makeContext(name,link,img,fanart,12,'Rename in Mylist.xml')))
		command.append((makeContext(name,link,img,fanart,12,'Remove from Mylist.xml')))
	else:
		command.append((makeContext(name,link,img,fanart,12,'Add to Mylist.xml')))
	command.append((makeContext(name,'addstring.xshare.vn',img,fanart,13,'Add item name to string search')))
	return command

def make_myFile(name,link,img,fanart,mode,query):
	name=re.sub('\[COLOR.{,12}\]|\[/COLOR\]|Fshare|4share|TenLua|List xml|-|:|"','',name).strip();command=[]
	if os.path.isfile(str2u(link)):
		command.append((makeContext(name,link,img,fanart,11,'Upload to MyFshare')));temp='file'
	else:temp='folder'
	command.append((makeContext(name,link,img,fanart,96,'Rename this %s'%temp)))
	command.append((makeContext(name,link,img,fanart,96,'Remove this %s'%temp)))
	return command

def make_mySearch(name,url,img,fanart,mode,query):
	attr='w';body=makerequest(search_file);r='<a href="%s">.+?</a>\n'%url
	if query=='Rename':
		string=get_input('Nhập chuổi mới',re.sub('\[.*\]-','',name)).strip()
		if not string or string==re.sub('\[.*\]-','',name):return
		string=' '.join(s for s in re.split(' |\.|\'|"\?',string));r1='<a href="%s">%s</a>\n'%(url,string)
		body=re.sub(r,r1,body) if re.search('http.?://',url) else body.replace(name,string)
	elif query=='Remove':
		body=re.sub(r,'',body) if re.search('http.?://',url) else re.sub('<a>%s</a>\n'%name,'',body)
	elif query=='Add':
		if not re.search(url,body):body='<a href="%s">%s</a>\n'%(url,name);attr='a'
		else:return
	elif query=='Input':
		query = get_input('Nhập chuổi tên phim cần tìm trên %s'%url);attr='a'
		if query:
			query = ' '.join(s for s in query.replace('"',"'").replace('?','').split() if s!='')
			if not re.search(query,body):body='<a>%s</a>\n'%query
			else:return query
		else:return ''
	elif query=='get':
		srv=url.split('.')[0];site='Google ' if mode==2 else ''
		name=color['search']+'%sSearch[/COLOR] trên %s%s: [/COLOR]Nhập chuỗi tìm kiếm mới'%(site,color[srv],url)
		addir(name,url,icon[srv],mode=mode,page=1,query='INP',isFolder=True)
		if myaddon.getSetting('history')=='true':
			for string in re.findall('<a>(.+?)</a>',makerequest(search_file)):
				addir(string,url,icon[srv],query='Search?'+string,page=4,mode=mode,isFolder=True)
		return
	if makerequest(search_file,string=body,attr=attr):
		if attr=='w':mess(u'%s chuổi thành công'%str2u(query));xbmc.executebuiltin("Container.Refresh")
	elif attr=='w':mess(u'%s chuổi thất bại'%str2u(query))
	return query
	
def make_request(url,headers={'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'},resp='b',maxr=0):
	try:
		if maxr==0:response=get(url,headers=headers)
		else:response=get(url,headers=headers,max_redirects=maxr)
		if resp=='o':resp=response
		else:
			if resp=='j':resp=response.json
			elif resp=='s':resp=response.status
			elif resp=='u':resp=response.text
			elif resp=='c':resp=response.cookiestring
			else:resp=response.body
			response.close()
	except: 
		mess(u'[COLOR red]Lỗi kết nối tới: %s[/COLOR]'%xshare_group(re.search('//(.+?)/',str2u(url)),1))
		resp='';print 'Make Request Error: %s'%url
	return resp#unicode:body=response.text
	
def make_post(url,headers={'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'},data='',resp='o'):
	try:
		if data:response=post(url=url,headers=headers,data=data)
		else:response=post(url=url,headers=headers)
		if resp=='b':response=response.body
		elif resp=='j':response=response.json
	except:
		mess(u'Post link error: %s'%str2u(url));print 'Post link error: %s'%str2u(url)
		response={} if resp=='j' else ''
	return response	
	
def makerequest(file,string='',attr='r'):
	file=str2u(file)
	if attr=='r':
		try:f=open(file);body=f.read();f.close()
		except:body=''
	else:
		try:f=open(file,attr);f.write(string);f.close();body=string
		except:mess(u'Lỗi ghi file: %s'%str2u(os.path.basename(file)));body=''
	return body
	
def rename_file(sf,df,kq='ok'):
	try:
		if os.path.isfile(df):os.remove(df)
		os.rename(sf,df)
	except:kq='';pass
	return kq

def download_subs(url):
	response=make_request(url,resp='o');downloaded=''
	if not response or response.status!=200:return
	print 'aaa'
	print response.getheaders()[0][1]
	#if int(response.getheaders()[0][1])<10485760:#size<10MB
	#if myaddon.getSetting('autodel_sub')=='true':delete_files(subsfolder)
	delete_files(subsfolder)
	filename=urllib.unquote(os.path.basename(url));delete_files(tempfolder)
	subfile=joinpath(tempfolder,re.sub('\[.+?\]','',filename))
	if makerequest(subfile,string=response.body,attr="wb"):
		if 	response.body[0] in 'R-P':
			xbmc.sleep(500);f1=subfile.encode('utf-8');f2=tempfolder.encode('utf-8')
			xbmc.executebuiltin('XBMC.Extract("%s","%s")'%(f1,f2),True);os.remove(subfile)
			exts = [".srt", ".sub", ".txt", ".smi", ".ssa", ".ass"];sub_list=[]
			for file in os.listdir(tempfolder):
				tempfile=joinpath(tempfolder,file)
				if os.path.isfile(tempfile) and os.path.splitext(tempfile)[1] in exts:
					if re.search('vietname|vie',filename):
						if rename_file(tempfile,joinpath(subsfolder,'Vie.%s'%re.sub(',|"|\'','',file))):
							downloaded='ok'
					elif rename_file(tempfile,joinpath(subsfolder,re.sub(',|"|\'','',file))):downloaded='ok'
		elif rename_file(subfile,joinpath(subsfolder,'Vie.%s'%re.sub('\[.+?\]','',filename))):downloaded='ok'
	else:mess(u'Lỗi download sub')
	if downloaded:mess(u'Đã download sub vào Subsfolder')
	#else:mess(u'Oh! Sorry. [COLOR red]Không chơi được file rar[/COLOR]')
	return downloaded
def get_input(title=u"", default=u""):
	result = ''
	keyboard = xbmc.Keyboard(default, title)
	keyboard.doModal()
	if keyboard.isConfirmed():
		result = keyboard.getText()
	return result

def logout_site(cookie,url):
	def logout(cookie,url,site):
		hd['Cookie']=cookie
		mess(u'Logout %s %sthành công'%(site,'' if make_request(url,hd,resp='s')==302 else u'không '))
	if cookie and myaddon.getSetting('logoutf')=="true":
		if 'fshare.vn' in url.lower():logout(cookie,'https://www.fshare.vn/logout','Fshare.vn')
		elif '4share.vn' in url.lower():logout(cookie,'http://4share.vn/default/index/logout','4share.vn')
		elif 'dangcaphd.com' in url.lower():logout(cookie,'http://dangcaphd.com/logout.html','dangcaphd.com')
		elif 'tenlua.vn' in url.lower():logouttenlua(cookie)
		
def trangtiep(query,items):
	if 'Trang' in query.split('?')[0]:
		trang=int(query.split('?')[0].split('Trang')[1])
		query=query.split('?')[1]
	else:trang=1
	del items[0:(trang-1)*rows]
	trang+=1
	return trang,query,items

def dangcaphd(name,url,img,mode,page,query):
	home='http://dangcaphd.com/'
	def dangcaphd_get_page_control(body,mode,query):
		pattern='<a class="current">\d{1,5}</a><a href="(.+?)">(\d{1,5})</a>.*<a href=".+?page=(\d{1,5})">.+?</a></div>'
		page_control=re.search(pattern,body)
		if page_control:
			href=re.sub('&amp;','',page_control.group(1));pagenext=page_control.group(2)
			pages=int(page_control.group(3))/rows+1
			name=color['trangtiep']+'Trang tiếp theo: trang %s/%d[/COLOR]'%(pagenext,pages)
			addir(name,href,mode=mode,query=query,isFolder=True)
	def dangcaphd_get_link(url):
		hd['Cookie']=login()
		body=make_request(url.replace('/movie-','/watch-'),headers=hd)
		if hd['Cookie']:logout_site(hd['Cookie'],'http://dangcaphd.com/logout.html')
		return re.findall('"(\d{,3})" _link="(.+?)" _sub="(.*?)"',body)
	def dangcaphd_download_sub(url):
		if myaddon.getSetting('autodel_sub')=='true':delete_files(subsfolder)
		subfullpathfilename=joinpath(subsfolder,'vie.%s'%os.path.basename(url));sub=''
		if os.path.splitext(subfullpathfilename)[1] in [".srt", ".sub", ".txt", ".smi", ".ssa", ".ass"]:
			if makerequest(subfullpathfilename,string=make_request(url),attr='wb'):sub=subfullpathfilename
		return sub
	def login(headers={'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'}):
		url="http://dangcaphd.com/login.html";u=myaddon.getSetting('mail_dchd');p=myaddon.getSetting('pass_dchd')
		response=make_post(url,headers,urllib.urlencode({"_submit":"true","email":u,"password": p}))
		try:
			if not response.json['login']:f=response.cookiestring;m='1';headers['Cookie']=f
			else:f='';m='2'
		except:f='';m='3'
		if m=='1' and re.search('Hết hạn.*</b></a></li>',make_request('http://dangcaphd.com/',headers=headers)):
			mess(u'[COLOR red]Tài khoản của bạn hết hạn sử dụng[/COLOR]')
			href='https://www.fshare.vn/folder/NCERC36BSSCY'#acc này do bạn vinhdo tặng
			hd=xshare_group(re.search('<title>.*xx(.+?)xx.*</title>',make_request(href)),1).split('=')
			data=urllib.urlencode({"_submit":"true","email":'%s@%s'%(hd[0],hd[1]),"password":hd[2]})
			resp=make_post(url,data=data)
			try:f=resp.cookiestring if not resp.json['login'] else ''
			except:f=''
		elif m=='1':mess(u'Login dangcaphd.com thành công')
		elif m=='2':mess('[COLOR red]'+re.sub('<..?>','',response.json['login'])+'[/COLOR]')
		elif m=='3':mess(u'[COLOR red]Login dangcaphd.com không thành công[/COLOR]')
		return f
		
	if query=='DHD':
		body=make_request(home)
		name=color['search']+"Search trên dangcaphd.com[/COLOR]"
		addir(name,"dangcaphd.com/movie/search.html",icon['dangcaphd'],mode=mode,query="DHS",isFolder=True)
		name=color['dangcaphd']+'Trang chủ dangcaphd.com[/COLOR]'
		addir(name,home,icon['dangcaphd'],mode=mode,query='DC0',isFolder=True)
		for name in re.findall('</i>(.+?)<span class="caret">',body):
			addir(color['dangcaphd']+name.strip()+'[/COLOR]',home,icon['dangcaphd'],mode=mode,query='DC1',isFolder=True)
		for href,name in re.findall('<a href="(.+?)"><i class=".+?"></i>(.+?)</a>',body):
			if 'channel.html' not in href and 'product.html' not in href:
				addir(color['dangcaphd']+name.strip()+'[/COLOR]',href,icon['dangcaphd'],mode=mode,query='DC2',isFolder=True)
	elif query=="DHS":make_mySearch('',url,'','',mode,'get')
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		return dangcaphd(name,url,img,mode,page,query) if query else 'no'
	elif url=="dangcaphd.com/movie/search.html":
		search_string = urllib.quote_plus(query)
		url='http://dangcaphd.com/movie/search.html?key=%s&search_movie=1'%search_string
		return dangcaphd(name,url,img,mode,page,query='DC2')
	elif query=='DC0':
		body=make_request(home)
		for href,name in re.findall('<a class="title" href="(.+?)"><i class="fa fa-film "></i>(.+?)</a>',body):
			addir(color['dangcaphd']+name.strip()+'[/COLOR]',href,icon['dangcaphd'],mode=mode,query='DC2',isFolder=True)
	elif query=='DC1':
		body=make_request(home)
		if 'the loai' in  no_accent(name).lower():
			for href,name in re.findall('<a href="(http://dangcaphd.com/cat.+?)" title="(.+?)">',body):
				addir(color['dangcaphd']+name.strip()+'[/COLOR]',href,icon['dangcaphd'],mode=mode,query='DC2',isFolder=True)
		if 'quoc gia' in  no_accent(name).lower():
			for href,name in re.findall('<a href="(http://dangcaphd.com/country.+?)" title="(.+?)">',body):
				addir(color['dangcaphd']+name.strip()+'[/COLOR]',href,icon['dangcaphd'],mode=mode,query='DC2',isFolder=True)
	elif query=='DC2':
		body=re.sub('\t|\n|\r|\f|\v','',make_request(url))
		items=re.findall('<a class="product.+?" href="(.+?)" title="(.+?)">.+?<img src="(.+?)" (.+?)</li>',body)
		for href,name,img,other in items:
			if re.search('<div class="sale">.+?</div>',other):
				name=name.strip()+'[/COLOR]'+' - ('+xshare_group(re.search('<div class="sale">(.+?)</div>',other),1)+')'
				addir(color['dangcaphd']+name,href,img,mode=mode,query='DC3',isFolder=True)
			else:addir(name.strip(),href,img,mode=mode,query='DCP')
		dangcaphd_get_page_control(body,mode,query)
	elif query=='DC3':
		for _epi,_link,_sub in dangcaphd_get_link(url):
			title=re.sub('\[.+?\]','',name.split('[/COLOR]')[0])+' - Tập '+_epi.strip()
			link=_link.replace(' ','%20').strip()+'xshare'+_sub.strip()
			addir(title,link,img,mode=mode,query='DCP')
	elif query=='DCP':
		subtitle=''
		if os.path.splitext(url)[1].lower()=='.html':
			links=dangcaphd_get_link(url)
			url=links[0][1].replace(' ','%20').strip()
			if links[0][2]:subtitle=dangcaphd_download_sub(links[0][2].strip())
		else:
			if url.split('xshare')[1]:subtitle=dangcaphd_download_sub(url.split('xshare')[1])
			url=url.split('xshare')[0]
		xbmcsetResolvedUrl(url)
		if subtitle:
			xbmc.sleep(500);xbmc.Player().setSubtitles(subtitle.encode('utf-8'));mess(u'Phụ đề của dangcaphd.com')

def vuahd(name,url,img,mode,page,query):
	color['vuahd']='[COLOR deeppink]';icon['vuahd']=os.path.join(iconpath,'vuahd.png');home='http://vuahd.tv'
	def vuahd_login(headers=''):
		if not headers:
			url='http://vuahd.tv/accounts/login'
			response=make_request(url,resp='o');hd['Cookie']=response.cookiestring
			t=xshare_group(re.search("name='csrfmiddlewaretoken' value='(.+?)'",response.body),1)
			u=myaddon.getSetting('usernamev');p=myaddon.getSetting('passwordv')
			data=urllib.urlencode({'csrfmiddlewaretoken':t,'username':u,'password':p})
			response=make_post(url,hd,data)
			if response.status==302:
				f=response.cookiestring;hd['Cookie']=f
				if re.search('<b>Free</b></span>',make_request('http://vuahd.tv/accounts/profile/',headers=hd)):
					mess(u'[COLOR red]Tài khoản free chỉ xem được một số phim.[/COLOR]')
				else:mess(u'Login vuahd.tv thành công')
			else:mess(u'[COLOR red]Login vuahd.tv không thành công[/COLOR]');f=''
			return f
		else:make_request('http://vuahd.tv/accounts/logout',headers=headers)
	def namecolor(name):return '%s%s[/COLOR]'%(color['vuahd'],name)
	def vuahd_play(url):
		hd['Cookie']=vuahd_login();body=make_request(url,hd)
		href=xshare_group(re.search('<source src = "(.+?)"',body),1)
		if not href:href=xshare_group(re.search('file: "(.+?)"',body),1)
		if href:xbmcsetResolvedUrl(home+href);return
		else:mess(u'Không get được maxspeed link của vuahd.tv')
		vuahd_login(hd)
	def vuahd_search(string,page=1):
		body=make_request('http://vuahd.tv/movies/q/%s'%urllib.quote(string))
		for name,href,img,type in pubvn_page(body):
			addir(name,href,img,fanart,mode,page,query=type,isFolder=(type=='folder'))
		trangcuoi=xshare_group(re.search('class="vpage(\d{1,4})".{,5}>Cuối</a></li>',body),1).strip()
		if trangcuoi and int(trangcuoi)>page:
			name=color['trangtiep']+'Trang tiếp theo: trang %s/%s[/COLOR]'%(str(page+1),trangcuoi)
			addir(name,url,img,fanart,mode,page=page+1,query=string,isFolder=True)
		return ''
	if query=='vuahd.tv':
		name=color['search']+"Search trên vuahd.tv (pub.vn)[/COLOR]"
		addir(name,url,icon['isearch'],mode=mode,query='vuahdsearch',isFolder=True)
		items=re.findall('<li><a href=".+(\d{2})/" rel="external">(Phim.+?)</a></li>',make_request(home))
		for query,name in items:
			addir(namecolor(name),'http://vuahd.tv/1',icon['vuahd'],fanart,mode,page=1,query=query,isFolder=True)
		items=re.findall('<option id="sel_cat_(.+?)">(.+?)</option>',make_request(home))
		for query,name in items:
			addir('Thể loại-'+namecolor(name),'http://vuahd.tv/2',icon['vuahd'],fanart,mode,page=1,query=query,isFolder=True)
	elif query=='vuahdsearch':make_mySearch('',url,'','',mode,'get')
	elif query=="INP":
		string=make_mySearch('',url,'','','','Input')
		if string:vuahd(string,'http://vuahd.tv/3',img,mode,page=1,query='search')
	elif url=='vuahd.tv':vuahd(query,'http://vuahd.tv/3',img,mode,page=1,query='search')
	elif url=='http://vuahd.tv/1' and query=="00":#Phim bộ nhiều tập
		body=make_request('http://vuahd.tv/movies/tv-series/00/')
		for query,name in re.findall('<option id="sel_tvseries_cat_(.+?)">(.+?)</option>',body):
			addir(namecolor(name),'http://vuahd.tv/bo',home+img,fanart,mode=mode,page=1,query=query,isFolder=True)
	elif query=="eps":
		items=re.findall('<a href="#" class="btn-1 btnUpgrade">Xem (.+?)</a>',make_request(url));temp=[]
		for eps in items:
			if eps not in temp:
				temp.append(eps);title=eps+'-'+name;tap=xshare_group(re.search('(\d{1,3})',eps),1)
				if tap:tap=format(int(tap),'02d')
				else:continue
				addir(title,url.replace('tv-series/','')+'-%s'%tap,img,fanart,mode,page=page,query='play')
	elif query=="play":vuahd_play(url+'/watch')
	else:
		href='http://vuahd.tv/movies/'
		if url=='http://vuahd.tv/bo':url='%stv-series-items/%s/?page=%d'%(href,'00' if query=='0' else query,page)
		elif url=='http://vuahd.tv/2' and query=='0':url='%sall-items?page=%d'%(href,page)
		elif url in 'http://vuahd.tv/1-http://vuahd.tv/2':url='%scats/%s/items?page=%d'%(href,query,page)
		elif url=='http://vuahd.tv/3':url='%sq/%s'%(href,urllib.quote(name))
		else:url=re.sub('page=\d{1,3}','page=%d'%page,url) #Trang tiep theo
		body=make_request(url)
		items=re.findall('img src="(.+?)".{,500}<a href="(.+?)" title="(.+?)"',body,re.DOTALL)
		for img,href,name in items:
			if 'tv-series' in href:
				addir(namecolor(name),home+href,home+img,fanart,mode=mode,page=1,query='eps',isFolder=True)
			else:addir(name,home+href,home+img,fanart,mode,page=page,query='play')
		if items and len(items)>25:
			name=color['trangtiep']+'Trang tiếp theo: trang %s[/COLOR]'%str(page+1)
			addir(name,url,icon['vuahd'],fanart,mode,page=page+1,query='trangtiep',isFolder=True)
		
def pubvn(name,url,img,mode,page,query):
	color['pubvn']='[COLOR deepskyblue]';icon['pubvn']=icon['xshare'];home='http://pubvn.net/'
	def login():
		u=myaddon.getSetting('usernamep');p=myaddon.getSetting('passwordp')
		data='txtusername=%s&txtpass=%s&remeber_me1=0&sercurity_code='%(u,p)
		response=make_post(home+'phim/aj/action_login.php',data=data)
		if 'pub_userid=deleted' in response.cookiestring:mess(u'[COLOR red]Login pub.vn không thành công[/COLOR]')
		else:mess(u'Login pub.vn thành công')
		return {'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0','Cookie':response.cookiestring}
	def getiMovEps(url):
		hd=login();pattern='<input id="thread_id" type="hidden" value="(.+?)"/>'
		thread_id=xshare_group(re.search(pattern,make_request(url)),1);pattern='id="player" src="(.+?)"'
		iMovEps=xshare_group(re.search(pattern,make_request(home+'/bar/dodamde/'+thread_id,headers=hd)),1)
		return home+iMovEps,hd
	def pubvn_play(url):
		if '=' not in url:url,hd=getiMovEps(url)
		else:hd=login()
		body=make_request(url+'&server=3',headers=hd)
		id=re.search('iMov=(\d{4,6})&iEps=(\d{5,7})',url);mov_id=xshare_group(id,1);eps_id=xshare_group(id,2)
		log_id=xshare_group(re.search('log_id : (\d{5,7})',body),1)
		pub_id=xshare_group(re.search('pub_id : "(.+?)"',body),1)
		lte_id=xshare_group(re.search('lte_id : (\w{6,10})',body),1)
		sercur=xshare_group(re.search('sercur : (\w{6,10})',body),1)
		hash=xshare_group(re.search("hash : '(\w{8,10})'",body),1)
		dlink=xshare_group(re.search("file: '(.+?)'",body),1)
		data='action=update_last_watched&user_id=%s&mov_id=%s&eps_id=%s&time=93.78&per=1&hash=%s'
		data=data%(log_id,mov_id,eps_id,hash)
		make_post(home+'movie/vn/vasi_blahblah.php',hd,data)
		make_request(home+'phim/logout.php',headers=hd);xbmcsetResolvedUrl(dlink+'?start=0')
	def pubvn_Eps(url):
		body=make_request(url+'&server=3');temp=[];items=[]
		epslist=re.findall('{"ver_id":(.+?),"ver_name":"(.+?)","eps_list":(\[.+?\])}',body,re.DOTALL)
		for ver_id,ver_name,eps_list in epslist:
			if ver_name not in temp:
				temp.append(ver_name)
				try:
					for eps in eval(re.sub('true|false','""',eps_list)):
						href='%s=%s=%d'%(url.split('=')[0],url.split('=')[1],eps['id'])
						name=eps['name']+'-'+ver_name.strip() if len(epslist)>2 else eps['name']
						items.append((name,href))
				except:pass
		return items
	def pubvn_page(body,items=[]):
		pattern='</p></a>(.+?)<a href=".+?">.{,20}<img src="(.+?)".{,200}<a href="(.+?)" title="(.+?)">'
		for eps,img,href,title in re.findall(pattern,body,re.DOTALL):
			eps=xshare_group(re.search('<p>(\d{1,3}/\d{1,3})</p>',eps.strip()),1).split('/')[0]>'1'
			if eps:items.append(('%s%s[/COLOR]'%(color['pubvn'],title),home+href,img,'folder'))
			else:items.append((title,home+href,img,'play'))
		return items
	def pubvn_search(string,page=1):
		data='boxphim=Filter&txtsearch=%s&page=%d'%(urllib.quote_plus(string),page)
		body=make_post(home+'phim/aj/advancesearch.php',data=data).body
		for name,href,img,type in pubvn_page(body):
			addir(name,href,img,fanart,mode,page,query=type,isFolder=(type=='folder'))
		trangcuoi=xshare_group(re.search('class="vpage(\d{1,4})".{,5}>Cuối</a></li>',body),1).strip()
		if trangcuoi and int(trangcuoi)>page:
			name=color['trangtiep']+'Trang tiếp theo: trang %s/%s[/COLOR]'%(str(page+1),trangcuoi)
			addir(name,url,img,fanart,mode,page=page+1,query=string,isFolder=True)
		return ''
	def pubvn_make_txt(items,temps=[]):
		txtfile=joinpath(data_path,'pubvn'+datetime.date.today().strftime("%d")+'.txt')
		for href,name,img in items:
			body=make_request(home+href)
			thread_id=xshare_group(re.search('/bar/threads/(\d{3,6})',body),1)
			eps=xshare_group(re.search('<p>(\d{1,3}/\d{1,3})</p>',body),1);page=0
			if eps.split('/')[0]>'1':page=1;name=color['pubvn']+name+'[/COLOR]'
			temps.append((name,home+'/bar/dodamde/'+thread_id,img,page))
		if temps:delete_files(data_path,mark='pubvn');makerequest(txtfile,string=str(temps),attr='w')
	if query=='pubvn.tv':
		name=color['search']+"Search trên pubvn.tv (pub.vn)[/COLOR]"
		addir(name,url,icon['icon'],mode=mode,query='search',isFolder=True)
		body=make_request(home+'phim/home.php')
		#blmenu_childs=re.findall('<li><a menuid = "(.+?)" tabid="(.+?)">(.+?)</a></li>',body)
		for name in re.findall('<a class="Title_menu">(.+?)</a>',body):
			page+=1;name='%s%s[/COLOR]'%(color['pubvn'],name)
			addir(name,'Title_menu',img,fanart,mode,page,query='blmenu_childs',isFolder=True)
		body=body[body.find('Phim Hot'):body.find('<a>Phim lẻ</a>')]
		phimhots=re.findall('<a href="(.+?)" class=".+?" title="(.+?)\|.{,2000}src="(.+?)"',body,re.DOTALL)
		name='%sPhim HOT[/COLOR]'%color['pubvn']
		addir(name,'Phim_Hot',img,fanart,mode,page,query=query,isFolder=True)
		temp=[('Phim lẻ','32','126'),('Phim bộ Âu - Mỹ','60-1','126-1'),('Phim bộ Châu Á','60-2','126-2')]
		for name,cat_id,type in temp:
			addir('%s%s[/COLOR]'%(color['pubvn'],name),'Home_Main',img,fanart,mode,page=1,query=cat_id,isFolder=True)
			if myaddon.getSetting('phim18')=="true":
				name='%s%s[/COLOR]'%(color['pubvn'],name+' - 18+')
				addir(name,'Home_Main',img,fanart,mode,page=1,query=type,isFolder=True)
		endxbmc();pubvn_make_txt(phimhots)
	elif query=='search':make_mySearch('',url,'','',mode,'get')
	elif query=="INP":pubvn_search(make_mySearch('',url,'','','','Input'))
	elif url=='pubvn.tv':page=1 if 'Trang tiếp theo' not in name else page;pubvn_search(query,page)
	elif url=='Title_menu':
		body=make_request(home+'phim/home.php')
		blmenu_childs=re.findall('<li><a menuid = "(.+?)" tabid="(.+?)">(.+?)</a></li>',body)
		for menuid,tabid,name in blmenu_childs:
			if int(tabid)==page:
				addir('%s%s[/COLOR]'%(color['pubvn'],name),'blmenu_child',img,fanart,mode,page,query=menuid,isFolder=True)
	elif url=='blmenu_child':
		data='tabid=%s&menuid=%s'%(str(page),query)
		body=make_post(home+'phim/aj/aj_top.php',data=data).body
		pattern='<div class="film_poster">(.+?)<a href="(.+?)" class="tooltip1" title="(.+?)\|.{,2000}src="(.+?)" (.{,500}End class = film_poster)'
		for s1,href,title,img,s2 in re.findall(pattern,body,re.DOTALL):
			s1=xshare_group(re.search('<p>(\d{1,3}/\d{1,3})</p>',s1.strip()),1).split('/')[0]>'1'
			s2=xshare_group(re.search('<p>(\d{1,3}/\d{1,3})</p>',s2.strip()),1).split('/')[0]>'1'
			if s1 or s2:addir('%s%s[/COLOR]'%(color['pubvn'],title),home+href,img,fanart,mode,page,query='folder',isFolder=True)
			else:addir(title,home+href,img,fanart,mode,page,query='play')
	elif query=='folder':
		url,hd=getiMovEps(url)
		for eps,href in pubvn_Eps(url):
			addir(eps+' - '+re.sub('\[.?COLOR.{,12}\]','',name),href,img,fanart,mode,page,query='play')
	elif url=='Phim_Hot':
		fn='pubvn'+datetime.date.today().strftime("%d")+'.txt';txtfile=joinpath(data_path,fn)
		if not os.path.isfile(txtfile):
			for file in os.listdir(data_path):
				if 'pubvn' in file:txtfile=joinpath(data_path,file);break
		try:items=eval(makerequest(txtfile))
		except:items=[]
		if items:
			for name,href,img,page in items:
				addir(name,href,img,fanart,mode,page=page,query='dodamde',isFolder=(page==1))
		else:mess(u'Đang cập nhật dữ liệu - chọn lại sau 30 giây nữa nhé!')
	elif query=='dodamde':
		iMovEps=xshare_group(re.search('id="player" src="(.+?)"',make_request(url)),1)
		if page==0:pubvn_play(home+iMovEps)
		else:
			for eps,href in pubvn_Eps(home+iMovEps):
				addir(eps+' - '+re.sub('\[.?COLOR.{,15}\]','',name),href,img,fanart,mode,page,query='play')
	elif url=='Home_Main':
		url=home+'phim/aj/';data='cat_id=%s&type=%s&page=%s'
		if 'Phim lẻ' in name:url+='aj_phimle.php';data='cat_id=%s&page=%s'%(query,str(page))
		else:url+='aj_series.php';data=data%(query.split('-')[0],query.split('-')[1],str(page))
		body=make_post(url,data=data).body
		for title,href,img,type in pubvn_page(body):
			addir(title,href,img,fanart,mode,page,query=type,isFolder=(type=='folder'))
		trangcuoi=xshare_group(re.search('class="catpage(\d{1,4})".{,5}>Cuối</a></li>',body),1).strip()
		if trangcuoi and int(trangcuoi)>page:
			name=re.sub('\[.?COLOR.{,12}\]','',name).split('*')[0].strip()
			name=color['trangtiep']+'%s * Trang tiếp theo: trang %s/%s[/COLOR]'%(name,str(page+1),trangcuoi)
			addir(name,'Home_Main',img,fanart,mode,page=page+1,query=query,isFolder=True)
	elif query=='play':pubvn_play(url)

def hdviet(name,url,img,mode,page,query):
	color['hdviet']='[COLOR darkorange]';icon['hdviet']=os.path.join(iconpath,'hdviet.png')
	home='http://movies.hdviet.com/'
	direct_link='https://api-v2.hdviet.com/movie/play?accesstokenkey=%s&movieid=%s'
	def namecolor(name):return '%s%s[/COLOR]'%(color['hdviet'],name)
	def s2s(string):
		return ' '.join(re.sub('&.+;',xsearch('&(\w).+;',s,1),s) for s in string.split())
	def getcookie():
		u=myaddon.getSetting('userhdviet');p=myaddon.getSetting('passhdviet')
		import hashlib;data=urllib.urlencode({'email':u,'password':hashlib.md5(p).hexdigest()})
		response=make_post('http://movies.hdviet.com/dang-nhap.html',hd,data)
		return response.cookiestring
	def login_hdviet():
		u=myaddon.getSetting('userhdviet');p=myaddon.getSetting('passhdviet')
		url='https://id.hdviet.com/authentication/login'
		response=make_post(url,data='email=%s&password=%s'%(u,p),resp='j')
		if response and response.get('error')==0:
			response=response.get('data')
			mess(u'[COLOR green]Login hdviet.com Success[/COLOR]',title='%sHDViet.com[/COLOR]'%color['hdviet'])
			json_rw('hdviet.cookie',response)
		elif response and response.get('error')==27:
			mess(u'[COLOR red]Acc bị khóa tạm thời. Vào web để login nhé!!![/COLOR]',title='%sHDViet.com[/COLOR]'%color['hdviet']);response=dict()
		elif response and response.get('error') in (25,22):
			mess(u'[COLOR red]%s[/COLOR]'%response.get('message'),title='%sHDViet.com[/COLOR]'%color['hdviet'])
			response=dict()
		else:
			import hashlib;data=urllib.urlencode({'email':u,'password':hashlib.md5(p).hexdigest()})
			response=make_post('http://movies.hdviet.com/dang-nhap.html',hd,data)
			try:resp=response.json
			except:resp={u'r': u'Lỗi đăng nhập hdviet.com', u'e': 3}
			if resp.get('e')==0:
				mess(u'[COLOR green]%s[/COLOR]'%resp['r'],title='%sHDViet.com[/COLOR]'%color['hdviet'])
				hd['Cookie']=response.cookiestring
				response=make_request('http://movies.hdviet.com/dieu-khoan-su-dung.html',headers=hd)
				import base64
				token=base64.b64decode(xsearch('<a class="userinfo".+?token=(.+?)"',response,1))
				response={'Cookie':hd['Cookie'],'access_token':token};json_rw('hdviet.cookie',response)
			else:response=dict();mess(u'[COLOR red]%s[/COLOR]'%resp['r'],title='%shdviet.com[/COLOR]'%color['hdviet'])
		return response#make_post('http://movies.hdviet.com/dang-xuat.html',hd)
	def getResolvedUrl(id_film,loop=0):#Phim le/phim chieu/ke doi dau thien ac
		def getlinkhdviet(token,id_film):
			id_film=id_film.replace('_e','&ep=')
			response=make_request(direct_link%(token,id_film),resp='j')
			try:links=response['r'];link=response['r']['LinkPlay']
			except:links=dict()
			return links
		print id_film
		data=json_rw('hdviet.cookie')
		links=getlinkhdviet(data.get('access_token'),id_film)
		if not links:return links
		link=links.get('LinkPlay')
		if '0000000000000000000000' in link:
			data=login_hdviet();links=getlinkhdviet(data.get('access_token'),id_film)
		if links:
			link=links.get('LinkPlay')
			max_resolution='_1920_' if myaddon.getSetting('hdvietresolution')=='1080' else '_1280_'
			resolutions=['_1920_','_1885_','_1876_','_1866_','_1792_','_1280_','_1024_','_800_','_640_','_480_']
			for resolution in resolutions:
				if resolution in link:link=link.replace(resolution,max_resolution);break
			if '_e' in id_film:link=re.sub('%s_e\d{1,3}_'%id_film.split('_')[0],'%s_'%id_film,link)
			extm3u=make_request(link);link=''
			for resolution in resolutions:
				if resolution in extm3u:
					link=xsearch('(http://.+%s.+m3u8)'%resolution,extm3u,1)
				if link:break
		if link and loop==0:
			response=make_request(link,resp='o')
			if response and 'filename' not in response.headers.get('content-disposition',''):
				data=login_hdviet();return getResolvedUrl(id_film,1)
		if link:
			try:linksub='xshare' if links["AudioExt"][0]['Label']==u'Thuyết Minh' else ''
			except:linksub=''
			if not linksub:
				for source in ['Subtitle','SubtitleExt','SubtitleExtSe']:
					try:
						linksub=links['%s'%source]['VIE']['Source']
						if linksub:
							if download_subs(linksub):break
					except:pass
		else:linksub=''
		return link,linksub
	if query=='hdvietplay':
		link,sub=getResolvedUrl(url);print link,sub
		if not link:mess(u'[COLOR red]Get link thất bại[/COLOR]',title='%sHDViet.com[/COLOR]'%color['hdviet'])
		else:
			if sub:mess(u'[COLOR green]Phụ đề của HDViet.com[/COLOR]',title='%sHDViet.com[/COLOR]'%color['hdviet'])
			xbmcsetResolvedUrl(link,urllib.unquote(os.path.splitext(os.path.basename(sub))[0]))


def sub_body(href,s1,s2,content=''):
	if not content:content=make_request(href,maxr=3)
	else:content=href
	return content[content.find(s1):content.find(s2)]

def json_rw(file,dicts={},key=''):
	if dicts:makerequest(joinpath(datapath,file),json.dumps(dicts),'w')
	else:
		try:dicts=json.loads(makerequest(joinpath(datapath,file)))
		except:dicts={}
		if key:dicts=dicts.get(key,())
	return dicts

def play_youtube(url):#https://www.youtube.com/get_video_info?video_id=xhNy0jnAgzI
	def choice_solution(items,label_quality):#label_quality in ('quality','quality_label')
		url=''
		for solution in ('1080','720','medium','small'):
			for item in items:
				x,y=item.get(label_quality),item.get('type')
				if x and y and solution in x and 'video' in y and 'mp4' in y:
					url=urllib.unquote(item.get('url'));break
			if url:break
		return url
	url='https://www.youtube.com/watch?v=%s&spf=navigate-back'%xsearch('(\w{10,20})',url,1)
	data=make_request(url,resp='j',maxr=3);fmts=''
	if not data:return
	for i in range(0,len(data)):#'adaptive_fmts','url_encoded_fmt_stream_map'
		try:fmts=data[i]['data']['swfcfg']['args']['url_encoded_fmt_stream_map'];break
		except:pass
	data=[];link=''
	for items in fmts.split(','):
		dict={}
		for item in items.split('&'):
			try:dict[item.split('=')[0]]=item.split('=')[1]
			except:pass
		data.append(dict)
	link=choice_solution(data,'quality')
	if link:xbmcsetResolvedUrl(link,re.sub(' \[COLOR.+?/COLOR\]','',name)+'Maxlink')
	else:mess(u'[COLOR red]Get maxspeed link fail[/COLOR]',title='[COLOR green]youtube.com[/COLOR]')
	
def hayhaytv(name,url,img,fanart,mode,page,query):
	home='http://www.hayhaytv.vn/';ajax=home+'ajax_hayhaytv.php';api='http://api.hayhaytv.vn/'
	color['hayhaytv']='[COLOR tomato]';icon['hayhaytv']=os.path.join(iconpath,'hayhaytv.png')
	def login():
		u=myaddon.getSetting('userhayhay');p=myaddon.getSetting('passhayhay')
		data=urllib.urlencode({'email':u,'password':p,'remember_account':0})
		response=make_post('%sajax_jsonp.php?p=jsonp_login'%home,data=data)
		try:
			if response.json['success']=='success':
				mes(u'[COLOR green]Login hayhaytv thành công[/COLOR]');f=response.cookiestring
				makerequest(joinpath(datapath,'hayhaytv.cookie'),f,'w')
			else:mes(u'[COLOR red]Bạn hãy kiểm tra user/pass trên hayhaytv.vn[/COLOR]');f=''
		except:mes(u'[COLOR red]Login hayhaytv thấy bại[/COLOR]');f=''
		return f
	def mes(string):mess(string,title=namecolor('hayhaytv.vn'))
	def namecolor(name):return '%s%s[/COLOR]'%(color['hayhaytv'],name)
	def get_date(string):
		s=xsearch('/(\d{8})/',string,1)
		return '%s/%s/%s'%(s[:2],s[2:4],s[4:8]) if s else None
	def get_year(string):return xsearch('(20\d\d|19\d\d)',string,1)
	def get_idw(url):return xsearch('-(\w{6,20})\.html',url,1)
	def get_id(content):return xshare_group(re.search('FILM_ID\D{3,7}(\d{3,6})',content),1)
	def get_i(content,tag):return xsearch('<.+%s:.+>(.+?)?</li>'%tag,content,1).strip()
	def setskin():
		if xbmc.getSkinDir()=='skin.confluence':xbmc.executebuiltin('Container.SetViewMode(504)')
	def hayhaytv_search(string):
		url='http://www.hayhaytv.vn/tim-kiem/%s/trang-1'%'-'.join(s for s in string.split())
		hayhaytv(name,url,img,mode,page=1,query='M3')
	def getinfo(body,sticky=dict()):
		for stic,info,plot in re.findall('id="(sticky.+?)" class="atip">(.+?)<p>(.*?)</p>',body,re.DOTALL):
			gen=get_i(info,'Thể loại');ctry=get_i(info,'Quốc Gia');rat=get_i(info,'IMDB')
			dur=xsearch('(\d{1,4})',get_i(info,'Thời lượng'),1)
			eps=xsearch('<span>Số tập:</span>(.+?)</li>',info,1,re.DOTALL).strip()
			sticky[stic]=(eps,gen,ctry,dur,rat,plot)
		#pattern='<a.+?tooltip="(.+?)" href="(.+?)">.*?"(http://img.*?)".*?color">(.*?)</span>.*?<span>(.*?)</span>(.*?)</a>'
		pattern='tooltip="(.+?)".+?href="(.+?)">.+?"(http://img.+?)".+?color">(.*?)</span>.*?<span>(.*?)</span>(.*?)</a>'
		items=list()#vie,eng,href,img,epi,eps,gen,ctry,dur,rat,plot
		for stic,href,img,eng,vie,tap in re.findall(pattern,body,re.DOTALL):
			if sticky.get(stic):items.append(((vie,eng,href,img,xsearch('<p>(.+?)</p>',tap,1))+sticky[stic]))
		return items
	def update_home(adict):
		mes(u'[COLOR green] Database updating...[/COLOR]')
		body=make_request(home,headers=hd)
		if not body:return adict
		content=sub_body(body,'class="menu_header"','class="box_login"','1')
		adict['mar-r20']=[s for s in re.findall('menu_fa_text.+?" href="(.+?)".*>(.+?)</a>',body) if os.path.basename(s[0])]
		for href,item in re.findall('href="(.+?)".+?<a (.+?)</ul>',content,re.DOTALL):
			for link,name in adict['mar-r20']:
				if href==link and 'trailer' not in link:
					name=os.path.basename(href)
					adict['m-%s'%name]=re.findall('href="(.+?)".*?>(.+?)</a>',item)
		pattern='href="(.+?)".*?>(.+\s.+|.+?)</a>.*\s?.*</h2>'
		adict['main']=[(s[0],' '.join(s for s in s[1].split())) for s in re.findall(pattern,body)]
		content=sub_body(body,'class="banner_slider"','class="main"','1')
		adict['banner_slider']=re.findall('<h3><a href=".+-(\w{5,20})\.html"',content)
		for p in ('phimbo','phimle','tvshow','clip'):
			mes(u'[COLOR green] Database updating...%s[/COLOR]'%p)
			for page in range(1,100):
				url='http://www.hayhaytv.vn/ajax_hayhaytv.php?p=%s&page=%d'%(p,page)
				items=getinfo(make_post(url,resp='b'));items_new=[s for s in items if get_idw(s[2]) not in adict]
				for s in items:adict[get_idw(s[2])]=s
				if len(items_new)==0:break
		xbmc.executebuiltin("Dialog.Close(all, true)")
		return json_rw('hayhaytv.json',dicts=adict)
	def addDirs(items,page='1'):
		listitems=list()
		for item in items:
			vie,eng,href,img,epi,eps,gen,ctry,dur,rat,plot=item
			#vie,eng,href,img,fan,thumb,date,year,gen,ctry,dur,rat,rev,views,epi,eps,drt,act,upl,sea,plot=item
			href='%s/%s'%(os.path.dirname(href),urllib.quote(u2s(os.path.basename(href))))
			title=vie+' - '+eng if vie and eng else vie if vie else eng;dur=xsearch('(\d{1,4})',dur,1)
			if eps and eps!='1':query='readfolder';title=namecolor(title)+' %s/%s'%(epi if epi else '?',eps)
			else:query='play'
			fan=img.replace('/crop/','/');thumb=img.replace('/crop/','/thumb/')
			date=get_date(img);year=get_year(eng);sea=xsearch('Season (\d{1,2})',eng,1)
			listItem = xbmcgui.ListItem(label=title,iconImage=img,thumbnailImage=thumb)
			if rat:plot='[COLOR tomato]IMDB:[/COLOR] %s\n'%rat+plot
			info={'title':title,'date':date,'year':year,'duration':dur,'rating':rat,'country':ctry,'genre':gen+' [COLOR green]%s[/COLOR]'%ctry,'plot':plot,'Episode':epi,'Season':sea}
			listItem.setInfo(type="Video", infoLabels=info)
			#listItem.setArt({"thumb":thumb,"poster":img,"fanart":fan})
			if query=='play':listItem.setProperty('IsPlayable', 'true')
			u=sys.argv[0]+"?url="+urllib.quote_plus(href)+"&img="+urllib.quote_plus(img)+"&fanart="+urllib.quote_plus(fan)+"&mode="+str(mode)+"&page="+str(page)+"&query="+query+"&name="+title
			listitems.append((u,listItem,False if query=='play' else True))
		xbmcplugin.addDirectoryItems(int(sys.argv[1]),listitems,totalItems=len(listitems))
		return len(listitems)
	def getlink(body):
		movie_id=get_id(body);pattern='<title>.*xx(.+?)xx.*</title>';print 'movie_id %s'%movie_id
		href=xsearch('<link rel="canonical" href="(.+?)"',body,1)
		list_episodes=dict(re.findall('class=.*?href="(.+?)".*?>\D*([\d-]+)</',body))
		tap=list_episodes.get(href);print 'Tap: %s'%tap
		s=xsearch(pattern,make_request('https://www.fshare.vn/folder/5VNFUPO32P6F'),1).split('-')
		hd={s[0]:'%s %s'%(s[1],s[2])};data={"secure_token":"1.0","request":'{"movie_id":"%s"}'%movie_id}
		response=make_post('%smovie/movie_detail'%api,hd,data,'j');print 'Tap %s'%tap
		if response.get('data') and response['data'].get('list_episode') and len(response['data']['list_episode'])>0:
			eps=response['data']['list_episode']
			ids=[(s.get('id'),s.get('vn_subtitle')) for s in eps if s.get('name')==tap or s.get('name')==u'Tập '+tap]
			if ids:movie_id,sub=ids[0];href='%sgetlink/movie_episode'%api
			else:href=sub=''
		else:
			href='%sgetlink/movie'%api
			try:sub=response['data']['vn_subtitle'];print 'movie_id %s'%movie_id
			except:sub=''
		if href:
			data["request"]='{"data":[{"type":"facebook","email":"%s"}]}'%myaddon.getSetting('userhayhay')
			response=make_post('%suser/signup_social_network'%api,hd,data,'j')
			if response:
				token=response['data']['token_app'];user_id=response['data']['user_id']
				data['request']='{"token":"%s","user_id":"%s","movie_id":"%s"}'%(token,user_id,movie_id)
				print data
				response=make_post(href,hd,data,'j')
				try:href=response['data']['link_play'][0]['mp3u8_link']
				except:href=''
		return href,sub

	if checkupdate('hayhaytv.cookie',type='day'):hd['Cookie']=login()
	else:hd['Cookie']=makerequest(joinpath(datapath,'hayhaytv.cookie'))
	if query=='hayhaytv.vn':
		name=color['search']+"Search trên hayhaytv.vn[/COLOR]"
		addir(name,'http://www.hayhaytv.vn/tim-kiem/',icon['hayhaytv'],fanart,mode,1,'search',True)
		addir(namecolor("HayhayTV giới thiệu"),'gioithieu',icon['hayhaytv'],fanart,mode,1,'gioithieu',True)
		adict=json_rw('hayhaytv.json')
		if not adict.get('mar-r20') or not adict.get('main'):adict=update_home(adict)
		for href,name in adict['mar-r20']:
			addir(namecolor(name),href,icon['hayhaytv'],fanart,mode,1,'mainmenu',True)
		for href,name in adict['main']:
			addir(namecolor(name),href,icon['hayhaytv'],fanart,mode,1,'submenu',True)
		if checkupdate('hayhaytv.json',type='day') and not os.path.isfile(joinpath(datapath,'hayhaytv.tmp')):
			endxbmc();makerequest(joinpath(datapath,'hayhaytv.tmp'),'','w')
			adict=update_home(adict);delete_files(datapath,mark='hayhaytv.tmp')
	elif query=='search':make_mySearch('','hayhaytv.vn','','',mode,'get')
	elif query=="INP":hayhaytv_search(make_mySearch('',url,'','','','Input'))
	elif url=='hayhaytv.vn':page=1 if 'Trang tiếp theo' not in name else page;hayhaytv_search(query)
	if query=='gioithieu':
		adict=json_rw('hayhaytv.json')
		addDirs([adict.get(s) for s in adict.get('banner_slider')]);setskin()
	elif query=='mainmenu':
		theloai=os.path.basename(url).replace('-','');q='filter'
		if theloai=='shows':theloai='tvshow'
		elif theloai=='cliphay':theloai='clip';q='theloai'
		elif url=='http://www.hayhaytv.vn/trailer':
			href='http://www.hayhaytv.vn/ajax_hayhaytv.php?p=trailer&page=1'
			return hayhaytv(name,href,img,fanart,mode,1,'submenu')
		for href,name in json_rw('hayhaytv.json',key='m-%s'%os.path.basename(url)):
			addir(namecolor(name),href,img,fanart,mode,1,'submenu',True)
	elif query=='submenu':
		body=make_request(url,maxr=3);adict=json_rw('hayhaytv.json')
		if 'http://www.hayhaytv.vn/su-kien/' in url or 'q=su-kien' in url:
			ids=re.findall('<a title=".+?" href=".+-(\w{10,20})\.html"',body)
			if not ids:mes(u'[COLOR red]Hiện tại không có nội dung mục này.[/COLOR]');return 'no'
			addDirs([adict.get(s) for s in ids])
			urlnext=home+xsearch('class=.active.+?onclick=.+?"(ajax_ht.php.+?)"',body,1)
			pagenext=xsearch('page=(\d{1,4})',urlnext,1);pagelast=xsearch('trang-(\d{1,4})-.{,50}Cuối',body,1)
		else:
			items=getinfo(body)
			if not items:mes(u'[COLOR red]Hiện tại không có nội dung mục này.[/COLOR]');return 'no'
			addDirs(items);urlnext=home+xsearch('class=.active.+?"(ajax_hayhaytv.php.+?)"',body,1)
			pagenext=xsearch('page=(\d{1,4})',urlnext,1);pagelast=xsearch('Trang \d{1,4}/(\d{1,4})',body,1)
		if pagenext:
			name=re.sub('\[.+?\]','',name.split('-')[0].strip())
			name='%s%s - Trang tiếp theo: trang %s/%s[/COLOR]'%(color['trangtiep'],name,pagenext,pagelast)
			addir(name,urlnext,img,fanart,mode,page+1,'submenu',True)
		setskin()
	elif query=='readfolder':#Phim bo moi: Truy Tìm Kho Báu
		pages=0;adict=json_rw('hayhaytv.json')
		if page==1:
			body=sub_body(make_request(url,headers=hd,maxr=3),'<div id="new_player">','class="content_div"','1')
			list_episodes=re.findall('class=.*?href="(.+?)".*?>\D*([\d-]+)</',body);items=list()
			item=adict.get(get_idw(url))
			if item:vie,eng,href,img,epi,eps,gen,ctry,dur,rat,plot=item
			else:vie=re.sub('\[.+?\]','',s2u(name));eps=xsearch('\w{0,3}/(\d{1,4})',name,1);eng=epi=gen=ctry=dur=rat=plot=''
			for href,tap in list_episodes:
				vi=u'Tập %s/%s%s'%(tap,eps,'-'+vie if vie else '')
				items.append((vi,eng,href,img,epi,'',gen,ctry,dur,rat,plot))
			if 'http://www.hayhaytv.vn/xem-show' in url:
				pages=xsearch("onclick='paging\((\d{1,3})\)'> &raquo",body,1)
				pages=int(pages) if pages else 0;id=xsearch('episode_(.+?)_unactive',body,1)
				url='http://www.hayhaytv.vn/tvshow/paging?page=2&q=episode&id=%s&pages=%d'%(id,pages)
			if pages or len(items)>rows:makerequest(joinpath(datapath,"temp.txt"),str(items),'w')
		else:
			try:items=eval(makerequest(joinpath(datapath,"temp.txt")))
			except:items=[]
			if 'http://www.hayhaytv.vn/tvshow/paging' in url and items:
				vie,eng,href,img,epi,eps,gen,ctry,dur,rat,plot=items[0]
				body=make_post(url.split('?')[0],data=url.split('?')[1],resp='b');items=list()
				for href,tap in re.findall('class=.*?href="(.+?)".*?>\D*([\d-]+)</',body):
					vi=re.sub(u'Tập \d{1,4}/',u'Tập %s/'%tap,vie)
					items.append((vi,eng,href,img,epi,'',gen,ctry,dur,rat,plot))
				pages=xsearch('pages=(\d{1,4})\Z',url.split('?')[1],1)
				if pages and int(pages)>page:
					url=re.sub('page=\d{1,4}&','page=%s&'%str(page+1),url);pages=int(pages)
				else:pages=0
		if 'http://www.hayhaytv.vn/tvshow' not in url:
			pages=len(items)/(rows+1)+1;del items[:rows*(page-1)];del items[rows:]
		addDirs(items)
		if pages>page:
			name=color['trangtiep']+'Trang tiếp theo...trang %d/%d[/COLOR]'%(page+1,pages)
			addir(namecolor(name),url,img,fanart,mode,page+1,'readfolder',True)
		setskin()
	elif query=='play':
		print url
		body=make_request(url,headers=hd,maxr=3);trailer=xsearch("initTrailerUrl = '(.+?)'",body,1)
		if trailer:xbmcsetResolvedUrl(trailer)
		elif '/xem-clip/' not in url:
			if '/xem-show/' in url:mes(u'[COLOR red]Chưa code phần này !!![/COLOR]');return
			href,sub=getlink(body)
			if href:
				if sub and download_subs(sub):mes(u'[COLOR green]Phụ đề của hayhaytv.vn[/COLOR]')
				xbmcsetResolvedUrl(href,urllib.unquote(os.path.splitext(os.path.basename(sub))[0]))
			else:mes(u'[COLOR red]Get max link thất bại...[/COLOR]')
		else:
			href=xsearch('src="(http://www.youtube.com.+?)"',body,1)
			if href:play_youtube(href)
			else:mes('[COLOR red]Link youtube.com find not found ![/COLOR]')
			
def xsearch(pattern,string,group,flags=0):
	research=re.search(pattern,string,flags)
	if research:
		try:result=research.group(group)
		except:result=''
	else:result=''
	return result
			