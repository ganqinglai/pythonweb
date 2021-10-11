# import os
import tornado.web
import tornado.ioloop
import tornado.options
from tornado.options import define, options
import tornado.httpserver
from url import url
from config import settings, svraddress, svrport  # , httpscrt, httpskey
import platform
from methods.schedule_test import joba

if platform.system() == "Windows":
    import asyncio

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# define("port", default=8083, help="run on the given port", type=int)
# define("address", default="168.0.0.71", type=str)
define("port", default=svrport, help="run on the given port", type=int)
define("address", default=svraddress, type=str)

application = tornado.web.Application(handlers=url, **settings)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(
        application, """
        ssl_options={
            # "certfile": os.path.join(os.path.abspath("."), "server.crt"),
            # "keyfile": os.path.join(os.path.abspath("."), "server.key.unsecure"),
            "certfile": httpscrt,
            "keyfile": httpskey,
        }
        """)
    http_server.listen(options.port, options.address)
    tornado.ioloop.PeriodicCallback(joba, 3600000).start()  # start scheduler 每隔2s执行一次f2s
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    # autorun()
    main()
