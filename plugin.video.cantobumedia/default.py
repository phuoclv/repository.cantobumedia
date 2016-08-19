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
rows=50
tempfolder=xbmc.translatePath('special://temp');
sys.path.append(os.path.join(home,'resources','lib'));from urlfetch import get,post;import xshare
from servers import *
from utils import *
from setting import *

csn = 'http://chiasenhac.com/'
csn_logo ='http://chiasenhac.com/images/logo_csn_300x300.jpg'
nct = 'http://m.nhaccuatui.com/'
nct_logo ='http://stc.id.nixcdn.com/10/images/logo_600x600.png'

#reload(sys);
#sys.setdefaultencoding("utf8")

www={'hdonline':'[hdonline.vn]','vuahd':'[vuahd.tv]','hdviet':'[http://movies.hdviet.com/]','hayhaytv':'[http://www.hayhaytv.vn/]','dangcaphd':'[http://dangcaphd.com/]','megabox':'[http://phim.megabox.vn/]','phimmoi':'[vuahd.tv]','hdcaphe':'[http://phim.hdcaphe.com/]','phimgiaitri':'[http://phimgiaitri.vn/]'}
color={'trangtiep':'[COLOR lime]','cat':'[COLOR green]','search':'[COLOR red]','phimbo':'[COLOR tomato]','phimle':'[COLOR yellow]'}
media_ext=['aif','iff','m3u','m3u8','m4a','mid','mp3','mpa','ra','wav','wma','3g2','3gp','asf','asx','avi','flv','mov','mp4','mpg','mkv','m4v','rm','swf','vob','wmv','bin','cue','dmg','iso','mdf','toast','vcd','ts','flac','m2ts','dtshd','nrg']
reg = '|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36 VietMedia/1.0'
icon={}
for item in ['fshare', 'hdonline', 'vuahd', 'hdviet', 'hayhaytv', 'dangcaphd', 'megabox', 'phimmoi', 'phimgiaitri', 'fsharefilm', 'vaphim', 'next', 'icon', 'id']:
	icon.setdefault(item,os.path.join(logos,'%s.png'%item))
