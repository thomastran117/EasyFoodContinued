# EasyFood

A hybrid service and e-commerce full stack application. It is a mixture between UberEats and OpenTable. Built with JavaScript and Python. The project follows best practice for software application design such as MVC, RESTful APIs and user validation.


## Authors

- [@thomastran117](https://www.github.com/thomastran117)


## EasyFood Features

- Authenication and Authorization System
- Email System
- Manage restaurants and foods
- Create a real-time order and place the order
- Reserve and book a restaurant for various occasions



## Tech Stack

**Client:** Vue, Pinia, JavaScript, TailwindCSS

**Server:** Python, FastAPI, SQLAlchemy, Alembic

**Database:** PostgreSQL


## Environment Variables

To run the project, you will need to add the following environment variables to in each directory .env file

Please refer to those README.md for more information

## Demo

Insert gif or link to demo

Deployed webite:


## Screenshots

![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)


## Requirements

To run the project locally, you will either need:

- Docker

or

- Python
- Node.js

Verify Docker is working with:

```bash
   docker --version
```

Verify Python and Node is working with:

Install EasyFood with npm

```bash
  python --version
  node --version
```

You are now ready to install and run the project
## Installation

### Clone the project

```bash
  git clone https://github.com/thomastran117/EasyFood.git
```

### Frontend

Install the frontend's dependencies with npm

```bash
  cd frontend
  npm install frontend
```

### Backend
Install the backend's dependencies with python. It is recommended to use a Virtual Environment to avoid package conflicts

```bash
  cd backend

  # Optional
  python -m venv <name>
  ./<name>/scripts/activate

  pip install -r requirements.txt
```

## Running the Application

### Running the frontend

```bash
  # If not already in frontend directory
  cd frontend

  npm run dev
```

The frontend is avaliable at http://localhost:3040
### Running the backend

The backend is avaliable at http://localhost:8040

```bash
  # If not already in backend directory
  cd backend

  # Optional: start the virtual environent
  ./<name>/scripts/activate
  
  python main.py
```
Remember to use the api prefix
### Docker (optional)

Using docker, run the following command in the root directory:
```bash
  docker-compose up --build
```
  
The frontend is avaliable at http://localhost:3040 and the backend is at http://localhost:8040. Remember to use the api prefix for the server.
## Running Tests

To run tests, run the following command

```bash
  npm run test
```
