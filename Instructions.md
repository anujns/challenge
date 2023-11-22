Instruction to run app

1. Install Docker [https://www.docker.com/get-started/]
2. Create a GIPHY API Key, and add your API Key to the .env file. [https://developers.giphy.com/]
3. Create a python virtual environment in the source directory and activate it.
`python3 -m venv venv`
`source venv/bin/activate`
4. Run the command `make start`.
5. Search for gifs on the browser: Eg. http://localhost:8080/query?searchTerm=a&searchTerm=b

Improvements to app.py to make production ready

1. Concurrency Handling [IMPLEMENTED]:
* Flask's built-in server is single-threaded, which means it cannot handle multiple requests simultaneously. This is not ideal for production environments.
* We can use a WSGI server like Gunicorn: Gunicorn can handle multiple requests concurrently by spawning multiple worker processes.
* Command: `gunicorn -w 4 -b 127.0.0.1:8080 app:app`
* This command runs app.py with 2 worker processes (-w 2) listening on localhost port 8080.

2. Latency [IMPLEMENTED]:
* If the Giphy API response is slow, it can cause high latency.
* Caching: Using a caching mechanism to store the results of queries for a specific time. This will reduce the number of API calls and improve response times for repeated requests.
* We can use the library Flask-caching, that uses the in-memory cache for development by default, which will cache the output of the search_gifs() function based on the unique query string parameters provided.
* In a production environment, it is better to use a persistent cache like Redis.

3. Edge Cases [IMPLEMENTED]:
* Input Validation: We can validate the search terms doing GET request to the Giphy API to prevent malformed requests. Example cases:
* a. Empty search terms. Eg. searchTerms=[], [""]
* b. Special characters in search terms.
* For such cases, we can return a 400 Bad Request response.

4. API Rate Limiter [IMPLEMENTED]:
* If the service becomes popular and user base increases, the request load may exceed the Giphy API's rate limits.
* By default, the GIPHY API is rate limited at
    - 42 reads per hour.
    - 1000 searches/API calls per day.
* We can still work with these constraints, but can also implement rate limiting in Flask, to control the number of requests from a client.
* We can use the library Flask-Limiter to limit the number of requests a client can make to the API within a certain time window.

5. Logging [IMPLEMENTED]:
* We can use Python library `logging` to log messages that are helpful when debugging in production environment.

6. Error Handling [IMPLEMENTED]:
* We can create custom error handlers to catch errors like 404 and 500 errors and return formatted responses to client. Examples:
* 404 Error Handler: Handler is invoked when a client requests a non-existent endpoint, for eg. http://localhost:8080/home
* 500 Error Handler: Handler is invoked for unhandled exceptions in the application which returns Internal Server Error.

7. Environment Variable Management [IMPLEMENTED]:
* Store all environment variables like API Keys and tokens in a .env file, which have benefits like protecting sensitive data, and making it easier to run the application in different environments.

8. Monitoring:
* We can use tools like AWS Cloudwatch to continuously monitor the application for performance and faults. We can set up metrics that measure things (eg. number of requests per hour) , and create alarms to alert is when thresholds are passed.

9. Testing
* In addition to unit testing, we can also have load testing by subjecting the application to high traffic.