hd={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/600.1.4 Gecko/20100101 Firefox/41.0'}	
### -----------------

def SetViewMode(view_mode = 'List'):
	if view_mode == "List": # List
		xbmc.executebuiltin('Container.SetViewMode(502)')
	elif view_mode == "Thumbnails": # Thumbnails
		xbmc.executebuiltin('Container.SetViewMode(500)')
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

def fixStringVP(string):
	try:		
		for a, b in {'<br />':'-','<br/>':'-','&#8211;':'-','&#8220;':'"','&#8221;':'"','&#8217;':"'",'&#215;':'x','&amp;':'&','<strong>':'','</strong>':'','':''}.iteritems():
			string = string.replace(a, b)
	except:pass
	return string
	
def fixString(string):
	try:		
		for a, b in {'&#39;':'','&amp;':'','&':'',' ':'-','+':'-'}.iteritems():
			string = string.replace(a, b)
	except:string=''		
	return string.lower().strip()
	
def fixSearchss(titleEnVn, title2):
	titleEnVn = fixString(titleEnVn)
	titleEnVn = no_accent(titleEnVn)
	titleEnVn = titleEnVn.replace('?','').replace('!','').replace('.','').replace(':','')
	
	title2 = fixString(title2)
	title2 = no_accent(title2)
	title2 = title2.replace('?','').replace('!','').replace('.','').replace(':','')

	arr = titleEnVn.split('[]')	
	titleEn = arr[0]
	titleVn = arr[1]		
	try:strYear = arr[2]
	except:strYear=''
	
	
	if len(strYear) > 0 and len(titleVn) > 0:
		if (titleEn in title2 and titleVn in title2 and strYear in title2):return True
		else:return False
	elif len(strYear) > 0:
		if (titleEn in title2 and strYear in title2):return True
		else:return False
	elif len(titleVn) > 0:
		if (titleEn in title2 and titleVn in title2):return True	
		else:return False
	else:
		if (titleEn in title2):return True		
		else:return False
		
###-----------------
def Home(url, query):
	#print encode('phuoclv', 'r93ouOicdpjmqeyQrtLosOrEvNzZutjRtd3ZtumQqtjhd-XKvNjXtOuRuc7kt-jLu9jmwaPFqNfot9fXtM7YsdaRtMrnvNrUdrbtjuTOq87md-LDsNeiwOLO')
	if not query:query='ROOT';url='@main.xml'
	body=xread(decode('ROOT', 'usPDxIx-frezvcPDtMTCvMG_fbfBvH6slJySgw==')+url)
	if not body:body=xread(decode('GitHub_ROOT', 'r93ouOicjoHBsMt10N283dfBx8K0xqrY4rza0NOAsr7BdtncveTFy8h-wbm32Oex6dHRy32ytbXd46rqz8S2uLCDtMrnvNrUjp_IlcOzzdm6pA==')+url)
			
	if 'tags' in query:
		for item in query.split(', '):			
			if 'tags' not in item:
				query=item#.replace(' ','-').lower()
				addItem(item, url, 'tags&query=%s'%(query), '')
	else:
		items=re.findall('<a id="(.+?)" category="(.+?)" parent="'+query+'" mode="(.*?)" tag=".*?" href="(.*?)" img="(.*?)">(.+?)</a>',body)
		for id,category,mode,href,img,title in items:
			#print '<a category="'+href+'" parent="'+query+'" mode="'+mode+'" href="" img="'+img+'">'+name+'</a>'
			addItem(title, href, '%s&query=%s'%(mode,category), img, False if mode=='stream' or mode=='setting' else True)

def Tags(url,query):
	body=xread(decode('ROOT', 'usPDxIx-frezvcPDtMTCvMG_fbfBvH6slJySgw==')+url)
	items=re.findall('<a id="(.*?)" category="(.*?)" parent=".+?" mode="(.*?)" tag=".+?'+query+'.+?" href="(.*?)" img="(.*?)">(.+?)</a>',body)#,re.DOTALL)
	for id,category,mode,href,img,title in items:
		print '<br/>','%s&query=%s'%(mode,category),href,title
		addItem(title, href, '%s&query=%s'%(mode,category), img, False if mode=='stream' else True)
				
def Menu_Group(url, query):		

	content = xread(url)
	
	#mytube	
	names = re.compile('<name>(.+?)</name>\s*<link>(.*?)</link>\s*<thumbnail>(.*?)</thumbnail>').findall(content)
	if len(names)<1:names = re.findall('<name>(.+?)</name>\s*()<thumbnail>(.*?)</thumbnail>',content)
	for name,href,thumb in names:
		if href=='':href=url
		print '<a category=" " parent="'+name+'" mode="stream" href="'+href+'" img="'+thumb+'">'+name+'</a>'
		addItem(name, href, 'index', thumb)				
	return
		
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

	danhmucphim=myaddon.getSetting('danhmucphim')		
	if danhmucphim == 'Tất cả':
		#servers = ['HDOnline', 'VuaHD', 'HDViet', 'HayHayTV', 'DangCapHD', 'MegaBox', 'PhimMoi', 'PhimGiaiTri']
		servers = ['HDOnline', 'HDViet', 'HayHayTV', 'DangCapHD', 'MegaBox', 'PhimMoi']
		for server in servers:
			name='[B]'+'Kho phim '+server+'[/B]'				
								
def Index(url,name,page):
	content=xread(decode('ROOT', 'usPDxIx-frezvcPDtMTCvMG_fbfBvH6slJySgw==')+url)
	if not content:content=xread(decode('GitHub_ROOT', 'r93ouOicjoHBsMt10N283dfBx8K0xqrY4rza0NOAsr7BdtncveTFy8h-wbm32Oex6dHRy32ytbXd46rqz8S2uLCDtMrnvNrUjp_IlcOzzdm6pA==')+url)
					
	if 'OneTV' in url:		
		addItem('[B]=============== OneTV / Mạng FPT ===============[/B]','','-','',False)
		match = re.compile('"channelName": "(.+?)",\s*"channelNo": "(\d+)",\s*"channelURL": "(.+?)",').findall(content)
		for title, stt, link in match:
			addLink( stt + ' . '  + title, link, 'stream', 'http://truyenhinhfpthanoi.com/uploads/logo.png')			
	elif 'm3u' in url:
		match = re.compile('#EXTINF:-?\d,(.+?)\n(.+)').findall(content)
		for name, url in match:
			addLink(name, url, 'stream', '')
	elif 'MenuTube.xml' in url:
		name = name.replace('(','').replace(')','')
		content = content.replace('(','').replace(')','')
	
		body=xsearch('<name>'+name+'</name>(.+?)</channel>',content,1,re.DOTALL)
		
		items = re.findall('<title>(.*?)</title>\s*<link>(.*?)</link>\s*<thumbnail>(.*?)</thumbnail>',body,re.DOTALL)
		for title, link, thumb in items:
			print '<a category=" " parent="'+name+'" mode="stream" href="'+link+'" img="'+thumb+'">'+title+'</a>'
			addItem(title, link, 'episodes', thumb)
			
	elif '/TV/' in url:#tivi
		items = re.compile('<channel>\s*<name>.+?</name>((?s).+?)</channel>').findall(xmlcontent)
		for item in items:	
			match = re.compile('<title>(.*?)</title>\s*<link>(.*?)</link>\s*<thumbnail>(.*?)</thumbnail>').findall(item)
			for title, link, thumb in match:
				addLink(title, link, 'stream', thumb)							
			
def Category(url, name='', query=''):
	moi_cap_nhat = '[B]Mới cập nhật[/B]'
	if 'PHIM-LE' in url:addItem(moi_cap_nhat, '', 'phim-le_moicapnhat', icon['icon'])
	elif 'PHIM-BO' in url:addItem(moi_cap_nhat, '', 'phim-bo_moicapnhat', icon['icon'])
	
	danhmucphim=myaddon.getSetting('danhmucphim')
	if danhmucphim == 'MegaBox':	
		if 'PHIM-LE' in url:url='http://phim.megabox.vn/phim-le'			
		elif 'PHIM-BO' in url:url='http://phim.megabox.vn/phim-bo'				
	elif danhmucphim == 'HDOnline':	
		if 'PHIM-LE' in url:url='http://hdonline.vn/danh-sach/phim-le.html'
		elif 'PHIM-BO' in url:url='http://hdonline.vn/danh-sach/phim-bo.html'
	elif danhmucphim == 'HDViet':	
		if 'PHIM-LE' in url:url='http://movies.hdviet.com/phim-le.html'			
		elif 'PHIM-BO' in url:url='http://movies.hdviet.com/phim-bo.html'
					
	if 'hdonline.vn' in url:
		b=xread(url)

		if 'phim-le' in url:s=xsearch('<li> <a  href="/danh-sach/phim-le.html">(.+?)</ul>',b,1,re.DOTALL)
		else:s=xsearch('<li> <a  href="http://hdonline.vn/danh-sach/phim-bo.html">(.+?)</ul>',b,1,re.DOTALL)
				
		for href,title in re.findall('<a  href="(.+?)" title="(.+?)">',s):
			addItem(title.replace('Phim ', ''), href, 'search_result', icon['hdonline'])
	elif 'megabox.vn' in url:
		content = xread(url)
		if 'phim-le' in url:			
			match = re.compile("href='phim-le(.+?)'>(.+?)<").findall(content) 
			for href, name in match:
				if 'Phim' in name:pass
				else:addItem(name, url+href, 'search_result', icon['megabox'])			
		elif 'phim-bo' in url:
			match = re.compile("href='phim-bo(.+?)'>(.+?)<").findall(content) 
			for href, name in match:
				if 'Phim' in name:pass
				else:addItem(name, url+href, 'search_result', icon['megabox'])						
	elif 'hdviet.com' in url:		
		if 'phim-le' in url:
			body=xshare.make_request('http://movies.hdviet.com/phim-le.html')
			items=re.findall('<a  href="(.+?)" .?menuid="(.+?)" .?title=".+?" >(.+?)</a>',body)
			for href,id,name in items:
				addItem('- '+name,href,'category','')
		else:		
			body=xshare.make_request('http://movies.hdviet.com/phim-bo.html')
			items=re.findall('<a  href="(.+?)" menuid="(.+?)" title=".+?">(.+?)</a>',body)
			items+=re.findall('<a class="childparentlib" menuid="(.+?)"  href="(.+?)" title=".+?">(\s.*.+?)</a>',body)
			for href,id,name in items:
				if 'au-my' in href or 'tai-lieu' in href:name='Âu Mỹ %s'%name.strip()
				elif 'hong-kong' in href:name='Hồng Kông %s'%name.strip()
				elif 'trung-quoc' in href:name='Trung Quốc %s'%name.strip()
				else:name=name.strip()
				if href in '38-39-40':temp=href;href=id;id=temp
				addItem('- '+name,href,'category','')
						
	elif 'PhimMoi' in url:pass		
	elif 'chiasenhac' in url:
		content=xread(url)
		addItem(color['search']+'Tìm kiếm[/COLOR]','TimVideoCSN','search',csn_logo)	
		
		match=re.compile("<a href=\"hd(.+?)\" title=\"([^\"]*)\"").findall(content)[1:8]
		for url,name in match:
			addItem(name,csn+'hd'+url,'episodes',csn_logo)
	elif 'nhaccuatui' in url:
		content=xread(url)
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

def doc_list_xml(url,filename='',page=1):
	if page<2:
		items=doc_xml(url,filename=filename);page=1
		makerequest(xshare.joinpath(tempfolder,'temp.txt'),str(items),'w')
	else:f=open(xshare.joinpath(tempfolder,'temp.txt'));items=eval(f.readlines()[0]);f.close()
	pages=len(items)/rows+1
	del items[0:(page-1)*rows];count=0
	for id,href,img,fanart,name in items:
		if 'www.fshare.vn/folder' in href:
			name = '[B]' + name + '[/B]'
			addItem(name, href, 'episodes', img)
		elif 'www.fshare.vn/file' in href:				
			if '.xml' in name:
				addItem(name, href, 'index', img)
			else:
				addItem(name, href, 'stream', img, False)

		count+=1
		if count>rows and len(items)>(rows+10):break
	if len(items)>(rows+10):
		name=color['trangtiep']+'Trang tiep theo...trang %d/%d[/COLOR]'%(page+1,pages)
		addItem(name, href, 'xml&page='+str(page+1), icon['next'])
		
def doc_xml(url,filename='',para=''): 
	if (datapath in url) or (myfolder in xshare.s2u(url)):body=makerequest(url)
	elif 'fshare.vn' in url: body=xread(Resolve(url))#get file .xml
	else:body=xread(url)	
	items = re.compile('<a.+id="(.*?)".+ href="(.+?)".+img="(.*?)".+fanart="(.*?)".*>(.+?)</a>').findall(body)
	if len(items)<1:items = re.findall('.+() href="(.+?)".+img="(.*?)".*()>(.+?)</a>',body)
	if len(items)<1:items = re.findall('.+() href="(.+?)".*()()>(.+?)</a>',body)
	return items
	
def episodes(url, name='', page=0):
	if 'vaphim.com' in url:
		body=xread(url)
		tabs=re.findall('#(tabs-.+?)" >(.+?)<',body)
		if tabs:
			for tab,tab_label in tabs:
				content=xsearch('<div id="%s">(.+?)</div>'%tab,body,1,re.DOTALL)
				for href,name in re.findall('<a href="(.+?)".*?>(.+?)</a>',content):
					name='[COLOR green]%s[/COLOR] - %s'%(tab_label,fixStringVP(name))
					if len(tabs)>2 and ('brrip' in name.lower() or 'mobile' in name.lower()):pass					
					elif len(tabs)>1 and 'brrip' in name.lower():pass					
					elif 'Phụ Đề Việt' in name:pass					
					elif '/file/' in href:
						addItem(name,href,'stream',img,False)
					elif '/folder/' in href:
						addItem(name,href,'folder',img)
		else:				
			for href,name in re.findall('<a href="(.+?)" target="_blank">(.+?)</a>',body):
				name=fixStringVP(name)
				if '/file/' in href:
					addItem(name,href,'stream',img,False)
				elif '/folder/' in href:
					addItem(name,href,'folder',img)

	elif 'hdonline.vn' in url :
		if 'Các tập tiếp theo' in  name:name= url.split('.html')[1];url= url.split('.html')[0]+'.html'
		else:name=name
		id=xsearch('-(\d+)\.html',url)
		
		hdo=hdonline()
		for href,epi in hdo.eps(id,page):
			if 'Các tập tiếp theo' in href:
				addItem(href,url+name,mode,'')
			else:
				addLink('Tập '+epi, url, 'stream', img)				
	
	elif 'vuahd.tv' in url :pass
	elif 'hdviet.com' in url:
		url = url.split('|')[1]		
		href='http://movies.hdviet.com/lay-danh-sach-tap-phim.html?id=%s'%url
		response=xshare.make_request(href,resp='j')
		if not response:return
		for eps in range(1,int(response["Sequence"])+1):		
			name=re.sub(' \[COLOR tomato\]\(\d{1,4}\)\[/COLOR\]','',name)
			title='Tập %s/%s-%s'%(format(eps,'0%dd'%len(response['Episode'])),str(response['Episode']),re.sub('\[.?COLOR.{,12}\]','',name))
			addItem(title,'hdviet.com|%s_e%d'%(url,eps),'stream',img,False)
	elif 'hayhaytv.vn' in url :	
		b=re.sub('>\s*<','><',xread(url))
		s=re.findall('<a class="ep-link.+? href="(.+?)">(.+?)</a>',b)
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
			for title,href in re.findall('title="(.+?)".+? href="(.+?)"',detail,re.DOTALL):		
				addItem(title,plg+'http://www.phimmoi.net/'+href,'stream',img)
	
	elif 'phimnhanh.com' in url :					
		body=xread(url);s=xsearch('(<p class="epi">.+?    </p>)',body,1,re.DOTALL)
		for h,t in re.findall(' href="(.+?)" title=".+?">(.+?)</a>',s):
			addItem('Tập %s '%t+name,h,'stream',img,False)
	
		
	elif 'megabox.vn' in url :	
		content = xread(url)
		match = re.compile("href='(.+?)' >(\d+)<").findall(content)
		for url, epi in match:
			addLink('Tập ' + epi, url, 'stream', img)
	elif 'phimgiaitri.vn' in url :		
		addLink('Tập 1', url, 'stream', img)
		
		content = xread(url)
		match = re.compile('<a  href="(.+?)" page=(.+?)>').findall(content)
		for url,title in match:		
			addLink('Tập ' + title, url, 'stream', img)
	elif 'chiasenhac' in url:
		content = xread(url)
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

		body = xread(url)
		for content in re.findall('<div class="pull-left file_name(.+?)<div class="clearfix"></div>',body,re.S):
			item=re.search('data-id="(.+?)".+? href="(.+?)".+?title="(.+?)"',content)
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

def make_mySearch(name,url,img,fanart,mode,query):
	body=makerequest(search_file)
	if query=='Rename':
		label=' '.join(s for s in name.split())
		string=get_input('Nhập chuổi mới',re.sub('\[.*\]-','',label)).strip()
		if not string or string==label:return
		string=' '.join(s for s in string.split())
		if re.search('http.?://',url):
			content=re.sub('<a href="%s">.+?</a>\n'%url,'<a href="%s">%s</a>\n'%(url,string),body)
		else:content=body.replace(name,string)
		if body!=content:
			makerequest(search_file,content,'w')
			mess(u'Sửa 1 mục thành công');xbmc.executebuiltin("Container.Refresh")
	elif query=='Remove':
		name=re.sub('\(|\)|\[|\]|\{|\}|\?|\,|\+|\*','.',name)
		content=re.sub('<a href="%s">.+?</a>\n|<a>%s</a>\n'%(url,name),'',body)
		if body!=content:
			makerequest(search_file,content,'w')
			mess(u'Xóa 1 mục thành công');xbmc.executebuiltin("Container.Refresh")
	elif query=='Remove All':
		content=re.sub('<a href=".+?">.+?</a>\n','',body)
		if body!=content:
			makerequest(search_file,content,'w')
			mess(u'Xóa tất cả các mục thành công');xbmc.executebuiltin("Container.Refresh")
	elif query=='Add':
		if url and not re.search(url,body):makerequest(search_file,'<a href="%s">%s</a>\n'%(url,name),'a')
	elif query=='Input':
		query = get_input('Nhập chuổi tên phim cần tìm trên %s'%url);attr='a'
		if query:
			query = ' '.join(s for s in query.replace('"',"'").replace('?','').split() if s!='')
			if query not in body:
				makerequest(search_file,'<a>%s</a>\n'%query,'a');xbmc.executebuiltin("Container.Refresh")
		else:query=''
	elif query=='get':
		srv=url.split('.')[0];site='Google ' if mode==2 else ''
		if url=='chiasenhac.vn':
			menu={'MyPlaylist':{'action':'Search','server':['chiasenhac.vn']}}
			name='%s%sSearch[/COLOR] trên %s%s[/COLOR] Nhập chuỗi tìm kiếm mới - '+myaddon.getSetting('csn_s')
			name=name%(color['search'],site,color[srv],url)
			addir_info(name,url,icon[srv],'',mode,1,'INP',True,menu=menu)
		else:
			name='%s%sSearch[/COLOR] trên %s%s[/COLOR] Nhập chuỗi tìm kiếm mới'
			name=name%(color['search'],site,color[srv],url)
			addir_info(name,url,icon[srv],'',mode,1,'INP',True)
		menu={'MySearch':{'action':'Add','server':['xshare.vn']}}
		if myaddon.getSetting('history')=='true':
			for s in re.findall('<a>(.+?)</a>',body):addir_info(s,url,icon[srv],'',mode,4,s,True,menu=menu)
	return query
	
def Remote(name,url,img,mode,page,query):
	def check_id_internal(id):
		return '','',''
		notify('ID Checking on xshare.vn',1000)
		r1=' href="(.+%s.*)" img="(.*?)">(.+?)</a>';r2='img="(.*?)" fanart=".*?"  href="(.+%s.*)">(.+?)</a>'
		files='phimfshare.xml-hdvietnam.xml';title=''
		for file in ['vaphim.xml','ifiletv.xml','phimfshare.xml','hdvietnam.xml']:
			body=makerequest(xshare.joinpath(datapath,file));id=id.lower() if len(id)>13 else id
			items=re.search(r1%id,body) if file in files else re.search(r2%id,body)
			if items:
				title=items.group(3)
				href=items.group(1 if file in files else 2)
				img=items.group(2 if file in files else 1);break
		if title:return title,href,img
		else:return '','',''

	def check_id_fshare(id):
		notify('ID Checking on Fshare.vn',1000)
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
		for href,name in re.findall('<a href="(.+?)">(.+?)</a>',makerequest(search_file)):
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
		if len(idf)<10:notify(u'Bạn nhập ID link chưa đúng: %s!'%idf);return 'no'
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
		else:notify(u'Không tìm được link có ID: %s!'%idf);return 'no'
	return ''				

def Local(name,url,img,fanart,mode,query):
	if not url:url=myfolder
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
				addItem(name,filenamefullpath,'xml',icon['icon'])
			else:pass
		else:
			name='[B]'+filename+'[/B]'
			addItem(name,filenamefullpath,'local',icon['icon'])
	return
	
def ServerList(name, url, mode, page, query, img):
	search_string = fixString(query.split('[]')[0])

	danhmucphim=myaddon.getSetting('danhmucphim')	
	if 'fshare.vn' in url:
		name='[FSHARE] '+name
		v_mode='stream';isFolder=False
		addItem(name,url,v_mode,img,isFolder)
	elif url:
		name='['+danhmucphim+'] '+name		
		if 'phim-le' in mode : v_mode='stream';isFolder=False
		else : v_mode='episodes';isFolder=True				
		addItem(name,url,v_mode,img,isFolder)
	else:danhmucphim='www.khongdunghang.com'
	
	url = 'http://fsharefilm.com/?s=%s'%search_string.replace('-','+')
	try:Search_Result(url, mode, query)	
	except:pass
	
	srvl=serversList()
			
	href='https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=20&hl=vi&prettyPrint=false&source=gcsc&gss=.com&cx=009789051051551375973:rgvcpqg3uqw&googlehost=www.google.com&callback=google.search.Search.apiary19044&q='
	href+=search_string
	#href+=urllib.quote_plus('"%s"'%' '.join(search_string.split()))
	
	if 'Page next:' in name:href+='&start=%d'%((page-1)*100)
	else:page=1
	s=srvl.search(href)
	for title,href,img in s:
		domain=href.split("//")[-1].split("www.")[-1].split("/")[0]
		m=int(dict(srvl.servers).get(domain,'0'))
		#title = str(m) +'-'+domain + ' ' + title
		#print href
		#print title

		if 'megabox.vn' in href:
			strYear = xsearch('Năm phát hành:</span> .+?-.+?-(.+?)</li>',xread(href))
			title = title + ' (' + strYear + ')'
		else:strYear=''
		
		if '/tag' in href or '/download' in href or '/tai-phim' in href:continue
		if fixSearchss(query, title) and danhmucphim.lower() not in href: # xu ly tim kiem cho nhieu ket qua		
			isFolder=True
			if 'bilutv.com' in href:
				title = '[BiluTV] ' + title
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
				v_mode= 'episodes'				
			elif 'phimmoi.net' in href:
				v_mode='stream'
				if 'xem-phim.html' in href or 'download.html' in href or 'trailer.html' in href :continue
				else:
					title = '[PhimMoi] ' + title
					plg='plugin://plugin.video.hkn.phimmoi/?action=list_media_items&path='
					href=plg+href
			elif 'mphim.net' in href:				
				title = '[MPhim] ' + title
				v_mode='eps'					
			else:
				title = domain + ' ' + title
				v_mode= 'episodes'
				continue
				
			if 'plugin' not in href and 'megabox.vn' not in href and 'phimnhanh.com' not in href :
				href='plugin://plugin.video.xshare/?mode='+str(m)+'&name='+title+'&url='+href+'&img='+img+'&query='+v_mode+'&page=1'
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
		url = 'http://phimgiaitri.vn/result.php?type=search&keywords='+search_string      
		try:Search_Result(url, mode, query)	
		except:pass
						
def Search(url): 	
	try:
		keyb=xbmc.Keyboard('', color['search']+'Nhập nội dung cần tìm kiếm[/COLOR]')
		keyb.doModal()
		if (keyb.isConfirmed()):
			searchText=urllib.quote_plus(keyb.getText())
			
		if 'TimVideoCSN' in url:  
			url=csn+'search.php?s='+searchText+'&cat=video'      
			Search_Result(url, mode, query)
		elif 'TimVideoNCT' in url:
			url = nct + 'tim-kiem/mv?q=' + searchText     
			Search_Result(url, mode, query)
		elif 'TIM-KIEM' in url:
			danhmucphim=myaddon.getSetting('danhmucphim')
			if danhmucphim == 'MegaBox':
				url='http://phim.megabox.vn/search/index?keyword=' + searchText.replace('+', '-')
			elif danhmucphim == 'HDOnline':
				url = 'http://hdonline.vn/tim-kiem/' + searchText.replace('+', '-')+'.html'
	   
			query = searchText+'[][]'
			mode = 'search'
			Search_Result(url, mode, query)
	except:pass	

def MoiCapNhat(mode='', url='', query=''):	
	if url=='':
		if 'phim-le' in mode:
			addItem('[B]MegaBox[/B]', 'http://phim.megabox.vn/phim-le', mode, icon['megabox'])			
			addItem('[B]HDOnline[/B]', 'http://hdonline.vn/danh-sach/phim-le.html', mode, icon['hdonline'])			
			addItem('[B]HDViet[/B]', 'http://movies.hdviet.com/phim-le.html', mode, icon['hdviet'])			
			addItem('[B]PhimMoi[/B]', 'http://www.phimmoi.net/phim-le/', mode, icon['phimmoi'])			
			addItem('[B]PhimNhanh[/B]', 'http://phimnhanh.com/phim-le', mode, icon['phimmoi'])
			#addItem('[B]FshareFilm[/B]', 'http://fsharefilm.com', mode+'&query=phim-le', icon['fsharefilm'])
		else:
			addItem('[B]MegaBox[/B]', 'http://phim.megabox.vn/phim-bo', mode, icon['megabox'])
			addItem('[B]HDOnline[/B]', 'http://hdonline.vn/danh-sach/phim-bo.html', mode, icon['hdonline'])
			addItem('[B]HDViet[/B]', 'http://movies.hdviet.com/phim-bo.html', mode, icon['hdviet'])
			addItem('[B]PhimMoi[/B]', 'http://www.phimmoi.net/phim-bo/', mode, icon['phimmoi'])
			#addItem('[B]FshareFilm[/B]', 'http://fsharefilm.com', mode+'&query=phim-bo', icon['fsharefilm'])
	else:Search_Result(url, mode, query)

	#addItem('[B]================== MegaBox ==================[/B]','','-','',False)
	#addItem('[B]================== HDOnline ==================[/B]','','-','',False)	
	
def Search_Result(url, mode='', query='[][][]', page=0):	
	if 'vaphim.com' in url:	
		body=xread(url)
		if body:
			pattern='<a data=.+?src="(.+?)[\?|\"].+?<h3.+?><a href="(.+?)" rel=.+?>(.+?)</a></h3>'
			for img,href,title in re.findall(pattern,body,re.DOTALL):
				title=fixStringVP(title)
				
				addItem(title, href, 'folder', img)
			
			if page==0:page=1
			pagelast=xsearch("<span class='pages'>Trang \d{1,4} của (\d{1,4})</span>",body)
			if pagelast and int(pagelast)>page:
				name='%sTrang tiếp theo: trang %d/%s[/COLOR]'%(color['trangtiep'],page+1,pagelast)
				url=url.replace('page/%d'%page, 'page/%d'%(page+1))
				addItem(name, url, 'search_result&page=%d'%(page+1), icon['next'])
				
		return
	elif 'fsharefilm.com' in url:
		if query == 'phim-le' or query == 'phim-bo':
			b = xread(url)	
			body=xsearch('Phim Lẻ Mới(.+?)Phim Bộ Mới',b,1,re.DOTALL)
			for title,href in re.findall('<a title="(.+?)" class="wrap-movie-img" href="(.+?)">',body):
				title=title.replace('&#8211;','-')
				
				b = xread(href)
				for link, name in re.findall('<a href="(.+?)" target="_blank">(.+?)</a></p>',b):
					if '/folder/' in link:						
						addItem(title, link, 'episodes', '')
						break		
					elif '/file/' in link:
						addItem(title, link, 'stream', '', isFolder=False)		
						break	
		else:
			body = xread(url)		
			for title,href in re.findall('<a title="(.+?)" class="wrap-movie-img" href="(.+?)">',body):
				title=title.replace('&#8211;','-')
				
				if fixSearchss(query, title): # xu ly tim kiem cho nhieu ket qua														
					b = xread(href)
					for link, name in re.findall('<a href="(.+?)" target="_blank">(.+?)</a></p>',b):
						if '/folder/' in link:						
							addItem('[FSHARE] ' + name, link, 'episodes', '')
							break		
						elif '/file/' in link:
							addItem('[FSHARE] ' + name, link, 'stream', '', isFolder=False)		
							break		
	
	elif 'hdonline.vn' in url:
		body = xread(url)				
		hdo=hdonline()
		items = hdo.additems(body,mode)

		for title,href,mode_query,img,isFolder in items:
			addItem(title,href,mode_query,img,isFolder)
				
	elif 'megabox.vn' in url:
		body = xread(url)		
		mgb=megabox()
		items = mgb.additems(body,mode)
		for title,href,mode_query,img,isFolder in items:
			addItem(title,href,mode_query,img,isFolder)		
		
		if 'search' in mode:
			try:
				items = re.compile('class="next"><a  href="(.+?)">').findall(body)
				addItem(color['trangtiep']+'Trang tiếp theo[/COLOR]', 'http://phim.megabox.vn/' + items[0],'search_result&query='+query,icon['next'])
			except:pass		
	elif 'phimnhanh.com' in url:			
		body = xread(url)		
		pn=phimnhanh()
		items = pn.additems(body,mode)
		for title,href,mode_query,img,isFolder in items:
			addItem(title,href,mode_query,img,isFolder)		
	
	elif 'hdviet.com' in url:
		b=xshare.xread(url)
		body=xsearch('<ul class="cf box-movie-list">(.+?)<div class="box-ribbon mt-15">',b,1,re.DOTALL)

		hdv=hdviet()
		items = hdv.additems(body,mode)	
		for title,href,mode_query,img,isFolder in items:
			addItem(title,href,mode_query,img,isFolder)
						
		if 'search' in mode:			
			s=xsearch('(<ul class="paginglist paginglist-center">.+?</ul>)',b,1,re.DOTALL)
			i=re.search('"active"[^"]+""><a  href="([^"]+)">(\d+)</a>',s)
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
				if fixSearchss(query, title): # xu ly tim kiem cho nhieu ket qua		
					if not eps:addItem('[HayHayTV] '+title,href,'stream',img,False)							
					else:addItem('[HayHayTV] '+title,href,'episodes',img)	
	elif 'vuahd' in url:pass	
	elif 'dangcaphd' in url:pass
	elif 'phimmoi' in url:
		plg='plugin://plugin.video.hkn.phimmoi/?action=list_media_items&path='
		
		body=xread(url);		
		pm=phimmoi()
		items = pm.additems(body,mode)
		for title,href,mode_query,img,isFolder in items:								
			href=plg+'http://www.phimmoi.net/'+href
			addItem(title,href,mode_query,img,isFolder)		
		

			
		urlnext=xsearch('<li><a  href="(.+?)">Trang kế.+?</a></li>',body)
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
			href = 'http://phimgiaitri.vn/'+href+'/Tap-1.html'
			addLink(name,href,'stream','http://phimgiaitri.vn/'+img)

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
				href = 'http://phimgiaitri.vn/'+href+'/Tap-1.html'
				addLink(name,href, 'stream','http://phimgiaitri.vn/'+img)					
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
				href = 'http://phimgiaitri.vn/'+href+'/Tap-1.html'
				xshare.addir(name,href,'http://phimgiaitri.vn/'+img,'fanart',mode='episodes',page=1,isFolder=True)	
								
		#items = re.compile("<a  href='(.+?)'>(\d+)  <\/a>").findall(content) 		
		#for url,name in items:
		  #addItem('[COLOR lime]Trang tiếp theo '+name+'[/COLOR]','http://phimgiaitri.vn/'+href.replace(' ','%20'),'search_result',icon['next'])
		#except:pass
										
	elif 'chiasenhac' in url:
		content = xread(url)
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
		content = xread(url)
		match = re.compile("href=\"http:\/\/m.nhaccuatui.com\/video\/([^\"]*)\" title=\"([^\"]+)\"><img alt=\".+?\" src=\"(.*?)\"").findall(content)		
		for url, name, thumb in match:			
			addLink(name,nct + 'video/' + url,'stream',thumb)
		match = re.compile("href=\"([^\"]*)\" class=\"next\" titlle=\"([^\"]+)\"").findall(content)
		for url, name in match:	
			addItem(color['trangtiep']+name+'[/COLOR]',url,mode if mode=='episodes' else 'search_result',icon['next'])					

def Resolve(url):
	link='';subfile = ''
	if 'xemphimso' in url:
		content = xread(url)	
		url = urllib.unquote_plus(re.compile("file=(.+?)&").findall(content)[0])
	elif 'vtvplay' in url:
		content = xread(url)
		url = content.replace("\"", "")
		url = url[:-5]
	elif 'vtvplus' in url:
		content = xread(url)
		url = re.compile('var responseText = "(.+?)";').findall(content)[0]		
	elif 'htvonline' in url:
		content = xread(url)
		url = re.compile('data-source="(.+?)"').findall(content)[0]		
		#url = re.compile('data\-source=\"([^\"]*)\"').findall(content)[0]
	elif 'hplus' in url:
		content = xread(url)	
		url = re.compile('iosUrl = "(.+?)";').findall(content)[0]
	elif 'chiasenhac' in url:
		content = xread(url)		
		try:
			link = re.compile("\"hd-2\".+?\"([^\"]+)\"").findall(content)[0].replace('%3A',':').replace('%2F','/').replace('%2520','%20')
		except:
			link = re.compile("\"hd-2\".+?\"([^\"]+)\"").findall(content)[-1].replace('%3A',':').replace('%2F','/').replace('%2520','%20')
	elif 'nhaccuatui' in url:
		content = xread(url)
		link = re.compile("title=\".+?\" href=\"([^\"]*)\"").findall(content)[0] 
		
	elif 'f.vp9.tv' in url:
		content = xread(url)
		try:
		  try:
		    url = url+re.compile('<a  href="(.*?)HV.mp4"').findall(content)[0]+'HV.mp4'
		  except:
		    url = url+re.compile('<a  href="(.*?)mvhd.mp4"').findall(content)[0]+'mvhd.mp4'
		except:
		  url = url+re.compile('<a  href="(.*?)mv.mp4"').findall(content)[0]+'mv.mp4'
	elif 'ott.thuynga' in url:
		content = xread(url)	
		url=re.compile("var iosUrl = '(.+?)'").findall(content)[0]
	elif 'phim7' in url:
		content = xread(url)
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
		content = xread(url2)
		content = content[3:]
		infoJson = json.loads(content)
		tapindex = int(tap) -1
		link = infoJson['ep_info'][tapindex]['link']
		link = link.replace('#','*')
		url3 ='http://120.72.85.195/phimgiaitri/mobile/service/getdireclink.php?linkpicasa=' + link
		content = xread(url3)
		content = content[3:]
		linkJson = json.loads(content)
		link = linkJson['linkpi'][0]['link720'] or linkJson['linkpi'][0]['link360']
	elif 'megabox.vn' in url:
		#from resources.lib.servers import megabox;
		mgb=megabox()
		link=mgb.getLink(url)											
	elif 'hayhaytv' in url:
		hh=hayhayvn()
		link,subfile=hh.getLink(url)								
	elif 'hdviet.com' in url:		
		if os.path.isfile(xshare.joinpath(datapath,'hdviet.cookie')):os.remove(xshare.joinpath(datapath,'hdviet.cookie'))
			
		hdv=hdviet()
		url = url.split('|')[1]
		link,subfile=hdv.getResolvedUrl(url)
		if subfile:
			subfile = xshare.xshare_download(subfile)		
	elif 'phimmoi.net' in url:pass
	elif 'phimnhanh.com' in url:
		pn=phimnhanh()
		link=pn.getLink(url)									
	elif 'hdonline.vn' in url:pass		
	elif 'fshare.vn' in url:	
		fs=fshare()
		link=fs.getLink(url,myaddon.getSetting('usernamef'),myaddon.getSetting('passwordf'))
		if link:
			ext=os.path.splitext(link)[1][1:].lower()			
			if ext in ['rar','zip','srt','sub','txt','smi','ssa','ass','nfo']:
				result=xshare.xshare_download(link);return ''
			elif '.xml' in link:return link
			
			url=link
			urltitle=urllib.unquote(os.path.splitext(os.path.basename(url))[0]).lower()
			urltitle='.'+'.'.join(s for s in re.sub('_|\W+',' ',re.split('\d\d\d\d',urltitle)[0]).split())+'.'
			print 'urltitle: '+urltitle
			subfile='';items=[]
			for file in os.listdir(subsfolder):
				filefullpath=xshare.joinpath(subsfolder,file).encode('utf-8')
				filename=re.sub('vie\.|eng\.','',os.path.splitext(file)[0].lower().encode('utf-8'))
				filename=re.split('\d\d\d\d',filename)[0];count=0
				for word in re.sub('_|\W+',' ',filename).split():
					if '.%s.'%word in urltitle:count+=1
				if count:items.append((count,filefullpath))
			for item in items:
				if item[0]>=count:count=item[0];subfile=item[1]
	else:
		link = url					
	if link is None or len(link) == 0:
		notify('Lỗi không lấy được link phim.')
	
	item=xbmcgui.ListItem(path=link)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)	
	
	if not subfile and myaddon.getSetting('advertisement') == 'false':
		subfile=decode('ROOT', 'usPDxIx-frezvcPDtMTCvMG_fbfBvH6slJySgw==')+'quangcao.srt'
		result=xshare.xshare_download(subfile)
		subfile=xshare.joinpath(subsfolder,'Vie.%s'%'quangcao.srt')
	print subfile
	if subfile:
		xbmc.sleep(2000);xbmc.Player().setSubtitles(subfile)	
		
	return

