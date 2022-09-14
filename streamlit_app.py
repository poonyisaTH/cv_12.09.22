
import streamlit as st
import pandas as pd
import numpy as np

private_gsheets_url = "https://docs.google.com/spreadsheets/d/1DZUnRl0vcmpP5rC4eUwIQy-CM1BQ2XYK6Sy_4vsLpRU/edit?usp=sharing"

type = "service_account"
project_id = "xxx"
private_key_id = "xxx"
private_key = "xxx"
client_email = "xxx"
client_id = "xxx"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "xxx"



st.title('การประเมินความเสี่ยงในการเกิดโรคหัวใจ')
st.subheader('ศูนย์การแพทย์กาญจนาภิเษก')


#database
title = st.text_input('ชื่อ-สกุล')
gender = st.radio('เพศ',('ชาย','หญิง'))
telephone = st.text_input('เบอร์โทรศัพท์')
current_address = st.selectbox('ที่อยู่ปัจจุบัน',('ในเขตมหาสวัสดิ์','นอกเขต'))
age = st.number_input('อายุ (ปี)',0,130,50)
smoking = st.selectbox('สูบบุหรี',('ไม่สูบ','สูบ'))
fbs = st.radio('เบาหวาน',('ไม่เป็น','เป็น'))

    #show if have diabets
if(fbs=='เป็น'):
   cal_fbs=5
else:
    cal_fbs=0


blood_pressure_up = st.number_input('ความดันโลหิตตัวบน(mmHg.)',0)
blood_pressure_down = st.number_input('ความดันโลหิตตัวล่าง(mmHg.)',0)
waist = st.number_input('รอบเอว (ซม.)',0)

#cal_age
if (age<=39):
    cal_age=-2
elif (age<=44):
    cal_age=0
elif (age<=49):
    cal_age=2
elif (age<=54):
    cal_age=4
elif (age<=59):
    cal_age=6
elif (age>=60):
    cal_age=8

#cal_BP
if(blood_pressure_up>=140)or(blood_pressure_down>=90):
    cal_BP=3
else:
    cal_BP=0

#cal_gender
if(gender=='ชาย'):
    cal_gender=3
else:
    cal_gender=0

#cal_smoking
if(smoking=='สูบ'):
    cal_smoking=2
else:
    cal_smoking=0

#cal_waist
if(gender=='ชาย')and(waist>=90):
    cal_waist=4
elif(gender=='หญิง')and(waist>=80):
    cal_waist=4
else:
    cal_waist=0


#Total_score
Total_score=int(cal_age+cal_BP+cal_gender+cal_smoking+cal_waist+cal_fbs)

#chance
if (Total_score<=0):
    chance=0
elif(Total_score<=5):
    chance=1
elif(Total_score<=8):
    chance=2
elif(Total_score<=9):
    chance=3
elif(Total_score<=11):
    chance=4
elif(Total_score<=12):
    chance=5
elif(Total_score<=13):
    chance=6
elif(Total_score<=14):
    chance=7
elif(Total_score<=15):
    chance=10
elif(Total_score>=16):
    chance=12
    
#Group
if(chance<=1):
    Group='ความเสี่ยงน้อย'
elif(chance<=4):
    Group='ความเสี่ยงปานกลาง'
elif(chance<=8):
    Group='ความเสี่ยงสูง'
elif(chance<=12):
    Group='ความเสี่ยงสูงมาก'

#suggestion 
if(Group=='ความเสี่ยงน้อย'):
    suggestion='สุขภาพของคุณอยู่ในเกณฑ์ดี ควรออกกำลังกายอย่างสม่ำเสมอ และตรวจสุขภาพประจำปีเพื่อป้องกันการเกิดโรคหลอดเลือดหัวใจ'
elif(Group=='ความเสี่ยงปานกลาง'):
    suggestion='ควรออกกำลังกายสม่ำเสมอ ควรควบคุมอาหารรสหวาน มัน และเค็มจัด งดการสูบบุหรี่ทันที และควรปรึกษาแพทย์เพื่อขอคำแนะนำที่ถูกต้องต่อไป'
