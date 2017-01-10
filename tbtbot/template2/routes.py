"""Bot routes
"""
import handlers
import tornado.web
import configuration


routes = [
    (r"/", handlers.MainHandler, dict(api=configuration.API)),
    (r"/.*", handlers.UnknownCommandHandler, dict(api=configuration.API))
]