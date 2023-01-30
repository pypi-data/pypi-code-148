导入 os
导入 随机数

从 pyecharts.faker 导入 _Faker
从 pyecharts.faker 导入 POPULATION
# 从 汉化通用 导入 _反向注入

各国人口 = POPULATION

类 _〇捏造器(_Faker):
    套路 机选(分身):
        返回 分身.choose()

    @staticmethod
    套路 值々(起=20, 止=150):
        返回 [随机数.随机整数(起, 止) 取 _ 于 范围(7)]

    @staticmethod
    def 随机颜色() -> str:
        return 随机数.单选(
            [
                "#c23531",
                "#2f4554",
                "#61a0a8",
                "#d48265",
                "#749f83",
                "#ca8622",
                "#bda29a",
                "#6e7074",
                "#546570",
                "#c4ccd3",
                "#f05b72",
                "#444693",
                "#726930",
                "#b2d235",
                "#6d8346",
                "#ac6767",
                "#1d953f",
                "#6950a1",
            ]
        )

    @staticmethod
    def 图像路径(路径: str, 前缀: str = "images") -> str:
        return os.路径.连接(前缀, 路径)

捏造器 = _〇捏造器()
捏造器.一周 = 捏造器.week
捏造器.十二个月 = 捏造器.months
捏造器.省份 = 捏造器.provinces
捏造器.三十天 = 捏造器.days_attrs
捏造器.三十天随机值 = 捏造器.days_values
捏造器.二十四小时 = 捏造器.clock
捏造器.服装 = 捏造器.clothes
捏造器.饮料 = 捏造器.drinks
捏造器.手机 = 捏造器.phones
捏造器.水果 = 捏造器.fruits
捏造器.动物 = 捏造器.animal
捏造器.汽车 = 捏造器.cars
捏造器.狗狗 = 捏造器.dogs
捏造器.视觉颜色 = 捏造器.visual_color