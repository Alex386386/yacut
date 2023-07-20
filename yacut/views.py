import random
import re
import string

from flask import abort, flash, redirect, render_template

from . import app, db
from .forms import URLMapForm
from .models import URLMap


def generate_unique_id():
    all_chars = string.ascii_letters + string.digits
    unique_id = ''.join(random.choice(all_chars) for _ in range(6))
    return unique_id


@app.route('/', methods=['GET', 'POST'])
def get_unique_short_id():
    form = URLMapForm()
    if form.validate_on_submit():
        if form.custom_id.data:
            link = form.original_link.data
            custom = form.custom_id.data
            if URLMap.query.filter_by(short=custom).first():
                flash(f'Имя {custom} уже занято!',
                      'custom-message')
                return render_template('index.html', form=form)
            if URLMap.query.filter_by(original=link).first():
                flash('На данный адрес уже существует короткая ссылка',
                      'link-message')
                return render_template('index.html', form=form)
            if not re.match("^[A-Za-z0-9]{1,16}$", custom):
                flash('Недопустимое имя короткой ссылки!', 'custom-message')
                return render_template('index.html', form=form)
            new_url = URLMap(
                original=form.original_link.data,
                short=form.custom_id.data,
            )
            db.session.add(new_url)
            db.session.commit()
            return render_template('index.html', form=form, short_url=new_url)
        elif not form.custom_id.data:
            link = form.original_link.data
            if URLMap.query.filter_by(original=link).first():
                flash('На данный адрес уже существует короткая ссылка',
                      'link-message')
                return render_template('index.html', form=form)
            value = generate_unique_id()
            while URLMap.query.filter_by(short=value).first():
                value = generate_unique_id()
            new_url = URLMap(
                original=form.original_link.data,
                short=value,
            )
            db.session.add(new_url)
            db.session.commit()
            return render_template('index.html', form=form, short_url=new_url)
    return render_template('index.html', form=form)


@app.route('/<string:short_url>')
def redirect_to_url(short_url):
    url = URLMap.query.filter_by(short=short_url).first_or_404()
    if not url:
        abort(404)
    return redirect(url.original)
