from flask import Flask, render_template, request
from database import create_database, get_all_users, get_vacation_location
import requests
import json

# Initialize Flask app
app = Flask(__name__)

# Initialize the database
create_database()

# Llama2 API configuration
URL = "http://<ip>:11434/api/generate"
MODEL = "tinyllama:latest"

def generate_response(prompt):
    """
    Sends a prompt to the Llama2 API and returns the AI-generated response.
    """
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "max_tokens": 150
        }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(URL, json=payload, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get("response", "No response received.")
        else:
            print(f"Error from Llama2 API: {response.text}")
            return "Error communicating with the AI service."
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return "Error connecting to the AI service."

@app.route('/')
def index():
    """Render the homepage with a dropdown of usernames."""
    users = get_all_users()
    return render_template('index.html', users=users)

@app.route('/vacation', methods=['POST'])
def vacation():
    """Handle the form submission and display the vacation location and AI response."""
    user_id = request.form.get('user_id')
    location = get_vacation_location(user_id)
    username = next((user[1] for user in get_all_users() if user[0] == int(user_id)), None)

    if not username or not location:
        return render_template(
            'vacation.html',
            username="Unknown",
            location="Unknown",
            ai_response="Could not retrieve data. Please try again."
        )

    # Generate AI response
    prompt = f"Tell me why {location} is a great vacation destination in 200 words only"
    ai_response = generate_response(prompt)

    return render_template(
        'vacation.html',
        username=username,
        location=location,
        ai_response=ai_response
    )

if __name__ == '__main__':
    app.run(debug=True)
