__author__ = 'phuoclv'
#coding=utf-8
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,urllib,urllib2,re,os,unicodedata,datetime,random,json
import base64
#import xbmc,xbmcaddon,xbmcplugin,xbmcgui,sys,urllib,urllib2,re,os,codecs,unicodedata,base64
#import cookielib,os,string,cookielib,StringIO,gzip

home = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('path')).decode("utf-8")
sys.path.append(os.path.join(home,'resources','lib'));from urlfetch import get,post;import xshare;import hdonline;import hdviet;import hayhaytv
from config import hayhaytv_vn, hdviet_com, dangcaphd_com, hdonline_vn, megabox_vn, vuahd_tv, phimmoi_net

#addonID = xbmcaddon.Addon('plugin.video.cantobumedia')
myaddon=xbmcaddon.Addon()

logos = xbmc.translatePath(os.path.join(home,"logos\\"))
dataPath = xbmc.translatePath(os.path.join(home, 'resources'))
csn = 'http://chiasenhac.com/'
csn_logo ='http://chiasenhac.com/images/logo_csn_300x300.jpg'
hdcaphe = 'http://phim.hdcaphe.com/'
megaboxvn = 'http://phim.megabox.vn/'
pgt = 'http://phimgiaitri.vn/'
vp9 = 'http://f.vp9.tv/music/'
tvreplay = 'http://113.160.49.39/tvcatchup/'
woim = 'http://www.woim.net/'
### -----------------
datapath=xbmc.translatePath(os.path.join(xbmc.translatePath(myaddon.getAddonInfo('profile')),'data'))
iconpath=xbmc.translatePath(os.path.join(xbmc.translatePath(myaddon.getAddonInfo('profile')),'icon'))

search_file=os.path.join(datapath,"search.xml");data_path=os.path.join(home,'resources','data')

myfolder= myaddon.getSetting('thumuccucbo').decode('utf-8');copyxml=myaddon.getSetting('copyxml')
if not os.path.exists(myfolder):myfolder=os.path.join(datapath,'myfolder')
subsfolder=os.path.join(myfolder,'subs');tempfolder=os.path.join(myfolder,'temp')
rows=int(myaddon.getSetting('sodonghienthi')) #Số dòng hiển thị cho 1 trang

#media_ext=['aif','iff','m3u','m4a','mid','mp3','mpa','ra','wav','wma','3g2','3gp','asf','asx','avi','flv','mov','mp4','mpg','mkv','m4v','rm','swf','vob','wmv','bin','cue','dmg','iso','mdf','toast','vcd','ts','flac']

www={'hdonline':'[hdonline.vn]','vuahd':'[vuahd.tv]','hdviet':'[http://movies.hdviet.com/]','hayhaytv':'[http://www.hayhaytv.vn/]','dangcaphd':'[http://dangcaphd.com/]','megabox':'[http://phim.megabox.vn/]','phimmoi':'[vuahd.tv]','hdcaphe':'[http://phim.hdcaphe.com/]','phimgiaitri':'[http://phimgiaitri.vn/]'}
color={'trangtiep':'[COLOR lime]','cat':'[COLOR green]','search':'[COLOR red]','phimbo':'[COLOR tomato]','phimle':'[COLOR yellow]'};icon={}
for item in ['hdonline', 'vuahd', 'hdviet', 'hayhaytv', 'dangcaphd', 'megabox', 'phimmoi', 'hdcaphe', 'phimgiaitri', 'next', 'icon']:
	icon.setdefault(item,os.path.join(logos,'%s.png'%item))
#hd = {'User-Agent' : 'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'}

danhmucphim=myaddon.getSetting('danhmucphim')
hdonline_view=myaddon.getSetting('hdonline_view')
vuahd_view=myaddon.getSetting('vuahd_view')
hdviet_view=myaddon.getSetting('hdviet_view')
hayhaytv_view=myaddon.getSetting('hayhaytv_view')
dangcaphd_view=myaddon.getSetting('dangcaphd_view')
megabox_view=myaddon.getSetting('megabox_view')
phimmoi_view=myaddon.getSetting('phimmoi_view')
hdcaphe_view=myaddon.getSetting('hdcaphe_view')
phimgiaitri_view=myaddon.getSetting('phimgiaitri_view')

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

def setViewMode(view_mode = '2'):
	skin_used = xbmc.getSkinDir()
	if skin_used == 'skin.xeebo':
		xbmc.executebuiltin('Container.SetViewMode(52)')
	else:
		if not view_mode == "0":
			try:
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
			except:
				addon_log("SetViewMode Failed: "+view_mode)
				addon_log("Skin: "+xbmc.getSkinDir())
	
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
	
def fixString(string):
	string = string.replace('&amp;','&').replace("&#39;","'")
	return string
	
def fixSearch(string):
	string = string.replace('+','-').replace(' ','-')	
	string = string.replace('?','').replace('!','').replace('.','').replace(':','').replace('"','')
	string = string.replace('&amp;','and').replace('&','and').replace("&#39;","")
	i = 1
	while i < 10:
		string = string.replace('(Season '+str(i)+'','Season '+str(i))
		i += 1  # This is the same as i = i + 1	
	string = string.replace('- Season','Season')	# MegaBox	
	string = string.strip()
	return string

def fixSearchss(string):
	string = string.replace('+','-').replace(' ','-')	
	string = string.replace('?','').replace('!','').replace('.','').replace(':','')	
	string = string.replace('&amp;','and').replace('&','and').replace("&#39;","")
	string = string.upper()
	string = string.strip()
	return string
###-----------------
def Home():
	content = Get_Url(DecryptData(homeurl))
	match=re.compile("<title>([^<]*)<\/title>\s*<link>([^<]+)<\/link>\s*<thumbnail>(.+?)</thumbnail>").findall(content)
	for title,url,thumbnail in match:
		title = '[B]'+title+'[/B]'
		if 'MenuMusic' in url:
			url = csn
			addDir(title,url,'category',thumbnail)
		elif 'MYPLAYLIST' in url or 'tvcatchup' in url:
			pass
		elif 'Setting' in url:			
			addLink(title,url,'menu_group',thumbnail)		
		else:
			addDir(title,url,'menu_group',thumbnail)		
		
def Menu_Group(url):
	if 'Setting' in url:
		xbmcaddon.Addon().openSettings()
		return
	elif 'MenuTivi' in url:
		content = Get_Url(url)
		match=re.compile("<title>([^<]*)<\/title>\s*<link>([^<]+)<\/link>\s*<thumbnail>(.+?)</thumbnail>").findall(content)
		for title,url,thumbnail in match:
			addDir(title,url,'indexgroup',thumbnail)
		setViewMode('3')
	elif 'MenuShows' in url:
		content = Get_Url(url)
		match=re.compile("<title>([^<]*)<\/title>\s*<link>([^<]+)<\/link>\s*<thumbnail>(.+?)</thumbnail>").findall(content)
		for title,url,thumbnail in match:
			if 'xml' in url:
				addDir(title,url,'index_group',thumbnail)
			elif 'm3u' in url:
				addDir(title,url,'get_m3u',thumbnail)		
		setViewMode('3')
	elif 'MenuMusic' in url:
		content = Get_Url(url)
		match=re.compile("<title>([^<]*)<\/title>\s*<link>([^<]+)<\/link>\s*<thumbnail>(.+?)</thumbnail>").findall(content)
		for title,url,thumbnail in match:
			if 'LIVESHOWS' in url:
				addDir(title,url,'index_group',thumbnail)
			elif 'm3u' in url:
				addDir(title,url,'get_m3u',thumbnail)
			else:
				addDir(title,url,'category',thumbnail)
		setViewMode('2')
	elif 'MenuMovie' in url:
		categoryroot(url)
	elif 'MenuTube' in url:
		content = Get_Url(url)
		names = re.compile('<name>(.+?)</name>\s*<thumbnail>(.+?)</thumbnail>').findall(content)
		for name,thumb in names:
			addDir(name, url+"?n="+name, 'index', thumb)		
		setViewMode('3')
	elif 'SEARCH' in url:
		#addDir('Tìm Video Nhạc','TimVideo','search',logos+'menu-music.png')
		#addDir('Tìm Album Nhạc Không Lời','TimAlbum','search',logos+'menu-music.png')	  
		servers = ['HDOnline', 'VuaHD', 'HDViet', 'HayHayTV', 'DangCapHD', 'MegaBox', 'PhimMoi', 'PhimGiaiTri']
		for server in servers:
			addDir(server,server,'search',icon[server.lower()])
		setViewMode('2')

