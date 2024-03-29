#importing required packages
import streamlit as st
import numpy as np
import pandas as pd
import easyocr
from PIL import Image
import mysql.connector
import re

#setting the sql server
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database='bizcardx'
)

mycursor = mydb.cursor(buffered=True)

#streamlit page layout setup
st.set_page_config(page_title='Bizcardx', page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
uploaded = st.file_uploader('''      Upload the business card to exctract ''', type = ['PNG', 'JPEG', 'JPG'])

#function to extract text
def extract(array):
    reader = easyocr.Reader(['en'],gpu=False)
    result = reader.readtext(array)
    text = ''
    for word in result:
        text += word[1] + ' '
    return text

#function to classify company name
def company(sent):
    key = ['Sun Electricals','selva digitals','Family Restaurant','BORCELLE AIRLINES','GLOBAL INSURANCE']
    company_name=''
    for word in sent:
        company_name=''
        for i in key:
            com = i.split()
            for j in com:
                if re.match(j,word):
                    company_name = i
    return company_name

#function to classify degination
def designation(sent):
    des=['Marketing Executive','Technical Manager','General Manager','CEO & FOUNDER','DATA MANAGER']
    design=''
    for word in sent:
        for i in des:
            role=i.split()
            for j in role:
                if re.match(j,word):
                    design = i
    return design

#function to classify mobile number
def number(sent):
    num =''
    for word in sent:
        if '-' in word:
            num = word
    return num

#function to classify email address
def mail(sent):
    email=''
    for word in sent:
        if re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b',word):
            email = word
    return email

#function to classify website url
def website(sent):
    url = ''
    for word in sent:
        if re.match(r'^www.[a-zA-Z]',word):
            url = word
    return url

#function to classify area
def area(sent):
    area_out=''
    for word in sent:
        if re.match('St$', word):
            x = sent.index(word)
            area_out+=sent[x-2]+' '+sent[x-1]+' '+word
    return area_out

#function to classify city
def city(sent):
    city_out=''
    for word in sent:
        if re.match('St$',word):
            x = sent.index(word)
            for i in range(1,3):
                if re.match('[A-Za-z]',sent[x+i]):
                    city_out+=sent[x+i]
                    break
    return city_out

#function to classify state
def state(sent):
    state = ['Andhra Pradesh','Arunachal Pradesh','Assam','Bihar','Chhattisgarh','Goa',
            'Gujarat','Haryana','Himachal Pradesh','Jharkhand','Karnataka','Kerala','Maharashtra',
            'Madhya Pradesh','Manipur','Meghalaya','Mizoram','Nagaland','Odisha','Punjab',
            'Rajasthan','Sikkim','TamilNadu','Tripura','Telangana','Uttar Pradesh','Uttarakhand','West Bengal']
    for word in sent:
        for i in state:
            if i in word:
                return i

#function to classify pincode
def pin(sent):
    pin = ''
    for word in sent:
        if len(word) == 6 and re.match(r'[0-9]',word):
            pin = word
    return pin

#function to classify card holder name
def name(sent):
    hold=''
    ext=[]
    des=['Marketing',' Executive','Technical','Manager','General','Manager','CEO','&','FOUNDER','DATA','MANAGER']
    for word in sent:
        for i in des:
          if i in word:
            ind=sent.index(i)
            ext =(sent[:ind])
            for role in ext:
              if role not in des and role not in hold:
                hold += role + ' '
    return hold

#function to create table in sql
def create_table():
    mycursor.execute("""CREATE TABLE IF NOT EXISTS data
                     (Company VARCHAR(50) Primary key,Card_holder_name VARCHAR(20),Designation VARCHAR(50),
                     Mobile VARCHAR(20),Email VARCHAR(30),Website VARCHAR(50),
                     Area VARCHAR(30),City VARCHAR(50),State VARCHAR(30),Pin_code Varchar(10))""")
    mydb.commit()

#streamlit columns setup
col1,col2,col3 = st.columns(3)


if uploaded is not None:
    img = Image.open(uploaded)
    arr = (np.array(img))
    data = extract(arr)

    extract_text = data.split()
    
    #assigning the sorted value
    company_name = company(extract_text)
    card_holder_name = name(extract_text)
    desig = designation(extract_text)
    mobile = number(extract_text)
    email_address = mail(extract_text)
    website_url = website(extract_text)
    area_line = area(extract_text)
    city_line = city(extract_text)
    state_line = state(extract_text)
    pin_code = pin(extract_text)

    with col1:
        #Writing the sorted values
        st.button('EXTRACTED TEXT')
        st.write('''Company:''',company_name)
        st.write('''Card holder name:''',card_holder_name)
        st.write('''Designation:''',desig)
        st.write('''Mobile:''',mobile)
        st.write('''Email:''',email_address)
        st.write('''Website:''',website_url)
        st.write('''Area:''',area_line)
        st.write('''City:''',city_line)
        st.write('''State:''',state_line)
        st.write('''Pin code:''',pin_code)
    
    with col2:
        #inserting the sorted values in sql table
        if st.button('SAVE'):
            create_table()
            try:
                query = """INSERT INTO data VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                mycursor.execute(query,(company_name,card_holder_name,desig,mobile,email_address,website_url,area_line,city_line,state_line,pin_code))
                mydb.commit()
                st.success('SUCCESSFULLY SAVED')
            except:
                st.error('ALREADY EXIST')
    
    with col3:
        #getting the saved data
        try:
            if st.button('SHOW THE STORED DATA'):
                mycursor.execute("""SELECT * FROM data""")
                data_df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
                st.write(data_df.T)       
        except:
            st.code('NO DATA SAVED')
        
        #deleting the saved data
        if st.button('DELETE'):
                mycursor.execute(""" DROP TABLE data""")
                mydb.commit()
                st.success('DELETED SUCCESSFULLY')

    
    if st.button('Image'):
        st.image(img)
