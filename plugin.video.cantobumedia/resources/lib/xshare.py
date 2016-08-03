__author__ = 'thaitni'
# -*- coding: utf-8 -*-
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,urllib,urllib2,re,os,unicodedata,datetime,time,random,json,sys

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


media_ext=['aif','iff','m3u','m3u8','m4a','mid','mp3','mpa','ra','wav','wma','3g2','3gp','asf','asx','avi','flv','mov','mp4','mpg','mkv','m4v','rm','swf','vob','wmv','bin','cue','dmg','iso','mdf','toast','vcd','ts','flac','m2ts','dtshd','nrg'];icon={}
color={'fshare':'[COLOR gold]','vaphim':'[COLOR gold]','phimfshare':'[COLOR khaki]','4share':'[COLOR blue]','tenlua':'[COLOR fuchsia]','fptplay':'[COLOR orange]','trangtiep':'[COLOR lime]','search':'[COLOR lime]','ifile':'[COLOR blue]','hdvietnam':'[COLOR red]','hdviet':'[COLOR darkorange]','xshare':'[COLOR blue]','subscene':'[COLOR green]','chiasenhac':'[COLOR orange]','phimmoi':'[COLOR ghostwhite]','megabox':'[COLOR orangered]','dangcaphd':'[COLOR yellow]','hayhaytv':'[COLOR tomato]','kenh88':'[COLOR cyan]','phimdata':'[COLOR magenta]','phim47':'[COLOR springgreen]','phimsot':'[COLOR orangered]','hdonline':'[COLOR turquoise]','phim3s':'[COLOR lightgray]','kphim':'[COLOR lightgreen]','phimnhanh':'[COLOR chartreuse]','bilutv':'[COLOR hotpink]','pubvn':'[COLOR deepskyblue]','anime47':'[COLOR deepskyblue]','phim14':'[COLOR chartreuse]','taifile':'[COLOR cyan]','phim':'[COLOR orange]','tvhay':'[COLOR gold]','nhacdj':'[COLOR fuchsia]','phimbathu':'[COLOR lightgray]','taiphimhd':'[COLOR blue]','hdsieunhanh':'[COLOR orangered]','vuahd':'[COLOR tomato]','nhaccuatui':'[COLOR turquoise]','imovies':'[COLOR orange]','vietsubhd':'[COLOR cyan]','imax':'[COLOR chartreuse]','mphim':'[COLOR deepskyblue]','vtvgo':'[COLOR green]'}
for hd in ['xshare','4share','dangcaphd','downsub','favorite','fptplay','fshare','gsearch','hdvietnam','icon','id','ifiletv','ifile','isearch','khophim','maxspeed','megabox','movie','msearch','myfolder','myfshare','phimfshare','serverphimkhac','setting','tenlua','vaphim','hdviet','hayhaytv','chiasenhac','kenh88','phimdata','phim47','phimsot','hdonline','phim3s','kphim','phimnhanh','bilutv','anime47','phim14','taifile','phim','tvhay','nhacdj','phimbathu','taiphimhd','hdsieunhanh','phimmoi','vuahd','pubvn','nhaccuatui','imovies','vietsubhd','imax','mphim','vtvgo']:
	icon.setdefault(hd,os.path.join(iconpath,'%s.png'%hd))
hd={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/600.1.4 Gecko/20100101 Firefox/41.0'}

def mess(message='',title='',timeShown=5000):
	if not message:xbmc.executebuiltin("Dialog.Close(all, true)")
	else:
		title=': [COLOR blue]%s[/COLOR]'%title if title else ''
		s0='[COLOR green][B]Xshare[/B][/COLOR]'+title
		s1='[COLOR red]%s[/COLOR]'%message if '!' in message else u'[COLOR gold]%s[/COLOR]'%message
		xbmc.executebuiltin((u'XBMC.Notification(%s,%s,%s,%s)'%(s0,s1,timeShown,icon['icon'])).encode("utf-8"))

def mess_yesno(title='[COLOR green]Xshare[/COLOR]', line1='', line2='',no='No',yes='Yes'):
	dialog=xbmcgui.Dialog()#dialog.yesno(heading, line1[, line2, line3,nolabel,yeslabel])
	return dialog.yesno(title,line1,line2,nolabel=no,yeslabel=yes)

def no_accent(s):
	s=re.sub(u'Đ','D',s2u(s));s=re.sub(u'đ','d',s)
	return unicodedata.normalize('NFKD', unicode(s)).encode('ASCII', 'ignore')

def resolu(s):
	s=s.replace('HDG','').replace('HD','1080').replace('SD','640').replace('large','640').replace('medium','480').replace('small','360')
	result=xsearch('(\d+)',s)
	return result if result else '240'

def dl(l):#Direct link
	o=make_request(l,resp='o',maxr=5);h=''
	try:s=int(o.headers.get('content-length'))
	except:s=0
	s=0 if s<10**7 else s
	if s and o.history:h=o.history[-1].headers['location']
	elif s:h=l
	return h

def gdl(l,link=''):
	if type(l)==list:
		for href,label in l:
			link=dl(href)
			if link:break
	else:link=l
	return link

def s2u(s):return s.decode('utf-8') if isinstance(s,str) else s
def unescape(string):return ' '.join(re.sub('&.+;',xsearch('&(\w).+;',s),s) for s in string.split())
def u2s(s):return s.encode('utf-8') if isinstance(s,unicode) else s
def printdict(mydict):print json.dumps(mydict,indent=2);return ''
def add_sep_item(label):addir_info('[COLOR lime]--%s--[/COLOR]'%label,'',icon['xshare'],'',100,1,'')
def labelsearch(label):return '%s%s[/COLOR]'%(color['search'],label)
def namecolor(name,c=''):return '[COLOR %s]%s[/COLOR]'%(c,name) if c else re.sub('\[[^\[]+?\]','',name)

def open_category(query): #category.xml
	if query=='MMN':root=True
	else:root=False
	pattern='<a server="(.+?)" category="(.+?)" mode="(\d+)" color="(.*?)" icon="(.*?)">(.+?)</a>'
	items=re.findall(pattern,makerequest(joinpath(data_path,'category.xml')));q='';fanart=home+'/fanart.jpg'
	for server,category,mode,colo,icon,name in items:
		if (server!=query) or (("18" in category) and (myaddon.getSetting('phim18')=="false")):continue
		if query=='VPH' and mode!='10':q='vaphim.xml'
		elif query=='IFI' and mode!='10':q='ifiletv.xml'
		else:q=category
		name='[COLOR '+colo+']'+name+'[/COLOR]';icon=joinpath(iconpath,icon)
		addir(name,category,icon,fanart,mode=int(mode),page=0,query=q,isFolder=(mode!='16'),root=root)
	if q=='vaphim.xml':
		body=makerequest(joinpath(datapath,"vp_menu.txt"));icon=joinpath(iconpath,'vaphim.png')
		if not body:mess(u'Đang update menu...','vaphim.com');return#vp_make_datanew();return
		for query,name in eval(body):
			if "18" in name and myaddon.getSetting('phim18')=="false":continue
			addir('%s%s[/COLOR]'%(color['vaphim'],name),'vaphim.xml',icon,fanart,92,1,query,True,root=root)
	if query=='MMN' and (myaddon.getSetting('my_nas_url')!="http://buffalonas.com/"):
		addir('[COLOR lime]My NAS[/COLOR]','',os.path.join(iconpath,'csn.png'),fanart,52,1,'home',True,root=root)

def servers_list(name,url,img,fanart,mode,page,query):
	def make_ls(s):
		i=0;l=len(s)
		for d,m in s:#sl:server location
			title=namecolor('Kho phim trên %s'%d,color[d.split('.')[0]].replace('[COLOR ','').replace(']',''));i+=1
			if i==1:menu={'servers_list':{'action':'Down'}}
			elif i<l:menu={'servers_list':{'action':'Up-Down'}}
			else:menu={'servers_list':{'action':'Up'}}
			addir_info(title,d,joinpath(iconpath,d.split('.')[0]+'.png'),'',int(m),1,d,True,menu=menu)
	
	from resources.lib.servers import servers_list;srv=servers_list()
	menu={'servers_list':{'action':'Up-Down'}}
	if query=='FRE':
		s=srv.mylist();l=len(s)
		for i in range(l/10+(1 if l%10>0 else 0)):
			addir_info(namecolor('Servers group %d'%(i+1),'lime'),str(i),icon['xshare'],'',mode,1,'group',True)
		
		add_sep_item('All servers ------------------------------------------------')
		make_ls(s)
	
	elif query=='group':
		s=srv.mylist();i=0;l=len(s)
		def mm(i):return i+10 if i+10<len(s) else i+len(s)%10
		make_ls([[s[i] for i in range(i,mm(i))] for i in range(0,len(s),10)][int(url)])
			
	
	else :step=-1 if query=='Up' else 1;srv.move(url,step);xbmc.executebuiltin("Container.Refresh")

def clean_string(string):
	return ' '.join(s for s in re.sub('Fshare|4share|Tenlua','',string).split())

def remove_tag(string):
	if '::' in string:string=string.split('::')[1]
	string=re.sub('\t|\n|\r|\f|\v|vn|Fshare|fshare|4share|4Share|TenLua|tenlua|List xml',' ',string)
	string=re.sub('\[/?COLOR.*?\]|\[\s*\]|\(.*?\)|\{.*?\}|<.*?>|\"|\'|-|\||,|&\w*;|/|br|\.',' ',string)
	return ' '.join(i for i in u2s(unescape(string)).split())

def joinpath(p1,p2):
	try:p=os.path.join(p1,p2)
	except:p=os.path.join(p1,s2u(p2))
	return p

def init_file():
	datafolder=xbmc.translatePath(myaddon.getAddonInfo('profile'))
	for folder in (datafolder,datapath,iconpath,myfolder,tempfolder,subsfolder,xsharefolder):
		if not os.path.exists(folder):os.mkdir(folder)
	xmlheader='<?xml version="1.0" encoding="utf-8">\n';p=datapath;q=myfolder
	for i in [(p,'search.xml'),(p,'hdvietnam.xml'),(p,'favourites.xml'),(p,'phimmoi.xml'),(p,'fpt.xml'),(q,'mylist.xml')]:
		file=joinpath(i[0],i[1])
		if not os.path.isfile(file):makerequest(file,xmlheader,'w')

def sub_body(content,s1,s2):
	if not isinstance(content,str):content=str(content)
	if s1 and s2:result=content[content.find(s1):content.find(s2)]
	elif s1:result=content[content.find(s1):]
	elif s2:result=content[:content.find(s2)]
	else:result=content
	return result

def json_rw(file,dicts={},key=''):
	if dicts:makerequest(joinpath(datapath,file),json.dumps(dicts),'w')
	else:
		try:dicts=json.loads(makerequest(joinpath(datapath,file)))
		except:dicts={}
		if key:dicts=dicts.get(key,())
	return dicts

def get_dict(dict,key_list=list(),result=''):
	for key in key_list:
		dict=dict.get(key,result)
		if dict==result:break
	return dict

def sets(lists):
	temp=list()
	for s in lists:
		if s not in temp:temp.append(s)
	return temp

def folders(folder,result=list()):#get files fullpath from folder and subfolders
	for f in os.listdir(folder):
		f=joinpath(folder,f)
		if os.path.isdir(f):folders(f,result)
		else:result.append(f)
	return result

def delete_files(folder,mark=''):
	temp='ok'
	for file in os.listdir(folder):
		if os.path.isfile(joinpath(folder,file)) and (not mark or mark in file):
			try:os.remove(joinpath(folder,file))
			except:temp='';pass
	return temp

def delete_folder(folder):
	for file in os.listdir(folder):
		try:
			files=joinpath(folder,file)
			if os.path.isdir(files):delete_folder(files);os.rmdir(files)
			#for f in os.listdir(files):
			#	os.remove(joinpath(files,f))
			else:os.remove(files)
		except:pass

def rename_file(sf,df,kq='ok'):
	try:
		if os.path.isfile(df):os.remove(df)
		os.rename(sf,df)
	except:kq='';pass
	return kq

def endxbmc():
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def xbmcsetResolvedUrl(url,name='',img=''):
	if img:item=xbmcgui.ListItem(path=url, iconImage=img, thumbnailImage=img)
	else:item=xbmcgui.ListItem(path=url)
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
			xbmc.sleep(2000);xbmc.Player().setSubtitles(subfile)
			mess(u'%s'%s2u(os.path.basename(subfile)),'Auto load sub',5000)

def addir(name,link,img='',fanart='',mode=0,page=0,query='',isFolder=False,root=False):
	def xquote(href):return urllib.quote_plus(href)
	if '18+' in name and phim18=="false":return
	name=unescape(re.sub(',|\|.*\||\||\<.*\>','',u2s(name)))
	item=xbmcgui.ListItem(name,iconImage=img,thumbnailImage=img)

	if not root:
		label='[COLOR lime]Add to My Favourites V2[/COLOR]'
		q='Add-'+(query.split('?')[1] if '?' in query else query)+'-'+('F' if isFolder else '')
		cmd='RunPlugin(plugin://%s/?'%myaddon.getAddonInfo('id');items=list()
		cmd=cmd+'&name=%s&url=%s&img=%s&fanart=%s&mode=%d&page=%d&query=%s)'
		cmd=cmd%(xquote(name),xquote(url),xquote(img),xquote(fanart),100+mode,page,xquote(q))
		command=[(label,cmd)]
	else:command=[]
	
	query=menuContext(name,link,img,fanart,mode,query,item,command)
	item.setInfo(type="Video", infoLabels={"title":name})
	if not fanart:fanart=joinpath(home,'fanart.jpg')
	item.setProperty('Fanart_Image',fanart)
	li='%s?name=%s&url=%s&img=%s&fanart=%s&mode=%d&page=%d&query=%s'
	li=li%(sys.argv[0],xquote(name),xquote(link),xquote(img),xquote(fanart),mode,page,xquote(query))
	if not isFolder:item.setProperty('IsPlayable', 'true')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),li,item,isFolder)

def addirs(name,href,img='',fanart='',query=''):
	name=clean_string(name)
	if not fanart and iconpath not in img:fanart=img
	if 'xml' in query:
		if name=='mylist.xml':name=color['subscene']+name+'[/COLOR]'
		query=query.replace('xml','');name='%sList xml[/COLOR]-%s'%(color['fptplay'],name)
		addir(name,href,img,fanart,mode=97,query=query,isFolder=True)
	elif query=='file':addir(name,href,img=icon['icon'],mode=96,query=query,isFolder=True)
	elif 'www.fshare.vn/file' in href:
		if 'phụ đề việt' in u2s(name).lower():
			name=color['fshare']+'Phụ đề Việt[/COLOR]-%s'%name
			addir(name,href,img,fanart,mode=3,query=query,isFolder=True)
		else:addir(color['fshare']+'Fshare[/COLOR]-%s'%name,href,img,fanart,mode=3,query=query)
	elif 'www.fshare.vn/folder' in href:
		if s2u('chia sẻ') in s2u(name):name=color['trangtiep']+name+'[/COLOR]'
		else:name=color['fshare']+name+'[/COLOR]'
		addir(name,href,img,fanart,mode=90,query=query,isFolder=True)
	elif '4share.vn/d/' in href:
		addir(color['4share']+name+'[/COLOR]',href,img,fanart,mode=38,query=query,isFolder=True)
	elif '4share.vn' in href:
		addir(color['4share']+'4share[/COLOR]-%s'%name,href,img,fanart,mode=3,query=query)
	elif 'tenlua.vn/fm/folder/' in href or '#download' in href:
		addir(color['tenlua']+name+'[/COLOR]',href,img,fanart,mode=95,query=query,isFolder=True)
	elif 'tenlua.vn' in href:
		addir(color['tenlua']+'TenLua[/COLOR]-%s'%name,href,img,fanart,mode=3,query=query)
	elif 'subscene.com' in href:
		addir(color['subscene']+'Subscene[/COLOR]-%s'%name,href,img,fanart,mode=94,query='download',isFolder=True)
	elif 'http://pubvn.' in href:
		addir(color['4share']+name+'[/COLOR]',href,img,fanart,mode=38,query=query,isFolder=True)
	elif 'http://vuahd.tv' in href:
		addir(color['vuahd']+name+'[/COLOR]',href,img,fanart,mode=38,query=query,isFolder=True)

def menuContext(name,link,img,fanart,mode,query,item,command=[]):
	if query.split('?')[0]=='Search':
		query=query.split('?')[1]
		command+=searchContext(name,link,img,fanart,mode)
	elif query.split('?')[0]=='ID':
		query=query.split('?')[1]
		command+=searchContext(name,link,img,fanart,15)
		command+=favouritesContext(name,link,img,fanart,mode)
	elif 'fshare.vn' in link or '4share.vn' in link or 'tenlua.vn' in link:#mode in (3,38,90,95):
		command+=favouritesContext(name,link,img,fanart,mode)
	elif myfolder in s2u(link):
		command+=make_myFile(name,link,img,fanart,mode,query)
	elif query in 'hdvietfolder-hdvietplay':
		command+=hdvietContext(name,link,img,fanart,mode)
	item.addContextMenuItems(command)
	return query

def makeContext(name,link,img,fanart,mode,query):
	if query=='Add to MyFshare favorite':make='AddFavorite'
	elif query=='Remove from MyFshare favorite':make='RemoveFavorite'
	elif query=='Remove All':make='Remove All'
	else:make=query.split()[0]
	if 'Rename' in make:colo=color['fshare']
	elif 'Remove' in make:colo=color['hdvietnam']
	else:colo=color['trangtiep']
	context=colo+query+'[/COLOR]'
	p=(myaddon.getAddonInfo('id'),mode,name,link,img,fanart,make)
	cmd='RunPlugin(plugin://%s/?mode=%d&name=%s&url=%s&img=%s&fanart=%s&query=%s)'%(p)
	return context,cmd

def hdvietContext(name,link,img,fanart,mode):
	context=color['trangtiep']+'Thêm vào phim yêu thích[/COLOR]'
	p=(myaddon.getAddonInfo('id'),mode,name,link.split('_')[0],img,fanart,'Themmucyeuthich')
	cmd='RunPlugin(plugin://%s/?mode=%d&name=%s&url=%s&img=%s&fanart=%s&query=%s)'%(p)
	command=[(context,cmd)]
	return command

def searchContext(name,link,img,fanart,mode):
	command=[(makeContext(name,link,img,fanart,9,'Rename item'))]
	command.append((makeContext(name,link,img,fanart,9,'Remove item')))
	command.append((makeContext(name,link,img,fanart,9,'Remove All')))
	return command

def favouritesContext(name,link,img,fanart,mode):
	def makecmd(mode,title):command.append((makeContext(name,link,img,fanart,mode,title)))
	command=[];link=u2s(link)
	if link in makerequest(joinpath(datapath,"favourites.xml")):	
		makecmd(98,'Rename in MyFavourites');makecmd(98,'Remove from MyFavourites')
	else:makecmd(98,'Add to MyFavourites')
	if 'www.fshare.vn' in link:
		if query=='MyFshare':makecmd(11,'Remove from MyFshare');makecmd(11,'Rename from MyFshare')
		else:makecmd(11,'Add to MyFshare')
		if query=='favorite':makecmd(11,'Remove from MyFshare favorite')
		else:makecmd(11,'Add to MyFshare favorite')
	if link in makerequest(joinpath(myfolder,'mylist.xml')):
		makecmd(12,'Rename in Mylist.xml');makecmd(12,'Remove from Mylist.xml')
	else:makecmd(12,'Add to Mylist.xml')
	command.append((makeContext(name,'addstring.xshare.vn',img,fanart,13,'Add item name to string search')))
	return command

def make_myFile(name,link,img,fanart,mode,query):
	name=re.sub('\[/?COLOR.*?\]|Fshare|4share|TenLua|List xml|-|:|"','',name).strip();command=[]
	if os.path.isfile(s2u(link)):
		command.append((makeContext(name,link,img,fanart,11,'Upload to MyFshare')));temp='file'
	else:temp='folder'
	command.append((makeContext(name,link,img,fanart,96,'Rename this %s'%temp)))
	command.append((makeContext(name,link,img,fanart,96,'Remove this %s'%temp)))
	return command

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

def make_myFshare(name,url,img,fanart,mode,query):#11
	def nameClean(s):
		return ' '.join(re.sub('\[/?COLOR.*?\]|\\\|/|:|\*|\?|\<|\>|\!|,|\@|\"|--|\.\.|\#|\$|\%|\^|\|','',s).split())
	
	myFshare=myaddon.getSetting('thumucrieng')
	from resources.lib.servers import fshare
	if query=='Add':
		fs=fshare(myaddon.getSetting('usernamef'),myaddon.getSetting('passwordf'),myFshare)
		name=nameClean(name);fs.myFshare_add(url,name);xbmc.sleep(1000)
	elif query=='Rename':
		fs=fshare();old_name=new_name='';
		new_name=get_input('Sửa tên 1 mục trong MyFshare',nameClean(name)).strip();new_name=nameClean(new_name)
		if not new_name or new_name==old_name:return
		else:new_name=url.split('/')[4].strip()+('FOLDER ' if 'folder' in url else 'FILE ')+new_name
		fs=fshare(myaddon.getSetting('usernamef'),myaddon.getSetting('passwordf'),myFshare)
		if fs.myFshare_rename(url,new_name):xbmc.executebuiltin("Container.Refresh")
	elif query=='Remove':
		fs=fshare(myaddon.getSetting('usernamef'),myaddon.getSetting('passwordf'),myFshare)
		if fs.myFshare_remove(url):xbmc.executebuiltin("Container.Refresh")
	elif query=='Upload':
		try:
			size=os.path.getsize(s2u(url));name=re.sub('\[/?COLOR.*?\]','',os.path.basename(url)).strip()
			if size>10*1024**2:mess(u'Add-on chưa hỗ trợ upload file>10MB!','myFshare');return
			f=open(s2u(url),'rb');content=f.read();f.close()
		except:mess(u'File read error','Fshare.vn');return
		fs=fshare(myaddon.getSetting('usernamef'),myaddon.getSetting('passwordf'),myFshare)
		fs.myFshare_upload(name,size,content)
	elif query=='AddFavorite':
		fs=fshare(myaddon.getSetting('usernamef'),myaddon.getSetting('passwordf'),myFshare)
		fs.Favorite_add(url)
	elif query=='RemoveFavorite':
		fs=fshare(myaddon.getSetting('usernamef'),myaddon.getSetting('passwordf'),myFshare)
		if fs.Favorite_remove(os.path.basename(url)):xbmc.executebuiltin("Container.Refresh")
	if fs.logged:fs.logout()
	return

