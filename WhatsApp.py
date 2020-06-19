import streamlit as st
import Txt_Parser as Me
import pandas as pd
import plotly.graph_objects as go



def prep(file):
    a = Me.ParseData(file)
    b = Me.Dataset(a)
    Data = pd.DataFrame(b)
    Data["Date"] = pd.to_datetime(Data.Date, dayfirst=True)
    return Data

st.title("Anino's Chat Analyzer")
file=st.file_uploader("Please upload your WhatsApp file here", type="txt", encoding="utf-8")
if file:
    data = prep(file)
    Month_dic = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
    Year = list(set([i.year for i in data.Date]))

    All_Mths = st.sidebar.checkbox("All Months",True)
    All_Yrs = st.sidebar.checkbox("All Years", True)

    if All_Mths and All_Yrs :
        st.dataframe(data)
    elif All_Mths and not All_Yrs :
        Year_sel = st.sidebar.selectbox(label="Year", options=Year)
        st.dataframe(data[(data.Date.dt.year == Year_sel)])
    elif not All_Mths and All_Yrs:
        Month_sel = st.sidebar.selectbox(label="Month", options=list(Month_dic.keys()))
        st.dataframe(data[(data.Date.dt.month == Month_dic[Month_sel])])
    elif not All_Mths and not All_Yrs :
        Month_sel = st.sidebar.selectbox(label="Month", options=list(Month_dic.keys()))
        Year_sel = st.sidebar.selectbox(label="Year", options=Year)
        st.dataframe(data[(data.Date.dt.month == Month_dic[Month_sel]) & (data.Date.dt.year == Year_sel)])


    st.subheader("Daily Message Count")
    radio = st.radio("Choose Type",["Tabular","Graph"])

    MessageCnt = data.groupby(["Date","Sender"])["Message"].count().unstack()
    MessageCnt = MessageCnt.fillna(0)

    senders = data["Sender"].unique()
    idx = MessageCnt.index
    MessageCnt["Total"] = MessageCnt[senders[0]] + MessageCnt[senders[1]]

    if radio == "Tabular":
        st.write(MessageCnt)

    else:
        Choices = st.multiselect("Select Data: ", options= MessageCnt.columns)
        fig = go.Figure()
        for col in Choices:
            fig.add_trace(go.Scatter(x=idx, y=MessageCnt[col], mode='lines', name=col, line_shape="spline"))

        st.plotly_chart(fig)


