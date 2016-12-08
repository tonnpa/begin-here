==================================
|   |\            |  |            |
|   |/  __ _      |__| __ _  __   |
|   | \|_ / _||\ ||  ||_ |_||_    |
|   |_/|__\_/|| \||  ||__| \|__   |
==================================

Developer's Guide | User's Manual

The following 4 sections will describe:
	1. Package structure
	2. Installation guide
	3. User manual (how to use)
	4. Showcase guide (how to demo)

Repository: https://github.com/tonnpa/begin-here

----------------------------
|   1. Package structure   |
----------------------------

BeginHere is a web application, and the structure follows
that of a Django project.
begin-here/
			begin_here/			<= location of Django
								   project-wide settings
			data/				<= location of raw data
								   files to populate the DB
			foodmap/			<= Django application,
								   we highlight the most
								   important files, folders
					models.py	<= database tables
					static		<= static web resources
								   such as images, css, js
					templates	<= HTML files
					views.py	<= contains functions that
				 				   define what data gets
				 				   rendered on the frontend
			load.py				<= script for populating
								   the database
			PostGISQueries.sql	<= script for calculating
								   grid point attributes
			requirements.txt	<= list of python package
								   dependencies
			venv/				<= suggested location for
								   virtualenv files

-----------------------------
|   2. Installation Guide   |
-----------------------------

2.1 Recommended Operation System
	Ubuntu 16.04 (LTS) Xenial

2.2 Software requirements
	Python 2.7.x
	python-pip
	virtualenv (install via pip)
	git
	PostgreSQL 9.5.5

2.3 Installation

Step 1. Clone the repository
	git clone https://github.com/tonnpa/begin-here.git
	cd begin-here

Step 2. Set up virtual environment with required packages
	From here onwards, we assume the current
	working directory is ~/begin-here
	- Activate the virtual environment
	virtualenv venv
	- Install required packages
	pip install -r requirements.txt

Step 3. Set up the database
	- Create the database tables
	python manage.py migrate

Following these steps, the web server could be started with
	python manage.py runserver
And the user should be able to access the homepage at the
assigned port.
