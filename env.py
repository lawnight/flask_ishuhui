import os
APP_PATH = os.path.dirname(os.path.abspath(__file__)) + '/ishuhui'
HOST = '0.0.0.0'
PORT = 5000
DEBUG = True
SQLALCHEMY_DATABASE_URI='sqlite:///' + APP_PATH + '/tmp/ishuhui.db'
SECRET_KEY='7c401a1e5fd54c6cd8cd0d5016c2911157a6127815ab7686'
USERNAME='lufficc'
PASSWORD='123456'
ENABLE_CELERY=False
CELERY_BROKER_URL='redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# 漫画图片的目录，需要把static目录下的js等文件，copy在这个目录下
ASSETS = r'D:\image'
# 漫画的id 对应漫画的文件夹名字
COMICS = [{'id':1,'title':'h-mate','description':'','classify_id':1}]

