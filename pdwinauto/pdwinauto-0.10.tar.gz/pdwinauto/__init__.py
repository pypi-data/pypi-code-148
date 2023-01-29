import os
import re
import time
from collections import namedtuple

import comtypes
import comtypes.client
import mss
import six
from a_cv_imwrite_imread_plus import save_cv_image
from ctypes_window_info import get_window_infos
from files_folders_with_timestamp import create_folder_with_timestamp
from flatten_everything import flatten_everything
from flexible_partial import FlexiblePartialOwnName
from kthread_sleep import sleep
from mousekey import MouseKey

mkey = MouseKey()
from a_pandas_ex_automate_win32 import pd_add_automate_win32
import pandas as pd
from PrettyColorPrinter import add_printer
import numpy as np

add_printer(True)
from ctypes import Structure as Struct

pd_add_automate_win32()
from a_pandas_ex_apply_ignore_exceptions import pd_add_apply_ignore_exceptions

pd_add_apply_ignore_exceptions()
from a_pandas_ex_horizontal_explode import pd_add_horizontal_explode

pd_add_horizontal_explode()
from a_pandas_ex_loc_no_exceptions import pd_add_loc_no_exceptions

pd_add_loc_no_exceptions()
from ctypes_windows import (
    window_HIDE,
    window_NORMAL,
    window_SHOWMINIMIZED,
    window_MAXIMIZE,
    window_SHOWNOACTIVATE,
    window_SHOW,
    window_MINIMIZE,
    window_SHOWMINNOACTIVE,
    window_SHOWNA,
    window_RESTORE,
    window_SHOWDEFAULT,
    window_FORCEMINIMIZE,
    resize_window,
)
from ctypes import LibraryLoader, c_buffer
from ctypes import WinDLL
from ctypes import wintypes
from ctypes import c_short
from ctypes import WINFUNCTYPE
from ctypes import c_void_p
from ctypes import c_int
from ctypes import c_uint
from ctypes import byref
from ctypes import POINTER
from ctypes import c_ubyte
from ctypes import c_size_t

windll = LibraryLoader(WinDLL)

menuclicker = namedtuple(
    "Menu",
    "text ind hwnd centerx centery width height square left_click_natural left_click move_to move_to_natural",
)

submenuclicker = namedtuple(
    "SubMenu",
    "hwnd ind text mhandle centerx centery width height square  left_click_natural left_click move_to move_to_natural",
)


