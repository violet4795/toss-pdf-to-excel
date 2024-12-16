import pdfplumber
import pandas as pd

# PDF 파일에서 테이블 추출
pdf_file = "sample.pdf"
output_excel = "output.xlsx"

# PDF 열기
with pdfplumber.open(pdf_file) as pdf:
    # PDF 페이지 선택 (예: 첫 번째 페이지)
    page = pdf.pages[0]
    
    # 테이블 추출
    table = page.extract_table()
    
    # Pandas DataFrame으로 변환
    df = pd.DataFrame(table[1:], columns=table[0])

    # DataFrame을 Excel 파일로 저장
    df.to_excel(output_excel, index=False)

print(f"PDF에서 데이터를 추출하여 {output_excel} 파일로 저장했습니다.")
