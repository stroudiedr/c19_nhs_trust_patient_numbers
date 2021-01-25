import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.title("COVID-19 NHS Trust Patient Numbers")

#Dataframe
@st.cache
def load_data():
		url = "https://api.coronavirus.data.gov.uk/v2/data?areaType=nhsTrust&metric=hospitalCases&metric=newAdmissions&metric=covidOccupiedMVBeds&format=csv"

		from urllib.request import urlretrieve
		urlretrieve(url,"covid-19.csv")

		df = pd.read_csv("covid-19.csv",parse_dates=["date"])
		df = df[df["areaCode"].str.len()== 3]
		df.columns = ["Date","Type","Code","NHS_Trust","Hosp_Cases","New_Adms","C19_Mech_Vent"]
		df_gp = df.groupby("NHS_Trust")[["Hosp_Cases","New_Adms","C19_Mech_Vent"]].max()
		df_gp = df_gp[df_gp["C19_Mech_Vent"]>0]
		Trust_MV = df_gp.index.tolist()
		df = df[df["NHS_Trust"].isin(Trust_MV)]

		return df

df = load_data()

#Grouped information
df_gp = df.groupby("NHS_Trust")[["Hosp_Cases","New_Adms","C19_Mech_Vent"]].max()

st.text("Maximum numbers by Acute NHS Trust")
st.write(df_gp," ")

#NHS Trust selection
hospitals = df["NHS_Trust"].sort_values().unique()
sel_hosp = st.selectbox("NHS Trust Name",hospitals)
max_date = df.loc[df["NHS_Trust"]==sel_hosp]["Date"].max()
max_date = max_date.strftime("%Y-%m-%d")

#Rolling average
rolling = st.radio("How many days to average the data over?",("1 day","3 days","5 days","7 days"))

if rolling == "3 days":
	roll = 3
elif rolling == "5 days":
	roll = 5
elif rolling == "7 days":
	roll = 7
else:
	roll = 1

#Graphing
hosp_date = df.loc[df["NHS_Trust"]==sel_hosp]["Date"]
hosp_newAdmissions = df.loc[df["NHS_Trust"]==sel_hosp]["New_Adms"]
hosp_hospCases = df.loc[df["NHS_Trust"]==sel_hosp]["Hosp_Cases"]
hosp_covidMVBeds = df.loc[df["NHS_Trust"]==sel_hosp]["C19_Mech_Vent"]

fig,[ax1,ax2,ax3] = plt.subplots(3,1,figsize=(15,15))

ax1.plot(hosp_date,hosp_newAdmissions.rolling(roll).mean())
ax1.set_title("New Hospital Admissions",fontsize=20)
ax1.set(xlabel="Date",ylabel="Daily patients (5day average)")
ax1.grid()

ax2.plot(hosp_date,hosp_hospCases.rolling(roll).mean())
ax2.set(xlabel="Date",ylabel="Daily total inpatient numbers (5day average)")
ax2.set_title("Hospital COVID19 +ve inpatient numbers",fontsize=20)
ax2.grid()

ax3.plot(hosp_date,hosp_covidMVBeds.rolling(roll).mean())
ax3.set(xlabel="Date",ylabel="Daily patients (5day average)")
ax3.set_title("COVID related inpatients requiring mechanical ventilation",fontsize=20)
ax3.grid()


plt.subplots_adjust(hspace=0.3)

st.pyplot(fig)

st.text(f"Latest date of the downloaded data for this NHS Trust is {max_date}")


# Sidebar information
st.sidebar.title("Welcome to this app ")
st.sidebar.text("""
This simple app displays NHS patient 
numbers that are associated with 
COVID-19 infection and hospital 
admission.

Graphs show new daily admissions,
number of hospital inpatients,
number of patients on mechanical
ventilation. Numbers are displayed
as a rolling 5 day average.
""")

st.sidebar.header("Data source")
st.sidebar.text("""
Data is downloaded from Gov.uk.
It is the most uptodate information
on COVID-19 infection that is 
publically available.
""")
st.sidebar.markdown("[https://coronavirus.data.gov.uk/](https://coronavirus.data.gov.uk/)")


st.sidebar.header("About")
st.sidebar.text("""
App made using Python 3.8 & Streamlit
by Dr David Freeman
Worcestershire Acute Hospitals
NHS Trust
""")

st.sidebar.text("""
For further information see:
""")
st.sidebar.markdown("[Github](https://github.com/stroudiedr/c19_nhs_trust_patient_numbers.git)")
st.sidebar.markdown("[Twitter](https://twitter.com/StroudieDr)")
