from flask import Flask, jsonify

app = Flask(__name__)

# Example transaction data
transactions = [
    {"id": 1, "amount": 100, "type": "credit"},
    {"id": 2, "amount": 50, "type": "debit"}
]

@app.route('/transactions', methods=['GET'])
def get_transactions():
    print("GET /transactions endpoint hit")
    return jsonify({"transactions": transactions})

@app.route('/')
def home():
    print("GET / endpoint hit")
    return "Flask API is working!"

if __name__ == '__main__':
    app.run(debug=True)
