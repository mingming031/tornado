import os.path
import random
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

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class MungedPageHandler(tornado.web.RequestHandler):
    def map_by_first_letter(self,text):
        mapped = dict()
        for line in text.split('\r\n'):
            for word in [x for x in line.split(' ') if len(x) > 0]:
                if word[0] not in mapped: mapped[word[0]]=[]
                mapped[word[0]].append(word)
        return mapped
    def post(self):
        source_text = self.get_argument('source')
        text_to_change = self.get_argument('change')
        source_map = self.map_by_first_letter(source_text)
        change_lines = text_to_change.split('\r\n')
        if text_to_change == "password":
            self.render(
                    'munged.html',
                    source_map=source_map,
                    change_lines=text_to_change,
                    choice=random.choice
                    )
        else:
            self.render('index.html')
class FileTransfer(tornado.web.RequestHandler):
    def get(self):
        self.render("upload-file.html")
        
    def post(self):
        file_dict_list = self.request.files['file'][0]
        filename = file_dict_list['filename']
        filetype = os.path.splitext(filename)[1]
        filemd5 = md5.new(file_dict_list['body']).hexdigest()
        finalfilename = filemd5+filetype

        f = open("/imagefile/"+final_filename, "wb")
        f.write(file_dict_list['body'])
        f.close()
        self.finish(finalfilename+"is uploaded")
        
    
if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
            handlers=[
                (r'/', IndexHandler),
                (r'/poem', MungedPageHandler),
                (r'/file', FileTransfer),
                ],
            template_path=os.path.join(os.path.dirname(__file__),"templates"),
            static_path=os.path.join(os.path.dirname(__file__),"static"),
            debug=True
            )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

