import json
import csv


# 从JSON文件中读取数据
def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"错误：未找到文件 {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"错误：文件 {file_path} 不是有效的JSON格式")
        return None


# 读取数据1和数据2
data1 = load_json_file('testdata.json')
data2 = load_json_file('testdata2.json')

# 检查数据是否加载成功
if not data1 or not data2:
    print("数据加载失败，程序退出")
    exit()

# 将数据2的标签信息转换为字典，便于查询
label_dict = {item['session_id']: item for item in data2.get('result', {}).get('list', [])}

# 准备CSV文件的表头（以session_id为单位）
csv_headers = [
    'session_id', 'session_type', 'all_chats',  # 合并所有聊天记录
    'first_label', 'labels'
]

# 写入CSV文件
with open('session_data6.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
    writer.writeheader()

    # 遍历数据1中的每个会话（每个session_id对应一条数据）
    for session in data1.get('sessions', []):
        session_id = session.get('session_id', '')
        session_type = session.get('session_type', '')

        # 合并当前会话中的所有聊天记录（格式：角色: 内容 [时间]）
        chat_records = []
        for chat in session.get('chats', []):
            role = chat.get('role', '')
            content = chat.get('content', '')
            msg_time = chat.get('msg_time', '')
            chat_records.append(f"{role}: {content} [{msg_time}]")

        # 用换行符分隔所有聊天记录
        all_chats = '\n'.join(chat_records)

        # 获取当前会话对应的标签信息
        label_info = label_dict.get(session_id, {})
        first_label = label_info.get('first_label', '')
        labels = ','.join(label_info.get('labels', []))  # 标签用逗号分隔

        # 构造一行数据（每个session_id对应一条）
        row_data = {
            'session_id': session_id,
            'session_type': session_type,
            'all_chats': all_chats,
            'first_label': first_label,
            'labels': labels
        }
        writer.writerow(row_data)

print("数据已成功保存到 session_data6.csv 文件")