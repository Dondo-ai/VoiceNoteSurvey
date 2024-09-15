from app.blueprints.home import home_bp

@home_bp.route('/', methods=['GET'])
def home():
    # Process the incoming data here
    # For example, you can log it or trigger some other actions
    return "<p>Welcome to the Dondo Api!</p>"

    # Return a response
    #return jsonify({'status': 'Welcome home', 'data': data}), 200
