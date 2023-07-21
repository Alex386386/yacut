import random
import re
import string

from flask import flash

from .models import URLMap

MARGINAL_ORIGINAL_LENGTH: int = 128
MINIMUM_FIELD_LENGTH: int = 1
MARGINAL_SHORT_LENGTH: int = 16
VALUE_FOR_RANDOMIZER: int = 6


def generate_unique_id():
    all_chars = string.ascii_letters + string.digits
    return ''.join(
        random.choice(all_chars) for _ in range(VALUE_FOR_RANDOMIZER)
    )


def check_index_view(form):
    if form.custom_id.data:
        link = form.original_link.data
        custom = form.custom_id.data
        if URLMap.query.filter_by(short=custom).first():
            flash(f'Имя {custom} уже занято!',
                  'custom-message')
            return None, None
        if URLMap.query.filter_by(original=link).first():
            flash('На данный адрес уже существует короткая ссылка',
                  'link-message')
            return None, None
        if not re.match("^[A-Za-z0-9]{1,16}$", custom):
            flash('Недопустимое имя короткой ссылки!', 'custom-message')
            return None, None
        return link, custom
    if not form.custom_id.data:
        link = form.original_link.data
        if URLMap.query.filter_by(original=link).first():
            flash('На данный адрес уже существует короткая ссылка',
                  'link-message')
            return None, None
        value = generate_unique_id()
        while URLMap.query.filter_by(short=value).first():
            value = generate_unique_id()
        return link, value