def make_favourites(name,url,img,fanart,mode,query):
	favourites=joinpath(datapath,"favourites.xml");name=remove_tag(name)
	if query=='Add':
		if url.strip() in makerequest(favourites):mess(u'Mục này đã có trong MyFavourites!','MyFavourites');return
		if img==fanart:fanart=''
		string='<a href="%s" img="%s" fanart="%s">%s</a>\n'%(url.strip(),img,fanart,name)
		if makerequest(favourites,string,'a'):mess(u'Đã thêm 1 mục vào MyFavourites','MyFavourites')
		else:mess(u'Thêm 1 mục vào MyFavourites thất bại!','MyFavourites')
	elif query=='Rename':
		title = get_input('Sửa tên trong mục MyFavourites',name).strip()
		if not title or title==name:return 'no'
		body=makerequest(favourites)
		string=re.search('((<a href="%s" img=".*?" fanart=".*?">).+?</a>)'%(url),body)
		if string:
			body=body.replace(string.group(1),string.group(2)+title+'</a>')
			if makerequest(favourites,body,'w'):
				mess(u'Đã sửa 1 mục trong MyFavourites','MyFavourites')
				xbmc.executebuiltin("Container.Refresh")
			else:mess(u'Sửa 1 mục trong MyFavourites thất bại!','MyFavourites')
		else:mess(u'Sửa 1 mục trong MyFavourites thất bại!','MyFavourites')
	elif query=='Remove':
		body=makerequest(favourites);string=xsearch('(<a href="%s" img=".*?" fanart=".*?">.+?</a>)'%url,body)
		if string:
			body=body.replace(string+'\n','')
			if makerequest(favourites,body,'w'):
				mess(u'Đã xóa 1 mục trong xshare favourites','MyFavourites')
				xbmc.executebuiltin("Container.Refresh")
			else:mess(u'Xóa 1 mục trong xshare favourites thất bại!','MyFavourites')
		else:mess(u'Xóa 1 mục trong xshare favourites thất bại!','MyFavourites')
	else:
		items=re.findall('<a href="(.+?)" img="(.*?)" fanart="(.*?)">(.+?)</a>',makerequest(favourites))
		for href,img,fanart,name in items:addirs(name,href,img,fanart)
	return

def make_mylist(name,url,img,fanart,mode,query):
	mylist=joinpath(myfolder,'mylist.xml')
	name=re.sub('\[COLOR.{,12}\]|\[/COLOR\]|Fshare|4share|TenLua|List xml|-|:|"','',name).strip()
	if query=='Add':
		if url.strip() in makerequest(mylist):mess(u'Mục này đã có trong MyList!','MyList');return
		if img==fanart:fanart=''
		string='<a href="%s" img="%s" fanart="%s">%s</a>\n'%(url.strip(),img,fanart,name)
		if makerequest(mylist,string,'a'):mess(u'Đã thêm 1 mục vào mylist.xml','MyList')
		else:mess(u'Thêm vào mylist.xml thất bại!','MyList')
	elif query=='Rename':
		title = get_input('Sửa tên 1 mục trong mylist.xml',name)
		if not title or title==name:return 'no'
		string1='<a href="%s" img=".*?" fanart=".*?">.+?</a>'%url
		string2='<a href="%s" img=".*?" fanart=".*?">%s</a>'%(url,title)
		body=re.sub(string1,string2,makerequest(mylist))
		if makerequest(mylist,body,'w'):
			mess(u'Đã sửa 1 mục trong mylist.xml','MyList');xbmc.executebuiltin("Container.Refresh")
		else:mess(u'Sửa 1 mục trong mylist.xml thất bại!','MyList')
	elif query=='Remove':
		string='<a href="%s" img=".*?" fanart=".*?">.+?</a>\n'%url
		body=re.sub(string,'',makerequest(mylist))
		if makerequest(mylist,body,'w'):
			mess(u'Đã xóa 1 mục trong mylist.xml','MyList');xbmc.executebuiltin("Container.Refresh")
		else:mess(u'Xóa 1 mục trong mylist.xml thất bại!','MyList')
	return

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

def get_input(title=u"", default=u""):
	result = ''
	keyboard = xbmc.Keyboard(default, title)
	keyboard.doModal()
	if keyboard.isConfirmed():result = keyboard.getText().strip()
	else:result = ''
	return result

def tenlua_get_detail_and_starting(id,headers={'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'}):
	data='[{"a":"filemanager_builddownload_getinfo","n":"%s","r":0}]'%id
	response=make_post('https://api2.tenlua.vn/',headers,data,resp='j')
	try:json=response[0]
	except:json={'type':'none'}
	return json

def resolve_url(url,xml=False):
	urltemp=url.lower()
	if 'fshare.vn' in urltemp:result=fshare_resolve('https://www.%s'%xsearch('(fshare.vn.+?)\Z',url),xml)
	elif '4share.vn' in urltemp:result=fourshare_resolve(url)
	elif 'tenlua.vn' in urltemp:result=tenlua_resolve(url,xml)
	return result

def fshare_resolve(url,xml):
	from resources.lib.servers import fshare
	fs=fshare(myaddon.getSetting('usernamef'),myaddon.getSetting('passwordf'))
	if fs.logged is None:return 'fail'
	for loop in range(6):
		if loop>0:mess(u'Get link lần thứ %d'%(loop+1),'fshare.vn');xbmc.sleep(sleep);sleep+=1000
		direct_link=fs.get_maxlink(url)
		if direct_link=='fail':break
		elif direct_link:break
	fs.logout()
	if not direct_link:mess('Sorry! Potay.com','fshare.vn');return 'fail'
	elif direct_link in 'notfound-fail':return 'fail'
	elif xml:return direct_link
	else:return xshare_resolve(direct_link,os.path.splitext(direct_link)[1][1:].lower())

def fourshare_resolve(url):
	hd['Cookie']=login4share()
	if not hd['Cookie']:return 'fail'#login fail
	response=xread(url,hd);logout_site(hd['Cookie'],url)
	if not response:xbmc.sleep(2000);return 'fail'
	direct_link=xsearch("<a style='text-decoration:none' href='(.+?)'>",response)
	if not direct_link:
		direct_link=xsearch("Link Download.+?href='(.+?4share.vn.+?)'>",response)
		if not direct_link:
			direct_link=xsearch("'http.+\?info=.+)'",response)
			if not direct_link:
				mess(u'Không get được maxspeed link!','resolve_url');return 'fail'
	ext=os.path.splitext(xsearch('<title>(.+?)</title>',response))[1][1:].lower()
	return xshare_resolve(direct_link,ext)

def fourshare_resolve1(url):
	hd['Cookie']=login4share()
	if not hd['Cookie']:return 'fail'#login fail
	response=make_request(url,hd,resp='o');logout_site(hd['Cookie'],url)
	if not response or response.status!=200:xbmc.sleep(2000);return 'fail'
	direct_link=xsearch("<a style='text-decoration:none' href='(.+?)'>",response.body)
	if not direct_link:
		direct_link=xsearch("Link Download.+?href='(.+?4share.vn.+?)'>",response.body)
		if not direct_link:
			direct_link=xsearch("'http.+\?info=.+)'",response.body)
			if not direct_link:
				mess(u'Không get được maxspeed link!','resolve_url');return 'fail'
	ext=os.path.splitext(xsearch('<title>(.+?)</title>',response.body))[1][1:].lower()
	return xshare_resolve(direct_link,ext)

def tenlua_resolve(url,xml):
	hd['Cookie']=logintenlua();id=xsearch('\w{14,20}',url,0);direct_link=''
	if not id:id=url.split('/download/')[1].split('/')[0]
	download_info=tenlua_get_detail_and_starting(id,hd);print download_info
	filename=u2s(download_info.get('n',''))
	ext=os.path.splitext(filename)[1][1:].lower()
	size=int(download_info.get('real_size','0'))
	dlink=download_info.get('dlink','')
	if not dlink:
		dlink=download_info.get('url','');mess(u'Slowly direct link!','resolve_url')
		if not dlink:mess(u'Không get được max speed link!','resolve_url');return 'fail'
	response=make_request(dlink,hd,resp='o');logout_site(hd['Cookie'],url)
	if response and response.status==302:return xshare_resolve(response.headers['location'],ext)
	else:mess(u'Không get được max speed link!','resolve_url');return 'fail'

def xshare_resolve(direct_link,ext='',filmlabel=''):
	def get_detail_maxlink(direct_link):
		response=make_request(direct_link,{'User-Agent':'xshare'},resp='o')
		if not response:return 'fail'
		detail=response.headers
		size=int(detail.get('content-length',0))
		filename=detail.get('content-disposition','').split('=')
		if len(filename)>1:filename=filename[1].replace('"','').replace("'","")
		else:filename=os.path.basename(direct_link)
		ext=os.path.splitext(filename)[1][1:].lower()
		return response,size,filename,ext
	
	if ext in media_ext:xbmcsetResolvedUrl(direct_link,filmlabel);return ''
	#elif ext in ['srt','sub','txt','smi','ssa','ass','nfo']:xbmcsetResolvedUrl(direct_link,filmlabel);return ''
	
	response,size,filename,ext=get_detail_maxlink(direct_link)
	if ext in 'xml':result=doc_list_xml(direct_link,'list_xml')
	elif ext in media_ext or filmlabel:xbmcsetResolvedUrl(direct_link,filmlabel);result=''
	elif ext in ['rar','zip','srt','sub','txt','smi','ssa','ass','nfo']:
		result=xshare_download(response,size,filename,ext)
	elif not ext:mess('sorry! this is not a media file','Check media extention');result='fail'
	else:xbmcsetResolvedUrl(direct_link);result=''
	#mess('sorry! this is not a media file','xshare resolve');result='fail'
	return result

def xshare_download(response,size,filename,ext):
	def checkmedia(file):
		return os.path.isfile(file) and os.path.getsize(file)>1024**2 and os.path.splitext(file)[1][1:] in media_ext
	
	temp_path=joinpath(tempfolder,'temp');mediafile=False
	if not os.path.exists(temp_path):os.mkdir(temp_path)
	else:delete_folder(temp_path)
	tempfile=joinpath(temp_path,'tempfile.%s'%ext)
	
	if size<1024**2:#sub file
		if myaddon.getSetting('autodel_sub')=='true':delete_folder(subsfolder)
		content=makerequest(tempfile,response.body,"wb")
	elif size<2*1024**3:
		if size>1024**3:size_str='%d.%d GB'%(size/(1024**3),(size%(1024**3))/10**7)
		else:size_str='%d.%d MB'%(size/(1024**2),(size%(1024**2))/10**4)
		line1='[COLOR green]File: %s - %s[/COLOR]'%(filename,size_str)
		line2='Sẽ mất nhiều thời gian tải file vào "[B]Thư Mục Cục Bộ[/B]"!';content=''
		if size<100*1024**2 or  mess_yesno('xshare cảnh báo',line1,line2,'No - Không tải','Yes - Đồng Ý tải'):
			losslessfolder=joinpath(myfolder,'Lossless')
			if not os.path.exists(losslessfolder):os.mkdir(losslessfolder)
			if size>100*1024**2:endxbmc()
			f=open(tempfile,'wb');i=0;mess(u'Started Background download...',timeShown=50000);i=j=t=0;fn=''
			for chunk in response:
				f.write(chunk);i+=len(chunk)
				if i*10/size>j:j+=1;mess(u'Đã download được %d%%'%(j*10),timeShown=20000)
			f.close();mess(u'Đang Unzip...',timeShown=10000)
			xbmc.sleep(1000);xbmc.executebuiltin('XBMC.Extract("%s","%s")'%(tempfile,u2s(losslessfolder)),True)
			for filefullpath in folders(losslessfolder):
				if not checkmedia(filefullpath) and 'nrg' not in filefullpath:os.remove(filefullpath)
				elif os.path.getmtime(filefullpath)>t:fn=filefullpath;t=os.path.getmtime(fn)
			if fn and size<100*1024**2:#File nhỏ, gọi play
				xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=fn))
			mess(u'Đã download xong. Hãy mở Thư Mục Cục Bộ và thưởng thức tiếp nhé',timeShown=20000)
	else:mess(u'Sorry! Dung lượng file quá lớn. Chưa xử lý');content=''
	if not content:return 'no'
	sub_ext = [".srt", ".sub", ".txt", ".smi", ".ssa", ".ass"];sub_list=[];p=',|"|\''
	if content[0] in 'R-P':
		xbmc.sleep(1000);xbmc.executebuiltin('XBMC.Extract("%s")'%tempfile,True)
		for filefullpath in folders(temp_path):
			file=os.path.basename(filefullpath)
			if os.path.isfile(filefullpath) and os.path.splitext(filefullpath)[1] in sub_ext:
				if re.search('english|eng\.|\.eng',filename.lower()) and myaddon.getSetting('autotrans_sub')=='true':
					mess(u'Google đang dịch sub từ tiếng Anh sang tiếng Việt','Subs Downloader',timeShown=20000)
					filetemp=xshare_trans(filefullpath,filefullpath)
					if rename_file(filetemp,joinpath(subsfolder,'Vie.%s'%re.sub(p,'',file))):
						mess(u'Đã dịch xong sub từ tiếng Anh sang tiếng Việt','Subs Downloader')
					elif rename_file(filefullpath,joinpath(subsfolder,'Eng.%s'%re.sub(p,'',file))):
						mess(u'Không dịch được sub. Giữ nguyên bản tiếng Anh!','Subs Downloader') 
				elif re.search('english|eng\.|\.eng',filename.lower()) and rename_file(filefullpath,joinpath(subsfolder,'Eng.%s'%re.sub(p,'',file))):
					mess(u'Đã download sub vào Subsfolder','Subs Downloader') 
				elif re.search('vietnam|vie\.|\.vie',filename.lower()) and rename_file(filefullpath,joinpath(subsfolder,'Vie.%s'%re.sub(p,'',file))):
					mess(u'Đã download sub vào Subsfolder','Subs Downloader') 
				elif rename_file(filefullpath,joinpath(subsfolder,re.sub(',|"|\'','',file))):
					mess(u'Đã download sub vào Subsfolder','Subs Downloader') 
	elif rename_file(tempfile,joinpath(subsfolder,'Vie.%s'%filename)):
		mess(u'Đã download sub vào Subsfolder','Subs Downloader')
	return 'no'

def xshare_trans(fs,fd):
	def trans(s):
		try:s=s.decode('unicode_escape') if '\\' in s else s.decode('utf-8')
		except:pass
		return s

	f=open(fs);b=f.read();f.close();s='';S=''
	u='https://translate.googleapis.com/translate_a/single?ie=UTF-8&oe=UTF-8&client=gtx&sl=en&tl=vi&dt=t&q=%s'
	list_1=b.splitlines();list_2=[];rows=len(list_1);row=0
	hd={'Referer':'https://translate.google.com/','User-Agent':'Mozilla/5.0 (Windows NT 6.3) Chrome/49.0.2623.112 Safari/537.36','Cookie':''}
	for i in list_1:
		row+=1
		if re.search('[a-zA-Z]',i):s=s+' '+i+' xshare';list_2.append('xshare')
		else:list_2.append(i.strip())
		if len(s)>1000 or row==rows:
			mess(u'Google đã dịch %d %%'%(row*100/rows), timeShown=1500)
			s=' '.join(i for i in s.split())
			tran=make_request(u%urllib.quote(s),headers=hd,resp='o')
			if not hd['Cookie']:hd['Cookie']=tran.cookiestring
			xbmc.sleep(1000)#;print tran.body
			try:
				l=eval(tran.body.replace(',,,',',').replace(',,"en"',''))
				S=S+' '.join(i[0] for i in l[0])
			except:xbmc.executebuiltin("Dialog.Close(all, true)");return ''
			s=''
	s=' '.join(trans(i) for i in S.split())
	list_3=s.split('xshare');d=0;f=open(fd,'w')
	f.write('0\n00:00:00,000 --> 00:01:30,000\n[COLOR gold]Xshare dich Anh-->Viet bang Google translate[/COLOR]\n\n')
	for i in list_2:
		try:
			if i=='xshare':f.write(list_3[d].strip().encode('utf-8')+'\n');d+=1
			else:f.write(i+'\n')
		except:pass
	f.close();xbmc.executebuiltin("Dialog.Close(all, true)")
	return fd

def logout_site(cookie,url):
	def logout(cookie,url,site):
		hd['Cookie']=cookie
		mess(u'Logout %s %sthành công'%(site,'' if make_request(url,hd,resp='s')==302 else u'không '))
	if cookie and myaddon.getSetting('logoutf')=="true":
		if 'fshare.vn' in url.lower():logout(cookie,'https://www.fshare.vn/logout','Fshare.vn')
		elif '4share.vn' in url.lower():logout(cookie,'http://4share.vn/default/index/logout','4share.vn')
		elif 'dangcaphd.com' in url.lower():logout(cookie,'http://dangcaphd.com/logout.html','dangcaphd.com')
		elif 'tenlua.vn' in url.lower():logouttenlua(cookie)

def loginfshare(headers={'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'}):
	response=make_request("https://www.fshare.vn/login",resp='o');result=''
	if not response:mess(u'Lỗi kết nối Fshare.vn!','fshare.vn');return result
	fs_csrf=xsearch('value="(.+?)".*name="fs_csrf',response.body);headers['Cookie']=response.cookiestring
	username=myaddon.getSetting('usernamef');password=myaddon.getSetting('passwordf')
	form_fields = {"LoginForm[email]":username,"LoginForm[password]":password,"fs_csrf":fs_csrf}
	response=make_post("https://www.fshare.vn/login",headers,form_fields)
	if response.status==302:mess(u'Login thành công','Fshare.vn');result=response.cookiestring
	else:mess(u'Login không thành công!','Fshare.vn')
	return result

def login4share(headers={'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'}):
	form_fields = {"username":myaddon.getSetting('username4'),"password":myaddon.getSetting('password4')}
	response=make_post('http://up.4share.vn/index/login',headers,form_fields)
	if response and response.status==302:mess(u'Login thành công','4share.vn');f=response.cookiestring
	else:mess(u'Login không thành công!','4share.vn');f=''
	return f

def logintenlua(headers={'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'}):
	user=myaddon.getSetting('usernamet');pw=myaddon.getSetting('passwordt')
	data='[{"a":"user_login","user":"'+user+'","password":"'+pw+'","permanent":"true"}]'
	response=make_post('https://api2.tenlua.vn/',headers,data)
	if response and response.body!='[-1]':mess(u'Login thành công','tenlua.vn');f=response.headers.get('set-cookie')
	else:mess(u'Login không thành công!','tenlua.vn');f=''
	return f

def logouttenlua(cookie):
	hd['Cookie']=cookie
	response=make_post('https://api2.tenlua.vn/',hd,'a=user_logout')
	if response:mess(u'Logout thành công','tenlua.vn')
	else:mess(u'Logout không thành công!','tenlua.vn')

def hdvn_boss_room(url,body):
	if re.search('-\d{1,3}\.html',url):
		body=xread(re.sub('-\d{1,3}\.html','.html',url))
	pattern='id="postcount\d{5,8}" name="1">.{,1000}line popupctrl.{40,55}/\d{4,10}-(.+?).html"'
	return xsearch(pattern,body,1,re.DOTALL)

def hdvn_body_thanked(body,hd,bossroom):
	sec_token= xsearch('name="securitytoken" value="(.{50,60})"',body)
	home='http://www.hdvietnam.com/diendan/';thanks_data=[];content=''
	pattern='id="postcount(\d{5,8})".{,1000}line popupctrl.{40,55}/\d{4,10}-(.+?)\.html'
	items=re.findall(pattern,body,re.DOTALL);dataremove='do=post_thanks_remove_user&using_ajax=1'
	if not items:return''
	for id_post,name in items:
		if name==bossroom:
			data='do=post_thanks_add&using_ajax=1&p=%s&securitytoken=%s'%(id_post,sec_token)
			make_post(home+'post_thanks.php',hd,data)
			data='do=whatever&p=%s&all=%s&securitytoken=%s'%(id_post,id_post,sec_token)
			content+=make_post(home+'showthread.php',hd,data).body
			if not re.search('return post_thanks_remove_user.%s'%id_post,body):
				thanks_data.append('%s&p=%s&securitytoken=%s'%(dataremove,id_post,sec_token))
	for data in thanks_data:make_post(home+'post_thanks.php',hd,data)
	return content

def google_ifile(url,name,temp=[]):
	if 'http://ifile.tv/phim/' not in url:return temp
	mess(url)
	for url4share,fanart,name2,catalog in ifile_tv_4share(url):
		if not name2:name2=name
		if url4share not in temp:temp.append(url4share);addirs(name2,url4share,fanart,fanart)
	mess()
	return temp

def google_vaphim(url,temp=[]):
	if url=='http://vaphim.com/':return temp
	elif '/tag/' in url:
		pattern='class="entry-title"><a href="(.+?)" rel="bookmark"'
		url=xsearch(pattern,xread(url))
		if not url:return temp
	mess(url)
	for id,title,href,img,fanart,category in vp_2fshare(url):
		if href not in temp:temp.append(href);addirs(title,href,img,fanart)
	mess()
	return temp

def search_get_page(name,url,img,fanart,mode,page,query):
	if 'vaphim.com/' in url:
		if url=='http://vaphim.com/':return
		elif '/tag/' in url:
			pattern='class="entry-title"><a href="(.+?)" rel="bookmark"'
			url=xsearch(pattern,xread(url))
			if not url:return
		for id,title,href,img,fanart,category in vp_2fshare(url):
			addir_info(title,href,img,fanart)
	if '4share.vn/' in url.lower():
		for href,img,title,category in ifile_tv_4share(url):
			addir_info(title,href,img,fanart)
	if 'ifile.tv/' in url.lower():
		if 'http://ifile.tv/phim/' not in url:return 
		for url4share,fanart,name2,catalog in ifile_tv_4share(url):
			if not name2:name2=name
			addir_info(name2,url4share,fanart,fanart)

