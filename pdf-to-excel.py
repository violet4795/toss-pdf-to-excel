import os
from flask import Flask, render_template, request, send_file
import pdfplumber
import pandas as pd
import pdb

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('index.html')

# PDF 파일 업로드 및 변환
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    
    # extract_pdf_data(file)

    # 파일 내용 읽기
    # file_contents = file.read()  # 이 시점에서 파일 내용이 읽혀집니다.
    # print(file_contents)  # 터미널에 출력됨
    
    # # 파일 내용을 다시 처음으로 되돌리기
    # file.seek(0)  # 파일 포인터를 처음으로 돌려야 이후 처리할 때 문제가 생기지 않음
    
    if file.filename == '':
        return 'No selected file'
    
    if file and file.filename.endswith('.pdf'):
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        # PDF를 Excel로 변환
        excel_path = convert_pdf_to_excel(file_path)
        return f'File uploaded and converted successfully. <a href="/download/{os.path.basename(excel_path)}">Download Excel</a>'

# 파일 다운로드
@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return 'File not found'


# PDF를 Excel로 변환하는 함수
def convert_pdf_to_excel(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        all_pages = []
        for page in pdf.pages:
            tables = page.extract_table()
            if tables:
                df = pd.DataFrame(tables[1:], columns=tables[0])
                all_pages.append(df)
    
    if all_pages:
        combined_df = pd.concat(all_pages, ignore_index=True)
        excel_path = os.path.splitext(pdf_path)[0] + '.xlsx'
        combined_df.to_excel(excel_path, index=False)
        return excel_path
    else:
        return 'No tables found in PDF'

if __name__ == '__main__':
    app.run(debug=True)


def extract_pdf_data(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        all_pages = []
        for page in pdf.pages:
            tables = page.extract_table()
            if tables:
                df = pd.DataFrame(tables[1:], columns=tables[0])  # 테이블을 데이터프레임으로 변환
                all_pages.append(df)
    return pd.concat(all_pages, ignore_index=True) if all_pages else None