def categoryroot(url):
	if danhmucphim == 'HDOnline' or 'HDOnline' in url:
		link = hdonline.GetContent("http://hdonline.vn/")
		link = ''.join(link.splitlines()).replace('\'','"')
		try:
			link =link.encode("UTF-8")
		except: pass
		vidcontent=re.compile('<nav class="tn-gnav">(.+?)</nav> ').findall(link)
		vidcontentlist=[]
		if(len(vidcontent)>0):
			addDir(color['search']+'Tìm kiếm trên HDOnline[/COLOR]','HDOnline-','search',icon['hdonline'])
			vidcontentlist=re.compile('<li>(.+?)</div>\s*</div>\s*</li>').findall(vidcontent[0])
			for vidcontent in vidcontentlist:
				mainpart=re.compile('<a href="(.+?)"> <span class="tnico-(.+?)"></span>(.+?)</a>').findall(vidcontent)
				mainname=mainpart[0][2]
				href=mainpart[0][0]
				if 'hdonline.vn' not in href:href='http://hdonline.vn'+mainpart[0][0]
				vidlist=re.compile('<li><a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a></li>').findall(vidcontent)
				
				if 'TIN' in mainname : mainname = "MORE";href='http://hdonline.vn/danh-sach/phim-moi.html'
				xshare.addir('[B]'+mainname+'[/B]',href,img,'fanart',mode='category',page=0,query='Index',isFolder=True)	
				for vurl,vname in vidlist:
					#vname = vname.replace('Phim ','')
					if 'Mỹ' in vname : vname = 'Âu/	' + vname
					if mainname == "MORE" : vurl = 'http://hdonline.vn'+vurl
					if(vurl.find("javascript:") ==-1 and len(vurl) > 3):
						xshare.addir("    "+vname,vurl,img,'fanart',mode='category',page=0,query='Index',isFolder=True)	
			
		#vidcontent=re.compile('<nav class="tn-gnav">(.+?)</nav> ').findall(link)		
		#vidcontent=re.compile('<span class="tnico-news"></span> (.+?) </a>').findall(link)						
		#items2=re.findall('<a href="(.+?)" .?title=".+?">(.+?)</a>',vidcontent[0])	
		#for href,name in items2:
			#xshare.addir(name,href,img,'fanart',mode=10,page=0,query='Index',isFolder=True)		

	elif danhmucphim == 'HDViet' or 'HDViet' in url:
		home='http://movies.hdviet.com/';direct_link='https://api-v2.hdviet.com/movie/play?movieid=%s'
				
		addDir(color['search']+'Tìm kiếm trên HDViet[/COLOR]','HDViet-','search',icon['hdviet'])
		
		xshare.addir('[B]PHIM LẺ[/B]',hdviet_com+'phim-le.html',img,fanart='',mode='category',page=1,query='',isFolder=True)
		body=xshare.make_request('http://movies.hdviet.com/phim-le.html')
		items=re.findall('<a href="(.+?)" .?menuid="(.+?)" .?title=".+?" >(.+?)</a>',body)
		for href,id,name in items:
			xshare.addir('    '+name,href,img,fanart='',mode='category',page=1,query=id,isFolder=True)		
		xshare.addir('[B]PHIM BỘ[/B]',hdviet_com+'phim-bo.html',img,fanart='',mode='category',page=1,query='',isFolder=True)
		body=xshare.make_request('http://movies.hdviet.com/phim-bo.html')
		items=re.findall('<a href="(.+?)" menuid="(.+?)" title=".+?">(.+?)</a>',body)
		items+=re.findall('<a class="childparentlib" menuid="(.+?)" href="(.+?)" title=".+?">(\s.*.+?)</a>',body)
		for href,id,name in items:
			if 'au-my' in href or 'tai-lieu' in href:name='Âu Mỹ %s'%name.strip()
			elif 'hong-kong' in href:name='Hồng Kông %s'%name.strip()
			elif 'trung-quoc' in href:name='Trung Quốc %s'%name.strip()
			else:name=name.strip()
			if href in '38-39-40':temp=href;href=id;id=temp
			xshare.addir('    '+name,href,img,fanart='',mode='category',page=1,query=id,isFolder=True)
		
		addLink('[B]THỂ LOẠI PHIM[/B]',"",0,img)
		for href,name in re.findall('<p><a href="(.+?)" title=".+?">(.+?)</a></p>',xshare.make_request(home)):
			xshare.addir('    '+name,href,img,fanart='',mode='category',page=1,query=id,isFolder=True)
			
		addLink('[B]THẾ GIỚI SAO[/B]',"",0,img)
		for href,name in re.findall('<li><a href="(.+?)" title=".+?">(.+?)</a></li>',xshare.make_request(home)):
			if 'Tất cả' not in name:
				xshare.addir('    '+name.replace('&nbsp;',''),href,img,fanart='',mode='category',page=1,query=id,isFolder=True)
	elif danhmucphim == 'HayHayTV' or 'HayHayTV' in url:
		addDir(color['search']+'Tìm kiếm trên HayHayTV[/COLOR]','HayHayTV-','search',icon['hayhaytv'])
		ajax=hayhaytv_vn+'ajax_hayhaytv.php'
		body=xshare.make_request(hayhaytv_vn)					
		for href,name in re.findall('menu_fa_text.+?" href="(.+?)".*>(.+?)</a>',body):
			url = href
			if name in 'PHIM LẺ-PHIM BỘ-SHOWS':
				name='[B]'+name+'[/B]'
				xshare.addir(name,href,img,fanart='',mode='category',page=1,query='M2',isFolder=True)
																			
				body=xshare.make_request(hayhaytv_vn+'/tim-kiem');pattern='http.+/\w{1,6}-'
				body=body[body.find(url):];body=body[:body.find('mar-r20')]
				for href,name in re.findall('href="(.+?)".*?>(.+?)</a></li>',body):
					xshare.addir('    '+name,href,img,fanart='',mode='category',page=1,query='M2',isFolder=True)
	elif danhmucphim == 'DangCapHD' or 'DangCapHD' in url:
		addDir(color['search']+'Tìm kiếm trên DangCapHD[/COLOR]','DangCapHD-','search',icon['dangcaphd'])
		body=xshare.make_request(dangcaphd_com)		
		for name in re.findall('</i>(.+?)<span class="caret">',body):
			name='[B]'+name.strip()+'[/B]'
			xshare.addir(name,dangcaphd_com,icon['dangcaphd'],mode='category',query='DC1',isFolder=True)
			
			#body=xshare.make_request(dangcaphd_com)
			if 'the loai' in  xshare.no_accent(name).lower():
				for href,name in re.findall('<a href="(http://dangcaphd.com/cat.+?)" title="(.+?)">',body):
					#name='[B]'+name.strip()+'[/B]'
					xshare.addir('    '+name.strip(),href,icon['dangcaphd'],mode='category',query='DC2',isFolder=True)
			if 'quoc gia' in  xshare.no_accent(name).lower():
				for href,name in re.findall('<a href="(http://dangcaphd.com/country.+?)" title="(.+?)">',body):
					xshare.addir('    '+name.strip(),href,icon['dangcaphd'],mode='category',query='DC2',isFolder=True)
			
		for href,name in re.findall('<a href="(.+?)"><i class=".+?"></i>(.+?)</a>',body):
			if 'channel.html' not in href and 'product.html' not in href:
				name='[B]'+name.strip()+'[/B]'
				xshare.addir(name,href,icon['dangcaphd'],mode='category',query='DC2',isFolder=True)
					
		setViewMode('2')
	elif danhmucphim == 'Tất cả':
		#servers = ['HDOnline', 'VuaHD', 'HDViet', 'HayHayTV', 'DangCapHD', 'MegaBox', 'PhimMoi', 'PhimGiaiTri']
		servers = ['HDOnline', 'HDViet', 'HayHayTV', 'DangCapHD']
		for server in servers:
			name='[B]'+server+'[/B]'				
			xshare.addir(name,'MenuMovie|'+server,icon[server.lower()],mode='menu_group',query='',isFolder=True)
		setViewMode('2')				
		
