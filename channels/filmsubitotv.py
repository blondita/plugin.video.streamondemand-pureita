# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand.- XBMC Plugin
# Canal para filmsubito.tv
# http://blog.tvalacarta.info/plugin-xbmc/streamondemand.
# ------------------------------------------------------------
import re
import urlparse

from core import config
from core import logger
from core import scrapertools
from core.item import Item
from core.tmdb import infoSod
from servers import servertools

__channel__ = "filmsubitotv"
__category__ = "F,A,S"
__type__ = "generic"
__title__ = "FilmSubito.tv"
__language__ = "IT"

host = "http://www.cinemasubito.net/"

DEBUG = config.get_setting("debug")


def isGeneric():
    return True


def mainlist(item):
    logger.info("streamondemand.filmsubitotv mainlist")
    itemlist = [Item(channel=__channel__,
                     title="[COLOR azure]Film - Novità[/COLOR]",
                     action="peliculas",
                     url=host + "film-2016-streaming.html",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/popcorn_cinema_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film per Genere[/COLOR]",
                     action="genere",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/genres_P.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Film per Anno[/COLOR]",
                     action="anno",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/movie_year_P.png"),
                # Item(channel=__channel__,
                # title="[COLOR azure]Serie TV degli anni '80[/COLOR]",
                # action="serie80",
                # url=host,
                # thumbnail="http://cdn8.staztic.com/app/i/4296/4296926/hey-guess-the-80s-pop-culture-fun-free-trivia-quiz-game-with-movies-song-icon-character-celebrities-logo-and-tv-show-from-the-80s-1-l-280x280.png"),
                Item(channel=__channel__,
                     title="[COLOR azure]Cartoni animati degli anni '80[/COLOR]",
                     action="cartoni80",
                     url=host,
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/cartoons_P.png"),
                # Item(channel=__channel__,
                # title="[COLOR azure]Documentari[/COLOR]",
                # action="documentari",
                # url=host,
                # thumbnail="http://repository-butchabay.googlecode.com/svn/branches/eden/skin.cirrus.extended.v2/extras/moviegenres/Documentary.png"),
                Item(channel=__channel__,
                     title="[COLOR yellow]Cerca...[/COLOR]",
                     action="search",
                     thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/channels_icon_pureita/search_P.png")]
    # itemlist.append( Item(channel=__channel__, title="[COLOR azure]Serie TV[/COLOR]", action="peliculas", url=sito+"serietv-streaming.html", thumbnail="http://xbmc-repo-ackbarr.googlecode.com/svn/trunk/dev/skin.cirrus%20extended%20v2/extras/moviegenres/New%20TV%20Shows.png"))

    return itemlist


def search(item, texto):
    logger.info("[filmsubitotv.py] " + item.url + " search " + texto)
    item.url = host + "search.php?keywords=" + texto
    try:
        return peliculas(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def peliculas(item):
    logger.info("streamondemand.filmsubitotv peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)
    patron = '<h3 dir="ltr"><a href="([^"]+)"[^>]+>(.*?)</a></h3>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvid",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title=scrapedtitle,
                 url=scrapedurl,
                 plot=scrapedplot,
                 thumbnail=scrapedthumbnail,
                 folder=True), tipo='movie'))

    # Extrae el paginador
    patronvideos = '<a href="([^"]+)">&raquo;</a>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="HomePage",
                 title="[COLOR yellow]Torna Home[/COLOR]",
                 folder=True)),
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/vari/successivo_P.png",
                 folder=True))

    return itemlist


def serietv80(item):
    logger.info("streamondemand.filmsubitotv serietv80")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)
    patron = '<span class="pm-video-li-thumb-info".*?'
    patron += 'href="([^"]+)".*?'
    patron += 'src="([^"]+)" '
    patron += 'alt="([^"]+)".*?'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle).strip()
        if (DEBUG): logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 folder=True,
                 fanart=scrapedthumbnail))

    # Extrae el paginador
    patronvideos = '<a href="([^"]+)">&raquo;</a>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 extra=item.extra,
                 action="serietv80",
                 title="[COLOR orange]Successivo>>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/vari/successivo_P.png",
                 folder=True))

    return itemlist


def genere(item):
    logger.info("[filmsubitotv.py] genere")
    itemlist = []

    data = scrapertools.cache_page(item.url)

    patron = '<li class=".*?"><a title="([^"]+)" alt=".*?" href="([^"]+)" class="">.*?</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedtitle, scrapedurl in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle).strip()
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title=scrapedtitle,
                 url=scrapedurl,
                 folder=True))

    return itemlist


