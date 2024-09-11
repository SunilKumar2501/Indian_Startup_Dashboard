import streamlit as st
import pandas as pd
import time
# Text uilities
st.title("Starting Dashboard")
st.header("I am learning Streamlit")
st.subheader("ans I am loving it")
st.write("This is a normal test")
st.markdown('''
### My Favourite movie
- Race3
- Humshakals
- Grand Masti
''')
st.code("""
def prints(input):
    return input ** 2
x = prints(5)
""")
st.latex("x^2 + y^2 + 2 = 0")

#display elements
df = pd.DataFrame({
    "name" : ["Sunil","Happy","Piush"],
    "marks": [67,89,55],
    "age" :[23,25,22]
})
st.dataframe(df)
st.metric("Revenue", "Rs 3L", "-3%")
st.json({
    "name" : ["Sunil","Happy","Piush"],
    "marks": [67,89,55],
    "age" :[23,25,22]
})

st.image("img.png")
st.video("video.mp4")

st.sidebar.title("Sidebar ka title")

col1, col2 ,col3= st.columns(3)
with col1:
    st.image("img.png")
with col2:
    st.image("img.png")
with col3:
    st.image("img.png")

st.error("Login Failed")
st.success("Login Successful")
st.warning("danger ahead")
st.info("Login successful")

bar = st.progress(0)
for i in range(1,101):
    time.sleep(0.001)
    bar.progress(i)

input = st.text_input("Enter Email:")
number = st.number_input("Enter your age")
date =st.date_input("Birth date")

email = st.text_input("Enter email")
password = st.text_input('Enter password')
gender = st.selectbox("Select gender",["male","female","other"])
btn = st.button("Login Karo")



if btn:
    if email == "sunil@gmail.com" and password == "1234":
        st.success("Login Successful")
        st.balloons()
        st.write(gender)
    else:
        st.error("Login Failed")


st.divider()
st.subheader("View any CSV file here")
st.divider()
file = st.file_uploader("Upload a csv file")
if file is not None:
    df = pd.read_csv(file)
    st.dataframe(df.describe())