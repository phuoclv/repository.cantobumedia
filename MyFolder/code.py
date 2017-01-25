def UpdateDB(query,server,page=1):
	content_old=makerequest(joinpath(datapath,'2@%s_movie.xml'%query))		
	#href_old=re.findall('titleEn="(.*?)" year="(.*?)"',content_old)
	href_old=re.findall('year="(.*?)" title=".*\[\](.*?)"',content_old)#titleEn
	href_old2=re.findall('year="(.*?)" title="(.*?)\[\].*"',content_old)#titleVn	
			
	filename_new='2@%s_%s.xml'%(query,server)
	content_new=makerequest(joinpath(datapath,filename_new))	
	if page:r='<a id="(%03d)" category="(.*?)" parent="(.+?)" tag="(.*?)" titleEn="(.*?)" year="(.*?)" title="(.+?)">(.+?)</a>'%(page)
	else:r='<a id="(.*?)" category="(.*?)" parent="(.+?)" tag="(.*?)" titleEn="(.*?)" year="(.*?)" title="(.+?)">(.+?)</a>'
	items_insert=re.findall(r,content_new)
	#print len(items_insert)
	
	items_new=[]						
	count_href=0

	#[s for s in items_insert if (s[4].lower(),s[5]) not in href_old]	
	#for id,category,parent,tag,titleEn,year,title,info in items_insert:
	for id,category,parent,tag,titleEn,year,title,info in [s for s in items_insert if (s[5],s[6].split('[]')[1]) not in href_old and (s[5],s[6].split('[]')[0]) not in href_old2]:
		j = json.loads(info)				
		for i in j["href"]:				
			href=u2s(i["url"])
		
		titleVn = u2s(j.get("titleVn"));titleEn = u2s(j.get("titleEn"));year = u2s(j.get("year"))

		if False:
			id = u2s(j.get("id"));
			v_href=''
			for i in j["href"]:				
				if server=='phimmoi':id=xsearch('-(\d+?)\/',u2s(i["url"]))
				else:id=xsearch('-(\d+?)\.html',u2s(i["url"]))

				v_url='{"label":"","url":'+json.dumps(u2s(i["url"]))+',"subtitle":'+json.dumps(u2s(i["subtitle"]))+'}'
				if v_href:v_href+=','+v_url
				else:v_href=v_url
			
			rating = u2s(j.get("rating"));plot = u2s(j.get("plot"))
			episode = u2s(j.get("episode"));director = u2s(j.get("director"));writer = u2s(j.get("writer"));country = u2s(j.get("country"));genre = u2s(j.get("genre"))
			duration = u2s(j.get("duration"));thumb = u2s(j.get("thumb"))
				
			info='{'
			info+='"id":"'+server+'-'+id+'"'
			info+=',"href":['+v_href+']'
			info+=',"titleVn":'+json.dumps(titleVn)		
			info+=',"titleEn":'+json.dumps(titleEn)
			info+=',"country":'+json.dumps(country)
			info+=',"genre":'+json.dumps(genre)
			info+=',"year":'+json.dumps(year)
			info+=',"writer":'+json.dumps(writer)
			info+=',"director":'+json.dumps(director)
			info+=',"duration":'+json.dumps(duration)
			info+=',"thumb":'+json.dumps(thumb)
			info+=',"rating":'+json.dumps(rating)				
			info+=',"episode":'+json.dumps(episode)				
			info+=',"plot":'+json.dumps(plot)
			info+='}'
			info=info.replace('/','\/')		
			
			titleVn = fixString(titleVn);titleEn = fixString(titleEn)
			title = titleVn + '[]' + titleEn if titleEn else titleVn		
			items_new.append(('ok',category,parent,tag,titleEn if titleEn else titleVn,year,title,info))
			continue

		titleVn = fixString(titleVn);titleEn = fixString(titleEn)
		title = titleVn + '[]' + titleEn if titleEn else titleVn		
		#if ('hdonline' in href or 'megabox' in href):
		items_new.append(('ok',category,parent,tag,titleEn if titleEn else titleVn,year,title,info))						
	####
	
	#try:
	v_query=u'Phim lẻ' if query=='phim-le' else u'Phim bộ'
	filename='2@%s_movie.xml'%query
	if count_href and False:
		if makerequest(joinpath(datapath,filename),content_old,'w'):
			notify(u'Đã cập nhật thêm %d link khác'%count_href,v_query)
										
	if items_new:			
		contents='<?xml version="1.0" encoding="utf-8">\n'
		for id,category,parent,tag,titleEn,year,title,info in items_new:
			content='<a id="%s" category="%s" parent="%s" tag="%s" titleEn="%s" year="%s" title="%s">%s</a>\n'						
			content=content%(id,category,parent,tag,titleEn,year,title,info);contents+=content
			
		contents+=content_old.replace('<?xml version="1.0" encoding="utf-8">\n','')
		if makerequest(joinpath(datapath,filename),contents,'w'):				
			notify(u'Đã cập nhật được %d phim'%len(items_new),v_query)
		else: notify(u'Đã xảy ra lỗi cập nhật!',v_query)
		
	content_new=content_new.replace('id="%03d"'%page,'id="ok"')
	makerequest(joinpath(datapath,filename_new),content_new,'w')			
	#except:print 'error!'	
	
