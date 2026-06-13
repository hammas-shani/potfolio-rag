# Chatbot-real-state
======================

## Project Overview
-------------------

This repository contains the implementation of a real estate chatbot using Python and various machine learning libraries. The chatbot is designed to assist users in finding properties in Karachi, Pakistan, based on their preferences and requirements.

## Features
------------

*   **Property Search**: The chatbot allows users to search for properties based on location, price range, and property type.
*   **Property Recommendation**: The chatbot recommends properties to users based on their preferences and search history.
*   **Property Details**: The chatbot provides detailed information about properties, including location, price, and amenities.

## Tech Stack
--------------

*   **Programming Language**: Python 3.9
*   **Machine Learning Library**: scikit-learn
*   **Natural Language Processing Library**: NLTK
*   **Database**: Pandas DataFrame (in-memory database)
*   **API**: Flask

## Architecture
--------------

The chatbot architecture is designed to be modular and scalable. The following components make up the architecture:

*   **Data Ingestion**: The `zmeenkarachi.csv` file contains real estate data for Karachi, which is loaded into a Pandas DataFrame.
*   **Data Preprocessing**: The data is preprocessed using scikit-learn libraries to handle missing values, outliers, and categorical variables.
*   **Model Training**: A machine learning model is trained on the preprocessed data to predict property recommendations.
*   **Chatbot Logic**: The `app.py` file contains the chatbot logic, which uses the trained model to provide property recommendations to users.
*   **API**: The Flask API is used to expose the chatbot logic to users.

## Requirements
--------------

The following requirements are needed to run the chatbot:

*   Python 3.9
*   scikit-learn
*   NLTK
*   Pandas
*   Flask

The requirements can be installed using the following command:

```bash
pip install -r req.txt
```

## Running the Chatbot
-----------------------

To run the chatbot, execute the following command:

```bash
python app.py
```

This will start the Flask API, and the chatbot will be available at `http://localhost:5000`.