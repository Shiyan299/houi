import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 2. 设置页面标题（显示你的名字，记得替换成自己的）
st.title('California Housing Data (1990) by [你的名字]')

# 3. 读取数据集（确保housing.csv和app.py在同一文件夹）
# 处理可能的编码问题，用encoding='latin-1'兼容多数情况
df = pd.read_csv('housing.csv', encoding='latin-1')

# 4. 侧边栏设置（过滤器都放在侧边栏）
st.sidebar.header('Filter Options')  # 侧边栏标题

# 4.1 位置类型多选项（multiselect）
# 先获取数据中所有的位置类型（ocean_proximity列），去重后作为选项
location_types = df['ocean_proximity'].unique()
selected_locations = st.sidebar.multiselect(
    'Select Location Type',  # 选项标题
    options=location_types,  # 可选的位置类型
    default=location_types  # 默认选中所有类型
)

# 4.2 收入水平单选按钮（radio）
# 按要求分3个收入等级，用if语句过滤数据
income_level = st.sidebar.radio(
    'Select Income Level',  # 选项标题
    options=['Low (≤2.5)', 'Medium (>2.5 & <4.5)', 'High (>4.5)'],  # 收入等级选项
    index=0  # 默认选中第一个（Low）
)

# 根据单选按钮选择过滤数据（核心：用if语句判断收入等级）
if income_level == 'Low (≤2.5)':
    df_filtered = df[df['median_income'] <= 2.5]
elif income_level == 'Medium (>2.5 & <4.5)':
    df_filtered = df[(df['median_income'] > 2.5) & (df['median_income'] < 4.5)]
else:  # High (>4.5)
    df_filtered = df[df['median_income'] > 4.5]

# 4.3 价格滑块（slider）
# 过滤后的数据集的房价范围作为滑块区间，单位是美元
min_price = df_filtered['median_house_value'].min()
max_price = df_filtered['median_house_value'].max()
selected_price = st.sidebar.slider(
    'Minimal Median House Price',  # 滑块标题
    min_value=int(min_price),  # 最小价格（转成整数，避免小数）
    max_value=int(max_price),  # 最大价格
    value=int(min_price)  # 默认值（最小价格）
)

# 最后一步过滤：结合位置类型和选中的最小价格
df_final = df_filtered[
    (df_filtered['ocean_proximity'].isin(selected_locations)) & 
    (df_filtered['median_house_value'] >= selected_price)
]

# 5. 显示地图（Streamlit自带地图功能，用经纬度定位）
st.subheader('Housing Location Map')  # 地图标题
# 地图需要两列：latitude（纬度）和longitude（经度），用median_house_value作为气泡大小
st.map(df_final[['latitude', 'longitude', 'median_house_value']], zoom=6)

# 6. 显示房价直方图（要求30个bin）
st.subheader('Median House Value Distribution')  # 直方图标题
# 设置中文字体（避免matplotlib显示乱码）
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 创建直方图
fig, ax = plt.subplots(figsize=(10, 6))  # 设置图表大小
ax.hist(
    df_final['median_house_value'],  # 要统计的房价数据
    bins=30,  #  bins数量（按要求设为30）
    color='skyblue',  # 柱子颜色
    edgecolor='black'  # 柱子边框颜色（更清晰）
)
# 设置坐标轴标签和标题
ax.set_xlabel('Median House Value (USD)')
ax.set_ylabel('Number of Houses')
ax.set_title('Histogram of Median House Value')

# 在Streamlit中显示直方图
st.pyplot(fig)

# 7. 可选：显示过滤后的数据表格（方便查看具体数据）
if st.checkbox('Show Filtered Data'):  # 勾选框，默认不显示
    st.subheader('Filtered Housing Data')
    st.dataframe(df_final)