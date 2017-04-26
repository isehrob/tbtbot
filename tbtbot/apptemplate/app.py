import json

import tornado
import tornado.httpserver
import tornado.ioloop
import tornado.web

import tbtbot.lib.custom

import configuration
import routes



def make_app():
	app = tbtbot.lib.Application(
		routes.get_routes(),
		debug=True,
		autoreload=True
	)

	app.add_handlers('', [
		(r"/webhook", tornado.web.RequestHandler),
	])
	return app

def start_bot():
    http_server = tornado.httpserver.HTTPServer(make_app(), ssl_options={
        "certfile": configuration.CERTFILE,
        "keyfile": configuration.KEYFILE
    })

    http_server.listen(
    	configuration.SERVER_PORT, 
    	configuration.SERVER_HOST
    )

    tornado.ioloop.IOLoop.current().start()


def stop_bot():
    tornado.ioloop.IOLoop.current().stop()
    return True

if __name__ == "__main__":

	start_bot()