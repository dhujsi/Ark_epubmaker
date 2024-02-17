# file_parser.py
import re
from script_elements import Narration, Image, Sticker, Dialogue_without_avatar,Dialogue_with_one_avatar,Dialogue_right
def extract_data(line):#提取入字典
    data_dict = {}
    first_match = re.search(r'\[([^[\]]*)\]', line)
    line=re.sub('Dr.{@nickname}',"博士",line)
    # 判断第0层是否有括号
    if not first_match:
        # 无括号，设定type为Narration，content为本行内容
        data_dict["type"] = "Narration"
        data_dict["content"] = line.strip()
    else:
        # 有括号，提取第一层括号中的内容
        first_layer_content = first_match.group(1)
        second_match = re.search(r'\((.*?)\)', first_layer_content)
        # 判断是否有第二层括号
        if not second_match:
            # 无第二层括号，判断内容是否有","和"="
            if "," in first_layer_content and "=" in first_layer_content:
                # 有","和"="，按","分割，将分割出的每一块等号左边作为键右边作为值存入字典
                key_value_pairs = [pair.strip() for pair in first_layer_content.split(",")]
                for pair in key_value_pairs:
                    key, value = pair.split("=")
                    data_dict[key] = value
                    data_dict['type'] = key
                data_dict["content"] = re.sub(r"[\[\(](.*?)[\]\)]", '', line)
            elif "=" in first_layer_content and "," not in first_layer_content:
                # 有"="，无","，等号左边作为键右边作为值存入字典
                key, value = first_layer_content.split("=")
                if key == 'name':
                    data_dict['type'] = "line"
                else:
                    data_dict['type'] = key
                data_dict[key] = value
                data_dict["content"] = re.sub(r"[\[\(](.*?)[\]\)]", '', line)
            else:
                # 无","和"="，type为第一层括号内容
                data_dict["type"] = first_layer_content
        else:
            # 有第二层括号，提取第二层括号内容，并将括号外内容赋值给type
            second_layer_content = second_match.group(1)
            data_dict["type"] = re.sub(r'\((.*?)\)', '', first_layer_content)
            # 判断第二层内容是否有","和"="
            if "," in second_layer_content and "=" in second_layer_content:
                data_dict["content"] = re.sub(r"[\[\(](.*?)[\]\)]", '', line)
                # 有","和"="，按","分割，将分割出的每一块等号左边作为键右边作为值存入字典
                key_value_pairs = [pair.strip() for pair in second_layer_content.split(",")]
                for pair in key_value_pairs:
                    if "=" in pair:
                        key, value = pair.split("=",1)#治标不治本吧，存在'text="<color=#000000><i>......微风轻声歌唱 ♪......</i></color>"'的例子
                    elif ":"in pair:
                        key, value = pair.split(":")
                    data_dict[key] = value
                
            elif "=" in second_layer_content:
                # 有"="，无","，等号左边作为键右边作为值存入字典
                key, value = second_layer_content.split("=")
                data_dict[key] = value
                if key == "name":
                    data_dict["content"] = re.sub(r"[\[\(](.*?)[\]\)]", '', line)
            else:
                # 无","和"="，type为第一层括号内容
                data_dict["type"] = first_layer_content

    return data_dict

def Classification_execution(title,origin_list):#判断并调用tohtml

    # 要实例化的类名列表
    class_names = ['Narration', 'Image', 'Sticker', 'Dialogue_without_avatar', 'Dialogue_with_one_avatar', 'Dialogue_right']

    html_content = ''''''
    temp_char = None
    
    for item in origin_list:
        if "type" in item: 
            #文字内容
            if item["type"].lower() == "narration":#旁白
                html_content += Narration(item["content"])
            elif item["type"].lower() in ["sticker", "subtitle"]:#信纸、字幕
                if item.get("text") and item.get("alignment"):
                    html_content += Sticker(item["text"],item["alignment"])
            elif item["type"].lower() in[ "charslot"  , "character" , "multiline", "line"]:#对话
                if item["type"].lower() in ["charslot"  , "character"]:
                    if item.get("focus"):
                        if item["focus"] == 1:
                            temp_char=item["name"]
                        elif item["focus"] == 2:
                            temp_char=item["name2"]
                    elif item.get("name2") and not item.get("focus"):
                        temp_char = None#本意用来指双人一起说话无头像，感觉这里有bug
                        '''
                        temp_char.append(item["name"])
                        temp_char.append(item["name2"])
                        '''
                    elif item.get("name"):
                        temp_char = item['name']
                    else:
                        temp_char = None
                if item["type"].lower() in ["multiline", "line"]:
                    if temp_char:
                        item["avatar"] = temp_char
                        temp_char = None
                        html_content += Dialogue_with_one_avatar(item["name"][1:-1],item["avatar"],item["content"])
                    else:
                        html_content += Dialogue_without_avatar(item["name"][1:-1],item["content"])
            #对话逻辑中，立绘表现移动的并没有处理
            elif item["type"].lower() in ["decision" , "predicate"]: #分支!有错：level_act3d0_st02根据这里写才对
                if item["type"].lower() == "decision":
                    options=re.sub("\"",'',item['options']).split(";")
                    values=re.sub("\"",'',item['values']).split(';')
                    html_content += Dialogue_right("分支") 
                if item["type"].lower() == "predicate":
                    if item.get('references'):
                        refs=re.sub("\"",'',item['references']).split(';')
                        for r in refs:
                            p = values.index(r) if r in values else None
                            if p  is not None and len(values) == len(options):
                                html_content += Dialogue_right(options[p]) 
                            elif  p is not None and len(values) != len(options) and len(options)==1:
                                html_content += Dialogue_right(options[0]) 
                                break
            #图像内容
            elif item["type"].lower() in ["image" , "background" , "showitem"]:
                if item.get("image"):
                    html_content += Image(item['image'])
                
            #效果内容
            elif item["type"].lower() =="cameraeffect":
                if item["effect"] == "Grayscale": 
                    if item["amount"] != 0:
                        html_content += Narration("[回忆]")
                    if item["amount"] == 0:
                        html_content += Narration("[回忆结束]")
            #blocker类，用来分隔演出节奏的
            elif item["type"].lower() in ["blocker"]:
                html_content +="""
                            <div class=blocker></div>"""
            #[characteraction(name="middle", type="move", xpos=-300, fadetime=2,block=false)]
            #elif item["type"].lower() in["cameraeffect" , "CameraShake"]:
    html_content +='''    
    </body>
</html>'''
    return html_content
def process_folder(story_path):#按storypath逐行读取单文件并输出列表
    result_list = []
    with open(story_path, "r", encoding="utf-8") as story_file:
    # 逐行读取文件内容
        for line in story_file:
        # 处理每一行的内容返回字典
            result_list.append(extract_data(line.strip()))
    return  result_list