def google_search_api(url,start,string,items):#url:fshare.vn,4share.vn,tenlua.vn,hdvietnam.com
	string_search = urllib.quote_plus('"%s"'%string)
	href = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&rsz=large&'
	href+='start=%s&q=site:%s+%s'%(start,url.lower(),string_search)
	try:j=json.loads(xread(href))
	except:j=dict()
	#json=make_request(href,resp='j')
	if not j:return items,'end'
	if j.get('responseStatus')!=200 and myaddon.getSetting('googlesearch')=='API':
		mess(u'Google: nghi ngờ lạm dụng Dịch vụ. Tự động chuyển sang web search!','google_search_api')
		return google_search_web(url,start+'xshare',string,items)
	data=j.get('responseData',dict())
	if not data.get('results'):return items,'end'
	currentPage=int(data['cursor']['currentPageIndex'])+1;nextPage=0
	for item in data['results']:
		name=remove_tag(item['titleNoFormatting'])
		if len(name.split())<2:name=os.path.basename(item['url'])
		if 'tenlua' in url and not re.search('\w{14,20}/(.*)\Z',item['url']):continue
		elif not name or 'Forum' in name or 'server-nuoc-ngoai' in item['url']:continue
		elif 'chuyenlink.php' in item['url']:continue
		items.append((name,urllib.unquote(item['url'].encode('utf-8'))))
	start=str(int(start)+8)
	if start not in [s['start'] for s in data['cursor']['pages']]:start='end'
	return items,start

def google_search(url,query,mode,page,items=[]):
	srv=url.split('.')[0]
	if page==0:make_mySearch('',url,'','',mode,'get');return
	elif page==1:
		query=make_mySearch('',url,'','','','Input');page=2
		if query is None or not query.strip():return 'no'
	query=no_accent(query)
	if '?' in query:start=query.split('?')[1];query=query.split('?')[0]
	else:start='0'
	if myaddon.getSetting('googlesearch')=='Web' or 'xshare' in start:items,start=google_search_web(url,start,query,items)
	else:items,start=google_search_api(url,start,query,items)
	if len(items)<10 and start!='end' and myaddon.getSetting('googlesearch')=='API':
		return google_search(url,'%s?%s'%(query,start),mode,page,items)
	if not items and start=='end':mess(u'Không tìm thấy dữ liệu yêu cầu!','google_search');return 'no'
	for name,link in set(items):
		if url=='hdvietnam.com':addir_info(name,link,icon[srv],query='get_link_post')
		elif url=='vaphim.com':
			if '/tag/' not in link:addir_info(name,link,icon[srv],query='vp_getsubpage')
		else:addir_info(name,link,icon[srv])
	if start!='end':
		name=color['trangtiep']+'Trang tiep theo...trang %s[/COLOR]'%str(page-2)
		addir_info(name,url,icon[srv],'',mode,page+1,'%s?%s'%(query,start),True)
	return ''

def google_search_web(url,start,query,items):
	num='30';google = 'https://www.google.com.vn/search?hl=vi&ie=utf-8&oe=utf-8&num=%s&'%num
	#num='30';google = 'https://www.google.com.vn/search?hl=vi&num=%s&'%num
	string_search = urllib.quote_plus('"%s"'%query);srv=url.split('.')[0]
	if 'xshare' in start:start=start.replace('xshare','');xshare='yes'
	else:xshare=''
	href=google+'start=%s&q=site:%s+%s'%(start,url.lower(),string_search);print href
	
	hd['Cookie']=makerequest(joinpath(xsharefolder,'google.cookie'))
	cookie=urllib2.HTTPCookieProcessor();opener=urllib2.build_opener(cookie);urllib2.install_opener(opener)
	body=xread(href,hd)
	cookie=';'.join('%s=%s'%(i.name,i.value) for i in cookie.cookiejar)
	if checkupdate('google.cookie',hours=240,folder=xsharefolder) and cookie:
		makerequest(joinpath(xsharefolder,'google.cookie'),cookie,'w')

	if '<TITLE>302 Moved</TITLE>' in body and myaddon.getSetting('googlesearch')=='Web':
		mess(u'Google: nghi ngờ lạm dụng Dịch vụ. Tự động chuyển sang API search!','google_search_web')
		return google_search_api(url,start,query,items)

	if url=='fshare.vn':
		links=re.findall('<h3 class="r"><a href="(http.?://www.fshare.vn/.+?)".+?>(.+?)</a>',body)
		for link,name in links:
			items.append((remove_tag(unescape(name)),link.replace('http:','https:')))
	elif url=='vaphim.com':
		links=re.findall('<h3 class="r"><a href="(http://vaphim.com/.+?)".+?>(.+?)</a>',body)
		for link,name in links:
			items.append((remove_tag(unescape(name)),link.replace('http:','https:')))
	else:
		links=re.findall('<a href=".*?(http.+?)["|&].+?>(.+?)</a></h3>',body)
		for link,name in links:
			if 'tenlua.vn' in link and not re.search('\w{14,20}/(.*)\Z',link):continue
			elif not name or 'Forum' in name or 'server-nuoc-ngoai' in link:continue
			elif 'chuyenlink.php' in link:continue
			items.append((remove_tag(unescape(name)),link))
	start=str(int(start)+int(num))
	if 'start=%s'%start not in body:start='end'
	elif 'xshare':start=start+'xshare'
	return items,start

def main_menu(category,page,mode,query): #Doc list tu vaphim.xml hoac ifiletv.xml
	items = doc_xml(joinpath(datapath,query),para=category);pages=len(items)/rows+1
	del items[0:page*rows];count=0;down=len(items)
	for id,img,fanart,href,name in items:
		down-=1;addirs(name,href,img,fanart);count+=1
		if count>rows and down>10:break
	if down>10:
		page+=1;name=color['trangtiep']+'Trang tiep theo...trang %d/%d[/COLOR]'%(page+1,pages)
		addir(name,category,icon['icon'],mode=mode,page=page,query=query,isFolder=True)

def update_xml(items_new,items_old,filename): #update vaphim,ifiletv xml
	try:items = sorted(items_new+items_old,key=lambda l:int(l[1]),reverse=True)
	except:items = items_new+items_old
	contents='<?xml version="1.0" encoding="utf-8">\n'
	for id_tip,id_htm,category,img,fanart,href,fullname in items:
		content='<a id_tip="%s" id="%s" category="%s" img="%s" fanart="%s" href="%s">%s</a>\n'
		content=content%(id_tip,id_htm,category,img,fanart,href,fullname);contents+=content
	if makerequest(joinpath(datapath,filename),contents,'w'):
		mess(u'Đã cập nhật được %d phim'%len(items_new),'%s Auto update'%filename)
	else: mess(u'Đã xảy ra lỗi cập nhật!','%s Auto update'%filename)
	return

def vp_page(url,body=''):#id,name,href,img,category
	hd['Cookie']=makerequest(joinpath(xsharefolder,'vaphim.cookie'))
	pattern='<li class="post-(\d{4,6})(.+?)">.+?src="(.+?)".+?<h3 class="entry-title">'
	pattern+='<a href="(.+?)" rel="bookmark" >(.+?)</a>';items=[]
	if not body:body=xread(url,hd)
	for id,category,img,href,name in re.findall(pattern,body,re.DOTALL):
		category=' '.join(s.replace('category-','') for s in category.split() if 'category-' in s)
		if [s for s in ['game','video-clip','phn-mm','ebooks'] if s in category]:continue
		name=' '.join(s for s in re.sub('<.+?>|&.+?; ?','',name).split())
		items.append((id,name,href,img,category))
	return items

def vp_2fshare(url):#id,title,href,img,fanart,category
	hd['Cookie']=makerequest(joinpath(xsharefolder,'vaphim.cookie'))
	body=xread(url,hd)
	if not body:
		body=xread(url,hd)
		if not body:return list()
	
	items=list();id=xsearch("href='http://vaphim.com/\?p=(.+?)'",body)
	temp=xsearch('<div id=".+?" class="post-(.+?)">',body)
	category=' '.join(s.replace('category-','') for s in temp.split() if 'category-' in s)
	if not id or [s for s in category.split() if s in 'game video-clip phn-mm ebooks']:return items
	temp=xsearch('<title>(.+?)</title>',body)
	name=' '.join(s for s in re.sub('<.+?>|&.+?; ?|\||VaPhim.com','',temp).split())
	image=xsearch('meta property="og:image" content="(.+?)"',body)
	pattern='<a \w{4,6}=".*?(fshare.vn/f.l.?e?r?/.+?|http://subscene.+?)".{,18}>(.+?)</a><'
	if 'collection' not in category:
		content=xsearch('id="attachment_(.+?)"cf5_wpts_cl"',body,1,re.DOTALL)
		if not name:
			temp=xsearch('class="wp-caption-text">(.+?)<',content)
			name=' '.join(s for s in re.sub('<.+?>|&.+?; ?','',temp).split())
		temp=re.findall('src="(.+?\.jpg|.+?\.png).{,10}"',content)
		img=temp[0] if len(temp)>0 else image;fanart=temp[1] if len(temp)>1 else ''
		for href,title in re.findall(pattern,content):
			if '//' in title:title=''
			title=' '.join(s for s in re.sub('<.+?>|&.+?; ?','',title).split() if s not in name)
			title='.'.join(s for s in title.split('.') if s not in name)
			title=name+' '+title;href=href.replace('fshare.vn','https://www.fshare.vn')
			items.append((id,title,href,img,fanart,category))
	else:
		body=body[body.find('"content"'):]
		links=re.findall(pattern,body)
		if body.find('"text-align: center;"')>0:begin='"text-align: center;"' 
		elif body.find('<p><strong>')>0:begin='<p><strong>'
		elif body.find('id="attachment_')>0:begin='id="attachment_'
		elif body.find('"wordpress-post-tabs"')>0:begin='"wordpress-post-tabs"'
		else:begin='"section"'
		for content in re.findall('(%s.+?"cf5_wpts_cl")'%begin,body,re.DOTALL):
			temp=re.findall('src="(.+?\.jpg|.+?\.png).{,10}"',content)
			img=temp[0] if len(temp)>0 else image;fanart=temp[1] if len(temp)>1 else ''
			title=xsearch('<strong>(.+?)</strong>(</span></p>|</p>|<br />)',content)
			if not title:title=xsearch('"wp-caption-text">(.+?)<',content)
			title=name+' '.join(s for s in re.sub('<.+?>|&.+?; ?','',title).split() if s not in name)
			for href,fn in re.findall(pattern,content):
				fn=' '.join(s for s in re.sub('<.+?>|&.+?; ?','',fn).split() if s not in title)
				fn='.'.join(s for s in fn.split('.') if s not in title)
				fn=title+' '+fn;href=href.replace('fshare.vn','https://www.fshare.vn')
				items.append((id,fn,href,img,fanart,category))
		if len(items)<len(links):
			temp='-'.join(os.path.basename(s[2]) for s in items)
			for href,fn in links:
				if os.path.basename(href) in temp:continue
				if '//' in fn:fn=''
				fn=' '.join(s for s in re.sub('<.+?>|&.+?; ?','',fn).split() if s not in name)
				fn='.'.join(s for s in fn.split('.') if s not in name)
				fn=name+' '+fn;href=href.replace('fshare.vn','https://www.fshare.vn')
				items.append((id,fn,href,image,fanart,category))
	return items

def vp_update(auto=True):#vp_2fshare(url):id,title,href,img,fanart,category
	timenow=datetime.datetime.now().strftime('%Y%m%d%H')
	my_dict=json_rw('xshare.json');time_vp_update=my_dict.get('vp_update_time','0')
	if int(timenow)-int(time_vp_update)<1 and auto:return 'no'
	else:my_dict['vp_update_time']=timenow;my_dict=my_dict=json_rw('xshare.json',my_dict)
	items=vp_page('http://vaphim.com/category/phim-2/');hrefs=[];items_new=[]
	if not items:return 'no'
	ids=my_dict.get('vp_update_ids',list());mess(u'Vaphim updating ...',homnay)
	my_dict['vp_update_ids']=[s[0] for s in items];my_dict=json_rw('xshare.json',my_dict)
	items_old=doc_xml(joinpath(datapath,"vaphim.xml"));href_old=[s[5] for s in items_old]
	if auto:#update all in phim-2 page
		for href in [s[2] for s in items]:hrefs+=vp_2fshare(href)
	else:
		for href in [s[2] for s in items if s[0] not in ids]:
			mess('Vaphim updating...','vaphim.com');hrefs+=vp_2fshare(href)
	for id,title,href,img,fanart,category in [s for s in hrefs if s[2] not in href_old]:
		items_new.append(('',id,category,img,fanart,href,title))
	if items_new:update_xml(items_new,items_old,"vaphim.xml")
	else:mess(u'Không có phim mới...','Vaphim.com auto update')
	return 'ok'

def vp_list(name,url,img,mode,page,query):#92 query='phim-le'
	if url=='folder':
		items=list(set([s for s in doc_xml(joinpath(datapath,'vaphim.xml')) if s[1]==query]))
		for id_tip,id,category,img,fanart,href,name in items:addirs(name,href,img,fanart)
	elif url in 'vaphim.xml-collection':
		if url=='collection':query=url;url='vaphim.xml';page=1
		items=list(set([s for s in doc_xml(joinpath(datapath,'vaphim.xml')) if query in s[2]]))
		ids=list(set([s[1] for s in items]));ids.sort(reverse=True);pages=len(ids)/rows+1
		del ids[:(page-1)*rows];down=len(ids);del ids[rows:]
		for id in ids:vp_addir([s for s in items if s[1]==id])
		if down>rows:
			name=color['trangtiep']+'Trang tiep theo...trang %d/%d[/COLOR]'%(page+1,pages)
			addir(name,url,icon['icon'],mode=mode,page=page+1,query=query,isFolder=True)

def vp_addir(items):
	def namecolor(name):return '%s%s[/COLOR]'%(color['phimfshare'],name)
	if not items:return
	elif len(items)==1:
		for id_tip,id,category,img,fanart,href,name in items:addirs(name,href,img,fanart)
	else:
		id_tip,id,category,img,fanart,href,name=items[0]
		name='[COLOR goldenrod]'+subtitle_of_year(name).replace('(','')+'[/COLOR]'
		addir(name,'folder',img,fanart,92,1,id,True)
	
def vp_phimmoi():
	txtfile=joinpath(datapath,'vp_phimmoi.txt')
	if not os.path.isfile(txtfile):return
	ids=eval(makerequest(txtfile))
	items=[s for s in doc_xml(joinpath(datapath,'vaphim.xml')) if s[1] in ids]
	for id in ids:vp_addir([s for s in items if s[1]==id])

def vp_xemnhieu():
	txtfile=joinpath(datapath,'vp_xemnhieu.txt')
	if not os.path.isfile(txtfile):return
	names=eval(makerequest(txtfile))
	items=doc_xml(joinpath(datapath,'vaphim.xml'));i=0
	for name in names:vp_addir([s for s in items if name in s[6]])

def vp_chonloc():
	txtfile=joinpath(datapath,'vp_chonloc.txt')
	if not os.path.isfile(txtfile):return
	names=eval(makerequest(txtfile))
	items_xml=doc_xml(joinpath(datapath,"vaphim.xml"));ids=[s[1] for s in items_xml]
	for name in names:
		name=name.split('<br/>');nv=' '.join(s for s in re.sub('<.+?>|&.+?; ?','',name[0]).split())
		if len(name)<2:vp_addir([s for s in items_xml if nv in s[6]])
		else:ne=' '.join(s for s in name[1].split());vp_addir([s for s in items_xml if nv in s[6] or ne in s[6]])

def vp_make_datanew():
	hd['Cookie']=makerequest(joinpath(xsharefolder,'vaphim.cookie'))
	body=xread('http://vaphim.com/huong-dan-lay-rss-cua-vaphim-com/',hd)
	names=re.findall('<li><a href=".+?" title=".+?">(.+?)<',body)
	if names:makerequest(joinpath(datapath,'vp_xemnhieu.txt'),str(names),'w')
	items=re.findall('<li><a href="/category.+?/([\w-]+?)/">(.+?)</a></li>',body)
	if items:makerequest(joinpath(datapath,"vp_menu.txt"),str(items),'w')
	body=xread('http://vaphim.com/',hd)
	items=re.findall('"post-(\d{4,6})(.+?)"',body);items_new=[]
	for id,category in items:
		category=' '.join(s.replace('category-','') for s in category.split() if 'category-' in s)
		if not any(s for s in category.split() if s in 'game video-clip phn-mm ebooks'):items_new.append(id)
	if items_new:makerequest(joinpath(datapath,'vp_phimmoi.txt'),str(items_new),'w')
	items=re.findall('rel="bookmark">(.+?)</a>',body)
	if items:makerequest(joinpath(datapath,"vp_chonloc.txt"),str(items),'w')

def daklak47(name,url,img):
	reps = make_request(url)
	if reps.status==302:
		req=reps.headers['location']
		url = req.replace('http:','https:')
		if 'www.fshare.vn/folder/' in url:mess(u"Chưa xử lý trường hợp đọc folder trên 47daklak.com");return
		else:resolve_url(url)
	else: mess(u'Không tìm thấy link trên %s!'%s2u(url),'47daklak.com')

def ifile_home(name,url,img,mode,page,query):
	pattern='href=".+(\d{5}).+" class="mosaic-backdrop"'
	
	if url=="search":make_mySearch('','ifile.tv','','',mode,'get')
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		if query:return ifile_home(name,'ifile.tv',img,mode,page,query)
		else:return 'no'
	elif url=="ifile.tv":
		search_string = urllib.quote_plus(query)
		url='http://ifile.tv/search?search_string=%22'+urllib.quote_plus(query)+'%22&search_module=phim&time_sort=new'
		body=make_request(url,headers=hd)
		for img,href,title in re.findall("src='(.+?)'.+?href='(.+?)'>([^<]+?)</a></b>",body):
			if 'http://ifile.tv' not in href:href='http://ifile.tv'+href
			if 'http://ifile.tv' not in img:img='http://ifile.tv'+img
			title=' '.join(s for s in title.split())
			addir_info(title,href,img,'',mode,1,'film',True)
			
	elif url=="demo" or query=="demo":#ifile de nghi
		url='http://ifile.tv/phim/index' if url=="demo" else url
		body=make_request(url,headers=hd)
		for s in re.findall('("box-widget-grid fl-box".+?"film_tooltip")',body,re.DOTALL):
			href=xsearch('href="(.+?)"',s)
			if 'http://ifile.tv' not in href:href='http://ifile.tv'+href
			img=xsearch('src="(.+?)"',s)
			if 'http://ifile.tv' not in img:img='http://ifile.tv'+img
			title=xsearch("<a href='.+?'>(.+?)</a>",s).replace('<br>','').replace('<br/>','')
			title=' '.join(s for s in title.split())
			addir_info(title,href,img,'',mode,1,'film',True)
		return
		pattern='a href=".+(\d{5})\.htm">.*\s.*\s.*<img src=".+?" title=".+?"';query="demo"
	elif query=="film":
		body=make_request(url,headers=hd)
		
		for href,size in re.findall("link_down.+?href='([^<]+?)'>.+?<b>([^/]+?)</b>",body):
			title=name+' - '+size.strip();addirs(title,href,img,'')
		subs=xsearch("<b>Subtitle:</b>.+?href='([^<]+?)'>",body)
		if subs:addirs(name,subs,img,'')
		
		add_sep_item('----------Phim Cùng thể loại---------')
		for s in re.findall('(left_news_div_table.+?news_tooltip)',body,re.DOTALL):
			href=xsearch("<a href='(.+?)'>",s)
			if 'http://ifile.tv' not in href:href='http://ifile.tv'+href
			img=xsearch("src=.?'(.+?)'",s)
			if 'http://ifile.tv' not in img:img='http://ifile.tv'+img
			title=xsearch("<a href='.+?'>(.+?)</a>",s).replace('<br>','').replace('<br/>','')
			title=' '.join(s for s in title.split())
			addir_info(title,href,img,'',mode,1,'film',True)
			
	elif url=="index" or query=="index":#xem nhieu
		hd['Referer']='http://ifile.tv/phim/page/1' if url=="index" else url
		response=make_post('http://ifile.tv/phim/index/filter/type/special_filter',hd,'type=special_filter&filter_by_view_desc=1')
		hd['Cookie']=response.cookiestring;query='index';hd['Referer']=='http://ifile.tv/phim/index'
		url='http://ifile.tv/phim' if url=="index" else url
	elif url=="new":url='http://ifile.tv/phim'#Moi nhat
	body=make_request(url,headers=hd)
	id_new='-'.join(s for s in re.findall(pattern,body))
	for id_tip,id,category,img,fanart,href,name in doc_xml(joinpath(datapath,"ifiletv.xml")):
		if id in id_new:addirs(name,href,img,fanart)
	url=xsearch('<a href="(.+?)" title="Next"',body)
	if url and query!="demo":
		page=xsearch('/(\d{1,3})',url);trangcuoi=xsearch('<a href=".+?/(\d{1,3})" title="End"',body)
		name=color['trangtiep']+'Trang tiếp theo: trang %s/%s[/COLOR]'%(page,trangcuoi)
		addir(name,'http://ifile.tv%s'%url,img,fanart,mode,int(page),query,True)
		
def doc_list_xml(url,filename='',page=1):
	if page<2:
		items=doc_xml(url,filename=filename);page=1
		makerequest(joinpath(tempfolder,'temp.txt'),str(items),'w')
	else:f=open(joinpath(tempfolder,'temp.txt'));items=eval(f.readlines()[0]);f.close()
	pages=len(items)/rows+1
	del items[0:(page-1)*rows];count=0
	for id,href,img,fanart,name in items:
		if '47daklak.com' in href: addir(name,href,img,mode=47)
		else: addirs(name,href,img,fanart)
		count+=1
		if count>rows and len(items)>(rows+10):break
	if len(items)>(rows+10):
		name=color['trangtiep']+'Trang tiep theo...trang %d/%d[/COLOR]'%(page+1,pages)
		addir(name,url,iconpath+'khophim.png','',97,page+1,'',isFolder=True)

