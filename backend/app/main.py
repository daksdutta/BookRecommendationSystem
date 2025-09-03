from flask import Flask, request, jsonify
from flask_cors import CORS
from recommendation import get_popular_books, recommend

app = Flask(__name__)
CORS(app)  


#Route for popular books
@app.route("/popular", methods=["GET"])
def popular_books():
    try:
        books = get_popular_books()
        return jsonify(books)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


#Route for recommendation
@app.route("/recommend", methods=["GET"])
def recommend_books():
    try:
        book_name = request.args.get("book")
        if not book_name:
            return jsonify({"error": "Please provide a book name"}), 400

        recommendations = recommend(book_name)
        if not recommendations:
            return jsonify({"message": f"No recommendations found for '{book_name}'"}), 404

        return jsonify(recommendations)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
