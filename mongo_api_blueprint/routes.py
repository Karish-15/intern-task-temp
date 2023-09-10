from .api_blueprint import User_details, User_by_id

def initialize_routes(api):
    api.add_resource(User_details, '/users')
    api.add_resource(User_by_id, '/users/<id>')