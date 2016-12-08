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

Step 4. Populate the database
	- Download the snapshot of our database containing
	the model instances with cleaned and aggregated
	attributes from:
	https://app.box.com/s/x6b75wp0hns3djr1ocxphjed15hhjh7y
	- Place the snapshot.json into the folder 
		~/begin-here/foodmap/fixtures
	- Load the data
	python manage.py loaddata snapshot

Following these steps, the web server could be started with
	python manage.py runserver
And the user should be able to access the homepage at the
assigned port.

-----------------------------
|   3. How to Use	    |
-----------------------------

Step 1: Copy the url generated from 
	python manage.py runserver (eg. http://127.0.0.1:8000/)
	to browser address bar

Step 2: On top-right panel, you can make choices:
	-- Price range
	-- Yelp rating
	-- Competitor cuisines: The restaurants you aim to stay 
		away from. Please choose single or multiple options, 
		or all.
	-- Complementary cuisines: The restaurants you aim to 
		be close to.

	Click "Filter Results". See color codes in instructions.

Step 3: On bottom-right panel, click the priority bars 
	according to preferences from most important to least.

	Choose importance ranking by clicking one of the 4 
	options below.

	Click 'Highlight Your Locations'. Wait for a pop-up 
	window showing 'All Done!'. Click 'OK'.

Step 4: Put http://127.0.0.1:8000/choropleth into browser
	address bar. A choropleth map is now displayed on the
	left panel.

-----------------------------
|   4. Demo		    |
-----------------------------

Step 1: CD to working folder, for example:
	yourID@machine:~/Development/cse6242/begin-here$

Step 2: Activate virtual environment:
	yourID@machine:~/Development/cse6242/begin-here$ 
	source venv/bin/activate

Step 3: Run server:
	yourID@machine:~/Development/cse6242/begin-here$ 
	python manage.py runserver

Step 4: Copy url http://127.0.0.1:8000/ to browser

Step 5: Make a query:
	-- Select 'Moderate$$' and 'Pricey $$$'
	-- Select rating 3 to 5
	-- In Competitors: select 'mediterranean', 
		'mexican'
	-- In Complementary cuisines: select 'italian'
	-- Click 'Filter Results'
	-- Click 'Proximity of competitors','Population
		income', 'Crimes in the neighborhood'
	-- Click 'Somewhat more important'
	-- Click 'Highlight Your Locations'

Step 6: Display choropleth map:
	-- Wait for a pop-up window. Click 'OK'.
	-- Copy http://127.0.0.1:8000/choropleth to browser.


