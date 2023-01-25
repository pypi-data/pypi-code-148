import time

import ddtank

keycode_dict = {
    "back": 0x08,
    "tab": 0x09,
    "return": 0x0D,
    "shift": 0x10,
    "control": 0x11,
    "menu": 0x12,
    "pause": 0x13,
    "capital": 0x14,
    "escape": 0x1B,
    "space": 0x20,
    "end": 0x23,
    "home": 0x24,
    "left": 0x25,
    "up": 0x26,
    "right": 0x27,
    "down": 0x28,
    "print": 0x2A,
    "snapshot": 0x2C,
    "insert": 0x2D,
    "delete": 0x2E,
    "lwin": 0x5B,
    "rwin": 0x5C,
    "numpad0": 0x60,
    "numpad1": 0x61,
    "numpad2": 0x62,
    "numpad3": 0x63,
    "numpad4": 0x64,
    "numpad5": 0x65,
    "numpad6": 0x66,
    "numpad7": 0x67,
    "numpad8": 0x68,
    "numpad9": 0x69,
    "multiply": 0x6A,
    "add": 0x6B,
    "separator": 0x6C,
    "subtract": 0x6D,
    "decimal": 0x6E,
    "divide": 0x6F,
    "f1": 0x70,
    "f2": 0x71,
    "f3": 0x72,
    "f4": 0x73,
    "f5": 0x74,
    "f6": 0x75,
    "f7": 0x76,
    "f8": 0x77,
    "f9": 0x78,
    "f10": 0x79,
    "f11": 0x7A,
    "f12": 0x7B,
    "numlock": 0x90,
    "scroll": 0x91,
    "lshift": 0xA0,
    "rshift": 0xA1,
    "lcontrol": 0xA2,
    "rcontrol": 0xA3,
    "lmenu": 0xA4,
    "rmenu": 0XA5
}


def get_keycode(key: str) -> int:
    """
    获取按键的键值
    :param key: 按键的名称
    :return: 按键的键值，如果没有找到该键键值，返回-1
    """
    if len(key) == 1 and key in ddtank.string.printable:
        return ddtank.VkKeyScanA(ord(key)) & 0xff
    elif key in keycode_dict.keys():
        return keycode_dict[key]
    else:
        return -1


