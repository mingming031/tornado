import string
import os
import sys
import md5

import tornado.httpserver 
import tornado.ioloop 
import tornado.options 
import tornado.web 

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class FileTransfer(tornado.web.RequestHandler):
    def checkfile(self, checkname=""):    
        if os.path.isfile("imagefile/"+checkname):
            return 0
        else:
            return 1

    def get(self):
        self.render("upload-file.html")
        
    def post(self):
        file_dict_list = self.request.files['file'][0]
        filename = file_dict_list['filename']
        filetype = os.path.splitext(filename)[1]
        filemd5 = md5.new(file_dict_list['body']).hexdigest()
        finalfilename = filemd5+filetype

        if self.checkfile(finalfilename):
            f = open("static/imagicfile/"+finalfilename, "wb")
            f.write(file_dict_list['body'])
            f.close()
            self.finish(finalfilename+"is uploaded")
        else:
            self.finish(finalfilename+"has been uploaded")


class ImagicShow(tornado.web.RequestHandler):
    def get(self):
        imagiclist = os.listdir("static/imagicfile/")
        self.render("imagic.html", imagiclist = imagiclist)

    def post(self):
        pass
class ImagicDel(tornado.web.RequestHandler):
    def get(self):
        del_list = self.get_argument('dellist')
        pass
    def del(self):
        pass
    
    
if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
            handlers=[
                (r'/imagic', ImagicShow),
               (r'/file', FileTransfer),
                ],
            template_path=os.path.join(os.path.dirname(__file__),"templates"),
            static_path=os.path.join(os.path.dirname(__file__),"static"),
            debug=True
            )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

