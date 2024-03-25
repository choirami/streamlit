#import folium
import streamlit as st

import pandas as pd
import altair as alt
import plotly.express as px
import numpy as np

st.title('환영합니다!')
st.image('https://cdn.pixabay.com/photo/2024/02/27/15/00/peace-8600311_1280.jpg')


st.write('오늘 당신의 하루는 어떠셨나요? 힘들진 않으셨나요?')
st.write("지친 당신을 위한 힐링 영상을 준비했어요.")
st.video("C:/Users/User/Desktop/choi/health/내 프로젝트.mp4")
st.caption('출처 : https://www.youtube.com/watch?v=cOLNoxjOLDE&ab_channel=멸종위기종김한별')
st.write('멍때리게 보게 되고 왜인지 모르게 힘을 얻게 되는 영상이라 몇 년에 한 번씩은 꼭 보는 영상이랍니다! 🍀')

st.header('지친 당신을 위한 랜덤 행운 뽑기!')
st.write('동물들 중 한마리를 골라주세요!')
#button
if st.button('🐇'):
    st.image('https://i.pinimg.com/originals/0b/2a/94/0b2a94df46573abed3dd21b352371c10.jpg')
elif st.button('🦊'):
    st.image('https://i.pinimg.com/564x/49/ef/87/49ef87ba4c373cc606876bc336f4755e.jpg')
elif st.button('🐱'):
    st.image('https://i.pinimg.com/564x/8c/1b/13/8c1b1365a1bb20117d9e6f5e2f2770c1.jpg')
elif st.button('🐯'):
    st.image('https://i.pinimg.com/564x/70/a5/bc/70a5bc8c14ad110dcf2b2b9957b22122.jpg')
else :
    st.write('행운이 곧 당신에게로!')

##아이디어 box
#우울증 체크하는 거 만들자,,,
#몇 년대 표가 궁금하세요?

#나이대별 증상 수
st.divider()

st.header('원본데이터')
st.caption('강보험심사평가원_시군구별 주요 정신질환 통계 2018-2022')

depress= pd.read_csv("C:/Users/User/Desktop/choi/health/depress2022.csv",encoding='cp949')
st.dataframe(depress)



chart = alt.Chart(depress, title='연령대 별 정신 질환 증상 비교').mark_bar().encode(
x='연령구분',y='환자수',color='상별구분')
st.altair_chart(chart, use_container_width=True)

#20에서 29세의 우울증 파이차트를 그려보자.
#어떤 연령의 차트가 궁금하신가요?



age = st.radio('어떤 연령대의 정신 질환 비율이 궁금하신가요?',('10~19세','20~29세','30~39세','40~49세','50~59세','60~69세','70~79세','90~99세','100세 이상'))


pie=depress[(depress['연령구분'] == f'{age}')].groupby(by='상별구분',as_index=False)['환자수'].sum()
fig = px.pie(pie,names="상별구분",values="환자수",title = f'{age}의 정신질환 비율')
fig.update_traces(textposition='inside',textinfo='percent+label+value')
fig.update_layout(font=dict(size=14))
st.plotly_chart(fig)
 
    
    


#서울, 강남구, 등 지도에 찍어도 되겠다 ..!


top10 = depress.groupby(by='시군구',as_index=False)['환자수'].sum().sort_values(by='환자수',ascending=False).head(10)
top10['lat'] = [37.4966645,37.3793356,37.5056205,37.4732933,35.1652494,37.5949159,36.2801669,35.2801669,35.8276369,37.5504483]
top10['lon'] = [127.0629804,127.01060411,127.01152992,126.7886531,127.0312101,129.0430314,126.977339,127.3450306,128.5292473,127.1470117]




# #지도 그리기
my_map=folium.Map(location = [top10['lat'].mean(),top10['lon'].mean()], zoom_start=7)

for index, row in top10.iterrows():
    
    folium.CircleMarker(
    location=[row['lat'],row['lon']],
    radius=row['환자수']/10000,
    color='pink',
    fill=True,
    fill_opacity=0.5).add_to(my_map)
    
    folium.Marker(location=[row['lat'],row['lon']],
                 icon=folium.DivIcon(html=f"<div>{row['시군구']}{row['환자수']}</div>"),).add_to(my_map)
    
st.title('정신 질환 전국 상위 10곳')
st.caption('2018년부터 2022까지 데이터 합산')

# #지도그리기


st.components.v1.html(my_map._repr_html_(),width=800,height=600)
#데이터 프레임 보시겠습니까?
on =st.toggle('DataFrame 보기')
if on:
    st.write(top10)
