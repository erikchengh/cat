import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 设置页面配置 - 使用暗色主题
st.set_page_config(
    page_title="制药工艺流程对比",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 应用CSS样式 - 暗色专业主题
st.markdown("""
<style>
    /* 全局暗色主题 */
    .main {
        background-color: #0e1117;
        color: #f0f2f6;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0e1117 0%, #1a1d2e 100%);
    }
    
    /* 侧边栏样式 */
    section[data-testid="stSidebar"] {
        background-color: #1a1d2e;
        border-right: 1px solid #2d3746;
    }
    
    /* 标题样式 */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-weight: 600;
    }
    
    /* 文本样式 */
    p, li, div, span {
        color: #e0e0e0 !important;
    }
    
    /* 卡片和容器样式 */
    .stExpander {
        background-color: #1e2130;
        border: 1px solid #2d3746;
        border-radius: 10px;
    }
    
    .stMetric {
        background-color: #1e2130;
        border: 1px solid #2d3746;
        border-radius: 8px;
        padding: 15px;
    }
    
    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    /* 标签页样式 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: #1a1d2e;
        padding: 8px;
        border-radius: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #1e2130;
        border-radius: 6px 6px 0 0;
        padding: 10px 20px;
        border: 1px solid #2d3746;
        color: #b0b0b0;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border: none;
    }
    
    /* 数据表格样式 */
    .dataframe {
        background-color: #1e2130 !important;
        color: #ffffff !important;
    }
    
    .dataframe th {
        background-color: #2d3746 !important;
        color: white !important;
        font-weight: 600;
    }
    
    .dataframe td {
        background-color: #1e2130 !important;
        color: #e0e0e0 !important;
        border-color: #2d3746 !important;
    }
    
    /* 选择框样式 */
    .stSelectbox, .stMultiselect, .stRadio {
        background-color: #1e2130;
        border-radius: 8px;
        padding: 5px;
    }
    
    /* 警告框样式 */
    .stAlert {
        background-color: #2d3746;
        border: 1px solid #667eea;
        border-radius: 8px;
    }
    
    /* 图表容器 */
    .js-plotly-plot {
        background-color: #1e2130 !important;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #2d3746;
    }
    
    /* 自定义卡片 */
    .custom-card {
        background: linear-gradient(135deg, #1e2130 0%, #2d3746 100%);
        border: 1px solid #3a4359;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    
    /* 流程图节点 */
    .process-node {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 8px;
        padding: 10px;
        margin: 5px;
        text-align: center;
        font-weight: 600;
        border: 2px solid rgba(255, 255, 255, 0.1);
    }
    
    /* 工艺步骤样式 */
    .step-card {
        background-color: #1e2130;
        border-left: 4px solid #667eea;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .step-number {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-right: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 应用标题
st.markdown('<h1 style="text-align: center; background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 20px;">⚗️ 制药工艺流程对比</h1>', unsafe_allow_html=True)
st.markdown('<h3 style="text-align: center; color: #b0b0b0; margin-bottom: 30px;">可视化展示不同制药品类的工艺步骤及其差异</h3>', unsafe_allow_html=True)

# 定义详细的制药工艺数据库
class PharmaceuticalProcesses:
    """制药工艺数据库"""
    
    PROCESSES = {
        # 1. 化学药物 - 固体制剂
        "化学药物-固体制剂": {
            "片剂": {
                "description": "最常见的口服固体制剂，通过粉末压缩成型",
                "关键特征": ["剂量准确", "稳定性好", "便于服用"],
                "工艺步骤": [
                    {"name": "原料验收", "关键参数": ["含量", "杂质", "粒度"], "设备": ["天平", "筛分机"], "时间(h)": 2, "温度(℃)": "室温"},
                    {"name": "称配", "关键参数": ["称量精度", "复核确认"], "设备": ["精密天平"], "时间(h)": 1, "温度(℃)": "室温"},
                    {"name": "制粒", "关键参数": ["粘合剂浓度", "搅拌时间", "粒度分布"], "设备": ["湿法制粒机"], "时间(h)": 3, "温度(℃)": "25-35"},
                    {"name": "干燥", "关键参数": ["温度", "时间", "水分含量"], "设备": ["流化床干燥机"], "时间(h)": 4, "温度(℃)": "50-60"},
                    {"name": "整粒", "关键参数": ["筛网目数", "颗粒收率"], "设备": ["整粒机"], "时间(h)": 1, "温度(℃)": "室温"},
                    {"name": "总混", "关键参数": ["混合时间", "均匀度"], "设备": ["三维混合机"], "时间(h)": 2, "温度(℃)": "室温"},
                    {"name": "压片", "关键参数": ["压力", "硬度", "片重差异"], "设备": ["旋转压片机"], "时间(h)": 4, "温度(℃)": "室温"},
                    {"name": "包衣", "关键参数": ["包衣液浓度", "喷雾速率", "温度"], "设备": ["包衣锅"], "时间(h)": 6, "温度(℃)": "40-50"},
                    {"name": "包装", "关键参数": ["密封性", "标签准确性"], "设备": ["泡罩包装机"], "时间(h)": 3, "温度(℃)": "室温"}
                ]
            },
            
            "胶囊剂": {
                "description": "药物封装在明胶或植物胶囊中",
                "关键特征": ["掩盖不良味道", "提高生物利用度", "便于个性化"],
                "工艺步骤": [
                    {"name": "原料处理", "关键参数": ["粒度", "流动性"], "设备": ["粉碎机", "筛分机"], "时间(h)": 2, "温度(℃)": "室温"},
                    {"name": "称配", "关键参数": ["称量精度"], "设备": ["精密天平"], "时间(h)": 1, "温度(℃)": "室温"},
                    {"name": "混合", "关键参数": ["混合均匀度"], "设备": ["V型混合机"], "时间(h)": 2, "温度(℃)": "室温"},
                    {"name": "胶囊填充", "关键参数": ["装量差异", "锁合完整性"], "设备": ["全自动胶囊填充机"], "时间(h)": 4, "温度(℃)": "20-25"},
                    {"name": "抛光", "关键参数": ["外观", "清洁度"], "设备": ["胶囊抛光机"], "时间(h)": 1, "温度(℃)": "室温"},
                    {"name": "检查", "关键参数": ["外观", "重量差异"], "设备": ["胶囊检查机"], "时间(h)": 2, "温度(℃)": "室温"},
                    {"name": "包装", "关键参数": ["密封性", "防潮性"], "设备": ["装瓶机"], "时间(h)": 3, "温度(℃)": "室温"}
                ]
            },
            
            "颗粒剂": {
                "description": "药物与辅料制成的干燥颗粒状制剂",
                "关键特征": ["分散性好", "剂量准确", "便于儿童服用"],
                "工艺步骤": [
                    {"name": "原料处理", "关键参数": ["粒度", "水分"], "设备": ["粉碎机"], "时间(h)": 2, "温度(℃)": "室温"},
                    {"name": "称配", "关键参数": ["配比准确性"], "设备": ["台秤"], "时间(h)": 1, "温度(℃)": "室温"},
                    {"name": "制粒", "关键参数": ["粒度分布", "收率"], "设备": ["干法制粒机"], "时间(h)": 3, "温度(℃)": "室温"},
                    {"name": "整粒", "关键参数": ["颗粒均匀度"], "设备": ["振荡筛"], "时间(h)": 1, "温度(℃)": "室温"},
                    {"name": "总混", "关键参数": ["混合均匀度"], "设备": ["双锥混合机"], "时间(h)": 2, "温度(℃)": "室温"},
                    {"name": "分装", "关键参数": ["装量差异"], "设备": ["自动分装机"], "时间(h)": 3, "温度(℃)": "室温"},
                    {"name": "包装", "关键参数": ["密封性"], "设备": ["袋包装机"], "时间(h)": 2, "温度(℃)": "室温"}
                ]
            }
        },
        
        # 2. 化学药物 - 半固体制剂
        "化学药物-半固体制剂": {
            "软膏剂": {
                "description": "药物与油脂性或水溶性基质混合制成的半固体制剂",
                "关键特征": ["局部给药", "缓释作用", "保护创面"],
                "工艺步骤": [
                    {"name": "基质处理", "关键参数": ["熔点", "纯净度"], "设备": ["加热罐"], "时间(h)": 2, "温度(℃)": "70-80"},
                    {"name": "药物分散", "关键参数": ["分散均匀度", "粒度"], "设备": ["胶体磨"], "时间(h)": 3, "温度(℃)": "60-70"},
                    {"name": "均质乳化", "关键参数": ["乳化时间", "温度", "pH值"], "设备": ["均质乳化机"], "时间(h)": 4, "温度(℃)": "60-70"},
                    {"name": "脱气", "关键参数": ["气泡含量"], "设备": ["真空脱气罐"], "时间(h)": 1, "温度(℃)": "50-60"},
                    {"name": "灌装", "关键参数": ["装量差异", "密封性"], "设备": ["软膏灌装机"], "时间(h)": 3, "温度(℃)": "40-50"},
                    {"name": "包装", "关键参数": ["密封完整性"], "设备": ["旋盖机"], "时间(h)": 2, "温度(℃)": "室温"}
                ]
            },
            
            "凝胶剂": {
                "description": "药物与亲水性基质制成的透明或半透明半固体制剂",
                "关键特征": ["生物相容性好", "透皮吸收", "美观"],
                "工艺步骤": [
                    {"name": "基质制备", "关键参数": ["粘度", "透明度"], "设备": ["搅拌罐"], "时间(h)": 2, "温度(℃)": "室温"},
                    {"name": "药物溶解", "关键参数": ["溶解度", "稳定性"], "设备": ["溶解罐"], "time(h)": 3, "温度(℃)": "室温"},
                    {"name": "混合", "关键参数": ["混合均匀度"], "设备": ["行星搅拌机"], "时间(h)": 4, "温度(℃)": "室温"},
                    {"name": "脱泡", "关键参数": ["气泡消除"], "设备": ["真空脱泡机"], "时间(h)": 1, "温度(℃)": "室温"},
                    {"name": "灌装", "关键参数": ["装量精度"], "设备": ["凝胶灌装机"], "时间(h)": 3, "温度(℃)": "室温"},
                    {"name": "包装", "关键参数": ["密封性"], "设备": ["铝管封尾机"], "时间(h)": 2, "温度(℃)": "室温"}
                ]
            }
        },
        
        # 3. 化学药物 - 液体制剂
        "化学药物-液体制剂": {
            "注射剂": {
                "description": "供注入体内的无菌制剂",
                "关键特征": ["起效迅速", "生物利用度高", "无菌要求严格"],
                "工艺步骤": [
                    {"name": "配液", "关键参数": ["浓度", "pH值", "澄明度"], "设备": ["配液罐"], "时间(h)": 3, "温度(℃)": "20-25"},
                    {"name": "过滤", "关键参数": ["滤器完整性", "除菌效果"], "设备": ["除菌过滤器"], "时间(h)": 1, "温度(℃)": "20-25"},
                    {"name": "灌封", "关键参数": ["灌装精度", "密封性"], "设备": ["洗烘灌封联动线"], "时间(h)": 4, "温度(℃)": "20-25"},
                    {"name": "灭菌", "关键参数": ["温度", "时间", "F0值"], "设备": ["蒸汽灭菌柜"], "时间(h)": 2, "温度(℃)": "121"},
                    {"name": "灯检", "关键参数": ["可见异物"], "设备": ["自动灯检机"], "时间(h)": 3, "温度(℃)": "室温"},
                    {"name": "贴签包装", "关键参数": ["标签准确性", "密封性"], "设备": ["贴标机"], "时间(h)": 2, "温度(℃)": "室温"}
                ]
            },
            
            "口服液": {
                "description": "供口服的液体制剂",
                "关键特征": ["吸收快", "便于儿童老人服用"],
                "工艺步骤": [
                    {"name": "药材提取", "关键参数": ["提取率", "有效成分"], "设备": ["提取罐"], "时间(h)": 6, "温度(℃)": "80-90"},
                    {"name": "过滤浓缩", "关键参数": ["澄清度", "相对密度"], "设备": ["真空浓缩器"], "时间(h)": 4, "温度(℃)": "60-70"},
                    {"name": "配制", "关键参数": ["pH值", "糖度"], "设备": ["配液罐"], "时间(h)": 2, "温度(℃)": "室温"},
                    {"name": "过滤", "关键参数": ["澄明度"], "设备": ["板框过滤器"], "时间(h)": 1, "温度(℃)": "室温"},
                    {"name": "灌装", "关键参数": ["装量差异"], "设备": ["液体灌装机"], "时间(h)": 3, "温度(℃)": "室温"},
                    {"name": "灭菌", "关键参数": ["温度", "时间"], "设备": ["水浴灭菌柜"], "时间(h)": 1, "温度(℃)": "100"},
                    {"name": "包装", "关键参数": ["密封完整性"], "设备": ["旋盖机"], "时间(h)": 2, "温度(℃)": "室温"}
                ]
            }
        },
        
        # 4. 生物制品
        "生物制品": {
            "疫苗": {
                "description": "用于预防疾病的生物制品",
                "关键特征": ["免疫原性", "安全性", "稳定性"],
                "工艺步骤": [
                    {"name": "细胞培养", "关键参数": ["细胞密度", "活力", "无菌"], "设备": ["生物反应器"], "时间(天)": 7, "温度(℃)": "37"},
                    {"name": "病毒接种", "关键参数": ["MOI", "感染时间"], "设备": ["无菌操作台"], "时间(h)": 2, "温度(℃)": "37"},
                    {"name": "病毒收获", "关键参数": ["病毒滴度", "收获时间"], "设备": ["连续流离心机"], "时间(h)": 4, "温度(℃)": "4"},
                    {"name": "纯化", "关键参数": ["纯度", "回收率"], "设备": ["层析系统"], "时间(天)": 2, "温度(℃)": "4-8"},
                    {"name": "灭活/减毒", "关键参数": ["灭活率", "免疫原性"], "设备": ["灭活罐"], "时间(h)": 24, "温度(℃)": "37"},
                    {"name": "配制", "关键参数": ["抗原含量", "佐剂比例"], "设备": ["配制罐"], "时间(h)": 6, "温度(℃)": "2-8"},
                    {"name": "无菌过滤", "关键参数": ["无菌保证"], "设备": ["除菌过滤器"], "时间(h)": 2, "温度(℃)": "室温"},
                    {"name": "灌装", "关键参数": ["灌装精度", "无菌操作"], "设备": ["隔离器灌装线"], "时间(h)": 8, "温度(℃)": "室温"},
                    {"name": "冻干", "关键参数": ["水分", "外观"], "设备": ["冷冻干燥机"], "时间(天)": 3, "温度(℃)": "-40~25"},
                    {"name": "包装", "关键参数": ["冷链管理"], "设备": ["自动包装线"], "时间(h)": 4, "温度(℃)": "2-8"}
                ]
            },
            
            "单克隆抗体": {
                "description": "由单一B细胞克隆产生的抗体",
                "关键特征": ["高特异性", "高纯度", "工艺复杂"],
                "工艺步骤": [
                    {"name": "细胞库复苏", "关键参数": ["细胞活力", "无菌"], "设备": ["液氮罐"], "时间(天)": 3, "温度(℃)": "37"},
                    {"name": "摇瓶培养", "关键参数": ["细胞密度", "活力"], "设备": ["摇床"], "时间(天)": 5, "温度(℃)": "37"},
                    {"name": "生物反应器培养", "关键参数": ["DO", "pH", "细胞密度"], "设备": ["不锈钢生物反应器"], "时间(天)": 14, "温度(℃)": "37"},
                    {"name": "收获", "关键参数": ["抗体浓度", "收获时间"], "设备": ["切向流过滤系统"], "时间(h)": 8, "温度(℃)": "4"},
                    {"name": "Protein A亲和层析", "关键参数": ["结合容量", "洗脱条件"], "设备": ["AKTA层析系统"], "时间(天)": 2, "温度(℃)": "4-8"},
                    {"name": "低pH病毒灭活", "关键参数": ["pH值", "灭活时间"], "设备": ["灭活罐"], "时间(h)": 2, "温度(℃)": "室温"},
                    {"name": "离子交换层析", "关键参数": ["纯度", "收率"], "设备": ["层析系统"], "时间(天)": 2, "温度(℃)": "4-8"},
                    {"name": "超滤浓缩", "关键参数": ["浓度", "收率"], "设备": ["切向流超滤系统"], "时间(h)": 6, "温度(℃)": "4-8"},
                    {"name": "无菌过滤", "关键参数": ["无菌保证"], "设备": ["除菌过滤器"], "时间(h)": 2, "温度(℃)": "室温"},
                    {"name": "灌装", "关键参数": ["灌装精度"], "设备": ["西林瓶灌装线"], "时间(h)": 8, "温度(℃)": "室温"},
                    {"name": "冻干", "关键参数": ["水分", "复溶性"], "设备": ["冷冻干燥机"], "时间(天)": 3, "温度(℃)": "-40~25"},
                    {"name": "包装", "关键参数": ["密封完整性"], "设备": ["轧盖机"], "时间(h)": 4, "温度(℃)": "室温"}
                ]
            }
        },
        
        # 5. 中药制剂
        "中药制剂": {
            "中药片剂": {
                "description": "中药提取物与辅料压制而成的片剂",
                "关键特征": ["携带方便", "剂量准确", "质量稳定"],
                "工艺步骤": [
                    {"name": "药材前处理", "关键参数": ["净选", "切割规格"], "设备": ["洗药机", "切药机"], "时间(h)": 4, "温度(℃)": "室温"},
                    {"name": "提取", "关键参数": ["溶剂", "温度", "时间"], "设备": ["多功能提取罐"], "时间(h)": 8, "温度(℃)": "80-90"},
                    {"name": "浓缩", "关键参数": ["相对密度", "温度"], "设备": ["真空浓缩器"], "时间(h)": 6, "温度(℃)": "60-70"},
                    {"name": "干燥", "关键参数": ["水分", "粒度"], "设备": ["喷雾干燥塔"], "时间(h)": 4, "温度(℃)": "80-100"},
                    {"name": "粉碎过筛", "关键参数": ["粒度分布"], "设备": ["粉碎机", "振荡筛"], "时间(h)": 3, "温度(℃)": "室温"},
                    {"name": "制粒", "关键参数": ["颗粒性状", "水分"], "设备": ["湿法制粒机"], "时间(h)": 4, "温度(℃)": "室温"},
                    {"name": "压片", "关键参数": ["片重差异", "硬度"], "设备": ["旋转压片机"], "时间(h)": 5, "温度(℃)": "室温"},
                    {"name": "包衣", "关键参数": ["增重", "外观"], "设备": ["高效包衣锅"], "时间(h)": 6, "温度(℃)": "40-50"},
                    {"name": "包装", "关键参数": ["密封防潮"], "设备": ["铝塑包装机"], "时间(h)": 3, "温度(℃)": "室温"}
                ]
            }
        },
        
        # 6. 新型制剂
        "新型制剂": {
            "脂质体": {
                "description": "药物包封于类脂质双分子层中形成的微型泡囊",
                "关键特征": ["靶向性", "缓释性", "降低毒性"],
                "工艺步骤": [
                    {"name": "脂质膜制备", "关键参数": ["磷脂比例", "成膜均匀性"], "设备": ["旋转蒸发仪"], "时间(h)": 3, "温度(℃)": "40-50"},
                    {"name": "水化", "关键参数": ["温度", "水化时间"], "设备": ["水浴超声仪"], "时间(h)": 2, "温度(℃)": "50-60"},
                    {"name": "载药", "关键参数": ["包封率", "载药量"], "设备": ["载药装置"], "时间(h)": 4, "温度(℃)": "50-60"},
                    {"name": "挤出均质", "关键参数": ["压力", "循环次数", "粒径"], "设备": ["挤出器"], "时间(h)": 3, "温度(℃)": "室温"},
                    {"name": "纯化", "关键参数": ["分离效率"], "设备": ["柱层析系统"], "时间(h)": 6, "温度(℃)": "4-8"},
                    {"name": "除菌过滤", "关键参数": ["无菌保证"], "设备": ["0.22μm滤器"], "时间(h)": 1, "温度(℃)": "室温"},
                    {"name": "灌装", "关键参数": ["灌装精度"], "设备": ["灌装机"], "时间(h)": 3, "温度(℃)": "室温"},
                    {"name": "冻干", "关键参数": ["冻干曲线", "复溶性"], "设备": ["冷冻干燥机"], "时间(天)": 2, "温度(℃)": "-40~25"},
                    {"name": "包装", "关键参数": ["密封性"], "设备": ["轧盖机"], "时间(h)": 2, "温度(℃)": "室温"}
                ]
            }
        }
    }
    
    @staticmethod
    def get_main_categories():
        return list(PharmaceuticalProcesses.PROCESSES.keys())
    
    @staticmethod
    def get_products(main_category):
        return list(PharmaceuticalProcesses.PROCESSES.get(main_category, {}).keys())
    
    @staticmethod
    def get_product_info(main_category, product):
        return PharmaceuticalProcesses.PROCESSES.get(main_category, {}).get(product, {})

# 辅助方法
def classify_parameter(param_name):
    param_lower = param_name.lower()
    if any(word in param_lower for word in ['温度', '压力', 'ph', '浓度']):
        return "物理化学参数"
    elif any(word in param_lower for word in ['时间', '速率', '速度']):
        return "过程控制参数"
    elif any(word in param_lower for word in ['含量', '纯度', '杂质']):
        return "质量参数"
    elif any(word in param_lower for word in ['收率', '效率', '产量']):
        return "经济性参数"
    else:
        return "其他参数"

def assess_importance(param_name):
    param_lower = param_name.lower()
    if any(word in param_lower for word in ['无菌', '灭菌', '病毒', '安全']):
        return 5
    elif any(word in param_lower for word in ['含量', '纯度', '关键质量']):
        return 4
    elif any(word in param_lower for word in ['温度', '时间', 'ph']):
        return 3
    else:
        return 2

def classify_equipment(equip_name):
    equip_lower = equip_name.lower()
    if any(word in equip_lower for word in ['反应器', '发酵罐', '生物']):
        return "生物反应设备"
    elif any(word in equip_lower for word in ['离心', '过滤', '层析', '纯化']):
        return "分离纯化设备"
    elif any(word in equip_lower for word in ['干燥', '浓缩', '蒸发']):
        return "干燥浓缩设备"
    elif any(word in equip_lower for word in ['混合', '搅拌', '制粒']):
        return "混合制备设备"
    elif any(word in equip_lower for word in ['灌装', '包装', '贴标']):
        return "灌装包装设备"
    elif any(word in equip_lower for word in ['灭菌', '消毒']):
        return "灭菌消毒设备"
    else:
        return "其他设备"

# 侧边栏配置
with st.sidebar:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('### ⚙️ 配置选项')
    
    mode = st.radio(
        "选择查看模式",
        ["单一产品详情", "多产品对比", "分类概览"],
        index=0
    )
    
    st.markdown("---")
    
    if mode == "单一产品详情":
        st.markdown('#### 选择产品')
        main_categories = PharmaceuticalProcesses.get_main_categories()
        selected_main = st.selectbox("选择药品主分类", main_categories, index=0)
        
        if selected_main:
            products = PharmaceuticalProcesses.get_products(selected_main)
            selected_product = st.selectbox("选择具体产品", products, index=0)
            
            product_info = PharmaceuticalProcesses.get_product_info(selected_main, selected_product)
            if product_info:
                with st.expander("📝 产品简介"):
                    st.write(f"**描述**: {product_info.get('description', '')}")
                    st.write("**关键特征**:")
                    for feature in product_info.get("关键特征", []):
                        st.write(f"- {feature}")
    
    elif mode == "多产品对比":
        st.markdown('#### 选择对比产品')
        all_products = []
        for main_cat in PharmaceuticalProcesses.get_main_categories():
            for product in PharmaceuticalProcesses.get_products(main_cat):
                all_products.append(f"{main_cat} | {product}")
        
        selected_comparison = st.multiselect(
            "选择要对比的产品（最多6个）",
            all_products,
            default=all_products[:3] if len(all_products) >= 3 else all_products
        )
        
        if len(selected_comparison) > 6:
            st.warning("最多选择6个产品进行对比")
            selected_comparison = selected_comparison[:6]
    
    else:
        st.markdown('#### 分类概览设置')
        overview_type = st.selectbox(
            "概览类型",
            ["工艺步骤数对比", "工艺复杂度雷达图", "设备需求对比"]
        )
    
    st.markdown("---")
    st.caption("💡 提示：点击不同标签页查看详细信息")
    st.markdown('</div>', unsafe_allow_html=True)

# 主显示区域
if mode == "单一产品详情":
    if 'selected_main' in locals() and 'selected_product' in locals():
        product_info = PharmaceuticalProcesses.get_product_info(selected_main, selected_product)
        
        if product_info:
            # 产品标题
            st.markdown(f'<div class="custom-card"><h2>🔬 {selected_product} 生产工艺流程</h2><p>所属分类: {selected_main}</p></div>', unsafe_allow_html=True)
            
            # 创建标签页
            tab1, tab2, tab3, tab4 = st.tabs(["📋 工艺步骤详情", "🔧 关键参数分析", "🏭 设备需求", "📊 工艺流程图"])
            
            with tab1:
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                st.subheader("工艺步骤详解")
                steps = product_info.get("工艺步骤", [])
                
                for i, step in enumerate(steps, 1):
                    with st.expander(f"步骤{i}: {step['name']}", expanded=(i==1)):
                        col1, col2, col3 = st.columns([2, 2, 1])
                        
                        with col1:
                            st.markdown("**关键参数:**")
                            for param in step.get("关键参数", []):
                                st.write(f"• {param}")
                        
                        with col2:
                            st.markdown("**主要设备:**")
                            for equip in step.get("设备", []):
                                st.write(f"• {equip}")
                        
                        with col3:
                            # 工艺条件
                            if "时间" in step:
                                st.metric("工艺时间", step.get("时间", ""))
                            if "温度" in step:
                                st.metric("工艺温度", step.get("温度", ""))
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # 工艺统计
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                st.subheader("工艺统计")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("总步骤数", len(steps))
                
                with col2:
                    total_params = sum(len(step.get("关键参数", [])) for step in steps)
                    st.metric("关键参数总数", total_params)
                
                with col3:
                    all_equipment = set()
                    for step in steps:
                        all_equipment.update(step.get("设备", []))
                    st.metric("设备种类数", len(all_equipment))
                
                with col4:
                    total_time = sum(float(str(step.get("时间", "0")).replace("(h)", "").replace("(天)", "")) 
                                   for step in steps if "时间" in step)
                    st.metric("总工艺时间", f"{total_time:.1f} 小时")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with tab2:
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                st.subheader("关键参数分析")
                steps = product_info.get("工艺步骤", [])
                all_params = []
                
                for step in steps:
                    for param in step.get("关键参数", []):
                        all_params.append({
                            "参数名称": param,
                            "所属步骤": step["name"],
                            "参数类型": classify_parameter(param),
                            "重要程度": assess_importance(param)
                        })
                
                if all_params:
                    params_df = pd.DataFrame(all_params)
                    
                    # 优化饼图颜色 - 使用高对比度配色
                    param_counts = params_df["参数类型"].value_counts()
                    
                    # 使用暗色主题友好的颜色
                    colors = ['#636efa', '#ef553b', '#00cc96', '#ab63fa', '#ffa15a']
                    
                    fig1 = px.pie(
                        values=param_counts.values,
                        names=param_counts.index,
                        title="关键参数类型分布",
                        color_discrete_sequence=colors
                    )
                    
                    # 更新饼图样式为暗色主题
                    fig1.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font_color='white',
                        title_font_color='white',
                        legend_font_color='white'
                    )
                    
                    fig1.update_traces(
                        textfont_color='white',
                        marker=dict(line=dict(color='#2d3746', width=2))
                    )
                    
                    st.plotly_chart(fig1, use_container_width=True)
                    
                    # 参数详情表格
                    st.write("### 参数详情")
                    st.dataframe(
                        params_df,
                        column_config={
                            "参数名称": st.column_config.TextColumn("参数名称"),
                            "所属步骤": st.column_config.TextColumn("所属步骤"),
                            "参数类型": st.column_config.TextColumn("参数类型"),
                            "重要程度": st.column_config.ProgressColumn(
                                "重要程度",
                                min_value=1,
                                max_value=5
                            )
                        },
                        use_container_width=True
                    )
                st.markdown('</div>', unsafe_allow_html=True)
            
            with tab3:
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                st.subheader("设备需求分析")
                steps = product_info.get("工艺步骤", [])
                equipment_data = []
                
                for step in steps:
                    for equip in step.get("设备", []):
                        equipment_data.append({
                            "设备名称": equip,
                            "使用步骤": step["name"],
                            "设备类型": classify_equipment(equip),
                            "使用频率": 1
                        })
                
                if equipment_data:
                    equip_df = pd.DataFrame(equipment_data)
                    
                    # 优化柱状图颜色
                    equip_type_counts = equip_df["设备类型"].value_counts()
                    
                    fig2 = px.bar(
                        x=equip_type_counts.index,
                        y=equip_type_counts.values,
                        title="设备类型分布",
                        labels={"x": "设备类型", "y": "使用次数"},
                        color=equip_type_counts.index,
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    
                    # 更新柱状图样式为暗色主题
                    fig2.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font_color='white',
                        title_font_color='white',
                        xaxis=dict(gridcolor='#2d3746'),
                        yaxis=dict(gridcolor='#2d3746')
                    )
                    
                    st.plotly_chart(fig2, use_container_width=True)
                    
                    # 详细设备列表
                    st.write("### 详细设备清单")
                    equip_summary = equip_df.groupby("设备名称").agg({
                        "设备类型": "first",
                        "使用频率": "sum",
                        "使用步骤": lambda x: ", ".join(x)
                    }).reset_index()
                    
                    st.dataframe(
                        equip_summary,
                        column_config={
                            "设备名称": st.column_config.TextColumn("设备名称"),
                            "设备类型": st.column_config.TextColumn("设备类型"),
                            "使用频率": st.column_config.NumberColumn("使用次数"),
                            "使用步骤": st.column_config.TextColumn("使用步骤", width="large")
                        },
                        use_container_width=True
                    )
                st.markdown('</div>', unsafe_allow_html=True)
            
            with tab4:
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                st.subheader("工艺流程图")
                steps = product_info.get("工艺步骤", [])
                
                # 创建优化的流程图 - 使用Plotly
                fig = go.Figure()
                
                # 计算节点位置
                num_steps = len(steps)
                x_positions = [i/(num_steps-1) if num_steps > 1 else 0.5 for i in range(num_steps)]
                y_position = 0.5
                
                # 定义节点颜色方案
                node_colors = ['#636efa', '#ef553b', '#00cc96', '#ab63fa', '#ffa15a', 
                              '#19d3f3', '#ff6692', '#b6e880', '#ff97ff', '#fecb52']
                
                # 添加节点
                for i, step in enumerate(steps):
                    color_idx = i % len(node_colors)
                    
                    # 添加主要节点
                    fig.add_trace(go.Scatter(
                        x=[x_positions[i]],
                        y=[y_position],
                        mode="markers+text",
                        marker=dict(
                            size=40,
                            color=node_colors[color_idx],
                            line=dict(width=3, color='white')
                        ),
                        text=[f"{i+1}"],
                        textposition="middle center",
                        textfont=dict(size=14, color="white", family="Arial Black"),
                        name=step["name"],
                        hoverinfo="text",
                        hovertext=f"<b>{step['name']}</b><br>关键参数: {', '.join(step.get('关键参数', []))}<br>设备: {', '.join(step.get('设备', []))}"
                    ))
                    
                    # 添加步骤名称标签
                    fig.add_annotation(
                        x=x_positions[i],
                        y=y_position - 0.15,
                        text=step["name"],
                        showarrow=False,
                        font=dict(size=12, color="#e0e0e0", family="Arial"),
                        yref="y"
                    )
                
                # 添加工艺连接线
                for i in range(num_steps - 1):
                    fig.add_trace(go.Scatter(
                        x=[x_positions[i] + 0.03, x_positions[i+1] - 0.03],
                        y=[y_position, y_position],
                        mode="lines",
                        line=dict(width=3, color='#667eea', dash='solid'),
                        hoverinfo="none",
                        showlegend=False
                    ))
                    
                    # 添加流向箭头
                    mid_x = (x_positions[i] + x_positions[i+1]) / 2
                    fig.add_annotation(
                        x=mid_x,
                        y=y_position,
                        ax=mid_x - 0.02,
                        ay=y_position,
                        xref="x",
                        yref="y",
                        axref="x",
                        ayref="y",
                        showarrow=True,
                        arrowhead=3,
                        arrowsize=1.5,
                        arrowwidth=2,
                        arrowcolor="#ffffff"
                    )
                
                # 添加工艺开始和结束标记
                fig.add_annotation(
                    x=-0.05,
                    y=y_position,
                    text="🏁 开始",
                    showarrow=False,
                    font=dict(size=14, color="#00cc96", family="Arial Black"),
                    xref="paper"
                )
                
                fig.add_annotation(
                    x=1.05,
                    y=y_position,
                    text="✅ 完成",
                    showarrow=False,
                    font=dict(size=14, color="#00cc96", family="Arial Black"),
                    xref="paper"
                )
                
                # 更新布局 - 优化暗色主题
                fig.update_layout(
                    title=dict(
                        text=f"{selected_product} 工艺流程图",
                        font=dict(size=20, color="white", family="Arial Black"),
                        x=0.5,
                        xanchor="center"
                    ),
                    height=400,
                    showlegend=False,
                    xaxis=dict(
                        showgrid=False,
                        zeroline=False,
                        showticklabels=False,
                        range=[-0.15, 1.15]
                    ),
                    yaxis=dict(
                        showgrid=False,
                        zeroline=False,
                        showticklabels=False,
                        range=[0, 1]
                    ),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=50, r=50, t=80, b=50),
                    hoverlabel=dict(
                        bgcolor="#1e2130",
                        font_size=12,
                        font_color="white"
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # 流程图说明
                st.info("""
                **流程图说明:**
                - 🔵 每个彩色圆点代表一个工艺步骤，数字表示步骤顺序
                - ⬇️ 下方文字显示步骤名称
                - ⬅️ 箭头表示工艺流向
                - 💡 悬停在圆点上查看详细参数和设备信息
                - 🏁 左侧为工艺开始，✅ 右侧为工艺完成
                """)
                st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        st.info("请在侧边栏选择产品和分类")

elif mode == "多产品对比":
    st.header("📊 多产品工艺对比分析")
    
    if 'selected_comparison' in locals() and selected_comparison:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.subheader("产品基本信息对比")
        
        # 这里简化对比逻辑，重点展示工艺差异
        comparison_data = []
        for product_path in selected_comparison:
            parts = product_path.split(" | ")
            if len(parts) == 2:
                main_cat, product = parts
                product_info = PharmaceuticalProcesses.get_product_info(main_cat, product)
                if product_info:
                    steps = product_info.get("工艺步骤", [])
                    comparison_data.append({
                        "产品名称": product,
                        "所属分类": main_cat,
                        "工艺步骤数": len(steps),
                        "关键参数总数": sum(len(step.get("关键参数", [])) for step in steps),
                        "设备种类数": len(set([equip for step in steps for equip in step.get("设备", [])]))
                    })
        
        if comparison_data:
            comparison_df = pd.DataFrame(comparison_data)
            
            # 显示对比表格
            st.dataframe(
                comparison_df,
                column_config={
                    "产品名称": st.column_config.TextColumn("产品名称"),
                    "所属分类": st.column_config.TextColumn("所属分类"),
                    "工艺步骤数": st.column_config.NumberColumn("工艺步骤数"),
                    "关键参数总数": st.column_config.NumberColumn("关键参数总数"),
                    "设备种类数": st.column_config.NumberColumn("设备种类数")
                },
                use_container_width=True,
                hide_index=True
            )
            
            # 创建对比图表
            col1, col2 = st.columns(2)
            
            with col1:
                fig1 = px.bar(
                    comparison_df,
                    x="产品名称",
                    y="工艺步骤数",
                    color="所属分类",
                    title="各产品工艺步骤数对比",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                
                fig1.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    title_font_color='white'
                )
                
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                fig2 = px.scatter(
                    comparison_df,
                    x="关键参数总数",
                    y="设备种类数",
                    size="工艺步骤数",
                    color="所属分类",
                    text="产品名称",
                    title="复杂度分析",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                
                fig2.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    title_font_color='white'
                )
                
                st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        st.info("请在侧边栏选择要对比的产品")

else:  # 分类概览
    st.header("🌐 制药品类工艺概览")
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    
    # 获取所有产品数据
    all_products_data = []
    for main_cat in PharmaceuticalProcesses.get_main_categories():
        for product in PharmaceuticalProcesses.get_products(main_cat):
            product_info = PharmaceuticalProcesses.get_product_info(main_cat, product)
            if product_info:
                steps = product_info.get("工艺步骤", [])
                all_products_data.append({
                    "产品": product,
                    "分类": main_cat,
                    "子分类": main_cat.split("-")[-1] if "-" in main_cat else main_cat,
                    "步骤数": len(steps),
                    "关键参数总数": sum(len(step.get("关键参数", [])) for step in steps),
                    "设备种类数": len(set([equip for step in steps for equip in step.get("设备", [])]))
                })
    
    if all_products_data:
        overview_df = pd.DataFrame(all_products_data)
        
        if 'overview_type' in locals() and overview_type == "工艺步骤数对比":
            st.subheader("各品类工艺步骤数对比")
            
            # 创建分类对比图
            category_stats = overview_df.groupby("分类").agg({
                "步骤数": ["mean", "min", "max", "count"]
            }).round(1).reset_index()
            
            category_stats.columns = ["分类", "平均步骤数", "最少步骤数", "最多步骤数", "产品数量"]
            
            fig = px.bar(
                category_stats,
                x="分类",
                y="平均步骤数",
                error_y="最多步骤数",
                title="各分类平均工艺步骤数对比",
                color="分类",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                title_font_color='white'
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# 页脚
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #1a1d2e 0%, #2d3746 100%); border-radius: 10px;'>
        <h3 style='color: #ffffff; margin-bottom: 10px;'>⚗️ 制药工艺流程对比系统</h3>
        <p style='color: #b0b0b0; font-size: 0.9em;'>
            专注于展示不同制药品类的工艺差异 | 数据来源: 制药工艺专业资料整理
        </p>
        <p style='color: #999999; font-size: 0.8em;'>
            版本 2.0 | 优化暗色主题 | 增强可视化效果
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
