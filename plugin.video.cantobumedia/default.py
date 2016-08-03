__author__ = 'phuoclv'
#coding=utf-8
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,urllib,urllib2,re,os,unicodedata,datetime,random,json
import base64

myaddon=xbmcaddon.Addon()
home=xbmc.translatePath(myaddon.getAddonInfo('path'))
datapath=xbmc.translatePath(myaddon.getAddonInfo('profile'))
logos = xbmc.translatePath(os.path.join(home,"logos\\"))
dataPath = xbmc.translatePath(os.path.join(home, 'resources'))
iconpath=os.path.join(datapath,'icon');datapath=os.path.join(datapath,'data')
search_file=os.path.join(datapath,"search.xml");
rows=30

sys.path.append(os.path.join(home,'resources','lib'));from urlfetch import get,post;import getlink;import xshare;
from servers import serversList,fshare,megabox,hdviet,hdonline,hayhayvn;
from utils import xsearch,xrw,xget
from config import hayhaytv_vn,hdviet_com,dangcaphd_com,megabox_vn,phimgiaitri_vn,phimmoi_net, hdonlinevn,megaboxvn,vuahdtv,phimmoinet, csn,csn_logo, nct,nct_logo
from setting import encode2, decode, alert, notify, myaddon

#reload(sys);
#sys.setdefaultencoding("utf8")

www={'hdonline':'[hdonline.vn]','vuahd':'[vuahd.tv]','hdviet':'[http://movies.hdviet.com/]','hayhaytv':'[http://www.hayhaytv.vn/]','dangcaphd':'[http://dangcaphd.com/]','megabox':'[http://phim.megabox.vn/]','phimmoi':'[vuahd.tv]','hdcaphe':'[http://phim.hdcaphe.com/]','phimgiaitri':'[http://phimgiaitri.vn/]'}
color={'trangtiep':'[COLOR lime]','cat':'[COLOR green]','search':'[COLOR red]','phimbo':'[COLOR tomato]','phimle':'[COLOR yellow]'}
media_ext=['aif','iff','m3u','m3u8','m4a','mid','mp3','mpa','ra','wav','wma','3g2','3gp','asf','asx','avi','flv','mov','mp4','mpg','mkv','m4v','rm','swf','vob','wmv','bin','cue','dmg','iso','mdf','toast','vcd','ts','flac','m2ts','dtshd','nrg']
reg = '|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36 VietMedia/1.0'
icon={}
for item in ['fshare', 'hdonline', 'vuahd', 'hdviet', 'hayhaytv', 'dangcaphd', 'megabox', 'phimmoi', 'phimgiaitri', 'next', 'icon', 'id']:
	icon.setdefault(item,os.path.join(logos,'%s.png'%item))
