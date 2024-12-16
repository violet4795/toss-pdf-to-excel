import re
import pdfplumber
import pandas as pd

# PDF 파일 경로
pdf_file = r"C:\Users\NHN\Downloads\0925.pdf"

# 날짜 패턴 정의
date_pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"
split_marker = "<SPLIT_MARKER>"  # 특정 텍스트 구분자

# 정규식을 사용하여 거래 내역 필터링 패턴
pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+(\S+)\s+(-?\d{1,3}(,\d{3})*)\s+(-?\d{1,3}(,\d{3})*)\s*(.*)$"
filtered_data = []

# pdfplumber로 PDF 읽기
with pdfplumber.open(pdf_file) as pdf:
    full_text = ""
    
    # PDF의 모든 페이지 텍스트를 하나의 문자열로 결합
    for page in pdf.pages:
        text = page.extract_text()
        # 날짜 패턴을 기준으로 특정 구분자를 추가
        modified_text = re.sub(f"({date_pattern})", split_marker + r"\1", text)
        full_text += modified_text

    # 구분자를 기준으로 데이터를 나누고 각 거래 내역에서 줄바꿈(\n)을 제거
    transactions = re.split(r'<SPLIT_MARKER>|\n+', full_text)
    transactions = [t.replace('\n', ' ').strip() for t in transactions if t.strip()]

    # 각 거래 내역에 대해 정규식 필터링 적용
    for i, transaction in enumerate(transactions):
        # 한 줄 내에서 날짜 형식이 마지막에 있는지 확인
        match = re.search(date_pattern, transaction)
        if match:
            # 날짜 형식을 기준으로 앞쪽은 기타 항목, 뒷쪽은 날짜와 함께 처리
            pre_date_text = transaction[:match.start()].strip()
            date_and_beyond = transaction[match.start():].strip()

            # 날짜 뒤쪽 내용을 정규식으로 필터링
            match = re.match(pattern, date_and_beyond)
            if match:
                # 쉼표가 포함된 금액들을 숫자로 변환
                date_time = match.group(1)
                payment_type = match.group(2)
                amount_spent = match.group(3).replace(",", "")
                balance = match.group(5).replace(",", "")
                other = match.group(7).strip()
                # print(match.group(1),match.group(2),match.group(3),match.group(4), match.group(5), match.group(6), match.group(7))
                # 기타 항목이 비어 있을 경우 이전 줄과 합침
                if not other.strip() and i > 0:
                    prev_transaction = transactions[i-1]
                    other = prev_transaction.strip()

                # 데이터프레임에 추가할 데이터
                filtered_data.append([date_time, payment_type, amount_spent, balance, other])


# print(filtered_data.reverse())
# 데이터프레임으로 변환
df = pd.DataFrame(list(reversed(filtered_data)), columns=["날짜", "결제유형", "금액", "잔액", "내용"])

# 결과를 Excel로 저장
df.to_excel("0925.xlsx", index=False)