def category(url):
	if 'hdonline.vn' in url:
		link = hdonline.GetContent(url)
		link = ''.join(link.splitlines()).replace('\'','"')
		try:
			link =link.encode("UTF-8")
		except: pass
		#vidcontentlist=re.compile('<ul id="cat_tatca"(.+?)</section>').findall(link)
		#if(len(vidcontentlist)>0):
		movielist=re.compile('<li>\s*<div class="tn-bxitem">(.+?)</li>').findall(link)
		for idx in range(len(movielist)):
			vcontent = movielist[idx]				
			items=re.compile('<a href="(.+?)"(.+?)<img src="(.+?)".+?<p class="name-vi">(.+?)</p>\s*<p class="name-en">(.+?)</p>').findall(vcontent)										
			for url, episodes, img, nameen, namevn in items :
				name =  namevn + ' - ' + nameen				
				if 'episodes' in episodes :	# Phim Bộ
					mode='120'
					name=color['phimbo']+name+'[/COLOR]'
				else :mode='12'
				
				if danhmucphim != 'Tất cả':
					xshare.addir(name,url,img,fanart='fanart',mode=mode,page=0,query=nameen,isFolder=True)
				else:
					if mode == '12' :
						fid = xshare.xshare_group(re.search('-(\d{1,4}).html',url),1)
						url = '/frontend/episode/loadxmlconfigorder?ep=1&fid='+str(fid)
						url = 'http://hdonline.vn' + url
						#url = hdonline_vn + 'http:%2F%2Fhdonline.vn' + url.replace('/', '%2F').replace('?', '%3F').replace('=', '%3D').replace('&', '%26')
						xshare.addir(name,url,img,'fanart',mode='16',page=1,query='',isFolder=False)
					else :
						home='http://m.hdonline.vn'
						xshare.addir(name,home+url,img,'fanart',mode='episodes',page=1,query='',isFolder=True)
												
		pagecontent=re.compile('<ul class="pagination">(.+?)</ul>').findall(link)
		if(len(pagecontent)>0):
			pagelist=re.compile('<li><a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a></li>').findall(pagecontent[0])
			for vurl,vname in pagelist:
				if 'Trang' not in vname : vname = 'Trang ' + vname
				addDir(vname,vurl,'category',"")	
	elif 'hdviet.com' in url:
		body=xshare.make_request(url);body=body[body.find('box-movie-list'):body.find('h2-ttl cf')];
		
		pattern='<a href="(.{,200})"><img src="(.+?)"(.+?)"h2-ttl3">(.+?)<span>(.+?)</span>(.*?)<a'
		links=re.findall(pattern,body)
		for link,img,temp,ttl3,title,cap in links:
			strNameEn, name = strVnEn(title, ttl3.replace('&nbsp;',''))
			caps=''
			if 'icon-SD' in cap:caps+='[COLOR gold]SD[/COLOR]'
			if 'icon-720' in cap:caps+='[COLOR gold]HD[/COLOR]720'
			if 'icon-1080' in cap:caps+='[COLOR gold]HD[/COLOR]1080'
			if 'icon-TM' in cap:caps+='[COLOR green]TM[/COLOR]'
			if '>18+<' in cap:caps+='[COLOR red]18+[/COLOR]'
			isFolder=xshare.xshare_group(re.search('"labelchap2">(\d{1,3})</span>',temp),1)
			link=xshare.xshare_group(re.search('id="tooltip(\d{,10})"',temp),1).strip()

			if not isFolder:mode='12'
			#elif isFolder=='1':hdviet(title,link,img,mode='22',page=1,query='folder',isFolder=True)
			else:
				mode='120'
				name = color['phimbo']+name+'[/COLOR]'

			if danhmucphim != 'Tất cả':
				xshare.addir(name,link,img,'fanart',mode=mode,page=1,query=strNameEn, isFolder=True)
			else:
				if mode == '12' :
					xshare.addir(name,link,img,'fanart',mode='22',page=1,query='hdvietplay',isFolder=False)
				else :
					xshare.addir(name,hdviet_com,img,'fanart',mode='episodes',page=1,query=link,isFolder=True)							
			
		pages=re.findall('<li class=""><a href="(.+?)">(.+?)</a></li>',body[body.find('class="active"'):])
		if pages:
			pagenext=pages[0][1];pageend=pages[len(pages)-1][1]
			name='%sTrang tiếp theo: trang %s/%s[/COLOR]'%(color['trangtiep'],pagenext,pageend)
			addDir(name,pages[0][0],'category',"")
			#xshare.addir(name,pages[0][0],img,fanart='fanart',mode='search_result',page=1,query='hdvietplay',isFolder=True)			
	elif 'hayhaytv.vn' in url:
		if '/shows' in url: Search_Result(url, query='')
		else:
			#body=xshare.make_request(url)		
			body=xshare.make_post(re.sub('page=\d{1,3}','page=%d'%page,url)).body
			pattern='tooltip="(.+?)" href="(.+?)">\s.*"(http://img.+?)".*\s.*color">(.*?)<.*\s.*>(.*?)</span>'
			items=re.findall(pattern,body)
			ids=dict((re.findall('id="(sticky\d{1,3})".{,250}Số tập[\D]{,30}(\d{1,4})',body,re.DOTALL)))
			
			for stic,href,img,name_e,name_v in items:
				name=name_v+' - '+name_e if name_v else name_e
				if re.search('Tap-\d{1,3}',href):			
				#if ids.has_key(stic) and ids[stic].strip()>'1':#? in ids.values()
					mode='120'
					name=color['phimbo']+name+'[/COLOR]'
				else:mode='12'
						
				if danhmucphim != 'Tất cả':
					xshare.addir(name,href,img,'fanart',mode=mode,page=1,query=name_e[:-7], isFolder=True)
				else:
					if mode == '12' or 'xem-show' in href:
						xshare.addir(name,href,img,'fanart',mode='23',page=1,query='play',isFolder=False)
					else :
						xshare.addir(name,href,img,'fanart',mode='episodes',page=1,query='',isFolder=True)														
				
			body=body[body.find('javascript:slideTogglePage1()'):body.find('data-tooltip="sticky')]						
			items=re.findall('<a href=\'(.+?)\' onclick=.*?>(.+?)</a>',body)
			for href, name in items:				
				name = color['trangtiep'] + 'Trang ' + name + '[/COLOR]'
				addDir(name,href,'category',"")
		setViewMode('3')
	elif 'dangcaphd.com' in url:
		Search_Result(url, query='-')
	elif 'ott.thuynga' in url:
		match=menulist(dataPath+'/data/category.xml')
		for title,url,thumbnail in match:	  
			if 'ott.thuynga' in url:
				addDir(title,url,'episodes',thumbnail)
			else:pass				
	elif 'chiasenhac' in url:
		content=Get_Url(url)
		addDir(color['search']+'Tìm kiếm[/COLOR]','TimVideo','search',csn_logo)
		match=re.compile("<a href=\"hd(.+?)\" title=\"([^\"]*)\"").findall(content)[1:8]
		for url,name in match:
			addDir(name,csn+'hd'+url,'episodes',csn_logo)

def episodes(url):
	if 'hdonline.vn' in url :
		items=re.findall('<a href="(.+?)" .+?"><span>(.+?)</span></a>',xshare.make_request(url));
		i=0
		for url, eps in items:
			i=i+1
			#url = url.replace('http://m.hdonline.vn/','').replace('tap-'+str(i)+'-', '')
			fid = xshare.xshare_group(re.search('-(\d{1,4}).html',url),1)
			url = '/frontend/episode/loadxmlconfigorder?ep=1&fid='+str(fid)
			url = 'http://hdonline.vn' + url
			#url = hdonline_vn + 'http:%2F%2Fhdonline.vn' + url.replace('/', '%2F').replace('?', '%3f').replace('=', '%3D')			
			xshare.addir('Tập '+str(i),url,img,'fanart',mode='16',isFolder=False)
	elif 'vuahd.tv' in url :
		items=re.findall('<a href="#" class="btn-1 btnUpgrade">Xem (.+?)</a>',xshare.make_request(url));temp=[]
		for eps in items:	
			if eps not in temp:
				temp.append(eps);title=eps+'-'+name;tap=xshare.xshare_group(re.search('(\d{1,3})',eps),1)
				if tap:tap=format(int(tap),'02d')
				else:continue
				url = url.replace('tv-series/','')+'-%s'%tap
				url = url+'/watch'
				url = vuahd_tv + url.replace('/', '%2F')			
				xshare.addir(title,url,img,'fanart',mode='16',isFolder=False)		
	elif 'hdviet.com' in url :
		url = query		
		print url
		href='http://movies.hdviet.com/lay-danh-sach-tap-phim.html?id=%s'%url
		try:
			response=xshare.make_request(href,resp='j')
			#if not response:return
			for eps in range(1,int(response["Sequence"])+1):
				title='Tập %s/%s-%s'%(format(eps,'0%dd'%len(response['Episode'])),str(response['Episode']),re.sub('\[.?COLOR.{,12}\]','',name))
				xshare.addir(title,'%s_e%d'%(url,eps),img,fanart='',mode='22',page=1,query='hdvietplay')
		except:pass
	elif 'hayhaytv.vn' in url :			
		#Đoạn code này sử dụng mã bảo mật từ add-on HayHayTV.vn
			
		if 'xem-show' in url:pattern='href="(.+?)".*src=".+?"\D*(\d{1,3})<'
		else:pattern='<a class=".*?" href="(.+?)"\D*(\d{1,3})<'
		resp=xshare.make_request(url,resp='o');body=resp.body if resp.status==200 else xshare.make_request(resp.headers['location'])
		items=re.findall(pattern,body)
		if not page:
			id=xshare.xshare_group(re.search('FILM_ID\D{3,7}(\d{3,6})',body),1)	
			print id
			url='https://www.fshare.vn/folder/5VNFUPO32P6F'
			hd=xshare.xshare_group(re.search('<title>.*xx(.+?)xx.*</title>',xshare.make_request(url)),1).split('-')
			#['Authorization', 'Basic', 'YXBpaGF5OmFzb2tzYXBySkRMSVVSbzJ1MDF1cndqcQ==']
			data='device=xshare&secure_token=1.0&request='+urllib.quote('{"movie_id":"%s"}'%id)
			response=xshare.make_post('http://api.hayhaytv.vn/movie/movie_detail',{hd[0]:'%s %s'%(hd[1],hd[2])},data)
			#print response.json['data']		
			try:json=response.json['data']
			except:json={}						
			if json:page=json['total_episode'].encode('utf-8')
		for href,epi in items:
			xshare.addir('Tập %s/%s-%s'%(epi,page,re.sub('\[.?COLOR.{,12}\]','',name)),href,img,fanart='',mode=23,page=1,query='play')						
	elif 'phimmoi.net' in url :	
		body=xshare.make_request(url+'xem-phim.html');body=body[body.find('data-servername'):body.find('/List tập phim')]
		colo=['[COLOR blue]','[COLOR green]'];numb=0
		while body:
			temp=body.find('data-serverid');numb+=1
			if temp>0:content=body[:temp];body=body[temp+10:]
			else:content=body;body=''
			temp=re.search('data-servername=".+?" data-language="(.+?)"',content)
			if temp:
				temp='S%d-%s[/COLOR] '%(numb,'sub' if temp.group(1)=='subtitle' else 'TM')
				temp+=re.sub('\[.?COLOR.{,12}\]|\(Lượt xem.*?\)|TM','',name)
			else:temp='[/COLOR]'+re.sub('\[.?COLOR.{,12}\]|\(Lượt xem.*?\)|TM','',name)
			
			i = 0
			for href,title in re.findall('href="(.+?)">(\d{1,3}).{,10}</a>',content,re.DOTALL):
				i=i+1
				title=colo[numb%2]+'Tập '+title.strip()+' '+temp				
				href = phimmoi_net + 'http:%2F%2Fphimmoi.net%2F' + href.replace('/', '%2F')
				xshare.addir(title,href,img,'fanart',mode='16',isFolder=False)
	elif 'megabox.vn' in url :	
		content = Get_Url(url)
		match = re.compile("href='(.+?)' >(\d+)<").findall(content)
		for url, title in match:
			url = megabox_vn + url.replace('/', '%2F')
			xshare.addir('Tập ' + title,url,img,'fanart',mode='16',isFolder=False)
	elif 'hdcaphe.com' in url :				
		name = '[UPPERCASE]' +url.replace('http://phim.hdcaphe.com/','').replace('video/movies/','').replace('-',' ').replace('/play/clip_',' - Tập ').replace('.html','')+ '[/UPPERCASE]'
		add_Link(name,url,img)  

		content = Get_Url(url)
		match = re.compile("<a style=\"margin-left:10px\" href=\"(.+?)\"  >(\d+)<\/a>").findall(content)
		for url,title in match:
			#title=title.split('.')[-1]
			add_Link('[UPPERCASE]' +url.replace('video/movies/','').replace('-',' ').replace('/play/clip_',' - Tập ').replace('.html','')+ '[/UPPERCASE]',hdcaphe + url,img)
	elif 'phimgiaitri.vn' in url :
		add_Link('Tập 1', url, img)
		
		content = Get_Url(url)
		match = re.compile('<a href="(.+?)" page=(.+?)>').findall(content)
		for url,title in match:		
			add_Link('Tập ' + title, url, img)
	elif 'youtube' in url:
		add_Link(name, url, thumbnail)
	elif 'chiasenhac' in url:
		content = Get_Url(url)
		items=re.compile("<a href=\"([^\"]*)\" title=\"(.*?)\"><img src=\"([^\"]+)\"\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s*<span style=\"color: .*?\">(.*?)</span>").findall(content)
		for url,name,thumbnail,cat in items:
			add_Link(name+color['cat']+' ['+cat+'][/COLOR]',csn+url,thumbnail)
		items=re.compile("<a href=\"hd\/video\/([a-z]-video\/new[0-9]+).html\" class=\"npage\">(\d+)<\/a>").findall(content)
		for url,name in items:
			addDir('[COLOR lime]Mới Chia Sẻ - Trang '+name+'[/COLOR]',csn+'hd/video/'+url+'.html','episodes',icon['next'])
		items=re.compile("<a href=\"hd\/video\/([a-z]-video\/down[0-9]+).html\" class=\"npage\">(\d+)<\/a>").findall(content)
		for url,name in items:
			addDir('[COLOR red]Download mới nhất - Trang '+name+'[/COLOR]',csn+'hd/video/'+url+'.html','episodes',icon['next'])			
			
