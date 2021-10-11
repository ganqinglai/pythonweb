from handlers.login import LoginHandler
from handlers.htmltest import Showstudent4
from handlers.jh import JhHandler
from handlers.img import ImgHandler, PictureHandler

url = [
    (r'/api/login/(\w+)', LoginHandler),
    (r'/api/show', Showstudent4),
    (r'/api/jh/(\w+)', JhHandler),
    (r'/api/img/(\w+)', ImgHandler),
    (r'/api/imgshow', PictureHandler),
]
