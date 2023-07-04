from flask import Flask, request, jsonify
import ai_model

app = Flask(__name__)

@app.route('/get_recommendation', methods=['POST'])
def get_recommendation():
    user_query = request.json['query']
    recommendation = ai_model.generate_recommendations(user_query)
    return jsonify({'recommendation': recommendation})

if __name__ == '__main__':
    app.run(debug=True)
