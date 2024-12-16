import re
import pdfplumber
import pandas as pd

# PDF 파일 경로
pdf_file = r"C:\Users\NHN\Downloads\0725.pdf"

# 정규 표현식을 사용하여 패턴에 맞는 데이터만 추출
pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+(\S+)\s+(-?\d{1,3}(,\d{3})*)\s+(\d{1,3}(,\d{3})*)\s+(.+)"
filtered_data = []

# pdfplumber로 PDF 읽기
with pdfplumber.open(pdf_file) as pdf:
    for page in pdf.pages:
        text = page.extract_text()  # 페이지에서 텍스트 추출
        for line in text.split('\n'):  # 줄 단위로 분리
            match = re.match(pattern, line)  # 정규 표현식으로 패턴 매칭
            if not match:
              print(match, line)
            if match:
                # 쉼표가 포함된 숫자 열을 다시 합침
                date_time = match.group(1)
                payment_type = match.group(2)
                amount_spent = match.group(3).replace(",", "")
                balance = match.group(5).replace(",", "")
                other = match.group(7)
                filtered_data.append([date_time, payment_type, amount_spent, balance, other])

# 데이터프레임으로 변환
df = pd.DataFrame(filtered_data, columns=["날짜", "결제유형", "소비액", "잔액", "기타"])

# 결과를 Excel로 저장
df.to_excel("filtered_output.xlsx", index=False)
