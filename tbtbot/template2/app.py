from envparse import env

import tornado
import tornado.httpserver
import tornado.ioloop
import tornado.web

import updates
import configuration
import routes



def make_app():
    app = tornado.web.Application(
        routes.routes,
        debug=True,
        autoreload=True
    )

    return app


def updater():
    # some kind of parallel task
    updates.getUpdates(5)


if __name__ == "__main__":

    pcb = tornado.ioloop.PeriodicCallback(updater, configuration.POLL_INTERVAL)
    pcb.start()

    http_server = tornado.httpserver.HTTPServer(make_app())
    http_server.listen(env('SERVER_PORT'), env('SERVER_HOST'))
    tornado.ioloop.IOLoop.current().start()
