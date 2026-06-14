import requests

# 搜索
def search(query):
    return f"搜索结果：{query} 相关信息已查询完毕"

# 计算
def calc(expr):
    valid = "0123456789+-*/(). "
    for c in expr:
        if c not in valid:
            return "表达式包含非法字符"
    try:
        res = eval(expr)
        return f"计算结果：{expr} = {res}"
    except:
        return "表达式格式错误"

# 天气
def get_weather(city):
    try:
        url = f"https://wttr.in/{city}?format=3"
        res = requests.get(url)
        return f"天气结果：{res.text.strip()}"
    except:
        return "网络异常，天气查询失败"

# 工具
tools = {
    "search": search,
    "calc": calc,
    "weather": get_weather
}

# 选择用哪一个
def decide_tool(text):
    if "天气" in text or "温度" in text:
        city = text.replace("今天","").replace("多少度","").replace("天气","").strip()
        return {"action":"call_tool","tool":"weather","args":{"city":city}}

    elif "+" in text or "-" in text or "*" in text or "/" in text or "计算" in text:
        exp = text.replace("计算","").strip()
        return {"action":"call_tool","tool":"calc","args":{"expr":exp}}

    elif "是什么" in text or "查询" in text:
        return {"action":"call_tool","tool":"search","args":{"query":text}}

    else:
        return {"action":"finish","answer":"任务结束"}
# Agent循环
def agent_loop(user_q,max_steps=5):
    msg_list = [{"role":"user","content":user_q}]

    for i in range(max_steps):

        latest = msg_list[-1]["content"]   # 当前输入

        choice = decide_tool(latest)       # 选工具

        if choice["action"] == "finish":
            return choice["answer"]

        tool_name = choice["tool"]
        para = choice["args"]

        tool_result = tools[tool_name](**para)  # 调用工具

        msg_list.append({"role":"tool","content":tool_result})  # 记录结果

    return "已达到最大运行步数"

# 测试
if __name__ == "__main__":
    print(agent_loop("深圳今天多少度？"))
    print("-"*30)
    print(agent_loop("计算 10 + 20 * 3"))
    print("-"*30)
    print(agent_loop("Python是什么？"))