def ServerList(name, url, mode, query):	
	search_string = fixSearch(query)
		
	name='['+danhmucphim+'] '+name
	if danhmucphim == 'HDOnline' and hdonline_view == 'true':
		if mode == '12' :
			fid = xshare.xshare_group(re.search('-(\d{1,4}).html',url),1)
			url = '/frontend/episode/loadxmlconfigorder?ep=1&fid='+str(fid)
			url = 'http://hdonline.vn' + url
			#url = hdonline_vn + 'http:%2F%2Fhdonline.vn' + url.replace('/', '%2F').replace('?', '%3f').replace('=', '%3D')
			xshare.addir(name,url,img,'fanart',mode='16',page=1,query='play',isFolder=False)
		else :
			home='http://m.hdonline.vn'
			xshare.addir(name,home+url,img,'fanart',mode='episodes',page=1,query='eps',isFolder=True)
	elif danhmucphim == 'HDViet' and hdviet_view == 'true':
		if mode == '12' :
			xshare.addir(name,url,img,'fanart',mode='22',page=1,query='hdvietplay',isFolder=False)
		else :
			xshare.addir(name,hdviet_com,img,'fanart',mode='episodes',page=1,query=url,isFolder=True)
	elif danhmucphim == 'HayHayTV' and hayhaytv_view == 'true':
		if mode == '12' :
			xshare.addir(name,url,img,'fanart',mode='23',page=1,query='play',isFolder=False)
		else :
			xshare.addir(name,url,img,'fanart',mode='episodes',page=page,query=query,isFolder=True)			
	elif danhmucphim == 'DangCapHD' and dangcaphd_view == 'true':
		if mode == '12' :
			xshare.addir(name,url,img,'fanart',mode='18',page=1,query='DCP',isFolder=False)
		else :
			xshare.addir(name,url,img,'fanart',mode='18',page=page,query='DC3',isFolder=True)			
						
	if danhmucphim <> 'HDOnline' and hdonline_view == 'true':
		url = 'http://hdonline.vn/tim-kiem/'+search_string+'.html'      					
		Search_Result(url, query)
			
	if danhmucphim <> 'VuaHD' and vuahd_view == 'true':
		url='http://vuahd.tv/movies/q/%s'%search_string
		Search_Result(url, query)

	if danhmucphim <> 'HDViet' and hdviet_view == 'true':
		url='http://movies.hdviet.com/tim-kiem.html?keyword=%s'%search_string
		Search_Result(url, query)

	if danhmucphim <> 'HayHayTV' and hayhaytv_view == 'true':
		url=hayhaytv_vn+'tim-kiem/%s/trang-1'%search_string
		Search_Result(url, query)

	if danhmucphim <> 'DangCapHD' and dangcaphd_view == 'true':
		url='http://dangcaphd.com/movie/search.html?key=%s&search_movie=1'%search_string
		Search_Result(url, query)
	
	if danhmucphim <> 'Megabox' and megabox_view == 'true':
		url='http://phim.megabox.vn/search/index?keyword=' + search_string#+'/phim-le'
		Search_Result(url, query)
	
	if danhmucphim <> 'PhimMoi' and phimmoi_view == 'true':
		url='http://www.phimmoi.net/tim-kiem/%s/'%search_string
		Search_Result(url, query)
	
	if danhmucphim <> 'HDCaphe' and hdcaphe_view == 'true':
		url = hdcaphe + 'search-result.html?keywords=' + search_string
		Search_Result(url, query)	
	
	if danhmucphim <> 'PhimGiaiTri' and phimgiaitri_view == 'true':
		url = pgt+'result.php?type=search&keywords='+search_string      
		try:
			Search_Result(url, query)	
		except: pass
			
			
def Search(url): 	
	if '-' in url:query='-'
	else:query=''

	try:
		keyb=xbmc.Keyboard('', color['search']+'Nhập nội dung cần tìm kiếm[/COLOR]')
		keyb.doModal()
		if (keyb.isConfirmed()):
			searchText=urllib.quote_plus(keyb.getText())
		if 'TimVideo' in url:  
			url=csn+'search.php?s='+searchText+'&cat=video'      
		elif 'TimAlbum' in url:  
			url=woim+'search/album/'+searchText.replace('+', '-')+'.html'      
		elif 'HDOnline' in url:
			url = 'http://hdonline.vn/tim-kiem/'+searchText.replace('+', '-')+'.html'      			
		elif 'VuaHD' in url:		
			url = 'http://vuahd.tv/movies/q/'+searchText.replace('+', '-')
		elif 'HDViet' in url:
			url = hdviet_com+'tim-kiem.html?keyword=%s'%searchText.replace('+', '-')
		elif 'HayHayTV' in url:
			url = hayhaytv_vn+'tim-kiem/%s/trang-1'%searchText.replace('+', '-')
		elif 'DangCapHD' in url:
			url = 'http://dangcaphd.com/movie/search.html?key=%s&search_movie=1'%searchText.replace('+', '-')
		elif 'MegaBox' in url:
			url = 'http://phim.megabox.vn/search/index?keyword='+searchText.replace('+', '-')
		elif 'PhimMoi' in url:
			url = 'http://www.phimmoi.net/tim-kiem/%s/'%searchText.replace('+', '-')     
		elif 'HDCaphe' in url:
			url = hdcaphe + 'search-result.html?keywords=' + searchText
		elif 'PhimGiaiTri' in url:  
			url = pgt+'result.php?type=search&keywords='+searchText
   
		Search_Result(url, query)
	except:pass	

