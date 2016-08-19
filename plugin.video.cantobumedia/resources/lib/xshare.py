__author__ = 'thaitni'
# -*- coding: utf-8 -*-
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,urllib,urllib2,re,os,unicodedata,datetime,time,random,json,sys

myaddon=xbmcaddon.Addon()
home=xbmc.translatePath(myaddon.getAddonInfo('path'));datapath=xbmc.translatePath(myaddon.getAddonInfo('profile'))
iconpath=os.path.join(datapath,'icon');datapath=os.path.join(datapath,'data')
sys.path.append(os.path.join(home,'resources','lib'));from urlfetch import get,post
search_file=os.path.join(datapath,"search.xml");data_path=os.path.join(home,'resources','data')
tempfolder=xbmc.translatePath('special://temp')

media_ext=['aif','iff','m3u','m3u8','m4a','mid','mp3','mpa','ra','wav','wma','3g2','3gp','asf','asx','avi','flv','mov','mp4','mpg','mkv','m4v','rm','swf','vob','wmv','bin','cue','dmg','iso','mdf','toast','vcd','ts','flac','m2ts','dtshd','nrg'];icon={}
color={'fshare':'[COLOR gold]','vaphim':'[COLOR gold]','phimfshare':'[COLOR khaki]','4share':'[COLOR blue]','tenlua':'[COLOR fuchsia]','fptplay':'[COLOR orange]','trangtiep':'[COLOR lime]','search':'[COLOR lime]','ifile':'[COLOR blue]','hdvietnam':'[COLOR red]','hdviet':'[COLOR darkorange]','xshare':'[COLOR blue]','subscene':'[COLOR green]','chiasenhac':'[COLOR orange]','phimmoi':'[COLOR ghostwhite]','megabox':'[COLOR orangered]','dangcaphd':'[COLOR yellow]','hayhaytv':'[COLOR tomato]','kenh88':'[COLOR cyan]','phimdata':'[COLOR magenta]','phim47':'[COLOR springgreen]','phimsot':'[COLOR orangered]','hdonline':'[COLOR turquoise]','phim3s':'[COLOR lightgray]','kphim':'[COLOR lightgreen]','phimnhanh':'[COLOR chartreuse]','bilutv':'[COLOR hotpink]','pubvn':'[COLOR deepskyblue]','anime47':'[COLOR deepskyblue]','phim14':'[COLOR chartreuse]','taifile':'[COLOR cyan]','phim':'[COLOR orange]','tvhay':'[COLOR gold]','nhacdj':'[COLOR fuchsia]','phimbathu':'[COLOR lightgray]','taiphimhd':'[COLOR blue]','hdsieunhanh':'[COLOR orangered]','vuahd':'[COLOR tomato]','nhaccuatui':'[COLOR turquoise]','imovies':'[COLOR orange]','vietsubhd':'[COLOR cyan]','imax':'[COLOR chartreuse]','mphim':'[COLOR deepskyblue]','vtvgo':'[COLOR green]','youtube':'[COLOR red]'}
for hd in ['xshare','4share','dangcaphd','downsub','favorite','fptplay','fshare','gsearch','hdvietnam','icon','id','ifiletv','ifile','isearch','khophim','maxspeed','megabox','movie','msearch','myfolder','myfshare','phimfshare','serverphimkhac','setting','tenlua','vaphim','hdviet','hayhaytv','chiasenhac','kenh88','phimdata','phim47','phimsot','hdonline','phim3s','kphim','phimnhanh','bilutv','anime47','phim14','taifile','phim','tvhay','nhacdj','phimbathu','taiphimhd','hdsieunhanh','phimmoi','vuahd','pubvn','nhaccuatui','imovies','vietsubhd','imax','mphim','vtvgo','youtube']:
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

subsfolder=joinpath(tempfolder,'subs')
	
def xshare_download(direct_link):
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

	def checkmedia(file):
		return os.path.isfile(file) and os.path.getsize(file)>1024**2 and os.path.splitext(file)[1][1:] in media_ext

	response,size,filename,ext=get_detail_maxlink(direct_link)
		
	temp_path=joinpath(tempfolder,'temp');mediafile=False
	if not os.path.exists(temp_path):os.mkdir(temp_path)
	else:delete_folder(temp_path)
	tempfile=joinpath(temp_path,'tempfile.%s'%ext)
	
	if size<1024**2:#sub file
		delete_folder(subsfolder)#if myaddon.getSetting('autodel_sub')=='true':delete_folder(subsfolder)
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
		#mess(u'Đã download sub vào Subsfolder','Subs Downloader')
		return joinpath(subsfolder,'Vie.%s'%filename)
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