def doc_xml(url,filename='',para=''): 
	if (datapath in url) or (myfolder in s2u(url)):body=makerequest(url)
	elif filename=='list_xml':body=make_request(url)
	else:body=make_request(resolve_url(url,xml=True))

	if ('vaphim' in url) or ('ifiletv' in url) or ('phimfshare' in url) or ('hdvietnam' in url):
		if para and para[:6]=='search':
			string=para[7:].replace('(','.').replace(')','.')
			if ('phimfshare' in url) or ('hdvietnam' in url):
				r='href="(.+?)" img="(.+?)">(.*%s.*)</a>'%string
				items=[(s[1],s[1],s[0],s[2]) for s in re.findall(r,no_accent(body),re.IGNORECASE)]
			else:
				r='img="(.*?)" fanart="(.*?)" href="(.+?)">(.*%s.*)</a>'%string
				items=re.compile(r, re.I).findall(no_accent(body))
		else:
			if not para:r='<a id_tip="(.*?)" id="(.+?)" category="(.*?)" img="(.*?)" fanart="(.*?)" href="(.+?)">(.+?)</a>'
			else: #Doc theo category
				r='<a.*id="(.+?)" category=".*%s.*" img="(.*?)" fanart="(.*?)" href="(.+?)">(.+?)</a>'%para
			items = sorted(re.findall(r,body),key=lambda l:l[0], reverse=True)
	else:#Doc cac list xml khac
		r='<a.+id="(.*?)".+href="(.+?)".+img="(.*?)".+fanart="(.*?)".*>(.+?)</a>'
		items = re.compile(r).findall(body)
		if len(items)<1:items = re.findall('.+()href="(.+?)".+img="(.*?)".*()>(.+?)</a>',body)
		if len(items)<1:items = re.findall('.+()href="(.+?)".*()()>(.+?)</a>',body)
		if (myaddon.getSetting('copyxml')=="true") and ('http' in url) and (len(items)>0) :
			filename=re.sub('\.xml.*','.xml',filename.replace('[COLOR orange]List xml[/COLOR]-',''))
			filename=re.sub('\[.{1,10}\]','',filename);f_fullpath=joinpath(myfolder,filename)
			if not os.path.isfile(f_fullpath):
				string='<?xml version="1.0" encoding="utf-8">\n'
				for id,href,img,fanart,name in items:
					string+='<a id="%s" href="%s" img="%s" fanart="%s">%s</a>\n'%(id,href,img,fanart,name)
				if makerequest(f_fullpath,string,'w'):
					mess(u'Đã tải file %s vào MyFolder'%s2u(filename))
	return items

def fshare_page_file(url):
	body = make_request(url)
	name=clean_string(xsearch('<title>(.+?)</title>',body))
	if not name or 'Lỗi 404' in name:mess(u'Không tìm thấy nội dung quý khách yêu cầu!','fshare.vn');return 'no'
	size=xsearch('<i class="fa fa-hdd-o"></i>(.+?)</div>',body).strip()
	return name+' - '+size

def doc_TrangFshare(name,url,img,fanart,query=''):
	from resources.lib.servers import fshare
	if 'favorite' in url:fs=fshare(myaddon.getSetting('usernamef'),myaddon.getSetting('passwordf'))
	else:fs=fshare()
	folder_detail=fs.get_folder(url)
	for title,href,iD,size,date in sorted(folder_detail.get('items'), key=lambda k: k[0]):
		if 'file' in href and len(size)>3:title+=' - size:%s'%size
		addirs(title,href,img,fanart,query+'xml' if '.xml' in title.lower() else query)
	if fs.logged:fs.logout()
	return folder_detail['pagename']

def doc_Trang4share(url,temp=[]):#38
	if '4share.vn/d/' in url:
		response=xread(url)
		if '[Empty Folder]' in response:mess('Folder is empty','4share.vn');return temp
		pattern="<a href='(.+?)' target='.+?'><image src = '.+?'>(.+?)<.*?><td style='text-align: right'>(.+?)</td>"
		pattern+="|<a href='(.+?)'>.*\s.*<image src = '.+?'>(.+?)</a></div>"
		for href,name,size,folder_link,folder_name in re.findall(pattern,response):
			if href:name=name.strip()+' - '+size.strip();href='http://4share.vn'+href
			else:href='http://4share.vn'+folder_link;name=folder_name.strip()
			if href not in temp:temp.append((href));addirs(name,href)
	elif '4share.vn/f/' in url:
		name_size=re.search('Filename:.{,10}>(.+?)</strong>.{,20}>(.+?)</strong>',make_request(url))
		if name_size:
			name=name_size.group(1)+' - '+name_size.group(2)
			if url not in temp:temp.append((url));addirs(name,url)
	return temp

def doc_thumuccucbo(name,url,img,fanart,mode,query):
	if url=='thumuccucbo':url=myfolder
	url=s2u(url)
	if query=='Remove':
		if os.path.isfile(url):
			try:os.remove(url);mess(u'Đã xóa file: %s'%s2u(url),'MyFolder');xbmc.executebuiltin("Container.Refresh")
			except:mess(u'Lỗi xóa file!','MyFolder')
		else:
			import shutil
			try:shutil.rmtree(url);mess(u'Đã xóa thư mục: %s'%s2u(url),'MyFolder');xbmc.executebuiltin("Container.Refresh")
			except:mess(u'Lỗi xóa thư mục!','MyFolder')
	elif query=='Rename':
		name=s2u(os.path.basename(url))
		name_new = get_input('xshare - Rename file/folder (chú ý phần mở rộng)',name)
		if name_new and name_new!=name:
			if rename_file(url,joinpath(os.path.dirname(url),name_new)):
				mess(u'Đã đổi tên file/folder: %s'%s2u(url),'MyFolder');xbmc.executebuiltin("Container.Refresh")
			else:mess(u'Lỗi Rename file/folder!','MyFolder')
	elif myfolder in url and query!='file':
		for filename in os.listdir(url):
			filenamefullpath = u2s(joinpath(url, filename));filename= u2s(filename)
			size=os.path.getsize(joinpath(url, filename))/1024
			if size>1024:size='%dMB'%(size/1024)
			else:size='%dKB'%size
			label=filename+' - %s'%size
			if os.path.isfile(joinpath(url, filename)):
				file_ext=os.path.splitext(filenamefullpath)[1][1:].lower()
				if file_ext in media_ext:
					item = xbmcgui.ListItem(label, iconImage=icon['khophim'])
					query=menuContext(label,filenamefullpath,'','',mode,query,item)
					xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=filenamefullpath,listitem=item)
				elif file_ext=='xml':addirs(label,filenamefullpath,icon['khophim'],query='xml')
				else:addirs(label,filenamefullpath,query='file')
			else:
				name='%s%s[/COLOR]'%(color['trangtiep'],filename)
				addir(name,filenamefullpath,icon['icon'],'',mode,1,filenamefullpath,True)
		return
	else:mess(u'Chưa xử lý kiểu file này','MyFolder')
	return 'no'

def play_maxspeed_link(url):
	if not url or url=='Maxlink':
		maxlink=get_input('Hãy nhập max speed link của Fshare, 4share hoặc tênlửa')
		if not maxlink or not maxlink.strip():return 'no'
		url=maxlink.replace(' ','')
	elif len(url)<13:
		fsend=getFsend(url)
		if fsend:url=fsend[0][1]
		else:mess(u'Lỗi get Fsend!','play_maxspeed_link');return 'no'
	return xshare_resolve(url,filmlabel='Maxlink')

def getFsend(id):
	response=make_request('http://fsend.vn/'+id,hd,'o')#http://fsend.vn/2LJL4GPVZ48L file XXOA5LADP6FC folder
	hd['Cookie']=response.cookiestring
	token=xsearch('"(.+?)"',urllib.unquote(response.cookiestring))
	data={"fs_csrf":"%s"%token,"DownloadForm[speed]":"slow","ajax":"download-form","undefined":"undefined"}
	resp=make_post('http://fsend.vn/default/download',data=urllib.urlencode(data),headers=hd)
	if resp.status==200:
		try:json=resp.json
		except:json=''
	else:json=''
	if json and json['code']==200:items=[(os.path.basename(json['url']),json['url'],'')]
	elif json and json['code']==400:
		pattern='avatar. title="(.+?)".+?<p><b>(.+?)</b></p>.+?<a href="/(.+?)"';items=[]
		for title,size,id in re.findall(pattern,response.body,re.DOTALL):items.append((title,size,id))
	else:items=[]
	return items

def tenlua_getlink(href):
	idf=xsearch('\w{14,20}',href,0)
	if not idf:return
	response=tenlua_get_detail_and_starting(idf)
	if response["type"]=="file":
		name=response['n'].encode('utf-8');url="https://www.tenlua.vn/download/"+idf
		addir(name,url,mode=3)
	elif response["type"]=="folder":
		for item in response['content']:
			tenlua_getlink(item['link'])

def id_2url(name,url,img,mode,page,query):
	def check_id_tenlua(id):
		mess('ID Checking on Tenlua.vn','',1000)
		response=tenlua_get_detail_and_starting(id);title='';img=icon['tenlua']
		if response["type"]=="file":title=response['n'];href="https://www.tenlua.vn/download/"+id
		elif response["type"]=="folder":title=response["folder_name"];href="https://www.tenlua.vn/fm/folder/"+id
		if title:return title,href,img
		else:return '','',''
	def check_id_4share(id):
		mess('ID Checking on 4share.vn','',1000)
		href='http://4share.vn/f/%s/'%id;title='';img=icon['4share']
		item=re.search('<center>.+?<strong>(.+?)</strong>.+?<strong>(.+?)</strong></center>',make_request(href))
		if item:title=item.group(1)+' - '+item.group(2)
		else:
			href='http://4share.vn/d/%s/'%id
			item=re.search("<br/><b>(.+?)</b>|<a href='(/f/\w+)|<a href='(/d/\w+)'>",make_request(href))
			if item:title,href,img=item.group(1),item.group(2),item.group(3)
		if title:return title,href,img
		else:return '','',''
	def check_id_internal(id):
		mess('ID Checking on xshare.vn','',1000)
		r1='href="(.+%s.*)" img="(.*?)">(.+?)</a>';r2='img="(.*?)" fanart=".*?" href="(.+%s.*)">(.+?)</a>'
		files='phimfshare.xml-hdvietnam.xml';title=''
		for file in ['vaphim.xml','ifiletv.xml','phimfshare.xml','hdvietnam.xml']:
			body=makerequest(joinpath(datapath,file));id=id.lower() if len(id)>13 else id
			items=re.search(r1%id,body) if file in files else re.search(r2%id,body)
			if items:
				title=items.group(3)
				href=items.group(1 if file in files else 2)
				img=items.group(2 if file in files else 1);break
		if title:return title,href,img
		else:return '','',''
	def check_id_fshare(id):
		mess('ID Checking on Fshare.vn','',1000)
		href='https://www.fshare.vn/file/%s'%id;body=make_request(href);title=''
		if 'class="file-info"' in body:title=xsearch('<title>(.+?)</title>',body).replace('Fshare - ','')
		else:
			href='https://www.fshare.vn/folder/%s'%id
			body=make_request(href)
			if 'class="filename"' in body:title=xsearch('<title>(.+?)</title>',body).replace('Fshare - ','')
		if title:return title,href,icon['fshare']
		else:return '','',''
	
	if query=='MyFshare':query=thumucrieng;page=4
	if page==0:
		name=color['search']+'Nhập ID/link:[/COLOR] %sFshare/Fsend[/COLOR]/%s4share[/COLOR]/%stenlua[/COLOR] hoặc link %ssubscene[/COLOR]'%(color['fshare'],color['4share'],color['tenlua'],color['subscene'])
		addir(name,url,icon['icon'],mode=mode,query=query,page=1,isFolder=True)
		for href,name in re.findall('<a href="(.+?)">(.+?)</a>',makerequest(search_file)):
			q='ID?xml' if '.xml' in name else 'ID?'+query
			addirs(name,href,icon['id'],query=q)
	elif page == 1:#Nhập ID mới BIDXFYDOZMWF
		idf = get_input('Hãy nhập chuỗi ID của Fshare/4share/tenlua Hoặc fulllink subscene')#;record=[]
		if idf is None or idf.strip()=='':return 'no'
		if 'subscene.com' in idf:return subscene(name,''.join(s for s in idf.split()),'subscene.com')
		idf = xsearch('(\w{10,20})',''.join(s for s in idf.split()).upper())
		if len(idf)<10:mess(u'Bạn nhập ID link chưa đúng: %s!'%idf);return 'no'
		title,href,img=check_id_internal(idf)
		if not title:# or True:
			title,href,img=check_id_fshare(idf)
			if not title:
				title,href,img=check_id_4share(idf)
				if not title:title,href,img=check_id_tenlua(idf)
		if title and href:make_mySearch(title,href,img,'',mode,'Add');addirs(title,href,img)
		else:mess(u'Không tìm được link có ID: %s!'%idf);return 'no'
	elif page == 4:#Mở thư mục chia sẻ trên Fshare
		title=color['search']+"Mục Link yêu thích của tôi trên Fshare (My fshare favorite)[/COLOR]"
		addir(title,"https://www.fshare.vn/files/favorite",img,fanart,mode=90,query='favorite',isFolder=True)
		doc_TrangFshare(name,query,iconpath+'fshare.png','')
	return ''

def ifile_tv_page(url):
	items=[]
	try: 
		pattern='id="(\d{,6})".{,300}<a href="(.+?)".{,300}src="(.+?)".{,300}"red">(.+?)</font>'
		item = re.compile(pattern,re.DOTALL).findall(make_request(url))
		for id_tip,href,img,name in item:
			http='http://ifile.tv';href=http+href;id_htm=href.rsplit('.')[2];img=http+img;name=name.strip()
			items.append((id_tip,id_htm,href,img,name))
	except:print 'ifile_tv_page Error: '+ url
	return items #id_tip,id_htm,href,img,name

def ifile_tv_4share(url):
	items = []
	body = make_request(url)
	pattern="href='/(.+?)'>.+?</a></u>|<div class='arrow_news'> <a.+>(.+?)</a>|<img src= '(.+?)' style='width: 100%'>"
	pattern+="|<b>(.+?)</b><br/><b>|<b>(http://4share.vn.+?)</b>.{,20}<b>(.+?)</b>"
	pattern+="|href='(http://subscene.com/subtitles/.+?)'"
	category=name=img=''
	for c,n1,i,n2,url4share,size,urlsubscene in re.findall(pattern,body):
		category+=xsearch('phim/(.+?)\.\d{,6}',c)+' '
		if n1:name=n1
		if n2 and not name:name=n2
		if i:img=i
		if url4share and url4share not in items:
			category=' '.join(s for s in category.split())
			name=clean_string(name)+' - '+size;url4share=urllib.unquote(url4share)
			items.append((url4share,'http://ifile.tv'+img,name,category))
		if urlsubscene and urlsubscene not in items:
			category=' '.join(s for s in category.split())
			name=clean_string(name)+' - '+size;urlsubscene=urllib.unquote(urlsubscene)
			items.append((urlsubscene,'http://ifile.tv'+img,name,category))
	return items

def ifile_update():
	mess(u'Ifile.tv auto updating ...',homnay)
	items_old=doc_xml(joinpath(datapath,"ifiletv.xml"));id_old=[s[1] for s in items_old]
	items_new = []#id_tip,id_htm,href,img,name
	for id_tip,id_htm,href,img,name in ifile_tv_page('http://ifile.tv/') :
		if id_htm not in id_old:
			for url4share,fanart,name2,catalog in ifile_tv_4share(href):
				fullname=name2 if name in name2 else name
				fullname=' '.join(s for s in fullname.split())
				items_new.append((id_tip,id_htm,catalog,img,fanart,url4share,fullname))
	if items_new:update_xml(items_new,items_old,"ifiletv.xml")
	else:mess(u'Không có phim mới...','Ifile.tv auto update')
	return 'ok'

def read_all_filexml(fn="vaphim.xml",string_search='',lists=[],index=[]):
	if string_search:lists=lists+doc_xml(joinpath(datapath,fn),para='search:'+string_search)
	else:lists=lists+doc_xml(joinpath(datapath,fn))
	if not string_search:
		for id_tip,id_htm,category,img,fanart,url,name in lists:index.append((id_htm))
	return lists,index

def googleapis_search(url,query,mode):
	if '?' not in query:start='0'
	else:start=query.split('?')[1];query=query.split('?')[0]
	if url=='hdvietnam.com':url_search='https://www.googleapis.com/customsearch/v1element?rsz=filtered_cse&num=20&key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&source=gcsc&gss=.com&cx=006389339354059003744:dxv8n47myyg&googlehost=www.google.com&sig=23952f7483f1bca4119a89c020d13def&nocache&start=%s&q=%s';ico=icon['hdvietnam']
	elif url=='phimfshare.com':url_search='https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=20&hl=vi&prettyPrint=false&source=gcsc&gss=.com&googlehost=www.google.com&sig=23952f7483f1bca4119a89c020d13def&cx=005609294674567689888:qyuk9aoqwmg&nocache&start=%s&q=%s';ico=icon['phimfshare']
	else:return list()
	url_search=url_search%(start,urllib.quote_plus(query))
	result=make_request(url_search,resp='j');items=list()
	if not result:return list()
	for item in result.get("results",dict()):
		href=urllib.unquote(item.get('url'))
		if not href:continue
		name=remove_tag(item.get('titleNoFormatting'))
		if len(name.split())<2:name=os.path.basename(item['url'])
		img=get_dict(item,['richSnippet','cseThumbnail','src'])
		if not img:img=ico
		fanart=get_dict(item,['richSnippet','cseImage','src'])
		items.append((name,href,img,fanart,0,1,'get_link_post'))
	page_dict=get_dict(result,['cursor','pages']);label=list();pages=0
	if page_dict:label=[s.get('label') for s in page_dict if s.get('start')==start]
	if label:label=label[0]+1;start=[s.get('start') for s in page_dict if s.get('label')==label]
	for item in page_dict:pages=item.get('label') if item.get('label',0)>pages else pages
	if label and start:
		label=color['trangtiep']+'Trang tiep theo...trang %d/%d[/COLOR]'%(label,pages)
		items.append((label,url,ico,'',mode,4,query+'?'+start[0]))
	return items

def xshare_search(name,url,query,mode,page,items=[]):#13
	def trang_search(string):
		if len(string.split('?'))==3:p=string.split('?')[2];trang=string.split('?')[1];string=string.split('?')[0]
		elif len(string.split('?'))==2:p=1;trang=string.split('?')[1];string=string.split('?')[0]
		else:p=trang='1'
		return string,trang,p

	if url=='addstring.xshare.vn' or query=='Add':
		name=remove_tag(name)
		if not re.search(name,makerequest(search_file)):
			makerequest(search_file,'<a>%s</a>\n'%name,'a')
			mess(u'Đã thêm tên phim này vào DS tìm kiếm')
	elif page==0:make_mySearch('',url,'','',mode,'get');return
	elif page==1:
		query=make_mySearch('',url,'','','','Input');page=2
		if query is None or not query.strip():return 'no'
	query=no_accent(query)
	
	if url=='vaphim.com':#print_dict(mp('http://vaphim.com/fast-search.php',data='term=hur+jun',resp='j'))
		query,trang,p=trang_search(query);hd['Cookie']=makerequest(joinpath(xsharefolder,'vaphim.cookie'))
		url_search='http://vaphim.com/page/%s/?s=%s'%(trang,urllib.quote_plus(query))
		#body=make_request(url_search,hd)
		body=xread(url_search,hd)
		items=vp_page(url_search,body)#id,name,href,img,category
		if not items:mess(u'Không tìm được tên phim phù hợp!','vaphim.com search');return 'no'
		for id,name,href,img,category in items:
			addir_info(name,href,img,query='vp_getsubpage')
		page_tag=re.search("class='pages'>(.+?)<.+span><a href='(.+?)' class='page larger'>(\d{,3})</a>",body)
		if page_tag:
			trang=str(int(trang)+1)
			name=color['trangtiep']+'Tiep theo %s...trang %s[/COLOR]'%(page_tag.group(1),page_tag.group(3))
			addir_info(name,url,icon[url.split('.')[0]],'',mode,4,'%s?%s?%s'%(query,trang,p),True)
	
	elif url in 'phimfshare.com hdvietnam.com':
		items=googleapis_search(url,query,mode)
		if not items:return
		for name,url,img,fanart,mode,page,query in items:
			addir_info(name,url,img,fanart,mode,page,query)
	
	elif url=='tenlua.vn':#get_dict(dict,key_list=list(),result='')
		query,trang,p=trang_search(query)
		href='https://api2.tenlua.vn/search?keyword=%s&page=%s'%(urllib.quote_plus("%s"%query),trang)
		dict=make_request(href,resp='j')
		if int(get_dict(dict,['pagging','total'],'0'))==0:
			mess(u'Không tìm được tên phim phù hợp!','tenlua search');return 'no'
		for item in dict.get('items',{}):
			if item is None or item.get('ext','no') not in media_ext:continue
			id=item.get('h')
			link=tenlua_get_detail_and_starting(id)
			if link.get('type')=="none":continue
			elif link.get('type')=="file":name=link['n'];href="https://www.tenlua.vn/download/%s"%id
			elif link.get('type')=="folder":name=link["folder_name"];href="https://www.tenlua.vn/fm/folder/%s"%id
			if href not in items:items.append(href);addir_info(name,href,icon['tenlua'])
		trang=str(int(trang)+1)
		if int(get_dict(dict,['pagging','pages'],'0'))>=int(trang) and len(items)<10 and int(trang)%15>0:
			return xshare_search(name,url,'%s?%s?%s'%(query,trang,p),mode,page,items)
		p=str(int(p)+1)
		if int(get_dict(dict,['pagging','pages'],'0'))>=int(trang):
			name=color['trangtiep']+'Trang tiep theo...trang %s[/COLOR]'%p
			addir_info(name,url,icon['tenlua'],'',mode,4,'%s?%s?%s'%(query,trang,p),True)
	
	elif '4share.vn' in url:
		def ext_media(url):return os.path.splitext(url)[1][1:].lower().strip() in media_ext
		if url=='4share.vn':url='http://4share.vn/search?search_string='+urllib.quote_plus(query)
		pattern="<a href='(.+?)' target='_blank' title='(.+?)'>.+?</a>"
		body=xread(url);items=[s for s in re.findall(pattern,body) if ext_media(s[0])]
		if not items:mess(u'Không tìm thấy dữ liệu yêu cầu!','xshare_search');return 'no'
		for href,title in items:addir_info(title,href.split()[0],icon['4share'])
		next=xsearch("<a href='([^<]+?)'> Next</a>",body)
		if next:
			title=color['trangtiep']+'Trang tiep theo...trang %s[/COLOR]'%xsearch('\?page=(\d{1,3})&',next)
			addir_info(title,'http://4share.vn'+next.replace(' ','+'),icon['4share'],'',mode,4,'',True)
	
	elif url=='ifile.tv':
		query,trang,p=trang_search(query)	
		url_search = 'http://ifile.tv/search?search_module=phim&search_name=1&'
		url_search += 'search_content=1&time_sort=new&search_string="%s"'%urllib.quote_plus(query)
		items = []
		for content in re.findall("<td>(.*?)</b>",xread(url_search)):
			items+=re.findall("<a.+href='(.+?)'.+src='(.+?)'.+(\d{5}).+>(.+?)</a>",content)
		if not items:mess(u'Không tìm được tên phim phù hợp!','Ifile.tv search');return 'no'
		items_xml,id_xml = read_all_filexml(fn="ifiletv.xml")
		for href,img,id_htm,name in items:
			if id_htm in id_xml:
				index = id_xml.index(id_htm)
				while id_xml[index] == id_htm:
					temp.append((items_xml[index]));index +=1 
			else:
				for url4share,fanart,name2,catalog in ifile_tv_4share('http://ifile.tv'+href):
					temp.append(('',id_htm,catalog,img,fanart,url4share,name))
		for id_tip,id_htm,catalog,img,fanart,href,name in temp:addir_info(name,href,img,fanart)
	
	elif url=='xshare.vn':
		query,trang,p=trang_search(query);items=[]
		if trang=='1':
			for fn in ['vaphim.xml','ifiletv.xml','phimfshare.xml','hdvietnam.xml']:
				items,index=read_all_filexml(fn=fn,string_search=".*".join(query.split()),lists=items)
			items=sorted(items,key=lambda l:no_accent(l[3]).lower());p=str(len(items))
			if not items:mess(u'Không tìm thấy phim nào có chuổi phù hợp!','Xshare search');return
			if len(items)>(rows+rows/2):makerequest(joinpath(data_path,'temp.txt'),str(items),'w')
		else:f=open(joinpath(data_path,'temp.txt'));items=eval(f.readlines()[0]);f.close()
		trang=int(trang);del items[:rows*(trang-1)]
		if len(items)>(rows+rows/2):
			del items[rows:];trang=str(trang+1)
		else:trang=''
		for img,fanart,href,name in items:addir_info(name,href,img,fanart)
		if trang:
			name=color['trangtiep']+'Trang tiep theo...trang %s/%s[/COLOR]'%(trang,str(int(p)/rows+1))
			addir_info(name,url,icon['icon'],'',mode,4,'%s?%s?%s'%(query,trang,p),True)

	elif 'taifile.net' in url:
		def taifile_search(url):
			q=xread(url);vp=[]
			for s in re.findall('(<div class="bgframe">.+?</a></div></div>)',q):
				if not 'fshare.vn' in s:continue
				title=xsearch('title="(.+?)"',s)
				size=xsearch('Size: <b>(.+?)</b>',s)
				title='[COLOR gold]Fshare[/COLOR] '+title.replace('Download ','')+ ' - '+size
				href='http://www.taifile.net'+xsearch('href="(/x.php\?id=.+?)"',q)
				link=xsearch('href="(http://vaphim.com[^<]+?)"',s)
				label=xsearch('title="([^"]+?)" target',s)
				addir_info(title,href,icon['taifile'],'',mode,4,'play')
				if link and link not in str(vp):vp.append((link,label))

			for link,label in vp:
				addir_info('[COLOR gold]'+label+'[/COLOR]',link,icon['vaphim'],'',1,1,'vp_getsubpage',True)

			pn=re.search('<a class="active" href="[^<]+?">\d+?</a><a href="([^<]+?)">(\d+?)</a>',q)
			if pn:
				href=pn.group(1).replace('amp;','').replace('/search.php?q=','')
				href='http://www.taifile.net/search.php?q='+'%20'.join(s for s in href.split())
				title=color['trangtiep']+' Trang tiep theo...trang %s[/COLOR]'%pn.group(2)
				addir_info(title,href,icon['taifile'],'',mode,4,'search',True)
		
		if query=='search':taifile_search(url)
		elif query=='play':
			b=make_request(url,resp='o')
			if b and b.getheader('location'):resolve_url(b.getheader('location'))
		else:
			b=make_post('http://www.taifile.net/suggest.php',data={'q':query},resp='j')
			if not b or len(b)<2:
				href='http://www.taifile.net/search.php?&host=fshare&q='+urllib.quote_plus(query)
				taifile_search(href)
			else:
				if '/search.php?q='+query not in b:b[query]=query
				for i in b:
					title='[COLOR lime]Search on:[/COLOR] '+' '.join(s for s in re.sub('<.*?>|\[.*?\]|\(.*?\)','',b.get(i)).split())
					href='http://www.taifile.net/search.php?&host=fshare&q='+urllib.quote(i.replace('/search.php?q=',''))
					addir_info(title,href,icon['taifile'],'',mode,4,'search',True)
	return ''

