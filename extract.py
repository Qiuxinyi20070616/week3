import re

# 测试文本
text = """
手机号:13812345678
邮箱:test@qq.com
日期:2026-06-08
"""

# 提取手机号
phone = re.findall(r"1[3-9]\d{9}", text)

# 提取邮箱
email = re.findall(r"\w+@\w+\.\w+", text)

# 提取日期
date = re.findall(r"\d{4}-\d{2}-\d{2}", text)

print("手机号：", phone)
print("邮箱：", email)
print("日期：", date)