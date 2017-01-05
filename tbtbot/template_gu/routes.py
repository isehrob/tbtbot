"""Bot routes
"""
import handlers
import tornado.web
import configuration


routes = [
    (r"/name", handlers.NameHandler, dict(api=configuration.API)),
    (r"/ask", handlers.QuestionHandler, dict(api=configuration.API)),
    (r"/greet", handlers.GreetHandler, dict(api=configuration.API)),
    (r"/broadcast", handlers.BroadcastHandler, dict(api=configuration.API)),
    (r"/", handlers.MainHandler, dict(api=configuration.API)),
    (r"/.*", handlers.UnknownCommandHandler, dict(api=configuration.API))
]