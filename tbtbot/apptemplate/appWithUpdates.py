from envparse import env

import tornado
import tornado.httpserver
import tornado.ioloop
import tornado.web

from tbtbot.lib import Updater

import configuration
import routes



def make_app():
    return tornado.web.Application(
        routes.get_routes(),
        debug=True,
        autoreload=True
    )


def start_bot():

    def callback():
        updater = Updater(
            configuration.API, 
            'http://localhost:%s' % configuration.SERVER_PORT
        )
        updater.getUpdates(5)

    pcb = tornado.ioloop.PeriodicCallback(callback, configuration.POLL_INTERVAL)
    pcb.start()

    http_server = tornado.httpserver.HTTPServer(make_app())
    http_server.listen(configuration.SERVER_PORT, configuration.SERVER_HOST)
    tornado.ioloop.IOLoop.current().start()


def stop_bot():
    tornado.ioloop.IOLoop.current().stop()
    return True


if __name__ == "__main__":

    start_bot()