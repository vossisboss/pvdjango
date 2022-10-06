# Step One: Set up Wagtail

## Create a virtual environment

### _Gitpod_

If you don't have Python already installed on your machine or if you would prefer not to troubleshoot environment issues, then you can complete this workshop in Gitpod. You will have to be more careful about saving your work since Gitpod environments deactivate after a period of inactivity.

Click the button below to launch Gitpod.

**NOTE**: A GitHub account is required to use Gitpod

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/vossisboss/pvdjango-gitpod)

### _Venv_

If you already have Python installed on your machine, you can create a local virtual environment using `venv`. Open your command line andnavigate to the directory you want to build your project in. Then enter the following commands to creative a virtual environment.

```
python 
python -m venv env
source env/bin/activate
```

## Set up Wagtail

Once you have a virtual environment set up, we can install Wagtail and start setting up our very first Wagtail website. In your project directory, enter the following command in your command line:

```
pip install wagtail
```

This command tells the Python package manager pip to install the latest release of Wagtail along with all of the dependencies that are needed for Wagtail. After Wagtail is installed, you can confirm that it is installed with:

```
pip show wagtail
```

After Wagtail is installed, you can use one of Wagtail's built-in commands to start a brand new website. For this tutorial, we're going to be creating a mini-blog project called `myblog`.

```
wagtail start myblog .
```

Don't forget the `.` at the end of the command. It is telling Wagtail to put all of the files in the current working directory.

Once all of the files are set up, you'll need to enter some commands to set up the test database and all of the migration files that Wagtail needs. You can do that with the `migrate` command.

```
python manage.py migrate
```

After the migrations are complete, you'll need to create a superuser so that you can access the backend of your Wagtail website. Use the following command:

```
python manage.py createsuperuser
```
Follow the prompts in your command line to create your superuser. Once you have a superuser set up, you can start up the test server to see your new Wagtail site in action.

```
python manage.py runserver
```
If the server has started up without any errors, you can navigate to [http://127.0.0.1:8000 ](http://127.0.0.1:8000 ) in your web browser to see your Wagtail website. If you've successfully installed Wagtail, you should see a home page with a large teal egg on it.

To test that your superuser works, navigate to [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) and login with the credentials you created.

Now you have a basic Wagtail website set up. Next, we're going to add a package that will help you organize and translate content across different languages and locales.

