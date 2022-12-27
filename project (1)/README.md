# Table of Contents
1. [Setting Up](#setting-up)
2. [Navigation](#navigation)
3. [Survey](#survey)
4. [Explore](#explore)
5. [Register](#register)
6. [Login](#login)
7. [Logout](#logout)
8. [Video Walkthrough](#video-walkthrough)

## Setting Up
Our project is designed to be run in the CS50 Codespace ([linked here](https://code.cs50.io/)). 
Download our ``` project.zip ``` file. Import it to your codespace and unzip using
```
unzip homepage.zip
```

to create a folder called  `project`. You no longer need the ZIP file, so you can execute
```
rm homepage.zip
```
and respond with “y” followed by Enter at the prompt to remove the ZIP file you downloaded.
Now type
```
cd project
```
followed by Enter to move yourself into that directory. Your prompt should now resemble the below.
```
project/ $
```
To run our Flask app, type the following command into your terminal
```
flask run --without-threads (check this)
```
Note that  you must include `--without-threads` for the webpage to work properly.

Click the link that pops up with Ctrl+click to open our app!

## Navigation
Upon opening our web app, you should see our homepage. There is a navigation bar on top, with links to the three main pages of our website: Home, Survey, and Explore. The glowing logo is also clickable and redirects to our homepage.
On the far right are two more links - one to register a new user, and one to log in. If you are already logged in, these buttons will not be present. Instead, there will be just one button on the far right that logs you out.

Additionally, there are three carousel slides on our homepage. The text on the slides is clickable, and they redirect to the 
Home, Survey and Explore pages respectively.

## Survey
To access the Survey page, you will have to log in. If you navigate to the Survey page through the navbar or through a URL before logging in, you will be redirected to the login page. Type in your username and password to be logged in. If you do not have a login yet, please [register](#register).

If you navigate to the Survey page after logging in, there are two things you may see. If it you haven't taken the survey before or have chosen to retake the survey, you will see five questions. Answer them and click the Submit Survey button at the bottom of the page, and you will get your recommendation!
*Note: The survey will not let you submit until you answer all questions.*

If you have taken the survey before, our database will remember the recommendation for you. So the next time you log in with the same username, you will be able to see the same recommendation on the Survey page. At the bottom of the page, there is a button you can click to retake the survey and get a new recommendation.

## Explore
You can also browse our Explore page, which does not require a log in. Our search bar is a basic keyword search that searches the descriptions of our musicals. You can use the advanced search function to condition your search for musicals based on languages, themes and settings.
*Note: We had to build the database of musicals from scratch by ourselves, so we apologize if there is not a lot of musicals in there yet.*

## Register
Use this page to register a new account on our website. There are three ways to reach this page - clicking the Register button on the navigation bar when you are not logged in already, clicking the register button on the Login page, or typing in the direct URL. 

On this page, you will be type in your proposed username and password, then to confirm your password.  After hitting the Register button, you will be logged in and redirected to the Home page if registration was successful. 

If you are redirected to an error page instead that contains a picture of a cat, your submission is invalid in some way. An error will occur in the following scenarios:

- The username, password, or confirm password fields are blank
- You try to register with a username that already exists in our database
- The confirm password and password fields do not match 

The error picture will tell you exactly what your error is. You may navigate away from the error page using the navigation bar at the top.

## Login
Once you navigate to this page (or are redirected to this page), please type in your username and password to login. Upon successful login, you will be redirected to the Home page. 

If you do not have an account, you can click the Register link on this page to be taken to the registration page.

## Logout
Clicking this button logs you out. You will be redirected to the Home page upon a successful logout.

## Video Walkthrough
https://youtu.be/jIeO3RbkhOA

___

> Written with [StackEdit](https://stackedit.io/).