elif(Group=='ความเสี่ยงสูง'):
    suggestion='ควรออกกำลังกายอย่างสม่ำเสมอ ควรควบคุมอาหารรสหวาน มัน และเค็มจัด งดการสูบบุหรี่ทันที และควรปรึกษาแพทย์เพื่อขอคำแนะนำที่ถูกต้องโดยเร็ว'
elif(Group=='ความเสี่ยงสูงมาก'):
    suggestion='ควรปรับเปลี่ยนพฤติกรรม เลิกบุหรี่ ออกกำลังกาย ควบคุมอาหาร รักษาความดันโลหิตอย่างเข็มงวด ลดความอ้วน และรีบปรึกษาแพทย์ เพื่อขอคำแนะนำที่ถูกต้องทันที'


#button
if(st.button('บันทึกข้อมูล')):
   st.write('คะแนนของคุณ =',Total_score)

   if(Group=='ความเสี่ยงน้อย'):
    st.success('ความเสี่ยงน้อย')
   elif(Group=='ความเสี่ยงปานกลาง'):
    st.warning('ความเสี่ยงปานกลาง')
   elif(Group=='ความเสี่ยงสูง'):
    st.error('ความเสี่ยงสูง')
   elif(Group=='ความเสี่ยงสูงมาก'):
    st.error('ความเสี่ยงสูงมาก')

   if(suggestion=='สุขภาพของคุณอยู่ในเกณฑ์ดี ควรออกกำลังกายอย่างสม่ำเสมอ และตรวจสุขภาพประจำปีเพื่อป้องกันการเกิดโรคหลอดเลือดหัวใจ'):
    st.success('สุขภาพของคุณอยู่ในเกณฑ์ดี ควรออกกำลังกายอย่างสม่ำเสมอ และตรวจสุขภาพประจำปีเพื่อป้องกันการเกิดโรคหลอดเลือดหัวใจ')
   elif(suggestion=='ควรออกกำลังกายสม่ำเสมอ ควรควบคุมอาหารรสหวาน มัน และเค็มจัด งดการสูบบุหรี่ทันที และควรปรึกษาแพทย์เพื่อขอคำแนะนำที่ถูกต้องต่อไป'):
    st.warning('ควรออกกำลังกายสม่ำเสมอ ควรควบคุมอาหารรสหวาน มัน และเค็มจัด งดการสูบบุหรี่ทันที และควรปรึกษาแพทย์เพื่อขอคำแนะนำที่ถูกต้องต่อไป')
   elif(suggestion=='ควรออกกำลังกายอย่างสม่ำเสมอ ควรควบคุมอาหารรสหวาน มัน และเค็มจัด งดการสูบบุหรี่ทันที และควรปรึกษาแพทย์เพื่อขอคำแนะนำที่ถูกต้องโดยเร็ว'):
    st.error('ควรออกกำลังกายอย่างสม่ำเสมอ ควรควบคุมอาหารรสหวาน มัน และเค็มจัด งดการสูบบุหรี่ทันที และควรปรึกษาแพทย์เพื่อขอคำแนะนำที่ถูกต้องโดยเร็ว')
   elif(suggestion=='ควรปรับเปลี่ยนพฤติกรรม เลิกบุหรี่ ออกกำลังกาย ควบคุมอาหาร รักษาความดันโลหิตอย่างเข็มงวด ลดความอ้วน และรีบปรึกษาแพทย์ เพื่อขอคำแนะนำที่ถูกต้องทันที'):
    st.error('ควรปรับเปลี่ยนพฤติกรรม เลิกบุหรี่ ออกกำลังกาย ควบคุมอาหาร รักษาความดันโลหิตอย่างเข็มงวด ลดความอ้วน และรีบปรึกษาแพทย์ เพื่อขอคำแนะนำที่ถูกต้องทันที') 
