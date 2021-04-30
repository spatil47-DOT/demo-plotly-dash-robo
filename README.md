# HerokuDashboardUR
Data Dashboard to visualize Robot Data on Heroku. 

You may view it [here](https://ur-robot-data-app.herokuapp.com/).

# Background
A web dashboard for data visualization, with the help of mainly Flask, Bootstrap, Plotly and Heroku.

# Deployment
  * First, create a virtual environment locally on your computer. I used [Anaconda](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) for this.

  * install [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

  * create new folders to house all your files. If you are using Linux:
    * `mkdir web_app`
    * `mv -t web_app data robotapp wrangling_scripts robot_app.py`

  * activate your environment and pip install the libraries for the web app:
    * ` pip install flask pandas plotly gunicorn`

  * [install Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli). I'm using the Windows method.

  * log into heroku
  
  * cd into the `web_app` folder so that you are inside the folder with the `robot_app.py` code

  * Create a proc file, which tells Heroku what to do when starting the web app
    * `touch Procfile`
  
  * Open the procfile and type:
    * `web gunicorn robot_app:app` (*name of the python file* : app)
    
  * Create a `requirements.txt` file, which lists all the Python libraries that your app depends on:
    * pip freeze > requirements.txt
    
  * Initialize a git repository and make a commit (still in web_app directory)
    * `git init`
    * `git add .`
    * `git commit -m "first commit"
    
  * Create a heroku app
    * `heroku create my-web-app-name`
    * The heroku create command should create a git repository on Heroku and a web address for accessing your web app. You can check that a remote repository was added to your git repository with the following terminal command:
      * git remote -v
   
  * Push your git repository to the remote heroku repository with this command:
    * `git push heroku master`
   
# Debugging
In the CLI, type in `heroku logs –t` while loading the page to look at debugging info.