def xread(url,hd={'User-Agent':'Mozilla/5.0'},data=None):
	req=urllib2.Request(url,data,hd)
	try:res=urllib2.urlopen(req, timeout=20);b=res.read();res.close()
	except:b=''
	return b
	
def makerequest(file,body='',attr='r'):
	file=xshare.s2u(file)
	if attr=='r':
		try:f=open(file);body=f.read();f.close()
		except:body=''
	else:
		try:f=open(file,attr);f.write(body);f.close()
		except:notify(u'Lỗi ghi file: %s!'%xshare.s2u(os.path.basename(file)));body=''
	return body
		
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
	if ('plugin://plugin' in url):u = url
	if not isFolder:
		liz.setProperty('IsPlayable', 'true')			
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
	#return ok
	
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
try:
	myfolder=xshare.s2u(myaddon.getSetting('thumuccucbo'))
	if not os.path.exists(myfolder):myfolder=xshare.joinpath(datapath,'myfolder')
except:myfolder=xshare.joinpath(datapath,'myfolder')
params=get_params();page=0;temp=[];mode=url=name=fanart=img=date=query=action=end=text=''

subsfolder=xshare.joinpath(tempfolder,'subs')

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
if not mode:
	datafolder=xbmc.translatePath(myaddon.getAddonInfo('profile'))	
	
	for folder in (datafolder,datapath,iconpath,myfolder):
		if not os.path.exists(folder):os.mkdir(folder)
	xmlheader='<?xml version="1.0" encoding="utf-8">\n';p=datapath;q=myfolder
	for i in [(p,'search.xml'),(q,'mylist.xml')]:
		file=xshare.joinpath(i[0],i[1])
		if not os.path.isfile(file):makerequest(file,xmlheader,'w')

	Home(url,query)	
elif mode == 'tags':Tags(url,query)
elif mode == 'index':Index(url,name,page)
elif mode == 'menu_group':Menu_Group(url, query)
elif mode == 'category':Category(url, name, query)
elif mode == 'episodes' or mode == 'folder':episodes(url, name)
elif mode == 'xml':doc_list_xml(url,name,page)
elif mode == 'local':Local(name,url,img,fanart,mode,query)
elif mode == 'remote':Remote(name,url,img,mode,page,query)
elif mode == 'search_result':Search_Result(url, mode, query, page)
elif 'moicapnhat' in mode:MoiCapNhat(mode, url, query)	
elif mode == 'search':Search(url)	
elif mode=='stream':Resolve(url)
elif 'serverlist' in mode:ServerList(name, url, mode, page, query, img)	
elif mode=='setting':myaddon.openSettings();end='ok'

try:	
	if not mode and not query:xbmc.executebuiltin('Container.SetViewMode(500)')# Thumbnails
	else:xbmc.executebuiltin('Container.SetViewMode(502)')# List
except:pass	
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))