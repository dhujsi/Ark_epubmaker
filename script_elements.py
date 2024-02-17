# script_elements.py

#旁白
def Narration(content):
        return f"""
        <div class="narration">{content}</div>"""

#字幕
def Sticker(content,alignment):
    # 如果 alignment 为空，则将其默认设置为 "left"
    alignment_style = f"text-align: {alignment};" if alignment else "text-align: left;"
    return f"""
    <div class="sticker" style="{alignment_style}">{content}</div>"""

#插图,包括background和各种
def Image(content):
    return f"""
    <img src="{content}" alt="{content}">"""
    
#单头像对话
def Dialogue_with_one_avatar(character_name, avatar, content):
    #<img src="{avatar}" alt="{character_name}">/* 头像没截，暂时留空 */
    return f"""
            <div class="dialogue">
                <div class="avatar-container">
                </div>
                <div class="info">
                    <span class="character-name">{character_name}</span>
                    <span class="content">{content}</span>
                </div>
            </div>"""
#无头像对话
def Dialogue_without_avatar(character_name,content):
    return f"""
            <div class="dialogue">
                <div class="avatar-container"></div>
                <div class="info">
                    <span class="character-name">{character_name}</span>
                    <span class="content">{content}</span>
                </div>
            </div>"""
#选项，右置对话
def Dialogue_right(content):
    return f"""
    <div class="dialogue_right">
        <span class="content_right">{content}</span>
    </div>"""