def serie80(item):
    logger.info("[filmsubitotv.py] genere")
    itemlist = []

    data = scrapertools.cache_page(item.url)

    #    patron = '<a href="#" class="dropdown-toggle wide-nav-link" data-toggle="dropdown">Serie anni 80<b class="caret"></b></a>(.*?)<li class="dropdown">'
    #    data = scrapertools.find_single_match(data, patron)

    patron = '<li class=".*?" ><a title="([^"]+)" alt=".*?" href="([^"]+)">.*?</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedtitle, scrapedurl in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle).strip()
        itemlist.append(
            Item(channel=__channel__,
                 action="serietv80",
                 title=scrapedtitle,
                 url=scrapedurl,
                 folder=True))

    return itemlist


def anno(item):
    logger.info("[filmsubitotv.py] genere")
    itemlist = []

    data = scrapertools.cache_page(item.url)

    patron = '<a href="#" class="dropdown-toggle wide-nav-link" data-toggle="dropdown">Anno<b class="caret"></b></a>(.*?)<li class="dropdown">'
    data = scrapertools.find_single_match(data, patron)

    patron = '<a.*?href="([^"]+)">(.*?)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle).strip()
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title=scrapedtitle,
                 url=scrapedurl,
                 folder=True))

    return itemlist


def cartoni80(item):
    logger.info("[filmsubitotv.py] genere")
    itemlist = []

    data = scrapertools.cache_page(item.url)

    patron = '<a href="#" class="dropdown-toggle wide-nav-link" data-toggle="dropdown">Cartoni anni 80<b class="caret"></b></a>(.*?)<li class="dropdown">'
    data = scrapertools.find_single_match(data, patron)

    patron = '<a.*?href="([^"]+)">(.*?)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle).strip()
        itemlist.append(Item(channel=__channel__, action="peliculas", title=scrapedtitle, url=scrapedurl, folder=True))

    return itemlist


def documentari(item):
    logger.info("[filmsubitotv.py] genere")
    itemlist = []

    data = scrapertools.cache_page(item.url)

    patron = '<a href="#" class="dropdown-toggle wide-nav-link" data-toggle="dropdown">Documentari<b class="caret"></b></a>(.*?)<li class="dropdown">'
    data = scrapertools.find_single_match(data, patron)

    patron = '<a.*?href="([^"]+)">(.*?)</a></li>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle).strip()
        itemlist.append(Item(channel=__channel__, action="peliculas", title=scrapedtitle, url=scrapedurl, folder=True))

    return itemlist


def serie(item):
    logger.info("streamondemand.filmsubitotv peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)
    patron = '</span>.*?<a href="([^"]+)" class="pm-thumb-fix pm-thumb-145">.*?"><img.*?src="([^"]+)" title="Young and Hungry " alt="([^"]+)" width="145">'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle).strip()
        if (DEBUG): logger.info(
            "title=[" + scrapedtitle + "], url=[" + scrapedurl + "], thumbnail=[" + scrapedthumbnail + "]")
        itemlist.append(
            Item(channel=__channel__,
                 action="findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 folder=True,
                 fanart=scrapedthumbnail))

    # Extrae el paginador
    patronvideos = '<a href="([^"]+)">&raquo;</a>'
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    if len(matches) > 0:
        scrapedurl = urlparse.urljoin(item.url, matches[0])
        itemlist.append(
            Item(channel=__channel__,
                 action="HomePage",
                 title="[COLOR yellow]Torna Home[/COLOR]",
                 folder=True)),
        itemlist.append(
            Item(channel=__channel__,
                 action="serie",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=scrapedurl,
                 thumbnail="https://raw.githubusercontent.com/orione7/Pelis_images/master/vari/successivo_P.png",
                 folder=True))

    return itemlist


def findvid(item):
    logger.info("[filmsubitotv.py] findvideos")

    # Descarga la página
    data = scrapertools.cache_page(item.url)

    # ---------------------------------------------------------------
    servers = {
        '2': 'http://embed.nowvideo.li/embed.php?v=%s',
        '3': 'http://speedvideo.net/embed-%s-607x360.html',
        '4': 'http://www.fastvideo.me/embed-%s-607x360.html',
        '5': 'http://www.rapidvideo.org/embed-%s-607x360.html',
        '11': 'https://openload.co/embed/%s/',
        '16': 'http://youwatch.org/embed-%s-640x360.html',
        '21': 'http://vidto.me/embed-%s',
        '22': 'http://www.exashare.com/embed-%s-700x400.html',
        '23': 'http://videomega.tv/cdn.php?ref=%s&width=700&height=430',
        '30': 'http://streamin.to/embed-%s-700x370.html'
    }

    patron = "=.setupNewPlayer.'([^']+)','(\d+)'"
    matches = re.compile(patron, re.DOTALL).findall(data)

    data = ""
    for video_id, i in matches:
        try:
            data += servers[i] % video_id + "\n"
        except:
            pass
    # ---------------------------------------------------------------

    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        videoitem.title = "".join([item.title, videoitem.title])
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.show = item.show
        videoitem.channel = __channel__

    return itemlist


def HomePage(item):
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10024,plugin://plugin.video.streamondemand-pureita-master)")
