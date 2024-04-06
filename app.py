from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import json
import uuid
import os

app = Flask(__name__)


# Helper function to read data from JSON file
def read_data():
    with open('storage.json', 'r') as file:
        return json.load(file)


# Helper Function to write data to JSON dil
def write_data(data):
    with open('storage.json', 'w') as file:
        json.dump(data, file, indent=4)


# Helper function to generate randon Unique ID
def generate_random_id():
    # Generate a random UUID (Universally Unique Identifier)
    random_id = uuid.uuid4()
    return random_id


# Helper function to search for posts by post_id
def fetch_post_by_id(post_id):
    blog_posts = read_data()
    for post in blog_posts:
        if post['id'] == post_id:
            return post


@app.route('/')
def index():
    blog_posts = read_data()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']

        # Check if an image was uploaded
        if 'image' in request.files:
            image_file = request.files['image']
            # Save the image to a folder (you may need to create a folder named "uploads" in your project directory)
            image_filename = os.path.join('static/uploads', image_file.filename)
            image_file.save(image_filename)

            image_file = os.path.join('uploads', image_file.filename)

            blog_posts = read_data()
            post_id = str(generate_random_id())  # Assigning post ID

            blog_posts.append({"id": post_id,  # Append new post to dictionary
                               "author": author,
                               "title": title,
                               "content": content,
                               "image": image_file,  # Add the image filename or path to the dictionary
                               "time-added": datetime.now().strftime("%B %d, %Y"),
                               "likes": 0
                               })
            # Write updated data back to JSON file
            write_data(blog_posts)

        return redirect(url_for('all_posts'))
    return render_template('add.html')


@app.route('/delete/<post_id>', methods=['GET', 'POST'])
def delete_post(post_id):
    if request.method == 'POST':
        blog_posts = read_data()
        # Remove the post from the list (or delete from database)
        for post in blog_posts:
            if post['id'] == post_id:
                blog_posts.remove(post)
                break
        # Write updated data back to JSON file
        write_data(blog_posts)
        # Redirect back to the homepage
        return redirect(url_for('all_posts'))
    else:
        # If the request method is not POST, redirect to homepage
        return redirect(url_for('all_posts'))


@app.route('/update/<post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the blog posts from the JSON file
    post = fetch_post_by_id(post_id)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        # Update the post in the JSON file
        blog_posts = read_data()
        for post in blog_posts:
            if post_id == post["id"]:
                post["author"] = request.form['author']
                post["title"] = request.form['title']
                post["content"] = request.form['content']

                # Check if an image was uploaded
                if 'image' in request.files:
                    image_file = request.files['image']
                    if image_file.filename != '':
                        # Save the uploaded image
                        image_filename = os.path.join('static/uploads', image_file.filename)
                        image_file.save(image_filename)
                        post['image'] = os.path.join('uploads', image_file.filename)

                    # Write updated data back to JSON file
                    write_data(blog_posts)
                    return redirect(url_for('all_posts'))

        # Redirect back to index
    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post)


@app.route('/post/<post_id>')
def blog_post(post_id):
    blog_posts = read_data()
    for post in blog_posts:
        if post_id == post['id']:
            return render_template('blog_post.html', post=post)
    # Return a message or handle the case when the post with the given ID is not found
    return redirect(url_for('page_not_found'))


@app.route('/like/<post_id>', methods=["POST"])
def post_likes(post_id):
    blog_posts = read_data()
    for post in blog_posts:
        if post_id == post['id']:
            if 'likes' not in post:
                post["likes"] = 1
            else:
                post["likes"] += 1

            # Write updated data back to JSON file
            write_data(blog_posts)
            return render_template('blog_post.html', post=post)
    # Redirect back to the homepage
    return redirect(url_for('index'))


@app.route('/new-category', methods=['GET', 'POST'])
def new_category():
    if request.method == 'POST':
        category = request.form['category']
        value = request.form['value']
        blog_posts = read_data()
        for post in blog_posts:
            if category not in post:
                post[category.lower()] = value
            else:
                return redirect(url_for('categories'))

        # Write updated data back to JSON file
        write_data(blog_posts)
        # Redirect back to the categories
        return redirect(url_for('categories'))
    # Redirect back to the homepage
    return render_template('category.html')


@app.route('/del/<category>', methods=['POST'])
def del_category(category):
    blog_posts = read_data()
    for post in blog_posts:
        if category in post:
            del post[category]

    # Write updated data back to JSON file
    write_data(blog_posts)

    # Redirect back to the categories
    return redirect(url_for('categories'))


@app.route('/categories', methods=['GET', 'POST'])
def categories():
    not_allowed = ['id', 'image']
    blog_posts = read_data()
    if request.method == 'POST':
        # Write updated data back to JSON file
        write_data(blog_posts)

    else:
        if isinstance(blog_posts, list) and all(isinstance(item, dict) for item in blog_posts):
            # Print keys of each dictionary
            for item in blog_posts:
                post_categories = (list(item.keys()))
                for category in not_allowed:
                    if category in post_categories:
                        post_categories.remove(category)
                    print(post_categories)
                return render_template('categories.html', categories=post_categories, posts=blog_posts)
        # Redirect back to the homepage
    return render_template('categories.html', posts=blog_posts)


@app.route('/posts')
def all_posts():
    blog_posts = read_data()
    return render_template('posts.html', posts=blog_posts)


# Route for handling 404 errors
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# Route for handling other errors (e.g., 500)
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500


# Route for handling other errors (e.g., 400)
@app.errorhandler(400)
def internal_server_error(error):
    return render_template('400.html'), 400


# Custom error handler for FileNotFoundError
@app.errorhandler(FileNotFoundError)
def handle_file_not_found_error(error):
    return render_template('405.html'), 405


if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)
