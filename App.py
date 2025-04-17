from flask import Flask,render_template,request
import pickle
import numpy as np
App = Flask(__name__)

import pickle
num_avg_rating_df = pickle.load(open('num_avg_rating_df_exported.pkl', 'rb'))
pivot_table = pickle.load(open('pivot_table.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))


@App.route('/')
def index():
    return render_template('index.html',
                           book_title=list(num_avg_rating_df['Book-Title'].values),
                           author_name=list(num_avg_rating_df['Book-Author'].values),
                           book_image_url=list(num_avg_rating_df['Image-URL-M'].values),
                           total_votes=list(num_avg_rating_df['number_of_total_ratings'].values)
                           )

@App.route('/recommend_part')
def recommend_part_ui():
    return render_template('recommend_part.html')

@App.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    indexes = np.where(pivot_table.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[indexes])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pivot_table.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)
    print(data)

    return render_template('recommend_part.html',data=data)


if __name__ == '__main__':
    App.run(debug=True)

