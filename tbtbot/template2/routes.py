"""Bot routes
"""
import handlers
import tornado.web
import configuration


def get_routes():
	return [
	    (r"/", handlers.MainHandler, dict(api=configuration.API), 'command description'),
	    (r"/.*", handlers.UnknownCommandHandler, dict(api=configuration.API), 'command description')
	]