hd={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/600.1.4 Gecko/20100101 Firefox/41.0'}	
### -----------------

try:
	local=xshare.s2u(myaddon.getSetting('thumuccucbo'))
	if not os.path.exists(local):local=xshare.joinpath(datapath,'local')
except:local=xshare.joinpath(datapath,'local')

def setViewMode(view_mode = '2'):
	skin_used = xbmc.getSkinDir()
	if skin_used == 'skin.xeebo':
		xbmc.executebuiltin('Container.SetViewMode(52)')
	else:
		if view_mode == "1": # List
			xbmc.executebuiltin('Container.SetViewMode(502)')
		elif view_mode == "2": # Big List
			xbmc.executebuiltin('Container.SetViewMode(51)')
		elif view_mode == "3": # Thumbnails
			xbmc.executebuiltin('Container.SetViewMode(500)')
		elif view_mode == "4": # Poster Wrap
			xbmc.executebuiltin('Container.SetViewMode(501)')
		elif view_mode == "5": # Fanart
			xbmc.executebuiltin('Container.SetViewMode(508)')
		elif view_mode == "6":  # Media info
			xbmc.executebuiltin('Container.SetViewMode(504)')
		elif view_mode == "7": # Media info 2
			xbmc.executebuiltin('Container.SetViewMode(503)')
		elif view_mode == "8": # Media info 3
			xbmc.executebuiltin('Container.SetViewMode(515)')
		return
	
def strVnEn(str1, str2):
	try:
		str = str1.lower()
		if str == '': return
		if type(str).__name__ == 'unicode': str = str.encode('utf-8')
		items = ["á","à","ả","ạ","ã","â","ấ","ầ","ẩ","ậ","ẫ","ă","ắ","ằ","ẳ","ặ","ẵ","đ","í","ì","ỉ","ị","ĩ","é","è","ẻ","ẹ","ẽ","ê","ế","ề","ể","ệ","ễ","ó","ò","ỏ","ọ","õ","ô","ố","ồ","ổ","ộ","ỗ","ơ","ớ","ờ","ở","ợ","ỡ","ú","ù","ủ","ụ","ũ","ư","ứ","ừ","ử","ự","ữ","ý","ỳ","ỷ","ỵ","ỹ"]
		for item in items:			
			if item in str :
				return str2, str1 + ' - ' + str2
		return str1, str2 + ' - ' + str1
	except: pass	
	
def no_accent(s):
	s=re.sub(u'Đ','D',xshare.s2u(s));s=re.sub(u'đ','d',s)
	return unicodedata.normalize('NFKD', unicode(s)).encode('ASCII', 'ignore')
	
def fixSearchss(titleEnVn, title2):
	titleEnVn = no_accent(titleEnVn).replace(' ','-').replace('+','-').lower().strip()
	titleEnVn = titleEnVn.replace('?','').replace('!','').replace('.','').replace(':','')
	titleEnVn = titleEnVn.replace('&amp;','and').replace('&','and').replace("&#39;",'')
	
	title2 = no_accent(title2).replace(' ','-').replace('+','-').lower().strip()
	title2 = title2.replace('?','').replace('!','').replace('.','').replace(':','')	
	title2 = title2.replace('&amp;','and').replace('&','and').replace("&#39;",'')

	arr = titleEnVn.split('[]')	
	titleEn = arr[0]
	titleVn = arr[1]
	
	try:strYear = arr[2]
	except:strYear=''
	
	if len(strYear) and len(titleVn):
		if (titleEn in title2 and titleVn in title2 and strYear in title2):return True
	elif len(titleVn):
		if (titleEn in title2 and titleVn in title2):return True
	else:
		if (titleEn in title2):return True		
		else:return False
		
###-----------------
def Home():
	datafolder=xbmc.translatePath(myaddon.getAddonInfo('profile'))	
	
	for folder in (datafolder,datapath,iconpath,local):
		if not os.path.exists(folder):os.mkdir(folder)
	xmlheader='<?xml version="1.0" encoding="utf-8">\n';p=datapath;q=local
	for i in [(p,'search.xml'),(q,'mylist.xml')]:
		file=xshare.joinpath(i[0],i[1])
		if not os.path.isfile(file):xshare.makerequest(file,xmlheader,'w')


	content = GetUrl(decode('phuoclv', '2Nzp352bpdPJ4-PSzuvj0OTfkc_l3ZfNsbCvpb3N4-SR5OPc'))
	match=re.compile('<title>(.*?)</title>\s*<link>(.*?)</link>\s*<thumbnail>(.*?)</thumbnail>').findall(content)
	for title,url,thumbnail in match:
		title = '[B]'+title+'[/B]'
		if 'MYPLAYLIST' in url or 'tvcatchup' in url:
			pass
		elif 'Setting' in url:			
			addItem(title,url,'menu_group',thumbnail, False)		
		else:
			addItem(title,url,'menu_group',thumbnail)
			
	setViewMode('3')
		
def Menu_Group(url):
	if 'Setting' in url:
		xbmcaddon.Addon().openSettings()
		return
	elif 'LOCAL' in url:
		Local(name='',url='thumuccucbo',img='',fanart='',mode='local',query='')
	elif 'REMOTE' in url:
		Remote(name='',url='thumuccucbo',img='',mode='remote',page=0,query='')
		
	elif 'PHIM-' in url:
		items2=list()
		
		name='a'
		href='1'
		id=1
		
		if len(items2) == 0:
			items2.append((name,href,id))
		else:
			i=0
			while i < len(items2):
				if name in items2[i]:break				
				i += 1	
			if i==len(items2):items2.append((name,href,id))
		
		
		name='b'
		href='1'
		id=1		

		if len(items2) == 0:
			items2.append((name,href,id))
		else:
			i=0
			while i < len(items2):
				if name in items2[i]:break				
				i += 1	
			if i==len(items2):items2.append((name,href,id))																
			items2.append((str(i),href,id))																
			
		name='b'
		href='1'
		id=1		

		if len(items2) == 0:
			items2.append((name,href,id))
		else:
			i=0
			while i < len(items2):
				if name in items2[i]:break				
				i += 1	
			if i==len(items2):items2.append((name,href,id))
													
		
		folder_list = {'items':items2}
		items = sorted(folder_list.get('items'), key=lambda k: k[0])
		#for title,href,id in items:
			#addItem(title,'MegaBox','search',icon['megabox'])

		danhmucphim = myaddon.getSetting('danhmucphim')
			
		if danhmucphim == 'Tất cả':
			#servers = ['HDOnline', 'VuaHD', 'HDViet', 'HayHayTV', 'DangCapHD', 'MegaBox', 'PhimMoi', 'PhimGiaiTri']
			servers = ['HDOnline', 'HDViet', 'HayHayTV', 'DangCapHD', 'MegaBox', 'PhimMoi']
			for server in servers:
				name='[B]'+'Kho phim '+server+'[/B]'				
				xshare.addir(name,'MenuMovie|'+server,icon[server.lower()],mode='menu_group',query='',isFolder=True)
		elif danhmucphim == 'MegaBox':
			if 'PHIM-LE' in url:href='http://phim.megabox.vn/phim-le'			
			else:href='http://phim.megabox.vn/phim-bo'				
			Category(url=href,mode=mode)			
			setViewMode('1')
		elif danhmucphim == 'HDOnline':	
			if 'PHIM-LE' in url:href='http://m.hdonline.vn/danh-sach/phim-le.html'			
			else:href='http://m.hdonline.vn/danh-sach/phim-bo.html'
			Category(url=href,mode=mode)
		elif danhmucphim == 'HDViet':	
			if 'PHIM-LE' in url:href='http://movies.hdviet.com/phim-le.html'			
			else:href='http://movies.hdviet.com/phim-bo.html'
			Category(url=href,mode=mode)		
			
		setViewMode('1')
		
	elif 'MenuTivi' in url:
		content = GetUrl(url)
		match=re.compile('<title>(.*?)</title>\s*<link>(.*?)</link>\s*<thumbnail>(.*?)</thumbnail>').findall(content)
		for title,url,thumbnail in match:
			addItem(title,url,'index',thumbnail)
		setViewMode('3')
	elif 'MenuMusic' in url:
		content = GetUrl(url)
		match=re.compile('<title>(.*?)</title>\s*<link>(.*?)</link>\s*<thumbnail>(.*?)</thumbnail>').findall(content)
		for title,url,thumb in match:
			if 'nhaccuatui.com' in url or 'chiasenhac.com' in url:
				addItem(title,url,'category',thumb)				
			else:
				addItem(title, url, 'index', thumb)								
		setViewMode('3')
	elif 'MenuShows' in url or 'MenuAddons' in url or 'MenuShare' in url or 'MenuSport' in url or 'MenuChildren' in url:
		content = GetUrl(url)
		match=re.compile('<title>(.*?)</title>\s*<link>(.*?)</link>\s*<thumbnail>(.*?)</thumbnail>').findall(content)
		for title,url,thumbnail in match:
			addItem(title,url,'index',thumbnail)
		setViewMode('3')
		
	elif 'MenuTube' in url or 'Collection' in url:
		content = GetUrl(url)
		names = re.compile('<name>(.+?)</name>\s*<thumbnail>(.+?)</thumbnail>').findall(content)
		for name,thumb in names:
			addItem(name, url, 'index', thumb)
			
		if 'MenuTube' in url: setViewMode('3')
		else: setViewMode('1')
		
	elif 'SEARCH' in url:
		addItem('Tìm kiếm phim','TIMPHIM','search','')
		addItem('Tìm Video Chia Sẻ Nhạc','TimVideoCSN','search',csn_logo)
		addItem('Tìm Video Nhạc Của Tui','TimVideoNCT','search',nct_logo)
		setViewMode('2')
				
def Index(url,name):
	xmlcontent = GetUrl(url)
	if 'FSHARE' in url:
		match = re.compile('<a .+? href="(.+?)" img="(.+?)" fanart="">(.+?)</a>').findall(xmlcontent)
		for link, thumb, title in match:
			if 'folder' in link:
				addItem('*'+title, link, 'episodes', thumb)
			else:
				addItem('-'+title, link, 'stream', thumb, False)
		setViewMode('1')
	elif 'OneTV' in url:
		match = re.compile('"channelName": "(.+?)",\s*"channelNo": "(\d+)",\s*"channelURL": "(.+?)",').findall(xmlcontent)
		for title, stt, link in match:
			addLink( stt + ' . '  + title, link, 'stream', 'http://truyenhinhfpthanoi.com/uploads/logo.png')			
	elif 'm3u' in url:
		match = re.compile('#EXTINF:-?\d,(.+?)\n(.+)').findall(m3ucontent)
		#match = re.compile('#EXTINF.+,(.+)\s(.+?)\s').findall(xmlcontent)
		for name, url in match:
			addLink(name.replace('TVSHOW - ','').replace('MUSIC - ',''), url, 'stream', iconimage)
	elif 'MenuCollection.xml' in url or 'MenuTube.xml' in url:#mytubetube, bo suu tap
		body=xsearch('<name>'+name+'</name>(.+?)</channel>',xmlcontent,1,re.DOTALL)
		
		items = re.findall('<title>(.*?)</title>\s*<link>(.*?)</link>\s*<thumbnail>(.*?)</thumbnail>',body,re.DOTALL)
		for title, link, thumb in items:
			if 'MenuTube' in url:
				addItem(title, link, 'episodes', thumb)
			else:#bo suu tap
				addItem(title, '', 'serverlist&query='+link, thumb)	
			
	elif 'xml' in url:#tivi
		items = re.compile('<channel>\s*<name>.+?</name>((?s).+?)</channel>').findall(xmlcontent)
		for item in items:	
			match = re.compile('<title>(.*?)</title>\s*<link>(.*?)</link>\s*<thumbnail>(.*?)</thumbnail>').findall(item)
			for title, link, thumb in match:
				addLink(title, link, 'stream', thumb)
		setViewMode('3')
	
	
def IndexLocal(url):
	xmlcontent = GetUrl(url)
	if 'xml' in url:
		match = re.compile('<a .+? href="(.+?)" img="(.+?)" fanart="">(.+?)</a>').findall(xmlcontent)
		for link, thumb, title in match:
			if 'folder' in link:
				addItem(title, link, 'episodes', thumb)
			else:
				addLink(title, link, 'stream', thumb)
	setViewMode('1')			
		
def Category(url, mode='', name='', query=''):
	moi_cap_nhat = '[B]Mới cập nhật[/B]'
	if 'hdonline.vn' in url:
		b=xshare.xread(url)
		if [s for s in ['Mới','Lẻ','Bộ'] if s in name]:
			s=xsearch('(<a href="%s".+?</ul>)'%url,b,1,re.DOTALL)
			
			addItem(moi_cap_nhat, 'http://phim.megabox.vn/phim-le', 'search_result&query=phim-le_moicapnhat', icon['hdonline'])
			for href,title in re.findall('<a href="(.+?)" title=.+?</i>(.+?)</a>',s):
				addItem(title.replace('Phim ', ''), href.replace('m.', ''), 'search_result&query=phimle-serverlist', icon['hdonline'])
	elif 'megabox.vn' in url:
		content = GetUrl(url)
		if 'phim-le' in url:			
			addItem(moi_cap_nhat, 'http://phim.megabox.vn/phim-le', 'search_result&query=phim-le_moicapnhat', icon['megabox'])
			match = re.compile("href='phim-le(.+?)'>(.+?)<").findall(content) 
			for href, name in match:
				if 'Phim' in name:pass
				else:addItem(name, url+href, 'search_result', icon['megabox'])			
		elif 'phim-bo' in url:
			addItem(moi_cap_nhat, 'http://phim.megabox.vn/phim-bo', 'search_result&query=phim-bo_moicapnhat', icon['megabox'])
			match = re.compile("href='phim-bo(.+?)'>(.+?)<").findall(content) 
			for href, name in match:
				if 'Phim' in name:pass
				else:addItem(name, url+href, 'search_result', icon['megabox'])						
	elif 'hdviet.com' in url:		
		if 'phim-le' in url:
			body=xshare.make_request('http://movies.hdviet.com/phim-le.html')
			items=re.findall('<a href="(.+?)" .?menuid="(.+?)" .?title=".+?" >(.+?)</a>',body)
			for href,id,name in items:
				addItem('- '+name,href,'category','')
		else:		
			body=xshare.make_request('http://movies.hdviet.com/phim-bo.html')
			items=re.findall('<a href="(.+?)" menuid="(.+?)" title=".+?">(.+?)</a>',body)
			items+=re.findall('<a class="childparentlib" menuid="(.+?)" href="(.+?)" title=".+?">(\s.*.+?)</a>',body)
			for href,id,name in items:
				if 'au-my' in href or 'tai-lieu' in href:name='Âu Mỹ %s'%name.strip()
				elif 'hong-kong' in href:name='Hồng Kông %s'%name.strip()
				elif 'trung-quoc' in href:name='Trung Quốc %s'%name.strip()
				else:name=name.strip()
				if href in '38-39-40':temp=href;href=id;id=temp
				addItem('- '+name,href,'category','')
						
	elif 'PhimMoi' in url:
		addItem(color['search']+'Tìm kiếm kho phim PhimMoi[/COLOR]','PhimMoi','search',icon['phimmoi'])
		body=xshare.make_request(phimmoi_net)
		content=xshare.xsearch('<ul id=".+?"(.+?)</ul></div>',body,1)
		for title in re.findall('<a>(.+?)</a>',content):
			addLink('[B]'+title+'[/B]',"",0,img)
			#xshare.addir('[B]'+title+'[/B]','',icon['phimmoi'],mode=mode,query='menubar',isFolder=True)

			content_=xshare.xsearch('<ul id=".+?"(.+?)</ul></div>',body,1)
			gen={'Thể loại':'the-loai','Quốc gia':'quoc-gia','Phim lẻ':'phim-le','Phim bộ':'phim-bo'}
			query=gen.get(re.sub('\[/?COLOR.*?\]|\(.+?\)','',title).strip())
			pattern='<a href="(%s/.*?)">(.+?)</a>'%query
			for href,title in re.findall(pattern,content_):
				xshare.addir('- '+title,phimmoi_net+href,icon['phimmoi'],mode='category',isFolder=True)
						
		for href,title in re.findall('<a href="([\w|-]+/|http://www.phimmoi.net/tags/.*?)">(.+?)</a>',content):
			if 'tags' not in href:href=phimmoi_net+href
			xshare.addir('[B]'+title+'[/B]',href,icon['phimmoi'],mode='category',isFolder=True)

			content_=xshare.xsearch('<ul id=".+?"(.+?)</ul></div>',body,1)
			gen={'Thể loại':'the-loai','Quốc gia':'quoc-gia','Phim lẻ':'phim-le','Phim bộ':'phim-bo'}
			query=gen.get(re.sub('\[/?COLOR.*?\]|\(.+?\)','',title).strip())
			pattern='<a href="(%s/.*?)">(.+?)</a>'%query
			for href,title in re.findall(pattern,content_):
				if len(href)>8:	#bỏ danh mục phim-le, phim-bo
					xshare.addir('- '+title,phimmoi_net+href,icon['phimmoi'],mode='category',isFolder=True)					
	
	
	elif 'ott.thuynga' in url:
		match=menulist(dataPath+'/data/category.xml')
		for title,url,thumbnail in match:	  
			if 'ott.thuynga' in url:
				addItem(title,url,'episodes',thumbnail)
			else:pass				
	elif 'chiasenhac' in url:
		content=GetUrl(url)
		addItem(color['search']+'Tìm kiếm[/COLOR]','TimVideoCSN','search',csn_logo)	
		
		match=re.compile("<a href=\"hd(.+?)\" title=\"([^\"]*)\"").findall(content)[1:8]
		for url,name in match:
			addItem(name,csn+'hd'+url,'episodes',csn_logo)
	elif 'nhaccuatui' in url:
		content=GetUrl(url)
		addItem(color['search']+'Tìm kiếm[/COLOR]','TimVideoNCT','search',nct_logo)	
	
		match = re.compile("href=\"http:\/\/m.nhaccuatui.com\/mv\/(.+?)\" title=\"([^\"]*)\"").findall(content)
		for url, name in match:		
			if 'Phim' in name:
				pass
			else:
				addItem(name,nct + 'mv/' + url,'search_result',nct_logo)
		#match = re.compile("href=\"http:\/\/m.nhaccuatui.com\/mv\/(.+?)\" title=\"([^\"]*)\"").findall(content)
		#for url, name in match:
			#if 'Phim' in name:
				#add_dir('[COLOR orange]' + name + '[/COLOR]', nctm + 'mv/' + url, 3, logos + 'nhaccuatui.png', fanart)					
	else:
		if 'moicapnhatserverkhac---' in query:
			#servers = ['HDOnline', 'VuaHD', 'HDViet', 'HayHayTV', 'DangCapHD', 'MegaBox', 'PhimMoi', 'PhimGiaiTri']
			servers = ['HDOnline', 'HDViet', 'HayHayTV', 'DangCapHD', 'MegaBox', 'PhimMoi']
			for server in servers:		
				if server == 'MegaBox' and danhmucphim != 'MegaBox':
					if 'phim-le' in query:
						addItem('[B]'+server+'[/B]', 'http://phim.megabox.vn/phim-le', 'search_result&query=phim-le_moicapnhat2', icon['megabox'])			
					else:
						addItem('[B]'+server+'[/B]', 'http://phim.megabox.vn/phim-bo', 'search_result&query=phim-bo_moicapnhat2', icon['megabox'])
			return
		elif 'moicapnhat---' in query and 'moicapnhat2' not in query:
			moi_cap_nhat = color['search']+'[B]Mới cập nhật server khác[/B][/COLOR]'
			addItem(moi_cap_nhat,'','category&query='+query+'serverkhac',"")
	
		Search_Result(url, mode=mode, query=query)
	setViewMode('1')

def episodes(url, name='', page=0):
	if 'hdonline.vn' in url :
		if 'Các tập tiếp theo' in  name:name= url.split('.html')[1];url= url.split('.html')[0]+'.html'
		else:name=name
		id=xsearch('-(\d+)\.html',url)
						
		for href,epi in hdonline.eps(id,page):
			if 'Các tập tiếp theo' in href:
				addItem(href,url+name,mode,'')
				#addir_info(href,url+name,img,'',mode,page+1,query,True)
			else:
				addLink('Tập-'+epi, url, 'stream', img)				
				#addir_info(title,href,img,'',mode,1,'play',menu=menu)		
	
		#items=re.findall('<a href="(.+?)" .+?"><span>(.+?)</span></a>',xshare.make_request(url));
		#for url, eps in items:
			#name = name.replace('[COLOR tomato]', '').replace('[/COLOR]', '')						
			#addLink('Tập ' + str(eps), url, 'stream', img)
	elif 'vuahd.tv' in url :
		items=re.findall('<a href="#" class="btn-1 btnUpgrade">Xem (.+?)</a>',xshare.make_request(url));temp=[]
		for eps in items:	
			if eps not in temp:
				temp.append(eps);title=eps+'-'+name;tap=xshare.xshare_group(re.search('(\d{1,3})',eps),1)
				if tap:tap=format(int(tap),'02d')
				else:continue
				url = url.replace('tv-series/','')+'-%s'%tap
				url = url+'/watch'
				url = vuahdtv + url.replace('/', '%2F')			
				xshare.addir(title,url,img,'fanart',mode='16',isFolder=False)		
	elif 'hdviet.com' in url :
		url = query		
		href='http://movies.hdviet.com/lay-danh-sach-tap-phim.html?id=%s'%url
		response=xshare.make_request(href,resp='j')
		if not response:return
		for eps in range(1,int(response["Sequence"])+1):		
			name=re.sub(' \[COLOR tomato\]\(\d{1,4}\)\[/COLOR\]','',name)
			title='Tập %s/%s-%s'%(format(eps,'0%dd'%len(response['Episode'])),str(response['Episode']),re.sub('\[.?COLOR.{,12}\]','',name))
			xshare.addir(title,'%s_e%d'%(url,eps),img,fanart='',mode='22',page=1,query='hdvietplay')		
	elif 'hayhaytv.vn' in url :	
		b=re.sub('>\s*<','><',xshare.xread(url))
		s=re.findall('<a class="ep-link.+?href="(.+?)">(.+?)</a>',b)
		if not s:
			addItem(name,href,'stream',img,False)
		else:
			for href,title in s:
				addItem('Tập '+title,href,'stream',img,False)				

	
	elif 'phimmoi.net' in url :	
		plg='plugin://plugin.video.hkn.phimmoi/?action=list_media_items&path='
	
		body=xshare.make_request(url+'xem-phim.html')
		menu={'tuphim':{'action':'Add','server':['phimmoi.net']}}
		eps=xsearch('(/\d{1,4})\)',name)
		name=re.sub('\[/?COLOR.*?\]|\(.+?\)|\d{1,3} phút/tập|\d{1,3} phút','',name).strip()
		
		for detail in re.findall('(<div class="server clearfix server-group".+?</ul>)',body,re.DOTALL):
			title=' '.join(s for s in xsearch('<h3 class="server-name">(.+?)</h3>',detail,1,re.DOTALL).split())
			if title and 'tập phim' not in title:
				serverid=xsearch('data-serverid="(.+?)"',detail)
				#add_sep_item('-------%s-------'%(title+' - '+serverid))
			label=name.replace('TM ','') if title and 'Thuyết minh' not in title else name
			for title,href in re.findall('title="(.+?)".+?href="(.+?)"',detail,re.DOTALL):		
				addItem(title+plg+'http://www.phimmoi.net/'+href,plg+'http://www.phimmoi.net/'+href,'stream',img)
	
		
	elif 'megabox.vn' in url :	
		content = GetUrl(url)
		match = re.compile("href='(.+?)' >(\d+)<").findall(content)
		for url, epi in match:
			addLink('Tập ' + epi, url, 'stream', img)
	elif 'phimgiaitri.vn' in url :		
		addLink('Tập 1', url, 'stream', img)
		
		content = GetUrl(url)
		match = re.compile('<a href="(.+?)" page=(.+?)>').findall(content)
		for url,title in match:		
			addLink('Tập ' + title, url, 'stream', img)
	elif 'youtube' in url:
		addLink(name, url, 'stream', thumbnail)
	elif 'chiasenhac' in url:
		content = GetUrl(url)
		items=re.compile("<a href=\"([^\"]*)\" title=\"(.*?)\"><img src=\"([^\"]+)\"\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s*<span style=\"color: .*?\">(.*?)</span>").findall(content)
		for url,name,thumbnail,cat in items:
			addLink(name+color['cat']+' ['+cat+'][/COLOR]',csn+url,'stream',thumbnail)
		items=re.compile("<a href=\"hd\/video\/([a-z]-video\/new[0-9]+).html\" class=\"npage\">(\d+)<\/a>").findall(content)
		for url,name in items:
			addItem('[COLOR lime]Mới Chia Sẻ - Trang '+name+'[/COLOR]',csn+'hd/video/'+url+'.html','episodes',icon['next'])
		items=re.compile("<a href=\"hd\/video\/([a-z]-video\/down[0-9]+).html\" class=\"npage\">(\d+)<\/a>").findall(content)
		for url,name in items:
			addItem('[COLOR red]Download mới nhất - Trang '+name+'[/COLOR]',csn+'hd/video/'+url+'.html','episodes',icon['next'])
	elif 'fshare.vn' in url:
		items2=list()

		body = GetUrl(url)
		for content in re.findall('<div class="pull-left file_name(.+?)<div class="clearfix"></div>',body,re.S):
			item=re.search('data-id="(.+?)".+?href="(.+?)".+?title="(.+?)"',content)
			if item:
				size=xsearch('<div class="pull-left file_size align-right">(.+?)</div>',content).strip()
				id=item.group(1);type='file' if 'file' in item.group(2) else 'folder';name=item.group(3)				
				if type=='file':href='https://www.fshare.vn/file/%s'%id
				else:href='https://www.fshare.vn/folder/%s'%id
				items2.append((name,href,id))														
			
		folder_list = {'items':items2}
		items = items = sorted(folder_list.get('items'), key=lambda k: k[0])
		for title,href,id in items:
			if 'www.fshare.vn/folder' in href:
				title = '[B]' + title + '[/B]'
				addItem(title, href, 'episodes', '')
			elif 'www.fshare.vn/file' in href:
				addLink(title, href, 'stream', '')

def Remote(name,url,img,mode,page,query):
	def check_id_internal(id):
		return '','',''
		xshare.mess('ID Checking on xshare.vn','',1000)
		r1='href="(.+%s.*)" img="(.*?)">(.+?)</a>';r2='img="(.*?)" fanart=".*?" href="(.+%s.*)">(.+?)</a>'
		files='phimfshare.xml-hdvietnam.xml';title=''
		for file in ['vaphim.xml','ifiletv.xml','phimfshare.xml','hdvietnam.xml']:
			body=xshare.makerequest(xshare.joinpath(datapath,file));id=id.lower() if len(id)>13 else id
			items=re.search(r1%id,body) if file in files else re.search(r2%id,body)
			if items:
				title=items.group(3)
				href=items.group(1 if file in files else 2)
				img=items.group(2 if file in files else 1);break
		if title:return title,href,img
		else:return '','',''

	def check_id_fshare(id):
		xshare.mess('ID Checking on Fshare.vn','',1000)
		href='https://www.fshare.vn/file/%s'%id;body=xshare.make_request(href);title=''
		if 'class="file-info"' in body:title=xsearch('<title>(.+?)</title>',body).replace('Fshare - ','')
		else:
			href='https://www.fshare.vn/folder/%s'%id
			body=xshare.make_request(href)
			if id in body:title=xsearch('<title>(.+?)</title>',body).replace('Fshare - ','')
		if title:return title,href,icon['fshare']
		else:return '','',''
	
	if page==0:
		name=color['search']+'Nhập ID/link: Fshare[/COLOR]'
		addItem(name,url,mode+'&page=1',icon['icon'])
		for href,name in re.findall('<a href="(.+?)">(.+?)</a>',xshare.makerequest(search_file)):
			#q='ID?xml' if '.xml' in name else 'ID?'+query									
			if 'www.fshare.vn/folder' in href:
				name = '[B]Fshare - ' + name + '[/B]'
				addItem(name, href, 'episodes', icon['id'])
			elif 'www.fshare.vn/file' in href:
				name = 'Fshare - ' + name
				addLink(name, href, 'stream', '')
	elif page == 1:#Nhập ID mới BIDXFYDOZMWF
		idf = xshare.get_input('Hãy nhập chuỗi ID của Fshare')#;record=[]
		if idf is None or idf.strip()=='':return 'no'
		if 'subscene.com' in idf:return subscene(name,''.join(s for s in idf.split()),'subscene.com')
		idf = xsearch('(\w{10,20})',''.join(s for s in idf.split()).upper())
		if len(idf)<10:xshare.mess(u'Bạn nhập ID link chưa đúng: %s!'%idf);return 'no'
		title,href,img=check_id_internal(idf)
		if not title:# or True:
			title,href,img=check_id_fshare(idf)
			#if not title:
				#title,href,img=check_id_4share(idf)
				#if not title:title,href,img=check_id_tenlua(idf)
		if title and href:
			xshare.make_mySearch(title,href,img,'',mode,'Add');
			
			if 'www.fshare.vn/folder' in href:
				title = '[B]Fshare - ' + title + '[/B]'
				addItem(title, href, 'episodes', icon['id'])
			elif 'www.fshare.vn/file' in href:
				title = 'Fshare - ' + title
				addLink(title, href, 'stream', '')
		else:xshare.mess(u'Không tìm được link có ID: %s!'%idf);return 'no'
	return ''				

def Local(name,url,img,fanart,mode,query):
	if url=='thumuccucbo':url=local
	url=xshare.s2u(url)
	for filename in os.listdir(url):
		filenamefullpath = xshare.u2s(xshare.joinpath(url, filename));filename= xshare.u2s(filename)
		if os.path.isfile(xshare.joinpath(url, filename)):
			size=os.path.getsize(xshare.joinpath(url, filename))/1024		
			if size>1048576:size='%dGB'%(size/1048576)
			elif size>1024:size='%dMB'%(size/1024)
			else:size='%dKB'%size
			name=filename+' - %s'%size		
				
			file_ext=os.path.splitext(filenamefullpath)[1][1:].lower()
			if file_ext=='xml':
				addItem(name,filenamefullpath,'indexlocal',icon['icon'])
			else:pass
		else:
			name='[B]'+filename+'[/B]'
			addItem(name,filenamefullpath,'local',icon['icon'])
	return
	
def ServerList(name, url, mode, page, query, img):
	strTitle = query
	search_string = query.split('[]')[0]
	strYear=str(page)	

	danhmucphim=myaddon.getSetting('danhmucphim')
	if url:	
		name='['+danhmucphim+'] '+name		
		if 'phim-le' in mode : v_mode='stream';isFolder=False
		else : v_mode='episodes';isFolder=True				
		addItem(name,url,v_mode,img,isFolder)
	else:danhmucphim='www.khongdunghang.com'
	
	try:	
		url = 'http://fsharefilm.com/?s=%s'%search_string
		body = GetUrl(url)
		for content in re.findall('<div class="movie col-xs-6 col-sm-3 col-md-3 col-lg-3">(.+?)<span class="pull-right movie-quality">',body,re.S):
			title=xsearch('alt="(.+?)"/>',content).replace('&#8211;','-')
			
			if fixSearchss(search_string, title): # xu ly tim kiem cho nhieu ket qua							
				href=xsearch('href="(.+?)">',content)
				img=xsearch('src="(.+?)" alt',content)
				eps=xsearch('<span class="pull-left movie-time">(.+?)</span>',content)
								
				content = GetUrl(href)
				match = re.compile('<a.+?href="(.+?)" target="_blank">(.+?</a>.+?)>').findall(content)
				if len(match) > 0:				
					for link, epi in match:
						if '4share' in link or 'Phụ đề Việt' in epi or 'Phụ Đề Việt' in epi:
							pass 
						elif 'fshare.vn/file' in link:
							if 'fshare.vn' in epi: artist = 'Link Vip'
							else: artist = epi.split('</a>')[0]
						elif 'fshare.vn/folder' in link:
							if 'fshare.vn/folder' in epi: artist = 'Link Vip' + epi.split('</a>')[-1].replace('</p','')
							else: artist = epi.replace('</a><br /','')
							
					if fixSearchss(strTitle, title):
						if 'tập' in eps.lower():
							addItem('[FSHARE] ' + title, link, 'episodes', img)
						else:addItem('[FSHARE] ' + title, link, 'stream', img, isFolder=False)		
	except:pass
						
	srvl=serversList()
			
	query=search_string
	href='https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=20&hl=vi&prettyPrint=false&source=gcsc&gss=.com&cx=009789051051551375973:rgvcpqg3uqw&googlehost=www.google.com&callback=google.search.Search.apiary19044&q='
	href+=urllib.quote_plus('"%s"'%' '.join(query.split()))
	
	if 'Page next:' in name:href+='&start=%d'%((page-1)*100)
	else:page=1
	s=srvl.search(href)
	for title,href,img in s:
		domain=href.split("//")[-1].split("www.")[-1].split("/")[0]
		m=int(dict(srvl.servers).get(domain,'0'))
		#title = str(m) +'-'+domain + ' ' + title

		if 'megabox.vn' in href:
			strYear = xsearch('Năm phát hành:</span> .+?-.+?-(.+?)</li>',GetUrl(href))
			title = title + ' (' + strYear + ')'
		else:strYear=''
		print '-'+href,title	
		
		if fixSearchss(strTitle, title) and danhmucphim not in href: # xu ly tim kiem cho nhieu ket qua		
			isFolder=True
			if 'bilutv.com' in href:			
				if '/xem-phim/' in href:v_mode='play'
				elif '/phim/' in href:v_mode='folder'
				elif '/tag/' in href:v_mode='page'
				else:v_mode='episodes'
			elif 'megabox.vn' in href:								
				title = '[MegaBox] ' + title
												
				v_mode='stream';isFolder=False				
			elif 'hdonline.vn' in href:
				title = '[HDOnline] ' + title
				if '/tag1/' in href:
					v_mode='page'
					continue
				else:
					v_mode= 'episodes'
					filmid = xsearch('-(\d+?).html',href)		
					plg='plugin://plugin.video.hkn.hdonline/?action=ListEpisodes&filmid='
					href = plg + str(filmid)
			elif 'hayhaytv.vn' in href:
				continue
				v_mode='eps'
			elif 'phimbathu.com' in href:
				if '/xem-phim/' in href:
					title = '[PhimBatHu] ' + title
					v_mode= 'episodes'				
				else:continue				
			elif 'phim3s.net' in href:
				if '/xem-phim/' in href:
					title = '[Phim3S] ' + title
					if '/phim-le/' in href:v_mode= 'stream';isFolder=False			
					else:v_mode= 'episodes';isFolder=True
				else:continue								
			elif 'hdsieunhanh.com' in href:			
				title = '[HDSieuNhanh] ' + title
				v_mode= 'play'
			elif 'phimnhanh.com' in href:			
				title = '[PhimNhanh] ' + title
				v_mode= 'series'				
			elif 'phimmoi.net' in href:
				v_mode='stream'
				if 'xem-phim.html' in href or 'download.html' in href or 'trailer.html' in href :continue
				else:
					title = '[PhimMoi] ' + title
					plg='plugin://plugin.video.hkn.phimmoi/?action=list_media_items&path='
					href=plg+href
			elif 'mphim.net' in href:				
				title = '[MPhim] ' + title
				if 'download-phim' in href:continue
				v_mode='eps'					
			else:
				title = domain + ' ' + title
				v_mode= 'episodes'
				#continue
				
			if 'plugin' not in href and 'megabox.vn' not in href: href='plugin://plugin.video.xshare/?mode='+str(m)+'&name='+title+'&url='+href+'&img='+img+'&query='+v_mode+'&page=1'
			addItem(title,href,v_mode,img,isFolder)		
			
	return
	if danhmucphim <> 'HDOnline':	
		url='http://hdonline.vn/tim-kiem/%s.html'%search_string
		#url='http://m.hdonline.vn/tim-kiem/%s/trang-1.html'%search_string
		Search_Result(url, mode, query)			
	if danhmucphim <> 'VuaHD':
		url='http://vuahd.tv/movies/q/%s'%search_string
		#Search_Result(url, mode, query)
	if danhmucphim <> 'HDViet':		
		url='http://movies.hdviet.com/tim-kiem.html?keyword=%s'%search_string
		Search_Result(url, mode, query)	
	if danhmucphim <> 'HayHayTV':
		url=hayhaytv_vn+'tim-kiem/%s/trang-1'%search_string
		url='http://www.hayhaytv.vn/tim-kiem.html?term='+search_string		
		#Search_Result(url, mode, query)	
	if danhmucphim <> 'DangCapHD':
		url='http://dangcaphd.com/movie/search.html?key=%s&search_movie=1'%search_string
		#Search_Result(url, mode, query)	
	if danhmucphim <> 'MegaBox':
		url='http://phim.megabox.vn/search/index?keyword=' + search_string#+'/phim-le'
		#try:Search_Result(url, mode, query)	
		#except:pass
	if danhmucphim <> 'PhimMoi':
		url='http://www.phimmoi.net/tim-kiem/%s/'%search_string
		Search_Result(url, mode, query)	
		
	if danhmucphim <> 'PhimGiaiTri':
		url = phimgiaitri_vn+'result.php?type=search&keywords='+search_string      
		try:Search_Result(url, mode, query)	
		except:pass
						
def Search(url): 	
	if '-' in url:query='-'
	else:query=''

	try:
		keyb=xbmc.Keyboard('', color['search']+'Nhập nội dung cần tìm kiếm[/COLOR]')
		keyb.doModal()
		if (keyb.isConfirmed()):
			string_input = keyb.getText()		
			searchText=urllib.quote_plus(keyb.getText())
			
		if 'TimVideoCSN' in url:  
			url=csn+'search.php?s='+searchText+'&cat=video'      
			Search_Result(url, mode, query)
		elif 'TimVideoNCT' in url:
			url = nct + 'tim-kiem/mv?q=' + searchText     
			Search_Result(url, mode, query)
		elif 'TIMPHIM' in url:
			url = 'http://hdonline.vn/tim-kiem/'+searchText.replace('+', '-')+'.html'      			
			#url='http://m.hdonline.vn/tim-kiem/%s/trang-1.html'%searchText.replace('+', '-')
	   
			query = string_input
			mode = 'search'
			Search_Result(url, mode, query)
	except:pass	

def Search_Result(url, mode='', query=''):
	search_string = '[]'
	if 'serverlist' not in mode:mode = mode +'_phim-le_phim-bo'	
	if 'search' in mode: search_string = query + '[]' + query + '[]' + query
	
	if 'hdonline.vn' in url:
		body = GetUrl(url)				
		hdo=hdonline()
		items = hdo.additems(body,mode)
		for title,href,mode_query,img,isFolder in items:
			if fixSearchss(search_string, title): # xu ly tim kiem cho nhieu ket qua		
				addItem(title,href,mode_query,img,isFolder)
				
	elif 'megabox.vn' in url:	
		body = GetUrl(url)		
		mgb=megabox()
		items = mgb.additems(body,mode)
		for title,href,mode_query,img,isFolder in items:
			addItem(title,href,mode_query,img,isFolder)		
		try:
			items = re.compile('class="next"><a href="(.+?)">').findall(body)
			addItem(color['trangtiep']+'Trang tiếp theo[/COLOR]', megabox_vn + items[0],'search_result&query='+query,icon['next'])
		except:pass					
	elif 'hdviet.com' in url:
		b=xshare.xread(url)
		body=xsearch('("cf box-movie-list box-movie-list-search".+?<div class="box-ribbon mt-15">)',b,1,re.DOTALL)

		hdv=hdviet()
		items = hdv.additems(body,mode)	
		for title,href,mode_query,img,isFolder in items:
			if fixSearchss(search_string, title): # xu ly tim kiem cho nhieu ket qua		
				addItem(title,href,mode_query,img,isFolder)
						
		if 'serverlist' not in mode:			
			s=xsearch('(<ul class="paginglist paginglist-center">.+?</ul>)',b,1,re.DOTALL)
			i=re.search('"active"[^"]+""><a href="([^"]+)">(\d+)</a>',s)
			if s:
				un=i.group(1);pn=i.group(2);pages=xsearch('>(\d+)</a></li></ul>',s)
				title='%sTrang tiếp theo: trang %s/%s[/COLOR]'%(color['trangtiep'],pn,pages)
				addLink(title, 'hdviet.com', 'search_result&query='+query, icon['next'])
				#addir(title,un,img,fanart,mode,page,'else',True)				
	elif 'hayhaytv' in url:					
		hd={'User-Agent':'Mozilla/5.0','X-Requested-With':'XMLHttpRequest'}
		try:j=json.loads(xshare.xread(url,{'User-Agent':'Mozilla/5.0','X-Requested-With':'XMLHttpRequest'}))
		except:j={}
		for s in ('director','phim','actor','show'):
			for i in j.get(s,[]):
				title=i.get('name').encode('utf-8')+' - '+i.get('extension').encode('utf-8')
				href=i.get('link')
				img=i.get('image')
				eps=(i.get('last_episode')+'/'+i.get('total_episode')) if i.get('total_episode')>'1' else ''
				eps=eps.encode('utf-8')
				if fixSearchss(search_string, title): # xu ly tim kiem cho nhieu ket qua		
					if not eps:addItem('[HayHayTV] '+title,href,'stream',img,False)							
					else:addItem('[HayHayTV] '+title,href,'episodes',img)	
	elif 'vuahd' in url:pass	
	elif 'dangcaphd' in url:pass
	elif 'phimmoi' in url:
		plg='plugin://plugin.video.hkn.phimmoi/?action=list_media_items&path='
	
		body=xshare.make_request(url);
		for s in re.findall('(<li class="movie-item">.+?</li>)',body,re.DOTALL):
			title=xsearch('title="(.+?)"',s)
			titleVn=xsearch('<span class="movie-title-1">(.+?)</span>',s)
			titleEn=xsearch('<span class="movie-title-2">(.+?)</span>',s)
			#duration=xsearch('>(\d{1,3}.?phút)',s)
			#label=xsearch('"ribbon">(.+?)</span>',s)
			#if label:title+=' [COLOR green]%s[/COLOR]'%label
			href=xsearch('href="(.+?)"',s)
						
			b=xshare.xread('http://www.phimmoi.net/'+href)
			if 'Năm:</dt><dd class="movie-dd">' in b:
				year = xsearch('Năm:</dt><dd class="movie-dd">.+?(\d{1,4})</a>',b,1,re.DOTALL)
			elif 'Ngày phát hành:</dt><dd class="movie-dd">' in b:
				year = xsearch('Ngày phát hành:</dt><dd class="movie-dd">.+?/.+?/(.+?)</dd>',b,1,re.DOTALL)
			else:
				year = xsearch('Ngày ra rạp:</dt><dd class="movie-dd">.+?/.+?/(.+?)</dd>',b,1,re.DOTALL)
			
			title = title + ' (' + year + ')'
				
			if fixSearchss(search_string, title): # xu ly tim kiem cho nhieu ket qua					
				img=xsearch('url=(.+?)%',s)
				eps=xsearch('Tập ?(\d{,4}/\d{,4}|\?/\d{,4}|\d{,4})',s)
				if not eps:
					epi=xsearch('class="eps">Trọn bộ ?(\d{1,4}) ?tập</div>',s)
					if epi:eps='%s/%s'%(epi,epi)
				else:epi=eps.split('/')[0]
				try:epi=int(epi)
				except:epi=0
				
				if xsearch('<dd class="movie-dd status">Trailer',b,0):
					v_mode='stream'
					return
				elif epi>1 or 'phút/tập' in s:# or 'Phim bộ hot trong tuần' in name:
					v_mode='episodes';title=(title)
				else:v_mode='stream'
				
				dur=xsearch('>(\d{1,3}.?phút)',s)			
				addItem('[PhimMoi] '+title,plg+'http://www.phimmoi.net/'+href,'',img)
				#if v_mode=='stream':addItem('[PhimMoi] '+title,plg+'http://www.phimmoi.net/'+href,'',img)
				#else:addItem('[PhimMoi] '+title,'http://www.phimmoi.net/'+href,v_mode,img)
			
		urlnext=xsearch('<li><a href="(.+?)">Trang kế.+?</a></li>',body)
		if urlnext:
			pagenext=xsearch('/page-(\d{1,3})\.html',urlnext)
			name='%sTrang tiếp theo: trang %s[/COLOR]'%(color['trangtiep'],pagenext)
			#xshare.addir_info(name,'http://www.phimmoi.net/'+urlnext,img,fanart,mode,page,'readpage',True)
	elif 'phimgiaitri' in url:
		content = xshare.make_request(url)			
		#try:
		#items = re.compile('<a style=\'text-decoration:none\' href=\'([^\']*).html\'>\s*<img style=.+?src=(.+?) ><table style.+?:0px\'>(.+?)\s*<\/font>').findall(content)
		items = re.compile('<a style=\'text-decoration:none\' href=\'([^\']*).html\'>\s*<img style=.+?src=(.+?) ><table style.+?:0px\'>(.+?)\s*</font>.+?\'> (.+?)</font>').findall(content)
		for href,img,namevn,nameen in items:		
			strNameEn, name =  strVnEn(namevn, nameen)
			if query=='':
				v_mode='16'						
				isFolder=False
			elif query=='-':
				v_mode='12'
			else:
				name = '[PhimGiaiTri] ' + name
				v_mode='12'			
			href = phimgiaitri_vn+href+'/Tap-1.html'
			addLink(name,href,'stream',phimgiaitri_vn+img)
			#xshare.addir(href,href,phimgiaitri_vn+img,'fanart',mode='stream',page=1,query='play',isFolder=False)
			
			#href = phimgiaitri_vn  + 'http:%2F%2Fphimgiaitri.vn%2F' + href.replace('/', '%2F')
			#xshare.addir(href,href,phimgiaitri_vn+img,'fanart',mode='16',page=1,query='play',isFolder=False)

		items = re.compile('<a style=\'text-decoration:none\' href=\'([^\']*).html\'>\s*<img style=.+?src=(.+?) ><div class=\'text\'>\s*(.+?)\s*</div><table style.+?:0px\'>(.+?)\s*</font>.+?\'> (.+?)</font>').findall(content)
		for href,img,eps,namevn,nameen in items:		
			name =  namevn + ' - ' + nameen
			if '01/01' in eps : #truong hop phim le o trang chu co hien thi (Tập 01/01)
				if query=='':
					v_mode='16'						
					isFolder=False
				elif query=='-':
					v_mode='12'
				else:
					name = '[PhimGiaiTri] ' + name
					v_mode='12'		
				href = phimgiaitri_vn+href+'/Tap-1.html'
				addLink(name,href, 'stream',phimgiaitri_vn+img)					
				#xshare.addir(name,url,phimgiaitri_vn+img,'fanart',v_mode='play',page=1,isFolder=False)	
			else : 
				if query=='':
					name = color['phimbo'] + name + '[/COLOR]'
					v_mode='episodes'	
				elif query=='-':
					name = color['phimbo'] + name + '[/COLOR]'
					v_mode='120'
				else:
					name = '[PhimGiaiTri] ' + name
					v_mode='120'	
				href = phimgiaitri_vn+href+'/Tap-1.html'
				xshare.addir(name,href,phimgiaitri_vn+img,'fanart',mode='episodes',page=1,isFolder=True)	
								
		#items = re.compile("<a  href='(.+?)'>(\d+)  <\/a>").findall(content) 		
		#for url,name in items:
		  #addItem('[COLOR lime]Trang tiếp theo '+name+'[/COLOR]',phimgiaitri_vn+href.replace(' ','%20'),'search_result',icon['next'])
		#except:pass
										
	elif 'chiasenhac' in url:
		content = GetUrl(url)
		items=re.compile("<a href=\"([^\"]*)\" title=\"(.*?)\"><img src=\"([^\"]+)\"").findall(content)
		#items=re.compile("<a href=\"([^\"]*)\" title=\"(.*?)\"><img src=\"([^\"]+)\"\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s*<span class=\"gen\">.*?<br /><span style=\"color: .*?\">(.*?)</span>").findall(content)
		cat = '...'
		if 'page=' not in url:url=url+"&page=1"
		for href,name,thumbnail in items:
			name=name.replace(';',' +')
			addLink(name+color['cat']+' ['+cat+'][/COLOR]',csn+href, 'stream',thumbnail)
		items=re.compile("href=\"(.+?)\" class=\"npage\">(\d+)<").findall(content)
		for href,name in items:
			if 'page='+name not in url:
				addItem(color['trangtiep']+'Trang '+name+'[/COLOR]',href.replace('&amp;','&'),'search_result',icon['next'])
	elif 'nhaccuatui' in url:
		content = GetUrl(url)
		match = re.compile("href=\"http:\/\/m.nhaccuatui.com\/video\/([^\"]*)\" title=\"([^\"]+)\"><img alt=\".+?\" src=\"(.*?)\"").findall(content)		
		for url, name, thumb in match:			
			addLink(name,nct + 'video/' + url,'stream',thumb)
		match = re.compile("href=\"([^\"]*)\" class=\"next\" titlle=\"([^\"]+)\"").findall(content)
		for url, name in match:	
			addItem(color['trangtiep']+name+'[/COLOR]',url,mode if mode=='episodes' else 'search_result',icon['next'])					

def menulist(homepath):
	try:
		mainmenu=open(homepath, 'r')  
		link=mainmenu.read()
		mainmenu.close()
		match=re.compile("<title>([^<]*)<\/title>\s*<link>([^<]+)<\/link>\s*<thumbnail>(.+?)</thumbnail>").findall(link)
		return match
	except:
		pass
	
def resolve_url(url):
	link='';subtitle = ''
	if 'xemphimso' in url:
		content = GetUrl(url)	
		url = urllib.unquote_plus(re.compile("file=(.+?)&").findall(content)[0])
	elif 'vtvplay' in url:
		content = GetUrl(url)
		url = content.replace("\"", "")
		url = url[:-5]
	elif 'vtvplus' in url:
		content = GetUrl(url)
		url = re.compile('var responseText = "(.+?)";').findall(content)[0]		
	elif 'htvonline' in url:
		content = GetUrl(url)
		url = re.compile('data-source="(.+?)"').findall(content)[0]		
		#url = re.compile('data\-source=\"([^\"]*)\"').findall(content)[0]
	elif 'hplus' in url:
		content = GetUrl(url)	
		url = re.compile('iosUrl = "(.+?)";').findall(content)[0]
	elif 'chiasenhac' in url:
		content = GetUrl(url)
		try:
		  url = re.compile("\"hd-2\".+?\"([^\"]+)\"").findall(content)[0].replace('%3A',':').replace('%2F','/').replace('%2520','%20')
		except:
		  url = re.compile("\"file\".*?\"([^\"]*)\"").findall(content)[-1].replace('%3A', ':').replace('%2F', '/').replace('%2520', '%20')		
		  #url = re.compile("\"hd-2\".+?\"([^\"]+)\"").findall(content)[-1].replace('%3A',':').replace('%2F','/').replace('%2520','%20')
	elif 'nhaccuatui' in url:
		content = GetUrl(url)
		url = re.compile("title=\".+?\" href=\"([^\"]*)\"").findall(content)[0] 
		
	elif 'f.vp9.tv' in url:
		content = GetUrl(url)
		try:
		  try:
		    url = url+re.compile('<a href="(.*?)HV.mp4"').findall(content)[0]+'HV.mp4'
		  except:
		    url = url+re.compile('<a href="(.*?)mvhd.mp4"').findall(content)[0]+'mvhd.mp4'
		except:
		  url = url+re.compile('<a href="(.*?)mv.mp4"').findall(content)[0]+'mv.mp4'
	elif 'ott.thuynga' in url:
		content = GetUrl(url)	
		url=re.compile("var iosUrl = '(.+?)'").findall(content)[0]
	elif 'phim7' in url:
		content = GetUrl(url)
		try:
		  url = 'https://redirector' + re.compile('file: "https://redirector(.+?)", label:".+?", type: "video/mp4"').findall(content)[-1]
		except:
		  url = 'plugin://plugin.video.youtube/play/?video_id=' + re.compile('file : "http://www.youtube.com/watch\?v=(.+?)&amp').findall(content)[0]		
	elif 'phimgiaitri' in url:
		xbmc.log(url)	
		arr = url.split('/')
		phimid = arr[len(arr) - 3]
		tap = arr[len(arr) - 1]
		tap2 = tap.split('-')
		tap3 = tap2[1].split('.')
		tap = tap3[0]
		url2 = 'http://120.72.85.195/phimgiaitri/mobile/service/getep3.php?phimid=' + phimid
		content = GetUrl(url2)
		content = content[3:]
		infoJson = json.loads(content)
		tapindex = int(tap) -1
		link = infoJson['ep_info'][tapindex]['link']
		link = link.replace('#','*')
		url3 ='http://120.72.85.195/phimgiaitri/mobile/service/getdireclink.php?linkpicasa=' + link
		content = GetUrl(url3)
		content = content[3:]
		linkJson = json.loads(content)
		link = linkJson['linkpi'][0]['link720'] or linkJson['linkpi'][0]['link360']
	elif 'megabox.vn' in url:
		#from resources.lib.servers import megabox;
		mgb=megabox()
		link,subtitle=mgb.getLink(url)											
	elif 'hayhaytv' in url:
		hh=hayhayvn()
		link,subtitle=hh.getLink(url)								
	elif 'hdviet.com' in url:		
		if os.path.isfile(xshare.joinpath(datapath,'hdviet.cookie')):os.remove(xshare.joinpath(datapath,'hdviet.cookie'))
			
		hdv=hdviet()
		url = url.split('|')[1]
		link,subtitle=hdv.getResolvedUrl(url)#;print link,sub		
		#print 'link: '+link,subtitle
	elif 'phimmoi.net' in url:pass
	elif 'hdonline.vn' in url:
		link,subtitle = getlink.get_hdonline(url)
	elif 'fshare.vn' in url:
		try:
			link = getlink.get(url)
		except:
			fs=fshare(myaddon.getSetting('usernamef'),myaddon.getSetting('passwordf'))
			if fs.logged is None:return 'fail'
			for loop in range(6):
				if loop>0:xshare.mess(u'Get link lần thứ %d'%(loop+1),'fshare.vn');xbmc.sleep(sleep);sleep+=1000
				direct_link=fs.get_maxlink(url)
				if direct_link=='fail':break
				elif direct_link:break
			fs.logout()
			if not direct_link:xshare.mess('Sorry! Potay.com','fshare.vn');return 'fail'
			elif direct_link in 'notfound-fail':return 'fail'
			else:link=direct_link		
	else:
		link = url		
		
	#print link
		
	if link is None or len(link) == 0:
		notify('Lỗi không lấy được link phim.')
					
	item=xbmcgui.ListItem(path=link)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)	
	
	
	if len(subtitle) == 0 and myaddon.getSetting('advertisement') == 'false':
		subtitle=decode("QC", "ubfFs4tygKayscWys7jEq8Czf6bAsICbk5CUcsK4srG4prKyf7bDtw==")	
	if len(subtitle) > 0:	
		subtitlePath = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('path')).decode("utf-8")
		subfile = xbmc.translatePath(os.path.join(subtitlePath, "temp.sub"))
		try:
			if os.path.exists(subfile):
				os.remove(subfile)
			f = urllib2.urlopen(subtitle)
			with open(subfile, "wb") as code:
				code.write(f.read())
				
			xbmc.sleep(3000)
			xbmc.Player().setSubtitles(subfile)
		except:
			notify(u'Không tải được phụ đề phim.');
		
	return

