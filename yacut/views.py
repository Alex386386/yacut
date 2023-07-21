from flask import redirect, render_template

from . import app, db
from .forms import URLMapForm
from .models import URLMap
from .utils import check_index_view


@app.route('/', methods=['GET', 'POST'])
def get_unique_short_id():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    value_original, value_custom = check_index_view(form)
    if value_original is None or value_custom is None:
        return render_template('index.html', form=form)
    new_url = URLMap(
        original=value_original,
        short=value_custom,
    )
    db.session.add(new_url)
    db.session.commit()
    return render_template('index.html', form=form, short_url=new_url)


@app.route('/<string:short_url>')
def redirect_to_url(short_url):
    url = URLMap.query.filter_by(short=short_url).first_or_404()
    return redirect(url.original)
