# trail-votes-api

FastAPI backend to vote on trailheads,
powering the [trail-votes-map](https://github.com/dvrpc/trail-votes-map) frontend.

## Development Environment Setup

- Create a Python virtual environment: `python -m venv env`
- Activate the environment: `source env/bin/activate`
- Install requirements: `pip install -r requirements.txt`

## Run the API locally

- `uvicorn app.app.main:app --reload`

## Test Deployment

Continuous deployment is setup using GitHub Actions,
and every push to `main` redeploys the app
to a Digital Ocean droplet running `dokku`.
The documentation can be found
here: https://vote-api.planninglab.org/api/trail-votes
