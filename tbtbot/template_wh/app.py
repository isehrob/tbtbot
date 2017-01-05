import json

import tornado
import tornado.httpserver
import tornado.ioloop
import tornado.web

import tbtbot.lib.custom

import configuration
import routes



def make_app():
	app = tbtbot.lib.custom.CustomApplication(
		routes.routes,
		debug=True,
		autoreload=True
	)

	app.add_handlers('', [
		(r"/webhook", tornado.web.RequestHandler),
	])
	return app


if __name__ == "__main__":

    http_server = tornado.httpserver.HTTPServer(make_app(), ssl_options={
        "certfile": configuration.CERTFILE,
        "keyfile": configuration.KEYFILE
    })

    http_server.listen(
    	configuration.SERVER_PORT, 
    	configuration.SERVER_HOST
    )

    tornado.ioloop.IOLoop.current().start()
