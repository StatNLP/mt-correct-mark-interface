# mt-correct-mark-interface
Interface for collecting machine translation error corrections and markings

## Requirements

### node.js

- yarn

- webpack

- (p)react // Preact is a drop-in replacement for React. Preact was used because it produces smaller javascript bundles and the webpack and babel configs are written for it

- Babel

- Postcss

Install all node requirements by running `yarn install` in the root project directory

Webpack uses the fsevents and the annotation interface uses node-sass, both of which are native addons and may be compiled locally if prebuilt binaries are not found by npm. In this case a C++ compiler and python2.7 may be neccessary. 

### Python3.53

- Flask-{bcrypt, login, migrate, sqlalchemy, wtf}

Install all python requirements by running `pip3 install -r requirements.txt`

## Building the site

After installing the requirements, the static assets (html, css, js) can be built by running `webpack-cli` in the root directory. This will compile all static assets and copy them to the directory `annotproj/static`. The default build produces development builds with source maps for debugging purposes but can be changed in the webpack.config.js file.

## Creating the database

The annotation backend uses an sqlite database to store user information and annotations. The following commands will create an empty sqlite database file, create the migrations folder for upgrading the database, and then create the empty tables in the database file.

    flask db init
    flask db migrate
    flask db upgrade

Once this is done you can add un-annotated data by importing the database definitions in python and writing your data. See `dummydata.py` or `mkdb.py` for examples.

Create as many empty user rows as you think you will need and set `registered=False` in each row. When users register through the website, the backend will select the first row that where `registered=False` and update it with the new user information. This allows you to pre-allocate data to user ids and limit the number of registered users. If you want users to register first then you can change the function `def register()` in `annotproj/routes.py` to create a new user object instead of selecting an empty user.

## Running the site

Once all the static assets are in place, you can run the website by exporting the `app.py` in the project root as the environment variable `FLASK_APP`.

    export FLASK_APP=app.py
    flask run

## Customizing the website

The website was written for native/fluent German speakers to annotate En->De translation data. As such, many things in the website are hard-coded for that language pair. You may wish to change the fluency fields in the registration page from English and German to whatever language pair you are studying. To do this you can edit the registration form in `annotproj/forms.py` to reflect the information you wish to collect. The database is defined in `annotproj/models.py` which also references English and German.

Additionally, when registering users, they agree that they have read and agree to the terms and conditions of the website. The terms and conditions would be found in `annotproj/static/consent_en.txt` and `annotproj/static/consent_de.txt` but have been removed because they contained information specific to our user study. The references to those files are in `annotproj/templates/register.html`, which you can update to reflect your own terms and conditions.

Static assets such as css and javascript are contained in the assets folder. The javascript files include the logic for tracking clicks, keystrokes, and time spent as well as collecting the postedits and markings. These can be updated for new feedback types or collecting new user statistics. The css can be updated to reflect your branding but a default bootstrap css theme is used.