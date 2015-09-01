# -*- coding: utf-8 -*-
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,urllib,re,os,unicodedata,datetime,random,json,sys

myaddon=xbmcaddon.Addon()
home=xbmc.translatePath(myaddon.getAddonInfo('path'))
datapath=xbmc.translatePath(os.path.join( xbmc.translatePath(myaddon.getAddonInfo('profile')),'data'))
iconpath=xbmc.translatePath(os.path.join( xbmc.translatePath(myaddon.getAddonInfo('profile')),'icon'))
#sys.path.append(os.path.join(home,'resources','lib'));import urlfetch
import urlfetch

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

def alert(message,title="Cantobu Media"):
  xbmcgui.Dialog().ok(title,"",message)

def notification(message, timeout=7000):
  xbmc.executebuiltin((u'XBMC.Notification("%s", "%s", %s)' % ('Cantobu Media', message, timeout)).encode("utf-8"))

def extract(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc)
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)


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
	#if myaddon.getSetting('autoload_sub')=='true' and name!='xshare':
	if name!='xshare':
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
	
def make_request(url,headers={'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'},resp='b'):
	try:
		response = urlfetch.get(url,headers=headers)
		if resp=='o':resp=response
		else:
			if resp=='j':resp=response.json
			elif resp=='s':resp=response.status
			else:resp=response.body
			response.close()
		return resp
	except: 
		mess(u'[COLOR red]Lỗi kết nối tới: %s[/COLOR]'%xshare_group(re.search('//(.+?)/',str2u(url)),1))
		print 'Make Request Error: %s'%url;resp=''
	return resp#unicode:body=response.text

def make_post(url,headers={'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'},data=''):
	try:
		if data:response=urlfetch.post(url=url,headers=headers,data=data)
		else:response=urlfetch.post(url=url,headers=headers)
	except:mess(u'Không truy cập được %s'%str2u(url));response=''
	return response

