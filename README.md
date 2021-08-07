# What is it
FinHelp is a web based currency converter. It allows you to:
- Convert a certain amount of one currency to another
- Be informed of the current [Bulgarian National Bank](https://www.bnb.bg/)'s currency conversion rates

The application autmatically updates its conversion rate information on a daily basis and presents a user-editable table with all supported currencies so that currency names and rates can be edited manually at any time.

# Run the app in evelopment mode
There are just a few things you need to do to run FinHelp in development mode:

1. Make sure you have [Python](https://www.python.org/downloads/) and [Django](https://www.djangoproject.com/download/) installed. 
2. Clone this repo by running `git clone https://github.com/ivi-dev/Fin-Help.git .` in a terminal/command prompt.
3. `cd` into the newly created directory.
4. Run `python manage.py runserver` in a terminal/command line. That starts up a lightweight local server and makes the app accessible at `http://localhost:8000` through a web browser.

When you're done working on the app hit **Ctrl + C** in the terminal/command line that you used to start the server.

Checkout the [Django's docs](https://docs.djangoproject.com/en/3.2/) for instructions on how to work with it. Make sure you select the version of Django that this project uses via the selector labeled _"Documetation version:"_ at the bottom right of the page. If not sure you can check the version of Django that's used by the project by running `pip show Django` in a terminal/command prompt from within the project's local root directory (the one that was created by cloninig this project).

# Authors
[Iliyan Videv](mailto:videviliyan@gmail.com)

# License
[**MIT License**](https://github.com/ivi-dev/CWG/blob/master/LICENSE)
