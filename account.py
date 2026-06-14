class BankAccount:
    
    # 初始化账户信息
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    # 存款
    def deposit(self, money):
        self.balance = self.balance + money
        print("存款成功")

    # 取款
    def withdraw(self, money):
        if money > self.balance:
            print("余额不足")
        else:
            self.balance = self.balance - money
            print("取款成功")

    # 查看余额
    def show_balance(self):
        print("账户：", self.name)
        print("当前余额：", self.balance)

# 创建账户
name = input("请输入账户名：")
balance = float(input("请输入初始余额："))
account = BankAccount(name, balance)

# 菜单循环
while True:
    print("\n===== 银行系统 =====")
    print("1.存款")
    print("2.取款")
    print("3.查看余额")
    print("4.退出")
    choice = input("请选择功能：")
    if choice == "1":
        money = float(input("请输入存款金额："))
        account.deposit(money)
    elif choice == "2":
        money = float(input("请输入取款金额："))
        account.withdraw(money)
    elif choice == "3":
        account.show_balance()
    elif choice == "4":
        print("欢迎下次使用")
        break
    else:
        print("输入有误，请重新选择")