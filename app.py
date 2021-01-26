
from flask import Flask,render_template,request,flash,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import (StringField,SelectField,TextAreaField,SubmitField)
from wtforms.validators import DataRequired
import csv

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mykey'

filename = "Reviews.csv"
header = ("Name", "Product", "Review")
submitReviews =[]
countOfReviews = 0 

# WTForm Class
class ReviewForm(FlaskForm):

   #Get the fields to be filled in the form
    name = StringField('Name*: ',validators=[DataRequired()])
    product = SelectField(u'Choose your product:',
                          choices=[('Samsung', 'Samsung'), ('Oneplus', 'Oneplus'),
                                   ('Vivo 5', 'Vivo 5'), ('Redmi 6', 'Redmi 6')])
    review = TextAreaField()
    submit = SubmitField('Submit your review')


@app.route('/', methods=['GET', 'POST'])
def index():
    # Set the breed to a boolean False.
    name=False
    product=False
    review=False
    submit=False
    submitReviews= loadReviews()
    # So we can use it in an if statement in the html.
    # Create instance of the form.
    form = ReviewForm()

    
    # If the form is valid on submission (we'll talk about validation next)
    if form.validate_on_submit() and  request.method == 'POST' :

        # Grab the data from the form.
        name= form.name.data
        product=form.product.data
        review=form.review.data
        data=[name,product,review]
        writeToCSV(header,data,filename)
        # Reset the form's breed data to be False
        form.name.data = ''
        form.product.data=False
        form.review.data=''
        form.submit.data=False
        submitReviews= loadReviews()
        flash('Your review has been submitted successfully')
        return redirect(url_for('index'))
    
    return render_template('index.html', form=form, submitReviews=submitReviews,countOfReviews=len(submitReviews))
    
def loadReviews():
    with open (filename, 'r') as readfile:
        reader = csv.DictReader(readfile) 
        dict_list = []
        for line in reader:
            dict_list.append(line)   
        return dict_list


def writeToCSV(header, data, filename):
        with open (filename, 'r', newline = "") as readfile:
            reader = csv.DictReader(readfile)
            # for row in reader:
            # print(row['id'])
            lineCount= len(list(reader))
            with open (filename, 'a') as writefile:
                if(lineCount < 1):
                    writer=csv.writer(writefile)
                    writer.writerow(header)
                    writer.writerow(data)
                else:
                    lineCount+=1
                    writer=csv.writer(writefile)
                    writer.writerow(data)
       

if __name__ == '__main__':
    app.run(debug=True)
