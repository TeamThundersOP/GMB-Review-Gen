from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

def generate_review(business_name, rating):
    keywords = ["digital marketing", "web development", "app development", "social media", "WhatsApp marketing", 
                "digital agency in Mumbai", "best digital agency", "professional", "reliable"]
    
    prompt = f"""Generate a simple, natural-sounding Google review for InboxTales digital agency from {business_name}. 
    Requirements:
    1. Must be exactly 3-4 short sentences
    2. Use simple, conversational language
    3. Include 1-2 of these keywords naturally: digital marketing, web development, app development, social media
    4. Mention one specific positive outcome
    5. {rating} stars out of 5
    6. Keep it very simple and easy to read
    7. Sound like a real customer review
    
    Example format:
    "Great digital agency for our web development needs. The team delivered exactly what we wanted on time. Very professional and reliable service."
    """

    url = "https://www.ninjachat.ai/api/chat"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if not response.text.strip():
            return {"error": "Received an empty response from AI API."}
        
        # Clean up and simplify the response
        review_text = response.text.strip()
        # Remove any quotes at the start and end
        review_text = review_text.strip('"\'')
        # Split into sentences and take only first 4
        sentences = [s.strip() for s in review_text.split('.') if s.strip()][:4]
        # Rejoin with proper spacing and punctuation
        final_review = '. '.join(sentences) + '.'
        # Remove any double periods
        final_review = final_review.replace('..', '.')
        
        return {"success": True, "review": final_review}
    except requests.exceptions.RequestException as e:
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