def pfs_update():
	timenow=datetime.datetime.now().strftime('%Y%m%d%H')
	my_dict=json_rw('xshare.json');pfs_update_time=my_dict.get('pfs_update_time','0')
	if int(timenow)-int(pfs_update_time)<5:return
	else:my_dict['pfs_update_time']=timenow;my_dict=json_rw('xshare.json',my_dict)
	mess(u'PhimFshare.com auto updating ...',homnay)
	body=make_request('http://phimfshare.com/external.php?type=RSS2');items=list()
	if not body:return
	phimfshare=makerequest(joinpath(datapath,'phimfshare.xml'));string='';count=0
	for item in re.findall('<item>(.+?)</item>',body,re.DOTALL):
		id=xsearch('<link>.*-(\d{5,6})/.*</link>',item)
		if not id:continue
		title=re.sub('<!\[CDATA\[|\]\]>','',xsearch('<title>(.+?)</title>',item))
		img=xsearch('img src="(.+?jpg)["|?| ]',item)
		content=xsearch('<content:encoded>(.+?)</content:encoded>',item,1,re.DOTALL)
		pattern='(https?://www.fshare.vn/\w{4,6}/\w{10,14}|http://4share.vn/./\w{14,20}|https?://w?w?w?/?tenlua.vn/.*?|http://subscene.com/subtitles/.+?)[ |"|\'|<]'
		for href in list(set([s for s in re.findall(pattern,content) if '..' not in s])):
			href=correct_link(href);server=xsearch('(\w{6,8})\.[v|c]',href)
			if href not in phimfshare:
				string+='<a id="%s" server="%s" href="%s" img="%s">%s</a>\n'%(id,server,href,img,title);count+=1
	if string:
		mess(u'Đã cập nhật được %d phim'%count,'Phimfshare auto update')
		makerequest(joinpath(datapath,'phimfshare.xml'),string,'a')
	else:mess(u'Không có phim mới','Phimfshare auto update')

def pfs_getlink(content):#6+
	items=[]
	pattern='(https?://www.fshare.vn/\w{4,6}/\w{10,14})|(http://4share.vn/./\w{14,20})|(https?://w?w?w?/?tenlua.vn/.*?)[ |"|<]'
	for links in re.findall(pattern,content):
		if links:
			for link in links:
				idf=xsearch('(\w{10,20})',link)
				if idf:
					link=link.lower()
					if 'fshare.vn/file' in link:url='https://www.fshare.vn/file/%s'%idf.upper();server="fshare"
					elif 'fshare.vn/folder' in link:url='https://www.fshare.vn/folder/%s'%idf.upper();server="fshare"
					elif 'tenlua.vn' in link and ('folder/' in link or '#download' in link) and len(idf)>16:
						url='https://tenlua.vn/fm/folder/%s'%idf;server="tenlua"
					elif 'tenlua.vn' in link and len(idf)>16:url='https://tenlua.vn/download/%s'%idf;server="tenlua"
					elif '4share.vn' in link:url=link;server="4share"
					else:continue
					items.append((server,url))
	return items

def subtitle_of_year(title):
	string=re.split('20\d\d|19\d\d',title)[0]
	string=re.sub(xsearch('multi ',string,0,re.IGNORECASE),'',string)
	return string if string else title

def phimFshare(name,url,img,fanart,mode,page,query):#6
	fphimfshare=joinpath(datapath,'phimfshare.xml');home='http://phimfshare.com/';pagenext=''
	def pfs_page(url,pattern):
		body=make_request(url)
		return re.findall(pattern,body),xsearch('<a rel="next" href="(.+?)" title=".+?">',body)
	def pfs_addir(items):
		for id,href,img,name in items:addirs(name,href,img)
	def pfs_xml():
		pattern='<a id="(.+?)" server=".+?" href="(.+?)" img="(.*?)">(.+?)</a>'
		return re.findall(pattern,makerequest(fphimfshare))
	
	if query=='phimfshare.com':make_mySearch('',url,'','',mode,'get');return
	elif page==4 and name==query:return phimFshare('Search',url,img,fanart,mode,page,query)
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		return phimFshare('Search',url,img,fanart,mode,page,query) if query else 'no'
	elif name=='Search':
		items=googleapis_search('phimfshare.com',query,mode)
		items=[(s[2],s[1],'',s[0]) for s in items if 'Trang tiep theo' not in s[0]]
		if not items:mess(u'Không tìm thấy phim có chứa chuổi tìm kiếm!','phimFshare');return 'no'
	elif query=='get_link_post':
		response=make_request(url)
		img=xsearch('<img src="(.+?)" border="0" alt="" />',response)
		for server,href in pfs_getlink(response):addir_info(re.sub('\[/?COLOR.*?\]','',name),href,img)
		return
	elif query=='PhimMoi':
		items,pagenext=pfs_page(home,'()<a href="(.+?)" ()class="title">(.+?)</a>')
	elif url=='folder':pfs_addir([s for s in pfs_xml() if query in s[3]]);return
	else:
		if home not in url:url=home+url+'/'
		pattern='<img class="preview" src="(.+?)" .+? class=".+?" href="(.+?)" id="thread_title_(.+?)">(.+?)</a>'
		items,pagenext=pfs_page(url,pattern)#img,href,id,title
		
	items=[(s[0],s[1],s[2] if len(s[2])>4 else xsearch('-(\d{5})',s[1]),s[3]) for s in items]
	lists=[s for s in pfs_xml() if s[0] in [f[2] for f in items]]
	for label in list(set([subtitle_of_year(s[3]) for s in lists])):
		temp=[s for s in lists if label in s[3]]
		if not temp:continue
		elif len(temp)>1:
			id,href,img,title=temp[0];title=[s[3] for s in temp if '~' in s[3]]
			title=label+' ~ '+re.sub('.+?~ ?','',title[0]) if title and '~' not in label else label
			addir(color['phimfshare']+title+'[/COLOR]','folder',img,'',mode,page,label,True)
		else:pfs_addir(temp)
	if pagenext:
		page=2 if not page else page+1
		label=color['trangtiep']+'Trang tiếp theo - Trang '+str(page)+' ...[/COLOR]'
		addir(label,pagenext,iconpath+'fshare.png',mode=mode,page=page,query=query,isFolder=True)
	if name=='Search':return
	endxbmc();ids=[s[2] for s in items if s[2] not in list(set([f[0] for f in lists]))];content_new=''
	if ids:mess(u'Databse updating...','phimfshare.com')
	for img,href,id,name in [s for s in items if s[2] in ids]:
		response=make_request(href)
		temp=xsearch('<title> (.+?)</title>',response)
		if temp:name=temp
		elif not name:continue
		if not img:img=xsearch('<img src="(.+?)" border="0" alt="" />',response)
		name=' '.join(s for s in re.sub('\[.+?\]|\(.+?\)|MuLtI|Fshare|fshare','',name).split())
		for server,link in pfs_getlink(response):
			if link not in content_new:
				content_new+='<a id="%s" server="%s" href="%s" img="%s">%s</a>\n'%(id,server,link,img,name)
	if content_new:makerequest(fphimfshare,content_new,'a');xbmc.executebuiltin("Container.Refresh")
	return ''

def correct_link(url):
	if 'tenlua.vn' in url:idf=xsearch('(\w{16,20})',url)
	elif 'subscene.com' in url and '...' not in url:idf='ok'
	else:idf=xsearch('(\w{10,20})',url)
	if idf:
		url=url.lower()
		if 'fshare.vn/file' in url:url='https://www.fshare.vn/file/%s'%idf.upper()
		elif 'fshare.vn/folder' in url:url='https://www.fshare.vn/folder/%s'%idf.upper()
		elif 'tenlua.vn' in url and ('folder/' in url or '#download' in url) and len(idf)>16:
			url='https://tenlua.vn/fm/folder/%s'%idf
		elif 'tenlua.vn' in url and len(idf)>16:url='https://tenlua.vn/download/%s'%idf
		elif '4share.vn' or 'subscene.com'in url:url=url
	else:url=''
	return url

def hdvn_update(items=[]):#33-146-311-265-110-116-123-57-157
	mess(u'HDVietnam.com auto updating ...',homnay)
	urlhome='http://www.hdvietnam.com/diendan/external.php?type=RSS2&forumids='
	if not items:
		pattern='(https?://www.fshare.vn/\w{4,6}/\w{10,14})|(http://4share.vn/./\w{14,20})|(https?://w?w?w?/?tenlua.vn/.*?)[ |"|<]|(http://subscene.com/subtitles/.+?)[ |"|\'|<]'
		for id in '-33-146-311-265-110-116-123-57-157'.split('-'):
			mess('hdvietnam forumids=%s updating ...'%id,homnay)
			for name,link,pubDate,img,description,uploader in hdvietnam_rss(urlhome+id):
				for links in re.findall(pattern,description):
					for href in [s for s in links if s and '...' not in s]:
						href=correct_link(href)
						if href not in str(items):items.append((href,img,name))
	file=joinpath(datapath,"hdvietnam.xml");string='';count=0
	urls=re.findall('href="(.+?)"',makerequest(file))
	for url,img,name in [s for s in items if s[0] not in urls]:
		string+='<a date="%s" href="%s" img="%s">%s</a>\n'%(homnay,url,img,name);count+=1
	if string:
		makerequest(file,string,'a')
		mess(u'Đã cập nhật được %d phim'%count,'hdvietnam update')
	else:mess(u'Không có phim mới','hdvietnam update')
	return 'ok'

def hdvietnam_rss(url):
	body=xread(url);items=list()
	for data in re.findall('<item>(.+?)</item>',body,re.DOTALL):
		label=xsearch('<title><!\[CDATA\[(.+?)\]\]></title>',data)
		link=xsearch('<link>(.+?)</link>',data)
		pubDate=xsearch('<pubDate>(.+?)</pubDate>',data)
		description=xsearch('<description><!\[CDATA\[(.+?)\]\]></description>',data,1,re.DOTALL)
		uploader=xsearch('<dc:creator>(.+?)</dc:creator>',data);img=''
		for img in re.findall('Image: (http.+?\.jpg|http.+?\.png)',data):
			if not [s for s in ['kho-phim','chuyenlink.php','header-'] if s in img]:break
		items.append((label,link,pubDate,img,description,uploader))
	return items

def hdvietnam(name,url,img,fanart,mode,page,query):
	ico=icon['hdvietnam'];tempfolder=xbmc.translatePath('special://temp')
	urlhome='http://www.hdvietnam.com/diendan/';c='orangered'
	from resources.lib.servers import hdvn;hdvn=hdvn()
	menu={'muctheodoi':{'action':'Add','server':['hdvietnam.com']}}
	menu['MyFshare']={'action':'Add','server':['fshare.vn']}
	menu['MyFavourites']={'action':'Add','server':['fshare.vn','4share.vn','tenlua.vn','subscene.com']}
	
	if url in '000-UPD':
		if query=='UPD':hdvn_update()
		body=makerequest(joinpath(datapath,"hdvietnam.xml"));homqua=''
		if not body:return
		dates=sorted(list(set(re.findall('date="(.+?)"',body))),key=lambda k:k[6:]+k[3:5]+k[:2],reverse=True)
		homnay=dates[0] if query in '000-UPD' else query
		items=re.findall('date="%s" href="(.+?)" img="(.+?)">(.+?)</a>'%homnay,body)
		for name in list(set([subtitle_of_year(s[2]) for s in items])):
			lists=[s for s in items if name in s[2]]
			if not lists:continue
			elif len(lists)==1:
				href,img,title=lists[0]
				addir_info(title,href,img,'',mode,1,'',True,menu=menu)
			else:
				href,img,title=lists[0]
				title=name+' ~ '+re.sub('.+?~ ?','',title) if '~' in title and '~' not in name else name
				addir_info(title,'hdvietnam.com',img,'',mode,1,name,True,menu=menu)
		if dates.index(homnay)+1<len(dates):
			homqua=dates[dates.index(homnay)+1]
			name=color['trangtiep']+"Thông tin ngày %s[/COLOR]"%homqua
			addir_info(name,"000",ico,'',mode,1,homqua,True)
	
	elif query=='get_room_id':
		id=get_input('Hãy nhập chuỗi ID Room của hdvietnam.com')
		if not id or not id.strip():return 'no'
		url='http://www.hdvietnam.com/diendan/showthread.php?t=%s'%id
		return hdvietnam(name,url,img,fanart,mode,page,'get_link_post')
	
	elif 'muctheodoi' in query:
		if 'Add' in query:hdvn.addRoom(url)
		elif 'Remove' in query:
			if hdvn.removeRoom(url):xbmc.executebuiltin("Container.Refresh")
		else:
			menu={'muctheodoi':{'action':'Remove','server':['hdvietnam.com']}}
			if query=='muctheodoi':url='http://www.hdvietnam.com/diendan/subscription.php?folderid=0'
			content=hdvn.getpage(url,loop=True)
			for href,title in re.findall('<a class="title.*?" href="(.+?)" id=".+?">(.+?)</a>',content):
				addir_info(namecolor(title,c),urlhome+href,ico,'',mode,1,'get_link_post',True,menu=menu)
	
	elif url=='hdvietnam.com':
		body=makerequest(joinpath(datapath,"hdvietnam.xml"));temp=[]
		items=[s for s in re.findall('date=".+?" href="(.+?)" img="(.+?)">(.+?)</a>',body) if query in s[2]]
		for href,img,name in list(set(items)):
			if href not in temp:
				temp.append(href)
				addir_info(name,href,img,menu=menu)

	elif re.search('\d\d',query):
		url='http://www.hdvietnam.com/diendan/external.php?type=RSS2&forumids=%s'%query
		items=list();page=-1
		rss_list=hdvietnam_rss(url)
		if not rss_list:mess(u"Hôm nay chưa tìm thấy nội dung RSS này!","hdvietnam.com");return
		for label,link,pubDate,img,description,uploader in rss_list:
			items.append(description);page+=1
			name='[COLOR gold]%s[/COLOR] [COLOR lime]%s[/COLOR]:: %s'%(uploader,pubDate,label)
			addir_info(name,link,img,'',mode,page,'read_rss',True)
			if xsearch('/(\d{6,10})-',link):
				href='http://www.hdvietnam.com/diendan/showthread.php?t='+xsearch('/(\d{6,10})-',link)
			else:href=link
			addir_info(namecolor('Đến trang ',c)+os.path.basename(link),href,img,'',mode,1,'get_link_post',True,menu=menu)
			addir_info(namecolor(remove_tag(label),c),link,img,'',mode,page,'read_rss',True,menu=menu)
		temp=makerequest(joinpath(tempfolder,"hdvietnam.rss"),str(items),'w')

	elif query=='read_rss':
		items=list();name=remove_tag(name)
		try:content=eval(makerequest(joinpath(tempfolder,"hdvietnam.rss")))[page]
		except:content=''
		pattern1='<a href="(.+?hdvietnam.com.+?|.+?fshare.vn.+?|.+?4share.vn.+?|.+?tenlua.vn.+?|.+?subscene.com.+?)" target="_blank">(.+?)</a>'
		pattern2='(https?://www.fshare.vn/\w{4,6}/\w{10,14})|(http://4share.vn/./\w{14,20})|(https?://w?w?w?/?tenlua.vn/.*?)[ |"|<]|(http://subscene.com/subtitles/.+?)[ |"|\'|<]'
		for href,title in re.findall(pattern1,content):
			if any(s for s in ['fshare.vn/','4share.vn/','tenlua.vn/','subscene.com/'] if s in title):
				items.append((0,name,href,img))
			elif 'http://' not in title:items.append((1,remove_tag(title),href,img))
		for links in re.findall(pattern2,content):
			for link in [s for s in links if s and '...' not in s]:
				if link not in str(items):items.append((0,name,link,img))
		for title,href,img in [(s[1],s[2].replace('amp;',''),s[3]) for s in sorted(items)]:
			addir_info(title,href,img,query='get_link_post',menu=menu)

	elif query=='MCS':
		body=hdvn.getpage('http://www.hdvietnam.com/diendan/34-chia-se-phim/?styleid=25')
		for href,name in re.findall('<h3><a href="(.+?)">(.+?)</a></h3>',body):
			addir_info(namecolor(name,c),urlhome+href.split('&')[0],img,query='PL1')

	elif query=='CSN':
		body=hdvn.getpage('http://www.hdvietnam.com/diendan/148-chia-se-nhac/?styleid=25')
		for href,name in re.findall('<h3><a href="(.+?)">(.+?)</a></h3>',body):
			addir_info(namecolor(name,c),urlhome+href.split('&')[0],img,query='PL1')

	elif query=='PL1':
		parent_path='http://www.hdvietnam.com/diendan/'
		if '&styleid=9' not in url:url=url+'&styleid=9'
		hd['Referer']='http://www.hdvietnam.com/diendan/'
		body=xread(url.replace('amp;',''),hd)
		if not body:body=xread(url.replace('amp;',''),hd)
		if page<2:#Phụ Mục
			for href,title in re.findall('<a href="(forumdisplay.php.+?)">(.+?)</a></h2>',body):
				href=parent_path+href;title=title.replace(', ',' - ')
				addir_info('[B]'+namecolor(title,c)+'[/B]',href,ico,'',mode,1,'PL1',True)
		
		#Normal Threads
		pattern='<a class="title" href="(showthread.php.+?)&.+?>(.+?)</a>.+?<b>(.+?)</span>'
		menu={'muctheodoi':{'action':'Add','server':['hdvietnam.com']}}
		body=xsearch('(Normal Threads.+?<span class="shade">)',body,1,re.DOTALL)
		
		for s in re.findall('(<h3 class="threadtitle">.+?<div class="threaddetails td">)',body,re.DOTALL):
			href=parent_path+xsearch('class="title[^"]*" href="(.+?)"',s)
			title=remove_tag(xsearch('<a class="title[^"]*"[^<]+?>(.+?)</a>',s))
			bossroom=remove_tag(xsearch('<b>(.+?)</span>',s))
			title='[COLOR yellow]%s[/COLOR]-%s'%(bossroom,namecolor(title,c))
			addir_info(title,href,ico,'',mode,1,'get_link_post',True,menu=menu)
			
		pages=xsearch('class="popupctrl">Trang \d{1,4}/(\d{1,4})</a></span>',body)
		page=2 if page<2 else page+1
		if pages and int(pages)>page:
			name=color['trangtiep']+'Trang tiep theo...trang %d%s[/COLOR]'%(page,('/'+pages) if pages else '')
			if '&page=' not in url:url=url+'&page=%d'%page
			else:url=re.sub('&page=\d{1,3}','&page=%d'%page,url)
			addir_info(name,url,ico,'',mode,page,'PL1',True)
	
	elif query=='get_link_post':
		temp='';roomid=xsearch('t=(\d+)',url) if xsearch('t=(\d+)',url) else xsearch('(\d{6,10})',url)
		add_sep_item('-%s-'%namecolor(name).replace('HDVN','Room:').replace('Đến trang ',''))
		
		if roomid:
			url='http://www.hdvietnam.com/diendan/showthread.php?t='+roomid;print 'get_link_post: %s'%url
			buian='BuiAn' if 'Xem gì hôm nay' in name else ''
			for title,href,img in hdvn.getlink(url,buian):
				if 'http' not in href:href=urlhome+href
				if img=='morethread':
					if not temp:add_sep_item('Các chủ đề cùng chuyên mục')
					img=ico;temp='added_sep_item'
				query='download' if 'subscene.com' in href else 'get_link_post'
				addir_info(title,href,img,'',mode,1,query,menu=menu)#query=download cho subscene
		else:
			content=hdvn.getpage(url,loop=True)
			for href,title in re.findall('<a class="title.*?" href="(.+?)" id=".+?">(.+?)</a>',content):
				addir_info(namecolor(title,c),urlhome+href,ico,'',mode,1,'get_link_post',True,menu=menu)

