
# Web Servers Monitoring System 🌐🔍

## Description
The Web Servers Monitoring System is designed to enable real-time health monitoring of web servers in the cloud. Utilizing Flask and SQLAlchemy, this Python application provides a robust API for managing web server records and performing automated health checks based on HTTP response codes and latency.

## Project Architecture
This project follows a multi-layered architecture designed to separate concerns and promote code reusability and modularity:
- **API Layer** (`api.py`): Flask routes that handle HTTP requests and responses.
- **Service Layer** (`webserverServices.py`, `schedulerServices.py`): Business logic and service routines. `schedulerServices.py` acts as a worker class within the threading model.
- **Model Layer** (`models.py`): Database schema definitions using SQLAlchemy.
- **Scheduler Layer** (`scheduler.py`): Utilizes APScheduler for scheduling tasks and a custom thread pool (`threadpoolManager.py`) to enhance performance by concurrent execution of health checks.

### OOP Principles and Design
Object-Oriented Programming (OOP) principles such as encapsulation, inheritance, and polymorphism are extensively used to organize the code into logical, reusable components. Design patterns like Singleton (for database connections and scheduler management), Service Layer (for encapsulating business logic), and Worker-Manager (for thread management in health checks) are applied to ensure the system is scalable and maintainable.


## Capabilities 🚀
This system offers comprehensive functionalities for web server management and automated health monitoring, ensuring real-time oversight and maintenance. Here are the key capabilities:

**1. Add a New Webserver** 🌐<br>
Allows the creation of new web server records by specifying their name and HTTP URL. This is crucial for expanding the monitoring scope as new servers go live.

**2. List All Webservers** 📋<br>
Provides a complete listing of all registered webservers, including detailed information such as name, URL, and current health status. This feature is essential for administrative oversight and operational checks.

**3. Update Webserver Details** 🛠️<br>
Enables updates to webserver details, supporting changes in URL or names as server configurations evolve. This ensures that monitoring remains accurate and reflective of the current network topology.

**4. Delete a Webserver** ❌<br>
Facilitates the removal of webservers from monitoring when they are decommissioned or no longer needed. This helps in maintaining a clean and relevant list of active servers.

**5. Get Webserver Health and Request History** 📊<br>
Retrieves the health status and a history of the monitoring requests for individual servers. This is vital for diagnosing issues, understanding patterns, and making informed decisions about infrastructure health.

**6. Automated Health Checks** 🏥<br>
Conducts automated health checks at scheduled intervals, assessing each webserver against predefined success criteria related to response codes and latency. This automatic surveillance is crucial for proactive maintenance and ensures high availability.

These capabilities collectively provide a robust framework for real-time monitoring and management of web servers, enhancing system reliability and performance.


## Technologies Used
- **Python**: Primary programming language.
- **Flask**: Web framework for building the API.
- **SQLAlchemy**: ORM for database interactions.
- **MySQL**: Relational database management system.
- **APScheduler**: To schedule periodic health checks.
- **Requests**: To make HTTP requests to web servers.

## Database Normalization
The database is normalized to 3NF (Third Normal Form) to avoid data redundancies and maintain data integrity. This ensures that:
- All tables have a primary key.
- There are no repeating groups or arrays.
- All attributes are non-transitively dependent on the primary key in their respective tables.

## Setup and Installation

### Requirements
Python 3.8 or higher and pip should be installed on your system. You can install all dependencies via pip:
```bash
pip install -r requirements.txt
```

### Configuration
Update the `config.py` with the correct settings for your environment. Here is an example configuration:
```python
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/mydatabase'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```
Replace `username`, `password`, and `mydatabase` with your MySQL user, password, and database name.

### Running the Application
Navigate to the project directory and run the following command to start the Flask server:
```bash
python api.py
```

## API Usage
Refer to the included Postman collection (`Web_Servers_Monitoring_System.postman_collection.json`) to explore and test the API endpoints. This collection provides pre-configured requests for adding, retrieving, updating, and deleting web server records, as well as fetching their health statuses and request histories.

## License
This project is proprietary and confidential. Unauthorized copying of files, via any medium, is strictly prohibited.