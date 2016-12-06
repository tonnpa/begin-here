-- Query the number of EvalPts in each of the Census Tracts
UPDATE foodmap_censustract
	SET no_eval_pts = Q.counter
	FROM
		(
			SELECT  B.geoid as geoid, count(*) as counter
			FROM (
				SELECT location
				FROM foodmap_evaluationpoint
				) AS A
			LEFT JOIN (
				SELECT geoid, geom
				FROM foodmap_censustract
				) AS B
			ON  ST_Contains(B.geom, A.location)
			GROUP BY geoid
		) AS Q
	WHERE foodmap_censustract.geoid = Q.geoid;


-- Calculate/Update the population density (per eval pt)
UPDATE foodmap_censustract
	SET pop_density = population/no_eval_pts;

-- Query to link the EvalPts with the CensusTracts
UPDATE foodmap_evaluationpoint
	SET ct_geoid = Q.geoid
	FROM
		(
			SELECT  A.id as id, B.geoid as geoid
			FROM (
				SELECT id, location
				FROM foodmap_evaluationpoint
				) AS A
			LEFT JOIN (
				SELECT geoid, geom
				FROM foodmap_censustract
				) AS B
			ON  ST_Contains(B.geom, A.location)
		) AS Q
	WHERE foodmap_evaluationpoint.id = Q.id;


-- Delete census tracts outside of the targeted region
DELETE FROM foodmap_censustract WHERE no_eval_pts IS NULL;


-- Update EvaluationPoints with population and income from CensusTracts
UPDATE foodmap_evaluationpoint
	SET population = pop_density,
		  income = income
	FROM foodmap_censustract WHERE foodmap_censustract.geoid = foodmap_evaluationpoint.ct_geoid;


-- Count local crimes
UPDATE foodmap_evaluationpoint
	SET crime_count_local = Q.counter
	FROM
		(
			SELECT  B.id, count(*) as counter
			FROM (
				SELECT location
				FROM foodmap_crime
				) AS A
			LEFT JOIN (
				SELECT id, poly_pts
				FROM foodmap_evaluationpoint
				) AS B
			ON  ST_Contains(B.poly_pts, A.location)
			GROUP BY B.id
		) AS Q
	WHERE foodmap_evaluationpoint.id = Q.id;


-- Count neighborhood crimes
UPDATE foodmap_evaluationpoint
	SET crime_count_neighborhood = Q.counter
	FROM
		(
			SELECT  B.id, count(*) as counter
			FROM (
				SELECT location
				FROM foodmap_crime
				) AS A
			LEFT JOIN (
				SELECT id, bigpoly_pts
				FROM foodmap_evaluationpoint
				) AS B
			ON  ST_Contains(B.bigpoly_pts, A.location)
			GROUP BY B.id
		) AS Q
	WHERE foodmap_evaluationpoint.id = Q.id;


-- Add evaluation point ID to the restaurants
UPDATE foodmap_restaurant
	SET eval_pt_id = Q.id
	FROM
		(
			SELECT  B.id, A.rest_id
			FROM (
				SELECT location, id as rest_id
				FROM foodmap_restaurant
				) AS A
			LEFT JOIN (
				SELECT id, poly_pts
				FROM foodmap_evaluationpoint
				) AS B
			ON  ST_Contains(B.poly_pts, A.location)
		) AS Q
	WHERE foodmap_restaurant.id=Q.rest_id;


-- Remove evaluation point that has no restaurant in its vicinity
DELETE FROM foodmap_evaluationpoint
  WHERE foodmap_evaluationpoint.id NOT IN (
      SELECT foodmap_restaurant.eval_pt_id
      FROM foodmap_restaurant
      WHERE foodmap_restaurant.eval_pt_id IS NOT NULL
  );

-- Normalize Crime Count (1/2)
UPDATE foodmap_evaluationpoint
	SET crime_count_local = crime_count_local/(population),
    crime_count_neighborhood = crime_count_neighborhood/(8*population) -- approximate population of the neighborhood
  WHERE population>0;

-- Normalize Crime Count (2/2)
UPDATE foodmap_evaluationpoint
SET crime_count_local = (select (avg(crime_count_local)) from foodmap_evaluationpoint Where population>0),
  crime_count_neighborhood = (select (avg(crime_count_neighborhood)) from foodmap_evaluationpoint Where population>0)
Where population=0;


