from flask import Flask, render_template, request, jsonify
import random
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

def generate_review(business_name, rating):
    # Templates for different parts of the review
    intros = [
        "Highly impressed with InboxTales' {service}.",
        "Had an excellent experience with InboxTales for our {service} needs.",
        "Working with InboxTales on our {service} project was fantastic.",
        "Really satisfied with InboxTales' approach to {service}.",
    ]
    
    services = [
        "digital marketing",
        "web development",
        "app development",
        "social media marketing",
        "digital solutions",
    ]
    
    outcomes = [
        "They delivered exactly what we needed on time.",
        "The results exceeded our expectations.",
        "Our online presence improved significantly.",
        "The project was completed perfectly.",
        "They helped us achieve our goals efficiently.",
    ]
    
    closings = [
        "Highly recommended for any business looking for professional service.",
        "Would definitely work with them again.",
        "A reliable partner for digital solutions.",
        "Great communication throughout the project.",
    ]

    try:
        # Generate the review
        intro = random.choice(intros).format(service=random.choice(services))
        outcome = random.choice(outcomes)
        closing = random.choice(closings)
        
        # Combine the parts
        review = f"{intro} {outcome} {closing}"
        
        return {"success": True, "review": review}
    except Exception as e:
        return {"error": str(e)}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    business_name = data.get('business_name')
    rating = data.get('rating')

    if not business_name or not rating:
        return jsonify({"error": "Business name and rating are required"}), 400

    result = generate_review(business_name, rating)
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 