def database_download():
	mess(u'Đang kiểm tra và download database cho xshare','database_download');delete_files(tempfolder)
	tempfile = joinpath(tempfolder,"xshare_data.zip");pattern='<title>.*xx(.+?)xx.*</title>'
	if not os.path.exists(datapath):os.mkdir(datapath)
	if not os.path.exists(iconpath):os.mkdir(iconpath)
	id=xsearch(pattern,make_request('https://www.fshare.vn/folder/9F3VWL147DYG'))
	response=make_request('https://docs.google.com/uc?id=%s&export=download'%id,resp='o',maxr=1)
	if  response.status==200:
		body=makerequest(tempfile,response.body,'wb');xbmc.sleep(500)
		try:xbmc.executebuiltin('XBMC.Extract("%s","%s")'%(tempfile,tempfolder), True)
		except:mess(u'Database download error!','database_download');return
		xml_size=dict();png_size=dict()
		for file in os.listdir(datapath):xml_size[file]=os.path.getsize(joinpath(datapath,file))
		for file in os.listdir(iconpath):png_size[file]=os.path.getsize(joinpath(iconpath,file))
		for file in os.listdir(tempfolder):
			if os.path.isfile(joinpath(tempfolder,file)):
				if '.xml' in file:
					a=makerequest(joinpath(tempfolder,file));s=a.splitlines()
					a=makerequest(joinpath(datapath,file));d=a.splitlines();w=False
					for i in s:
						if i not in d:d.append(i);w=True
					if w:a='';makerequest(joinpath(datapath,file),'\n'.join(i for i in d),'w')
				elif '.xml' in file and xml_size.get(file,0)<os.path.getsize(joinpath(tempfolder,file)):
					rename_file(joinpath(tempfolder,file),joinpath(datapath,file))
				elif '.png' in file and png_size.get(file,0)!=os.path.getsize(joinpath(tempfolder,file)):
					rename_file(joinpath(tempfolder,file),joinpath(iconpath,file))
				elif '.jpg' in file and os.path.getsize(joinpath(tempfolder,file))!=613866:
					rename_file(joinpath(tempfolder,file),joinpath(home,file))
		if os.path.isfile(joinpath(data_path,'checkdatabase.txt')):os.remove(joinpath(data_path,'checkdatabase.txt'))
		myaddon.setSetting('checkdatabase','false');mess(u'Download database cho xshare thành công','database_download')
	else:mess(u'Download database cho xshare không thành công!','database_download')

def xshare_auto_update():
	try:
		if checkupdate('last_update.dat',17,datapath):
			xshare_update();vp_make_datanew();vp_update();ifile_update()
			makerequest(joinpath(datapath,"last_update.dat"),'','w')
			mess('Xshare auto update completed','vaphim ifiletv')
		#if checkupdate('phimfshare.xml',11,datapath):pfs_update()
		if checkupdate('hdvietnam.xml',7,datapath):hdvn_update()
	except:mess('Data update error!')

def checkupdate(filename,hours=1,folder=datapath,xdict=dict()):
	filecheck=joinpath(folder,filename);timeformat='%Y%m%d%H'
	filetime=os.path.getmtime(filecheck) if os.path.isfile(filecheck) else 0
	last_update=datetime.datetime.fromtimestamp(filetime).strftime(timeformat)
	timenow=datetime.datetime.now().strftime(timeformat)
	#if int(timenow)-int(last_update)>hours:
	#	xshare_dict=json_rw('xshare.json');file_time=xshare_dict.get(filename,'0')
	#	if timenow > file_time:xshare_dict[filename]=timenow;json_rw('xshare.json',xshare_dict);result=True
	return (int(timenow)-int(last_update))>hours

def xshare_update():
	timenow=datetime.datetime.now().strftime('%Y%m%d%H')
	my_dict=json_rw('xshare.json');time_xshare=my_dict.get('time_xshare','0')
	if int(timenow)-int(time_xshare)<24*7:return
	room_id=my_dict.get('room_id') if my_dict.has_key('room_id') else '997745'
	url='http://www.hdvietnam.com/diendan/showthread.php?t=%s&mode=threaded&styleid=9'%room_id
	items=re.findall('writeLink\((.+?),.+?,.+?, (.+?),',make_request(url,maxr=1));temp=False
	for post_id in [s[0] for s in items if s[1]=='528657' and not my_dict.has_key(s[0])]:
		my_dict[post_id]='';temp=True
	if not temp:my_dict['room_id']='997745' if room_id=='947935' else '947935'
	my_dict['time_xshare']=timenow;json_rw('xshare.json',my_dict)

def xshare_postks(body,hd,token):
	if myaddon.getSetting('usernameh')=='thaitni':return body,token,hd['Cookie']
	my_dict=json_rw('xshare.json');url='http://www.hdvietnam.com/diendan/post_thanks.php'
	for post_id in my_dict:
		if not my_dict[post_id]:
			response=make_post(url,hd,'do=post_thanks_add&using_ajax=1&p=%s&securitytoken=%s'%(post_id,token))
			my_dict[post_id]='Y';json_rw('xshare.json',my_dict);break
	return body,token,hd['Cookie']

def write_trans(fo,string,m):
	translist=google_trans(string);j=0
	for i in m:
		if i=='xshare':
			try:fo.write(translist[j].strip()+'\n');j+=1
			except:pass
		else:fo.write(i)
    
def google_trans(s):
	hd={'User-Agent':'Mozilla/5.0','Accept-Language':'en-US,en;q=0.8,vi;q=0.6','Cookie':''}
	url='https://translate.google.com.vn/translate_a/single?oe=UTF-8&tl=vi&client=t&hl=vi&sl=en&dt=t&ie=UTF-8&q=%s'%s
	body= xread(url,hd)
	body=body.replace(',,"en"','').replace('[[[','').replace(']]]','')
	result=''
	for i in body.split('],['):
		research=re.search('"(.+?)","(.+?)"',i)
		if research:result+=research.group(1)+' '
		else:print '%s :not research'%i
	return result.replace('Xshare','xshare').split('xshare')

def subscene(name,href,query):
	if not re.search('\d{5,10}',href):
		if not os.path.basename(href):href=os.path.dirname(href)
		pattern='<a href="(/subtitles/.+?)">\s+<span class=".+?">\s*(.+?)\s+</span>\s+<span>\s+(.+?)\s+</span>'
		body=make_request(href.replace('amp;',''),headers={'Cookie':'LanguageFilter=13,45'})
		subs=re.findall(pattern,body)
		if not subs:
			temp=xsearch('<a href="(.+?)"',xsearch('<h2 class="exact">Exact</h2>(.+?)</ul>',body,1,re.DOTALL))
			if temp:
				body=make_request('http://subscene.com'+temp,headers={'Cookie':'LanguageFilter=13,45'})
				subs=re.findall(pattern,body)
		mess(u'Tên phim: %s'%s2u(name).replace('[COLOR green]Subscene[/COLOR]-',''))
		for url,lang,name in sorted(subs,key=lambda l:l[1], reverse=True):
			name='Eng.'+name if '/english/' in url else '[COLOR red]Vie.[/COLOR]'+name
			addirs(name,'http://subscene.com'+url,query='download')
		return ''
	pattern='<a href="(.+?)" rel="nofollow" onclick="DownloadSubtitle.+">'
	downloadlink='http://subscene.com' + xsearch(pattern,make_request(href))
	if len(downloadlink)<20:mess(u'Không tìm được maxspeed link sub!')
	else:xshare_resolve(downloadlink)
	return 'ok'