def makerequest(file,string='',attr='r'):
	file=str2u(file)
	if attr=='r':
		try:f=open(file);body=f.read();f.close()
		except:mess(u'Lỗi đọc file: %s'%str2u(os.path.basename(file)));body=''
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
			href=re.sub('&amp;','',xshare_group(page_control,1));trangke=xshare_group(page_control,2)
			tongtrang=int(xshare_group(page_control,3))/35+1
			name=color['trangtiep']+'Trang tiếp theo: trang %s/%d[/COLOR]'%(trangke,tongtrang)
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
		url="http://dangcaphd.com/login.html";u=myaddon.getSetting('userhdviet');p=myaddon.getSetting('passhdviet')
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
	home='http://movies.hdviet.com/';direct_link='https://api-v2.hdviet.com/movie/play?movieid=%s'
	def namecolor(name):return '%s%s[/COLOR]'%(color['hdviet'],name)
	def login():
		u=myaddon.getSetting('userhdviet');p=myaddon.getSetting('passhdviet')
		import hashlib;data=urllib.urlencode({'email':u,'password':hashlib.md5(p).hexdigest()})
		response=make_post('http://movies.hdviet.com/dang-nhap.html',hd,data)
		try:resp=response.json
		except:resp={u'r': u'Lỗi đăng nhập hdviet.com', u'e': 3}
		mess(u'HDViet.com: '+resp['r'],2000);f=''
		if resp['e']==0:f=response.cookiestring;makerequest(joinpath(tempfolder,'hdviet.cookie'),f,'w')
		return f#make_post('http://movies.hdviet.com/dang-xuat.html',hd)
	def additems(body):
		pattern='<a href="(.{,200})"><img src="(.+?)"(.+?)"h2-ttl3">(.+?)<span>(.+?)</span>(.*?)<a'
		links=re.findall(pattern,body)
		for link,img,temp,ttl3,title,cap in links:
			title=ttl3.replace('&nbsp;','')+'-'+title;caps=''
			if 'icon-SD' in cap:caps+='[COLOR gold]SD[/COLOR]'
			if 'icon-720' in cap:caps+='[COLOR gold]HD[/COLOR]720'
			if 'icon-1080' in cap:caps+='[COLOR gold]HD[/COLOR]1080'
			if 'icon-TM' in cap:caps+='[COLOR green]TM[/COLOR]'
			if '>18+<' in cap:caps+='[COLOR red]18+[/COLOR]'
			isFolder=xshare_group(re.search('"labelchap2">(\d{1,3})</span>',temp),1)
			link=xshare_group(re.search('id="tooltip(\d{,10})"',temp),1).strip()
			if not isFolder:addir(caps+' '+title,link,img,fanart,mode,page,query='hdvietplay')
			elif isFolder=='1':hdviet(title,link,img,mode,page,'hdvietfolder')
			else:addir(caps+' '+namecolor(title),link,img,fanart,mode,page,query='hdvietfolder',isFolder=True)
	def getResolvedUrl(id):
		response=make_request(direct_link%id,headers=hd,resp='j')
		try:result=response['r']
		except:result=''
		return result
	def hdviet_search(string):
		url='http://movies.hdviet.com/tim-kiem.html?keyword=%s'%urllib.quote(string)
		hdviet(name,url,img,mode,page,query='timkiem')
	if query=='hdviet.com':
		name=color['search']+"Search trên hdviet.com[/COLOR] (Hãy chọn độ phân giải trên settings nhé)"
		addir(name,'http://movies.hdviet.com/tim-kiem.html',icon['icon'],mode=mode,query='search',isFolder=True)
		body=make_request(home)
		items=re.findall('"mainitem" menuid="(.+?)" href="(.+?)" title=".+?">(.+?)</a>',body)
		for id,href,name in items:
			addir(namecolor(name),home,icon['hdviet'],fanart,mode,page,query=id,isFolder=True)
		addir(namecolor('Thể loại phim'),'the-loai',icon['icon'],mode=mode,query='the-loai-phim',isFolder=True)
		url='http://movies.hdviet.com/phim-yeu-thich.html'
		addir(namecolor('Phim yêu thích'),url,icon['icon'],mode=mode,query='yeu-thich',isFolder=True)
		items=re.findall('"h2-ttl cf">.+?<a href="(.+?)" title=".+?" >(.+?)</a>',body)
		tempbody=body[body.find('h2-ttl cf')+10:]
		for href,name in items:
			addir(namecolor(name),href,icon['hdviet'],fanart,mode,page,query='1',isFolder=True)
			subbody=tempbody[:tempbody.find('h2-ttl cf')];tempbody=tempbody[tempbody.find('h2-ttl cf')+10:]
			additems(subbody)
	elif query=='search':make_mySearch('','hdviet.com','','',mode,'get')
	elif query=="INP":hdviet_search(make_mySearch('',url,'','','','Input'))
	elif url=='hdviet.com':page=1 if 'Trang tiếp theo' not in name else page;hdviet_search(query)
	elif query=='the-loai-phim':		
		for href,name in re.findall('<p><a href="(.+?)" title=".+?">(.+?)</a></p>',make_request(home)):
			addir(namecolor(name),href,icon['hdviet'],fanart,mode,page,query='1',isFolder=True)
	elif query=='the-gioi-sao':
		for href,name in re.findall('<li><a href="(.+?)" title=".+?">(.+?)</a></li>',make_request(home)):
			addir(namecolor(name),href,icon['hdviet'],fanart,mode,page,query='1',isFolder=True)
	elif query=='3' and url==home:#Phim lẻ
		items=re.findall('<a href="(.+?)" .?menuid="(.+?)" .?title=".+?" >(.+?)</a>',make_request(home))
		for href,id,name in items:
			addir(namecolor(name),href,icon['hdviet'],fanart,mode,page,query=id,isFolder=True)
	elif query=='10' and url==home:#Phim bộ
		body=make_request(home)
		items=re.findall('<a href="(.+?)" menuid="(.+?)" title=".+?">(.+?)</a>',body)
		items+=re.findall('<a class="childparentlib" menuid="(.+?)" href="(.+?)" title=".+?">(\s.*.+?)</a>',body)
		for href,id,name in items:
			if 'au-my' in href:name='Phim bộ Âu Mỹ %s'%name.strip()
			elif 'hong-kong' in href:name='Phim bộ Hồng Kông %s'%name.strip()
			elif 'trung-quoc' in href:name='Phim bộ Trung Quốc %s'%name.strip()
			else:name='Phim bộ %s'%name.strip()
			if href in '38-39-40':temp=href;href=id;id=temp
			addir(namecolor(name),href,icon['hdviet'],fanart,mode,page,query=id,isFolder=True)
	elif query=='hdvietfolder':
		href='http://movies.hdviet.com/lay-danh-sach-tap-phim.html?id=%s'%url
		response=make_request(href,resp='j')
		if not response:return
		for eps in range(1,int(response["Sequence"])+1):
			title='Tập %s/%s-%s'%(format(eps,'0%dd'%len(response['Episode'])),str(response['Episode']),re.sub('\[.?COLOR.{,12}\]','',name))
			addir(title,'%s_e%d'%(url,eps),img,fanart,mode,page,query='hdvietplay')
	elif query=='hdvietplay':
		links=getResolvedUrl(url);linksub='';maxspeedlink=''
		if not links:mess(u'[COLOR red]HDViet.com: Get link thất bại[/COLOR]');return
		link=re.sub('_320_480_','_320_1920_vip_',links['LinkPlay'])
		epi=xshare_group(re.search('/(\d{1,6}_e\d{1,4})_',link),1)
		if epi:link=link.replace(epi,url)
		href=link+'?audioindex=1' if myaddon.getSetting('hdvietaudio')=='true' else link
		allresolution=make_request(href)
		if len(allresolution)<100:
			href=link;allresolution=make_request(href)
			if len(allresolution)<100:mess(u'[COLOR red]HDViet.com: Get maxspeed link thất bại[/COLOR]');return
		hd['Cookie']=login();resolutions=['1920','1792','1280','1024','800','640','480']
		if not hd['Cookie']:resolution=3
		else:
			body=make_request('http://movies.hdviet.com/dang-ky-hdvip.html',headers=hd)
			maxresolution=myaddon.getSetting('hdvietresolution')
			vip=xshare_group(re.search('<span>HDVip</span>.+(\d)',body),1)
			if (vip or 'xshare' in myaddon.getSetting('userhdviet')) and maxresolution=='1080':resolution=0
			else:resolution=2
			make_post('http://movies.hdviet.com/dang-xuat.html',headers=hd).close
		if resolution>1 and maxresolution=='1080':
			mess(u'[COLOR red]Hãy gia hạn acc VIP để có độ phân giải tối đa nhé.[/COLOR]',title=u'HDViet thông báo')
			xbmc.sleep(5000)
		for res in range(resolution,len(resolutions)):
			maxspeedlink=xshare_group(re.search('(http.+%s.+)'%resolutions[res],allresolution),1)
			if maxspeedlink:break
		if not maxspeedlink: maxspeedlink=href
		try:linksub='xshare' if links["AudioExt"][0]['Label']==u'Thuyết Minh' else linksub
		except:pass
		if not linksub:
			for source in ['Subtitle','SubtitleExt','SubtitleExtSe']:
				try:
					linksub=links['%s'%source]['VIE']['Source']
					if linksub:
						ep1=xshare_group(re.search('/(e\d{1,3})/',linksub,re.I),1)
						ep2=xshare_group(re.search('_(e\d{1,3})_',maxspeedlink,re.I),1)
						if ep1 and ep2:linksub=linksub.replace(ep1,ep2.upper())
						if download_subs(linksub):break
				except:pass
		print urllib.unquote(os.path.splitext(os.path.basename(linksub))[0])
		xbmcsetResolvedUrl(maxspeedlink,urllib.unquote(os.path.splitext(os.path.basename(linksub))[0]))
	elif query=='Themmucyeuthich':
		def post_url(cookie):
			hd['Cookie']=cookie
			body=make_post('http://movies.hdviet.com/them-phim-yeu-thich.html',hd,urllib.urlencode({"MovieID":"%s"%url}))
			try:json=body.json
			except:json={'e':1,'r':'Lỗi thêm phim yeu thisch'}
			return json
		json=post_url(makerequest(joinpath(tempfolder,'hdviet.cookie')))
		if json['e']>0 and 'nằm trong' not in json['r'].encode('utf-8'):json=post_url(login())
		mess(u'%s'%json['r'])
	else:
		if query=='yeu-thich':
			hd['Cookie']=makerequest(joinpath(tempfolder,'hdviet.cookie'))
			body=make_request(url,hd)
			if myaddon.getSetting('userhdviet') not in body:hd['Cookie']=login();body=make_request(url,hd)
		else:body=make_request(url)
		body=body[body.find('box-movie-list'):body.find('h2-ttl cf')];additems(body)
		pages=re.findall('<li class=""><a href="(.+?)">(.+?)</a></li>',body[body.find('class="active"'):])
		if pages:
			pagenext=pages[0][1];pageend=pages[len(pages)-1][1]
			name='%sTrang tiếp theo: trang %s/%s[/COLOR]'%(color['trangtiep'],pagenext,pageend)
			addir(name,pages[0][0],img,fanart,mode,page,query,isFolder=True)

