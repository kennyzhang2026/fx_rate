import requests
import json

# 你的飞书Webhook地址（已帮你填好）
FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/4d04f305-8766-4679-a0a4-3013a7329b4b"
# 免费汇率接口（澳元为基准）
RATE_API = "https://open.er-api.com/v6/latest/AUD"

def get_aud_cny_rate():
    try:
        # 调用汇率接口
        res = requests.get(RATE_API, timeout=10)
        data = res.json()
        # 获取澳元兑人民币汇率（保留4位小数）
        aud2cny = round(data["rates"]["CNY"], 4)
        return f"1澳元 = {aud2cny}人民币"
    except Exception as e:
        return f"汇率获取失败：{str(e)[:20]}"

def send_to_feishu(content):
    # 飞书机器人要求的固定格式（解决msg_type报错）
    payload = {
        "msg_type": "text",
        "content": {
            "text": f"【澳元兑人民币汇率】{content}"
        }
    }
    headers = {"Content-Type": "application/json"}
    requests.post(FEISHU_WEBHOOK, data=json.dumps(payload), headers=headers, timeout=10)

if __name__ == "__main__":
    rate_info = get_aud_cny_rate()
    send_to_feishu(rate_info)
    print(f"推送成功：{rate_info}")