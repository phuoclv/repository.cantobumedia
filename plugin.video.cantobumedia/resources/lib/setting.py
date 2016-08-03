import xbmcaddon, xbmc, os, xbmcgui
import base64

myaddon = xbmcaddon.Addon()
addonID = xbmcaddon.Addon('plugin.video.cantobumedia')

def alert(message,title="Cantobu Media"):
	xbmcgui.Dialog().ok(title,"",message)

def notify(message, timeout=5000, image=None):
  	if image is None:
		home = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('path')).decode("utf-8")	
    	image = xbmc.translatePath(os.path.join(home, "icon.png"))
	xbmc.executebuiltin((u'XBMC.Notification("%s", "%s", "%d", "%s")' % ('Cantobu Media', message, timeout, image)).encode("utf-8"))
	
def encode2(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = (ord(clear[i]) + ord(key_c)) % 256
        enc.append(enc_c)
    return base64.urlsafe_b64encode(bytes(enc))

def decode2(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc)
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + enc[i] - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)

def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc))
	
def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc)
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)
	