def hayhaytv(name,url,img,mode,page,query):
	color['hayhaytv']='[COLOR tomato]';icon['hayhaytv']=os.path.join(iconpath,'hayhaytv.png')
	home='http://movies.hayhaytv.vn/';ajax=home+'ajax_hayhaytv.php'
	def namecolor(name):return '%s%s[/COLOR]'%(color['hayhaytv'],name)
	def login():
		u=myaddon.getSetting('userhayhay');p=myaddon.getSetting('passhayhay')
		data=urllib.urlencode({'email':u,'password':p,'remember_account':0})
		response=make_post('http://www.hayhaytv.vn/ajax_jsonp.php?p=jsonp_login',data=data)
		makerequest(joinpath(data_path,'hayhaytv.cookie'),response.cookiestring,attr="wb")
		return response.cookiestring
	def getmaxspeedlink(url,headers):
		body=make_request(url,headers=headers)
		id=xshare_group(re.search('FILM_ID\D{3,7}(\d{3,6})',body),1) if ".sub'" in body else ''
		url=xshare_group(re.search("initVideoUrl.+'(.+?)'",body),1)
		if 'cdnviet.com' not in url:url=xshare_group(re.search("initVideoUrlOld.+'(.+?)'",body),1)
		return url,id
	def getdata(id):#Đoạn code này sử dụng mã bảo mật từ add-on HayHayTV.vn
		url='https://www.fshare.vn/folder/5VNFUPO32P6F'
		hd=xshare_group(re.search('<title>.*xx(.+?)xx.*</title>',make_request(url)),1).split('-')
		data='device=xshare&secure_token=1.0&request='+urllib.quote('{"movie_id":"%s"}'%id)
		response=make_post('http://api.hayhaytv.vn/movie/movie_detail',{hd[0]:'%s %s'%(hd[1],hd[2])},data)
		#print response.json['data']
		try:json=response.json['data']
		except:json={}
		return json		
	def getitems(body):
		p='<a data-tooltip.{,100}href="(.+?)".{,500}data-original="(.+?)".{,300}'
		p+='class="orange_color">(.+?)</span>.{,100}<span>(.*?)</span>'
		for href,img,name_e,name_v in re.findall(p,body,re.DOTALL):
			name=name_v+'-'+color['subscene']+name_e+'[/COLOR]' if name_v else name_e
			addir(name,href,img,fanart,mode,page,query='play')
	def hayhaytv_search(string):
		url='http://www.hayhaytv.vn/tim-kiem/%s/trang-1'%'-'.join(s for s in string.split())
		hayhaytv(name,url,img,mode,page=1,query='M3')

	if query=='hayhaytv.vn':
		name=color['search']+"Search trên hayhaytv.vn[/COLOR]"
		addir(name,'http://www.hayhaytv.vn/tim-kiem/',icon['icon'],mode=mode,query='search',isFolder=True)
		body=make_request(home)
		for href,name in re.findall('menu_fa_text.+?" href="(.+?)".*>(.+?)</a>',body):
			if name in 'PHIM LẺ-PHIM BỘ-SHOW':
				addir(namecolor(name),href,icon['hayhaytv'],fanart,mode,page,query='M1',isFolder=True)
		body=body[body.find('"title_h1_st1"'):body.find('"slider_box_sim slider_clip_box"')]
		items=re.findall('"title_h1_st1">.{,20}<a.{,20}href="(.+?)".{,20}>(.+?)</a>.{,20}</h2>',body,re.DOTALL)
		mucs={'su-kien':'q=su-kien&p=eventfilms&key=32386E61&page=1','phim-le':'p=phimle&page=1',
			'phim-bo':'p=phimbo&page=1','phim-chieu-rap':'p=phimle&phimchieurap&page=1','shows':'p=tvshow&page=1'}
		for href,name in items:
			muc=xshare_group(re.search('http://www.hayhaytv.vn/([\w|-]{1,20})',href),1)
			if muc and mucs[muc]:
				href='http://www.hayhaytv.vn/ajax_ht.php?'+mucs[muc] if 'su-kien' in href else ajax+'?'+mucs[muc]
				name=' '.join(s for s in name.replace('\n','').split() if s)
			else:name=name.replace('JJ','Just Japan')
			addir(namecolor(name),href,img,fanart,mode,page=1,query='M3' if 'su-kien' in href else 'M2',isFolder=True)
	elif query=='search':make_mySearch('','hayhaytv.vn','','',mode,'get')
	elif query=="INP":hayhaytv_search(make_mySearch('',url,'','','','Input'))
	elif url=='hayhaytv.vn':page=1 if 'Trang tiếp theo' not in name else page;hayhaytv_search(query)
	elif query=='M1':
		theloai=os.path.basename(url).replace('-','')
		if theloai=='shows':theloai='tvshow'
		body=make_request('http://www.hayhaytv.vn/tim-kiem');pattern='http.+/\w{1,6}-'
		body=body[body.find(url):];body=body[:body.find('mar-r20')]
		for href,name in re.findall('href="(.+?)".*?>(.+?)</a></li>',body):
			if href==url:href='%s?p=%s&page=1'%(ajax,theloai)
			else:id=re.sub(pattern,'',href);href='%s?p=%s&q=filter&id=%s&page=1'%(ajax,theloai,id)
			addir(namecolor(name),href,img,fanart,mode,page=1,query='M2',isFolder=True)
	elif query=='M2':
		if 'ajax' in url:
			body=make_post(re.sub('page=\d{1,3}','page=%d'%page,url)).body
			pattern='tooltip="(.+?)" href="(.+?)">\s.*"(http://img.+?)".*\s.*color">(.*?)<.*\s.*>(.*?)</span>'
			items=re.findall(pattern,body)
			ids=dict((re.findall('id="(sticky\d{1,3})".{,250}Số tập[\D]{,30}(\d{1,4})',body,re.DOTALL)))
			for stic,href,img,name_e,name_v in items:
				name=name_v+'-'+name_e if name_v else name_e
				if ids.has_key(stic) and ids[stic].strip()>'1':#? in ids.values()
					addir(namecolor(name),href,img,fanart,mode,page=1,query='folder'+ids[stic],isFolder=True)
				else:addir(name,href,img,fanart,mode,page,query='play')
			if len(items)>31 or ('p=tvshow' in url and len(items)>11):
				name='%sTrang tiếp theo: trang %s[/COLOR]'%(color['trangtiep'],page+1)
				addir(name,url,img,fanart,mode,page+1,query,isFolder=True)
			return
		elif 'jj' in url:#Just Japan
			pattern='href="(.+?)">\s.*src="(.+?)".*\s.*\s.*\s.*>(.*?)</a></p>\s.*>(.*?)</a></p>'
			for href,img,name_e,name_v in re.findall(pattern,make_request(url)):
				name=name_v+'-'+color['subscene']+name_e+'[/COLOR]' if name_v else name_e
				addir(name,href,img,fanart,mode,page,query='play')
	elif query=='M3':
		body=make_request(url);body=body[body.find('slide_child_div_dt'):];body=body[:body.find('class="paging"')]
		pattern='href="(.+?)".*\s.*alt="poster phim (.+?)" src="(.+?)"'
		items=re.findall(pattern,body)
		for href,name,img in items:
			if re.search('Tap-\d{1,3}',href):
				addir(namecolor(name),href,img,fanart,mode,page=1,query='folder',isFolder=True)
			else:addir(name,href,img,fanart,mode,page,query='play')
		if len(items)>14 or (len(items)>7 and 'su-kien' in url):
			temp='trang-' if 'trang-' in url else 'page=';url=re.sub('%s\d{1,3}'%temp,'%s%d'%(temp,page+1),url)
			name='%sTrang tiếp theo: trang %s[/COLOR]'%(color['trangtiep'],page+1)
			addir('tt-'+name,url,img,fanart,mode,page+1,query,isFolder=True)
	elif query[:6]=='folder':
		if 'xem-show' in url:pattern='href="(.+?)".*src=".+?"\D*(\d{1,3})<'
		else:pattern='<a class=".*?" href="(.+?)"\D*(\d{1,3})<'
		resp=make_request(url,resp='o');body=resp.body if resp.status==200 else make_request(resp.headers['location'])
		items=re.findall(pattern,body)
		if not query[6:]:
			json=getdata(xshare_group(re.search('FILM_ID\D{3,7}(\d{3,6})',body),1))
			if json:query+=json['total_episode'].encode('utf-8')
		for href,epi in items:
			addir('Tập %s/%s-%s'%(epi,query[6:],re.sub('\[.?COLOR.{,12}\]','',name)),href,img,fanart,mode,page,query='play')
	elif query=='play':
		hd['Cookie']=makerequest(joinpath(data_path,'hayhaytv.cookie'))
		href,id=getmaxspeedlink(url,hd);sub=''
		if not href:hd['Cookie']=login();href,id=getmaxspeedlink(url,hd)
		if href:
			if id:
				json=getdata(id)
				if json:sub=download_subs(json['vn_subtitle'])
			xbmcsetResolvedUrl(href,json['vn_subtitle'] if sub else '')		