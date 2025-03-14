from flask import Flask, render_template, request, jsonify
import random
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

def generate_review(business_name, rating):
    try:
        # Simple templates for reviews
        templates = [
            "Really impressed with InboxTales' {service}. {outcome} {closing}",
            "Had a great experience with InboxTales for our {service} needs. {outcome} {closing}",
            "InboxTales did an excellent job with our {service}. {outcome} {closing}",
            "Very satisfied with InboxTales' {service} service. {outcome} {closing}"
        ]

        services = [
            "digital marketing",
            "web development",
            "app development",
            "social media marketing",
            "digital solutions"
        ]

        outcomes = [
            "They delivered exactly what we needed on time",
            "The results exceeded our expectations",
            "Our online presence improved significantly",
            "The project was completed perfectly",
            "They helped us achieve our goals efficiently"
        ]

        closings = [
            "Highly recommended!",
            "Would definitely work with them again.",
            "A reliable partner for digital solutions.",
            "Great communication throughout."
        ]

        # Generate review components
        template = random.choice(templates)
        service = random.choice(services)
        outcome = random.choice(outcomes)
        closing = random.choice(closings)

        # Format the review
        review = template.format(
            service=service,
            outcome=outcome,
            closing=closing
        )

        return {"success": True, "review": review}

    except Exception as e:
        print(f"Error generating review: {str(e)}")  # Server-side logging
        return {"success": False, "error": "Failed to generate review. Please try again."}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400

        business_name = data.get('business_name', '').strip()
        rating = data.get('rating', '5')

        if not business_name:
            return jsonify({"success": False, "error": "Business name is required"}), 400

        result = generate_review(business_name, rating)
        return jsonify(result)

    except Exception as e:
        print(f"Server error: {str(e)}")  # Server-side logging
        return jsonify({"success": False, "error": "Server error. Please try again."}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 