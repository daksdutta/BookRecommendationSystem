import os
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#Load Dataset
books = pd.read_csv(os.path.join(BASE_DIR, "data/Books.csv"), low_memory=False)
users = pd.read_csv(os.path.join(BASE_DIR, "data/Users.csv"), low_memory=False)
ratings = pd.read_csv(os.path.join(BASE_DIR, "data/Ratings.csv"), low_memory=False)

# Merge books with ratings
ratings_with_name = ratings.merge(books, on="ISBN")

# Convert ratings to numeric
ratings_with_name["Book-Rating"] = pd.to_numeric(ratings_with_name["Book-Rating"], errors="coerce")

# Aggregate: number & avg ratings
num_rating_df = ratings_with_name.groupby("Book-Title").count()["Book-Rating"].reset_index()
num_rating_df.rename(columns={"Book-Rating": "num_ratings"}, inplace=True)

avg_rating_df = (
    ratings_with_name.groupby("Book-Title", as_index=False)["Book-Rating"]
    .mean()
    .rename(columns={"Book-Rating": "avg_rating"})
)

# Popular books
popular_df = num_rating_df.merge(avg_rating_df, on="Book-Title")
popular_df = popular_df[popular_df["num_ratings"] >= 250].sort_values("avg_rating", ascending=False).head(50)
popular_df = popular_df.merge(books, on="Book-Title").drop_duplicates("Book-Title")[
    ["Book-Title", "Book-Author", "Image-URL-M", "num_ratings", "avg_rating"]
]

# User filtering
x = ratings_with_name.groupby("User-ID").count()["Book-Rating"] > 200
valid_users = x[x].index
filtered_rating = ratings_with_name[ratings_with_name["User-ID"].isin(valid_users)]

y = filtered_rating.groupby("Book-Title").count()["Book-Rating"] >= 50
famous_books = y[y].index
final_ratings = filtered_rating[filtered_rating["Book-Title"].isin(famous_books)]

# Pivot table (sparse rating matrix)
pt = final_ratings.pivot_table(index="Book-Title", columns="User-ID", values="Book-Rating")
pt.fillna(0, inplace=True)

# Similarity matrix
similarity_scores = cosine_similarity(pt)

#Recommend
def recommend(book_name):
    if book_name not in pt.index:
        return [{"error": f"Book '{book_name}' not found"}]

    index = np.where(pt.index == book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        temp_df = books[books["Book-Title"] == pt.index[i[0]]].drop_duplicates("Book-Title")
        if not temp_df.empty:
            data.append({
                "title": temp_df["Book-Title"].values[0],
                "author": temp_df["Book-Author"].values[0],
                "image": temp_df["Image-URL-M"].values[0]
            })

    return data


def get_popular_books():
    return popular_df.to_dict(orient="records")
