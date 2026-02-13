import requests
import json
from datetime import datetime
from zoneinfo import ZoneInfo

# 你的飞书Webhook地址（无需修改）
FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/4d04f305-8766-4679-a0a4-3013a7329b4b"
# 免费汇率接口（澳元为基准）
RATE_API = "https://open.er-api.com/v6/latest/AUD"

def get_aud_cny_rate():
    """获取最新澳元兑人民币汇率"""
    try:
        # 调用汇率接口
        res = requests.get(RATE_API, timeout=10)
        data = res.json()
        
        # 校验接口返回是否正常
        if data.get("result") != "success":
            return None, "汇率接口返回异常"
        
        # 获取澳元兑人民币汇率（保留4位小数）
        aud2cny = round(data["rates"]["CNY"], 4)
        return aud2cny, None
    except Exception as e:
        return None, f"汇率获取失败：{str(e)[:30]}"

def generate_reminder(rate):
    """根据汇率生成分级提醒文案"""
    # 获取当前时间（北京时间 UTC+8）
    current_time = datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S")
    
    # 分级判断逻辑
    if rate < 4.5:
        return f"🚨【紧急提醒】{current_time}\n1澳元 = {rate}人民币\n⚠️ 汇率已低于4.5！"
    elif rate < 4.6:
        return f"🔴【重要提醒】{current_time}\n1澳元 = {rate}人民币\n⚠️ 汇率已低于4.6！"
    elif rate < 4.7:
        return f"🟡【注意提醒】{current_time}\n1澳元 = {rate}人民币\n⚠️ 汇率已低于4.7！"
    else:
        return f"🟢【正常汇率】{current_time}\n1澳元 = {rate}人民币"

def send_to_feishu(content):
    """推送消息到飞书"""
    # 飞书机器人消息格式
    payload = {
        "msg_type": "text",
        "content": {
            "text": f"【澳元兑人民币汇率】\n{content}"
        }
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(
            FEISHU_WEBHOOK, 
            data=json.dumps(payload), 
            headers=headers, 
            timeout=10
        )
        # 校验推送是否成功
        if response.status_code != 200:
            print(f"推送失败：{response.text}")
        else:
            print(f"推送成功：{content}")
    except Exception as e:
        print(f"推送异常：{str(e)}")

if __name__ == "__main__":
    # 获取汇率
    rate, error = get_aud_cny_rate()
    
    if error:
        # 汇率获取失败时推送错误信息
        send_to_feishu(f"❌ 汇率获取失败：{error}")
    else:
        # 生成分级提醒文案并推送
        reminder = generate_reminder(rate)
        send_to_feishu(reminder)