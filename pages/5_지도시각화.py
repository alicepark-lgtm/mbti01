import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import os

st.set_page_config(page_title="안산시 인구 마커 지도", layout="wide")

st.title("🗺️ 안산시 행정동별 인구 공간 분포 지도")
st.markdown("안산시 행정동의 지리적 위치 좌표와 2025년 기준 주민등록인구 데이터를 결합하여 시각화합니다.")

# 데이터 무결성을 위한 위경도 좌표 및 구 정보 사전 정의
COORDINATES = {
    # 상록구 (기본 테마: 파란색 계열)
    "일동": {"구": "상록구", "위도": 37.3075, "경도": 126.8647},  # 💡 오타 수정 완료! ("경度" -> "경도")
    "이동": {"구": "상록구", "위도": 37.3069, "경도": 126.8539},
    "사동": {"구": "상록구", "위도": 37.2922, "경도": 126.8664},
    "사이동": {"구": "상록구", "위도": 37.2847, "경도": 126.8586},
    "해양동": {"구": "상록구", "위도": 37.2894, "경도": 126.8436},
    "본오1동": {"구": "상록구", "위도": 37.2922, "경도": 126.8778},
    "본오2동": {"구": "상록구", "위도": 37.3006, "경도": 126.8778},
    "본오3동": {"구": "상록구", "위도": 37.3042, "경도": 126.8731},
    "부곡동": {"구": "상록구", "위도": 37.3278, "경도": 126.8631},
    "월피동": {"구": "상록구", "위도": 37.3203, "경도": 126.8517},
    "성포동": {"구": "상록구", "위도": 37.3161, "경도": 126.8458},
    "반월동": {"구": "상록구", "위도": 37.3183, "경도": 126.8997},
    "안산동": {"구": "상록구", "위도": 37.3486, "경도": 126.8903},
    # 단원구 (기본 테마: 빨간색 계열)
    "와동": {"구": "단원구", "위도": 37.3253, "경도": 126.8372},
    "고잔동": {"구": "단원구", "위도": 37.3117, "경도": 126.8344},
    "중앙동": {"구": "단원구", "위度": 37.3150, "경도": 126.8306},
    "호수동": {"구": "단원구", "위도": 37.3003, "경도": 126.8306},
    "원곡동": {"구": "단원구", "위도": 37.3325, "경도": 126.8117},
    "백운동": {"구": "단원구", "위도": 37.3278, "경도": 126.8089},
    "신길동": {"구": "단원구", "위도": 37.3258, "경도": 126.7778},
    "초지동": {"구": "단원구", "위도": 37.3117, "경도": 126.8031},
    "선부1동": {"구": "단원구", "위도": 37.3422, "경도": 126.8208},
    "선부2동": {"구": "단원구", "위도": 37.3381, "경도": 126.8167},
    "선부3동": {"구": "단원구", "위도": 37.3361, "경도": 126.8031},
    "대부동": {"구": "단원구", "위도": 37.2611, "경도": 126.5744}
}

@st.cache_data
def load_and_prepare_data():
    pop_paths = ["population.csv", "data/population.csv"]
    pop_df = None
    
    for path in pop_paths:
        if os.path.exists(path):
            pop_df = pd.read_csv(path, encoding='utf-8-sig')
            break
            
    if pop_df is not None:
        # 전처리 파일의 컬럼명 규격인 'Year', 'Dong', 'Gu' 구조일 경우 리네임
        if "Year" in pop_df.columns:
            pop_df = pop_df.rename(columns={"Year": "연도", "Dong": "동", "Gu": "구", "Total": "총인구수", "Male": "남자인구수", "Female": "여자인구수"})
        
        pop_2025 = pop_df[pop_df["연도"] == 2025].copy()
        
        # 💡 .get() 연산과 안전장치를 사용하여 딕셔너리에 매핑 키가 없거나 오타가 있어도 KeyError가 안 나도록 방어 코딩 적용
        pop_2025["구"] = pop_2025["동"].apply(lambda x: COORDINATES[x]["구"] if x in COORDINATES else "안산시")
        pop_2025["위도"] = pop_2025["동"].apply(lambda x: COORDINATES[x].get("위도") if x in COORDINATES else None)
        pop_2025["경도"] = pop_2025["동"].apply(lambda x: COORDINATES[x].get("경도") if x in COORDINATES else None)
        
        return pop_2025[pop_2025["위도"].notna() & pop_2025["경도"].notna()]
    return None

df = load_and_prepare_data()

if df is not None and not df.empty:
    # 1. 안산시 중심부 좌표로 기본 지도 생성
    m = folium.Map(
        location=[37.315, 126.83],
        zoom_start=12,
        tiles="CartoDB positron"
    )

    # 2. 마커 클러스터 기능 추가
    marker_cluster = MarkerCluster().add_to(m)

    # 3. 데이터프레임을 순회하며 마커 추가
    for _, row in df.iterrows():
        marker_color = "blue" if row["구"] == "상록구" else "red"
        icon_type = "info-sign" if row["구"] == "상록구" else "home"
        
        popup_html = f"""
        <div style="
            font-family: 'Malgun Gothic', sans-serif; 
            width: 180px; 
            padding: 5px;
            border-radius: 8px;
        ">
            <h4 style="margin: 0 0 8px 0; color: #2c3e50; font-size: 14px; border-bottom: 2px solid #34495e; padding-bottom: 4px;">
                📍 {row['구']} {row['동']}
            </h4>
            <table style="width: 100%; font-size: 12px; border-collapse: collapse;">
                <tr style="border-bottom: 1px solid #eee;">
                    <td style="padding: 4px 0; color: #7f8c8d; font-weight: bold;">총인구</td>
                    <td style="padding: 4px 0; text-align: right; font-weight: bold; color: #2980b9;">{int(row['총인구수']):,}명</td>
                </tr>
                <tr style="border-bottom: 1px solid #eee;">
                    <td style="padding: 4px 0; color: #3498db;">👨 남성</td>
                    <td style="padding: 4px 0; text-align: right; color: #2c3e50;">{int(row['남자인구수']):,}명</td>
                </tr>
                <tr>
                    <td style="padding: 4px 0; color: #e74c3c;">👩 여성</td>
                    <td style="padding: 4px 0; text-align: right; color: #2c3e50;">{int(row['여자인구수']):,}명</td>
                </tr>
            </table>
        </div>
        """
        
        folium.Marker(
            location=[row["위도"], row["경도"]],
            popup=folium.Popup(popup_html, max_width=220),
            tooltip=f"<b>{row['구']} {row['동']}</b> (클릭하여 인구 확인)",
            icon=folium.Icon(color=marker_color, icon=icon_type, prefix="glyphicon")
        ).add_to(marker_cluster)

    # 지도를 화면에 렌더링
    st_folium(m, width=900, height=600)
    
    # 하단 데이터 테이블
    with st.expander("📄 지도 플롯 데이터 원본 테이블 보기"):
        st.dataframe(df[["구", "동", "총인구수", "남자인구수", "여자인구수", "위도", "경도"]].reset_index(drop=True), use_container_width=True)
else:
    st.error("⚠️ 'population.csv' 데이터를 불러오지 못했거나 2025년 데이터가 존재하지 않습니다. 전처리 파일을 확인해 주세요.")
