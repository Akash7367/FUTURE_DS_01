# Business Sales Performance Analytics

This repository contains the solution for the "Data Science & Analytics – Task 1 (2026)" by Future Interns.

## Project Overview
This project analyzes business sales data to uncover insights such as top-performing products, regional profitability, and sales trends over time. It includes generating realistic synthetic data, performing exploratory data analysis (EDA), and presenting the final insights in an interactive dashboard.

## Data Download Instructions
The dataset used in this project is the **Online Retail Dataset**. Due to its size, it is not included in this repository. 
You can download it from Kaggle:
[Online Retail Dataset on Kaggle](https://www.kaggle.com/datasets/ulrikthygepedersen/online-retail-dataset)

After downloading, please extract the `online_retail.csv` file and place it in the `data/` directory.

## Folder Structure
- `data/online_retail.csv`: The primary dataset for analysis (needs to be downloaded, see above).
- `EDA.ipynb`: Jupyter notebook containing data cleaning, exploration, and initial analysis (adapted for `online_retail.csv`).
- `PowerBI_Guide.md`: A step-by-step guide outlining how to build the required Power BI dashboard visuals using this dataset.

## How to Run The Project
1. **Download Data**: Follow the instructions above to download and place `online_retail.csv` in the `data/` directory.
2. **Explore Analysis**: Open `EDA.ipynb` in your preferred Jupyter environment to see trends from `online_retail.csv`.
2. **Open Dashboard**: Build or open your `.pbix` file in Microsoft Power BI Desktop to view the interactive visualizations.

## Tools & Tech Stack
- **Python**: Data generation, EDA, and preprocessing.
- **Power BI**: Interactive business dashboard and reporting.

## Key Insights & Recommendations
The primary insights, answering questions such as *Which products generate the most revenue?* and *Where should the business focus to grow faster?*, are thoroughly documented within the "Business Insights" tab of the interactive Streamlit dashboard.

## Exploratory Data Analysis Visualizations
Here are some of the key plots and graphs generated during the EDA phase:

### 1. Monthly Revenue & Estimated Profit Trend
This line chart visualizes the business's performance over time. It tracks both total monthly revenue (circles) and an estimated profit margin (squares) to help identify seasonal patterns and overall growth trends.
![Monthly Trend](images/plot_1.png)

### 2. Revenue Heatmap: Day of Week vs. Hour of Day
By mapping revenue generation across days and hours, this heatmap pinpoints peak shopping times. Darker areas indicate higher sales volume, allowing for optimized staff scheduling and targeted marketing campaigns.
![Revenue Heatmap](images/plot_2.png)

### 3. Order Value Distributions
A pair of histograms showing the distribution of customer spending habits.
- **Average Order Value**: Tracks the typical spend per item within an invoice.
- **Total Order Value**: Displays the overall shape of total invoice amounts across the customer base.
![Order Value Distribution](images/plot_3.png)

### 4. Impact of Returns and Cancellations
This pie chart breaks down the total revenue into completed (gained) revenue versus revenue lost due to returned or cancelled orders. It highlights the overall impact of product returns on the business bottom line.
![Returns Impact](images/plot_4.png)

### 5. Top 10 Countries by Estimated Profit
A bar chart highlighting the most profitable international markets. It lists the top 10 countries generating the highest estimated profit, which is crucial for guiding international expansion efforts.
![Top Profit Countries](images/plot_5.png)