class Status:
    def __init__(self, info_dict: dict):
        self.platform = info_dict['platform']
        self.service = info_dict['service']
        self.name = info_dict['name']
        self.index = info_dict['index']
        self.hwnd = info_dict['hwnd']

    def __repr__(self) -> str:
        return self.name

    @staticmethod
    def sleep(period: int, precise: bool = True):
        """
        角色等待一段时间
        :param period: 按键间隔时长(ms)
        :param precise: 是否使用高精度计时，默认为是
        :return: 无返回值
        """
        if precise:
            time_start = ddtank.time.perf_counter()
            while ((ddtank.time.perf_counter() - time_start) * 1000) < period:
                continue
        else:
            time.sleep(period / 1000)

    def activate(self, period: int = 10):
        """
        激活角色游戏窗口
        :param period: 发送激活信息后的等待时长(ms)，默认为10ms
        :return: 无返回值
        """
        ddtank.win32api.PostMessage(self.hwnd, ddtank.win32con.WM_SETFOCUS, 0, 0)
        self.sleep(period)

    def click(self, coordinate_x: int, coordinate_y: int, period: int = 10) -> bool:
        """
        对角色模拟单击操作
        :param coordinate_x: 单击点的x坐标
        :param coordinate_y: 单击点的y坐标
        :param period: 按键间隔时长(ms)
        :return: 返回布尔类型变量，代表模拟信息传递是否成功
        """
        if 0 <= coordinate_x <= 1000 and 0 <= coordinate_y <= 600:
            coordinate = ddtank.win32api.MAKELONG(coordinate_x, coordinate_y)
            ddtank.win32api.SendMessage(self.hwnd, ddtank.win32con.WM_LBUTTONDOWN, ddtank.win32con.MK_LBUTTON,
                                        coordinate)
            self.sleep(period)
            ddtank.win32api.SendMessage(self.hwnd, ddtank.win32con.WM_LBUTTONUP, ddtank.win32con.MK_LBUTTON, coordinate)
            return True
        else:
            return False

    def click_pixel(self, coordinate_x: int, coordinate_y: int, pixel: tuple, repeat: bool = True) -> bool:
        """
        当指定位置像素符合条件时，对角色模拟单击操作
        :param coordinate_x: 单击点的x坐标
        :param coordinate_y: 单击点的y坐标
        :param pixel: 指定点像素的RGB值
        :param repeat: 是否重复判断，默认为是
        :return: 返回布尔类型变量，代表模拟信息传递是否成功
        """
        status_img = self.capture()
        pixel = pixel[::-1]
        while repeat:
            if (status_img[coordinate_y, coordinate_x] == pixel).all():
                self.click(coordinate_x, coordinate_y)
                return True
            status_img = self.capture()
        if (status_img[coordinate_y, coordinate_x] == pixel).all():
            self.click(coordinate_x, coordinate_y)
            return True
        return False

    def click_pixel_back(self, coordinate_x: int, coordinate_y: int, pixel_x: int, pixel_y: int, pixel: tuple, period: int = 500) -> bool:
        """
        对角色模拟单击操作后等待一段时间，如果指定位置像素不符合条件时将继续模拟单击操作直到符合条件
        :param coordinate_x: 单击点的x坐标
        :param coordinate_y: 单击点的y坐标
        :param pixel_x: 检测点的x坐标
        :param pixel_y: 检测点的y坐标
        :param pixel: 检测点像素的RGB值
        :param period: 模拟单击操作后等待的时间(ms)
        :return: 返回布尔类型变量，代表模拟信息传递是否成功
        """
        pixel = pixel[::-1]
        self.click(coordinate_x, coordinate_y)
        self.sleep(period)
        status_img = self.capture()
        while True:
            if (status_img[pixel_y, pixel_x] == pixel).all():
                return True
            self.click(coordinate_x, coordinate_y)
            self.sleep(period)
            status_img = self.capture()

    def press(self, key: str, period: int = 10) -> bool:
        """
        对角色模拟按键操作
        :param key: 模拟按键的名称
        :param period: 按键间隔时长(ms)
        :return: 返回布尔类型变量，代表模拟信息传递是否成功
        """
        keycode = get_keycode(key)
        if keycode == -1:
            return False
        else:
            ddtank.win32api.SendMessage(self.hwnd, ddtank.win32con.WM_KEYDOWN, keycode,
                                        (ddtank.win32api.MapVirtualKey(keycode, 0) << 16) | 1)
            self.sleep(period)
            ddtank.win32api.SendMessage(self.hwnd, ddtank.win32con.WM_KEYUP, keycode,
                                        (ddtank.win32api.MapVirtualKey(keycode, 0) << 16) | 0XC0000001)
            return True

    def capture(self, position: tuple = (0, 0, 1000, 600)) -> ddtank.np.ndarray:
        """
        对角色游戏窗口执行截图操作
        :param position: 指明截图位置的元组，分别为左上角x坐标、左上角y坐标、宽度、高度，默认为(0, 0, 1000, 600)即整个窗口
        :return: 返回cv2格式的图片
        """
        x, y, w, h = position
        hwnd_dc = ddtank.win32gui.GetWindowDC(self.hwnd)
        mfc_dc = ddtank.win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()
        save_bit_map = ddtank.win32ui.CreateBitmap()
        save_bit_map.CreateCompatibleBitmap(mfc_dc, w, h)
        save_dc.SelectObject(save_bit_map)
        save_dc.BitBlt((0, 0), (w, h), mfc_dc, (x, y), ddtank.win32con.SRCCOPY)
        signed_ints_array = save_bit_map.GetBitmapBits(True)
        img = ddtank.np.frombuffer(signed_ints_array, dtype="uint8")
        img.shape = (h, w, 4)
        ddtank.win32gui.DeleteObject(save_bit_map.GetHandle())
        mfc_dc.DeleteDC()
        save_dc.DeleteDC()
        return ddtank.cv2.cvtColor(img, ddtank.cv2.COLOR_RGBA2RGB)

    def task(self):
        pass
