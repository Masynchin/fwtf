from app.api.jobs_api import blueprint as jobs_blueprint
from app.api.users_api import blueprint as users_blueprint


api_blueprints = [jobs_blueprint, users_blueprint]