def megabox(name,url,img,fanart,mode,page,query):
	home='http://phim.megabox.vn/'
	cat={1:'Phim lẻ',2:'Phim bộ',3:'Show',4:'Clip'}
	gen={1:'Hành động',2:'Phiêu lưu',3:'Ma kinh dị',4:'Tình cảm',5:'Hoạt hình',6:'Võ thuật',7:'Hài',8:'Tâm lý',9:'Kiếm hiệp',10:'Sử thi',11:'',12:'',13:'Hình sự',14:'',15:'Âm nhạc',16:'Khoa học',17:'Tài liệu',18:'Gia đình',21:'Chiến tranh',22:'Thể thao',25:'Độc-Lạ',27:'Khoa học viễn tưởng',28:'Ẩm thực',29:'Thời trang',30:'Điện ảnh',31:'Thiếu nhi',32:'Giáo dục',33:'TV-Show',34:'Live Show',36:'Công nghệ',37:'Khám phá thế giới',38:'Động vật',39:'Shock'}
	country={1:'Âu-Mỹ',2:'Hàn Quốc',3:'Hồng Kông',4:'Trung Quốc',5:'Nhật Bản',6:'Thái Lan',7:'Quốc Gia khác',8:'Mỹ',9:'Pháp',11:'Việt Nam',12:'Ấn Độ',13:'Philippines'}#get(url,headers=hd,maxr=2)
	def mes(string):mess(string,title=namecolor('megabox.vn'))
	def namecolor(name):return color['megabox']+name+'[/COLOR]'
	def get_id(url):return xsearch('-(\d{1,6})\.html',url,1)
	def duration(string):return xsearch('Thời lượng:<.+?> (.+?)</li>',string,1)
	def countview(string,tag='span'):return xsearch('class=.count-view.><%s></%s> (.+?)</span>'%(tag,tag),string,1)
	def thuyetminh(string):return color['subscene']+'TM[/COLOR] ' if xsearch('class=.ico-sub.',string,0) or string=='TM' else ''
	def phim18(string):return '[COLOR red][B]M+[/B][/COLOR] ' if xsearch('class=.ico-rating.',string,0) or string=='M+' else ''
	def episode(string):return xsearch('class=.esp.><i>(.+?)</span>',string,1).replace('</i>','')
	def update_dict(dict):
		body=make_request(home,headers=hd)
		#(phim-le,Phim lẻ),(phim-bo,Phim bộ),(show,Show),(clip,Clip)
		dict['MGB1']=re.findall('<li><a href="(.+?)" title="">(.+?)</a></li>',body)
		#(Lẻ Bộ Show Clip Mới Nhất, Chiếu Rạp) (Megabox giới thiệu, Top 10, sắp chiếu, lẻ-bộ-show-clip xem nhiều)
		dict['MGB2']=re.findall('"H2title">(.+?)</h2>',body)
		content=sub_body(body,'id="phimle"','id="phimbo"')
		dict['phim-letl']=re.findall("title='(.+?)'.{1,3}href='(.+?)'",content[:content.find('Quốc gia')])
		dict['phim-leqg']=re.findall("title='(.+?)'.{1,3}href='(.+?)'",content[content.find('Quốc gia'):])
		content=sub_body(body,'id="phimbo"','id="tvshow"')
		dict['phim-boqg']=re.findall("title='(.+?)'.{1,3}href='(.+?)'",content[:content.find('Thể Loại')])
		dict['phim-botl']=re.findall("title='(.+?)'.{1,3}href='(.+?)'",content[content.find('Thể Loại'):])
		content=sub_body(body,'id="tvshow"','id="clip"')
		dict['showtl']=re.findall("title='(.+?)'.{1,3}href='(.+?)'",content[:content.find('Quốc gia')])
		dict['showqg']=re.findall("title='(.+?)'.{1,3}href='(.+?)'",content[content.find('Quốc gia'):])
		content=sub_body(body,'id="clip"','class="search-toogle"')
		dict['cliptl']=re.findall("title='(.+?)'.{1,3}href='(.+?)'",content)
		dict['gioithieu']=re.findall("<li><a href='(.+?)'",sub_body(body,'class="hotFilmSlider"','id="bx-pager"'))
		dict['top10']=re.findall('href="(.+?)"',sub_body(body,'begin topFilm','end topFilm'))
		dict['sapchieu']=re.findall("<a href='(.+?)'>",sub_body(body,'Phim sắp chiếu','end primary'))
		for i in range(1,5):
			s1='id="subCate-%d"'%i;s2='id="ul-%d"'%i
			dict['subCate%d'%i]=re.findall('data=.(.+?). data1=.(.+?).>(.+?)</a>',sub_body(body,s1,s2))
		return json_rw(dict)
	def get_detail(urls,dict):
		mes('[COLOR green]Xshare database updating ...[/COLOR]')
		for url in urls:
			id=get_id(url);body=sub_body(make_request(url,maxr=3),'begin primary','end primary');tm='TM' if thuyetminh(body) else ''
			views=countview(body);esp=xsearch('Số tập <i>(.+?)</i>',body,1);p18='M+' if phim18(body) else ''
			items=re.findall('alt=\'(.+?)\' src="(.+?)"',body)
			if not items:continue
			elif len(items)==1:title=items[0][0];fanart=img=items[0][1]
			else:title=items[0][0];fanart=items[0][1];img=items[1][1]
			if esp:series='y'
			else:series='n';esp=duration(body)
			dict[id]=(series,title,img,fanart,views,esp,tm,p18)
		return dict
	def json_rw(dicts={}):
		if dicts:makerequest(joinpath(datapath,'megabox.json'),json.dumps(dicts),'w')
		else:
			try:dicts=json.loads(makerequest(joinpath(datapath,'megabox.json')))
			except:dicts={}
		return dicts
	def load_urls(urls):
		dict=json_rw();urls_old=[];urls_new=[];ids=[];update=False
		for url in urls:
			id=get_id(url)
			if not id:continue
			elif dict.has_key(id) and dict[id]:urls_old.append(url)
			else:urls_new.append(url)
			ids.append((id,url))
		if urls_new:dict=get_detail(urls_new,dict)
		for id,url in ids:
			try:tm=thuyetminh(dict[id][6])+phim18(dict[id][7])
			except:tm=''
			img=dict[id][2];fanart=dict[id][3]
			if dict[id][0]=='y':
				epi=xsearch('(.+?)\W(.*?)\Z',dict[id][5],1);eps=xsearch('(.+?)\W(.*?)\Z',dict[id][5],2)
				title=namecolor(dict[id][1])+color['subscene'];query='1episode'+eps;isFolder=True
				title=title+' - %s views:%s[/COLOR]'%(dict[id][5],dict[id][4])
			else:
				title=dict[id][1]+color['subscene']+' - (%s - views:%s)[/COLOR]'%(dict[id][5],dict[id][4].strip())
				query='mgbplay';isFolder=False
			addir(tm+title,url,img,fanart,mode,1,query,isFolder=isFolder)
		if urls_new:endxbmc();json_rw(get_detail(urls_old,dict));mes('[COLOR lime]Xshare database updated[/COLOR]')
	def put_items(items,tag='span'):#class='count-view'><span></span> 551</span>
		dict=json_rw();cl=color['subscene']
		href_old=[s[0] for s in items if get_id(s[0]) in dict]
		href_new=[s[0] for s in items if s[0] not in href_old]
		for href,name,dura,img,esp,view in items:
			id=get_id(href);views=countview(view,tag);dura=duration(dura)
			tm=thuyetminh(esp)+phim18(esp);esp=episode(esp);eps=xsearch('\W(.*)\Z',esp,1)
			if esp:title,query,series,isFolder=namecolor(name),'1episode'+eps,'y',True
			else:title,esp,query,series,isFolder=name,dura,'mgbplay','n',False
			title=tm+title+' %s%s views: %s[/COLOR]'%(cl,esp,views)
			try:fanart=dict[id][3] if href in href_old else img
			except:fanart=img
			p18='M+' if 'M+' in tm else '';tm='TM' if 'TM' in tm else ''
			dict[id]=(series,name,img,fanart,views,esp,tm,p18)
			addir(title,href,img,fanart,mode,1,query,isFolder)
		return href_new,dict
	def update_href_new(hrefs,dict):
		mes('[COLOR green]Xshare database updating ...[/COLOR]')
		for href in href_new:
			id=get_id(href);body=sub_body(make_request(href,maxr=3),'begin primary','end primary')
			items=re.findall('alt=\'(.+?)\' src="(.+?)"',body)
			if len(items)<2:continue
			series,name,img,fanart,views,esp,tm,p18=dict[id];fanart=items[0][1];img=items[1][1]
			dict[id]=(series,name,img,fanart,views,esp,tm,p18)
		json_rw(dict);mes('[COLOR lime]Xshare database updated[/COLOR]')
	
	if query=='megabox.vn':make_mySearch('',url,'','',mode,'get')
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		if query:return megabox(query,url,img,fanart,mode,page,query)
		else:return 'no'
	elif query==name:#Search in megabox.vn
		search_string = urllib.quote_plus(query)
		body=make_post('http://phim.megabox.vn/tim-kiem?keyword=%s'%search_string).body
		body=sub_body(body,'class="item"','id="footer"')
		patt='<a class.+?href="(.+?)".+?title.>(.+?)</h3>(.+?)<img.+?src="(.+?)"(.+?)</a>.+?<a.+?a>(.+?)</div></div>'
		put_items(re.findall(patt,body,re.DOTALL))
	elif query=='MGB':
		dict=json_rw()
		if not dict.get('MGB1'):dict=update_dict(dict)
		name=color['search']+"Search trên megabox.vn[/COLOR]"
		addir(name,'megabox.vn',icon['megabox'],'',mode,1,'megabox.vn',True)
		for href,name in dict['MGB1']:#(phim-le,Phim lẻ),(phim-bo,Phim bộ),(show,Show),(clip,Clip)
			addir(color['megabox']+name+'[/COLOR]',href,icon['megabox'],'',mode,1,'mainmenu',True)
		for name in dict['MGB2']:
			if isinstance(name,unicode):name=name.encode('utf-8')
			result=re.search('href="(.+?)">(.+?)</a>',name)
			if result:#Lẻ Bộ Show Clip Mới Nhất, Chiếu Rạp
				title=namecolor(result.group(2));href=result.group(1)
				addir(title,href,icon['megabox'],'',mode,1,'subCate',True)
			else:#Megabox giới thiệu, Top 10, sắp chiếu, lẻ-bộ-show-clip xem nhiều
				title=namecolor(re.sub('<.+?>','',name+' trong ngày' if 'xem' in name else name))
				addir(title,home,icon['megabox'],'',mode,1,'xemnhieu',True)
		if checkupdate('megabox.json')>8:dict=update_dict(dict)
	elif query=='mainmenu' and url in ('phim-letl','phim-leqg','phim-botl','phim-boqg','showtl','showqg','cliptl'):
		dict=json_rw()
		for title,href in dict[url]:
			title=color['megabox']+title.replace('Phim ','')+'[/COLOR]'
			addir(title,href,icon['megabox'],'',mode,1,'mainmenu',True)
	elif query=='mainmenu':#url:(phim-le,phim-bo,show,clip)
		submenu={'phim-le':'Phim lẻ','phim-bo':'Phim bộ','show':'Show','clip':'Clip'}
		if url=='clip':
			title=color['xshare']+submenu[url]+' theo thể loại[/COLOR]'
			addir(title,url+'tl',icon['megabox'],'',mode,1,query,True)
		elif url in ('phim-le','phim-bo','show'):
			title=color['xshare']+submenu[url]+' theo thể loại[/COLOR]'
			addir(title,url+'tl',icon['megabox'],'',mode,1,query,True)
			title=color['xshare']+submenu[url]+' theo quốc gia[/COLOR]'
			addir(title,url+'qg',icon['megabox'],'',mode,1,query,True)
		pattern='<a class.+?href="(.+?)".+?title.>(.+?)</h3>(.+?)<img.+?src="(.+?)">(.+?)</a>.+?<a.+?a>(.+?)</div><'
		body=sub_body(make_request(home+url,maxr=3),'begin primary','end primary')
		href_new,dict=put_items(re.findall(pattern,body,re.DOTALL),'i')
		url_next=xsearch('<li class="next"><a href="(.+?)">',body,1)
		if url_next:
			page_end=xsearch('<span></span>Trang.{1,10}/(\d{1,3})</div>',body,1)
			page_next=xsearch('trang-(.+)\Z',url_next,1)
			name=color['trangtiep']+'Trang tiếp theo: trang %s/%s[/COLOR]'%(page_next,page_end)
			addir(name,url_next,icon['megabox'],'',mode,1,query,True)
		if href_new:endxbmc();update_href_new(href_new,dict)
	elif query=='mgbplay':
		url='/'.join((os.path.dirname(url),urllib.quote(os.path.basename(url))))
		body=make_request(url,resp='o',maxr=5);link=xsearch("changeStreamUrl\('(.+?)'\)",body.body,1)
		if not link:play_youtube(xsearch("\'(https://www.youtube.com/watch\?v=.+?)\'",body.body,1));return
		hd['Cookie']=body.cookiestring
		maxspeedlink=make_post('http://phim.megabox.vn/content/get_link_video_lab',data={"link":"%s"%link},resp='j')
		if maxspeedlink.get('link'):
			name=re.sub(' \[COLOR.+?/COLOR\]','',name)
			xbmcsetResolvedUrl(maxspeedlink.get('link')+'|'+urllib.urlencode(hd),name+'Maxlink')
		else:mes('[COLOR red]Get maxspeed link thất bại[/COLOR]')
	elif 'episode' in query:
		art=fanart.split('/banner/')[0] if fanart!=fanart.split('/banner/')[0] else ''
		href=os.path.dirname(url);id=get_id(url)
		start=query.split('episode')[0];eps=query.split('episode')[1]
		try: eps=int(eps)
		except:eps=int(xsearch('(\d{1,4})/\?',name,1) if xsearch('(\d{1,4})/\?',name,1) else '1')
		for epi in make_request('http://phim.megabox.vn/content/ajax_episode?id=%s&start=%s'%(id,start),resp='j'):
			name=epi['name'];href='%s/%s-%s.html'%(href,epi['cat_id'],epi['content_id'])
			if not art:fanart='http://img.phim.megabox.vn/300x168'+epi['image_banner']
			else:fanart=art+epi['image_banner']
			addir(name,href,img,fanart,mode,1,'mgbplay')
		if int(start)+30<eps:
			name=color['trangtiep']+u'Các tập tiếp theo: %d-%d[/COLOR]'%(int(start)+30,eps)
			addir(name,url,img,fanart,mode,1,'%depisode%d'%(int(start)+30,eps),True)
	elif 'Megabox giới thiệu' in name:dict=json_rw();load_urls(dict['gioithieu'])
	elif 'Top 10 phim trong ngày' in name:dict=json_rw();load_urls(dict['top10'])
	elif 'Phim sắp chiếu' in name:dict=json_rw();load_urls(dict['sapchieu'])
	elif query=='xemnhieu':#lẻ-bộ-show-clip xem nhiều
		cats={'lẻ':1,'bộ':2,'show':3,'clip':4};cat=[cats[s] for s in cats if s in name][0]
		href='http://phim.megabox.vn/mostviewed/ajax/?cat=%d&period=%d'
		period=[('ngày',1),('tuần',2),('tháng',3)];per=[s[0] for s in period if s[0] in name][0]
		for pe in period:
			if pe[0]==per:href=href%(cat,pe[1]);continue
			title=color['xshare']+re.sub('\[.?COLOR.*?\]','',name).replace(per,pe[0])+'[/COLOR]'
			addir(title,url,icon['megabox'],'',mode,1,query,True)
		load_urls(re.findall('<a href="(.+?)">',make_request(href,hd)))
	elif 'Phim Chiếu Rạp' in name or query=='phim-chieu-rap':
		href='http://phim.megabox.vn/t/phim-chieu-rap-29/phim-le/trang-%d'
		body=sub_body(make_request(href%page,maxr=3),'begin main','end main')
		pattern='<a class.+?href="(.+?)".+?title.>(.+?)</h3>(.+?)<img.+?src="(.+?)">(.+?)</a>.+?<a.+?a>(.+?)</div><'
		href_new,dict=put_items(re.findall(pattern,body,re.DOTALL))
		page_end=xsearch('<li class="last"><a href="t/phim-chieu-rap-29/phim-le/trang-(.+?)">',body,1)
		name=color['trangtiep']+'Trang tiếp theo: trang %d/%s[/COLOR]'%(page+1,page_end)
		addir(name,href,icon['megabox'],'',mode,page+1,'phim-chieu-rap',True)
		if href_new:endxbmc();update_href_new(href_new,dict)
	elif query=='subCate':#url=phim-le,phim-bo,t/phim-chieu-rap-29,show,clip
		if '/' in url:gen=url.split('/')[1];url=url.split('/')[0]
		else:gen='ALL'
		cat={'phim-le':('Lẻ',1),'phim-bo':('Bộ',2),'show':('Show',3),'clip':('Clip',4)}
		href='http://phim.megabox.vn/home/getcontent/?cat=%s&genre=%s&country=%s';dict=json_rw()
		for genre,country,gen_name in dict['subCate%d'%cat[url][1]]:
			gen_name=gen_name.encode('utf-8') if type(gen_name)==unicode else str2u(gen_name)
			if gen_name==gen:href=href%(cat[url][1],genre,country);continue
			title=color['xshare']+re.sub('\[.?COLOR.*?\]','',name);
			title=re.sub('%s.+\Z'%cat[url][0],cat[url][0]+' %s Mới Nhất[/COLOR]'%gen_name,title)
			addir(title,url+'/'+gen_name,icon['megabox'],'',mode,1,query,True)
		patt="<a class.+?href='(.+?)'.+?title.>(.+?)</h3>(.+?)<img.+?src='(.+?)'(.+?)</a>.+?<a.+?a>(.+?)</div></div>"
		put_items(re.findall(patt,make_request(href,hd),re.DOTALL),'i')
		cat={'phim-le':'Phim lẻ','phim-bo':'Phim bộ','show':'Show','clip':'Clip'}
		name=color['trangtiep']+'%s Xem Thêm...[/COLOR]'%cat[url]
		addir(name,url,icon['megabox'],'',mode,1,'mainmenu',True)
	return ''
	
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
		url='http://movies.hdviet.com/dang-xuat.html?accesstokenkey=%s'
		make_post(url%response.get('access_token')).body
		return response
	def getResolvedUrl(id_film,loop=0):#Phim le/phim chieu/ke doi dau thien ac
		def getlinkhdviet(token,id_film):
			id_film=id_film.replace('_e','&ep=')
			response=make_request(direct_link%(token,id_film),resp='j')
			try:links=response['r'];link=response['r']['LinkPlay']
			except:links=dict()
			return links
		data=json_rw('hdviet.cookie')
		links=getlinkhdviet(data.get('access_token'),id_film)
		if not links:return links
		link=links.get('LinkPlay')
		if '0000000000000000000000' in link:
			data=login_hdviet();links=getlinkhdviet(data.get('access_token'),id_film);link=links.get('LinkPlay')
		if links:
			max_resolution='_1920_' if myaddon.getSetting('hdvietresolution')=='1080' else '_1280_'
			resolutions=['_1920_','_1885_','_1876_','_1866_','_1792_','_1280_','_1024_','_800_','_640_','_480_']
			if '_e' in id_film:link=re.sub('%s_e\d{1,3}_'%id_film.split('_')[0],'%s_'%id_film,link)
			href=link
			for resolution in resolutions:
				if resolution in link:link=link.replace(resolution,max_resolution);break
			extm3u=make_request(link);link=''
			if not extm3u:extm3u=make_request(href)
			for resolution in resolutions:
				if resolution in extm3u:link=xsearch('(http://.+%s.+m3u8)'%resolution,extm3u,1)
				if link:break
		if link and loop==0:
			response=make_request(link,resp='o')
			if response and 'filename' not in response.headers.get('content-disposition',''):
				data=login_hdviet();return getResolvedUrl(id_film,1)
		if link:
			audioindex=-1
			try:
				for audio in links.get('AudioExt'):
					if audio.get('Label')==u'Thuyết Minh':
						audioindex=int(audio.get('Index'))-1
				linksub='xshare' if audioindex>-1 else ''
			except:linksub=''
			if not linksub:
				for source in ['Subtitle','SubtitleExt','SubtitleExtSe']:
					try:
						linksub=links['%s'%source]['VIE']['Source']
						if linksub:
							if download_subs(linksub):break
					except:pass
			if audioindex>-1:link=link+'?audioindex=%d'%audioindex
		else:linksub=''
		return link,linksub
	def additems(body):
		pattern='<li class="mov-item".+?href="(.+?)".+?src="(.+?)".+?title="Phim (.+?)".+?<span(.+?) data-id="(.+?)">'
		data=re.findall(pattern,body,re.DOTALL);listitems=list()
		for href,img,title,detail,id_film in data:
			epi=xsearch('"labelchap2">(\d{1,3})</span>',detail,1);title=unescape(title)
			res=xsearch('id="fillprofile" class="icon-(.+?)11">',detail,1)
			res='[COLOR gold]SD[/COLOR]' if 'SD' in res else '[COLOR gold]HD[/COLOR]%s'%res
			phim18=xsearch('class="children11".+?>(.+?)</label></span>',detail,1)
			TM=xsearch('id="fillaudio" class="icon-(.+?)">',detail,1)
			TM='%s[COLOR green]%s[/COLOR][COLOR red]%s[/COLOR]'%(res,TM,phim18)
			plot=xsearch('<span class="cot1">(.+?)</span>',detail,1)
			year=xsearch('<span class="chil-date".+?>(.*?)</label></span>',detail,1)
			act=', '.join(s for s in re.findall('<a href="http://movies.hdviet.com/dien-vien/.+?">(.+?)</a>',detail))
			drt=', '.join(s for s in re.findall('<a href="http://movies.hdviet.com/dao-dien/.+?">(.+?)</a>',detail))
			rat=xsearch('<span class="fl-left">.+?<span>(.+?)</span>',detail,1)
			upl=xsearch('<span class="fl-right">.+?<span>(.+?)</span>',detail,1)
			if not epi:title=TM+' '+title;query='hdvietplay'
			elif epi=='1':query='hdvietfolder'
			else:title=TM+' '+namecolor(title)+' [COLOR green](%s)[/COLOR]'%epi;query='hdvietfolder'
			listItem = xbmcgui.ListItem(label=title,iconImage=img,thumbnailImage=img)
			if rat:rat='[COLOR tomato]IMDb:[/COLOR] %s, '%rat
			if upl:upl='[COLOR tomato]Uploader:[/COLOR] %s, '%upl
			if act:act='[COLOR tomato]Diễnviên:[/COLOR] %s, '%act
			if drt:drt='[COLOR tomato]Đạodiễn:[/COLOR] %s, '%drt
			plot=rat+upl+act+drt+'\n'+plot
			info={'title':title,'year':year,'rating':xsearch('(\d\.\d{1,2})',rat,1),'plot':plot,'episode':epi,'director':drt,'writer':act}
			listItem.setInfo(type="Video", infoLabels=info)
			listItem.setArt({"thumb":img,"poster":img,"fanart":img})
			if query=='hdvietplay':listItem.setProperty('IsPlayable', 'true')
			u=sys.argv[0]+"?url="+id_film+"&img="+urllib.quote_plus(img)+"&fanart="+urllib.quote_plus(img)+"&mode="+str(mode)+"&page="+str(page)+"&query="+query+"&name="+title
			listitems.append((u,listItem,False if query=='hdvietplay' else True))
		xbmcplugin.addDirectoryItems(int(sys.argv[1]),listitems,totalItems=len(listitems))
	def hdviet_search(string):
		url='http://movies.hdviet.com/tim-kiem.html?keyword=%s'%urllib.quote_plus(string)
		hdviet(name,url,img,mode,page,query='timkiem')
	if query=='hdviet.com':
		name=color['search']+"Search trên hdviet.com[/COLOR] (Hãy chọn độ phân giải trên settings nhé)"
		addir(name,'http://movies.hdviet.com/tim-kiem.html',icon['icon'],fanart,mode,1,'search',True)
		if checkupdate('hdviet.html')>8:body=makerequest(joinpath(datapath,'hdviet.html'),make_request(home),'w')
		else:body=makerequest(joinpath(datapath,'hdviet.html'))
		items=re.findall('"mainitem" menuid="(.+?)" href="(.+?)" title=".+?">(.+?)</a>',body)
		for id,href,name in items:
			addir(namecolor(name),home,icon['hdviet'],fanart,mode,1,id,True)
		addir(namecolor('Thể loại phim'),'the-loai',icon['icon'],fanart,mode,1,'the-loai-phim',True)
		url='http://movies.hdviet.com/phim-yeu-thich.html'
		addir(namecolor('Phim yêu thích'),url,icon['icon'],fanart,mode,1,'yeu-thich',True)
		items=re.findall('<div class="h2-ttl cf">.+?<a href="(.+?)" title=".+?" >(.+?)</a>.+?</div>(.+?)</ul>',body,re.DOTALL)
		for href,name,subbody in items:
			addir('%s%s[/COLOR]'%(color['search'],name),href,icon['hdviet'],fanart,mode,page,'1',True)
			additems(subbody)
	elif query=='search':make_mySearch('','hdviet.com','','',mode,'get')
	elif query=="INP":hdviet_search(make_mySearch('',url,'','','','Input'))
	elif url=='hdviet.com':page=1 if 'Trang tiếp theo' not in name else page;hdviet_search(query)
	elif query=='the-loai-phim':
		for href,name in re.findall('<p><a href="(.+?)" title=".+?">(.+?)</a></p>',makerequest(joinpath(datapath,'hdviet.html'))):
			addir(namecolor(name),href,icon['hdviet'],fanart,mode,page,'theloai',True)
	elif query=='3' and url==home:#Phim lẻ
		items=re.findall('<a href="(.+?)" .?menuid="(.+?)" .?title=".+?" >(.+?)</a>',makerequest(joinpath(datapath,'hdviet.html')))
		for href,id,name in items:
			addir(namecolor(name),href,icon['hdviet'],fanart,mode,page,id,True)
	elif query=='10' and url==home:#Phim bộ
		body=makerequest(joinpath(datapath,'hdviet.html'))
		items=re.findall('<a href="(.+?)" menuid="(.+?)" title=".+?">(.+?)</a>',body)
		items+=re.findall('<a class="childparentlib" menuid="(.+?)" href="(.+?)" title=".+?">(\s.*.+?)</a>',body)
		for href,id,name in items:
			if 'au-my' in href:name='Phim bộ Âu Mỹ %s'%name.strip()
			elif 'hong-kong' in href:name='Phim bộ Hồng Kông %s'%name.strip()
			elif 'trung-quoc' in href:name='Phim bộ Trung Quốc %s'%name.strip()
			else:name='Phim bộ %s'%name.strip()
			if href in '38-39-40':temp=href;href=id;id=temp
			addir(namecolor(name),href,icon['hdviet'],fanart,mode,page,id,True)
	elif query=='hdvietfolder':
		href='http://movies.hdviet.com/lay-danh-sach-tap-phim.html?id=%s'%url
		response=make_request(href,resp='j')
		if not response:return
		for eps in range(1,int(response["Sequence"])+1):
			name=re.sub(' \[COLOR green\]\(\d{1,4}\)\[/COLOR\]','',name)
			title='Tập %s/%s-%s'%(format(eps,'0%dd'%len(response['Episode'])),str(response['Episode']),re.sub('\[.?COLOR.{,12}\]','',name))
			addir(title,'%s_e%d'%(url,eps),img,fanart,mode,page,'hdvietplay',False)
	elif query=='hdvietplay':
		link,sub=getResolvedUrl(url)
		if not link:mess(u'[COLOR red]Get link thất bại[/COLOR]',title='%sHDViet.com[/COLOR]'%color['hdviet'])
		else:
			if sub:
				mess(u'[COLOR green]Phụ đề của HDViet.com[/COLOR]',title='%sHDViet.com[/COLOR]'%color['hdviet'])
				sub=urllib.unquote(os.path.splitext(os.path.basename(sub))[0])
			xbmcsetResolvedUrl(link+'|'+urllib.urlencode(hd),sub)
	elif query=='Themmucyeuthich':
		hd['Cookie']=getcookie()
		body=make_post('http://movies.hdviet.com/them-phim-yeu-thich.html',hd,urllib.urlencode({"MovieID":"%s"%url}))
		try:mess(u'[COLOR green]%s[/COLOR]'%body.json['r'],title='%sHDViet.com[/COLOR]'%color['hdviet'])
		except:mess(u'[COLOR red]Lỗi thêm phim yêu thích[/COLOR]',title='%sHDViet.com[/COLOR]'%color['hdviet'])
	else:
		if query=='yeu-thich':hd['Cookie']=getcookie();body=make_request(url,hd)
		else:body=make_request(url)
		body=sub_body(body,'class="homesection"','class="h2-ttl cf"')
		additems(body)
		pages=re.findall('<li class=""><a href="(.+?)">(.+?)</a></li>',sub_body(body,'class="active"',''))
		if pages:
			pagenext=pages[0][1];pageend=pages[len(pages)-1][1]
			name='%sTrang tiếp theo: trang %s/%s[/COLOR]'%(color['trangtiep'],pagenext,pageend)
			addir(name,pages[0][0],img,fanart,mode,page,query,True)
		xbmc.executebuiltin('Container.SetViewMode(504)')

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
		content=sub_body(body,'class="menu_header"','class="box_login"')
		adict['mar-r20']=[s for s in re.findall('menu_fa_text.+?" href="(.+?)".*>(.+?)</a>',body) if os.path.basename(s[0])]
		for href,item in re.findall('href="(.+?)".+?<a (.+?)</ul>',content,re.DOTALL):
			for link,name in adict['mar-r20']:
				if href==link and 'trailer' not in link:
					name=os.path.basename(href)
					adict['m-%s'%name]=re.findall('href="(.+?)".*?>(.+?)</a>',item)
		pattern='href="(.+?)".*?>(.+\s.+|.+?)</a>.*\s?.*</h2>'
		adict['main']=[(s[0],' '.join(s for s in s[1].split())) for s in re.findall(pattern,body)]
		content=sub_body(body,'class="banner_slider"','class="main"')
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

	if checkupdate('hayhaytv.cookie')>24:hd['Cookie']=login()
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
		if checkupdate('hayhaytv.json')>8 and not os.path.isfile(joinpath(datapath,'hayhaytv.tmp')):
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
			body=sub_body(make_request(url,headers=hd,maxr=3),'<div id="new_player">','class="content_div"')
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

#phimmoi.net	
def namecolor(name):return '[COLOR tomato]%s[/COLOR]'%name
		
def getid(url):return xshare_group(re.search('-(\d{3,5})/',url),1)
def geteps(string):
	try:url=json.loads(string)['url'];part=json.loads(string)['part']
	except:url=part=''
	return url,part
def make_eps(url,eps):
	id=getid(url);content=makerequest(phimmoixml);string=''
	string_old=xshare_group(re.search('(<a id="%s" part=".+?"/>)'%id,content),1)
	for part_id in eps:string+=str(geteps(part_id)[1])+'-'
	string_new='<a id="%s" part="%s"/>\n'%(id,string[:len(string)-1])
	string=content.replace(string_old+'\n',string_new) if string_old else content+string_new
	makerequest(phimmoixml,string,'w')
def addirpm(name,link,img='',fanart='',mode=0,page=0,query='',isFolder=False,menu=list()):
	def xquote(href):return urllib.quote_plus(href)
	if '18+' in name and myaddon.getSetting('phim18')=="false":return
	name=unescape(re.sub(',|\|.*\||\||\<.*\>','',u2s(name)))
	item=xbmcgui.ListItem(name,iconImage=img,thumbnailImage=img)
	query=menuContext(name,link,img,fanart,mode,query,item)
	item.setInfo(type="Video", infoLabels={"title":name})
	if not fanart:fanart=joinpath(home,'fanart.jpg')
	item.setProperty('Fanart_Image',fanart)
	li='%s?name=%s&url=%s&img=%s&fanart=%s&mode=%d&page=%d&query=%s'
	li=li%(sys.argv[0],urllib.quote(name),xquote(link),xquote(img),xquote(fanart),mode,page,query)
	if not isFolder:item.setProperty('IsPlayable', 'true')
	if menu:#info={'name':'','url':'','img':'','fanart':'','query':''}
		cmd='RunPlugin(plugin://%s/?mode=%d'%(myaddon.getAddonInfo('id'),mode);items=list()
		for label,info in menu:
			name=info.get('name');url=info.get('url');img=info.get('img')
			fanart=info.get('fanart');query=info.get('query')
			command=cmd+'&name=%s&url=%s&img=%s&fanart=%s&query=%s)'%(name,url,img,fanart,query)
			items.append(('[COLOR lime]%s[/COLOR]'%label,command))
		item.addContextMenuItems(items)
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),li,item,isFolder)
def addir_pm(items,name='',menu=list()):#title,href,img,detail
	for title,href,img,detail in items:
		eps=xsearch('Tập ?(\d{,4}/\d{,4}|\?/\d{,4}|\d{,4})',detail,1)
		if not eps:
			epi=xsearch('class="eps">Trọn bộ ?(\d{1,4}) ?tập</div>',detail,1)
			if epi:eps='%s/%s'%(epi,epi)
		else:epi=eps.split('/')[0]
		try:epi=int(epi)
		except:epi=0
		dur=xsearch('>(\d{1,3}.?phút)',detail,1)
		if 'url=' in img:img=img.split('url=')[1]
		if eps:title='%s %s(%s)[/COLOR]'%(title,color['subscene'],eps)
		if dur:title='%s [COLOR gold]%s[/COLOR]'%(title,dur)
		if epi>1 or 'Phim bộ hot trong tuần' in name:query='pmfolder';isFolder=True;title=namecolor(title)
		else:query='pmplay';isFolder=False
		if 'Thuyết minh' in detail:title='[COLOR gold]TM[/COLOR] %s'%title
		label=xsearch('(HD[\w|-]*|SD[\w|-]*|Bản đẹp[\w|-]*)',detail,1)
		if label:title='%s - [COLOR green]%s[/COLOR]'%(title,label)
		addirpm(title,home+href,img,'',mode,page,query,isFolder,menu)
def get_epi(epi):
	try:epi=int(epi)
	except:epi=0
	return epi
def get_info(title,href,img,detail):
	home='http://www.phimmoi.net/'
	eps=xsearch('Tập ?(\d{,4}/\d{,4}|\?/\d{,4}|\d{,4})',detail,1)
	if not eps:
		epi=xsearch('class="eps">Trọn bộ ?(\d{1,4}) ?tập</div>',detail,1)
		if epi:eps='%s/%s'%(epi,epi)
	else:epi=eps.split('/')[0]
	dur=xsearch('>(\d{1,3}.?phút)',detail,1)
	audio='TM' if 'Thuyết minh' in detail else ''
	label=xsearch('(HD[\w|-]*|SD[\w|-]*|Bản đẹp[\w|-]*)',detail,1)
	if 'url=' in img:img=img.split('url=')[1]
	if eps:title='%s %s(%s)[/COLOR]'%(title,color['subscene'],eps)
	if dur:title='%s [COLOR gold]%s[/COLOR]'%(title,dur)
	#if get_epi(epi)>1 or 'Phim bộ hot trong tuần' in name:query='pmfolder';isFolder=True;title=namecolor(title)
	if get_epi(epi)>1:query='pmfolder';isFolder=True;title=namecolor(title)	
	else:query='pmplay';isFolder=False
	if audio:title='[COLOR gold]TM[/COLOR] %s'%title
	if label:title='%s - [COLOR green]%s[/COLOR]'%(title,label)
	return title,home+href,img,query,isFolder
