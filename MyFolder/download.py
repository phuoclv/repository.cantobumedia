def download():
	icon_check='icon_12222016.txt'
	version_new='1.0.17'

	file=os.path.join(addonDataPath,icon_check)
	if not os.path.isfile(file):
		notify(u'Đang kiểm tra và tải dữ liệu');delete_files(tempfolder)
		tempfile = os.path.join(tempfolder,"data.zip")
		href=decode('ROOT', 'usPDxIx-frezvcPDtMTCvMG_fbfBvH6slJySgw==')+'icon.zip'
		response=xfetch(href)
		if response.status==200:
			body=makerequest(tempfile,response.body,'wb');xbmc.sleep(1000)
			try:
				xbmc.executebuiltin('XBMC.Extract("%s","%s")'%(tempfile,addonDataPath), True)
				makerequest(joinpath(addonDataPath,file),'','w')
				notify(u'Tải dữ liệu thành công')				
			except:notify(u'Tải dữ liệu lỗi!')			
		else:notify(u'Tải dữ liệu không thành công!')			
		
	version=myaddon.getAddonInfo('version')	
	if version_new != version:
		try:
			if checkupdate('last_update.dat',24,addonDataPath):
				makerequest(joinpath(addonDataPath,"last_update.dat"),'','w')
				#path='https://github.com/phuoclv/repository.cantobumedia/raw/master/plugin.video.cantobumedia/plugin.video.cantobumedia-%s.zip'%version_new
				path='https://github.com/phuoclv/repository.cantobumedia/raw/master/repository.cantobumedia/repository.cantobumedia-1.0.1.zip'
				repo_zip = xbmc.translatePath(os.path.join(tempfolder,"tmp.zip"))
				urllib.urlretrieve(path,repo_zip)
				with contextlib.closing(zipfile.ZipFile(repo_zip, "r")) as z:
					z.extractall(addons_folder)			
					
				xbmc.executebuiltin("XBMC.UpdateLocalAddons()")
				xbmc.executebuiltin("XBMC.UpdateAddonRepos()")				
				#xbmcgui.Dialog().ok('Cantobu Media', "Đã cập nhật phiên bản [B]%s[/B]."%version_new)
		except:pass
		
def UpdateDB(query):
	query=query.lower()
	movie_check='%s_12172016.txt'%query		
	file=os.path.join(addonDataPath,movie_check)
	
	filename='2@%s_movie.xml'%query
	filename_check=os.path.join(datapath,filename)
	try:					
		if not os.path.isfile(filename_check) or not os.path.isfile(file):
			v_query='Phim lẻ' if query=='phim-le' else 'Phim bộ'									
			notify(u'Đang cập nhật dữ liệu...',v_query,timeout=5000);delete_files(tempfolder)
			
			filedownload='2@%s_movie.zip'%query
			tempfile = os.path.join(tempfolder,filedownload)		
			#href=decode('ROOT', 'usPDxIx-frezvcPDtMTCvMG_fbfBvH6slJySgw==')+filedownload
			href=decode('GitHub_ROOT', 'r93ouOicjoHBsMt10N283dfBx8K0xqrY4rza0NOAsr7BdtncveTFy8h-wbm32Oex6dHRy32ytbXd46rqz8S2uLCDtMrnvNrUjp_IlcOzzdm6pA==')+filedownload
			response=xfetch(href)
			if response.status==200:
				body=makerequest(tempfile,response.body,'wb');xbmc.sleep(1000)
				try:					
					xbmc.executebuiltin('XBMC.Extract("%s","%s")'%(tempfile,datapath), True)					
					makerequest(joinpath(addonDataPath,file),'','w')
					notify(u'Cập nhật dữ liệu thành công.',v_query)					
				except:notify(u'Đã xảy ra lỗi cập nhật!',v_query,timeout=2000)
			else:notify(u'Cập nhật dữ liệu không thành công!',v_query)
	except:pass