# rent-a-car-system
=====================

## Project Overview
---------------

This is a simple Rent-A-Car system built using Dart. The system allows users to rent cars, view available cars, and manage their bookings.

## Features
------------

*   User registration and login functionality
*   Car listing with details (make, model, year, price, etc.)
*   Booking and cancellation of cars
*   User profile management

## Tech Stack
-------------

*   **Language:** Dart
*   **Framework:** None (native Dart application)
*   **Database:** None (local storage used for simplicity)
*   **Dependencies:**
    *   `path_provider` for accessing local storage
    *   `shared_preferences` for storing user data

## Architecture
--------------

The application is structured as follows:

*   `main.dart`: The entry point of the application
*   `models`: Contains the data models for users and cars
*   `services`: Contains the services for user registration, login, and car booking
*   `screens`: Contains the screens for user registration, login, car listing, and user profile management

### Directory Structure
```markdown
rent-a-car-system/
README.md
main.dart
models/
user.dart
car.dart
services/
user_service.dart
car_service.dart
screens/
login_screen.dart
register_screen.dart
car_list_screen.dart
user_profile_screen.dart
```

### Getting Started
-------------------

To run the application, simply open `main.dart` in a Dart IDE and execute it. The application will start on the local machine.

### Contributing
--------------

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

### License
-------

This project is licensed under the MIT License. See the LICENSE file for details.