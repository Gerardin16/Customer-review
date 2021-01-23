
from flask import Flask,render_template,request,url_for,flash,redirect
from flask_wtf import FlaskForm
from wtforms import (Form,StringField, BooleanField, DateTimeField,
                     RadioField,SelectField,TextField,
                     TextAreaField,SubmitField)
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

# WTForm Class
class ReviewForm(FlaskForm):

   #Get the fields to be filled in the form
    name = StringField('Name*: ',validators=[DataRequired()])
    # product = RadioField('Please choose your product: ', choices=[('opt-1', 'Samsung'), ('opt-2', 'Oneplus'),
    #                                                             ('opt-3', 'Vivo 5'), ('opt-4', 'Redmi 6')])

    product = SelectField(u'Please choose your product:',
                          choices=[('opt-1', 'Samsung'), ('opt-2', 'Oneplus'),
                                   ('opt-3', 'Vivo 5'), ('opt-4', 'Redmi 6')])
    review = TextAreaField()
    submit = SubmitField('Submit your review')


@app.route('/', methods=['GET', 'POST'])
def index():

    # Create instance of the form.
    form = ReviewForm()
    # If the form is valid on submission 
    if form.validate_on_submit() and request.method =='POST':
        #Display a success message
        flash("Your review has been submitted succesfully")
        # return redirect(url_for("thankyou"))


    return render_template('index.html', form=form)

# @app.route('/')
# def home():
#     return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