def Search_Result(url, query=''):
	search_string = fixSearch(query)
	if search_string=='-':search_string=''	
	if 'hdonline.vn' in url:
		content = hdonline.GetContent(url)
		content = ''.join(content.splitlines()).replace('\'','"')
		try:
			content =content.encode("UTF-8")
		except: pass
		#vidcontentlist=re.compile('<ul id="cat_tatca"(.+?)</section>').findall(content)
		#if(len(vidcontentlist)>0):
		movielist=re.compile('<li>\s*<div class="tn-bxitem">(.+?)</li>').findall(content)
		for idx in range(len(movielist)):
			vcontent = movielist[idx]				
			items=re.compile('<a href="(.+?)"(.+?)<img src="(.+?)".+?<p class="name-vi">(.+?)</p>\s*<p class="name-en">(.+?)</p>').findall(vcontent)										
			for url, episodes, img, nameen, namevn in items :
				isFolder=True
				name = namevn + ' - ' + nameen							
				if fixSearchss(search_string) in fixSearchss(name) or search_string == '' : # xu ly tim kiem cho nhieu ket qua			
					if 'episodes' in episodes :														
						if query!='':mode='120'
						if query!='' and query!='-':name = '[HDOnline] ' + name
						else:name = color['phimbo'] + name + '[/COLOR]'
						if query=='' or (query!='' and danhmucphim <> 'HDOnline'):
							mode='episodes'
							url = 'http://m.hdonline.vn' + url
					else :						
						if query!='':mode='12'
						if query!='' and query!='-':name = '[HDOnline] ' + name
						if query=='' or (query!='' and danhmucphim <> 'HDOnline'):
							mode='16';isFolder=False
							fid = xshare.xshare_group(re.search('-(\d{1,4}).html',url),1)
							url = '/frontend/episode/loadxmlconfigorder?ep=1&fid='+str(fid)
							url = 'http://hdonline.vn' + url							
							#url = hdonline_vn + 'http:%2F%2Fhdonline.vn' + url.replace('/', '%2F').replace('?', '%3f').replace('=', '%3D')
					xshare.addir(name,url,img,fanart='fanart',mode=mode,page=1,query=nameen,isFolder=isFolder)
		if query=='':				
			pagecontent=re.compile('<ul class="pagination">(.+?)</ul>').findall(content)
			if(len(pagecontent)>0):
				pagelist=re.compile('<li><a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a></li>').findall(pagecontent[0])
				for vurl,vname in pagelist:
					if 'Trang' not in vname : vname = 'Trang ' + vname
					addDir(vname,'http://hdonline.vn'+vurl,'search_result',"")
	elif 'hdviet' in url:	
		body=xshare.make_request(url);body=body[body.find('box-movie-list'):body.find('h2-ttl cf')];		
		pattern='<a href="(.{,200})"><img src="(.+?)"(.+?)"h2-ttl3">(.+?)<span>(.+?)</span>(.*?)<a'
		links=re.findall(pattern,body)		
		for link,img,temp,ttl3,title,cap in links:
			#isFolder=True
			strNameEn, name = strVnEn(title, ttl3.replace('&nbsp;',''))
			caps=''
			#if 'icon-SD' in cap:caps+='[COLOR gold]SD[/COLOR]'
			#if 'icon-720' in cap:caps+='[COLOR gold]HD[/COLOR]720'
			#if 'icon-1080' in cap:caps+='[COLOR gold]HD[/COLOR]1080'
			#if 'icon-TM' in cap:caps+='[COLOR green]TM[/COLOR]'
			#if '>18+<' in cap:caps+='[COLOR red]18+[/COLOR]'
			isFolder=xshare.xshare_group(re.search('"labelchap2">(\d{1,3})</span>',temp),1)
			link=xshare.xshare_group(re.search('id="tooltip(\d{,10})"',temp),1).strip()

			if fixSearchss(search_string) in fixSearchss(name) or search_string == '' : # xu ly tim kiem cho nhieu ket qua			
				if not isFolder:
					isFolder=True
					if query!='':mode='12'
					if query!='' and query!='-':name = '[HDViet] ' + name
					if query=='' or (query!='' and danhmucphim <> 'HDViet'):
						mode='16';isFolder=False
						xshare.addir(name,link,img,fanart='fanart',mode='22',page=1,query='hdvietplay')
					else:
						xshare.addir(name,link,img,fanart='fanart',mode=mode,page=1,query=strNameEn,isFolder=isFolder)
				#elif isFolder=='1':hdviet(title,link,img,mode='22',page=1,query='hdvietfolder',isFolder=True)
				else:
					isFolder=True
					if query!='':mode='120'
					if query!='' and query!='-':name = '[HDViet] ' + name
					else:name = color['phimbo'] + name + '[/COLOR]'
					if query=='' or (query!='' and danhmucphim <> 'HDViet'):
						mode='episodes'
					xshare.addir(name,link,img,fanart='fanart',mode=mode,page=1,query=strNameEn,isFolder=isFolder)
		if query=='':
			pages=re.findall('<li class=""><a href="(.+?)">(.+?)</a></li>',body[body.find('class="active"'):])
			if pages:
				pagenext=pages[0][1];pageend=pages[len(pages)-1][1]
				name='%sTrang tiếp theo: trang %s/%s[/COLOR]'%(color['trangtiep'],pagenext,pageend)
				addDir(name,pages[0][0],'search_result',"")
				#xshare.addir(name,pages[0][0],img,fanart='fanart',mode='search_result',page=1,query='hdvietplay',isFolder=True)
	elif 'hayhaytv' in url:					
		body=xshare.make_request(url);#body=body[body.find('slide_child_div_dt'):];body=body[:body.find('class="paging"')]
		content=body[body.find('slide_child_div_dt'):];content=content[:content.find('class="paging"')]
		pattern='tooltip="(.+?)" href="(.+?)">\s.*"(http://img.+?)".*\s.*color">(.*?)<.*\s.*>(.*?)</span>'
		#pattern='href="(.+?)".*\s.*alt="poster phim (.+?)" src="(.+?)"'
		ids=dict((re.findall('id="(sticky\d{1,3})".{,250}Số tập[\D]{,30}(\d{1,4})',body,re.DOTALL)))		
		items=re.findall(pattern,content)
		print len(items)			
		for stic,href,img,name_e,name_v in items:		
			print stic
			isFolder=True
			name=name_v+' - '+name_e if name_v else name_e			
			if fixSearchss(search_string) in fixSearchss(name) or search_string == '' : # xu ly tim kiem cho nhieu ket qua					
				v_query = name_e[:-7]
				if re.search('Tap-\d{1,3}',href):
					if query!='' and query!='-':name = '[HayHayTV] ' + name
					else:name = color['phimbo'] + name + '[/COLOR]'
					if query=='' or (query!='' and danhmucphim <> 'HayHayTV') or 'xem-show' in href:
						mode='episodes'#episodes
					else:mode='120'#list_server
				else:
					if query!='' and query!='-':name = '[HayHayTV] ' + name
					if query=='' or (query!='' and danhmucphim <> 'HayHayTV') or 'xem-show' in href:
						mode='23';isFolder=False
						v_query = 'play'
					else:mode='12'#list_server
				xshare.addir(name,href,img,fanart='fanart',mode=mode,page=1,query=v_query,isFolder=isFolder)
								
		if query=='':
			if len(items)>14 or (len(items)>7 and 'su-kien' in url):
				temp='trang-' if 'trang-' in url else 'page=';url=re.sub('%s\d{1,3}'%temp,'%s%d'%(temp,page+1),url)
				name='%sTrang tiếp theo: trang %s[/COLOR]'%(color['trangtiep'],page+1)
				addDir(name,url,'search_result&page=%d'%(page+1),"")
				
	elif 'vuahd' in url:
		body=xshare.make_request(url)
		items=re.findall('img src="(.+?)".{,500}<a href="(.+?)" title="(.+?)"',body,re.DOTALL)
		home='http://vuahd.tv'
		for img,href,name in items:			
			names=re.findall('<h2>(.+?)<br />\s*(.+?)\s*</h2>',xshare.make_request(home+href),re.DOTALL)
			for nameen, namevn in names:
				name = namevn.replace('( ', '').replace(')', '') + ' - ' + nameen.strip()				

			if fixSearchss(search_string) in fixSearchss(name) or search_string == '' : # xu ly tim kiem cho nhieu ket qua			
				isFolder=True
				if 'tv-series' in href:	#Phim bộ
					if query=='':
						name = color['phimbo'] + name + '[/COLOR]'
						mode='episodes'	
					elif query=='-':
						name = color['phimbo'] + name + '[/COLOR]'
						mode='120'
					else:
						name = '[VuaHD] ' + name
						mode='120'
					mode='episodes'
					href = home+href
				elif 'actors' not in href:
					isFolder=False
					href = vuahd_tv + 'http%3A%2F%2Fvuahd.tv' + href.replace('/', '%2F')					
					if query=='':
						name = '[Phim lẻ] ' + name
						mode='16'						
					elif query=='-':
						name = '[Phim lẻ] ' + name
						mode='12'
					else:
						name = '[VuaHD] ' + name
						mode='12'
					mode='16'	
				xshare.addir(fixString(name),href,img,fanart='fanart',mode=mode,page=1,query=nameen.strip(),isFolder=isFolder)
		if query=='':pass			
			#if items and len(items)>25:
				#name=color['trangtiep']+'Trang tiếp theo: trang %s[/COLOR]'%str(page+1)
				#xshare.addir(name,url,icon['vuahd'],fanart,mode,page=page+1,query='trangtiep',isFolder=True)		
	elif 'dangcaphd' in url:			
		body=re.sub('\t|\n|\r|\f|\v','',xshare.make_request(url))
		items=re.findall('<a class="product.+?" href="(.+?)" title="(.+?)">.+?<img src="(.+?)" (.+?)</li>',body)		
		for href,name,img,other in items:			
			if ' - ' in name:
				arrName = name.split(' - ')
				str1=str2=strYear=''
				str1 = arrName[0]#.strip()
				if len(arrName) > 1: str2 = arrName[1]#.strip()		
				strNameEn, name = strVnEn(str2, str1)
				if len(arrName) > 2:
					strYear = arrName[2]#.strip()
					name = name + ' (' + strYear + ')'
			print search_string
			if fixSearchss(search_string) in fixSearchss(name) or search_string == '' : # xu ly tim kiem cho nhieu ket qua			
				isFolder=True
				v_query=strNameEn
				if re.search('<div class="sale">.+?</div>',other):
					name=name+' - ('+xshare.xshare_group(re.search('<div class="sale">(.+?)</div>',other),1)+')'
					if query!='' and query!='-':name = '[DangCapHD] ' + name
					else:name = color['phimbo'] + name + '[/COLOR]'
					if query=='' or (query!='' and danhmucphim <> 'DangCapHD'):
						#mode='episodes'#episodes
						mode='18'
						v_query = 'DC3'
					else:mode='120'#list_server
				else:
					if query!='' and query!='-':name = '[DangCapHD] ' + name
					if query=='' or (query!='' and danhmucphim <> 'DangCapHD'):
						mode='18';isFolder=False
						v_query = 'DCP'
					else:mode='12'#list_server
				xshare.addir(name,href,img,fanart='fanart',mode=mode,page=1,query=v_query,isFolder=isFolder)
		#dangcaphd_get_page_control(body,mode,query)
	elif 'megabox.vn' in url:
		content = Get_Url(url)	
		items = re.compile('src="(.+?)">\s*<span class="features">\s*</span>\s*</a>\s*<div class="meta">\s*<h3 class="H3title">\s*<a href="(.+?)">(.+?)</a></h3>\s*<div class="explain">(.+?)</div>').findall(content)
		for img, href, titleVn, titleEn in items:
			name = titleVn + ' - ' + titleEn	
			if fixSearchss(search_string) in fixSearchss(name) or search_string == '' : # xu ly tim kiem cho nhieu ket qua			
				if query=='':
					#name = '[Phim lẻ] ' + name
					mode='16'						
					isFolder=False
				elif query=='-':
					#name = '[Phim lẻ] ' + name
					mode='12'
				else:
					name = '[MegaBox] ' + name
					mode='12'				
			
				href = megabox_vn + href.replace('/', '%2F').replace(':', '%3A')			
				xshare.addir(name,href,img,'fanart',mode='16',page=1,query='play',isFolder=False)
		items = re.compile('src="(.+?)">\s*<span class=\'esp\'>.+?<span class="features">\s*</span>\s*</a>\s*<div class="meta">\s*<h3 class="H3title">\s*<a href="(.+?)">(.+?)</a></h3>\s*<div class="explain">(.+?)</div>').findall(content)
		for img, href, titleVn, titleEn in items:
			name = titleVn + ' - ' + titleEn
			if fixSearchss(search_string) in fixSearchss(name) or search_string == '' : # xu ly tim kiem cho nhieu ket qua
				if query=='':
					name = color['phimbo'] + name + '[/COLOR]'
					mode='episodes'	
				elif query=='-':
					name = color['phimbo'] + name + '[/COLOR]'
					mode='120'
				else:
					name = '[MegaBox] ' + name
					mode='120'											
				xshare.addir(name,href,img,'fanart',mode='episodes',page=1,query='eps',isFolder=True)
				
		#items = re.compile('class="next"><a href="(.+?)">').findall(content)
		#addDir('[COLOR red]Trang Tiếp Theo[/COLOR]', megaboxvn + items[0],'episodes',icon['next'])	
			
	elif 'phimmoi' in url:
		content = Get_Url(url)	
		home='http://www.phimmoi.net/'	
		body=xshare.make_request(url);body=body[body.find('"list-movie"'):body.find('- Sidebar -')]
		pattern='title="(.+?)" href="(.+?)".*?\((.+?)\).*?chap">(.*?)<()'
		if '/tim-kiem/' not in url:pattern=re.sub('\(\)','.*?ribbon">(.*?)<',pattern)
		for name,href,img,chap,rib in re.findall(pattern,body,re.DOTALL):
			if fixSearchss(search_string) in fixSearchss(name) or search_string == '' : # xu ly tim kiem cho nhieu ket qua			
				epi=xshare.xshare_group(re.search('Tập (\d{1,3})/?',chap+rib),1)
				if (epi and int(epi)>1) or '/tập' in chap:
					if query=='':
						name = color['phimbo'] + name + '[/COLOR]'
						mode='episodes'	
					elif query=='-':
						name = color['phimbo'] + name + '[/COLOR]'
						mode='120'
					else:
						name = '[PhimMoi] ' + name
						mode='120'															
					xshare.addir(fixString(name),home+href,img,'fanart',mode='episodes',page=1,query='eps',isFolder=True)
				else:
					if query=='':
						#name = '[Phim lẻ] ' + name
						mode='16'						
						isFolder=False
					elif query=='-':
						#name = '[Phim lẻ] ' + name
						mode='12'
					else:
						name = '[PhimMoi] ' + name
						mode='12'							
				
					#xshare.addir(fixString(name),home+href,img,'fanart',mode=15,page=1,query='play',isFolder=False)
					href = phimmoi_net  + 'http:%2F%2Fphimmoi.net%2F' + href.replace('/', '%2F') + 'xem-phim.html'
					xshare.addir(fixString(name),href,img,'fanart',mode='16',page=1,query='play',isFolder=False)
								
				#if 'Thuyết minh' in chap+'-'+rib:name='[COLOR gold]TM [/COLOR]'+name
				#name=name+' (%s%s)[/COLOR]'%(chap.strip(),'-'+rib.replace('|','') if rib else '')
			
				#trangtiep=xshare.xshare_group(re.search('<li><a href="(.+?)">Trang kế.+?</a></li>',body),1)
				#if trangtiep:
					#trang=xshare.xshare_group(re.search('/page-(\d{1,3})\.html',trangtiep),1)
					#name='%sTrang tiếp theo: trang %s[/COLOR]'%(color['trangtiep'],trang)
					#xshare.addir(name,home+trangtiep,img,fanart,mode,page,'page',isFolder=True)	
	elif 'phimgiaitri' in url:
		content = xshare.make_request(url)			
		#try:
		#items = re.compile('<a style=\'text-decoration:none\' href=\'([^\']*).html\'>\s*<img style=.+?src=(.+?) ><table style.+?:0px\'>(.+?)\s*<\/font>').findall(content)
		items = re.compile('<a style=\'text-decoration:none\' href=\'([^\']*).html\'>\s*<img style=.+?src=(.+?) ><table style.+?:0px\'>(.+?)\s*</font>.+?\'> (.+?)</font>').findall(content)
		for href,img,namevn,nameen in items:		
			strNameEn, name =  strVnEn(namevn, nameen)
			if fixSearchss(search_string) in fixSearchss(name) or search_string == '' : # xu ly tim kiem cho nhieu ket qua			
				if query=='':
					mode='16'						
					isFolder=False
				elif query=='-':
					mode='12'
				else:
					name = '[PhimGiaiTri] ' + name
					mode='12'			
			href = pgt+href+'/Tap-1.html'
			add_Link(name,href,pgt+img)
			#xshare.addir(href,href,pgt+img,'fanart',mode='stream',page=1,query='play',isFolder=False)
			
			#href = phimgiaitri_vn  + 'http:%2F%2Fphimgiaitri.vn%2F' + href.replace('/', '%2F')
			#xshare.addir(href,href,pgt+img,'fanart',mode='16',page=1,query='play',isFolder=False)

		items = re.compile('<a style=\'text-decoration:none\' href=\'([^\']*).html\'>\s*<img style=.+?src=(.+?) ><div class=\'text\'>\s*(.+?)\s*</div><table style.+?:0px\'>(.+?)\s*</font>.+?\'> (.+?)</font>').findall(content)
		for href,img,eps,namevn,nameen in items:		
			name =  namevn + ' - ' + nameen
			if fixSearchss(search_string) in fixSearchss(name) or search_string == '' : # xu ly tim kiem cho nhieu ket qua					
				if '01/01' in eps : #truong hop phim le o trang chu co hien thi (Tập 01/01)
					if query=='':
						mode='16'						
						isFolder=False
					elif query=='-':
						mode='12'
					else:
						name = '[PhimGiaiTri] ' + name
						mode='12'		
					href = pgt+href+'/Tap-1.html'
					add_Link(name,href,pgt+img)					
					#xshare.addir(name,url,pgt+img,'fanart',mode='play',page=1,isFolder=False)	
				else : 
					if query=='':
						name = color['phimbo'] + name + '[/COLOR]'
						mode='episodes'	
					elif query=='-':
						name = color['phimbo'] + name + '[/COLOR]'
						mode='120'
					else:
						name = '[PhimGiaiTri] ' + name
						mode='120'	
					href = pgt+href+'/Tap-1.html'
					xshare.addir(name,href,pgt+img,'fanart',mode='episodes',page=1,isFolder=True)	
								
		#items = re.compile("<a  href='(.+?)'>(\d+)  <\/a>").findall(content) 		
		#for url,name in items:
		  #addDir('[COLOR lime]Trang tiếp theo '+name+'[/COLOR]',pgt+href.replace(' ','%20'),'search_result',icon['next'])
		#except:pass
				
	elif 'hdcaphe' in url:
		content = Get_Url(url)
		items = re.compile("a style=\"position: relative;display: block;\" href=\"(.+?)\">\s*<img class=\"imgborder\" width=\"165\" src=\"(.+?)\"").findall(content)		
		for url,thumbnail in items:
			name = '[UPPERCASE]' + url.replace('detail/movies/','').replace('-',' ').replace('.html','') + '[/UPPERCASE]'
			if fixSearchss(search_string) in fixSearchss(name) or search_string == '' : # xu ly tim kiem cho nhieu ket qua											
				url = hdcaphe + url.replace('detail','video').replace('.html','/play/clip_1.html')			
				content = Get_Url(url)
				if 'clip_2' in content:
					if query=='':
						name = color['phimbo'] + name + '[/COLOR]'
						mode='episodes'	
					elif query=='-':
						name = color['phimbo'] + name + '[/COLOR]'
						mode='120'
					else:
						name = '[HDCaphe] ' + name
						mode='120'											
					addDir(name,url,13,hdcaphe + thumbnail)
				else :
					if query=='':
						#name = '[Phim lẻ] ' + name
						mode='16'						
						isFolder=False
					elif query=='-':
						#name = '[Phim lẻ] ' + name
						mode='12'
					else:
						name = '[HDCaphe] ' + name
						mode='12'							
					add_Link(name,url,hdcaphe + thumbnail)
			
		#items = re.compile("<span class=\"next\"><a href=\"(.+?)\" class=\"next\" title=\"(.+?)\">").findall(content)	
		#for url,name in items:	
			#addDir('[COLOR yellow]' + name.replace('Go to page','Trang Tiếp Theo') + '[/COLOR]',hdcaphe + url,'search_result',icon['next'])  
						
	elif 'chiasenhac' in url:
		content = Get_Url(url)
		items=re.compile("<a href=\"([^\"]*)\" title=\"(.*?)\"><img src=\"([^\"]+)\"").findall(content)
		#items=re.compile("<a href=\"([^\"]*)\" title=\"(.*?)\"><img src=\"([^\"]+)\"\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s*<span class=\"gen\">.*?<br /><span style=\"color: .*?\">(.*?)</span>").findall(content)
		print len(items)
		cat = '...'
		if 'page=' not in url:url=url+"&page=1"
		for href,name,thumbnail in items:
			name=name.replace(';',' +')
			add_Link(name+color['cat']+' ['+cat+'][/COLOR]',csn+href,thumbnail)
		items=re.compile("href=\"(.+?)\" class=\"npage\">(\d+)<").findall(content)
		for href,name in items:
			if 'page='+name not in url:
				addDir(color['trangtiep']+'Trang '+name+'[/COLOR]',href.replace('&amp;','&'),'search_result',icon['next'])
	elif 'woim' in url:
		content = Get_Url(url)
		items=re.compile('href="(.+?)" title="(.+?)" target="_blank"><img src="(.+?)"').findall(content)
		for url,name,thumb in items:
			addDir(name,url,'get_listep',thumb)			 

