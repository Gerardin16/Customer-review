# Necessary packages
from flask import Flask,render_template,request,flash,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import (StringField,SelectField,TextAreaField,SubmitField)
from wtforms.validators import DataRequired
import csv

app = Flask(__name__)

# Configure a secret SECRET_KEY
app.config['SECRET_KEY'] = 'mykey'

# CSV File to store the submitted reviews
filename = "Reviews.csv"
#Header in CSV File
header = ("Name", "Product", "Review")

submitReviews =[]
countOfReviews = 0 

# WTForm Class
class ReviewForm(FlaskForm):

   #Get the fields to be filled in the form
    name = StringField('Name*: ',validators=[DataRequired(message="Please fill this field")])
    product = SelectField(u'Choose your product:',
                          choices=[('Samsung', 'Samsung'), ('Oneplus', 'Oneplus'),
                                   ('Vivo 5', 'Vivo 5'), ('Redmi 6', 'Redmi 6')])
    review = TextAreaField()
    submit = SubmitField('Submit your review')


@app.route('/', methods=['GET', 'POST'])
def index():
    # Set varibles to hold the form data and initialize to False
    name=False
    product=False
    review=False
    

    #Retrieve the submitted reviews from the CSV file and assign to s list
    submitReviews= loadReviews()
    
    # Create instance of the form.
    form = ReviewForm()

    
    # If the form is valid on submission and the method is 'POST'
    if form.validate_on_submit() and request.method =='POST' :
        try:
        # Grab the data from the form.
            name= form.name.data
            product=form.product.data
            review=form.review.data
            data=[name,product,review]
            writeToCSV(header,data,filename)
            # Reset the form's data to be False
            form.name.data = ''
            form.product.data=False
            form.review.data=''

            submitReviews= loadReviews()

            # Message to display on successful submission of the review
            flash('Your review has been submitted successfully')
            return redirect(url_for('index'))
   
        except:
            flash("Your review has not been submitted successfully")
            return redirect(url_for('index'))

    return render_template('index.html', form=form, submitReviews=submitReviews,countOfReviews=len(submitReviews))


#Function to retrieve the submitted reviews from the CSV file 
def loadReviews():
    try:
        with open (filename, 'r') as readfile:
            reader = csv.DictReader(readfile) 
            dict_list = []
            for line in reader:
                dict_list.append(line)   
            return dict_list
    except:
        flash("Reviews cannot be loaded")


 # Function to save the form details in CSV file
def writeToCSV(header, data, filename):
    try:
        with open (filename, 'r') as readfile:
            reader = csv.DictReader(readfile)
            # for row in reader:
            # print(row['id'])
            lineCount= len(list(reader))
            if(lineCount < 1):
                with open (filename, 'w') as writefile:
                    writer=csv.writer(writefile)
                    writer.writerow(header)
                    writer.writerow(data)
            else:
                with open (filename, 'a') as writefile:
                    writer=csv.writer(writefile)
                    writer.writerow(data)
    except:
        flash("Your review has not been submitted successfully")                
       

if __name__ == '__main__':
    app.run(debug=True)
