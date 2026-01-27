Project Overview

This project focuses on collecting laptop data from Flipkart, cleaning and analyzing the dataset, and building machine learning models to predict laptop prices and cluster similar laptops. The goal is to demonstrate end-to-end data analytics and machine learning workflow, including web scraping, data preprocessing, exploratory data analysis, and model building.
mlproject/
│
├── flipkart_scraper.py              # Web scraping script

├── 1_Webscraping.ipynb              # Web scraping notebook

├── 2_Data_cleaning.ipynb            # Data cleaning & preprocessing

├── 4_Unsupervised_Learning.ipynb    # Clustering models

├── laptops.csv                      # Raw dataset

├── flipkart_laptops_full.csv        # Scraped dataset

├── flipkart_laptops_cleaned.csv     # Cleaned dataset

├── laptops_final_dataset.csv        # Final dataset for ML

├── flipkart_laptops_clustered.csv   # Clustered output

├── project_summary.csv              # Project summary file

├── Capstone Project - DS.pdf         # Detailed project report

└── README.md                         # Project documentation




Web Scraping

Scraped laptop data (name, price, rating, specs) from Flipkart using Python and BeautifulSoup.

✅ Data Cleaning & Preprocessing

Removed missing values and duplicates

Converted prices and ratings into numeric format

Feature engineering for machine learning

✅ Exploratory Data Analysis (EDA)

Analyzed laptop price distribution

Compared brands, ratings, and specifications

Visualized insights using Python libraries

✅ Machine Learning

Supervised Learning: Laptop price prediction model

Unsupervised Learning: Laptop clustering using K-Means

Model evaluation and performance analysis
