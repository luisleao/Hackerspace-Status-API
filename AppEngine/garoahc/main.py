#!/usr/bin/env python
# coding=utf-8


from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db

from google.appengine.api import datastore
from google.appengine.api import memcache
from google.appengine.ext.webapp import template


import time
import simplejson as json
import logging
import random
import config
from datetime import datetime


class Log(db.Model):
	open_in = db.DateTimeProperty(auto_now_add=True)
	closed_in = db.DateTimeProperty()
	closed = db.BooleanProperty(default=False)


class Event(db.Model):
	name = db.StringProperty(required=True)
	type = db.StringProperty(required=True, choices=["check-in", "check-out", "door"], default="check-in")
	t = db.DateTimeProperty(auto_now_add=True)
	extra = db.StringProperty()
	
	#name (string, mandatory) – name or nickname of person or object associated with this event;
	#type (string, mandatory) – ‘check-in’ or ‘check-out’ (other values may be specified, but receivers of the object are not obligated to be able to understand these)
	#t (long int, mandatory) – time since the epoch for this event
	#extra (string, optional) – additional information
	




"""

	/					> raiz
	/rest/status/open	> muda status para aberto
	/rest/status/close	> muda status para fechado 
	/rest/event/		> POST: gera novo evento (fora checkin/open/close)
	
	/foursquare/checkin	> push do foursquare da venue (inclui registro em events)
	


	usar memcache com ID do lastStatus, principalmente se ele estiver aberto
	se o status estiver fechado e receber outro closed, nao faz nada
	se o status estiver aberto e receber closed, fecha e atualiza
	
	se o status estiver aberto e receber outro open, nao faz nada
	se o status estiver fechado e receber open, criar novo registro e atualizar
	

"""


# toda vez que gerar evento limpar cache

def get_data():
	# verificar memcache
	# listar ultimos eventos
	
	status = memcache.get("status")
	if status is None:
		status = config.JSON_STATUS
		status["lastchange"] = int(time.mktime(datetime.now().timetuple()))
		
		last_log = memcache.get("log")
		if last_log is None:
			last_log = Log.all().order("-open_in").get()
		
		if not last_log is None:
			status["open"] = not last_log.closed
		
		events = []
		for event in Event.all().order("-t").fetch(config.TOTAL_EVENTS):
			events.append({
				"name": event.name,
				"type": event.type,
				"t": int(time.mktime(event.t.timetuple())),
				"extra": event.extra
			})
		
		events.reverse()
		status["events"] = events
		memcache.add("status", status)
		
	return status



class RestHandler(webapp.RequestHandler):
	def get(self, objeto, acao=None, token=None):
		
		if token != config.ARDUINO_TOKEN:
			self.response.out.write("<e9>")
			return
		
		if objeto == "status":
			last_log = memcache.get("log")
			if last_log is None:
				last_log = Log.all().order("-open_in").get()
			
			if acao == "open":
				if last_log is None or last_log.closed:
					last_log = Log()
					last_log.put()
					#memcache.delete("log")
					#memcache.add("log", last_log)
					#memcache.delete("status")
					self.response.out.write("<o1>")
				else:
					self.response.out.write("<o0>")
				
			elif acao == "close":
				if not last_log is None and not last_log.closed:
					last_log.closed = True
					last_log.closed_in = datetime.now()
					last_log.put()
					#memcache.delete("log")
					#memcache.add("log", last_log)
					#memcache.delete("status")
					self.response.out.write("<o1>")
				else:
					self.response.out.write("<o0>")
					
			memcache.delete("status")
			memcache.add("log", last_log)
			memcache.delete("status")
				
		elif objeto == "event":
			#TODO: implementar registro de outros eventos
			self.response.out.write("<e0>")
			
		else:
			self.response.out.write("<x0>")
	


