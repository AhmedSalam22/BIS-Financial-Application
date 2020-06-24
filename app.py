import streamlit as st
import pandas as  pd 
import numpy as np 
import datetime
import plotly.graph_objects as go
import matplotlib as plt



st.title("Financial Application")



def ratio_analysis():
    df = pd.read_csv("ratio analysis.csv" )
    return df 

# latest_iteration = st.empty()
# bar = st.progress(0)
# @st.cache(allow_output_mutation=True)
def load_data(path , sheets_num ):
    data = []
    # c= 0
    for i in range(sheets_num):
        df = pd.read_excel(path , sheet_name = i)
        df["return"] = df["Adj Close"].pct_change()
        df["down"] = df["return"].apply(lambda x: x if x <=0 else 0)
        data.append(df)
        # c= int(i/sheets_num * 100)
        # latest_iteration.text("progress is {}%".format(c))
        # bar.progress(c)
    # c = 100
    # latest_iteration.text("progress is {}%".format(c ))
    # bar.progress(c )

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

Operating_cycles_inputs = {
    "cost of goods sold": 1.0 ,
    "average inventory" : 1.0 ,
    "Net sales": 1.0 , 
    "Average gross receivables": 1.0,

}

def profitability_inputs_f():
    for k , v in profitability_inputs.items():
        profitability_inputs[k] = st.number_input("Enter {}".format(k)  , 1.0)

def liquidity_inputs_f():
    for k , v in liquidity_inputs.items():
        liquidity_inputs[k] = st.number_input("Enter {}".format(k)  , 1.0)

def operating_inputs_f():
    for k , v in Operating_cycles_inputs.items():
        Operating_cycles_inputs[k] = st.number_input("Enter {}".format(k)  , 1.0)

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

def result_liquidity():
    liq_result = {
        "Current Ratio": liquidity_inputs["Current assets"] /  liquidity_inputs["current liabilities"] ,
        "Acid-test ratio": (liquidity_inputs["Cash"] + liquidity_inputs["Receivables"] +liquidity_inputs["Marketable securitis"] )/  liquidity_inputs["current liabilities"] ,
        "Quick Ratio" : (liquidity_inputs["Current assets"] -( liquidity_inputs["Inventory"] +liquidity_inputs["Prepayments"]) )/  liquidity_inputs["current liabilities"] ,
        "Cash Ratio": (liquidity_inputs["Cash"] + liquidity_inputs["Marketable securitis"]) / liquidity_inputs["current liabilities"]

    }
    for k , v in liq_result.items():
        st.markdown("#### {k} is `{v:.2f}` times".format(k=k, v=v))

def result_oprerating_cycle():
    #     "cost of goods sold": 1.0 ,
    # "average inventory" : 1.0 ,
    # "Net sales": 1.0 , 
    # "Average gross receivables": 1.0,
    inventoryTurnOverTimes = Operating_cycles_inputs["cost of goods sold"] / Operating_cycles_inputs["average inventory"]
    inventoryTurnOverDays =  365 / inventoryTurnOverTimes 
    AccRecTimes = Operating_cycles_inputs["Net sales"] / Operating_cycles_inputs["Average gross receivables"]
    AccRecDays = 365 / AccRecTimes
    OC = inventoryTurnOverDays + AccRecDays
  
    operating_result = {
        "Inventory trunover in times": inventoryTurnOverTimes ,
        "Inventory trunover in days" : inventoryTurnOverDays ,
        "Acc. Rec. trunover in times": AccRecTimes ,
        "Acc. Rec. trunover in days" : AccRecDays,
        "Operating Cycle in term of days" : OC 

    }
    for k , v in operating_result.items():
        st.markdown("#### {k} is `{v:.2f}` ".format(k=k, v=v))


if st.sidebar.checkbox("ratio analysis" , False):
    if st.checkbox("Main key points" , False):
        st.table(ratio_analysis())
    analysis_options = st.sidebar.radio("What type of analysis do you want" , ["Profitability" , "Liquidity" , "Operating cycle analysis"])
    if analysis_options == "Profitability":
        profitability_inputs_f()
        if st.checkbox("Show result" , False):
            result_profitability()
    elif analysis_options == "Liquidity":
        liquidity_inputs_f()
        if st.checkbox("Show result" , False):
            result_liquidity()
    elif analysis_options == "Operating cycle analysis":
        operating_inputs_f()
        if st.checkbox("Show result" , False):
            result_oprerating_cycle()
  
        
if st.sidebar.checkbox("Compare between stocks return" , False):
    
    sheets_num = st.number_input("How many sheets (Stock) do you want to compare between them" , 1)

    file_uploader = st.file_uploader("Import your excel stock data" , type="xlsx")
    start_date = None
    end_date = None
    if st.checkbox("Do you want to filter the data by date?" , False):
        start_date = st.date_input("Start date" , datetime.date(2001, 7, 6))
        end_date =  st.date_input("End date" , datetime.date(2003, 7, 6))
    if file_uploader != None:
        dfs = load_data(file_uploader , sheets_num =sheets_num )
        if start_date != None and end_date != None:
            for i in  range(len(dfs)):
                dfs[i] = dfs[i].query('Date >= @start_date and Date <= @end_date')

        if st.checkbox("Do you want see a head, to check if data loaded corretly" , False):
            c = 0
            for df in dfs:
                c += 1
                st.title("Stock {c}".format(c=c))
                st.write(df.head())
        if st.checkbox("Do you want to see candlestick charts" , False):
            for  k , df in enumerate(dfs):
                st.markdown("#### stock {c}".format(c=k + 1))
                fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'])])
                st.plotly_chart(fig)

        if st.checkbox("compare" , False):
            risk_free_rate = st.number_input("Risk free Rate")
            st.warning("Sharpe ratio take into consideration the move up or down for the stock wihle sotion take just into consderation just when stock go down")
            stock_results = {}
            for  k , df in enumerate(dfs):
                st.markdown("#### stock {c}".format(c=k + 1))
                st.write(df["return"].describe())
                st.write("Sharpe ratio is equal to ")
                sharp = (df["return"].mean() -  risk_free_rate) / df["return"].std()
                st.write( sharp )
                st.write("sortino ratio is equal to ")
                sortino = (df["return"].mean() -  risk_free_rate) / df["down"].std()
                stock_results["stock {c}".format(c=k + 1)] = (("sharp ratio" , sharp) , ("sortino ratio" ,sortino ))
                st.write(  sortino)

                df["return"].plot(kind="box" , title="stock {c}".format(c=k + 1))
                st.pyplot()
            st.markdown("#### a simple comparison")
            st.table(stock_results)