from flask import Flask, request, render_template, redirect, url_for
import json

app = Flask(__name__)


# Load blog posts from JSON file
def load_blog_posts():
    with open('blog.json', 'r') as file:
        return json.load(file)


# Save blog posts to JSON file
def save_blog_posts(blog_posts):
    with open('blog.json', 'w') as file:
        json.dump(blog_posts, file, indent=4)


# Global variable for blog posts
blog_posts = load_blog_posts()


@app.route('/')
def index():
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')
        # Generate a new ID
        new_id = max(post['id'] for post in blog_posts) + 1 if blog_posts else 1

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
    blog_posts = load_blog_posts()
    post = next((post for post in blog_posts if post['id'] == post_id), None)
    if 'likes' not in post:
        post['likes']=0  # Initialize likes if missing
    post['likes']+=1  # Increment the likes
    save_blog_posts(blog_posts)  # Save updated blog posts
    return redirect(url_for('index'))  # Redirect to refresh the page


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    blog_posts = load_blog_posts()
    # Find the blog post with the given ID
    post = next((post for post in blog_posts if post['id'] == post_id), None)

    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        # Get updated data from the form
        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')
        # Save the updated list to JSON file
        save_blog_posts(blog_posts)
        # Redirect back to the home page
        return redirect(url_for('index'))
    # If GET request, show the form with current data
    return render_template('update.html', post=post)


@app.route('/delete/<int:post_id>')
def delete(post_id):
    global blog_posts
    blog_posts = [post for post in blog_posts if post['id'] != post_id]
    save_blog_posts(blog_posts)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
