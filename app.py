import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout = "wide",page_title="Indian Startup Analysis")

# some data preprocessing
df = pd.read_csv("startup_clean.csv")
df["investors"] = df["investors"].fillna("Undisclosed")
lst = sorted(set(df["investors"].str.split(",").sum()))
del lst[0:2]
df["date"] = pd.to_datetime(df["date"],errors = "coerce")
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df.replace({
    "Bangalore" : "Bengaluru"
},inplace = True)
df.replace({
    "Flipkart.com": "Flipkart"
},inplace = True)
df["startup"].replace({'"BYJU\\\\\'S"': "Byju's"}, inplace=True)
df.replace({"https://www.wealthbucket.in/" : "WealthBucket"},inplace = True)

def load_overall_analysis():
    #total invested amount
    total = df["amount"].sum()
    #maximum amount infused in single startup
    max = df.groupby("startup")["amount"].max().sort_values(ascending=False).head(2).values[0]
    #avergae invested amount
    mean = df.groupby("startup")["amount"].sum().mean()
    #total funded startups
    all = df["startup"].nunique()

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.metric("Total" , str(total)+"Cr")
    with col2:
        st.metric("Max", str(max) + "Cr")
    with col3:
        st.metric("Average",str(round(mean,2))+ "Cr")
    with col4:
        st.metric("Funded Startup",str(all))
    col1, col2 = st.columns(2)
    st.divider()
    with col1:
        st.header("MoM graph")
        selected_option = st.selectbox("Select Type", ["Total", "Count","All Total","All Count"])
        if selected_option == "Total":
            temp_df = df.groupby(["year", "month"], as_index=False)["amount"].sum()
            temp_df["x_axis"] = temp_df["month"].astype("str") + "/" + (temp_df["year"] % 100).astype('str')

            fig3, ax3 = plt.subplots()
            # Create a dropdown to select a year
            selected_year = st.selectbox("Select Year", temp_df["year"].unique())
            # Filter the DataFrame based on the selected year
            filtered_df = temp_df[temp_df["year"] == selected_year]
            # Plot the filtered data
            ax3.plot(filtered_df["x_axis"], filtered_df["amount"])
            st.pyplot(fig3)
        elif selected_option == "Count":
            temp_df = df.groupby(["year", "month"], as_index=False)["amount"].count()
            temp_df["x_axis"] = temp_df["month"].astype("str") + "/" + (temp_df["year"] % 100).astype('str')

            fig3, ax3 = plt.subplots()
            # Create a dropdown to select a year
            selected_year = st.selectbox("Select Year", temp_df["year"].unique())
            # Filter the DataFrame based on the selected year
            filtered_df = temp_df[temp_df["year"] == selected_year]
            # Plot the filtered data
            ax3.plot(filtered_df["x_axis"], filtered_df["amount"])
            st.pyplot(fig3)
        elif selected_option == "All Total":
            temp_df = df.groupby(["year", "month"], as_index=False)["amount"].sum()
            temp_df["x_axis"] = temp_df["month"].astype("str") + "/" + (temp_df["year"] % 100).astype('str')
            fig3, ax3 = plt.subplots()
            ax3.plot(temp_df["x_axis"], temp_df["amount"])
            st.pyplot(fig3)
        else:
            temp_df = df.groupby(["year", "month"], as_index=False)["amount"].count()
            temp_df["x_axis"] = temp_df["month"].astype("str") + "/" + (temp_df["year"] % 100).astype('str')
            fig3, ax3 = plt.subplots()
            ax3.plot(temp_df["x_axis"], temp_df["amount"])
            st.pyplot(fig3)
    col1,col2= st.columns(2)
    with col1:
        st.header("Sector wise Investment graph")
        selected_option = st.selectbox("Select Type", ["Total", "Count"])
        if selected_option == "Total":
            temp_df = df.groupby("vertical")["amount"].sum().sort_values(ascending=False).head(10)
            fig3, ax3 = plt.subplots()
            ax3.pie(temp_df, labels=temp_df.index, autopct="%0.01f%%")
            st.pyplot(fig3)
        else:
            temp_df = df.groupby("vertical")["investors"].count().sort_values(ascending=False).head(10)
            fig3, ax3 = plt.subplots()
            ax3.pie(temp_df, labels=temp_df.index, autopct="%0.01f%%")
            st.pyplot(fig3)

    col1,col2,col3,col4= st.columns(4)
    with col1:
        st.header("Type of Funding")
        rounds_funding = df.groupby("round")["amount"].sum().sort_values(ascending=False).reset_index()
        rounds_funding = rounds_funding.set_index("round")
        st.dataframe(rounds_funding)
    with col2:
        st.header("City Wise Funding")
        city_funding = df.groupby("city")["amount"].sum().sort_values(ascending = False).reset_index().set_index("city").head(50)
        st.dataframe(city_funding)
    with col3:
        st.header("Top Startup Year Wise ")
        new = df.groupby(["year", "startup"], as_index=False)["amount"].sum().sort_values(["year", "amount"],ascending=[True,False]).drop_duplicates("year", keep="first")
        new["year"] = new["year"].astype("str")
        new = new.set_index("year")
        st.dataframe(new)
    with col4:
        st.header("Top Startup Overall ")
        data = df.groupby("startup", as_index=False)["amount"].sum().sort_values("amount", ascending=False)[["startup", "amount"]]
        data = data.set_index("startup")
        st.dataframe(data.head(100))

    st.header("Top Investors Overall ")
    data = df.groupby("investors")["amount"].sum().sort_values(ascending = False).head(100)
    st.dataframe(data)

    st.header("Funding Heatmap")
    grouped_data = df.groupby("startup", )["amount"].sum().head(500)
    fig, ax = plt.subplots(figsize=(20, 10))  # Adjust figure size as needed
    sns.heatmap(grouped_data.to_frame().T, ax=ax, cmap="YlGnBu")  # Use your preferred colormap
    plt.title("Total Funding Amount per Startup")
    plt.tight_layout()

    # Display the heatmap in Streamlit
    st.pyplot(fig)



