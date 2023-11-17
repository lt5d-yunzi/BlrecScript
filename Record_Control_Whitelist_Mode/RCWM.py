# 此项目使用ChatGPT3.5生成
# 导入所需的库
from flask import Flask, request, jsonify
import json
import requests
import logging

app = Flask(__name__)

werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.ERROR)

# 读取配置文件
with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)

# 定义录制状态，默认为配置文件中的值
recording_enabled = config.get("recording", True)
specified_room_id = config.get("room_id", None)

# Webhook路由，用于接收信息
# Webhook 路由，用于接收信息
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    # 输出原始内容到控制台
    #print("Received Webhook Data:")
    #print(json.dumps(data, indent=2))

    # 检查data中是否包含room_info
    if 'room_info' in data.get('data', {}):
        room_info = data['data']['room_info']

        # 打印room_info的内容
        #print("Room Info:")
        #print(json.dumps(room_info, indent=2))

        # 提取关键信息
        title = room_info.get("title", "")
        room_id = room_info.get("room_id", "")
        area_name = room_info.get("area_name", "")
        parent_area_name = room_info.get("parent_area_name", "")

        # 输出信息到控制台
        print("--------监控信息--------")
        print(f"标题: {title}")
        print(f"直播间号: {room_id}")
        print(f"直播分区: {area_name}")
        print(f"主直播分区: {parent_area_name}")

        # 判断是否满足录制条件
        if check_recording_conditions(title, room_id, area_name, parent_area_name):
            enable_recording(room_id)  # 传递正确的 room_id
        else:
            disable_recording(room_id)  # 传递正确的 room_id
    else:
        print("没有直播间数据.")

    return "Webhook received", 200

# 此项目 使用Chat GPT3.5 生成
# 获取当前录制状态的路由
@app.route('/get_recording_status', methods=['GET'])
def get_recording_status():
    return jsonify({"recording_enabled": recording_enabled, "specified_room_id": specified_room_id})

# 判断是否满足录制条件的函数
def check_recording_conditions(title, room_id, area_name, parent_area_name):
    # 你的条件判断逻辑
    if config["check_mode"] == "area" and area_name not in config["area_name"]:
        return False
    elif config["check_mode"] == "keywords" and not any(keyword in title for keyword in config["keywords"]):
        return False
    elif config["check_mode"] == "parent_area" and parent_area_name not in config["parent_area_name"]:
        return False
    elif config["check_mode"] == "all" and (area_name not in config["area_name"] or not any(keyword in title for keyword in config["keywords"]) or parent_area_name not in config["parent_area_name"]):
        return False

    return True

def get_recording_status_api(room_id):
    api_url = f'http://localhost:2233/api/v1/tasks/{room_id}/data'
    headers = {'accept': 'application/json', 'x-api-key': 'bili2233'}
    response = requests.get(api_url, headers=headers)
    response_json = response.json()
    return response_json.get('task_status', {}).get('recorder_enabled', False)

# 启用录制的函数
def enable_recording(room_id):
    global recording_enabled
    
    # 获取当前录制状态
    current_recording_status = get_recording_status_api(room_id)
    
    # 判断当前录制状态，如果已启用则不进行操作
    if current_recording_status:
        print("已经启用录制.")
        return
    
    recording_enabled = True
    
    # 发送开始录制的 API 请求
    start_recording_response = start_recording(room_id)
    print(start_recording_response)
# 此项目 使用ChatGPT3.5 生成
# 禁用录制的函数
def disable_recording(room_id):
    global recording_enabled
    
    # 获取当前录制状态
    current_recording_status = get_recording_status_api(room_id)
    
    # 判断当前录制状态，如果已禁用则不进行操作
    if not current_recording_status:
        print("录制已禁用.")
        return
    
    recording_enabled = False
# 此项目 使用ChatGPT3.5 生成
    # 发送结束录制的 API 请求
    stop_recording_response = stop_recording(room_id)
    print(stop_recording_response)

# 发送开始录制的 API 请求
def start_recording(room_id):
    api_url = f'http://localhost:2233/api/v1/tasks/{room_id}/recorder/enable'
    headers = {'accept': 'application/json', 'x-api-key': 'bili2233'}
    response = requests.post(api_url, headers=headers, data='')
    response_json = response.json()
    print("录制已启用：" + response_json.get('message', ''))
    #return response.json()

# 发送结束录制的 API 请求
def stop_recording(room_id):
    api_url = f'http://localhost:2233/api/v1/tasks/{room_id}/recorder/disable'
    headers = {'accept': 'application/json', 'x-api-key': 'bili2233'}
    response = requests.post(api_url, headers=headers, data='')
    response_json = response.json()
    print("录制已禁用：" + response_json.get('message', ''))
    #return response.json()
# 此项目 使用ChatGPT 3.5生成
# 启动Flask应用
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Run the Flask app with logging options.')
    parser.add_argument('--log-level', dest='log_level', default='INFO', help='Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)')
    
    args = parser.parse_args()
    
    logging.basicConfig(level=args.log_level)
    
    app.run(port=5000)



# 此项目使用ChatGPT3.5生成