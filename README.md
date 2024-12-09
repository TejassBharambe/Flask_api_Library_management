# Flask_api_Library_management



## Overview

This is a RESTful API for a **Library Management System** built using Flask. The API allows users to manage books and members through various CRUD operations. Additionally, the system includes features like **search functionality** for books, **pagination** for listing resources, and **token-based authentication** to ensure secure access.

## Features

### 1. **Book Management (CRUD Operations)**
   - **Create**: Add a new book to the library.
   - **Read**: Retrieve details of a book or list of books.
   - **Update**: Modify details of an existing book.
   - **Delete**: Remove a book from the library.

### 2. **Member Management (CRUD Operations)**
   - **Create**: Register a new member.
   - **Read**: Retrieve details of a member or list of members.
   - **Update**: Modify member details.
   - **Delete**: Remove a member from the system.

### 3. **Search Functionality for Books**
   - Users can search books by **title** and/or **author** via query parameters.
   - This enables users to quickly find books in a large collection.

### 4. **Pagination**
   - Book and member lists are paginated for efficient data retrieval.
   - Parameters like `page` and `per_page` can be used to control the number of records returned.

### 5. **Token-based Authentication**
   - Token authentication is required for all CRUD operations.
   - Users must log in to get an authentication token, which is then used in the request headers to access protected resources.

## How to Run the Project

### 1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/library-management-system.git
   cd library-management-system
   python3 -m venv venv
   source venv/bin/activate  # For macOS/Linux
   venv\Scripts\activate     # For Windows

   pip install -r requirements.txt
```
### 2. ** run the following command **

```bash
python app.py
python -m unittest test.py # run in another terminal
```


# Assumptions and Limitations

## In-memory Database
- **Data Loss**: The application utilizes an in-memory database, which means that all data is lost when the server is restarted. This limitation affects the persistence of user data and application state.

## Authentication
- **Hardcoded Credentials**: The login credentials for the application are hardcoded. This approach poses a security risk and limits flexibility.
- **Non-persistent Authentication**: Authentication does not persist after the server restarts, requiring users to log in again each time the server is restarted.

## Data Validation
- **Lack of Advanced Validation**: The application does not perform detailed validation of user inputs. For example:
  - Email addresses are not validated for proper format.
  - There is no mechanism to ensure that book titles are unique within the database.


# Tests Include

## Login
- **Purpose**: Ensures that the login process returns a valid token upon successful authentication.

## CRUD Operations
- **Purpose**: Verifies that the following operations work as expected:
  - **Add**: Confirms that new books and members can be added to the database.
  - **Update**: Checks that existing books and members can be updated correctly.
  - **Get**: Validates that books and members can be retrieved from the database.
  - **Delete**: Ensures that books and members can be deleted from the database.

## Search
- **Purpose**: Tests the search functionality for books by title, ensuring that relevant results are returned based on user input.


# Design Choices

## In-memory Database
- **Description**: For simplicity, the application uses in-memory lists (books and members) as databases. This approach allows for fast prototyping and development but does not provide data persistence across server restarts.

## Token-based Authentication
- **Description**: To secure the API, all CRUD operations are protected with token-based authentication. A token is generated upon successful login and must be included in the header of requests to access protected resources.

## Search and Pagination
- **Description**: To handle large amounts of data efficiently, both search and pagination features are implemented:
  - **Search**: Allows filtering of books by title and/or author.
  - **Pagination**: Splits large datasets into smaller, manageable chunks to prevent overwhelming the client and improve performance.

