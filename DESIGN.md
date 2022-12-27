
# Table of Contents
1. [Database](#database)
2. [HTML](#html)
3. [Python](#python)
4. [Home](#home)
5. [Survey](#third-example)
6. [Explore](#third-example)
7. [Specific Musicals](#specific-musicals)
8. [Images](#images)
9. [Login, Logout, Register](#login-logout-register)

## Database
We built our own database ``` musical.db ``` for this project because there were no existing available databases that classified musicals in a way that enable advanced search and algorithm recommendation. 

There are 5 tables in our database.
1. Table ``` musical ``` includes one row for each musical. Besides the id, the name, language, setting, description, a vertical poster(BLOB), a horizontal poster(BLOB), and 5 kinds of ratings (INT) are included for each musical. The ratings rate the musicals on 5 aspects - romance, humour, fiction/history, action, mystery. 

	The columns name, language, setting are used for advanced search function in ``` explore.html ```.

	We uploaded the images stored in the BLOB columns ```vphoto``` and ```hphoto``` using the Python script ``` insertimage.py ```. If we needed to edit images after uploading, we used phpLiteAdmin for ease of use. When retrieving images from the database to display on our webpage, we used the flask route ```photo``` to retrieve the images.
	
	The ratings for each musical on the 5 aspects are subjectively given by us. The ratings are used by the recommendation algorithm found in ```recommendation.py``` to recommend musicals to users using data retrieved from ``` survey.html ```. The recommended musical is then displayed on the website.

2. Table ``` theme ``` contains two columns. One stores the id of the theme, one stores the actual theme.
3. Table ``` match``` matches the themes to the musicals using the ids of the themes and musicals (which are both foreign keys. It is used for advanced search and to display the themes on each musical's info page (implemented in ``` musical_info.html ```).
4. Table ``` survey``` contains our survey questions and answers. Each answer corresponds to a rating along one of our predetermined aspects - answer1 stands for 1 point and answer 5 stands for 5 points on that aspect. Each question corresponds to one aspect - romance, humor, fiction history, action, or mystery. The ratings for each musical are stored in table ``` musical```. We designed it this way so that we can easily associate the values of each answer to the aspects and call our recommendation algorithm to find the best musical to recommend.
5. Table ``` users ``` has a column for an id, username, and hashed password. It also contains the column survey_completed to record if the user has submitted the survey and the column recommended_musical_id to store the recommendation given by the algorithm after doing the survey.

## HTML
There are 9 HTML files that are part of our web app. All use Jinja. They are listed here in alphabetical order, with quick descriptions of what they are meant to render.
1. ```apology.html``` Renders the apology page (ft. a cat) when an error occurs. Modified from CS50's Finance Pset.
2. ```explore.html``` Renders the Explore page on the website and the search results when a search is done.
3. ```index.html``` Renders the Home page on the website
4. ```layout.html``` Provides the layout for the entire website - all other ```.html``` files in our code extend this one. The code for the navigation bar that is present on all pages is contained in this file. 
5. ```login.html``` Renders the login page. Modified from CS50's Finance Pset.
6. ```musical_info.html``` Renders the information page for a a specific musical. Which musical is rendered depends on the inputted information. 
7. ```register.html``` Renders the registration page. Modified from CS50's Finance Pset.
8. ```survey_completed.html``` Renders the Survey page when the user has completed the survey before - this shows the previously recommended show.
9. ```survey.html``` Renders the Survey page when the user has never completed the survey before - this shows the actual survey.

## Python 
We have 4 Python files on our app. Below, we dive into the implementation of each of these files.  
### app.py
Contains the functions that render the pages of our Flask app. Some of these functions will be covered in more detail below, when we detail how we implemented specific pages.

### helpers.py 
Contains two helper functions - a decorator that checks if a user is logged in and a function that returns an apology page.
Modified from CS50's Finance Pset.

### insertimage.py
Contains two helper functions that allow us to turn image data into BLOB data that we can insert into our SQL database. Modified from [https://pynative.com/python-sqlite-blob-insert-and-retrieve-digital-data/](https://pynative.com/python-sqlite-blob-insert-and-retrieve-digital-data/).

### recommendation.py
Contains two functions that together allow us to recommend the user a musical based on their inputted values. 

The function ```find_distance``` takes the user's data and the 
ratings of a specific musical as parameters, then returns the "distance" between the user's data and the specific musical. The distance is calculated by taking the square of the difference in the ratings, summing all the squared differences, and then returning the square root of that value. 

The function ```find_closest``` takes in the user's data and a list of the ratings of all the shows as parameters. It calculates the "distance" between each show and the user's data using ```find_distance```, storing the "distances" in a dictionary with the ids of the musicals as keys. It then returns the id of the musical that was the "closest" to the users data. 

## Home
The Python function for rendering the home page is simply ```index()```, and it just renders the ```index.html``` page. It only accepts ```GET``` requests. No login is required to access this page.

For the home page, there are three carousel pages with buttons on them. Both the carousel and buttons were implemented with Bootstrap. When clicking on the buttons on the pictures in the carousel, the user will be directed to corresponding page.

This is just another way to jump to pages other than the navigation bar. 

## Survey
The Python function for rendering the survey page is ```survey()```. It accepts ```GET``` and ```POST``` requests, and depending on various inputs it will render differently. Login is required because we need to access and save user data.

If the request is a ```GET``` request, there are two possibilities: the user has submitted the survey before or the user has not submitted the survey before. We check this by checking the value of the user's ```survey_completed``` column in our SQL database. 

If the user has submitted the survey before, the value in ```survey_completed``` is 1. We then select the musical data from our database using SQL and then render the ```survey_completed.html``` page with this data.  

If the user has not submitted the survey before (or wants to retake the survey), the value in ```survey_completed``` is 0. We then select the questions and answers from our database and render the ```survey.html	``` page using this data.

If the request is a ```POST``` request, there are two possibilities: the user is trying to submit the survey, or the user wants to retake the survey. We check which action they want to take by checking the value of the ```request.form["survey_page_action"]``` field. 

If the value of ```request.form["survey_page_action"]``` is ```submit_survey```, the user is trying to submit their survey. We then try to retrieve their data, convert it into the right datatype (integer), and add it to a dictionary. We also check that their data is in the correct range of values. If any of these checks fail, we return an apology page.  

If the user's data successfully passes these checks, we query our SQL database for the data of the musicals - specifically, we get the values of the romance, humour, fiction_history, action, and mystery columns for every musical. 

We then pass the user's data and the musicals' data into our ```find_closest``` helper function (see [recommendation.py](#recommendation.py)) to find the id of the recommended musical. Afterwards, we get this musical's data and themes. We also update the user's ```survey_completed``` column to be 1 and their ```recommended_musical_id``` to contain the id of the recommended musical. Finally, we render the ```survey_completed.html``` page with the recommended musical's data.

If the value of ```request.form["survey_page_action"]``` is ```retake_survey```, the user is trying to retake the survey.  We set the user's ```survey_completed``` column to be 0 and their ```recommended_musical_id``` to be ```NULL``` before redirecting them to 	```/survey``` to take the survey again. 

Of course, it is possible to mess with the values of buttons. If the value of ```request.form["survey_page_action"]``` is neither of the above options, we return an apology page.

## Explore

The Python function for rendering the explore page is ```explore()```. It accepts ```GET``` and ```POST``` requests, and depending on various inputs it will render differently. 

If the Explore page receives a ```POST``` request, users will be first directed to ``` explore.html ```. This page has a container that contains our search inputs and has info cards for all of the musicals in our database below that. To get lists for our advanced search options and for the info cards, we query our database. 

The user can type words into the search bar and also select options in the advanced search. Clicking the Reset button will send another ```GET``` request to ```/explore```, effectively clearing all the inputs. Clicking the Submit button will send a ```POST``` request to ```/explore```.

When ```explore()``` receives a ```POST``` request, we perform two searches. For the basic search, we simply look to see if any of the descriptions of the musicals contain the characters inputted. For the advanced search function, we started with the basic search's SQL query and appended any additional criteria the users selected. We then we pass this modified SQL query into ```db.execute```. We then render the Explore page again, with this new info inputted. If there is a match(s), only the match(s) will be shown on the Explore page. If there is no match, we will just show text that indicates there is no match and the info cards of all the musicals will be shown shown again.

The info cards on the Explore page only contain the snippets of the musicals. By clicking on the card, users will be directed to ``` /musical_info/<musical_name> ```, where we use jinja to render corresponding posters, name, language, theme, settings and description for each musical.

## Specific Musicals
When a user clicks on an info card in Explore, they are directed to the url ``` /musical_info/<musical_name> ```, where ```<musical_name>``` is the name of a specific musical in our database. If an invalid name is inputted, we return an apology message. This page is rendered with ```musical_info(musical_name)```. We simply get the musical's data from our database and render a simple info page from the data. 

## Images
The ```/images/<photo_type>/<musical_name>``` URL is not normally accessible from our webpage. However, you can access it by keying it in manually, where ```<photo_type>``` is either ```vphoto``` or ```hphoto``` and  ```<musical_name>``` is the name of a specific musical in our database.  It is necessary to display the images stored in the BLOB columns of our database as images in our HTML pages. 

When a user accesses this page, we first check if the inputted parameters are valid. If they are not, we return an apology page. Otherwise, we select the correct type of photo from the database and convert it into a format that HTML can understand with Python's built in ```BytesIO()``` function. We then send the converted data with Flask's built in ```send_file()``` function. 

The code to display the images (and the code for this route/Python function) is modified from https://stackoverflow.com/questions/63340686/render-blob-from-sqlite-server-in-html-with-flask-python.

## Login, Logout, Register
The Login, Logout, and Register pages are implemented with ```login()```, ```logout()```, and ```register()```. They are pretty simple, and are modified from CS50's Finance Pset.

----

> Written with [StackEdit](https://stackedit.io/).

