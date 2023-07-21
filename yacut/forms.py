from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional

from .utils import (MARGINAL_ORIGINAL_LENGTH, MINIMUM_FIELD_LENGTH,
                    MARGINAL_SHORT_LENGTH, )


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка:',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(MINIMUM_FIELD_LENGTH, MARGINAL_ORIGINAL_LENGTH)]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки:',
        validators=[Length(MINIMUM_FIELD_LENGTH, MARGINAL_SHORT_LENGTH),
                    Optional()]
    )
    submit = SubmitField('Создать')
