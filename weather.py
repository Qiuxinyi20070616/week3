import requests
import json
import os
import time
import re

class WeatherTool:
    # 初始化
    def __init__(self):
        self.cache_file = "weather_cache.json"
        self.cache_time = 3600
        self.cache = self.load_cache()

    # 读缓存
    def load_cache(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    # 存缓存
    def save_cache(self):
        with open(self.cache_file, "w", encoding="utf-8") as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=4)

    # 检查城市是否合法
    def check_city(self, city):
        pattern = r"^[\u4e00-\u9fa5a-zA-Z]+$"
        return re.match(pattern, city)

    # 获取天气
    def get_weather(self, city):
        now = time.time()

        if city in self.cache:
            old_time = self.cache[city]["time"]
            if now - old_time < self.cache_time:
                print(city, "使用缓存数据")
                return self.cache[city]["data"]
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            raise Exception("请求失败")
        data = response.json()

        # 保存
        self.cache[city] = {
            "time": now,
            "data": data
        }
        return data

    def parse_weather(self, data):
        current = data["current_condition"][0]
        temp = current["temp_C"]
        weather = current["weatherDesc"][0]["value"]
        humidity = current["humidity"]
        return temp, weather, humidity

    # 显示结果
    def show_weather(self, city, data):
        temp, weather, humidity = self.parse_weather(data)
        print("{:<10}{:<10}{:<15}{:<10}".format(
            city,
            temp + "℃",
            weather,
            humidity + "%"
        ))

        # 温度提醒
        if int(temp) < 10:
            print(city, "提示：记得加衣服")

    # 输入城市
    def input_city(self):
        text = input("请输入城市（多个城市用逗号分隔）：")
        city_list = []
        for city in text.split(","):
            city = city.strip()
            if city != "":
                city_list.append(city)
        return city_list

    def run(self):
        print("===== 天气查询工具 =====")
        cities = self.input_city()
        print()
        print("{:<10}{:<10}{:<15}{:<10}".format(
            "城市",
            "温度",
            "天气",
            "湿度"
        ))
        print("-" * 45)
        for city in cities:
            # 正则
            if not self.check_city(city):
                print(city, "城市名称不合法")
                continue
            try:
                data = self.get_weather(city)
                # 城市判断
                if "current_condition" not in data:
                    print(city, "城市不存在")
                    continue
                self.show_weather(city, data)
            except requests.exceptions.Timeout:
                print(city, "请求超时")
            except requests.exceptions.RequestException:
                print(city, "网络错误")
            except Exception:
                print(city, "查询失败")

        # 保存缓存
        self.save_cache()
        print()
        print("查询结束")

# 程序入口
if __name__ == "__main__":
    tool = WeatherTool()
    tool.run()