class MainHandler(webapp.RequestHandler):
	def get(self):
		#if self.request.get("force"):
		#	memcache.delete("status")
		
		#self.response.headers.add_header("Access-Control-Allow-Origin", "*")
		#self.response.headers.add_header("Cache-Control", "no-cache")
		#self.response.out.write(json.dumps(get_data()))
		
		template_values = {
			#"channel_token": channel.create_channel("TOKEN"),
		}
		self.response.out.write(template.render("./template/geral.html", template_values))
		
	

class StatusHandler(webapp.RequestHandler):
	def get(self):
		if self.request.get("force"):
			memcache.delete("status")
		
		self.response.headers['Content-Type'] = "application/json"
		self.response.headers.add_header("Access-Control-Allow-Origin", "*")
		self.response.headers.add_header("Cache-Control", "no-cache")
		self.response.out.write(json.dumps(get_data()))
	

class ImageHandler(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = "image/png"
		self.response.headers.add_header("Access-Control-Allow-Origin", "*")
		self.response.headers.add_header("Cache-Control", "no-cache")
		
		json_status = get_data()
		
		image = json_status["open"] and json_status["icon"]["open"] or json_status["icon"]["closed"]
		self.redirect(image)
	



class FoursquareHandler(webapp.RequestHandler):
	def post(self):
		if self.request.get("secret") != config.FOURSQUARE_SECRET:
			self.response.out.write("INVALID SECRET")
			logging.warning("INVALID SECRET: %s." % self.request.get("secret"))
			return
		
		retorno = json.loads(self.request.get("checkin"))
		logging.info(json.dumps(retorno))
		
		if retorno["venue"]["id"] != config.FOURSQUARE_VENUE_ID:
			self.response.out.write("INVALID VENUE")
			logging.warning("INVALID VENUE %s." % retorno["venue"]["id"])
			return
		
		event = Event(name = "%s %s" % (retorno["user"]["firstName"], retorno["user"]["lastName"]),
			extra = retorno["user"]["photo"]
		)
		event.put()
		
		memcache.delete("status")
		self.response.out.write("OK")
		
		"""
		{
			"venue": {
				"verified": true, 
				"name": "Ag\u00eanciaClick Isobar", 
				"url": "http://www.agenciaclickisobar.com.br", 
				"contact": {"phone": "+551137593600", "twitter": "agenciaclick", "formattedPhone": "+55 11 3759-3600"}, 
				"location": {"city": "S\u00e3o Paulo", "country": "Brazil", "postalCode": "05686-002", "state": "SP", "crossStreet": "2\u00b0 Andar", "address": "Av. Duquesa de Goi\u00e1s, 716", "lat": -23.613699445896213, "lng": -46.702966690063477}, 
				"stats": {"tipCount": 29, "checkinsCount": 7914, "usersCount": 467}, 
				"id": "4b4cb2c1f964a520bdba26e3", 
				"categories": [{"pluralName": "Offices", "primary": true, "name": "Office", "parents": ["Professional & Other Places"], "shortName": "Corporate / Office", "id": "4bf58dd8d48988d124941735", "icon": "https://foursquare.com/img/categories/building/default.png"}]}, 
			"user": {
				"photo": "https://img-s.foursquare.com/userpix_thumbs/MDDZM3K0RK0MD112.jpg", 
				"canonicalUrl": "https://foursquare.com/user/5350109", 
				"firstName": "Livia", 
				"lastName": "C.", 
				"homeCity": "S\u00e3o Paulo, Brasil", 
				"gender": "female", 
				"id": "5350109"}, 
			"timeZone": "America/Sao_Paulo", 
			"type": "checkin", 
			"id": "4f4c0f98e4b0accb02fdd2f0", 
			"createdAt": 1330384792
		}
		"""
	
	

	

def main():
	handlers = [
		("/foursquare/push", FoursquareHandler),
		("/rest/(status)/(open|close)/([\w\d]*)", RestHandler),
		("/status", StatusHandler),
		("/status.png", ImageHandler),
		("/view", MainHandler),
		("/", MainHandler),
	]
	application = webapp.WSGIApplication(handlers, debug=True)
	util.run_wsgi_app(application)
	


if __name__ == '__main__':
	main()

