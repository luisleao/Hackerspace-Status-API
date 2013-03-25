#!/usr/bin/env python
# coding=utf-8

from datetime import tzinfo, timedelta, datetime



TOTAL_EVENTS = 10
FOURSQUARE_VENUE_ID = "THE_FOURSQUARE_NEW_VENUE_ID"

FOURSQUARE_SECRET = "YOUR_FOURSQUARE_PUSH_SECRET"
FOURSQUARE_CLIENT_ID = "YOUR_FOURSQUARE_CLIENT_ID"
FOURSQUARE_CLIENT_SECRET = "YOUR_FOURSQUARE_CLIENT_SECRET"

FACEBOOK_FANPAGE_TOKEN = "FANPAGE_TOKEN" #you need manage_pages permission
FACEBOOK_FANPAGE_ID = "FANPAGE_ID"

TEMPO_EXPIRACAO_FACEBOOK = timedelta(minutes=10)
FACEBOOK_PHOTO_ID_DEFAULT = "278416315569719"
FACEBOOK_PHOTO_ID_OPEN = "FBID" #used to change the page cover status
FACEBOOK_OFFSET_OPEN = 0
FACEBOOK_PHOTO_ID_CLOSE = "FBID"
FACEBOOK_OFFSET_CLOSE = 100


ARDUINO_TOKEN = "YOUR_ARDUINO_TOKEN"

JSON_STATUS = {
	"api":"0.12",
	"space":"Garoa Hacker Clube",
	"url":"https://garoa.net.br",
	"address":"Rua Costa Carvalho, 567, Fundos - Pinheiros - 05429-130 - São Paulo/SP - Brasil",
	"contact": {
		"phone": "+551136620571",
		"twitter": "garoahc",
		"foursquare": FOURSQUARE_VENUE_ID,
		"ml":"cs@garoa.net.br",
		#"keymaster": "+551112345678 (nome)",
	},
	"status": "open for public",
	"logo":"https://garoahc.appspot.com/static/img/logo.png",
	"icon":{
		"open":"https://garoahc.appspot.com/static/img/icon_open.png",
		"closed":"https://garoahc.appspot.com/static/img/icon_closed.png"
	},
	"open":False,
	"lastchange": 1298244863,
	"events":[],
	"lon":-46.65151967777777,
	"lat":-23.532896
}

CADASTRO_MACS = {'1234': 'Lechuga', '4321': 'Lechuga','0000': 'Teste'}
JSON_MACS = {
	"known":"0",
	"unknown":"0",
	"names":[],
	"lastchange": 1298244863
}
