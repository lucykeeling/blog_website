# Blog Website

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-black?logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-8.x-orange?logo=mysql&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?logo=bootstrap&logoColor=white)



## 🌟 Highlights

- User registration and login with hashed passwords via Flask-Bcrypt
- Write, read, and manage blog posts with a clean Bootstrap 5 UI
- Personalise your profile with a custom avatar (auto-resized on upload)
- Protected routes — only authenticated users can post or edit their account
- MySQL backend with raw SQL queries 


## ℹ️ Overview

The blog website is a full-stack blogging platform built with Flask and MySQL. Users can sign up, log in, and publish posts that are visible to everyone on the home feed. The project follows the application-factory pattern with Blueprints to keep the codebase modular and avoid circular imports. It was built as a learning project to explore Flask fundamentals: authentication, form validation, file uploads, session management, and database integration.  

It is based off the Corey Schafer Flask Tutorial (https://www.youtube.com/@coreyms), but built with MySQL instead of SQLAlechmy.

### ✍️ Authors

**Lucy Keeling** — [GitHub](https://github.com/lucykeeling)


## 🚀 Usage

Register an account, log in, and start posting:

1. Navigate to `/register` to create an account.
2. Log in at `/login`.
3. Go to **New Post** to publish your first entry.
4. Visit `/account` to update your username, email, or profile picture.


## ⬇️ Installation

**Prerequisites**

- Python 3.10+
- MySQL 8.x running locally
- A `blog` database with `user` and `post` tables (see schema below)

**1. Clone the repo and install dependencies**

```bash
git clone https://github.com/lucykeeling/blog_website.git
cd Flask_Blog
pip install flask flask-bootstrap5 flask-mysqldb flask-bcrypt flask-login flask-wtf pillow python-dotenv email-validator
```

**2. Create the MySQL database**

```sql
CREATE DATABASE blog;
USE blog;

CREATE TABLE user (
    user_id   INT AUTO_INCREMENT PRIMARY KEY,
    username  VARCHAR(20)  NOT NULL UNIQUE,
    email     VARCHAR(120) NOT NULL UNIQUE,
    password  VARCHAR(60)  NOT NULL,
    image_file VARCHAR(255) DEFAULT 'img/default.jpg'
);

CREATE TABLE post (
    post_id     INT AUTO_INCREMENT PRIMARY KEY,
    title       VARCHAR(100) NOT NULL,
    content     TEXT         NOT NULL,
    date_posted DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id     INT          NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);
```

**3. Configure environment variables**

Create a `.env` file in the project root:

```
DB_PASSWORD=your_mysql_root_password
```

**4. Run the app**

```bash
python run.py
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.


## 💭 Feedback and Contributing

Found a bug or have a feature request? Open an issue on the [GitHub Issues](https://github.com/lucykeeling/blog_website/issues) page.

Pull requests are welcome — feel free to fork the repo and submit a PR with your improvements.
