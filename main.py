from file_parser import Classification_execution, process_folder
import os,requests,json
from ebooklib import epub
def get_index(file_path):
    try:
        url = "https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/story_review_table.json"
        response = requests.get(url,proxies={})
        index_json = response.json()
        return index_json
    except (requests.exceptions.RequestException, ValueError) as e:
        with open(file_path, "rb") as file:
        # 使用二进制模式打开文件，并手动解码文件内容
            file_content = file.read().decode('utf-8')
            index_json = json.loads(file_content)
        return index_json

def generate_folder_structure(index, ark_path ,base_folder="Ark_stories"):
    Main_No= 0
    Mini_No=0
    Activity_No=0
    with open (ark_path+"/name_pair.json", "rb") as file:
        npi=file.read().decode('utf-8')
        name_pair_index = json.loads(npi)
    for activity_id, activity_info in index.items():#获取键值对
        if activity_info["actType"] =="MAIN_STORY":  
            activity_type = "主线"
            activity_name = str(Main_No)+" "+activity_info["name"]
            Main_No += 1
        elif activity_info["actType"] =="MINI_STORY":  
            Mini_No += 1
            activity_type = "故事集"
            activity_name = str(Mini_No)+" "+activity_info["name"]
        elif activity_info["actType"] =="ACTIVITY_STORY":  
            Activity_No += 1
            activity_type = "活动"
            activity_name = str(Activity_No)+" "+activity_info["name"]
        elif activity_info["actType"] == "NONE": 
            activity_type = "干员秘录"
            cha_id=activity_info["id"].replace("story_","").replace("_set_1","").replace("_set_2","")
            #干员id对应替换，但我懒得一个个打了，就只有一部分
            activity_name = name_pair_index.get(cha_id,cha_id)#+" "+activity_info["name"]
        
        stories = activity_info["infoUnlockDatas"]
        # 类型文件夹
        activity_folder = os.path.join(ark_path,base_folder, activity_type)
        #创建书（以活动为单位）
        char_list=[]
        book=epub.EpubBook()
        book.set_language('zh')
        book.set_title(activity_name)
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        # 添加样式
        with open(os.path.join(ark_path,"ark-style.css"), "r", encoding="utf-8") as css_file:
            css_content = css_file.read()
            style = epub.EpubItem(uid="style", file_name="ark-style.css", content=css_content, media_type="text/css")
        book.add_item(style)
        # 遍历，添加章节
        for story in stories:
            '''#本来是给html解决文件名非法符号问题，但是epub有这问题吗？
            if ":" in story['storyName']:
                story['storyName'] = story['storyName'].replace(":","：")
            if "?" in story['storyName']:
                story['storyName'] = story['storyName'].replace("?","？")'''
            char_title = f"{story['storyCode'] or ''} {story['storyName'] or ''} {story['avgTag'] or ''}"
            story_path=os.path.join(ark_path, "story", story["storyTxt"])+".txt"
            #整理成字典方便提取内容
            origin_list = process_folder(story_path)
            #变成html内容并添加为章节
            epub_content= Classification_execution(char_title, origin_list)
            chapter = epub.EpubHtml(title=char_title, file_name=char_title+'.xhtml', content=epub_content)
            chapter.add_item(style)
            book.add_item(chapter)
            char_list.append(chapter)
        #不知道有没有用，总之按gpt说的写了
        book.toc = []
        for chapter in char_list:
            link = epub.Link(chapter.file_name, chapter.title)
            book.toc.append(link)
        file_path=os.path.join(activity_folder,activity_name+'.epub')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        try:
            epub.write_epub(file_path, book, {})
        except Exception as e:
            print(f"Error creating EPUB file: {e}")
        '''# 创建HTML文件,中间删了点什么但是我忘了。不过反正用不到（
        with open(html_file_path, 'a', encoding='utf-8') as html_content:
            # 输出处理好的故事文本字典列表
            story_path=os.path.join(ark_path, "story", story["storyTxt"])+".txt"
            origin_list = process_folder(story_path)
            # 处理成html文件

            title=f"{story['storyCode'] or ''} {story['storyName'] or ''} {story['avgTag'] or ''}.html"

            html_content.write(Classification_execution(char_title, origin_list))
            pass'''

if __name__ == "__main__":
    # 假设已有的活动数据
    ark_path = os.path.dirname(os.path.abspath(__file__))
    index_json=get_index(os.path.join(ark_path,"index.json"))
    # 生成文件夹结构
    generate_folder_structure(index_json, ark_path)

