import os.path

import tornado.autoreload
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html', head="index sync")

class PoemPageHandler(tornado.web.RequestHandler):
    def post(self):
        noun1 = self.get_argument('noun1')
        noun2 = self.get_argument('noun2')
        verb = self.get_argument('verb')
        noun3 = self.get_argument('noun3')
        self.render('poem.html', roads=noun1, wood=noun2, made=verb, difference=noun3)

class PathPageHandler(tornado.web.RequestHandler):
    def get(self, input):
        file=input
        path=os.listdir(input)
        self.render('path.html', head="PathPage",path=path,file=file)

class Myself(tornado.web.RequestHandler):
    def get(self):
        self.render('test.html', string="this is myself")
        
class BookHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
                'book.html',
                title="home page",
                header="books that are great",
                books=[
                    "Learning Python",
                    "Programming collective intellingence",
                    "Restful web services"
                    ]
                )

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r'/', IndexHandler),
            (r'/poem', PoemPageHandler),
            (r'/path(.*)',PathPageHandler),
            (r'/myself', Myself),
            (r'/books', BookHandler)
            ],
        template_path=os.path.join(os.path.dirname(__file__), "templates")      
    )
    http_server = tornado.httpserver.HTTPServer(app)     
    http_server.listen(options.port)     
    loop=tornado.ioloop.IOLoop.instance()     
    tornado.autoreload.start(loop)
    loop.start()
