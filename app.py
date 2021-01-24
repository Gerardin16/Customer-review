
from flask import Flask,render_template,request
from flask_wtf import FlaskForm
from wtforms import (Form,StringField, BooleanField, DateTimeField,
                     RadioField,SelectField,TextField,
                     TextAreaField,SubmitField)
from wtforms.validators import DataRequired
import pandas as pd

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mykey'

# to read csv file named "samplee" 
a = pd.read_csv("Reviews.csv") 
  
# to save as html file 
# named as "Table" 
a.to_html("Table.htm") 
  
# assign it to a  
# variable (string) 
html_file = a.to_html() 

# with open('Reviews.csv') as reviews_file:
#     csv_reader= csv.reader(reviews_file, delimiter=',')
#     line_count=0;

# WTForm Class
class ReviewForm(FlaskForm):

   #Get the fields to be filled in the form
    name = StringField('Name*: ',validators=[DataRequired()])
    product = SelectField(u'Choose your product:',
                          choices=[('opt-1', 'Samsung'), ('opt-2', 'Oneplus'),
                                   ('opt-3', 'Vivo5'), ('opt-4', 'Redmi6')])
    review = TextAreaField()
    submit = SubmitField('Submit your review')


@app.route('/', methods=['GET', 'POST'])
def index():
    # Set the breed to a boolean False.
    # So we can use it in an if statement in the html.
    # Create instance of the form.
    form = ReviewForm()
    # If the form is valid on submission (we'll talk about validation next)
    if form.validate_on_submit() :
        # Grab the data from the breed on the form.
        name= form.name.data
        product=form.product.data
        review=form.review.data
        # Reset the form's breed data to be False
        form.name.data = ''
        form.product.data='Samsung'
        form.review.data=''
    return render_template('index.html', form=form,)


if __name__ == '__main__':
    app.run(debug=True)
