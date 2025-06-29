class Car:
    def __init__(self, brand):
        self.brand = brand  # 品牌属性
        self.speed = 0  # 速度属性初始化为0

    def accelerate(self, m):
        """加速方法：速度增加m次，每次增加10"""
        self.speed += m * 10

    def brake(self, n):
        """刹车方法：速度减少n次，每次减少10，不低于0"""
        self.speed -= n * 10
        if self.speed < 0:
            self.speed = 0



# 创建Car实例
my_car = Car("Toyota")

# 加速操作
my_car.accelerate(3)
print(f"{my_car.brand}当前速度: {my_car.speed}")

# 刹车操作
my_car.brake(2)
print(f"{my_car.brand}当前速度: {my_car.speed}")



class ElectricCar(Car):
    def __init__(self, brand):
        super().__init__(brand)
        self.battery = 0

    def charge(self):
        """充电方法：电量增加20，不超过100"""
        self.battery += 20
        if self.battery > 100:
            self.battery = 100


tesla = ElectricCar("Tesla")
tesla.charge()  # 充电一次
print(f"{tesla.brand}电量: {tesla.battery}")
tesla.charge()  # 再次充电
print(f"{tesla.brand}电量: {tesla.battery}")