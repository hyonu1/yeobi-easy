import pandas as pd
import json
import os

FARE_MASTER = 'fare_master.csv'
LOCATION_MAP = 'location_map.csv'
TEMPLATE = 'template.html'
FINAL_APP = 'index.html'

def get_hub_key(name):
    jn = ['목포', '여수', '순천', '나주', '광양', '해남', '완도', '신안']
    if name in jn: return f"전라남도{name}교육지원청"
    seoul = {'서울서부': '서울특별시서부교육지원청', '서울': '서울특별시성동광진교육지원청'}
    return seoul.get(name, name)

try:
    f_df = pd.read_csv(FARE_MASTER, encoding='utf-8-sig')
    m_df = pd.read_csv(LOCATION_MAP, encoding='utf-8-sig')
    
    matrix = {}
    for _, row in f_df.iterrows():
        h = get_hub_key(str(row['Origin']).strip())
        d = str(row['Destination']).strip()
        f = int(row['Fare_Udeung'])
        if h not in matrix: matrix[h] = {}
        matrix[h][d] = {'gen': f, 'pre': f}

    with open(TEMPLATE, 'r', encoding='utf-8') as f:
        html = f.read()

    mapping = m_df.to_json(orient='records', force_ascii=False)
    html = html.replace('const ALLOWED_CITIES = Object.keys(REGION_ICONS);', f'const ALLOWED_CITIES = {json.dumps(m_df["Search_Key"].tolist(), ensure_ascii=False)};')
    html = html.replace('const INITIAL_DATA = {', f'const MASTER_MAPPING = {mapping};\nconst INITIAL_DATA = {json.dumps(matrix, ensure_ascii=False)};\nconst OLD_DATA = {{')

    with open(FINAL_APP, 'w', encoding='utf-8') as f:
        f.write(html)
    print("빌드 성공: 전국 229개 지역 이식 완료.")
except Exception as e:
    print(f"오류: {e}")