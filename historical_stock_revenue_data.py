import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


#1
def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()

# Using the `Ticker` function enter the ticker symbol of the stock we want to extract 
# data on to create a ticker object. The stock is Tesla and its ticker symbol is `TSLA`.
ticker_obj = yf.Ticker('TSLA')
# print(ticker_obj.history(period="max"))

tesla_data = ticker_obj.history(period="max")
# print(typetesla_data))

# Ensure datetime index is timezone unawaretesla_data
#.index = tesla_data
#.index.tz_localize(None)

# with pd.ExcelWriter('tesla_stock_max_per.xlsx') as writer:
#     tesla_data.to_excel(writer, sheet_name='TSLA Data')
tesla_data.reset_index(inplace=True)
tesla_data.head()

# print(tesla_data.head())

#2
url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm'
response = requests.get(url)
html_data = response.text

beautiful_soup = BeautifulSoup(html_data, 'html.parser')


tesla_quarterly_revenue_table = pd.DataFrame(columns=["Date", "Revenue"])
# print(tesla_quarterly_revenue_table)

# pd_read_html  = pd.read_html(html_data)

# tesla_quarterly_revenue_table = pd_read_html[1]
# print(type(tesla_quarterly_revenue_table))

# all_a = beautiful_soup.find_all("tbody")[1]
# print(all_a)

# Find all tables and select the relevant one
tables = beautiful_soup.find_all('table')

# Check for Tesla Quarterly Revenue Table by inspecting the text
for table in tables:
    if "Tesla Quarterly Revenue" in str(table):
        tesla_table = table
        break

data = []

# Find all rows in the table body
for row in tesla_table.find('tbody').find_all('tr'):
    cols = row.find_all('td')
    date = cols[0].text.strip()  # First column for Date
    revenue = cols[1].text.strip()  # Second column for Revenue
    data.append({"Date": date, "Revenue": revenue})

# Create DataFrame from the list
    tesla_revenue = pd.DataFrame(data)
    # print(tesla_revenue)

# Clean Revenue column
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].replace(',|\$',"", regex=True)
# print(tesla_revenue)

# Remove an null or empty strings in the Revenue column.
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

last_five_rows = tesla_revenue.tail()
# print(last_five_rows)


game_stop_obj = yf.Ticker('GME')
# game_stop_obj

gme_data = game_stop_obj.history(period="max")
# gme_data

#Reset the index using the reset_index(inplace=True) function on the gme_data DataFrame 
# and display the first five rows of the gme_data dataframe using the head function. 
# Take a screenshot of the results and code from the beginning of Question 3 to the results below.

gme_data.reset_index(inplace=True)
gme_data.head()


url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html'
requesr_url = requests.get(url)
html_data_2 = requesr_url.text
# html_data_2

#Parse the html data using beautiful_soup using parser i.e html5lib or html.parser.
beautiful_soup_gme = BeautifulSoup(html_data_2, 'html.parser')
# beautiful_soup

#Using BeautifulSoup or the read_html function extract the table with GameStop Revenue 
# and store it into a dataframe named gme_revenue. 
# The dataframe should have columns Date and Revenue. 
# Make sure the comma and dollar sign is removed from the Revenue column.

tables_gme = beautiful_soup_gme.find_all('table')

for table in tables_gme:
    if 'GameStop Revenue' in str(tables_gme):
        gme_table = table
        break

data_gme = []

# Find all rows in the table body
for row in gme_table.find('tbody').find_all('tr'):
    cols = row.find_all('td')
    date = cols[0].text.strip()  # First column for Date
    revenue = cols[1].text.strip()  # Second column for Revenue
    data_gme.append({"Date": date, "Revenue": revenue})

gme_revenue = pd.DataFrame(data_gme)

print(gme_revenue)

# Clean Revenue column
gme_revenue["Revenue"] = gme_revenue['Revenue'].replace(',|\$',"", regex=True)
# print(gme_revenue)

# Remove an null or empty strings in the Revenue column.
gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]

last_five_rows = gme_revenue.tail()
print(last_five_rows)

make_graph(tesla_data, tesla_revenue, 'Tesla')
# make_graph(gme_data, gme_revenue, 'GameStop')