def GetUrl(url):
    try:
		req=urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)')
		response=urllib2.urlopen(req)
		link=response.read()
		response.close()  
		return link
    except:pass
    	
def addLink(name,url,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&img="+urllib.quote_plus(iconimage)
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name})
	liz.setProperty("IsPlayable","true")
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz, isFolder=False)
	return ok
	
def addItem(name,url,mode,iconimage,isFolder=True):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&img="+urllib.quote_plus(iconimage)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	if ('www.youtube.com/user/' in url) or ('www.youtube.com/channel/' in url):
		u = 'plugin://plugin.video.youtube/%s/%s/' % (url.split( '/' )[-2], url.split( '/' )[-1])
		ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
		return ok		
	if ('plugin://plugin' in url):
		u = url
		ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
		return ok
	if not isFolder:
		liz.setProperty('IsPlayable', 'true')			
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
	return ok
	
def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
	return param
### ------------
#xbmcplugin.setContent(int(sys.argv[1]), 'movies');
params=get_params();mode=0;page=0;temp=[]
homnay=datetime.date.today().strftime("%d/%m/%Y");url=name=fanart=img=date=query=end=''

try:url=urllib.unquote_plus(params["url"])
except:pass
try:name=urllib.unquote_plus(params["name"])
except:pass
try:img=urllib.unquote_plus(params["img"])
except:pass
try:fanart=urllib.unquote_plus(params["fanart"])
except:pass
try:mode=str(params["mode"])
except:pass
try:page=int(params["page"])
except:pass
try:query=urllib.unquote_plus(params["query"])
except:pass#urllib.unquote

### ------------
print "Main---------- Mode: "+str(mode),"URL: "+str(url),"Name: "+str(name),"query: "+str(query),"page: "+str(page),"img: "+str(img)
if not mode:Home()
elif mode == 'index':Index(url,name)
elif mode == 'indexlocal':IndexLocal(url)
elif mode == 'menu_group':Menu_Group(url)
elif mode == 'category':Category(url, mode, name, query)
elif mode == 'episodes':episodes(url, name)
elif mode == 'local':Local(name,url,img,fanart,mode,query)
elif mode == 'remote':Remote(name,url,img,mode,page,query)
elif mode == 'search_result':Search_Result(url, mode, query)
elif mode == 'search':Search(url)	
elif mode=='stream':resolve_url(url)
elif 'serverlist' in mode:ServerList(name, url, mode, page, query, img)	

xbmcplugin.endOfDirectory(int(sys.argv[1]))