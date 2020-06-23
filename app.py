import streamlit as st
import pandas as  pd 
import numpy as np 


st.title("Financial Application")


def ratio_analysis():
    df = pd.read_csv("ratio analysis.csv" )
    return df

profitability_inputs = {
    "Net Income": 1.0 , 
    "Net Sales":1.0, 
    "Gross Profit": 1.0, 
    "average total assets": 1.0,
    "Average total equity": 1.0 
}

if st.sidebar.checkbox("ratio analysis" , False):
    if st.checkbox("Main key points" , False):
        st.table(ratio_analysis())
    analysis_options = st.sidebar.radio("What type of analysis do you want" , ["All" , "Profitability" , "Liquidity" , "Operating cycle analysis"])
    if analysis_options == "Profitability":
        for k , v in profitability_inputs.items():
            profitability_inputs[k] = st.number_input("Enter {}".format(k)  , 0.0)
        if st.checkbox("Show result" , False):
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


        
if st.sidebar.checkbox("Compare between stocks return" , False):
    pass
