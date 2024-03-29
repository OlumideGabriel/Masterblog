from flask import Flask, render_template, request, redirect, url_for
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

            blog_posts = read_data()
            post_id = str(generate_random_id())  # Assigning post ID

            blog_posts.append({"id": post_id,  # Append new post to dictionary
                               "author": author,
                               "title": title,
                               "content": content,
                               "image": image_filename  # Add the image filename or path to the dictionary
                               })
            # Write updated data back to JSON file
            write_data(blog_posts)

        return redirect(url_for('index'))
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
        return redirect(url_for('index'))
    else:
        # If the request method is not POST, redirect to homepage
        return redirect(url_for('index'))


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

        # Write updated data back to JSON file
        write_data(blog_posts)
        # Redirect back to the homepage
        return redirect(url_for('index'))

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


# Route for handling 404 errors
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# Route for handling other errors (e.g., 500)
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(port=5000, debug=True)
