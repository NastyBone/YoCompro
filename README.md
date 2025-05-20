# Promo Radar

Promo Radar is a web application developed as a final project for the CS50 Harvard Introduction to Computer Science course by David Malan. The project aims to help users discover businesses, products, and discounts in their city, with features for searching, filtering, and managing business and product information.

#### Name

José Prieto

#### Project Name

Promo Radar / YoCompro

#### Username on Github / edX

NastyBone

#### City / Country

Maturín, Monagas, Venezuela.

#### Recording Date

2025-05-20

#### Video Demo

[Youtube](https://youtu.be/80H7VLUhbbI)

## About

This project was built as part of my journey through CS50. While the complexity and scope of Promo Radar go beyond the requirements of the course, it was a valuable learning experience. I encountered and learned from many design challenges, especially regarding planning, setting boundaries, and defining clear goals for the application. These lessons were as important as the technical skills gained.

## Features

- User authentication and profile management
- Business and product CRUD operations
- Search and filter businesses and products by tags, popularity, distance, and discounts
- Ratings and reviews for businesses and products
- Owner and admin dashboards
- Tag and image management
- Responsive UI with Tailwind CSS and Bootstrap

## Project Structure

```
.
├── app.py
├── database.db
├── schema.sql
├── helpers.py
├── guard.py
├── location.py
├── classes/
├── services/
├── routes/
├── static/
│   ├── css/
│   └── ...
├── templates/
│   └── ...
└── ...
```

- **app.py**: Main Flask application entry point
- **classes/**: Data models and business logic
- **services/**: Database and business logic services
- **routes/**: Flask route handlers
- **static/**: Static assets (CSS, JS, images)
- **templates/**: Jinja2 HTML templates

## Setup

1. **Clone the repository**
2. **Install dependencies**  
   This project uses Python 3 and Flask. Install dependencies with:
   ```sh
   pip install flask
   ```
3. **Initialize the database**  
   Run the schema in `schema.sql` to set up the database:
   ```sh
   sqlite3 database.db < schema.sql
   ```
4. **Run the application**
   ```sh
   flask run
   ```
5. **Access the app**  
   Open your browser at [http://localhost:5000](http://localhost:5000)

## Notes

- This project was a learning experience and may contain design flaws or areas for improvement.
- Planning and setting clear boundaries are crucial for managing complexity and avoiding delays.
- Most of the complexity here is beyond the CS50 course scope, but it was worth the effort.

## Acknowledgements

- [CS50: Introduction to Computer Science](https://cs50.harvard.edu/)
- David Malan and the CS50 team

---

I'm glad to have completed this project and grateful for the lessons learned along the way. Thanks!
