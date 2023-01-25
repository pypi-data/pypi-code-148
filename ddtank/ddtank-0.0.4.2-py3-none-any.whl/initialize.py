import ddtank


def get_game_window_information() -> list:
    """
    获取所有游戏窗口信息
    :return: 由游戏窗口信息字典组成的列表
        platform: 代理平台
        service: 服务器
        name: 账号或备注
        index: 窗口编号
        hwnd: 游戏窗口句柄
    """
    windows_list, info_dict_list = [], []
    ddtank.win32gui.EnumWindows(lambda w, param: param.append(w), windows_list)
    pattern_for_36 = ddtank.re.compile(r'\[(.*)-(.*)-(.*)]\|(.*)\|(.*)\|(.*)\|(.*)\|(.*)')
    for window in windows_list:
        title = ddtank.win32gui.GetWindowText(window)
        re_rst = pattern_for_36.search(title)
        if re_rst:
            rst = re_rst.groups()
            info_dict = {'platform': rst[0], 'service': int(rst[1]), 'name': rst[2], 'index': int(rst[3]), 'hwnd': int(rst[5])}
            info_dict_list.append(info_dict)
    return info_dict_list


def get_game_window_handle() -> list:
    """
    获取所有游戏窗口句柄
    :return: 由游戏窗口句柄组成的列表
    """
    windows_list, hwnd_list = [], []
    ddtank.win32gui.EnumWindows(lambda w, param: param.append(w), windows_list)
    pattern_for_36 = ddtank.re.compile(r'\[(.*)-(.*)-(.*)]\|(.*)\|(.*)\|(.*)\|(.*)\|(.*)')
    for window in windows_list:
        title = ddtank.win32gui.GetWindowText(window)
        re_rst = pattern_for_36.search(title)
        if re_rst:
            rst = re_rst.groups()
            hwnd_list.append(int(rst[5]))
    return hwnd_list


