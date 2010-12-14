from local_settings import *
import re
from foursquare import *
import logging, email
from google.appengine.ext import webapp 
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler 
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import mail

class LogSenderHandler(InboundMailHandler):
    def receive(self, mail_message):
        logging.info('Received a message from ' + mail_message.sender)
        bodies = mail_message.bodies(content_type='text/plain')
        for content_type, body in bodies:
            logging.debug('found body ' + body.decode())
            body_content = body.decode()
            vitals_start = body_content.find('VITALS')
            if vitals_start > -1:
                name_start = body_content.find('*', vitals_start) + 1
                name_end = body_content.find('*', name_start)
                name = body_content[name_start:name_end]
                logging.info('found venue ' + name)
                fs = Foursquare(BasicCredentials(username, password))
                venue = fs.venues(geolat='40.72', geolong='-74.0', q=name)
                venue_id = venue['groups'][0]['venues'][0]['id']
                logging.debug('found venue id ' + str(venue_id))
                tip_id = fs.addtip(vid=str(venue_id), text='from ud', type='todo')
                
application = webapp.WSGIApplication([
  LogSenderHandler.mapping()
], debug=True)
def main():
  run_wsgi_app(application)
if __name__ == "__main__":
  main()