def Get_ListEp(url,name):
  content = Get_Url(url)
  if 'woim' in url:
    thumb=re.compile('img itemprop="image" src="(.+?)&w').findall(content)[0]
    items=re.compile('ascii" value="([^"]*)".+?\s.+\s.+\s.+\s.+\s*\s.+href=".+?download/(.+?).html').findall(content)
    for name,url in items:
      url=urllib2.urlopen(woim+'ma/'+url)
      link=url.geturl()         
      url.close()
      link=urllib.unquote (link)
      link=link[40:len(link)-23]
      content = Get_Url(link)
      items=re.compile('location="(.+?)"').findall(content)[-1]  
      add_Link(name.upper(),items,thumb)

def Get_M3U(url,iconimage):
  m3ucontent = Get_Url(url)
  items = re.compile('#EXTINF:-?\d,(.+?)\n(.+)').findall(m3ucontent)
  for name,url in items:
	  add_Link(name.replace('TVSHOW - ','').replace('MUSIC - ',''),url,iconimage)
	  
def Index(url,iconimage):
    byname = url.split("?n=")[1]
    url = url.split("?")[0]
    xmlcontent = GetUrl(url)
    channels = re.compile('<channel>(.+?)</channel>').findall(xmlcontent)
    for channel in channels:
        if byname in channel:
            items = re.compile('<item>(.+?)</item>').findall(channel)
            for item in items:
                thumb=""
                title=""
                link=""
                if "/title" in item:
                    title = re.compile('<title>(.+?)</title>').findall(item)[0]
                if "/link" in item:
                    link = re.compile('<link>(.+?)</link>').findall(item)[0]
                if "/thumbnail" in item:
                    thumb = re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
                if "youtube" in link:					
                    addDir(title, link, 'episodes', thumb)
                else:					
                    addLink('' + title + '', link, 'play', thumb)
    skin_used = xbmc.getSkinDir()
    if skin_used == 'skin.xeebo':
        xbmc.executebuiltin('Container.SetViewMode(50)')
		
