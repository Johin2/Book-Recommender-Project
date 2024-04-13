from flask import Flask, render_template, request
import pickle
import pandas as pd

popular_df = pickle.load(open('popular.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_score = pickle.load(open('similarity_score.pkl', 'rb'))
pivot_table = pickle.load(open('pivot_table.pkl', 'rb'))


app = Flask(__name__)

@app.route('/')
def index():

    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           image = list(popular_df['Image-URL-M'].values),
                           author_name = list(popular_df['Book-Author'].values),
                           votes = list(popular_df['num_rating'].values),
                           rating = [round(value, 1) for value in list(popular_df['avg_rating'].values)],
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommended_books', methods= ['POST'])
def recommend():
    user_input = request.form.get('user-input')
    try:
        index = pivot_table.index.get_loc(user_input)
        similarity_row = similarity_score[index]
        similar_items = sorted(list(enumerate(similarity_row)), key = lambda x : x[1], reverse = True)[1:5]
        similar_books = [pivot_table.index[i[0]] for i in similar_items]
    except KeyError:
        return render_template('booknotfound.html')
    
    data = []
    for book in similar_books:
        item = []
        temp_df = books[books['Book-Title'] == book]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title']))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author']))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M']))
        data.append(item)
    
    return render_template('recommend.html', data = data)

if __name__ == '__main__':
    app.run(debug=True)
