import streamlit as st
from snowflake.snowpark.context import get_active_session
import altair as alt
import datetime


session = get_active_session()
st.set_page_config(layout="wide")
new_line = '\n'


@st.cache_data
def load_data():
    df = session.table('streamlit_apps.public.raw_transactions').to_pandas()
    return df


df = load_data()

st.title("Streamlit App Demo")


st.subheader("Input Widgets")
st.write('')

col1,col2,col3 = st.columns(3)

product = col1.selectbox("Product",df['PRODUCT_CATEGORY'].unique())
channel = col2.multiselect("Channel",df['SALES_CHANNEL'].unique())
comment = col3.text_input(("Type in your comment"))

filtered_df = df[df['PRODUCT_CATEGORY'] == product]
product_df = filtered_df.groupby('REGION')[['QUANTITY_SOLD','TOTAL_AMOUNT']].sum().reset_index()


st.subheader("Chart Widgets")

st.markdown(f"""<span style="font-size:20px;text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3); color:#45b39d">**Bar Chart**</span>""", unsafe_allow_html=True)                
st.line_chart(filtered_df, x='TRANSACTION_DATE', y='TOTAL_AMOUNT')


chart1,chart2 = st.columns(2)

chart1.markdown(f"""<span style="font-size:20px; color:#45b39d">**Bar Chart**</span>""", unsafe_allow_html=True)                
chart1.bar_chart(product_df, x='REGION', y='QUANTITY_SOLD')

chart2.markdown(f"""<span style="font-size:20px; color:#45b39d">**Scatter Chart**</span>""", unsafe_allow_html=True)                