def IndexGroup(url):
    xmlcontent = GetUrl(url)
    names = re.compile('<name>(.+?)</name>').findall(xmlcontent)
    if len(names) == 1:
        items = re.compile('<item>(.+?)</item>').findall(xmlcontent)
        for item in items:
            thumb=""
            title=""
            link=""
            if "/title" in item:
                title = re.compile('<title>(.+?)</title>').findall(item)[0]
            if "/link" in item:
                link = re.compile('<link>(.+?)</link>').findall(item)[0]
            if "/thumbnail" in item:
                thumb = re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
            add_Link(title, link, thumb)
        skin_used = xbmc.getSkinDir()
        if skin_used == 'skin.xeebo':
            xbmc.executebuiltin('Container.SetViewMode(52)')
        else:
            xbmc.executebuiltin('Container.SetViewMode(%d)' % 500)			
    else:
        for name in names:
            addDir('' + name + '', url+"?n="+name, 'index', '')

def Index_Group(url):
	xmlcontent = GetUrl(url)
	names = re.compile('<name>(.+?)</name>\s*<thumbnail>(.+?)</thumbnail>').findall(xmlcontent)
	if len(names) == 1:
		items = re.compile('<item>(.+?)</item>').findall(xmlcontent)
		for item in items:
			thumb=""
			title=""
			link=""
			if "/title" in item:
				title = re.compile('<title>(.+?)</title>').findall(item)[0]
			if "/link" in item:
				link = re.compile('<link>(.+?)</link>').findall(item)[0]
			if "/thumbnail" in item:
				thumb = re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
			addLink(title, link, 'play', thumb)
		skin_used = xbmc.getSkinDir()
		if skin_used == 'skin.xeebo':
				xbmc.executebuiltin('Container.SetViewMode(50)')
	else:
		for name,thumb in names:
			addDir(name, url+"?n="+name, 'index', thumb)

def menulist(homepath):
	try:
		mainmenu=open(homepath, 'r')  
		link=mainmenu.read()
		mainmenu.close()
		match=re.compile("<title>([^<]*)<\/title>\s*<link>([^<]+)<\/link>\s*<thumbnail>(.+?)</thumbnail>").findall(link)
		return match
	except:
		pass
	
