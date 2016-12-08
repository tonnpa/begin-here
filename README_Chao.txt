-----------------------------
|   3. How to Use		    |
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

Step 3: On bottom-right panel, click the priority bars according 
	to your preferences from most important to least.

	Then, choose importance ranking by clicking one of the 4 
	options below.

	Click 'Highlight Your Locations'. Wait for a pop-up 
	window showing 'All Done!'. Click 'OK'.

Step 4: Put http://127.0.0.1:8000/choropleth into browser
	address bar. A choropleth map is now displayed on the
	left panel.

-----------------------------
|   4. Demo				    |
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
	-- Copy http://127.0.0.1:8000/choropleth to browser


