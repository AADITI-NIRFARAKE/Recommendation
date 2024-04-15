import pickle
import streamlit as st
import numpy as np

# Load model and data
book_names = pickle.load(open('artifacts/book_names.pkl','rb'))
pt = pickle.load(open('artifacts/pt.pkl','rb'))
similarity_scores = pickle.load(open('artifacts/similarity_scores.pkl','rb'))
books = pickle.load(open('artifacts/books.pkl','rb'))
popular_df = pickle.load(open('artifacts/popular.pkl','rb'))



# Function to recommend books
def recommend_book(book_name):
    index = np.where(pt.index == book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)
    return data    

# Welcome page
def welcome():
    st.title('Welcome to BookWise!')
    st.write("")
    st.write("")  

    num_columns = 3  # Number of columns to display
    num_books = len(popular_df)
    num_rows = (num_books + num_columns - 1) // num_columns  # Calculate number of rows based on number of books and columns

    for row in range(num_rows):
        cols = st.columns(num_columns)
        for col_idx in range(num_columns):
            book_idx = row * num_columns + col_idx
            if book_idx < num_books:
                with cols[col_idx]:
                    st.image(popular_df.iloc[book_idx]['Image-URL-M'], width=150)  # Book image
                    st.markdown(f"<h5>{popular_df.iloc[book_idx]['Book-Title']}</h5>", unsafe_allow_html=True)  # Book title
                    st.write(f"Author: {popular_df.iloc[book_idx]['Book-Author']}")  # Book author
                    st.write(f"Votes: {popular_df.iloc[book_idx]['num_ratings']}")  # Number of votes
                    st.write(f"Rating: {round(popular_df.iloc[book_idx]['avg_rating'],2)}")  # Average rating
                    st.write("")
                    st.write("")  

# Recommendation page
def recommendation():
    selected_books = st.selectbox(
        "Type or select a book from the dropdown",
        pt.index
    )

    if st.button('Show Recommendation'):
        #recommended_books,poster_url = recommend_book(selected_books)

        recommended_books = recommend_book(selected_books)
        num_columns = 4  # Number of columns to display
        num_books = len(recommended_books)
        num_rows = (num_books + num_columns - 1) // num_columns  # Calculate number of rows based on number of books and columns

        for row in range(num_rows):
            cols = st.columns(num_columns)
            for col_idx in range(num_columns):
                book_idx = row * num_columns + col_idx
                if book_idx < num_books:
                    with cols[col_idx]:
                        st.markdown(f"<h6>{recommended_books[book_idx][0]}</h6>", unsafe_allow_html=True)  # Book title
                        st.image(recommended_books[book_idx][2], width=150)  # Book image
                        st.write(f"Author: {recommended_books[book_idx][1]}")  # Book author
                        st.write("")
                        st.write("")  
                    # cols[col_idx].text(recommended_books[book_idx][0])  # Book title
                    # cols[col_idx].image(recommended_books[book_idx][2])
                    # cols[col_idx].text(recommended_books[book_idx][1])  # Book image URL

# App navigation
app_mode = st.sidebar.selectbox("Explore or Get Recommendations?",
["Popular Books", "Personalized Recommendations"])

if app_mode == "Popular Books":
    welcome()
elif app_mode == "Personalized Recommendations":
    recommendation()