def resolveUrl(url):
	if 'xemphimso' in url:
		content = Get_Url(url)	
		url = urllib.unquote_plus(re.compile("file=(.+?)&").findall(content)[0])
	elif 'vtvplay' in url:
		content = Get_Url(url)
		url = content.replace("\"", "")
		url = url[:-5]
	elif 'vtvplus' in url:
		content = Get_Url(url)
		url = re.compile('var responseText = "(.+?)";').findall(content)[0]		
	elif 'htvonline' in url:
		content = Get_Url(url)	
		url = re.compile('data\-source=\"([^\"]*)\"').findall(content)[0]
	elif 'hplus' in url:
		content = Get_Url(url)	
		url = re.compile('iosUrl = "(.+?)";').findall(content)[0]
	elif 'megabox' in url:
		content = Get_Url(url)	
		url = re.compile('var iosUrl = "(.+?)"').findall(content)[0]+'|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36 VietMedia/1.0'		
	elif 'chiasenhac' in url:
		content = Get_Url(url)
		try:
		  url = re.compile("\"hd-2\".+?\"([^\"]+)\"").findall(content)[0].replace('%3A',':').replace('%2F','/').replace('%2520','%20')
		except:
		  url = re.compile("\"hd-2\".+?\"([^\"]+)\"").findall(content)[-1].replace('%3A',':').replace('%2F','/').replace('%2520','%20')
	elif 'hdcaphe' in url:
		content = Get_Url(url)	
		url=re.compile('\'http.startparam\':\'start\',\s*file: \'(.+?)\'').findall(content)[0].replace(' ','%20')

	elif 'f.vp9.tv' in url:
		content = Get_Url(url)
		try:
		  try:
		    url = url+re.compile('<a href="(.*?)HV.mp4"').findall(content)[0]+'HV.mp4'
		  except:
		    url = url+re.compile('<a href="(.*?)mvhd.mp4"').findall(content)[0]+'mvhd.mp4'
		except:
		  url = url+re.compile('<a href="(.*?)mv.mp4"').findall(content)[0]+'mv.mp4'
	elif 'ott.thuynga' in url:
		content = Get_Url(url)	
		url=re.compile("var iosUrl = '(.+?)'").findall(content)[0]
	elif 'phim7' in url:
		content = Get_Url(url)
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
		content = Get_Url(url2)
		content = content[3:]
		infoJson = json.loads(content)
		tapindex = int(tap) -1
		link = infoJson['ep_info'][tapindex]['link']
		link = link.replace('#','*')
		url3 ='http://120.72.85.195/phimgiaitri/mobile/service/getdireclink.php?linkpicasa=' + link
		content = Get_Url(url3)
		content = content[3:]
		linkJson = json.loads(content)
		url = linkJson['linkpi'][0]['link720'] or linkJson['linkpi'][0]['link360']		
	else:
		url = url
	item=xbmcgui.ListItem(path=url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)	  
	return

def PlayVideo(url,title):
    if(url.find("youtube") > 0):
        vidmatch=re.compile('(youtu\.be\/|youtube-nocookie\.com\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)').findall(url)
        vidlink=vidmatch[0][len(vidmatch[0])-1].replace('v/','')
        url = 'plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid=' + vidlink.replace('?','')
        xbmc.executebuiltin("xbmc.PlayMedia("+url+")")	
    else:
        title = urllib.unquote_plus(title)
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem(title)
        listitem.setInfo('video', {'Title': title})
        xbmcPlayer = xbmc.Player()
        playlist.add(url, listitem)
        xbmcPlayer.play(playlist)
	
def Get_Url(url):
    try:
		req=urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)')
		response=urllib2.urlopen(req)
		link=response.read()
		response.close()  
		return link
    except:
		pass
    
def GetUrl(url):
    link = ""
    if os.path.exists(url)==True:
        link = open(url).read()
    else:
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
    link = ''.join(link.splitlines()).replace('\'','"')
    link = link.replace('\n','')
    link = link.replace('\t','')
    link = re.sub('  +',' ',link)
    link = link.replace('> <','><')
    return link
	
def add_Link(name,url,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode=stream"+"&img="+urllib.quote_plus(iconimage)
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty('IsPlayable', 'true')  
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)  

def addLink(name,url,mode,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
    return ok
	
def addDir(name,url,mode,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&img="+urllib.quote_plus(iconimage)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    if ('www.youtube.com/user/' in url) or ('www.youtube.com/channel/' in url):
		u = 'plugin://plugin.video.youtube/%s/%s/' % (url.split( '/' )[-2], url.split( '/' )[-1])
		ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
		return ok	
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok	
	
DecryptData = base64.b64decode	
homeurl = 'aHR0cDovL2NhbnRvYnVzaG9wLmNvbS9YQk1DL01lbnUueG1s'

def get_params():#print json.dumps(json["content"],indent=2,sort_keys=True)
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
xbmcplugin.setContent(int(sys.argv[1]), 'movies');params=get_params();mode=page=1;temp=[]
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
print "Main---------- Mode: "+str(mode),"URL: "+str(url),"Name: "+str(name),"query: "+str(query),"page: "+str(page)
#if not mode:#xbmc.executebuiltin("Dialog.Close(all, true)")
	#Home()
if mode == 'index':Index(url,img)
elif mode == 'indexgroup':IndexGroup(url)	
elif mode == 'index_group':Index_Group(url)	
elif mode == 'menu_group':Menu_Group(url)
elif mode == 'category':category(url)
elif mode == 'episodes':episodes(url)
elif mode == 'get_listep':Get_ListEp(url,name)	
elif mode == 'get_m3u':Get_M3U(url,img)
elif mode == 'search_result':Search_Result(url)
elif mode == 'search':Search(url)
	
elif mode=='stream':
    dialogWait = xbmcgui.DialogProgress()
    dialogWait.create('Cantobu Media', 'Đang tải. Vui lòng chờ trong giây lát...')
    resolveUrl(url)
    dialogWait.close()
    del dialogWait	
elif mode=='play':
    dialogWait = xbmcgui.DialogProgress()
    dialogWait.create('Cantobu Media', 'Đang tải. Vui lòng chờ trong giây lát...')
    PlayVideo(url,name)
    dialogWait.close()
    del dialogWait

elif mode=='12' or mode=='120':#serverlist	
	ServerList(name, url, mode, query)
	
elif mode=='15':
	def getid(url):return xshare.xshare_group(re.search('-(\d{3,5})/',url),1)
	def geteps(string):
		try:url=json.loads(string)['url'];part=json.loads(string)['part']
		except:url=part=''
		return url,part
	def make_eps(url,eps):
		id=getid(url);content=makerequest(phimmoixml);string=''
		string_old=xshare.xshare_group(re.search('(<a id="%s" part=".+?"/>)'%id,content),1)
		for part_id in eps:string+=str(geteps(part_id)[1])+'-'
		string_new='<a id="%s" part="%s"/>\n'%(id,string[:len(string)-1])
		string=content.replace(string_old+'\n',string_new) if string_old else content+string_new
		makerequest(phimmoixml,string,'w')

	#phimmoi.net
	href='http://www.phimmoi.net/player/v1.46/plugins/gkplugins_picasa2gdocs/plugins/plugins_player.php?url=%s'
	if '.html' not in url:url=url+'xem-phim.html'
	pattern='data-language="(.+?)".*href="(.+?)">.*\s.*Xem Full';content=xshare.make_request(url)
	content=content[content.find('- slider -'):content.find('- Sidebar -')]
	links=dict(re.findall(pattern,content));temp=body='';pattern="currentEpisode.url='(.+?)'"
	if not links:#Khong co ban full
		eps=[s.replace('\\','') for s in re.findall('({"episodeId":.+?})',content)]
		if not eps:body=''
		elif len(eps)==1:body=xshare.make_post(href%geteps(eps[0])[0])
		elif xshare.xshare_group(re.search('Part (\d{1,3}) - ',name),1):
			part_id=int(xshare.xshare_group(re.search('Part (\d{1,3}) - ',name),1));epiurl=''
			for epi in eps:
				if geteps(epi)[1]==part_id:epiurl=geteps(epi)[0];break
			body=xshare.make_post(href%epiurl) if epiurl else ''
		elif 'xem-phim.html' not in url:body=xshare.make_post(href%xshare.xshare_group(re.search(pattern,content),1))
		else:make_eps(url,eps);body=xshare.make_post(href%geteps(eps[0])[0])	

elif mode=='16':

	content = hdonline.GetContent(url)
	print content
		
	vurl=re.compile('<jwplayer:file>(.+?)</jwplayer:file>').findall(content)[0]
	if(vurl.find("http") == -1):
		vurl=hdonline.decodevplug(vurl)		
	vsubtitle=re.compile('<jwplayer:vplugin.subfile>(.+?)</jwplayer:vplugin.subfile>').findall(content)
	suburl=""
	if(len(vsubtitle)>0 and vsubtitle[0].find("http")>-1):
		suburl=vsubtitle[0]
		if ',' in suburl: suburl=suburl.split(',')[0]
	elif(len(vsubtitle)>0):
		suburl=decodevplug(vsubtitle[0])

	print vurl
	print suburl
	
	link=vurl
	subtitle=suburl
	
	listitem = xbmcgui.ListItem(path=link)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
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
		notification(u'Không tải được phụ đề phim.');
	  #urllib.urlretrieve (subtitle,subfile )
	else:
	  notification('Video này không có phụ đề rời.');

elif mode==17:end=xshare.megabox(name,url,mode,page,query)
elif mode=='18':xshare.dangcaphd(name,url,img,mode,page,query)
elif mode==19:xshare.pubvn(name,url,img,mode,page,query)
elif mode=='21':xshare.vuahd(name,url,img,mode,page,query)
elif mode=='22':
	#hdviet.play(url, ep = 1)
	xshare.hdviet(name,url,img,mode,page,query)
elif mode=='23':
	print url
	hd = {'User-Agent' : 'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'}
	body=xshare.make_request(url,headers=hd,maxr=3)	
	movie_id=xshare.xshare_group(re.search('FILM_ID\D{3,7}(\d{3,6})',body),1)
	print movie_id
	hayhaytv.play(movie_id, 1, subtitle='')
	
	#xshare.hayhaytv(name,url,img,'fanart',mode,page,query)
elif mode==24:xshare.phimmoi(name,url,img,mode,page,query)
	
else:xshare.init_file(),Home();setViewMode('3')
xbmcplugin.endOfDirectory(int(sys.argv[1]))