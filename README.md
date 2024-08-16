# Masterblog

Masterblog is a blogging platform built with Flask. It allows users to create, view, update, and delete blog posts, manage categories, and like posts. This project utilizes JSON for data storage and Bootstrap for styling.

## Features

- **Dashboard**: Navigate through the blog using a sidebar.
- **Posts Management**: Create, view, update, and delete blog posts.
- **Categories Management**: Add, update, and delete categories for blog posts.
- **Like Posts**: Users can like individual posts.
- **Responsive Design**: Built with Bootstrap for a modern, responsive layout.
- **Error Handling**: Custom error pages for 404, 500, 400, and FileNotFoundError.

## Requirements

- Python 3.7 or higher
- Flask
- Jinja2 (Flask's template engine)
- Bootstrap (for frontend styling)


## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/masterblog.git
   cd masterblog
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

4. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application:**

   ```bash
   flask run
   ```
  
6. **Run the application:**

   navigate to `http://127.0.0.1:5000/` to view the application

## Usage

### Routes

- **`/`** - Home page displaying all blog posts.
- **`/add`** - Form to create a new post.
- **`/delete/<post_id>`** - Endpoint to delete a post.
- **`/update/<post_id>`** - Form to update an existing post.
- **`/post/<post_id>`** - View a single post.
- **`/like/<post_id>`** - Endpoint to like a post.
- **`/new-category`** - Form to add a new category.
- **`/del/<category>`** - Endpoint to delete a category.
- **`/update/<category>`** - Form to update a category.
- **`/categories`** - View and manage categories.
- **`/posts`** - List of all posts.

### Error Handling

- **404 Error** - Page not found.
- **500 Error** - Internal server error.
- **400 Error** - Bad request.
- **405 Error** - Method not allowed.

## Configuration

- **`storage.json`**: This file stores all blog posts and categories. Ensure it is present in the project directory.
- **Uploads**: Images are saved in the `static/uploads` directory. Make sure this directory exists.

## Contributing

If you would like to contribute to the project, please fork the repository and submit a pull request with your changes. Ensure that your code follows the existing style and includes appropriate tests.


## Acknowledgments

- **Flask:** A micro web framework for Python.
- **Bootstrap:** Frontend framework for building responsive, mobile-first sites.
- **Jinja2:** A template engine for Python, used by Flask.

## Contact

If you have any questions or suggestions, feel free to open an issue on the GitHub repository or contact me at [your-email@example.com].

```

### Key Customizations:

1. **Features Section**: Updated to reflect the functionalities provided by the `app.py` file, including like functionality and custom error handling.
2. **Routes Section**: Detailed the different routes and their purposes.
3. **Configuration Section**: Noted the importance of the `storage.json` file and the uploads directory.
4. **Dependencies**: Listed Flask as the main dependency. You might want to include `requirements.txt` if you have additional dependencies.

Feel free to modify any section further based on your project's specifics or if you have additional features or configuration details!