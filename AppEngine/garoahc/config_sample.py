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
	"api":"0.13",

	"space":"Garoa Hacker Clube",
	"url":"https://garoa.net.br",
	"logo":"https://garoahc.appspot.com/static/img/logo.png",
	"contact": {
		"phone": "+551136620571",
		"twitter": "garoahc",
		"foursquare": FOURSQUARE_VENUE_ID,
		"email":"cs@garoa.net.br",
		"ml":"hackerspacesp@googlegroups.com"
		#"keymaster": "+551112345678 (nome)",
	},
	"events":[],

	#0.12
	"address":"Rua Costa Carvalho, 567, Fundos - Pinheiros - 05429-130 - São Paulo/SP - Brasil",
	"status": "open for public",
	"icon":{
		"open":"https://garoahc.appspot.com/static/img/icon_open.png",
		"closed":"https://garoahc.appspot.com/static/img/icon_closed.png"
	},
	"open":false,
	"lastchange": 1298244863,
	"lon":-46.69918,
	"lat":-23.564968,

	#0.13
	"state": {
		"icon": {
			"open": "https://garoahc.appspot.com/static/img/icon_open.png",
			"closed": "https://garoahc.appspot.com/static/img/icon_closed.png"
		},
		"open": false,
		"lastchange": 1298244863
	},
	
	"sensors" : {
		"total_member_count": [
			{
				"value" : 41
			}
		],
		"people_now_present": [
			{
				"value" : 1,
				"Names" : [ "desconhecido"]
			}
		]
	},  
    
	"location": {
		"address": "Rua Costa Carvalho, 567, Fundos - Pinheiros - 05429-130 - São Paulo/SP - Brasil",
		"lon": -46.69918,
		"lat": -23.564968
	},
	"projects":["https://garoa.net.br/wiki/Categoria:Projetos"],
	"issue_report_channels": [
		"email"
	],
	"cache": {
		"schedule": "m.05"
	}
}

MAC_SPREADSHEET_STR = "https://docs.google.com/spreadsheet/pub?key=ZZZZZZZ&single=true&gid=0&output=csv"

JSON_MACS = {
	"unknown":0,
	"known":{},
	#"known":{
	  #"Lechuga": 123456789,
	  #"name": timestamp
	#},
	"lastchange": 1298244863
}
