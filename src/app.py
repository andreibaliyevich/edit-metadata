import os
import math
import secrets
from datetime import datetime
from exif import Image as ExifImage
from exif import DATETIME_STR_FORMAT
from PIL import Image, ImageDraw, ImageFont, ImageOps
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import DateTimeField, IntegerField, SelectField, SubmitField
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename
from flask import Flask, render_template, send_file


app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)
Bootstrap5(app)


class ImageDateGPSForm(FlaskForm):
    image = FileField(
        'Image',
        validators=[
            FileRequired(),
            FileAllowed(['jpg', 'jpeg', 'png']),
        ],
    )

    date = DateTimeField(
        'Date',
        default=datetime.now,
        validators=[InputRequired()],
    )

    latitude_a = IntegerField('Latitude angle', validators=[InputRequired()])
    latitude_m = IntegerField('Latitude minute', validators=[InputRequired()])
    latitude_s = IntegerField('Latitude second', validators=[InputRequired()])

    latitude_ref = SelectField(
        'Latitude ref',
        choices=[
            ('N', 'north latitude'),
            ('S', 'south latitude'),
        ],
        default='N',
        validators=[InputRequired()],
    )

    longitude_a = IntegerField('Longitude angle', validators=[InputRequired()])
    longitude_m = IntegerField('Longitude minute', validators=[InputRequired()])
    longitude_s = IntegerField('Longitude second', validators=[InputRequired()])

    longitude_ref = SelectField(
        'Longitude ref',
        choices=[
            ('E', 'east longitude'),
            ('W', 'west longitude'),
        ],
        default='E',
        validators=[InputRequired()],
    )

    submit = SubmitField('Get image')


def edit_image(img_path, form):
    with Image.open(img_path) as pil_img:
        ImageOps.exif_transpose(pil_img, in_place=True)

        img_width, img_height = pil_img.size

        datetime_str = form.date.data.strftime('%m/%d/%Y %H:%M:%S')
        gps_str = (
            f'{ form.latitude_a.data }º '
            f'{ form.latitude_m.data }\' '
            f'{ form.latitude_s.data }" '
            f'{ form.latitude_ref.data }, '
            f'{ form.longitude_a.data }º '
            f'{ form.longitude_m.data }\' '
            f'{ form.longitude_s.data }" '
            f'{ form.longitude_ref.data }'
        )

        dp = math.sqrt(math.pow(img_width, 2) + math.pow(img_height, 2))
        fnt_size = int(dp * 125 / 5040)
        datetime_width = int(img_width - (dp * 1280 / 5040))
        datetime_height = int(img_height - (dp * 380 / 5040))
        gps_height = int(img_height - (dp * 240 / 5040))

        if len(gps_str) == 28:
            gps_width = int(img_width - (dp * 1650 / 5040))
        elif len(gps_str) == 27:
            gps_width = int(img_width - (dp * 1580 / 5040))
        elif len(gps_str) == 26:
            gps_width = int(img_width - (dp * 1510 / 5040))
        elif len(gps_str) == 25:
            gps_width = int(img_width - (dp * 1440 / 5040))
        elif len(gps_str) == 24:
            gps_width = int(img_width - (dp * 1370 / 5040))
        elif len(gps_str) == 23:
            gps_width = int(img_width - (dp * 1300 / 5040))
        elif len(gps_str) == 22:
            gps_width = int(img_width - (dp * 1230 / 5040))
        else:
            gps_width = int(img_width - (dp * 1650 / 5040))

        fnt = ImageFont.truetype('/usr/src/app/static/arialmt.ttf', fnt_size)

        draw = ImageDraw.Draw(pil_img)
        draw.multiline_text(
            (datetime_width, datetime_height),
            datetime_str,
            font=fnt,
            fill=(255, 255, 255),
        )
        draw.multiline_text(
            (gps_width, gps_height),
            gps_str,
            font=fnt,
            fill=(255, 255, 255),
        )

        pil_img_path = f'/usr/src/app/media/{datetime.now().timestamp()}.jpg'
        pil_img.save(pil_img_path)

    with open(pil_img_path, 'rb') as img_file:
        exif_img = ExifImage(img_file)

        datetime_str = form.date.data.strftime(DATETIME_STR_FORMAT)
        exif_img.datetime = datetime_str
        exif_img.datetime_digitized = datetime_str
        exif_img.datetime_original = datetime_str

        gps_latitude = (
            form.latitude_a.data,
            form.latitude_m.data,
            form.latitude_s.data,
        )
        gps_longitude = (
            form.longitude_a.data,
            form.longitude_m.data,
            form.longitude_s.data,
        )
        exif_img.gps_latitude = gps_latitude
        exif_img.gps_latitude_ref = form.latitude_ref.data
        exif_img.gps_longitude = gps_longitude
        exif_img.gps_longitude_ref = form.longitude_ref.data

        datetime_str = form.date.data.strftime('%Y%m%d_%H%M%S')
        new_img_path = f'/usr/src/app/media/IMG_{datetime_str}.jpg'

        with open(new_img_path, 'wb') as new_img_file:
            new_img_file.write(exif_img.get_file())

    os.remove(pil_img_path)
    return new_img_path


@app.route('/', methods=['GET', 'POST'])
def index():
    form = ImageDateGPSForm()
    if form.validate_on_submit():
        img = form.image.data
        img_name = secure_filename(img.filename)
        img_path = f'/usr/src/app/media/{img_name}'
        img.save(img_path)
        new_img_path = edit_image(img_path, form)
        os.remove(img_path)
        return send_file(new_img_path, as_attachment=True)
    else:
        return render_template('index.html', form=form)
