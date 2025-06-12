from langchain.tools import tool
import sqlite3

import os
import requests

db_url = "https://www.dropbox.com/scl/fi/1ikhm2muo220tmhlt1tk4/movies.db?rlkey=tr7lo6dhh316qnstog5uzl528&st=spv9frtn&dl=1"
db_path = "movies.db"

def download_db():
    if not os.path.exists(db_path):
        print("Downloading movies.db from Dropbox...")
        response = requests.get(db_url)
        with open(db_path, "wb") as f:
            f.write(response.content)
        print("Download complete.")
    else:
        print("movies.db already exists, skipping download.")

download_db()


@tool
def search_movies_by_genre(genre: str) -> list:
    """Search movies by genre. Returns titles and release years."""
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT title, release_date 
        FROM movies 
        WHERE genres LIKE ? 
        ORDER BY vote_average DESC
    """, (f"%{genre}%",))
    results = cursor.fetchall()
    conn.close()
    return [f"{title} ({year[:4]})" for title, year in results]

@tool
def get_movie_details(title: str) -> dict:
    """Fetch full details of a movie by title."""
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies WHERE title = ?", (title,))
    movie = cursor.fetchone()
    conn.close()
    if not movie:
        return {"error": "Movie not found"}
    # Convert to dict with column names (adjust based on your schema)
    columns = ["adult", "backdrop_path", ..., "vote_count"]  # Add all your columns
    return dict(zip(columns, movie))

@tool
def analyze_movies(question: str) -> str:
    """Answer analytical questions about movies (e.g., budgets, ratings)."""
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    
    if "highest budget" in question:
        cursor.execute("SELECT title, budget FROM movies ORDER BY budget DESC LIMIT 1")
        result = cursor.fetchone()
        return f"Highest budget movie: {result[0]} (${result[1]:,})"
    
    elif "best rated" in question:
        cursor.execute("SELECT title, vote_average FROM movies ORDER BY vote_average DESC LIMIT 1")
        result = cursor.fetchone()
        return f"Best rated movie: {result[0]} ({result[1]}/10)"
    
    conn.close()
    return "Question not supported."