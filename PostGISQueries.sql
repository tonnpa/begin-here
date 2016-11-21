## Query the number of EvalPts in each of the Census Tracts
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


## Calculate/Update the population density (per eval pt)
UPDATE foodmap_censustract
	SET pop_density = population/no_eval_pts;

## Query to link the EvalPts with the CensusTracts
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


## Delete census tracts outside of the targeted region
DELETE FROM foodmap_censustract WHERE no_eval_pts IS NULL;


## Update EvaluationPoints with population and income from CensusTracts

UPDATE foodmap_evaluationpoint
	SET population = pop_density,
		income = income
	FROM foodmap_censustract WHERE foodmap_censustract.geoid = foodmap_evaluationpoint.ct_geoid;



### MODIFY THIS TO CALCULATE CRIMES

SELECT foodmap_censustract.geoid, count(*)
	FROM foodmap_evaluationpoint, foodmap_censustract
	WHERE ST_DWithin(geography(location), geography(geom), 1)
	GROUP BY geoid
	LIMIT 10;