def DownloadDB(query='phim-le',server='megabox',page=1,page_max=1,update_db=False):
	filename='2@%s_%s.xml'%(query,server)
	content_old=makerequest(joinpath(datapath,filename))
	#href_old=re.findall('"url":"(.+?)",',content_old)
	href_old=re.findall('titleEn="(.*?)" year="(.*?)"',content_old)

	items=[];
	while page <= page_max:				
		if page_max != page:notify(u'Đang tiến hành download trang %d'%(page),timeout=5000)
		if server=='megabox':			
			url = 'http://phim.megabox.vn/%s/trang-%d'%(query,page)
		elif server=='phimmoi':						
			url='http://www.phimmoi.net/%s/page-%d.html'%(query,page)			
		elif server=='phimnhanh':						
			url = 'http://phimnhanh.com/%s?page=%d'%(query,page)				
		elif server=='vaphim':
			v_query = 'series' if query=='phim-bo' else query		
			url='http://vaphim.com/category/phim-2/%s/page/%d/'%(v_query,page)			
				
		elif server=='fsharefilm':
			if page==1:url = 'http://fsharefilm.com/chuyen-muc/phim/'
			else:url = 'http://fsharefilm.com/chuyen-muc/phim/page/%d/'%page
				
		elif server=='hdonline':
			url = 'http://hdonline.vn/danh-sach/%s/trang-%d.html'%(query,page)				
		elif server=='fcine':						
			url='http://fcine.net/?page=%d&listResort=1'%(page)
		elif server=='phimbathu':						
			url='http://phimbathu.com/danh-sach/%s.html?page=%d'%(query,page)
		elif server=='bilutv':						
			url='http://bilutv.com/danh-sach/%s.html?page=%d'%(query,page)
		elif server=='vietsubhd':						
			url='http://www.vietsubhd.com/%s/trang-%d.html'%(query,page)
		elif server=='hdsieunhanh':						
			url='http://www.hdsieunhanh.com/%s.html&page=%d'%(query,page)

		items+=additems2(url,0,page)
			
		page+=1		
	####	
	if items:
		contents='<?xml version="1.0" encoding="utf-8">\n';check=0
		#for id,title,theloai,tag,titleEn,year,info in [s for s in items if json.dumps(s[4]).replace('/','\/').replace('"','') not in href_old]:
		for id,title,theloai,tag,titleEn,year,info in [s for s in items if (fixString(s[4]),s[5]) not in href_old]:
			titleVn=fixString(title);titleEn=fixString(titleEn);title=titleVn+'[]'+(titleEn if titleEn else titleVn)
			check+=1
			category='';parent=theloai
		
			content='<a id="%s" category="%s" parent="%s" tag="%s" titleEn="%s" year="%s" title="%s">%s</a>\n'			
			content=content%(id,category,parent,tag,titleEn if titleEn else titleVn,year,title,info);contents+=content
		
		v_query='Phim lẻ' if query=='phim-le' else 'Phim bộ'
		if check:			
			contents+=content_old.replace('<?xml version="1.0" encoding="utf-8">\n','')
			if makerequest(joinpath(datapath,filename),contents,'w'):
				notify(u'Đã cập nhật được %d phim'%check,u'%s - %s'%(v_query,eval("www['"+server+"']")))
			else: notify(u'Đã xảy ra lỗi cập nhật!',u'%s - %s'%(v_query,eval("www['"+server+"']")))
		else:notify(u'Không có phim mới...',u'%s - %s'%(v_query,eval("www['"+server+"']")))
		if update_db and (server=='megabox' or server=='hdonline'):
			while page_max > 0:			
				UpdateDB(query,server,page_max)
				page_max-=1	