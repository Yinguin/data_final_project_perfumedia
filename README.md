### Project Description
Build a recommendation system that helps users to find perfumes that correspond to their preferences.

**Details of the Data**
--------------------
Initially, I searched a lot for a dataset but could not find any that matched the features I wanted. So, the best option I found was to web-scrape a fragrance website and get the data. The website I chose for this is https://en.parfumdreams.de/Fragrances.

The data I scraped from this website include:
- Brand of the perfume
- Perfume name
- Category (EDT, EDP, Perfume, etc.)
• Gender
• Base price (price in Euro per 1000ml)
• Notes of the perfume
• Fragrance of the perfume
• Character of the perfume
• Customer ratings
• Review counts
• URL of the perfume
• Image of the perfume

**Design Flow**
These are the things I would like to perform to achieve results:
• Web scraping
• Data preprocessing
• EDA (Exploratory Data Analysis)
• More data exploration with SQL
• Data visualization (in Python and Tableau)
• Data processing - feature selection & extraction
• Data modeling & model evaluation
• Perfume APPs
• Steamlit project of perfume apps 

**Models**
For classifying the fragrance of perfumes, I experimented with three models to predict the class:
• **K-Nearest Neighbors (KNN)**
• **Random Forest**
• **Extreme Gradient Boosting (XGBoost)**
After evaluating these models, the Random Forest model exhibited the best performance. As a result, I opted for the **Random Forest model**, conducted hyperparameter tuning, and utilized it to predict the fragrances.

To discover similar perfumes based on a specific input perfume, I employed **cosine similarities** on the perfume notes to calculate the similarity scores with other perfumes.

**Summary**
• The recommendation system that I built targets users who fancy perfumes but struggle to decide what to wear.
• This is a content-based recommendation system.
• Perfume Finder by brand and name: A brand and name-based recommendation system that provides curated lists of perfumes matching specific brand and name preferences.
• Perfume Finder of similar perfumes: Utilizes cosine similarity to recommend perfumes similar to a user's favorite perfume based on perfume notes.
• Perfume Recommender: Allows users to input criteria like perfume category, gender, price range, fragrances, and notes to receive personalized top-rated perfume recommendations.
• The apps are deployed with Streamlit.

### Usage Instructions

The repository contains:
•	A folder (data) with the original datasets that I web scraped (perfume_basic.csv, perfume_data.csv, fragrance_links.csv) for the project and a dataset after cleaning and processing (perfume_final.csv) as well as a dataset for SQL (perfume_sql.csv).
•	A Jupyter notebook with the analysis and the models (data_final_project_perfumedia.ipynb).
•	An SQL-Query-File exploring the data (data_final_project_perfumedia.sql)
•	A Tableau Public workbook to visualize the data (data_final_project_perfumedia.twbx)
• A PowerPoint presentation of the project

I have created documentation of my workflow here: https://trello.com/b/nyboyGj5/fragrance

This project is part of the IRONHACK Data Analysis bootcamp from January to July 2023.

