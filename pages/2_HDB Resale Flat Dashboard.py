import streamlit as st
import pandas as pd
from decimal import Decimal
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px




df = pd.read_csv('./data/ResaleflatpricesbasedonregistrationdatefromJan2017onwards.csv')
df["address"] = df["block"] + " " + df["street_name"]
df["year"] = df['month'].str[:4]
df["date"] = pd.to_datetime(df['month'])
df["date_year"] = pd.to_datetime(df['month'].str[:4])

st.set_page_config(
    page_title="HDB Resale Price Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
    )


if 'df' not in st.session_state:
    st.session_state.df = df

# Unique towns and years
towns = sorted(st.session_state.df["town"].unique().tolist())

year = sorted(st.session_state.df["year"].unique().tolist(), reverse=True)

# Sidebar for filtering dashboard
with st.sidebar:
    st.header("Filter options")
    town_option = st.selectbox(label="Select Town", options=towns)
    year_option = st.selectbox(label="Select Year", options=year)


# Calculate the
# Filter the DataFrame for the selected town and year
filtered_data_current = df[(df['town'] == town_option) & (df['year'] == year_option)]
# Calculate the metric for the selected town and year
max_price_current = filtered_data_current['resale_price'].max() if not filtered_data_current.empty else None
min_price_current = filtered_data_current['resale_price'].min() if not filtered_data_current.empty else None
total_num_transactions = filtered_data_current["town"].count() if not filtered_data_current.empty else None

previous_year = str(int(year_option) - 1)

# Filter the DataFrame for the selected town and previous year
filtered_data_previous = df[(df['town'] == town_option) & (df['year'] == previous_year)]

def get_delta(var, type):
    if year_option != year[-1]:
        if type == "count":
            delta = (filtered_data_current[var].count() - filtered_data_previous[var].count())
        elif type == "sum":
            delta = (filtered_data_current[var].sum() - filtered_data_previous[var].sum())
        elif type == "min":
            delta = (filtered_data_current[var].min() - filtered_data_previous[var].min())
        elif type == "max":
            delta = (filtered_data_current[var].max() - filtered_data_previous[var].max())
        elif type == "median":
            delta = (filtered_data_current[var].median() - filtered_data_previous[var].median())
        return f"{numerize(delta)} vs {previous_year}"
    return None

def round_num(n, decimals):
    return n.to_integral() if n == n.to_integral() else round(n.normalize(), decimals)


def drop_zero(n):
    n = str(n)
    return n.rstrip("0").rstrip(".") if "." in n else n

def numerize(n, decimals=2):
    """
    Adapted from numerize (https://github.com/davidsa03/numerize) to handle numbers over 1 million only
    """
    is_negative_string = ""
    if n < 0:
        is_negative_string = "-"
    try:
        n = abs(Decimal(n))
    except:
        n = abs(Decimal(n.item()))
    if n >= 1000000 and n < 1000000000:
        if n % 1000000 == 0:
            return is_negative_string + str(int(n / 1000000)) + "M"
        else:
            n = n / 1000000
            return is_negative_string + str(drop_zero(round_num(n, decimals))) + "M"
    elif n >= 1000000000 and n < 1000000000000:
        if n % 1000000000 == 0:
            return is_negative_string + str(int(n / 1000000000)) + "B"
        else:
            n = n / 1000000000
            return is_negative_string + str(drop_zero(round_num(n, decimals))) + "B"
    elif n >= 1000000000000 and n < 1000000000000000:
        if n % 1000000000000 == 0:
            return is_negative_string + str(int(n / 1000000000000)) + "T"
        else:
            n = n / 1000000000000
            return is_negative_string + str(drop_zero(round_num(n, decimals))) + "T"
    else:
        return is_negative_string + f"{n:,}"

with st.container():
    st.title("Singapore HDB Resale Price since 2017")
    st.info("Use the Filter Options in the side bar.")


with st.container():
    st.markdown(f"## Transactions in {town_option} for Year {year_option}")
    st.markdown("### Key Metrics")
    # Display current year metric
    met1, met2 ,met3 = st.columns(3)
    met1.metric(
            label="Highest Resale Price",
            value=f"${max_price_current:,.2f}",
            delta=get_delta('resale_price',"max"),
            delta_color="normal" , 
            help = "Highest Resale Price for the selected period"
)
    met2.metric(
        label = "Total Number of Transactions",
        value = total_num_transactions,
        delta= get_delta('town',"count"),
        delta_color= 'normal',
        help = "Total number of resale transactions for the selected period"
    )
    met3.metric(
        label = "Lowest Resale Price",
        value=f"${min_price_current:,.2f}",
        delta = get_delta('resale_price',"min"),
        delta_color= 'normal',
        help = "Lowest Resale Price for the selected period"
    )

st.markdown("---")
line_data = df[df['town'] == town_option]
tab1_data = line_data.groupby(['town','month'])['resale_price'].mean().reset_index()
tab2_data = line_data.groupby(['town','year'])['resale_price'].mean().reset_index()

tab1, tab2 = st.tabs(["Monthly", "Yearly"])
with tab1: 
    st.subheader(f"Average Resale Price Over Time (Monthly) - {town_option}")
    tab1_data.set_index('month', inplace=True)
    st.line_chart(tab1_data["resale_price"],y_label= "Average Resale Price")
with tab2:
    st.subheader(f"Average Resale Price Over Time (Yearly) - {town_option}")
    tab2_data.set_index('year', inplace=True)
    st.line_chart(tab2_data["resale_price"],y_label= "Average Resale Price")


line_data = df[df['town'] == town_option]
tab3_data = line_data.groupby(['town','month'])['resale_price'].count().reset_index()
tab4_data = line_data.groupby(['town','year'])['resale_price'].count().reset_index()
tab3_data["Number of Transactions"] = tab3_data["resale_price"]
tab4_data["Number of Transactions"] = tab4_data["resale_price"]

tab3, tab4 = st.tabs(["Monthly", "Yearly"])
with tab3: 
    st.subheader(f"Total number of Transactions Over Time (Monthly) - {town_option}")
    tab3_data.set_index('month', inplace=True)
    st.line_chart(tab3_data["Number of Transactions"],y_label="Number of transactions")
with tab4:
    st.subheader(f"Total number of Transactions Over Time (Yearly) - {town_option}")
    tab4_data.set_index('year', inplace=True)
    st.line_chart(tab4_data["Number of Transactions"],y_label="Number of transactions")

flat_data = df[(df['town'] == town_option) & (df["year"] == year_option)]
flat_data = flat_data.groupby('flat_type')['resale_price'].mean().reset_index()

st.subheader(f"Average Resale Price in {town_option} by Flat Type ({year_option})")

# Create the bar chart with Plotly
fig = px.bar(flat_data, x='flat_type', y='resale_price',
             labels={'resale_price': 'Average Resale Price', 'flat_type': 'Flat Type'},
             text='resale_price')

# Add value labels on top of the bars
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')

# Customize layout
fig.update_layout(yaxis_title='Average Resale Price', xaxis_title='Flat Type')

# Display the chart in Streamlit
st.plotly_chart(fig)


