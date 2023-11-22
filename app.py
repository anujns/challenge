from flask import Flask, request, jsonify
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

app = Flask(__name__)
GIPHY_API_KEY = os.environ.get('GIPHY_API_KEY')

# Configure cache with a default timeout of 5 minutes (300s)
cache = Cache(config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 300})
cache.init_app(app)

# Initialize a rate limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "40 per hour"]
)

@app.route('/query')
@cache.cached(query_string=True)
@limiter.limit("10 per minute")
def search_gifs():
    app.logger.info('Processing search request...')
    search_terms = request.args.getlist("searchTerm")
    try:
        if not search_terms or not all(search_terms):
            return jsonify({'error': "Invalid search terms provided"}), 400
        results={"data":[]}
        for term in search_terms:
            response = requests.get(
                "http://api.giphy.com/v1/gifs/search",
                params={"api_key": GIPHY_API_KEY, "q": term, "limit": 10}
            )
            gifs=response.json()["data"]
            gif_urls=[{"gif_id": gif['id'], "url": gif['images']['fixed_height']['url']} for gif in gifs]
            results["data"].append(
                {"search_term": term,
                "gifs": gif_urls }
            )
        app.logger.info('Processed results...')
        return jsonify(results)

    except requests.exceptions.HTTPError as e:
        # Check if the rate limit has been exceeded
        if e.response.status_code == 429:
            app.logger.error('GIPHY API rate limit exceeded')
            return jsonify(error='Rate limit exceeded'), 429
        else:
            app.logger.error(f'HTTPError: {e}')
            return jsonify(error='An error occurred'), 500
    except Exception as e:
        app.logger.error(f'An unexpected error occurred: {e}')
        return jsonify(error='An internal error occurred'), 500


@app.errorhandler(400)
def bad_request(error):
    app.logger.error(f"Bad request: {error}")
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(404)
def not_found(error):
    app.logger.error(f"Not found: {request.url}")
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_server_error(e):
    app.logger.error('Server Error: %s', (e,))
    return jsonify(error='An internal error occurred.'), 500

if __name__ == "main":
    app.run(port=8080)