def load_investor_detail(investor):
    st.title(investor)
    # load last 5 investments of the investor
    last5df = df[df["investors"].str.contains(investor)].head()[["date", "startup", "vertical", "city", "round", "amount"]]
    st.subheader("Most Recent Investments")
    st.dataframe(last5df)

    #biggest investments
    col1,col2 = st.columns(2)
    with col1:
        biggest_inv = df[df["investors"].str.contains(investor)].groupby("startup")["amount"].sum().sort_values(ascending=False).head(5)
        st.subheader("Biggest Investments")
        st.dataframe(biggest_inv)
        st.write("Bar Graph Representation")
        fig, ax = plt.subplots()
        ax.bar(biggest_inv.index, biggest_inv.values)
        st.pyplot(fig)
    with col2:
        #sector invested
        vertical_series = df[df["investors"].str.contains(investor)].groupby("vertical")["amount"].sum()
        st.subheader("Biggest Sectors Invested")
        st.dataframe(vertical_series.head(5))
        st.subheader("Sector invested in ")
        fig, ax = plt.subplots()
        ax.pie(vertical_series,labels = vertical_series.index,autopct = "%0.01f%%")
        st.pyplot(fig)

    col3,col4 = st.columns(2)
    with col3:
        rounds_series = df[df["investors"].str.contains(investor)].groupby("round")["amount"].sum()
        st.subheader("Rounds Stage ")
        fig, ax = plt.subplots()
        ax.pie(rounds_series,labels = rounds_series.index,autopct = "%0.01f%%")
        st.pyplot(fig)

    with col4:
        city_series = df[df["investors"].str.contains(investor)].groupby("city")["amount"].sum()
        st.subheader("Most Invested City")
        fig, ax = plt.subplots()
        ax.pie(city_series,labels = city_series.index,autopct = "%0.01f%%")
        st.pyplot(fig)

    col5,col6 = st.columns(2)
    with col5:
        year_series = df[df["investors"].str.contains(investor)].groupby("year")["amount"].sum()
        st.subheader("Year on Year Investments")
        val = year_series.index.astype("str")
        fig, ax = plt.subplots()
        ax.plot(val, year_series.values)
        st.pyplot(fig)
    with col6:
        st.subheader("Similar Investors with regards to Sectors ")
        investor = df[df["investors"].str.contains(investor)]
        # Check for overlapping verticals between investor and df DataFrames
        matching_verticals = np.intersect1d((investor["vertical"]), (df["vertical"].unique()))
        v = list(matching_verticals)
        # Filter based on matching verticals
        filtered_df = df[df["vertical"].isin(v)][["startup", "vertical", 'investors']].set_index("vertical")
        st.dataframe(filtered_df)



def company_details(name):
    st.title(name)
    col1,col2,col3 = st.columns(3)
    # Industry
    with col1:
        industry = df[df["startup"] == name]["vertical"].values
        st.subheader("Industry of the Company")
        st.write(industry)
    with col2:
        industry = df[df["startup"] == name]["subVertical"].values
        st.subheader("Sub Industry of the Company")
        st.write(industry)

    with col3:
        industry = df[df["startup"] == name]["city"].values
        st.subheader("City of the Company")
        st.write(industry)
    st.subheader("Funding Rounds")
    temp_df = df.copy()
    temp_df["date"] = temp_df["date"].astype("str")
    details = temp_df[temp_df["startup"]== name][["round","investors","date"]].set_index("round")
    st.dataframe(details)

    st.subheader("Similar Company")
    temp_df = df.copy()
    temp_df["date"] = temp_df["date"].astype("str")
    s = df[df["startup"] == name]
    v = s["subVertical"].unique()
    v_list = list(v)
    filtered_df = temp_df[temp_df["subVertical"].isin(v_list)][["startup","subVertical","date"]].set_index("startup")
    st.dataframe(filtered_df)


st.sidebar.title("Startup Funding Analysis")

option = st.sidebar.selectbox("Select One",["Overall Analysis","Startup","Investor"])

if option == "Overall Analysis":
    # st.title("Overall Analysis")
    btn0 = st.sidebar.button("Show Overall analysis")
    load_overall_analysis()
elif option == "Startup":
    selected = st.sidebar.selectbox("Select Startup",sorted(df["startup"].unique().tolist()))
    button1 = st.sidebar.button("Find Startup Details")
    # st.title("Startup Analysis")
    print(button1)
    if button1:
        company_details(selected)

else:
    selected = st.sidebar.selectbox("Select Startup", lst)
    button2 = st.sidebar.button("Find Investor Details")
    if button2:
        st.divider()
        load_investor_detail(selected)


