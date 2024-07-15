INSTRUCTIONS


Before testing this API, you need to create and run a local PostgreSQL database.
If you have a running database, you need to edit the 'database.py' file in the 'app' folder such that the database url is that of your own local database:

	DATABASE_URL = "{url of your database}"


The Application can be started as follows:

	1. go to the project directory
	2. start the pip virtual environment
	3. run 'main.py'



When the application is running, the endpoints can be tested using Postman.

The arxiv endpoint can be tested as follows:

	1. create a new request
	2. choose POST as http method
	3. enter the following url: http://localhost:5000/api/arxiv
	4. go to the tab 'Body'
	5. choose 'raw' and select JSON from dropdown menu
	6. enter desired JSON payload, for example:

		{
    			"query": "dermatology",
    			"max_results": 5
		}

	7. click Send


The queries endpoint can be tested as follows:

	1. create a new request
	2. choose GET as http method
	3. enter the following url: http://localhost:5000/api/queries
	4. go to the tab 'Params'
	5. add the parameters 'query_start_time' and 'query_end_time'
	6. enter the desired values in datetime format, for example:
		
		'2024-07-15T12:00:00',
		'2024-07-15T18:00:00'

	7. click Send


The results endpoint can be tested as follows:

	1. create a new request
	2. choose GET as http method
	3. enter the following url: http://localhost:5000/api/results
	4. click Send




