#!/usr/bin/python
# -*- coding: utf-8 -*-
#plugin.video.hdviet / Tác giả: Anphunl
import urllib, urllib2, json, re, urlparse, sys, time, os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from BeautifulSoup import BeautifulSoup

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
#args = urlparse.parse_qs(sys.argv[2][1:])

#xbmcplugin.setContent(addon_handle, 'movies')

my_addon = xbmcaddon.Addon()
subtitle_lang = 'VIE'
video_quality = my_addon.getSetting('video_quality') == 'HD'
use_vi_audio = 'true'
use_dolby_audio= 'true'
#reload(sys);

fixed_quality = (video_quality != 'Chọn khi xem')

min_width = {'SD' : 0, 'HD' : 1024, 'Full HD' : 1366}
max_width = {'SD' : 1024, 'HD' : 1366, 'Full HD' : 10000}

header_web = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
			'Content-type': 'application/x-www-form-urlencoded',
			'Referer' : 'http://www.google.com'}
header_app = {'User-agent' : 'com.hdviet.app.ios.HDViet/2.0.1 (unknown, iPhone OS 8.2, iPad, Scale/2.000000)'}

def make_request(url, params=None, headers=None):
	if headers is None:
		headers = header_web
	try:
		if params is not None:
			params = urllib.urlencode(params)
		req = urllib2.Request(url,params,headers)
		f = urllib2.urlopen(req)
		body=f.read()
		f.close()
		return body
	except:
		pass

def play2(movie_id, ep = 0):
	# get link to play and subtitle
	movie = json.loads(make_request('https://api-v2.hdviet.com/movie/play?movieid=%s&sign=sign&ep=%s' % (movie_id, ep), None, header_app))['r']
	print movie
	print '1111'
	
def play(movie_id, ep = 0):

	# get link to play and subtitle
	movie = json.loads(make_request('https://api-v2.hdviet.com/movie/play?movieid=%s&sign=sign&ep=%s' % (movie_id, ep), None, header_app))['r']
	
	if movie:
		subtitle_url = ''
		if subtitle_lang != 'Tắt':
			try:
				subtitle_url = movie['Subtitle'][subtitle_lang]['Source']
				if subtitle_url == '':
					subtitle_url = movie['SubtitleExt'][subtitle_lang]['Source']
				if subtitle_url == '':
					subtitle_url = movie['SubtitleExtSe'][subtitle_lang]['Source']
			except:
				pass

		# get link and resolution
		link_to_play = re.sub(r'_\d+_\d+_', '_320_4096_', movie['LinkPlay'])
		result = make_request(link_to_play, None, header_app)
		print link_to_play
		print result

		# audioindex
		audio_index = 0
		if (use_vi_audio and movie['Audio'] > 0) or (movie['Audio'] == 0 and use_dolby_audio):
			audio_index = 1
		
		playable_items = []
		lines = result.splitlines()

		i = 0
		# find the first meaning line
		while (i < len(lines)):
			if 'RESOLUTION=' in lines[i]:
				break
			i += 1
		while (i < len(lines)):
			playable_item = {}
			playable_item['res'] = lines[i][lines[i].index('RESOLUTION=') + 11:]

			if lines[i + 1].startswith('http'):
				playable_item['url'] = lines[i + 1]
			else:
				playable_item['url'] = movie['LinkPlay'].replace('playlist.m3u8', lines[i + 1])

			playable_items.append(playable_item)
			i += 2

		if not fixed_quality:
			for item in playable_items:
				addMovie(item['res'], {'mode':'play_url', 'stream_url' : '%s?audioindex=%d' % (item['url'], audio_index), 'subtitle_url' : subtitle_url}, '', '')
		else:
			i = len(playable_items) - 1
			while (i >= 0):
				current_width = int(playable_items[i]['res'].split('x')[0])
				if (min_width[video_quality] <= current_width and max_width[video_quality] > current_width) or current_width < min_width[video_quality]:
					break
				i -= 1

			if i >= 0:
				set_resolved_url('%s?audioindex=%d' % (playable_items[i]['url'], audio_index), subtitle_url)

	
def set_resolved_url(stream_url, subtitle_url):
	print stream_url
	h1 = '|User-Agent=' + urllib.quote_plus('HDViet/2.0.1 CFNetwork/711.2.23 Darwin/14.0.0')
	h2 = '&Accept=' + urllib.quote_plus('*/*')
	h3 = '&Accept-Language=' + urllib.quote_plus('en-us')
	h4 = '&Connection=' + urllib.quote_plus('Keep-Alive')
	h5 = '&Accept-Encoding=' + urllib.quote_plus('gzip, deflate')
	xbmcplugin.setResolvedUrl(addon_handle, succeeded=True, listitem=xbmcgui.ListItem(label = '', path = stream_url + h1 + h2 + h3 + h5))
	player = xbmc.Player()
	
	subtitlePath = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('path')).decode("utf-8")
	subfile = xbmc.translatePath(os.path.join(subtitlePath, "temp.sub"))
	try:
		if os.path.exists(subfile):
			os.remove(subfile)
		f = urllib2.urlopen(subtitle_url)
		with open(subfile, "wb") as code:
			code.write(f.read())
		xbmc.sleep(3000)
		xbmc.Player().setSubtitles(subfile)
	except:
		pass
	
	for _ in xrange(30):
		if player.isPlaying():
			break
		time.sleep(1)
	else:
		raise Exception('No video playing. Aborted after 30 seconds.')