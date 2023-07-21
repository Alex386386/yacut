import re
from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import generate_unique_id


@app.route('/api/id/<string:short_url>/', methods=['GET'])
def get_url(short_url):
    url = URLMap.query.filter_by(short=short_url).first()
    if url is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    url = url.original
    return jsonify({'url': url}), HTTPStatus.OK


@app.route('/api/id/<int:id>/', methods=['DELETE'])
def delete_opinion(id):
    url = URLMap.query.get(id)
    if url is None:
        raise InvalidAPIUsage('Url с указанным id не найдено',
                              HTTPStatus.NOT_FOUND)
    db.session.delete(url)
    db.session.commit()
    return '', HTTPStatus.NO_CONTENT


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    short = data.get('custom_id', None)
    original = data.get('url', None)
    if not original:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if short:
        if not re.match("^[A-Za-z0-9]{1,16}$", short):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки')
        if URLMap.query.filter_by(original=original).first() is not None:
            raise InvalidAPIUsage(f'Имя "{short}" уже занято.')
        if URLMap.query.filter_by(short=short).first() is not None:
            raise InvalidAPIUsage('Такая укороченная ссылка уже существует.')
    else:
        instance_original = URLMap.query.filter_by(original=original).first()
        if instance_original is not None:
            raise InvalidAPIUsage(
                f'Имя "{instance_original.short}" уже занято.'
            )
        short = generate_unique_id()
        while URLMap.query.filter_by(short=short).first():
            short = generate_unique_id()
    new_url = URLMap(original=original, short=short)
    db.session.add(new_url)
    db.session.commit()
    return jsonify(new_url.to_dict()), HTTPStatus.CREATED
