import re, requests
from flask import render_template, Blueprint, json, abort, redirect, request, jsonify, url_for, flash

import ishuhui.data as data
from ishuhui.extensions.flasksqlalchemy import db

from env import *
import os

bp_comic = Blueprint('comic', __name__)


@bp_comic.route('/')
def latest_chapters():
    chapters = data.get_latest_chapters(12)
    return render_template('latest.html', comic=None, chapters=chapters)


@bp_comic.route('/comics')
def comics():
    classify_id = request.args.get('classify_id')
    comics = data.get_comics(classify_id)
    return render_template('comics.html', comics=comics)

image_pattern = re.compile(r'<img [^>]*src="([^"]+)')


def get_images_from_url(url):
    html = requests.get(url).text
    images = image_pattern.findall(html)
    return images


@bp_comic.route('/refresh_chapters/<int:chapter_id>', methods=['GET'])
def refresh_chapter(chapter_id):
    chapter = data.get_chapter(chapter_id)
    url = 'http://www.ishuhui.net/ComicBooks/ReadComicBooksToIsoV1/' + str(chapter_id) + '.html'
    images = get_images_from_url(url)
    chapter.images = json.dumps(images)
    db.session.commit()
    flash('Refresh succeed!', 'success')
    return redirect(url_for('comic.chapter', comic_id=chapter.comic().id, chapter_id=chapter.id))



@bp_comic.route('/comics/<int:comic_id>/chapters')
def chapters(comic_id):

    comic = data.get_comic(comic_id)

    #chapters = data.get_chapters(comic_id)
    chapters = data_get_chapters(comic)
    return render_template('chapters.html', comic=comic, chapters=chapters)



def data_get_chapters(comic):
    """
    @comic_path:漫画的路径
    """
    comic_path = os.path.join(ASSETS,comic.title)
    #comic_name = os.path.basename(comic_path) 
    chapters = os.listdir(comic_path)
    chapters.sort(key=lambda x:int(re.findall(r'\d+',x)[0]))
    
    db_chapters  = []
    for chapter in chapters:
        db_chapters.append(get_chapter_db(chapter,comic))
    return db_chapters




def get_chapter_db(name,comic = None):
    """
    根据章节文件夹的name 找出title和数字
    """
    chapter = data.Chapter()
    
    chapter.title = str(name)
    chapter_num = re.findall(r'\d+',str(name))[0]
    chapter.chapter_number =chapter_num
    chapter.id = chapter_num
    if comic:
        chapter.comic_id = comic.id
        chapter.front_cover = "/assets/{}/{}/{}".format(comic.title,chapter_num,'1.png')
    else:
        chapter.comic_id = 1
    return chapter



@bp_comic.route('/comics/<int:comic_id>/chapters/<int:chapter_id>')
def chapter(comic_id, chapter_id):
    """
    @chapter_id 第几章
    """
    comic = data.get_comic(comic_id)   
    comic_path = os.path.join(ASSETS,comic.title)    
    
    

    state = 1
    next_chapter = None
    prev_chapter = None
    chapter = None
    for c in data_get_chapters(comic):
        print(c.id,chapter_id)
        if int(c.id) == chapter_id:
            state = 2
            chapter = c
            continue
        if state == 2:
            next_chapter = c
            break
        else:
            prev_chapter = c
    # 文件目录   
   
    #comic_name = os.path.basename(comic_path) 
    comic_name = os.path.basename(comic_path) 

    #找出当前章节，所有的image    
    chapter_path = os.path.join(comic_path,str(chapter.title))
    images = os.listdir(chapter_path)
    images = [x for x in images if 'jpg' in x]
    images.sort(key=lambda x:int(re.findall(r'\d+',x)[0]))
    images = ["/assets/{}/{}/{}".format(comic_name,chapter.title,x) for x in images]  
    
    #前后章节


    return render_template(
        'images.html',
        comic=comic,
        chapter=chapter,
        next_chapter=next_chapter,
        prev_chapter=prev_chapter,
        images=images,
        url='')