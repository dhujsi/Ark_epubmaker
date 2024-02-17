import requests,json,os
from datetime import datetime
from bs4 import BeautifulSoup

def extract_data_from_url(url):
    try:
        # 发送HTTP请求获取页面内容
        #response = requests.get(url)
        # 将提取的数据存储到列表中
        with open(url, 'r', encoding='utf-8') as file:
        # 读取文件内容
            response = file.read()
            response_dict = json.loads(response)

        index_list = {}#完整索引
        story_list=[]#单节
        timeline={}
        char_list=[]#章节/活动
        for char in response_dict.values():#对于每个活动
            act_name=char["name"]#获取活动名
            act_type= char['actType']#获取活动类型
            timeline[act_name]=char["startTime"]#活动名：活动时间添加到时间线
            for story in char["infoUnlockDatas"]:#获取所有小节的集合
                story_id = story['storyTxt'][story['storyTxt'].rfind('/') + 1:]
                story_name = str(story['storyCode']) +" "+ story['storyName'] +" "+ story['avgTag']
                story_list.append({story_id:story_name})#形成整个活动所有小节的集合
            char_content[act_name]=story_list}#活动名：内容 赋值到对应活动类型：{}的中
            
        return index_list, timeline
    except Exception as e:
        print(f"提取数据时出现错误: {e}")
        return []

# 示例用法：
#url = "https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/story_review_table.json"
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'data_file.json')
index_list, timeline = extract_data_from_url(file_path)
current_time = datetime.now().strftime("%Y%m%d")
file_name = f"{current_time}_index.json"
timeline_name=f"{current_time}_timeline.json"
with open(file_name, 'w') as f:
    json.dump( index_list, f, indent=2)
with open(timeline_name, 'w') as f:
    json.dump(timeline, f, indent=2)