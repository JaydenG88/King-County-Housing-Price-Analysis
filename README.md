# King County Housing Price Analysis

This project is a full-stack application that analyzes and visualizes real estate market data for single-family homes in King County, Washington.
It utilizes a weekly automated web-scraping ETL pipeline built with Python that stores housing data in a MongoDB database.
A Flask application is used to create a RESTful API for the backend, and a Next.js frontend data dashboard is built for data visualization and user interaction.

## Check it out!
You can see my data dashboard [Here](https://king-county-housing-price-analysis-fxrigb9yi.vercel.app/) (Charts may take a minute to load if the Render instance is asleep)
<img width="1907" height="908" alt="image" src="https://github.com/user-attachments/assets/33bfe152-1180-49d7-88a5-a44788f70dd5" />

## Features
- __Weekly web-scraping ETL pipeline__ automated on GitHub Actions utilizing Selenium and BeautifulSoup4 for web-scraping Redfin listings, Pandas and Numpy for data cleaning and analysis, stored and transferred in a MongoDB database.
- __Backend RESTful API__  hosted on Render, built with Flask to send analysis data to the frontend application.
- **Interactive frontend dashboard** built with Next.js and hosted on Vercel. Includes:
  - Averages bar chart across King County cities
  - Time-series chart for regional price trends
  - Correlation heatmap for numerical variables
  - Price quartile histogram
  - Best-valued listings page by region
## Tech Stack
- __Frontend:__ Next.js (JavaScript), Recharts, Apexcharts
- __Backend:__ Flask (Python), REST API
- __Database:__ MongoDB (PyMongo)
- __ETL pipeline:__
  - Web-scraping: Selenium, Selenium Stealth, BeautifulSoup4 (Python)
  - Data Cleaning and Analysis: Pandas, Numpy (Python)
- __Automation:__ GitHub Actions (CRON schedule)
- __Deployment:__ Render (Backend), Vercel (Frontend)

