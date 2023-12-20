import csv
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, SelectField
from wtforms.validators import DataRequired, URL

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = URLField(label="Cafe location on google's Map",
                        validators=[DataRequired(), URL(message="Enter a right URL which starts with 'http'")])
    opening_time = StringField(label="Opening time e.g.8AM", validators=[DataRequired()])
    closing_time = StringField(label="Closing time e.g.10PM", validators=[DataRequired()])
    rating = SelectField(label="Coffee Rating", validators=[DataRequired()],
                         choices=['☕️' * num for num in range(1, 6)])
    wifi = SelectField(label="Wifi Strength Rating", validators=[DataRequired()],
                       choices=['✘' if num == 0 else '💪' * num for num in range(0, 6)])
    power = SelectField(label="power socket availability", validators=[DataRequired()],
                        choices=['✘' if num == 0 else '🔌' * num for num in range(0, 6)])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        print(list_of_rows)
    cafes_length_horizontal = len(list_of_rows[0])
    cafes_length_vertical = len(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows,
                           cafes_len_horizontal=cafes_length_horizontal, cafes_len_vertical=cafes_length_vertical)


@app.route('/add', methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = [
            form.cafe.data,
            form.location.data,
            form.opening_time.data,
            form.closing_time.data,
            form.rating.data,
            form.wifi.data,
            form.power.data
        ]
        with open("cafe-data.csv", "a", encoding='utf-8') as csv_data:
            csv_data.write("\n")
            for data in new_cafe:
                csv_data.write(f"{data},")
        return cafes()
    return render_template('add.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
