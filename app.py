import streamlit as st
import pandas as  pd 
import numpy as np 



st.title("Financial Application")

@st.cache(persist=True)
def ratio_analysis():
    df = pd.read_csv("ratio analysis.csv" )
    return df 

latest_iteration = st.empty()
bar = st.progress(0)
@st.cache(persist=True)
def load_data(path , sheets_num ):
    data = []
    c= 0
    for i in range(sheets_num):
        df = pd.read_excel(path , sheet_name = sheets_num - 1)
        data.append(df)
        c= int(i/sheets_num * 100)
        latest_iteration.text("progress is {}%".format(c))
        bar.progress(c)
    c = 100
    latest_iteration.text("progress is {}%".format(c ))
    bar.progress(c )

    return data

profitability_inputs = {
    "Net Income": 1.0 , 
    "Net Sales":1.0, 
    "Gross Profit": 1.0, 
    "average total assets": 1.0,
    "Average total equity": 1.0 
}

liquidity_inputs = {
    "Current assets": 1.0 , 
    "current liabilities": 1.0,
    "Cash": 1.0 , 
    "Inventory": 1.0, 
    "Receivables" : 1.0 , 
    "Prepayments": 1.0 ,
    "Marketable securitis": 1.0
}

def profitability_inputs_f():
    for k , v in profitability_inputs.items():
        profitability_inputs[k] = st.number_input("Enter {}".format(k)  , 1.0)

def liquidity_inputs_f():
    for k , v in liquidity_inputs.items():
        liquidity_inputs[k] = st.number_input("Enter {}".format(k)  , 1.0)

def result_profitability():
    result = {
    "ROROS": profitability_inputs["Net Income"] / profitability_inputs["Net Sales"] , 
    "GPM" : profitability_inputs["Gross Profit"] / profitability_inputs["Net Sales"] ,
    "TAT": profitability_inputs["Net Sales"] / profitability_inputs["average total assets"] , 
    "ROI": profitability_inputs["Net Income"] / profitability_inputs["average total assets"] ,
    "ROROTE": profitability_inputs["Net Income"] / profitability_inputs["Average total equity"]

    }

    st.markdown("#### rate of return on sales(Net profit margin) = `{:.2f}` pound ".format(result["ROROS"]))
    st.markdown("#### Gross profit margin = `{:.2f}` pound ".format(result["GPM"]))
    st.markdown("#### Total asset turnover = `{:.2f}` time".format(result["TAT"]))
    st.markdown("#### Rate of return on assets (return on investment )--ROI= `{:.2f}` pound".format(result["ROI"]))
    st.markdown("#### Rate of return on total equity= `{:.2f}` pound".format(result["ROROTE"]))



if st.sidebar.checkbox("ratio analysis" , False):
    if st.checkbox("Main key points" , False):
        st.table(ratio_analysis())
    analysis_options = st.sidebar.radio("What type of analysis do you want" , ["All" , "Profitability" , "Liquidity" , "Operating cycle analysis"])
    if analysis_options == "Profitability":
        profitability_inputs_f()
    elif analysis_options == "Liquidity":
        liquidity_inputs_f()
    elif analysis_options == "All":
        profitability_inputs_f()
        liquidity_inputs_f()

    if st.checkbox("Show result" , False):
        result_profitability()



        
if st.sidebar.checkbox("Compare between stocks return" , False):
    
    sheets_num = st.number_input("How many sheets (Stock) do you want to compare between them" , 1)
    file_uploader = st.file_uploader("Import your excel stock data" , type="xlsx")
    if file_uploader != None:
        dfs = load_data(file_uploader , sheets_num =sheets_num )
        if st.checkbox("Do you want see a sample, to chech if data loaded corretly" , False):
            c = 0
            for df in dfs:
                c += 1
                st.title("Stock {c}".format(c=c))
                st.write(df.sample())
    