class Singleton(type):

    """
    Singleton metaclass implementation from StackOverflow

    http://stackoverflow.com/q/6760685/3648361
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


@six.add_metaclass(Singleton)
class IUIA(object):
    # GUI Application automation and testing library
    # Copyright (C) 2006-2018 Mark Mc Mahon and Contributors
    # https://github.com/pywinauto/pywinauto/graphs/contributors
    # http://pywinauto.readthedocs.io/en/latest/credits.html
    # All rights reserved.
    #
    # Redistribution and use in source and binary forms, with or without
    # modification, are permitted provided that the following conditions are met:
    #
    # * Redistributions of source code must retain the above copyright notice, this
    #   list of conditions and the following disclaimer.
    #
    # * Redistributions in binary form must reproduce the above copyright notice,
    #   this list of conditions and the following disclaimer in the documentation
    #   and/or other materials provided with the distribution.
    #
    # * Neither the name of pywinauto nor the names of its
    #   contributors may be used to endorse or promote products derived from
    #   this software without specific prior written permission.
    #
    # THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    # AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    # IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    # DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
    # FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
    # DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
    # SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
    # CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
    # OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
    # OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

    def __init__(self):
        self.UIA_dll = comtypes.client.GetModule("UIAutomationCore.dll")
        self.ui_automation_client = comtypes.gen.UIAutomationClient
        self.iuia = comtypes.CoCreateInstance(
            self.ui_automation_client.CUIAutomation().IPersist_GetClassID(),
            interface=self.ui_automation_client.IUIAutomation,
            clsctx=comtypes.CLSCTX_INPROC_SERVER,
        )
        self.true_condition = self.iuia.CreateTrueCondition()
        self.tree_scope = {
            "ancestors": self.UIA_dll.TreeScope_Ancestors,
            "children": self.UIA_dll.TreeScope_Children,
            "descendants": self.UIA_dll.TreeScope_Descendants,
            "element": self.UIA_dll.TreeScope_Element,
            "parent": self.UIA_dll.TreeScope_Parent,
            "subtree": self.UIA_dll.TreeScope_Subtree,
        }
        self.root = self.iuia.GetRootElement()
        self.raw_tree_walker = self.iuia.RawViewWalker

        self.get_focused_element = self.iuia.GetFocusedElement

        # collect all known control types
        start_len = len("UIA_")
        end_len = len("ControlTypeId")
        self._control_types = [
            attr[start_len:-end_len]
            for attr in dir(self.UIA_dll)
            if attr.endswith("ControlTypeId")
        ]

        self.known_control_types = {"InvalidControlType": 0}  # string id: numeric id
        self.known_control_type_ids = {0: "InvalidControlType"}  # numeric id: string id

        for ctrl_type in self._control_types:
            type_id_name = "UIA_" + ctrl_type + "ControlTypeId"
            type_id = getattr(self.UIA_dll, type_id_name)
            self.known_control_types[ctrl_type] = type_id
            self.known_control_type_ids[type_id] = ctrl_type

    def build_condition(
        self,
        process=None,
        class_name=None,
        name=None,
        control_type=None,
        content_only=None,
    ):
        """Build UIA filtering conditions"""
        conditions = []
        if process:
            conditions.append(
                self.iuia.CreatePropertyCondition(
                    self.UIA_dll.UIA_ProcessIdPropertyId, process
                )
            )

        if class_name:
            conditions.append(
                self.iuia.CreatePropertyCondition(
                    self.UIA_dll.UIA_ClassNamePropertyId, class_name
                )
            )

        if control_type:
            if isinstance(control_type, six.string_types):
                control_type = self.known_control_types[control_type]
            elif not isinstance(control_type, int):
                raise TypeError("control_type must be string or integer")
            conditions.append(
                self.iuia.CreatePropertyCondition(
                    self.UIA_dll.UIA_ControlTypePropertyId, control_type
                )
            )

        if name:
            # TODO: CreatePropertyConditionEx with PropertyConditionFlags_IgnoreCase
            conditions.append(
                self.iuia.CreatePropertyCondition(self.UIA_dll.UIA_NamePropertyId, name)
            )

        if isinstance(content_only, bool):
            conditions.append(
                self.iuia.CreatePropertyCondition(
                    self.UIA_dll.UIA_IsContentElementPropertyId, content_only
                )
            )

        if len(conditions) > 1:
            return self.iuia.CreateAndConditionFromArray(conditions)

        if len(conditions) == 1:
            return conditions[0]

        return self.true_condition


# Build a list of named constants that identify Microsoft UI Automation
# control patterns and their appropriate comtypes classes
# We'll try to add all patterns available for the given version of Windows OS
# Reference:
# https://msdn.microsoft.com/en-us/library/windows/desktop/ee671195(v=vs.85).aspx
# header: UIAutomationClient.h


def _build_pattern_ids_dic():
    """
    A helper procedure to build a registry of control patterns
    supported on the current system
    """
    base_names = [
        "Dock",
        "ExpandCollapse",
        "GridItem",
        "Grid",
        "Invoke",
        "ItemContainer",
        "LegacyIAccessible",
        "MulipleView",
        "RangeValue",
        "ScrollItem",
        "Scroll",
        "SelectionItem",
        "Selection",
        "SynchronizedInput",
        "TableItem",
        "Table",
        "Text",
        "Toggle",
        "VirtualizedItem",
        "Value",
        "Window",
        "Transform",
        # Windows 8 and later
        "Annotation",
        "Drag",
        "Drop",
        "ObjectModel",
        "Spreadsheet",
        "SpreadsheetItem",
        "Styles",
        "TextChild",
        "TextV2",
        "TransformV2",
        # Windows 8.1 and later
        "TextEdit",
        # Windows 10 and later
        "CustomNavigation",
    ]

    ptrn_ids_dic = {}

    # Loop over the all base names and try to retrieve control patterns
    for ptrn_name in base_names:

        # Construct a class name and check if it is supported by comtypes
        v2 = ""
        name = ptrn_name
        if ptrn_name.endswith("V2"):
            name = ptrn_name[:-2]
            v2 = "2"
        cls_name = "".join(["IUIAutomation", name, "Pattern", v2])
        if hasattr(IUIA().ui_automation_client, cls_name):
            klass = getattr(IUIA().ui_automation_client, cls_name)

            # Contruct a pattern ID name and get the ID value
            ptrn_id_name = "UIA_" + name + "Pattern" + v2 + "Id"
            ptrn_id = getattr(IUIA().UIA_dll, ptrn_id_name)

            # Update the registry of known patterns
            ptrn_ids_dic[ptrn_name] = (ptrn_id, klass)

    return ptrn_ids_dic


pattern_ids = _build_pattern_ids_dic()


# Return values for the toggle_state propery
#     enum ToggleState {
#       ToggleState_Off,
#       ToggleState_On,
#       ToggleState_Indeterminate
# };
# The definition can also be found in the comtypes package
# In a file automatically generated according to UIAutomation GUID:
# comtypes\gen\_944DE083_8FB8_45CF_BCB7_C477ACB2F897_*.py
toggle_state_off = IUIA().ui_automation_client.ToggleState_Off
toggle_state_on = IUIA().ui_automation_client.ToggleState_On
toggle_state_inderteminate = IUIA().ui_automation_client.ToggleState_Indeterminate


class NoPatternInterfaceError(Exception):

    """There is no such interface for the specified pattern"""

    pass


# values for enumeration 'ExpandCollapseState'
expand_state_collapsed = IUIA().ui_automation_client.ExpandCollapseState_Collapsed
expand_state_expanded = IUIA().ui_automation_client.ExpandCollapseState_Expanded
expand_state_partially = (
    IUIA().ui_automation_client.ExpandCollapseState_PartiallyExpanded
)
expand_state_leaf_node = IUIA().ui_automation_client.ExpandCollapseState_LeafNode

# values for enumeration 'WindowVisualState'
window_visual_state_normal = IUIA().ui_automation_client.WindowVisualState_Normal
window_visual_state_maximized = IUIA().ui_automation_client.WindowVisualState_Maximized
window_visual_state_minimized = IUIA().ui_automation_client.WindowVisualState_Minimized

# values for enumeration 'ScrollAmount'
scroll_large_decrement = IUIA().ui_automation_client.ScrollAmount_LargeDecrement
scroll_small_decrement = IUIA().ui_automation_client.ScrollAmount_SmallDecrement
scroll_no_amount = IUIA().ui_automation_client.ScrollAmount_NoAmount
scroll_large_increment = IUIA().ui_automation_client.ScrollAmount_LargeIncrement
scroll_small_increment = IUIA().ui_automation_client.ScrollAmount_SmallIncrement

vt_empty = IUIA().ui_automation_client.VARIANT.empty.vt
vt_null = IUIA().ui_automation_client.VARIANT.null.vt


def get_elem_interface(element_info, pattern_name):
    """A helper to retrieve an element interface by the specified pattern name

    TODO: handle a wrong pattern name
    """
    ptrn_id, cls_name = pattern_ids[pattern_name]
    try:
        cur_ptrn = element_info.GetCurrentPattern(ptrn_id)
        iface = cur_ptrn.QueryInterface(cls_name)

    except Exception as fazx:
        raise fazx
    return iface


def get_fu(fa, atr):

    try:
        atra = getattr(fa, atr)
        tax = str(type(atra))
        if "method" in tax or "comtypes" in tax:
            return FlexiblePartialOwnName(
                atra,
                "()",  # for __str__ and __repr__
                True,
            )
        else:
            return atra
    except Exception as fe:
        # print(fe)
        return pd.NA


def get_center(x):
    try:
        a = (x[1] - x[0]) // 2 + x[0]
        b = (x[3] - x[2]) // 2 + x[2]
        return int(a), int(b)
    except Exception as fe:
        return pd.NA


def get_automation_frame_from_all_pids(uia=True, screenshot_folder=None):
    df2ba = get_window_frame(pid=0)
    dfxa = get_automation_frame(df2ba, uia=uia, screenshot_folder=screenshot_folder)
    return dfxa


def get_information_frame(pid=0):
    return get_window_frame(pid)


def get_automation_frame_from_filenames(
    exefiles, uia=True, screenshot_folder=None, timeout=30
):
    exefiles = [x.lower() for x in exefiles]
    pids = [
        x.pid
        for x in get_window_infos()
        if re.split(r"[\\/]+", x.path)[-1].lower() in exefiles
    ]
    return get_automation_frame_from_pid(
        pids, uia=uia, screenshot_folder=screenshot_folder, timeout=timeout
    )


def get_automation_frame_from_pid(pids, uia=True, screenshot_folder=None, timeout=30):
    if not isinstance(pids, list):
        pids = [pids]
    ada = []
    for pid in pids:
        ada.append(get_window_frame(pid))
    df22 = pd.concat(ada, ignore_index=True)
    subprodf = df22.loc[df22.pid.isin(pids)]
    finaltime = time.time() + timeout
    ada2 = []
    while subprodf.empty and finaltime > time.time():
        ada2.clear()
        for pid in pids:
            ada2.append(get_window_frame(pid))
        df22 = pd.concat(ada2, ignore_index=True)
        subprodf = df22.loc[df22.pid.isin(pids)]

    dfsad = get_automation_frame(subprodf, uia=uia, screenshot_folder=screenshot_folder)
    return dfsad


def click_on_main_menu(df, menu1text):
    for key0, item in df.dropna(subset="aa_menu_items").iterrows():
        xx = item["aa_menu_items"]
        for x in xx:
            if x.text == menu1text:
                x.left_click()
                return


def click_on_submenu(df9, menu1text, menu2text):
    for key1, item1 in df9.dropna(subset="aa_menu_items").iterrows():
        xx1 = item1["aa_menu_items"]
        for x1 in xx1:
            if x1.text == menu1text and x1.subitems.text == menu2text:
                x1.subitems.left_click()
                return


def get_height(x):
    try:
        b = x[3] - x[2]

        return abs(int(b))
    except Exception as fe:
        return pd.NA


def get_width(x):
    try:
        a = x[1] - x[0]
        return abs(int(a))
    except Exception as fe:
        return pd.NA


def get_ele_from_hwnd(x):
    try:
        return IUIA().iuia.ElementFromHandle(int(x))
        # return han
    except Exception as fa:
        return pd.NA


def get_automation_dataframe(df2):
    df3 = df2.copy()
    df2["element"] = df2.hwnd.apply(lambda x: get_ele_from_hwnd(x))
    df2 = df2.dropna(subset="element")
    alafa = []
    for key, item in df2.iterrows():
        for p in pattern_ids:
            try:
                elefa = get_elem_interface(element_info=item["element"], pattern_name=p)
                alafa.append((key, *item.__array__().tolist(), p, elefa))
            except Exception as fa:
                continue
    df = pd.DataFrame(alafa)
    df.columns = (
        ["aa_key"]
        + [f"aa_{x}" for x in df2.columns.to_list()]
        + ["aa_pattern_name", "aa_interface"]
    )
    notuse = [
        "DocumentRange",
        "TextRange",
        "CachedCanMaximize",
        "CachedCanMinimize",
        "CachedCanMove",
        "CachedCanResize",
        "CachedCanRotate",
        "CachedCanSelectMultiple",
        "CachedChildId",
        "CachedColumnCount",
        "CachedDefaultAction",
        "CachedDescription",
        "CachedHelp",
        "CachedHorizontalScrollPercent",
        "CachedHorizontalViewSize",
        "CachedHorizontallyScrollable",
        "CachedIsModal",
        "CachedIsReadOnly",
        "CachedIsSelectionRequired",
        "CachedIsTopmost",
        "CachedKeyboardShortcut",
        "CachedLargeChange",
        "CachedMaximum",
        "CachedMinimum",
        "CachedName",
        "CachedRole",
        "CachedRowCount",
        "CachedRowOrColumnMajor",
        "CachedSmallChange",
        "CachedState",
        "CachedToggleState",
        "CachedValue",
        "CachedVerticalScrollPercent",
        "CachedVerticalViewSize",
        "CachedVerticallyScrollable",
        "CachedWindowInteractionState",
        "CachedWindowVisualState",
    ]
    emp = pd.DataFrame(
        columns=list(
            sorted(
                [
                    f"ff_{x}"
                    for x in set(flatten_everything(df.aa_interface.apply(dir)))
                    if not str(x).startswith("_") and x not in notuse
                ]
            )
        )
    )
    for co_ in emp.columns:
        df[co_] = df.aa_interface.ds_apply_ignore(pd.NA, lambda x: get_fu(x, co_[3:]))
        df = df.copy()  # avoiding PerformanceWarning: DataFrame is highly fragmented.

    vadx = df3.loc[~df3.hwnd.isin(df.aa_hwnd)].copy()
    vadx.columns = [f"aa_{x}" for x in vadx.columns]
    df = pd.concat([df, vadx], ignore_index=True)  # .copy()

    return df.copy()


def perform_natural_left_click(
    x,
    delay=0.1,
    min_variation=-3,
    max_variation=3,
    use_every=4,
    sleeptime=(0.005, 0.009),
    print_coords=True,
    percent=90,
    offset_x=0,
    offset_y=0,
):
    mkey.left_click_xy_natural(
        int(x[0] + offset_x),
        int(x[1] + offset_y),
        delay=delay,
        # duration of the mouse click (down - up)
        min_variation=min_variation,
        # a random value will be added to each pixel  - define the minimum here
        max_variation=max_variation,
        # a random value will be added to each pixel  - define the maximum here
        use_every=use_every,  # use every nth pixel
        sleeptime=sleeptime,  # delay between each coordinate
        print_coords=print_coords,  # console output
        percent=percent,  # the lower, the straighter the mouse movement
    )


def perform_natural_middle_click(
    x,
    delay=0.1,
    min_variation=-3,
    max_variation=3,
    use_every=4,
    sleeptime=(0.005, 0.009),
    print_coords=True,
    percent=90,
    offset_x=0,
    offset_y=0,
):
    mkey.middle_click_xy_natural(
        int(x[0] + offset_x),
        int(x[1] + offset_y),
        delay=delay,
        # duration of the mouse click (down - up)
        min_variation=min_variation,
        # a random value will be added to each pixel  - define the minimum here
        max_variation=max_variation,
        # a random value will be added to each pixel  - define the maximum here
        use_every=use_every,  # use every nth pixel
        sleeptime=sleeptime,  # delay between each coordinate
        print_coords=print_coords,  # console output
        percent=percent,  # the lower, the straighter the mouse movement
    )


def perform_natural_right_click(
    x,
    delay=0.1,
    min_variation=-3,
    max_variation=3,
    use_every=4,
    sleeptime=(0.005, 0.009),
    print_coords=True,
    percent=90,
    offset_x=0,
    offset_y=0,
):
    mkey.right_click_xy_natural(
        int(x[0] + offset_x),
        int(x[1] + offset_y),
        delay=delay,
        # duration of the mouse click (down - up)
        min_variation=min_variation,
        # a random value will be added to each pixel  - define the minimum here
        max_variation=max_variation,
        # a random value will be added to each pixel  - define the maximum here
        use_every=use_every,  # use every nth pixel
        sleeptime=sleeptime,  # delay between each coordinate
        print_coords=print_coords,  # console output
        percent=percent,  # the lower, the straighter the mouse movement
    )


def add_natural_left_click(
    df,
    delay=0.1,
    min_variation=-3,
    max_variation=3,
    use_every=4,
    sleeptime=(0.005, 0.009),
    print_coords=True,
    percent=90,
):
    df["mm_left_click_xy_natural"] = df.aa_center_coords.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            perform_natural_left_click,
            f"left_click{x}",
            True,
            x,
            delay=delay,
            # duration of the mouse click (down - up)
            min_variation=min_variation,
            # a random value will be added to each pixel  - define the minimum here
            max_variation=max_variation,
            # a random value will be added to each pixel  - define the maximum here
            use_every=use_every,  # use every nth pixel
            sleeptime=sleeptime,  # delay between each coordinate
            print_coords=print_coords,  # console output
            percent=percent,  # the lower, the straighter the mouse movement
        )
        if x[0] > 0 or x[1] > 0
        else pd.NA,
    )
    return df.copy()


def add_natural_middle_click(
    df,
    delay=0.1,
    min_variation=-3,
    max_variation=3,
    use_every=4,
    sleeptime=(0.005, 0.009),
    print_coords=True,
    percent=90,
):
    df["mm_middle_click_xy_natural"] = df.aa_center_coords.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            perform_natural_middle_click,
            f"middle_click{x}",
            True,
            x,
            delay=delay,
            # duration of the mouse click (down - up)
            min_variation=min_variation,
            # a random value will be added to each pixel  - define the minimum here
            max_variation=max_variation,
            # a random value will be added to each pixel  - define the maximum here
            use_every=use_every,  # use every nth pixel
            sleeptime=sleeptime,  # delay between each coordinate
            print_coords=print_coords,  # console output
            percent=percent,  # the lower, the straighter the mouse movement
        )
        if x[0] > 0 or x[1] > 0
        else pd.NA,
    )
    return df.copy()


def add_natural_right_click(
    df,
    delay=0.1,
    min_variation=-3,
    max_variation=3,
    use_every=4,
    sleeptime=(0.005, 0.009),
    print_coords=True,
    percent=90,
):
    df["mm_right_click_xy_natural"] = df.aa_center_coords.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            perform_natural_right_click,
            f"right_click{x}",
            True,
            x,
            delay=delay,
            # duration of the mouse click (down - up)
            min_variation=min_variation,
            # a random value will be added to each pixel  - define the minimum here
            max_variation=max_variation,
            # a random value will be added to each pixel  - define the maximum here
            use_every=use_every,  # use every nth pixel
            sleeptime=sleeptime,  # delay between each coordinate
            print_coords=print_coords,  # console output
            percent=percent,  # the lower, the straighter the mouse movement
        )
        if x[0] > 0 or x[1] > 0
        else pd.NA,
    )
    return df.copy()


def perform_right_click_direct(x, y, offset_x=0, offset_y=0):
    mkey.right_click_xy(int(x + offset_x), int(y + offset_y))


def perform_left_click_direct(x, y, offset_x=0, offset_y=0):
    mkey.left_click_xy(int(x + offset_x), int(y + offset_y))


def perform_middle_click_direct(x, y, offset_x=0, offset_y=0):
    mkey.middle_click_xy(int(x + offset_x), int(y + offset_y))


def add_direct_right_click(df):
    df["mm_right_click_xy_direct"] = df.aa_center_coords.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            perform_right_click_direct,
            f"right_click{x}",
            True,
            *x,
        )
        if x[0] > 0 or x[1] > 0
        else pd.NA,
    )
    return df.copy()


def add_direct_left_click(df):
    df["mm_left_click_xy_direct"] = df.aa_center_coords.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            perform_left_click_direct,
            f"left_click{x}",
            True,
            *x,
        )
        if x[0] > 0 or x[1] > 0
        else pd.NA,
    )
    return df.copy()


def add_direct_middle_click(df):
    df["mm_middle_click_xy_direct"] = df.aa_center_coords.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            perform_middle_click_direct,
            f"middle_click{x}",
            True,
            *x,
        )
        if x[0] > 0 or x[1] > 0
        else pd.NA,
    )
    return df.copy()


def perform_move_to_natural(
    x,
    y,
    min_variation=-2,
    max_variation=2,
    use_every=1,
    sleeptime=(0.005, 0.009),
    print_coords=True,
    percent=90,
    offset_x=0,
    offset_y=0,
):
    mkey.move_to_natural(
        int(x + offset_x),
        int(y + offset_y),
        min_variation=min_variation,
        max_variation=max_variation,
        use_every=use_every,
        sleeptime=sleeptime,
        print_coords=print_coords,
        percent=percent,
    )


def perform_move_to(x, y, offset_x=0, offset_y=0):
    mkey.move_to(int(x + offset_x), int(y + offset_y))


def add_move_to_natural(df):
    df["mm_move_to_natural"] = df.aa_center_coords.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            perform_move_to_natural,
            f"move_to_natural{x}",
            True,
            *x,
        )
        if x[0] > 0 or x[1] > 0
        else pd.NA,
    )
    return df.copy()


def add_moveto(df):
    df["mm_moveto"] = df.aa_center_coords.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            perform_move_to,
            f"move_to{x}",
            True,
            *x,
        )
        if x[0] > 0 or x[1] > 0
        else pd.NA,
    )
    return df.copy()


def add_activate_window(df):
    df["mm_activate_window"] = df.aa_hwnd.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            mkey.activate_window,
            f"activate_window({x})",
            True,
            x,
        ),
    )
    return df.copy()


def add_force_activate_window(df):
    df["mm_force_activate_window"] = df.aa_hwnd.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            mkey.force_activate_window,
            f"force_activate_window({x})",
            True,
            x,
        ),
    )
    return df.copy()


def send_keys_simul_to_hwnd_force_activate(hwnd, keystopress, presstime):
    mkey.force_activate_window(hwnd)
    mkey.press_keys_simultaneously(
        keystopress=keystopress,
        presstime=presstime,
        percentofregularpresstime=100,
    )


def send_key_to_hwnd_force_activate(hwnd, key, delay):
    mkey.force_activate_window(hwnd)
    mkey.press_key(key, delay=delay)


def send_unicode_to_hwnd_force_activate(hwnd, stri):
    mkey.force_activate_window(hwnd)
    mkey.send_unicode(stri)


def send_keystrokes_to_hwnd(hwnd, stri):
    # https://pywinauto.readthedocs.io/en/latest/code/pywinauto.keyboard.html?highlight=VK_SPACE#pywinauto-keyboard
    mkey.send_keystrokes_to_hwnd(
        handle=hwnd, keystrokes=stri, activate_window_before=False
    )


def add_send_keys_simul_to_hwnd_fa(df):
    df["mm_press_keys_simultaneously_force_activate"] = df.aa_hwnd.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            send_keys_simul_to_hwnd_force_activate,
            f"press_keys_simultaneously(keystopress:list,presstime:float)",
            True,
            x,
        ),
    )
    return df.copy()


def add_send_key_to_hwnd_fa(df):
    df["mm_press_key_force_activate"] = df.aa_hwnd.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            send_key_to_hwnd_force_activate,
            f"press_key(keystopress:str,delay:float)",
            True,
            x,
        ),
    )
    return df.copy()


def add_send_unicode_to_hwnd_fa(df):
    df["mm_send_unicode_force_activate"] = df.aa_hwnd.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            send_unicode_to_hwnd_force_activate,
            f"send_unicode(str)",
            True,
            x,
        ),
    )
    return df.copy()


def _select_and_sleep(x):
    if "ff_Select" in x:
        try:

            x.ff_Select(1)
            sleep(0.1)
        except Exception:
            pass


def send_keys_simul_to_hwnd_select(x, keystopress, presstime):
    _select_and_sleep(x)
    mkey.press_keys_simultaneously(
        keystopress=keystopress,
        presstime=presstime,
        percentofregularpresstime=100,
    )


def add_send_keys_simul_to_hwnd_select(df):
    df["mm_press_keys_simultaneously"] = df.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            send_keys_simul_to_hwnd_select,
            f"press_keys_simultaneously(str)",
            True,
            x,
        ),
        axis=1,
    )
    return df.copy()


def send_keystrokes_select(x, stri):
    _select_and_sleep(x)
    send_keystrokes_to_hwnd(int(x.aa_hwnd), stri)


def add_send_keystrokes_to_hwnd(df):
    df["mm_send_keystrokes"] = df.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            send_keystrokes_select,
            f"send_keystrokes(str)",
            True,
            x,
        ),
        axis=1,
    )
    return df.copy()


def send_unicode_to_hwnd_select(x, stri):
    _select_and_sleep(x)
    mkey.send_unicode(stri)


def add_send_unicode_to_hwnd_select(df):
    df["mm_send_unicode"] = df.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            send_unicode_to_hwnd_select,
            f"send_unicode(str)",
            True,
            x,
        ),
        axis=1,
    )
    return df.copy()


def send_key_to_hwnd_select(x, key, delay):
    _select_and_sleep(x)
    mkey.press_key(key, delay=delay)


def add_send_key_to_hwnd_select(df):
    df["mm_press_key"] = df.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            send_key_to_hwnd_select,
            f"press_key(str)",
            True,
            x,
        ),
        axis=1,
    )
    return df.copy()


def add_activate_topmost(df):
    df["mm_activate_topmost"] = df.aa_hwnd.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            mkey.activate_topmost,
            f"activate_topmost()",
            True,
            int(x),
        ),
    )
    return df.copy()


def add_deactivate_topmost(df):
    df["mm_deactivate_topmost"] = df.aa_hwnd.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            mkey.deactivate_topmost,
            f"deactivate_topmost()",
            True,
            int(x),
        ),
    )
    return df.copy()


def add_ctypes_funcs(df):
    df["window_HIDE".lower()] = df.aa_hwnd.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            window_HIDE,
            f"{'window_HIDE'.lower()}()",
            True,
            int(x),
        ),
    )

    df["window_NORMAL".lower()] = df.aa_hwnd.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            window_NORMAL,
            f"{'window_NORMAL'.lower()}()",
            True,
            int(x),
        ),
    )

    df["window_SHOWMINIMIZED".lower()] = df.aa_hwnd.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            window_SHOWMINIMIZED,
            f"{'window_SHOWMINIMIZED'.lower()}()",
            True,
            int(x),
        ),
    )

    df["window_MAXIMIZE".lower()] = df.aa_hwnd.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            window_MAXIMIZE,
            f"{'window_MAXIMIZE'.lower()}()",
            True,
            int(x),
        ),
    )

    df["window_SHOWNOACTIVATE".lower()] = df.aa_hwnd.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            window_SHOWNOACTIVATE,
            f"{'window_SHOWNOACTIVATE'.lower()}()",
            True,
            int(x),
        ),
    )

    df["window_SHOW".lower()] = df.aa_hwnd.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            window_SHOW,
            f"{'window_SHOW'.lower()}()",
            True,
            int(x),
        ),
    )

    df["window_MINIMIZE".lower()] = df.aa_hwnd.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            window_MINIMIZE,
            f"{'window_MINIMIZE'.lower()}()",
            True,
            int(x),
        ),
    )

    df["window_SHOWMINNOACTIVE".lower()] = df.aa_hwnd.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            window_SHOWMINNOACTIVE,
            f"{'window_SHOWMINNOACTIVE'.lower()}()",
            True,
            int(x),
        ),
    )

    df["window_SHOWNA".lower()] = df.aa_hwnd.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            window_SHOWNA,
            f"{'window_SHOWNA'.lower()}()",
            True,
            int(x),
        ),
    )

    df["window_RESTORE".lower()] = df.aa_hwnd.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            window_RESTORE,
            f"{'window_RESTORE'.lower()}()",
            True,
            int(x),
        ),
    )

    df["window_SHOWDEFAULT".lower()] = df.aa_hwnd.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            window_SHOWDEFAULT,
            f"{'window_SHOWDEFAULT'.lower()}()",
            True,
            int(x),
        ),
    )

    df["window_FORCEMINIMIZE".lower()] = df.aa_hwnd.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            window_FORCEMINIMIZE,
            f"{'window_FORCEMINIMIZE'.lower()}()",
            True,
            int(x),
        ),
    )

    df["resize_window".lower()] = df.aa_hwnd.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            resize_window,
            f"{'resize_window'.lower()}()",
            True,
            int(x),
        ),
    )

    return df.copy()


def save_im_no_ex(path, fold):
    exception_value = pd.NA
    try:
        return save_cv_image(path, fold)
    except Exception:
        return exception_value


def _save_screenshot(df, foldertosave):
    badcha = re.compile(r"\W+")
    foldertosave = create_folder_with_timestamp(
        folder=foldertosave, prefix="", suffix="", sep="-", create_folder=False
    )

    df["screenshot_save"] = df.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            save_im_no_ex,
            f"""{(g1:=os.path.join(foldertosave, str(x.name).zfill(6) + '__' +badcha.sub( '_', x.aa_path) + '.png'))}""",
            True,
            g1,
            x.screenshot,
        ),
        axis=1,
    )
    return df.copy()


def _get_screenshot(df):
    def cropimage(img, coo_):
        coords = [_ if _ > 0 else 0 for _ in coo_]
        try:
            return img[coords[1] : coords[3], coords[0] : coords[2]].copy()
        except Exception as fe:
            return pd.NA

    def get_screenshot_with_msc(monitor: int = 1):
        with mss.mss() as sct:
            bildneu = np.array(sct.grab(mss.mss().monitors[monitor]))
        return bildneu

    im = get_screenshot_with_msc(monitor=0)
    df["screenshot"] = df.aa_coords_win.ds_apply_ignore(
        pd.NA, lambda x: cropimage(im, (x[0], x[2], x[1], x[3]))
    )

    return df.copy()


def _show_chi(item, df):
    chi = item.aa_all_children
    if not pd.isna(chi):
        return df.loc[df.aa_hwnd.isin(chi)]


def add_show_children(df):
    df["aa_show_children"] = df.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            _show_chi,
            f"show_children()",
            True,
            x,
            df,
        ),
        axis=1,
    )
    return df.copy()


PostMessage = windll.user32.PostMessageW
PostMessage.restype = wintypes.BOOL
PostMessage.argtypes = [
    wintypes.HWND,
    wintypes.UINT,
    wintypes.WPARAM,
    wintypes.LPARAM,
]


def post_message_prepare(hwnd, operation, wparam, lparam):
    PostMessage(
        wintypes.HWND(int(hwnd)),
        wintypes.UINT(int(operation)),
        wintypes.WPARAM(int(wparam)),
        wintypes.LPARAM(int(lparam)),
    )


def click_no_move(hwnd):
    hwnd = int(hwnd)
    WM_LBUTTONDOWN = 0x0201
    WM_LBUTTONUP = 0x0202
    LBUTTON = 0x1
    wParam = 0
    post_message_prepare(hwnd, WM_LBUTTONDOWN, wParam | LBUTTON, 1)
    time.sleep(0.004)
    post_message_prepare(hwnd, WM_LBUTTONUP, wParam | LBUTTON, 0)


def add_direct_click(df):

    df["aa_direct_click"] = df.aa_hwnd.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            click_no_move,
            f"direct_click()",
            True,
            int(x),
        ),
    )

    return df.copy()


def add_postmessage(df):

    df["aa_postmessage"] = df.aa_hwnd.ds_apply_ignore(
        pd.NA,
        lambda x: FlexiblePartialOwnName(
            post_message_prepare,
            f"PostMessage(operation:int, wparam:int, lparam:int)",
            True,
            int(x),
        ),
    )

    return df.copy()


def MakeLong(high, low):
    """Pack high into the high word of a long and low into the low word"""
    # we need to AND each value with 0xFFFF to account for numbers
    # greater then normal WORD (short) size
    return ((high & 0xFFFF) << 16) | (low & 0xFFFF)


def get_automation_frame(dfr, uia=True, screenshot_folder=None):
    df = dfr.copy()
    if uia:
        df = get_automation_dataframe(df)
    else:
        df.columns = [f"aa_{x}" for x in df.columns]
    df["aa_center_coords"] = df.aa_coords_win.ds_apply_ignore(pd.NA, get_center)
    df["aa_1width"] = df.aa_coords_win.ds_apply_ignore(pd.NA, get_height)
    df["aa_1height"] = df.aa_coords_win.ds_apply_ignore(pd.NA, get_width)
    df = add_show_children(df)

    df = add_natural_left_click(df)
    df = add_natural_middle_click(df)
    df = add_natural_right_click(df)
    df = add_direct_right_click(df)
    df = add_direct_left_click(df)
    df = add_direct_middle_click(df)
    df = add_activate_window(df)
    df = add_force_activate_window(df)
    df = add_send_keys_simul_to_hwnd_fa(df)
    df = add_send_key_to_hwnd_fa(df)
    df = add_send_unicode_to_hwnd_fa(df)
    df = add_send_keystrokes_to_hwnd(df)
    df = add_ctypes_funcs(df)
    df = add_send_keys_simul_to_hwnd_select(df)
    df = add_send_unicode_to_hwnd_select(df)
    df = add_send_key_to_hwnd_select(df)
    df = add_moveto(df)
    df = add_move_to_natural(df)
    df = add_postmessage(df)
    try:
        df = get_menu_items(df)
    except Exception as fe:
        df["aa_menu_items"] = pd.NA
    try:
        df = get_submenu_items(df)
    except Exception as fe:
        pass
    df = add_direct_click(df)
    if screenshot_folder is not None:
        df = _get_screenshot(df)
        df = _save_screenshot(df, screenshot_folder)
    df.aa_menu_items = df.aa_menu_items.ds_apply_ignore(pd.NA, lambda x: x[0])
    return df.filter(sorted(df.columns)).copy()


GetMenuItemCount = windll.user32.GetMenuItemCount
GetMenuItemCount.restype = c_int
GetMenuItemCount.argtypes = [
    wintypes.HMENU,
]


def menu_name(hMenu, nn):
    dummy = c_buffer(b"\000" * 32)
    windll.user32.GetMenuStringA(
        c_int(hMenu), c_int(nn), dummy, c_int(len(dummy)), 0x00000400
    )
    return dummy.value


class StructureMixIn(object):
    # from pywinauto

    """Define printing and comparison behaviors to be used for the Structure class from ctypes"""

    # ----------------------------------------------------------------
    def __str__(self):
        """Print out the fields of the ctypes Structure"""
        lines = []
        for field_name, _ in getattr(self, "_fields_", []):
            lines.append("%20s\t%s" % (field_name, getattr(self, field_name)))

        return "\n".join(lines)

    # ----------------------------------------------------------------
    def __eq__(self, other):
        """Return True if the two instances have the same coordinates"""
        fields = getattr(self, "_fields_", [])
        if isinstance(other, Struct):
            try:
                # pretend they are two structures - check that they both
                # have the same value for all fields
                if len(fields) != len(getattr(other, "_fields_", [])):
                    return False
                for field_name, _ in fields:
                    if getattr(self, field_name) != getattr(other, field_name):
                        return False
                return True

            except AttributeError:
                return False

        elif isinstance(other, (list, tuple)):
            # Now try to see if we have been passed in a list or tuple
            if len(fields) != len(other):
                return False
            try:
                for i, (field_name, _) in enumerate(fields):
                    if getattr(self, field_name) != other[i]:
                        return False
                return True

            except Exception:
                return False

        return False

    # ----------------------------------------------------------------
    def __ne__(self, other):
        """Return False if the two instances have the same coordinates"""
        return not self.__eq__(other)

    __hash__ = None


class Structure(Struct, StructureMixIn):
    # from pywinauto
    """Override the Structure class from ctypes to add printing and comparison"""

    pass


class PointIteratorMixin(object):
    # from pywinauto
    """Add iterator functionality to POINT structure"""

    x = None
    y = None

    def __iter__(self):
        """Allow iteration through coordinates"""
        yield self.x
        yield self.y

    def __getitem__(self, key):
        """Allow indexing of coordinates"""
        if key == 0 or key == -2:
            return self.x
        elif key == 1 or key == -1:
            return self.y
        else:
            raise IndexError("Illegal index")


# ====================================================================
class RectExtMixin(object):
    # from pywinauto
    """Wrap the RECT structure and add extra functionality"""

    # To be initiated by OS-specific types
    _RECT = type(None)
    _POINT = type(None)

    # ----------------------------------------------------------------
    def __init__(self, other=0, top=0, right=0, bottom=0):
        """Provide a constructor for _RECT structures
        A _RECT can be constructed by:
        - Another RECT (each value will be copied)
        - Values for left, top, right and bottom
        e.g. my_rect = _RECT(otherRect)
        or   my_rect = _RECT(10, 20, 34, 100)
        """
        if isinstance(other, self._RECT):
            self.left = other.left
            self.right = other.right
            self.top = other.top
            self.bottom = other.bottom
        else:
            # if not isinstance(other, (int, long)):
            #    print type(self), type(other), other
            long_int = six.integer_types[-1]
            self.left = long_int(other)
            self.right = long_int(right)
            self.top = long_int(top)
            self.bottom = long_int(bottom)

    # ----------------------------------------------------------------
    def __str__(self):
        """Return a string representation of the _RECT"""
        return "(L%d, T%d, R%d, B%d)" % (self.left, self.top, self.right, self.bottom)

    # ----------------------------------------------------------------
    def __repr__(self):
        """Return some representation of the _RECT"""
        return "<RECT L%d, T%d, R%d, B%d>" % (
            self.left,
            self.top,
            self.right,
            self.bottom,
        )

    # ----------------------------------------------------------------
    def __iter__(self):
        """Allow iteration through coordinates"""
        yield self.left
        yield self.top
        yield self.right
        yield self.bottom

    # ----------------------------------------------------------------
    def __sub__(self, other):
        """Return a new rectangle which is offset from the one passed in"""
        new_rect = self._RECT()

        new_rect.left = self.left - other.left
        new_rect.right = self.right - other.left

        new_rect.top = self.top - other.top
        new_rect.bottom = self.bottom - other.top

        return new_rect

    # ----------------------------------------------------------------
    def __add__(self, other):
        """Allow two rects to be added using +"""
        new_rect = self._RECT()

        new_rect.left = self.left + other.left
        new_rect.right = self.right + other.left

        new_rect.top = self.top + other.top
        new_rect.bottom = self.bottom + other.top

        return new_rect

    # ----------------------------------------------------------------
    def width(self):
        """Return the width of the rect"""
        return self.right - self.left

    # ----------------------------------------------------------------
    def height(self):
        """Return the height of the rect"""
        return self.bottom - self.top

    # ----------------------------------------------------------------
    def mid_point(self):
        """Return a POINT structure representing the mid point"""
        pt = self._POINT()
        pt.x = self.left + int(float(self.width()) / 2.0)
        pt.y = self.top + int(float(self.height()) / 2.0)
        return pt


class POINT(wintypes.POINT, PointIteratorMixin, StructureMixIn):
    pass


RectExtMixin._POINT = POINT


class RECT(wintypes.RECT, RectExtMixin, StructureMixIn):
    # from pywinauto
    """Wrap the wintypes.RECT structure and add extra functionality"""

    # ----------------------------------------------------------------
    def __init__(self, other=0, top=0, right=0, bottom=0):
        """
        Try to construct RECT from wintypes.RECT otherwise pass it down to RecExtMixin
        """
        if isinstance(other, wintypes.RECT):
            self.left = other.left
            self.right = other.right
            self.top = other.top
            self.bottom = other.bottom
        else:
            RectExtMixin.__init__(self, other, top, right, bottom)


GetMenuItemRect = windll.user32.GetMenuItemRect
GetMenuItemRect.restype = wintypes.BOOL
GetMenuItemRect.argtypes = [
    wintypes.HWND,
    wintypes.HMENU,
    wintypes.UINT,
    POINTER(wintypes.RECT),
]

GetSubMenu = windll.user32.GetSubMenu
GetSubMenu.restype = wintypes.HMENU
GetSubMenu.argtypes = [
    wintypes.HMENU,
    c_int,
]


def get_all_me(x):
    x = int(x)
    try:
        alli = []
        bax = windll.user32.GetMenu(int(x))
        co = 0
        howmany = GetMenuItemCount(wintypes.HMENU(bax))
        if howmany < 1:
            return bax, x, tuple(alli)
        for p in range(howmany):
            try:
                acs = menu_name(bax, co)
                rect = RECT()
                GetMenuItemRect(
                    wintypes.HWND(x),
                    wintypes.HMENU(int(bax)),
                    wintypes.UINT(int(p)),
                    rect,
                )
                subhaw = GetSubMenu(wintypes.HMENU(int(bax)), c_int(p))

                alli.append((co, acs, rect, subhaw))
                co = co + 1
            except Exception:
                return bax, x, tuple(alli)
        return bax, x, tuple(alli)
    except Exception as va:
        return None


def get_menu_items(df):
    ma = df.aa_hwnd.drop_duplicates().apply(get_all_me)
    ma = ma.dropna()
    ma = ma.loc[ma.apply(lambda x: len(x[2]) > 0)]
    manu = (
        ma.ds_horizontal_explode(concat=False)
        .drop(columns="0_1")
        .rename(columns={"0_0": "aa_menu_hwnd", "0_2": "aa_menu_items"})
    )
    df = pd.concat([df, manu], axis=1).copy()
    df.aa_menu_hwnd = df.aa_menu_hwnd.astype("Int64")

    mei = df.dropna(subset="aa_menu_hwnd")

    df["aa_menu_items"] = pd.NA
    df["aa_menu_items"] = df["aa_menu_items"].astype("object")
    for key, item in mei.iterrows():
        try:
            allme = []
            for mi in item.aa_menu_items:
                try:
                    textb = mi[1].decode("utf-8", "ignore")
                    indexb = mi[0]
                    handle = mi[-1]
                    xmiddle = mi[2].mid_point().x
                    ymiddle = mi[2].mid_point().y
                    width = mi[2].width()
                    height = mi[2].height()
                    square = mi[2].left, mi[2].top, mi[2].right, mi[2].bottom
                    mkey_left_click_xy_natural = FlexiblePartialOwnName(
                        mkey.left_click_xy_natural,
                        f"left_click_xy_natural({xmiddle, ymiddle})",
                        True,
                        xmiddle,
                        ymiddle,
                    )
                    mkey_left_click_xy = FlexiblePartialOwnName(
                        mkey.left_click_xy,
                        f"left_click_xy({xmiddle, ymiddle})",
                        True,
                        xmiddle,
                        ymiddle,
                    )
                    mkey_move_to = FlexiblePartialOwnName(
                        mkey.move_to,
                        f"move_to({xmiddle, ymiddle})",
                        True,
                        xmiddle,
                        ymiddle,
                    )

                    mkey_move_to_natural = FlexiblePartialOwnName(
                        mkey.move_to_natural,
                        f"move_to_natural({xmiddle, ymiddle})",
                        True,
                        xmiddle,
                        ymiddle,
                    )
                    allme.append(
                        menuclicker(
                            textb,
                            indexb,
                            handle,
                            xmiddle,
                            ymiddle,
                            width,
                            height,
                            square,
                            mkey_left_click_xy_natural,
                            mkey_left_click_xy,
                            mkey_move_to,
                            mkey_move_to_natural,
                        )
                    )
                except Exception as fe:
                    continue
        except Exception as fa:
            continue
        df.at[key, "aa_menu_items"] = tuple(allme)
    df = df.drop(columns="aa_menu_hwnd")
    return df.copy()


def dict_to_namedtuple(dic: dict, name: str = "data") -> namedtuple:
    dicn = {}
    for key, item in dic.items():
        dicn[key] = item
    return namedtuple(name, dicn.keys())(**dicn)


def get_submenu_items(df):

    allmens = []

    for key, item in df.dropna(subset="aa_menu_items").copy().iterrows():
        try:
            for ha in item["aa_menu_items"]:
                try:
                    hMenu = int(ha.hwnd)
                    bighw = int(item.aa_hwnd)
                    p = 0
                    while True:
                        dummy = c_buffer(b"\000" * 32)
                        windll.user32.GetMenuStringA(
                            c_int(hMenu),
                            c_int(p),
                            dummy,
                            c_int(len(dummy)),
                            0x00000400,
                        )
                        mi = RECT()
                        GetMenuItemRect(
                            wintypes.HWND(bighw),
                            wintypes.HMENU(int(hMenu)),
                            wintypes.UINT(int(p)),
                            mi,
                        )
                        if mi.mid_point().x <= 0 and mi.mid_point().y <= 0:
                            break
                        p += 1

                        xmiddle = mi.mid_point().x
                        ymiddle = mi.mid_point().y
                        width = mi.width()
                        height = mi.height()
                        square = mi.left, mi.top, mi.right, mi.bottom
                        mkey_left_click_xy_natural = FlexiblePartialOwnName(
                            mkey.left_click_xy_natural,
                            f"left_click_xy_natural({xmiddle, ymiddle})",
                            True,
                            xmiddle,
                            ymiddle,
                        )
                        mkey_left_click_xy = FlexiblePartialOwnName(
                            mkey.left_click_xy,
                            f"left_click_xy({xmiddle, ymiddle})",
                            True,
                            xmiddle,
                            ymiddle,
                        )
                        mkey_move_to = FlexiblePartialOwnName(
                            mkey.move_to,
                            f"move_to({xmiddle, ymiddle})",
                            True,
                            xmiddle,
                            ymiddle,
                        )

                        mkey_move_to_natural = FlexiblePartialOwnName(
                            mkey.move_to_natural,
                            f"move_to_natural({xmiddle, ymiddle})",
                            True,
                            xmiddle,
                            ymiddle,
                        )
                        hte = ha._asdict()
                        hte["subitems"] = submenuclicker(
                            bighw,
                            ha.ind,
                            dummy.value.decode("utf-8", "ignore"),
                            ha.hwnd,
                            xmiddle,
                            ymiddle,
                            width,
                            height,
                            square,
                            mkey_left_click_xy_natural,
                            mkey_left_click_xy,
                            mkey_move_to,
                            mkey_move_to_natural,
                        )
                        allmens.append(hte.copy())
                except Exception as da:
                    continue
            allresa = []
            for di in allmens:
                try:
                    nt = dict_to_namedtuple(di, "MItems")
                    allresa.append(nt)
                except Exception as asx:
                    continue
            allresa = tuple(allresa)
            df.at[key, "aa_menu_items"] = [allresa]
        except Exception as cas:
            continue
    return df.copy()


def get_window_frame(pid=0):
    return pd.Q_get_automate32_df(pid).copy()
