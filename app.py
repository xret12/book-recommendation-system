import pickle
import streamlit as st
import numpy as np


## INITIALIZE VARIABLES
MODEL = pickle.load(open('artifacts/model.pkl', 'rb'))
FINAL_RATING = pickle.load(open('artifacts/final_rating.pkl', 'rb'))
BOOK_PIVOT = pickle.load(open('artifacts/book_pivot.pkl', 'rb'))
book_names = BOOK_PIVOT.index


def recommend_books(selected_book):
    _, suggestions = MODEL.kneighbors(BOOK_PIVOT.loc[selected_book].values.reshape(1,-1), n_neighbors=6)
    suggestion_indexes = suggestions.flatten()
    # get recommended book titles
    books_list = [BOOK_PIVOT.index[sugg_idx] for sugg_idx in suggestion_indexes]

    # get corresponding poster image
    poster_urls = [FINAL_RATING[['title', 'img_url']].loc[FINAL_RATING['title'] == book].values[0][1] for book in books_list]
    return books_list, poster_urls



st.header('Book Recommendation System using Collaborative Filtering Algorithm')
selected_book = st.selectbox("Type or select a book", book_names)

if st.button('Show Recommendations'):
    recommendation_books, poster_url = recommend_books(selected_book)    

    for idx, col in enumerate(st.columns(5)):
        with col:
            st.text(recommendation_books[idx+1])
            st.image(poster_url[idx+1])
