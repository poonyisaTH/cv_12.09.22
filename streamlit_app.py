import pandas as pd
import streamlit as st
from pandas import DataFrame
import google_auth_httplib2
import httplib2

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import HttpRequest

SCOPE = "https://www.googleapis.com/auth/spreadsheets"
SPREADSHEET_ID = "1DZUnRl0vcmpP5rC4eUwIQy-CM1BQ2XYK6Sy_4vsLpRU"
SHEET_NAME = "Sheet1"
GSHEET_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}"
from gsheetsdb import connect

# Create a connection object.
conn = connect()

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

sheet_url = st.secrets["private_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')




@st.experimental_singleton()
def connect_to_gsheet():
    # Create a connection object.
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[SCOPE],
    )

    # Create a new Http() object for every request
    def build_request(http, *args, **kwargs):
        new_http = google_auth_httplib2.AuthorizedHttp(
            credentials, http=httplib2.Http()
        )
        return HttpRequest(new_http, *args, **kwargs)

    authorized_http = google_auth_httplib2.AuthorizedHttp(
        credentials, http=httplib2.Http()
    )
    service = build(
        "sheets",
        "v4",
        requestBuilder=build_request,
        http=authorized_http,
    )
    gsheet_connector = service.spreadsheets()
    return gsheet_connector


def get_data(gsheet_connector) -> pd.DataFrame:
    values = (
        gsheet_connector.values()
        .get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!A:N",
        )
        .execute()
    )

    df = pd.DataFrame(values["values"])
    df.columns = df.iloc[0]
    df = df[1:]
    return df


def add_row_to_gsheet(gsheet_connector, row) -> None:
    gsheet_connector.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME}!A:N",
        body=dict(values=row),
        valueInputOption="USER_ENTERED",
    ).execute()

gsheet_connector = connect_to_gsheet()

#detail  
form = st.form(key="annotation")

def clear_form():
    st.session_state["ชื่อ-สกุล"] = ""
    st.session_state["เบอร์โทรศัพท์"] = ""
    st.session_state["อายุ (ปี)"] = ""
with form:
   
    st.title('ประเมินความเสี่ยงในการเกิดโรคหัวใจ')
    st.subheader('ศูนย์การแพทย์กาญจนาภิเษก')

   
    title = st.text_input('✍️ชื่อ-สกุล',key='ชื่อ-สกุล')
    gender = st.radio('เพศ',('ชาย','หญิง'))
    telephone = st.text_input('เบอร์โทรศัพท์',key='เบอร์โทรศัพท์')
    current_address = st.selectbox('ที่อยู่ปัจจุบัน',('ในเขตมหาสวัสดิ์','นอกเขต'))
    age = st.number_input('อายุ (ปี)',0,130)
    smoking = st.selectbox('สูบบุหรี',('ไม่สูบ','สูบ'))
    fbs = st.radio('เบาหวาน',('ไม่เป็น','เป็น'))
    blood_pressure_up = st.number_input('ความดันโลหิตตัวบน(mmHg.)',0)
    blood_pressure_down = st.number_input('ความดันโลหิตตัวล่าง(mmHg.)',0)
    waist = st.number_input('รอบเอว (ซม.)',0)
    submitted = st.form_submit_button(label="Submit")
    clear = st.form_submit_button(label="Clear", on_click=clear_form)

#show if have diabets
if(fbs=='เป็น'):
    cal_fbs=5
else:
    cal_fbs=0

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

#chance of diseases
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

# percentage of diseases
if (chance == 0):
    p_diseases = '0 %'
elif(chance==1):
    p_diseases = '1 %'
elif(chance==2):
    p_diseases = '2 %'
elif(chance==3):
    p_diseases = '3 %'
elif(chance==4):
    p_diseases = '4 %'
elif(chance==5):
    p_diseases = '5 %'
elif(chance==7):
    p_diseases = '7 %'
elif(chance==8):
    p_diseases = '8 %'
elif(chance==10):
    p_diseases = '10 %'
elif(chance==12):
    p_diseases = '12 %'

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



if submitted:
    add_row_to_gsheet(
        gsheet_connector,
        [[title,gender,telephone,current_address,age,smoking,fbs,blood_pressure_up,blood_pressure_down,waist,Total_score,p_diseases,Group,suggestion]],
    )
    st.write('✅ คะแนนของคุณ 👉',Total_score)
    st.write('✅ ระดับความเสี่ยงต่อการเกิดโรคเส้นเลือดหัวใจ และหลอดเลือดในระยะเวลา 10 ปีของท่าน 👉',p_diseases)
    st.write('✅ จัดอยู่ในกลุ่ม 👉',Group)
    st.write('✅ ข้อแนะนำเบื้องต้น :',suggestion)

expander = st.expander("See all records")
with expander:
    st.write(f"Open original [Google Sheet]({GSHEET_URL})")
    st.dataframe(get_data(gsheet_connector))
