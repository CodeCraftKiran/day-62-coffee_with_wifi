from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, TimeField, SelectField
from wtforms.validators import DataRequired
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = URLField(label="Cafe location on google's Map", validators=[DataRequired()])
    opening_time = TimeField(label="Opening time e.g.8AM", validators=[DataRequired()])
    closing_time = TimeField(label="Closing time e.g.10PM", validators=[DataRequired()])
    rating = SelectField(label="Coffee Rating", validators=[DataRequired()], choices=['☕️'*num for num in range(1,6)])
    wifi = SelectField(label="Wifi Strength Rating", validators=[DataRequired()],
                       choices=['✘' if num == 0 else '💪'*num for num in range(0,6)])
    power = SelectField(label="power socket availability", validators=[DataRequired()],
                        choices=['✘' if num == 0 else '🔌'*num for num in range(0,6)])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add')
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


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


if __name__ == '__main__':
    app.run(debug=True)
