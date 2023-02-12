from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import requests 

site = Blueprint('site', __name__, template_folder='app/templates')

@site.route('/', methods=["POST", "GET"])
def landing_page():
    '''
    if request.method == 'POST':
        form_data = request.form
        
        url = '/numbers'
        response = request.post(url, json=form_data)
        
        if response.status_code == 200:
            response_data = response.json()
            
            # Issue the GET request to the same API
            get_response = request.get(url)
            if get_response.status_code == 200:
                get_response_data = get_response.json()
                # Process the response data as needed
                # ...
                
                # Return the processed data to the client as part of the response
                return jsonify(get_response_data)
            else:
                return 'GET request failed', get_response.status_code
        else:
            return 'POST request failed', response.status_code
    else:
        '''
    return render_template('index.html')