def pm_addir2(name,link,img='',fanart='',mode='0',page=0,query='',isFolder=False,menu=list()):
	home='http://www.phimmoi.net/'
	def xquote(href):return urllib.quote_plus(href)
	#if '18+' in name and myaddon.getSetting('phim18')=="false":return
	name=unescape(re.sub(',|\|.*\||\||\<.*\>','',u2s(name)))
	item=xbmcgui.ListItem(name,iconImage=img,thumbnailImage=img)
	item.setInfo(type="Video", infoLabels={"title":name})
	if not fanart:fanart=joinpath(home,'fanart.jpg')
	item.setProperty('Fanart_Image',fanart)
	li='%s?name=%s&url=%s&img=%s&fanart=%s&mode=%s&page=%d&query=%s'
	li=li%(sys.argv[0],urllib.quote(name),xquote(link),xquote(img),xquote(fanart),mode,page,query)
	if not isFolder:item.setProperty('IsPlayable', 'true')
	if menu:#info={'name':'','url':'','img':'','fanart':'','query':''}
		cmd='RunPlugin(plugin://%s/?mode=%s'%(myaddon.getAddonInfo('id'),mode);items=list()
		for label,info in menu:
			name=info.get('name');url=info.get('url');img=info.get('img')
			fanart=info.get('fanart');query=info.get('query')
			command=cmd+'&name=%s&url=%s&img=%s&fanart=%s&query=%s)'%(name,url,img,fanart,query)
			items.append(('[COLOR lime]%s[/COLOR]'%label,command))
		item.addContextMenuItems(items)
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),li,item,isFolder)			
			
def phimmoi(name,url,img,mode,page,query):
	color['phimmoi']='[COLOR ghostwhite]';icon['phimmoi']=os.path.join(iconpath,'phimmoi.png')
	home='http://www.phimmoi.net/';refresh=False;phimmoixml=joinpath(datapath,'phimmoi.xml')
	tempfolder=xbmc.translatePath('special://temp')
	def namecolor(name):return '%s%s[/COLOR]'%(color['phimmoi'],name)
	def mes(string):mess(string,title=namecolor('phimmoi.net'))
	def login_pm():
		u=myaddon.getSetting('userphimmoi');p=myaddon.getSetting('passphimmoi')
		import hashlib;p=hashlib.md5(p).hexdigest()
		response=make_post('http://www.phimmoi.net/login/',data=urllib.urlencode({'username':u,'password_md5':p}))
		if response.status==302 and makerequest(joinpath(datapath,'phimmoi.cookie'),response.cookiestring,'w'):
			mes(u'[COLOR green]Login thành công[/COLOR]');f=response.cookiestring
		else:mes(u'[COLOR red]Login không thành công[/COLOR]');f=''
		return f
	def pm_search(string):
		url='http://www.phimmoi.net/tim-kiem/%s/'%urllib.quote_plus(string)
		phimmoi(name,url,img,mode,page=1,query='readpage')
	def getid(url):return xshare_group(re.search('-(\d{3,5})/',url),1)
	def geteps(string):
		try:url=json.loads(string)['url'];part=json.loads(string)['part']
		except:url=part=''
		return url,part
	def make_eps(url,eps):
		id=getid(url);content=makerequest(phimmoixml);string=''
		string_old=xshare_group(re.search('(<a id="%s" part=".+?"/>)'%id,content),1)
		for part_id in eps:string+=str(geteps(part_id)[1])+'-'
		string_new='<a id="%s" part="%s"/>\n'%(id,string[:len(string)-1])
		string=content.replace(string_old+'\n',string_new) if string_old else content+string_new
		makerequest(phimmoixml,string,'w')
	def addirpm(name,link,img='',fanart='',mode=0,page=0,query='',isFolder=False,menu=list()):
		def xquote(href):return urllib.quote_plus(href)
		if '18+' in name and myaddon.getSetting('phim18')=="false":return
		name=unescape(re.sub(',|\|.*\||\||\<.*\>','',u2s(name)))
		item=xbmcgui.ListItem(name,iconImage=img,thumbnailImage=img)
		query=menuContext(name,link,img,fanart,mode,query,item)
		item.setInfo(type="Video", infoLabels={"title":name})
		if not fanart:fanart=joinpath(home,'fanart.jpg')
		item.setProperty('Fanart_Image',fanart)
		li='%s?name=%s&url=%s&img=%s&fanart=%s&mode=%d&page=%d&query=%s'
		li=li%(sys.argv[0],urllib.quote(name),xquote(link),xquote(img),xquote(fanart),mode,page,query)
		if not isFolder:item.setProperty('IsPlayable', 'true')
		if menu:#info={'name':'','url':'','img':'','fanart':'','query':''}
			cmd='RunPlugin(plugin://%s/?mode=%d'%(myaddon.getAddonInfo('id'),mode);items=list()
			for label,info in menu:
				name=info.get('name');url=info.get('url');img=info.get('img')
				fanart=info.get('fanart');query=info.get('query')
				command=cmd+'&name=%s&url=%s&img=%s&fanart=%s&query=%s)'%(name,url,img,fanart,query)
				items.append(('[COLOR lime]%s[/COLOR]'%label,command))
			item.addContextMenuItems(items)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),li,item,isFolder)
	def addir_pm(items,name='',menu=list()):#title,href,img,detail
		for title,href,img,detail in items:
			eps=xsearch('Tập ?(\d{,4}/\d{,4}|\?/\d{,4}|\d{,4})',detail,1)
			if not eps:
				epi=xsearch('class="eps">Trọn bộ ?(\d{1,4}) ?tập</div>',detail,1)
				if epi:eps='%s/%s'%(epi,epi)
			else:epi=eps.split('/')[0]
			try:epi=int(epi)
			except:epi=0
			dur=xsearch('>(\d{1,3}.?phút)',detail,1)
			if 'url=' in img:img=img.split('url=')[1]
			if eps:title='%s %s(%s)[/COLOR]'%(title,color['subscene'],eps)
			if dur:title='%s [COLOR gold]%s[/COLOR]'%(title,dur)
			if epi>1 or 'Phim bộ hot trong tuần' in name:query='pmfolder';isFolder=True;title=namecolor(title)
			else:query='pmplay';isFolder=False
			if 'Thuyết minh' in detail:title='[COLOR gold]TM[/COLOR] %s'%title
			label=xsearch('(HD[\w|-]*|SD[\w|-]*|Bản đẹp[\w|-]*)',detail,1)
			if label:title='%s - [COLOR green]%s[/COLOR]'%(title,label)
			addirpm(title,home+href,img,'',mode,page,query,isFolder,menu)
	def get_epi(epi):
		try:epi=int(epi)
		except:epi=0
		return epi
	def get_info(title,href,img,detail):
		eps=xsearch('Tập ?(\d{,4}/\d{,4}|\?/\d{,4}|\d{,4})',detail,1)
		if not eps:
			epi=xsearch('class="eps">Trọn bộ ?(\d{1,4}) ?tập</div>',detail,1)
			if epi:eps='%s/%s'%(epi,epi)
		else:epi=eps.split('/')[0]
		dur=xsearch('>(\d{1,3}.?phút)',detail,1)
		audio='TM' if 'Thuyết minh' in detail else ''
		label=xsearch('(HD[\w|-]*|SD[\w|-]*|Bản đẹp[\w|-]*)',detail,1)
		if 'url=' in img:img=img.split('url=')[1]
		if eps:title='%s %s(%s)[/COLOR]'%(title,color['subscene'],eps)
		if dur:title='%s [COLOR gold]%s[/COLOR]'%(title,dur)		
		if get_epi(epi)>1 or 'Phim bộ hot trong tuần' in name:query='pmfolder';isFolder=True;title=namecolor(title)
		else:query='pmplay';isFolder=False
		if audio:title='[COLOR gold]TM[/COLOR] %s'%title
		if label:title='%s - [COLOR green]%s[/COLOR]'%(title,label)
		return title,home+href,img,query,isFolder
	def pm_addir(name,link,img='',fanart='',mode=0,page=0,query='',isFolder=False,menu=list()):
		def xquote(href):return urllib.quote_plus(href)
		if '18+' in name and myaddon.getSetting('phim18')=="false":return
		name=unescape(re.sub(',|\|.*\||\||\<.*\>','',u2s(name)))
		item=xbmcgui.ListItem(name,iconImage=img,thumbnailImage=img)
		item.setInfo(type="Video", infoLabels={"title":name})
		if not fanart:fanart=joinpath(home,'fanart.jpg')
		item.setProperty('Fanart_Image',fanart)
		li='%s?name=%s&url=%s&img=%s&fanart=%s&mode=%d&page=%d&query=%s'
		li=li%(sys.argv[0],urllib.quote(name),xquote(link),xquote(img),xquote(fanart),mode,page,query)
		if not isFolder:item.setProperty('IsPlayable', 'true')
		if menu:#info={'name':'','url':'','img':'','fanart':'','query':''}
			cmd='RunPlugin(plugin://%s/?mode=%d'%(myaddon.getAddonInfo('id'),mode);items=list()
			for label,info in menu:
				name=info.get('name');url=info.get('url');img=info.get('img')
				fanart=info.get('fanart');query=info.get('query')
				command=cmd+'&name=%s&url=%s&img=%s&fanart=%s&query=%s)'%(name,url,img,fanart,query)
				items.append(('[COLOR lime]%s[/COLOR]'%label,command))
			item.addContextMenuItems(items)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),li,item,isFolder)

	if query=='phimmoi.net':
		name=color['search']+"Search trên phimmoi.net[/COLOR] (Chọn độ phân giải max trên settings nhé)"
		addir(name,'http://www.phimmoi.net/tim-kiem/',icon['phimmoi'],mode=mode,query='search',isFolder=True)
		name=color['search']+'Tủ phim trên phimmoi.net của tôi[/COLOR]'
		addir(name,'http://www.phimmoi.net/tu-phim/',img,'',mode,1,'readpage',True)
		body=makerequest(joinpath(tempfolder,'phimmoi.html'))
		print joinpath(tempfolder,'phimmoi.html')
		content=xsearch('<ul id=".+?"(.+?)</ul></div>',body,1)
		for title in re.findall('<a>(.+?)</a>',content):
			addir(namecolor('0'+title),'',icon['phimmoi'],mode=mode,query='menubar',isFolder=True)
		for href,title in re.findall('<a href="([\w|-]+/|http://www.phimmoi.net/tags/.*?)">(.+?)</a>',content):
			addir(namecolor('0-'+title),href,icon['phimmoi'],'',mode,1,'menubar',isFolder=True)
		for title in re.findall('<h2 class="right-box-header star-icon"><span>(.+?)</span>',body):
			if title=='Phim đã đánh dấu':continue
			addir(namecolor('0+'+title),'right-box',img,'',mode,1,'menubar',True)
		for title,content in re.findall('<h2 class="hidden">(.+?)</h2>(.+?)</div></li></ul>',body):
			addir('[COLOR lime]%s[/COLOR]'%title,'',img,'',mode,1,'no')
			pattern='title="(.+?)" href="(.+?)".+?\(\'(http.+?)\'\).+?</div></a>(.+?)</div></li>'
			addir_pm(re.findall(pattern,content))#title,href,img,detail
		for label,content in re.findall('class="title-list-index">(.+?)</span>(.+?)</div></div></div>',body):
			addir('[COLOR lime]%s[/COLOR]'%label,'',img,'',mode,1,'no')
			pattern='<li><a href="(.+?)" title="(.+?)">.+?<img src="(.+?)".+?<h3(.+?)</p>'
			items=re.findall(pattern,content)
			if items:addir_pm([(s[1],s[0],s[2],s[3]) for s in items])#title,href,img,detail
			else:
				pattern='"movie-item m-block" title="(.+?)" href="(.+?)".+?(http.+?\.jpg).+?<div(.+?)</div></a></li>'
				addir_pm(re.findall(pattern,content))#title,href,img,detail
		if checkupdate('phimmoi.html',tempfolder)>8:
			endxbmc();makerequest(joinpath(tempfolder,'phimmoi.html'),make_request('http://www.phimmoi.net/'),'w')
	elif query=='search':make_mySearch('','phimmoi.net','','',mode,'get')
	elif query=="INP":pm_search(make_mySearch('',url,'','','','Input'))
	elif url=='phimmoi.net':page=1 if 'Trang tiếp theo' not in name else page;pm_search(query)
	elif query=='menubar':
		if any(s for s in ['kinh','rap','tags','trailer'] if s in url):
			if 'tags' not in url:url=home+url
			return phimmoi(name,url,img,mode,page,'readpage')
		elif url=='right-box':
			pattern='<span>%s</span>(.+?</li></ul></div></div>)'%re.sub('\[/?COLOR.*?\]','',name).strip()
			content=xsearch(pattern,makerequest(joinpath(tempfolder,'phimmoi.html')),1)
			pattern='title="(.+?)" href="(.+?)">.+?\(\'(.+?)\'\).+?</span>(.+?)</a></li>'
			addir_pm(re.findall(pattern,content),name)#title,href,img,detail
		else:
			content=xsearch('<ul id=".+?"(.+?)</ul></div>',makerequest(joinpath(tempfolder,'phimmoi.html')),1)
			gen={'Thể loại':'the-loai','Quốc gia':'quoc-gia','Phim lẻ':'phim-le','Phim bộ':'phim-bo'}
			query=gen.get(re.sub('\[/?COLOR.*?\]|\(.+?\)','',name).strip())
			pattern='<a href="(%s/.*?)">(.+?)</a>'%query
			for href,title in re.findall(pattern,content):
				addir(namecolor('1'+title),home+href,icon['phimmoi'],'',mode,1,'readpage',True)
	elif query=='readpage':
		if url=='http://www.phimmoi.net/tu-phim/':
			hd['Cookie']=makerequest(joinpath(datapath,'phimmoi.cookie'))
			body=make_request(url,headers=hd);token=xsearch("fx\.token='(.+?)'",body,1);menu1='Remove from Tủ phim'
			if not token:
				hd['Cookie']=login_pm();body=make_request(url,headers=hd)
		else:body=make_request(url);menu1='Add to Tủ phim'
		print url
		for content in re.findall('<li class="movie-item">(.+?)</li>',body,re.DOTALL):
			title=xsearch('title="(.+?)"',content,1);href=xsearch('href="(.+?)"',content,1)
			print title
			img=xsearch('\((http.+?)\)',content,1);detail=' '.join(re.findall('<span(.+?)</span>',content))
			title,href,img,query,isFolder=get_info(title,href,img,detail)
			menu=[(menu1,{'name':menu1,'url':href,'query':'tuphim'})]
			pm_addir('2'+title,href,img,'',mode,page,query,isFolder,menu)
		urlnext=xshare_group(re.search('<li><a href="(.+?)">Trang kế.+?</a></li>',body),1)
		if urlnext:
			pagenext=xshare_group(re.search('/page-(\d{1,3})\.html',urlnext),1)
			name='%sTrang tiếp theo: trang %s[/COLOR]'%(color['trangtiep'],pagenext)
			addir(name,home+urlnext,img,fanart,mode,page,'readpage',True)
	elif query=='tuphim':
		hd['Cookie']=makerequest(joinpath(datapath,'phimmoi.cookie'))
		token=xsearch("fx\.token='(.+?)'",make_request('http://www.phimmoi.net/tu-phim/',headers=hd),1)
		if not token:
			hd['Cookie']=login_pm()
			token=xsearch("fx\.token='(.+?)'",make_request('http://www.phimmoi.net/tu-phim/',headers=hd),1)
		data={'_fxAjax':'1','_fxResponseType':'JSON','_fxToken':'%s'%token}
		action='add' if 'Add' in name else 'remove'
		response=make_post('%s%s.html'%(url,action),hd,data,resp='j')
		if response.get('_fxStatus',0)==1:
			mes(response.get('_fxMessage','success'))
			if action=='remove':xbmc.executebuiltin("Container.Refresh")
		else:
			try:mes(response.get('_fxErrors')[0])
			except:mes(u'Đã phát sinh lỗi!')
	elif query=='pmfolder':
		body=make_request(url+'xem-phim.html');name=re.sub('\[/?COLOR.*?\]|\(.+?\)|\d{1,3} phút','',name).strip()
		for detail in re.findall('data-serverid="pcs"(.+?)</li></ul></div>',body,re.DOTALL):
			title=' '.join(s for s in xsearch('<h3 class="server-name">(.+?)</h3>',detail,1,re.DOTALL).split())
			if title and 'tập phim' not in title:addir('[COLOR lime]%s[/COLOR]'%title,'',img,'',mode,1,'no')
			label=name.replace('TM ','') if title and 'Thuyết minh' not in title else name
			for title,href in re.findall('title="(.+?)".+?href="(.+?)"',detail,re.DOTALL):
				addir(title+' '+label,home+href,img,fanart,mode,page,query='pmplay')
	#elif query=='pmplay':
	href='http://www.phimmoi.net/player/v1.46/plugins/gkplugins_picasa2gdocs/plugins/plugins_player.php?url=%s'
	link_youtube=url;pyoutube="trailerUrl='(https://www.youtube.com/.+?)'"
	if '.html' not in url:url=url+'xem-phim.html'
	content=make_request(url,resp='o');hd['Cookie']=content.cookiestring
	print content.body
	content=sub_body(content.body,'- slider -','- Sidebar -')
	if not content:return play_youtube(xsearch(pyoutube,make_request(link_youtube),1))
	pattern='data-language="(.+?)".*href="(.+?)">.*\s.*Xem Full'
	links=dict(re.findall(pattern,content));body={};pattern="currentEpisode.url='(.+?)'"
	if not links:#Khong co ban full
		eps=[s.replace('\\','') for s in re.findall('({"episodeId":.+?})',content)]
		if not eps:body={};a=1
		elif len(eps)==1:body=make_post(href%geteps(eps[0])[0],headers=hd,resp='j');a=2
		elif xshare_group(re.search('Part (\d{1,3}) - ',name),1):
			part_id=int(xshare_group(re.search('Part (\d{1,3}) - ',name),1));epiurl='';a=3
			for epi in eps:
				if geteps(epi)[1]==part_id:epiurl=geteps(epi)[0];break
			body=make_post(href%epiurl,headers=hd,resp='j') if epiurl else ''
		elif 'xem-phim.html' not in url:
			print href%xshare_group(re.search(pattern,content),1)
			body=make_post(href%xshare_group(re.search(pattern,content),1),headers=hd,resp='j');a=4
		else:make_eps(url,eps);body=make_post(href%geteps(eps[0])[0],headers=hd,resp='j');a=5
	elif len(links)==1:#Chi co 1 ban full
		body=make_post(href%xshare_group(re.search(pattern,make_request(home+links.values()[0])),1),headers=hd,resp='j');a=6
	elif myaddon.getSetting('phimmoiaudio')=='true' and links.has_key('illustrate'):#sub Vie
		body=make_post(href%xshare_group(re.search(pattern,make_request(home+links['illustrate'])),1),headers=hd,resp='j');a=7
	elif links.has_key('subtitle'):#sub Eng
		body=make_post(href%xshare_group(re.search(pattern,make_request(home+links['subtitle'])),1),headers=hd,resp='j');a=8
	height=0;url='';maxresolution=int(myaddon.getSetting('phimmoiresolution'))
	for item in [s for s in body.get("content",list()) if 'video' in s.get('type')]:
		if item.has_key('height') and item['height']==maxresolution:url=item['url'];break
		elif item.has_key('height') and item['height']>height:height=item['height'];url=item['url']
	if not url:mess(u'[COLOR red]Không get được maxspeedlink hoặc link bị die[/COLOR]')
	else:xbmcsetResolvedUrl(url)
			
def xsearch(pattern,string,group,flags=0):
	research=re.search(pattern,string,flags)
	if research:
		try:result=research.group(group)
		except:result=''
	else:result=''
	return result
			
def additemshdviet(body, danhmucphim):
	pattern='<li class="mov-item".+?href="(.+?)".+?src="(.+?)".+?title="Phim (.+?)".+?<span(.+?) data-id="(.+?)">'
	#print body;return
	data=re.findall(pattern,body,re.DOTALL);listitems=list()
	for href,img,title,detail,id_film in data:
		epi=xsearch('"labelchap2">(\d{1,3})</span>',detail,1);title=unescape(title)
		res=xsearch('id="fillprofile" class="icon-(.+?)11">',detail,1)
		res='[COLOR gold]SD[/COLOR]' if 'SD' in res else '[COLOR gold]HD[/COLOR]%s'%res
		phim18=xsearch('class="children11".+?>(.+?)</label></span>',detail,1)
		TM=xsearch('id="fillaudio" class="icon-(.+?)">',detail,1)
		TM='%s[COLOR green]%s[/COLOR][COLOR red]%s[/COLOR]'%(res,TM,phim18)
		plot=xsearch('<span class="cot1">(.+?)</span>',detail,1)
		year=xsearch('<span class="chil-date".+?>(.*?)</label></span>',detail,1)
		act=', '.join(s for s in re.findall('<a href="http://movies.hdviet.com/dien-vien/.+?">(.+?)</a>',detail))
		drt=', '.join(s for s in re.findall('<a href="http://movies.hdviet.com/dao-dien/.+?">(.+?)</a>',detail))
		rat=xsearch('<span class="fl-left">.+?<span>(.+?)</span>',detail,1)
		upl=xsearch('<span class="fl-right">.+?<span>(.+?)</span>',detail,1)
		
		page=1
		if not epi:
			mode='22'
			#title=TM+' '+title;
			query='hdvietplay'			
		#elif epi=='1':query='hdvietfolder'
		else:
			mode='episodes'
			title = color['phimbo']+title+'[/COLOR]'
			#title=TM+' '+title+' [COLOR green](%s)[/COLOR]'%epi;
			query='hdvietfolder'	
		
		if danhmucphim != 'Tất cả':
			query='qua nhanh'
		elif mode == 'episodes':
			query=id_film
			id_film='hdviet.com'						
		
		listItem = xbmcgui.ListItem(label=title,iconImage=img,thumbnailImage=img)
		if rat:rat='[COLOR tomato]IMDb:[/COLOR] %s, '%rat
		if upl:upl='[COLOR tomato]Uploader:[/COLOR] %s, '%upl
		if act:act='[COLOR tomato]Diễnviên:[/COLOR] %s, '%act
		if drt:drt='[COLOR tomato]Đạodiễn:[/COLOR] %s, '%drt
		plot=rat+upl+act+drt+'\n'+plot
		info={'title':title,'year':year,'rating':xsearch('(\d\.\d{1,2})',rat,1),'plot':plot,'episode':epi,'director':drt,'writer':act}
		listItem.setInfo(type="Video", infoLabels=info)
		#listItem.setArt({"thumb":img,"poster":img,"fanart":img})		
		if query=='hdvietplay':listItem.setProperty('IsPlayable', 'true')
		u=sys.argv[0]+"?url="+id_film+"&img="+urllib.quote_plus(img)+"&fanart="+urllib.quote_plus(img)+"&mode="+str(mode)+"&page="+str(page)+"&query="+query+"&name="+title		
		listitems.append((u,listItem,False if query=='hdvietplay' else True))
	xbmcplugin.addDirectoryItems(int(sys.argv[1]),listitems,totalItems=len(listitems))			