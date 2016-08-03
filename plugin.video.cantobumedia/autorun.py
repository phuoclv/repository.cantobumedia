import xbmc, xbmcaddon

myaddon = xbmcaddon.Addon()

if myaddon.getSetting('autorun') == 'true':
	xbmc.executebuiltin("RunAddon(plugin.video.cantobumedia)")