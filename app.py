from flask import Flask, request, render_template, redirect, url_for, jsonify
import json

app = Flask(__name__)


def load_blog_posts():
    """
    Load blog posts from the JSON file.

    Returns:
        list: A list of blog posts.
    """
    with open('blog.json', 'r', encoding="utf-8") as file:
        return json.load(file)


def save_blog_posts(posts):
    """
    Save blog posts to the JSON file.

    Args:
        posts (list): A list of blog posts to be saved.
    """
    with open('blog.json', 'w', encoding="utf-8") as file:
        json.dump(posts, file, indent=4)


@app.route('/')
def index():
    """
    Render the home page with a list of blog posts.

    Returns:
        str: Rendered HTML template for the index page.
    """
    blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Handle adding a new blog post. If the request method is POST,
    save the new post to the JSON file and redirect to the index page.
    If GET, render the form for adding a new post.

    Returns:
        str: Rendered HTML template for adding a post or redirect to the index page.
    """
    blog_posts = load_blog_posts()

    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        # Generate a new ID
        new_id = (max(post['id'] for post in blog_posts) + 1
                  if blog_posts else 1)

        # Create a new blog post
        new_post = {
            'id': new_id,
            'author': author,
            'title': title,
            'content': content
        }

        # Append to the list and save
        blog_posts.append(new_post)
        save_blog_posts(blog_posts)
        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/like/<int:post_id>')
def like(post_id):
    """
    Handle the liking of a blog post by incrementing its like count.
    Reload the blog posts, update the like count, save, and redirect.

    Args:
        post_id (int): The ID of the blog post to be liked.

    Returns:
        str: Redirect to the index page.
    """
    blog_posts = load_blog_posts()
    post = next((post for post in blog_posts if post['id'] == post_id), None)

    if 'likes' not in post:
        post['likes'] = 0  # Initialize likes if missing

    post['likes'] += 1  # Increment the likes
    save_blog_posts(blog_posts)  # Save updated blog posts

    return redirect(url_for('index'))


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """
    Handle the deletion of a blog post. Reload blog posts, remove the
    specified post, save the remaining posts, and redirect.

    Args:
        post_id (int): The ID of the blog post to be deleted.

    Returns:
        str: Redirect to the index page.
    """
    blog_posts = load_blog_posts()
    blog_posts = [post for post in blog_posts if post['id'] != post_id]
    save_blog_posts(blog_posts)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Handle updating a blog post. If the request method is POST, update
    the post data and save it. If GET, render the form with current data.

    Args:
        post_id (int): The ID of the blog post to be updated.

    Returns:
        str: Rendered HTML template for updating the post or redirect to the index page.
    """
    blog_posts = load_blog_posts()
    post = next((post for post in blog_posts if post['id'] == post_id), None)

    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')

        save_blog_posts(blog_posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


@app.route('/api/books', methods=['GET', 'POST'])
def books():
    """
    Handle GET and POST requests for books. GET returns a static list
    of books. POST returns the data sent by the user.

    Returns:
        Response: JSON response with books or newly added book.
    """
    if request.method == 'GET':
        books = [
            {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
            {"id": 2, "title": "1984", "author": "George Orwell"}
        ]
        return jsonify(books)

    elif request.method == 'POST':
        new_book = request.get_json()
        return jsonify(new_book), 201


if __name__ == "__main__":
    app.run(debug=True)