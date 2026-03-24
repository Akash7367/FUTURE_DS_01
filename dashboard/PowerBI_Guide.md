# Building the Power BI Dashboard (Online Retail Data)

Since you are using the `online_retail.csv` dataset, here is the updated step-by-step guide to building your Power BI dashboard.

## 1. Connect the Data
1. Open **Power BI Desktop**.
2. Click **Get Data** > **Text/CSV**.
3. Select `online_retail.csv` and click **Load**.
4. **Important**: Open **Transform Data** (Power Query Editor).
   - Ensure `InvoiceDate` is recognized as a Date/Time type.
   - Ensure `UnitPrice` and `Quantity` are numeric.
   - Filter out rows where `Quantity` < 0 (these represent returns and cancelled orders which might skew revenue, or keep them if you want to analyze returns separately).
   - **Crucial Step**: Add a Custom Column to calculate Sales/Revenue. Go to *Add Column* > *Custom Column*, name it `Sales`, and set the formula to `=[Quantity] * [UnitPrice]`.
   - Click *Close & Apply*.

## 2. Core Visualizations to Create

### Executive KPIs (Card Visuals)
Create **Card** visuals summing the following metrics:
- Total Revenue (Sum of `Sales`)
- Total Quantity Sold (Sum of `Quantity`)
- Unique Customers (Count Distinct of `CustomerID`)

### Sales Trend over Time (Line Chart)
- **X-axis**: `InvoiceDate` (Set to Month/Year hierarchy)
- **Y-axis**: Sum of `Sales`
- *Purpose*: Answers "How do sales change over time?".

### Top Selling Products (Bar Chart)
- **Y-axis**: `Description` (Product Name)
- **X-axis**: Sum of `Sales`
- *Purpose*: Answers "Which products generate the most revenue?". Filter to the Top 10 products using the Filters pane.

### Most Profitable Countries (Map or Column Chart)
- **Location/X-axis**: `Country`
- **Y-axis/Values**: Sum of `Sales`
- *Purpose*: Answers "Which regions/countries are most profitable?".

## 3. Formatting & Final Touches
- Add Slicers for **Country** and **InvoiceDate** (Year/Month) so the end-user can interactively filter the dashboard.
- Create a **Text Box** titled "Business Insights" where you summarize your findings. (e.g. "The United Kingdom accounts for the vast majority of revenue, and the 'White Hanging Heart T-Light Holder' is our absolute best-seller.")
