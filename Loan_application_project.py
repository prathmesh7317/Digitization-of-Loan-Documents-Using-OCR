

import pytesseract
import re
import streamlit as st
from PIL import Image
import os

# Set the path of Tesseract to cmd
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\hp\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# Function to extract text using pytesseract
def extract_text_from_image(image):
    return pytesseract.image_to_string(image)

# Function to handle display and text extraction based on file type
def display_file(file, file_type):
    image = Image.open(file)
    st.image(image, caption=f"{file_type} Document", use_column_width=True)
    extracted_text = extract_text_from_image(image)

    if file_type == 'Aadhar':
        aadhar_num = re.search(r"\b\d{4}\s\d{4}\s\d{4}\b", extracted_text)
        aadhar_dob = re.search(r"\b\d{2}/\d{2}/\d{4}\b", extracted_text)
        st.write(f'Aadhar Number: {aadhar_num.group(0) if aadhar_num else "Not found!"}')
        st.write(f'Aadhar DOB: {aadhar_dob.group(0) if aadhar_dob else "Not found!"}')
    elif file_type == 'PAN':
        pan_num = re.search(r"\b[A-Z]{5}\d{4}[A-Z]\b", extracted_text)
        st.write(f'PANCARD Number: {pan_num.group(0) if pan_num else "Not found!"}')
    elif file_type == 'Bank Statement':
        acc_gmail = re.search(r"\b[a-zA-Z0-9.%-]{1,25}[@][a-zA-Z0-9-]{1,15}[.][a-zA-Z]{1,9}\b",extracted_text)
        acc_num = re.search(r"\b\d{12,16}\b", extracted_text)
        st.write(f'Nameholder Gmail ID: {acc_gmail.group(0) if acc_gmail else "Not found!"}')
        st.write(f'Account Number: {acc_num.group(0) if acc_num else "Not found!"}')
    elif file_type == 'Payslip':
        payslip_id = re.search(r"\b\d{4}\b", extracted_text)
        payslip_date = re.search(r"\b\d{2}\/\d{2}\/\d{4}\b", extracted_text)
        st.write(f'Payslip Employee ID: {payslip_id.group(0) if payslip_id else "Not found!"}')
        st.write(f'Payslip Date: {payslip_date.group(0) if payslip_date else "Not found!"}')

# Function to calculate EMI
@st.cache_data
def calculate_emi(principal, rate, period):
    rate = rate / (12 * 100)  # Monthly interest rate
    period = period * 12  # Convert years to months
    emi = (principal * rate * (1 + rate) ** period) / (((1 + rate) ** period) - 1)
    total_payment = emi * period
    total_interest = total_payment - principal
    return emi, total_payment, total_interest

# Function to determine interest rate based on inputs
def determine_interest_rate(loan_amount, credit_score, tenure):
    if credit_score >= 750:
        if loan_amount < 500000:
            return 9.99
        elif loan_amount < 1000000:
            return 10.99
        else:
            return 11.99
    elif credit_score >= 600:
        if loan_amount < 500000:
            return 12.99
        elif loan_amount < 1000000:
            return 14.99
        else:
            return 16.99
    else:
        return 20.0  # Higher rate for lower credit scores

# Application starts here
st.set_page_config(page_title='Personal Loan Application', layout="wide")

# # Display the header first
# st.write("## Personal Loan Application")

# Display the loan information image
st.header("💸Apply for Instant Personal Loan Online of Up To Rs. 40 Lakhs! 🤩🤩")
image_path = r"C:\Users\hp\Downloads\IDFC Loan img QR Code Project.jpg"
if os.path.exists(image_path):
    image = Image.open(image_path)
    st.image(image, caption='Personal Loan', use_column_width=True)
else:
    st.error('Image not found, please check the file path!')

# Introduction to personal loan
st.markdown(""" 
#### 👉👉Fill the Google Form using Above QR Code or Google Form Link: https://forms.gle/rs6iZijhdLJitixL8                       

## Why Choose Our Personal Loan? :

- **Unlock financial freedom** 💸
- **Competitive Interest Rates** 📈 - Enjoy attractive rates to suit your needs.
- **Flexible Repayment Options** 🗓 - Tailor your repayment plan to fit your lifestyle.
- **Quick and Easy Processing** ⏳ - Get approval fast, without the hassle.
- **No Hidden Charges** 🔒 - Transparent terms and conditions with no surprises.
""")

# Sidebar for uploads and inputs from user
st.sidebar.header("📂 Upload Documents")

# Upload Aadhar, PAN, Bank statement, and Payslip
aadhar_file = st.sidebar.file_uploader('Upload Aadhar Document', type=['jpg', 'jpeg', 'png'])
pan_file = st.sidebar.file_uploader('Upload PAN Document', type=['jpg', 'jpeg', 'png'])
bank_statement_file = st.sidebar.file_uploader('Upload Bank Statement', type=['jpg', 'jpeg', 'png'])
payslip_file = st.sidebar.file_uploader('Upload Payslip', type=['jpg', 'jpeg', 'png'])

st.sidebar.header("📱 Personal Loan Calculator")

# Inputs for loan calculator
principal = st.sidebar.number_input('Principal Amount', min_value=0, value=100000, step=5000)
credit_score = st.sidebar.number_input('Credit Score', min_value=300, max_value=850, value=700)
period = st.sidebar.slider('Period (in years)', min_value=1, max_value=10, value=5)

# Automatically determine the interest rate based on inputs
rate = determine_interest_rate(principal, credit_score, period)

if st.sidebar.button('Calculate EMI'):
    with st.spinner('Calculating...'):
        emi, total_payment, total_interest = calculate_emi(principal, rate, period)
        st.sidebar.success(f'Estimated Monthly EMI: ₹ {emi:,.2f}')
        st.sidebar.write(f'Total Payment: ₹ {total_payment:,.2f}')
        st.sidebar.write(f'Total Interest: ₹ {total_interest:,.2f}')
        st.sidebar.write(f'Interest Rate Applied: {rate:.2f}%')

# Submission button to show document results
if st.sidebar.button('Submit Documents'):
    st.write('### Document Results')
    col1, col2 = st.columns(2)

    with col1:
        if aadhar_file:
            display_file(aadhar_file, 'Aadhar')
        if pan_file:
            display_file(pan_file, 'PAN')

    with col2:
        if bank_statement_file:
            display_file(bank_statement_file, 'Bank Statement')
        if payslip_file:
            display_file(payslip_file, 'Payslip')