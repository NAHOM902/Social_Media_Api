# Social Media API

This project is a RESTful API for a social media platform designed to handle essential features such as user registration, login, posts, . It provides a secure and scalable backend using JWT token-based authentication.

![image alt](https://github.com/NAHOM902/Social_Media_Api/blob/main/nao.png?raw=true)

## 📌 Features

- **User Management ✔️**
   - Register a new user
   - Login with token authentication
   - Users list
   - users post list with specific id of the posts
- **Posts Management ✔️**
   - Create a new post
   - Retrieve all posts
   - Update a post
   - Delete a post

- **follow | unfolllow | following ✔️**
   - follow a user
   - Unfollow a user
   - List of following users

---

## 🟦 API Endpoints

### **User Endpoints ✔️**
- **Register a User:**  
  `POST /api/register/`  
- **Login User:**  
  `POST /api/login/`
- **users Specific post**
  `POST' /user/<int:user_id>/posts/`
- **Specific user with specific post**
  `POST' user/<int:user_id>/post/<int:post_id>/`

### **Post Endpoints ✔️**
- **Create a Post:**  
  `POST post/create/`  
- **Retrieve All Posts:**  
  `GET post/create/`
- **Update a specific Post:**  
  `PUT post/detail/<int:post_id>/`
- **Detail view of a Post:**  
  `GET post/detail/<int:post_id>/`
- **Delete a Post:**  
  `DELETE post/detail/<int:post_id>/`

### **follow Endpoints ✔️**
- **Follow a user:**
- `follow/<int:user_id>/`
- **Unfollow a user:**
- `unfollow/<int:user_id>/`
- **List of following:**
- `following/`


### **Likes Endpoints ✔️**
- **Like a Post:**  
  `POST /api/posts/{id}/like/`  
- **Unlike a Post:**  
  `POST /api/posts/{id}/unlike/`  
- **List Likes on a Post:**  
  `GET /api/posts/{id}/likes/`

---

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd <project_directory>

bash 
copy code
python -m venv venv
source venv/bin/activate   # on window use `venv/scripts/activate`
install Dependencies:


bash 
copy code
pip install -r requirements.txt
run Migrations:

bash 
copy code
python manage.py makemigrations
python manage.py migrate
run the server

bash 
copy code
python manage.py runserver
 
then test api end points `🟦 API Endpoints 👆`


✅ Technologies Used
Python
Django
Django REST Framework
Token-based Authentication
MySQL

**Contact**
For questions or Support, feel free to contact:

Name: Nahom Belayneh Abrah
Email: nahombelayneh387@gmail.com
