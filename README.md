## Pure_Aroma Fragrance Website 
Welcome to Pure_Aroma! This is an e-commerce platform designed to bring a personalized fragrance experience to users. Built with a modern tech stack, including FastAPI, PostgreSQL, and a simple frontend using HTML and CSS, Pure_Aroma allows users to browse and purchase premium fragrances with ease and security.

### Table of Contents
1) Project Overview
2) Tech Stack
3) Features
4) Installation
5) Usage
6) Contribution

### Project Overview
Pure_Aroma is an online fragrance store where users can:
1) Browse a wide selection of high-quality perfumes.
2) Create and manage accounts with secure login and password hashing.
3) View detailed product descriptions and images.
4) The platform uses FastAPI for making Api's , PostgreSQL for the database, and a simple HTML/CSS frontend. The backend ensures fast API responses, secure user data handling, and efficient database management.

### Tech Stack
**Frontend**: HTML, CSS

**Backend**: FastAPI

**Database**: PostgreSQL

### Features
**User Authentication**: Users can sign up, log in, and manage their accounts. Passwords are securely hashed using bcrypt to ensure user security.

**Fragrance Catalog**: Users can browse a collection of fragrances that are fetched dynamically from the database.

**Product Detail Page**: Each product has its own detail page with descriptions, images, and pricing.
Secure Checkout: Fast and secure processing of user data for purchases.

### Installation
1) Clone the repository: git clone https://github.com/Ahsan-ij/Pure_Aroma_fast_Api_website.git

2) cd Pure_Aroma

#### Set up Virtual Enivornment
1) python3 -m venv venv
2) venv\Scripts\activate 

#### Install the required dependencies
pip install -r requirements.txt


### Api Endpoints
**GET /products:** 
Retrieve the list of available fragrances.

**POST /signup:** 
Create a new user account.

**POST /login:**
User login with password authentication.

**GET /product/{id}**: 
Retrieve details for a specific fragrance.

**POST /purchase:**
Make a purchase (currently simulated).

### License
This project is licensed under the MIT License.