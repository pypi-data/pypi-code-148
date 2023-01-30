import math

import numpy as _np
import matplotlib
from matplotlib import patches
import matplotlib.patheffects

from pyfie import _pyplot_util
import pyfie as fie


def _determine_plot_scale(axes):
    ysize_img = abs(axes.get_ylim()[0] - axes.get_ylim()[1])
    if ysize_img <= 1.0:
        # no imshow executed. plot_scale will be broken
        plot_scale = 1.0
    else:
        extent_bbox = axes.get_window_extent().get_points()
        ysize_plot = extent_bbox[1, 1] - extent_bbox[0, 1]
        plot_scale = ysize_plot / ysize_img
    return plot_scale

def _get_decent_font_size(axes):
    if "font.size" in matplotlib.rcParams:
        font_size = matplotlib.rcParams["font.size"]
    else:
        font_size = 10

    ysize_img = abs(axes.get_ylim()[0] - axes.get_ylim()[1])
    if ysize_img <= 1.0:
        # no imshow executed. plot_scale will be broken
        font_size_multiplier = 1.0
    else:
        extent_bbox = axes.get_window_extent().get_points()

        xsize_plot = extent_bbox[1, 0] - extent_bbox[0, 0]
        xsize_inch = xsize_plot / axes.figure.dpi
        
        font_size_multiplier = min(xsize_inch / 8.0, 10.0)

    font_size *= font_size_multiplier
    font_size = max(8, font_size)
    return font_size

def _point_to_inch(pt, dpi):
    return pt / 72 * dpi

# グレイサーチ

def plot_gs2_results(
    hgs_pat, results, nresults=None, plot_obj=None, show_no=True, show_score=True,
    font_size=None,
    no_props=None, score_props=None, bbox_props=None, point_props=None):
    """グレイサーチ(正規化相関サーチ)のサーチ回答のプロットを行います。

    パラメータ **hgs_pat** にグレイサーチパターンオブジェクトを、 **results** にサーチ回答を表す ``F_GS_RESULT`` 型の配列を指定します。

    パラメータ **nresults** にはサーチ回答数を指定します。
    None を指定した場合は可能であれば自動的にサーチ回答数を決定します。
    
    パラメータ **show_no**, **show_score** により、
    それぞれサーチ回答番号、サーチスコアの表示可否を指定できます。
    True を設定すると各項目を表示し、 False を設定すると非表示となります。

    パラメータ **font_size** にはプロットで使用するポイント単位のフォントサイズを指定します。
    None を指定した場合は自動的にフォントサイズが決定されます。

    :param hgs_pat:        グレイサーチパターンオブジェクトを指定します。
    :param results:        グレイサーチの回答を表す ``F_GS_RESULT`` 型の配列を指定します。
    :param nresults:       グレイサーチのサーチ回答の個数を指定します。None を指定した場合は可能であれば自動的にサーチ回答数を決定します。
    :param plot_obj:       プロットを行う |figure| もしくは |axes| を指定します。
                            None を指定した場合はカレント |axes| が使用されます。
    :param show_no:        サーチ回答番号を表示する場合は True を、表示しない場合は False を指定します。
    :param show_score:     サーチスコアを表示する場合は True を、表示しない場合は False を指定します。
    :param font_size:      プロットで使用するポイント単位のフォントサイズを指定します。
                            None を指定した場合は自動的にフォントサイズが決定されます。
    :param no_props:       サーチ回答番号を表示する際に |pyplot| のプロット関数に渡すキーワード引数を指定します。
    :param score_props:    サーチスコアを表示する際に |pyplot| のプロット関数に渡すキーワード引数を指定します。
    :param bbox_props:     バウンディングボックスを表示する際に |pyplot| のプロット関数に渡すキーワード引数を指定します。
    :param point_props:    マッチング回答位置を表示する際に |pyplot| のプロット関数に渡すキーワード引数を指定します。

    :return: プロットが行われた |axes| を返します。"""

    if not hasattr(hgs_pat, "objtag") or hgs_pat.objtag != fie.F_OBJID_GS_PATTERN:
        raise ValueError("hgs_pat ({}) is not a pattern object of gray search".format(hgs_pat.objtag))
    if isinstance(results, fie.F_GS_RESULT):
        results = [results]
    
    if nresults is None:
        try:
            nresults = len(results)
        except:
            raise ValueError("nresults is required to be specified")
    
    if no_props is None:
        no_props = {}
    if score_props is None:
        score_props = {}
    if bbox_props is None:
        bbox_props = {}
    if point_props is None:
        point_props = {}
    
    plot_obj = _pyplot_util.get_figure(plot_obj)
    axes = _pyplot_util.get_axes(plot_obj)
    
    if not axes.yaxis_inverted():
        axes.invert_yaxis()
    axes.set_aspect('equal')
    
    pat_w, pat_h, offset_x, offset_y = fie._GsResultProtocol._get_pattern_and_offset_size(hgs_pat)
    
    plot_scale = _determine_plot_scale(axes)
    
    if font_size is None:
        font_size = _get_decent_font_size(axes)
    
    # bboxes
    for res_no in range(nresults):
        res = results[res_no]
        if not isinstance(res, fie.F_GS_RESULT):
            raise TypeError(f"{res_no}-th element of results is not an F_SEARCH_RESULT")

        x, y, score = res.x / 100, res.y / 100, res.score
        xmin = x - offset_x
        ymin = y - offset_y
        
        point_props_extended = dict(zorder=4, color="red", marker=(4, 2, 0))
        point_props_extended.update(point_props)
        _pyplot_util.draw_points(x, y, plot_obj=plot_obj, **point_props_extended)
        bbox_props_extended = dict(fill=False, edgecolor='blue', lw=1)
        bbox_props_extended.update(bbox_props)
        axes.add_patch(patches.Rectangle((xmin, ymin), pat_w, pat_h, **bbox_props_extended))
        
        if show_score:
            pad_size = 3
            shift = _point_to_inch(pad_size + 1, axes.figure.dpi) / plot_scale
            score_props_extended = dict(
                size=font_size, ha="left", va="bottom", color="yellow", fontweight="bold",
                bbox={'facecolor': "black", 'pad': pad_size, 'linewidth': 0})
            score_props_extended.update(score_props)
            axes.text(
                x + shift, y - shift,
                str(res.score), **score_props_extended)
        
        if show_no:
            pad_size = 3
            shift = _point_to_inch(pad_size + 1, axes.figure.dpi) / plot_scale
            no_props_extended = dict(
                size=font_size, ha="left", va="bottom", color="red", fontweight="bold",
                bbox={'pad': pad_size, 'facecolor': "black"})
            no_props_extended.update(no_props)
            axes.text(
                xmin + shift, ymin - shift,
                str(res_no), **no_props_extended)

    return axes

# FPM

def plot_fpm_results(
    hfpm, results, plot_obj=None, show_no=True, show_text=True,
    show_edges=True, show_relative_edges=True, err_wide=1, font_size=None,
    no_props=None, score_props=None, pose_props=None, pose_format="{q:.1f}° {s:.0f}%",
    edges_props=None, relative_edges_props=None, bbox_props=None, point_props=None):
    """FPM(特徴点応用マッチング)のサーチ回答のプロットを行います。

    パラメータ **hfpm** にFPMオブジェクトを、 **results** にサーチ回答を表す ``F_SEARCH_RESULT`` 型の配列を指定します。
    指定するFPMオブジェクトは、マッチング処理（ ``fnFIE_fpm_matching()`` など）を実行済みである必要があります。
    
    パラメータ **show_no**, **show_text**, **show_edges**, **show_relative_edges** により、
    それぞれサーチ回答番号、位置姿勢とサーチスコアのテキスト表示、エッジ情報、対応エッジ情報の表示可否を指定できます。
    True を設定すると各項目を表示し、 False を設定すると非表示となります。

    パラメータ **err_wide** には対応エッジ情報を取得する際に使用する誤差範囲を0以上の整数で指定します。

    パラメータ **font_size** にはプロットで使用するポイント単位のフォントサイズを指定します。
    None を指定した場合は自動的にフォントサイズが決定されます。

    パラメータ **pose_format** は位置姿勢のテキスト表示のためのフォーマット文字列を指定します。
    q が度数単位の角度、 s がパーセント単位のスケール値です。

    :param hfpm:           FPMオブジェクトを指定します。
    :param results:        FPMのサーチ回答を表す ``F_SEARCH_RESULT`` 型の配列を指定します。
    :param plot_obj:       プロットを行う |figure| もしくは |axes| を指定します。
                            None を指定した場合はカレント |axes| が使用されます。
    :param show_no:        サーチ回答番号を表示する場合は True を、表示しない場合は False を指定します。
    :param show_text:      位置姿勢とサーチスコアを表示する場合は True を、表示しない場合は False を指定します。
    :param show_edges:     エッジ情報を表示する場合は True を、表示しない場合は False を指定します。
    :param show_relative_edges:    対応エッジ情報を表示する場合は True を、表示しない場合は False を指定します。
    :param err_wide:       対応エッジ情報を取得する際に使用する誤差範囲を0以上の整数で指定します。
    :param font_size:      プロットで使用するフォントサイズをポイント単位で指定します。
                            None を指定した場合は自動的にフォントサイズが決定されます。
    :param no_props:       サーチ回答番号を表示する際に |pyplot| のプロット関数に渡すキーワード引数を指定します。
    :param score_props:    サーチスコアを表示する際に |pyplot| のプロット関数に渡すキーワード引数を指定します。
    :param pose_props:     位置姿勢を表示する際に |pyplot| のプロット関数に渡すキーワード引数を指定します。
    :param edges_props:    エッジ情報を表示する際に |pyplot| のプロット関数に渡すキーワード引数を指定します。
    :param pose_format:    位置姿勢のテキスト表示のためのフォーマット文字列を指定します。
    :param relative_edges_props:    対応エッジ情報を表示する際に |pyplot| のプロット関数に渡すキーワード引数を指定します。
    :param bbox_props:     バウンディングボックスを表示する際に |pyplot| のプロット関数に渡すキーワード引数を指定します。
    :param point_props:    マッチング回答位置を表示する際に |pyplot| のプロット関数に渡すキーワード引数を指定します。

    :return: プロットが行われた |axes| を返します。"""

    if not hasattr(hfpm, "objtag") or hfpm.objtag != fie.F_OBJID_FPM:
        raise ValueError("hfpm ({}) is not an FPM object".format(hfpm.objtag))

    if isinstance(results, fie.F_SEARCH_RESULT):
        results = [results]
    
    max_nresults = 10000
    try:
        max_nresults = len(results)
        nresults = max_nresults
    except:
        pass
    
    if no_props is None:
        no_props = {}
    if score_props is None:
        score_props = {}
    if pose_props is None:
        pose_props = {}
    if edges_props is None:
        edges_props = {}
    if relative_edges_props is None:
        relative_edges_props = {}
    if bbox_props is None:
        bbox_props = {}
    if point_props is None:
        point_props = {}

    plot_obj = _pyplot_util.get_figure(plot_obj)
    axes = _pyplot_util.get_axes(plot_obj)
    
    if not axes.yaxis_inverted():
        axes.invert_yaxis()
    axes.set_aspect('equal')
    
    pat_w, pat_h, ptn_offset = fie._SearchResultProtocol._get_pattern_and_offset_size(hfpm)
    
    plot_scale = _determine_plot_scale(axes)
    
    if font_size is None:
        font_size = _get_decent_font_size(axes)
    
    # edges
    nedges = fie.INT()
    err = fie.fnFIE_fpm_get_matching_feature_num(hfpm, nedges)
    if err != fie.F_ERR_NONE:
        raise RuntimeError("fnFIE_fpm_get_matching_feature_num")
    # print(nedges)
    edges = fie.F_DEDGE.ARRAY(nedges)
    err = fie.fnFIE_fpm_get_matching_feature_edges(hfpm, edges)
    if err != fie.F_ERR_NONE:
        raise RuntimeError("fnFIE_fpm_get_matching_feature_edges")
    if show_edges:
        edges_props_extended = dict(s=1)
        edges_props_extended.update(edges_props)
        edges.plot(plot_obj=plot_obj, **edges_props_extended)
    nrel_edges = fie.INT()
    rel_edges = fie.F_DEDGE.ARRAY(nedges)
    for res_no in range(max_nresults):
        try:
            err = fie.fnFIE_fpm_get_relative_edge(hfpm, res_no, err_wide, rel_edges, nrel_edges)
        except RuntimeError as e:
            if "F_ERR_INVALID_PARAM" in str(e.args[0]):
                err = fie.F_ERR_INVALID_PARAM
            else:
                # unknown error
                raise e
        if err == fie.F_ERR_INVALID_PARAM:
            nresults = res_no
            break
        if show_relative_edges:
            rel_props_extended = dict(s=2)
            rel_props_extended.update(relative_edges_props)
            rel_edges.plot(num=nrel_edges, plot_obj=plot_obj, **rel_props_extended)
            
    for res_no in range(nresults):
        try:
            result = results[res_no]
        except TypeError:
            raise TypeError(f"Failed to get {res_no}-th element of results")
        if not isinstance(result, fie.F_SEARCH_RESULT):
            raise TypeError(f"{res_no}-th element of results is not an F_SEARCH_RESULT")
    
    # bboxes
    for res_no in range(nresults):
        res = results[res_no]
        x, y, q, s = res.x, res.y, res.q, res.s
        bbox = fie._SearchResultProtocol._get_bbox(x, y, q, s, pat_w, pat_h, ptn_offset)
        
        point_props_extended = dict(zorder=4, color="red", marker=(4, 2, -q))
        point_props_extended.update(point_props)
        _pyplot_util.draw_points(x, y, plot_obj=plot_obj, **point_props_extended)
        bbox_props_extended = dict(fill=False, edgecolor='blue', lw=1)
        bbox_props_extended.update(bbox_props)
        axes.fill(*zip(*bbox), **bbox_props_extended)
        
        bbox_tl = bbox[0]
        q_rad = (q + 0) * math.pi / 180
        unitvec_l = (math.cos(q_rad), math.sin(q_rad))
        unitvec_b = (-unitvec_l[1], unitvec_l[0])
        
        if show_text:
            pad_size = 3
            shift_l = _point_to_inch(pad_size, axes.figure.dpi) / plot_scale
            shift_b = shift_l
            pose_props_extended = dict(
                size=font_size, ha="left", va="top", color="lime", fontweight="bold",
                bbox={'facecolor': "black", 'pad': pad_size, 'linewidth': 0},
                rotation=-q, rotation_mode='anchor')
            pose_props_extended.update(pose_props)
            axes.text(
                x + shift_l * unitvec_l[0] + shift_b * unitvec_b[0], y + shift_l * unitvec_l[1] + shift_b * unitvec_b[1],
                pose_format.format(q=q, s=s), **pose_props_extended)
        
        if show_text:
            pad_size = 3
            shift_l =  _point_to_inch(pad_size, axes.figure.dpi) / plot_scale
            shift_b = -shift_l
            score_props_extended = dict(
                size=font_size, ha="left", va="bottom", color="yellow", fontweight="bold",
                bbox={'facecolor': "black", 'pad': pad_size, 'linewidth': 0},
                rotation=-q, rotation_mode='anchor')
            score_props_extended.update(score_props)
            axes.text(
                x + shift_l * unitvec_l[0] + shift_b * unitvec_b[0], y + shift_l * unitvec_l[1] + shift_b * unitvec_b[1],
                str(res.score), **score_props_extended)
        
        if show_no:
            pad_size = 3
            shift = 0
            no_props_extended = dict(
                size=font_size, ha="left", va="bottom", color="red", fontweight="bold",
                bbox={'pad': pad_size, 'facecolor': "black"},
                rotation_mode='anchor')
            no_props_extended.update(no_props)
            axes.text(
                bbox_tl[0] - shift * unitvec_b[0], bbox_tl[1] - shift * unitvec_b[1],
                str(res_no), **no_props_extended)

    return axes

# 2値ブロブ解析

def _get_blob_prop(hmeasure, blobno, feature_type):
    def get_1(func, value_type):
        v = value_type()
        err = func(hmeasure, blobno, v)
        if err != fie.F_ERR_NONE:
            raise RuntimeError("faild to get a blob property")
        return v
    def get_d(func):
        return get_1(func, fie.DOUBLE)
    def get_ui(func):
        return get_1(func, fie.UINT)

    def get_n(func, value_types, idx):
        vs = [value_type() for value_type in value_types]
        err = func(hmeasure, blobno, *vs)
        if err != fie.F_ERR_NONE:
            raise RuntimeError("faild to get blob properties")
        return vs[idx]
    def get_i2(func, idx):
        return get_n(func, [fie.INT] * 2, idx)
    def get_i4(func, idx):
        return get_n(func, [fie.INT] * 4, idx)
    def get_ll2(func, idx):
        return get_n(func, [fie.DLONG] * 2, idx)
    def get_d2(func, idx):
        return get_n(func, [fie.DOUBLE] * 2, idx)
    def get_d3(func, idx):
        return get_n(func, [fie.DOUBLE] * 3, idx)
    def get_d4(func, idx):
        return get_n(func, [fie.DOUBLE] * 4, idx)

    def get_hu_moment(idx):
        hu = fie.DOUBLE.ARRAY(7)
        fie.fnFIE_measure_get_hu_moments(hmeasure, blobno, hu)
        return hu[idx]

    if feature_type == fie.F_FEATURE_COLOR:
        return get_ui(fie.fnFIE_measure_get_color)
    elif feature_type == fie.F_FEATURE_XMIN:
        return get_i4(fie.fnFIE_measure_get_xyrange, 0)
    elif feature_type == fie.F_FEATURE_YMIN:
        return get_i4(fie.fnFIE_measure_get_xyrange, 1)
    elif feature_type == fie.F_FEATURE_XMAX:
        return get_i4(fie.fnFIE_measure_get_xyrange, 2)
    elif feature_type == fie.F_FEATURE_YMAX:
        return get_i4(fie.fnFIE_measure_get_xyrange, 3)
    elif feature_type == fie.F_FEATURE_XMIN_AT_YMIN:
        return get_i4(fie.fnFIE_measure_get_maxminpos, 0)
    elif feature_type == fie.F_FEATURE_XMAX_AT_YMAX:
        return get_i4(fie.fnFIE_measure_get_maxminpos, 1)
    elif feature_type == fie.F_FEATURE_YMIN_AT_XMAX:
        return get_i4(fie.fnFIE_measure_get_maxminpos, 2)
    elif feature_type == fie.F_FEATURE_YMAX_AT_XMIN:
        return get_i4(fie.fnFIE_measure_get_maxminpos, 3)
    elif feature_type == fie.F_FEATURE_XDIFF:
        return get_i2(fie.fnFIE_measure_get_xydiff, 0)
    elif feature_type == fie.F_FEATURE_YDIFF:
        return get_i2(fie.fnFIE_measure_get_xydiff, 1)
    elif feature_type == fie.F_FEATURE_M10:
        assert feature_type == fie.F_FEATURE_SUMX
        return get_ll2(fie.fnFIE_measure_get_moment1, 0)
    elif feature_type == fie.F_FEATURE_M01:
        assert feature_type == fie.F_FEATURE_SUMY
        return get_ll2(fie.fnFIE_measure_get_moment1, 1)
    elif feature_type == fie.F_FEATURE_M20:
        assert feature_type == fie.F_FEATURE_SUMX2
        return get_n(fie.fnFIE_measure_get_moment2, [fie.UDLONG, fie.UDLONG, fie.DLONG], 0)
    elif feature_type == fie.F_FEATURE_M02:
        assert feature_type == fie.F_FEATURE_SUMY2
        return get_n(fie.fnFIE_measure_get_moment2, [fie.UDLONG, fie.UDLONG, fie.DLONG], 1)
    elif feature_type == fie.F_FEATURE_M11:
        assert feature_type == fie.F_FEATURE_SUMXY
        return get_n(fie.fnFIE_measure_get_moment2, [fie.UDLONG, fie.UDLONG, fie.DLONG], 2)
    elif feature_type == fie.F_FEATURE_AREA:
        return get_ui(fie.fnFIE_measure_get_area)
    elif feature_type == fie.F_FEATURE_CENTERX:
        return get_d2(fie.fnFIE_measure_get_center, 0)
    elif feature_type == fie.F_FEATURE_CENTERY:
        return get_d2(fie.fnFIE_measure_get_center, 1)
    elif feature_type == fie.F_FEATURE_RECT1AREA:
        return get_ui(fie.fnFIE_measure_get_rect1_area)
    elif feature_type == fie.F_FEATURE_RECT1LRATIO:
        return get_d(fie.fnFIE_measure_get_rect1_lratio)
    elif feature_type == fie.F_FEATURE_RECT1SRATIO:
        return get_d(fie.fnFIE_measure_get_rect1_sratio)
    elif feature_type == fie.F_FEATURE_LSIZE:
        return get_d2(fie.fnFIE_measure_get_rect2_size, 0)
    elif feature_type == fie.F_FEATURE_WSIZE:
        return get_d2(fie.fnFIE_measure_get_rect2_size, 1)
    elif feature_type == fie.F_FEATURE_RECT2AREA:
        return get_d(fie.fnFIE_measure_get_rect2_area)
    elif feature_type == fie.F_FEATURE_RECT2LRATIO:
        return get_d(fie.fnFIE_measure_get_rect2_lratio)
    elif feature_type == fie.F_FEATURE_RECT2SRATIO:
        return get_d(fie.fnFIE_measure_get_rect2_sratio)
    elif feature_type == fie.F_FEATURE_MAJORAXIS:
        return get_d4(fie.fnFIE_measure_get_equivalent_ellipse, 0)
    elif feature_type == fie.F_FEATURE_MINORAXIS:
        return get_d4(fie.fnFIE_measure_get_equivalent_ellipse, 1)
    elif feature_type in (fie.F_FEATURE_AXISTHETA, fie.F_FEATURE_AXISTHETA_CYCLIC):
        return get_d4(fie.fnFIE_measure_get_equivalent_ellipse, 2)
    elif feature_type == fie.F_FEATURE_AXISRATIO:
        return get_d4(fie.fnFIE_measure_get_equivalent_ellipse, 3)
    elif feature_type == fie.F_FEATURE_DIAMETER_EQUIDISK:
        return get_d(fie.fnFIE_measure_get_equivalent_disk)
    elif feature_type == fie.F_FEATURE_DIAMETER_EQUICIRCLE:
        return get_d(fie.fnFIE_measure_get_equivalent_circle)
    elif feature_type == fie.F_FEATURE_CIRCULARITY1:
        return get_d(fie.fnFIE_measure_get_circularity1)
    elif feature_type == fie.F_FEATURE_CIRCULARITY2:
        return get_d(fie.fnFIE_measure_get_circularity2)
    elif feature_type == fie.F_FEATURE_CIRCULARITY3:
        return get_d(fie.fnFIE_measure_get_circularity3)
    elif feature_type == fie.F_FEATURE_CONVEX_AREA:
        return get_d2(fie.fnFIE_measure_get_convexfeature, 0)
    elif feature_type == fie.F_FEATURE_CONVEX_PERIM:
        return get_d2(fie.fnFIE_measure_get_convexfeature, 1)
    elif feature_type == fie.F_FEATURE_CONVEX_AREARATIO:
        return get_d2(fie.fnFIE_measure_get_convexratio, 0)
    elif feature_type == fie.F_FEATURE_CONVEX_PERIMRATIO:
        return get_d2(fie.fnFIE_measure_get_convexratio, 1)
    elif feature_type == fie.F_FEATURE_FERET_MAX:
        return get_d4(fie.fnFIE_measure_get_feret_diameter_maxmin, 0)
    elif feature_type == fie.F_FEATURE_FERET_MIN:
        return get_d4(fie.fnFIE_measure_get_feret_diameter_maxmin, 2)
    elif feature_type in (fie.F_FEATURE_FMAX_THETA, fie.F_FEATURE_FMAX_THETA_CYCLIC):
        return get_d4(fie.fnFIE_measure_get_feret_diameter_maxmin, 1)
    elif feature_type in (fie.F_FEATURE_FMIN_THETA, fie.F_FEATURE_FMIN_THETA_CYCLIC):
        return get_d4(fie.fnFIE_measure_get_feret_diameter_maxmin, 3)
    elif feature_type == fie.F_FEATURE_DPMIN:
        return get_d4(fie.fnFIE_measure_get_distance_to_boundary, 1)
    elif feature_type == fie.F_FEATURE_DPMAX:
        return get_d4(fie.fnFIE_measure_get_distance_to_boundary, 0)
    elif feature_type == fie.F_FEATURE_DPAVE:
        return get_d4(fie.fnFIE_measure_get_distance_to_boundary, 2)
    elif feature_type == fie.F_FEATURE_DPSIGMA:
        return get_d4(fie.fnFIE_measure_get_distance_to_boundary, 3)
    elif feature_type == fie.F_FEATURE_DCMAX:
        return get_d3(fie.fnFIE_measure_get_distance_to_childs, 0)
    elif feature_type == fie.F_FEATURE_DCMIN:
        return get_d3(fie.fnFIE_measure_get_distance_to_childs, 1)
    elif feature_type == fie.F_FEATURE_DCAVE:
        return get_d3(fie.fnFIE_measure_get_distance_to_childs, 2)
    elif feature_type == fie.F_FEATURE_DSMAX:
        return get_d3(fie.fnFIE_measure_get_distance_to_siblings, 0)
    elif feature_type == fie.F_FEATURE_DSMIN:
        return get_d3(fie.fnFIE_measure_get_distance_to_siblings, 1)
    elif feature_type == fie.F_FEATURE_DSAVE:
        return get_d3(fie.fnFIE_measure_get_distance_to_siblings, 2)
    elif feature_type == fie.F_FEATURE_NS:
        return get_ui(fie.fnFIE_measure_get_sibling_num)
    elif feature_type == fie.F_FEATURE_PERIM:
        return get_d(fie.fnFIE_measure_get_perimeter)
    elif feature_type == fie.F_FEATURE_ST:
        return get_ui(fie.fnFIE_measure_get_area_with_hole)
    elif feature_type == fie.F_FEATURE_SC:
        return get_ui(fie.fnFIE_measure_get_hole_area)
    elif feature_type == fie.F_FEATURE_HOLES:
        return get_ui(fie.fnFIE_measure_get_hole_num)
    elif feature_type == fie.F_FEATURE_HRATIO:
        return get_d(fie.fnFIE_measure_get_hole_ratio)
    elif feature_type == fie.F_FEATURE_PPS:
        return get_d(fie.fnFIE_measure_get_pps)
    # elif feature_type == fie.F_FEATURE_AXISTHETA_CYCLIC:
    # elif feature_type == fie.F_FEATURE_FMAX_THETA_CYCLIC:
    # elif feature_type == fie.F_FEATURE_FMIN_THETA_CYCLIC:
    #     pass
    elif feature_type == fie.F_FEATURE_M30:
        return get_d4(fie.fnFIE_measure_get_moment3, 0)
    elif feature_type == fie.F_FEATURE_M03:
        return get_d4(fie.fnFIE_measure_get_moment3, 1)
    elif feature_type == fie.F_FEATURE_M21:
        return get_d4(fie.fnFIE_measure_get_moment3, 2)
    elif feature_type == fie.F_FEATURE_M12:
        return get_d4(fie.fnFIE_measure_get_moment3, 3)
    elif feature_type == fie.F_FEATURE_MG20:
        return get_d3(fie.fnFIE_measure_get_central_moment2, 0)
    elif feature_type == fie.F_FEATURE_MG02:
        return get_d3(fie.fnFIE_measure_get_central_moment2, 1)
    elif feature_type == fie.F_FEATURE_MG11:
        return get_d3(fie.fnFIE_measure_get_central_moment2, 2)
    elif feature_type == fie.F_FEATURE_MG30:
        return get_d4(fie.fnFIE_measure_get_central_moment3, 0)
    elif feature_type == fie.F_FEATURE_MG03:
        return get_d4(fie.fnFIE_measure_get_central_moment3, 1)
    elif feature_type == fie.F_FEATURE_MG21:
        return get_d4(fie.fnFIE_measure_get_central_moment3, 2)
    elif feature_type == fie.F_FEATURE_MG12:
        return get_d4(fie.fnFIE_measure_get_central_moment3, 3)
    elif feature_type == fie.F_FEATURE_HU_MOMENT0:
        return get_hu_moment(0)
    elif feature_type == fie.F_FEATURE_HU_MOMENT1:
        return get_hu_moment(1)
    elif feature_type == fie.F_FEATURE_HU_MOMENT2:
        return get_hu_moment(2)
    elif feature_type == fie.F_FEATURE_HU_MOMENT3:
        return get_hu_moment(3)
    elif feature_type == fie.F_FEATURE_HU_MOMENT4:
        return get_hu_moment(4)
    elif feature_type == fie.F_FEATURE_HU_MOMENT5:
        return get_hu_moment(5)
    elif feature_type == fie.F_FEATURE_HU_MOMENT6:
        return get_hu_moment(6)
    else:
        raise ValueError("Unknown feature type: " + feature_type)

def _get_blob_prop_format(feature_type):
    if feature_type in (
        fie.F_FEATURE_COLOR,
        fie.F_FEATURE_XMIN,
        fie.F_FEATURE_YMIN,
        fie.F_FEATURE_XMAX,
        fie.F_FEATURE_YMAX,
        fie.F_FEATURE_XMIN_AT_YMIN,
        fie.F_FEATURE_XMAX_AT_YMAX,
        fie.F_FEATURE_YMIN_AT_XMAX,
        fie.F_FEATURE_YMAX_AT_XMIN,
        fie.F_FEATURE_XDIFF,
        fie.F_FEATURE_YDIFF,
        fie.F_FEATURE_M10,
        fie.F_FEATURE_SUMX,
        fie.F_FEATURE_M01,
        fie.F_FEATURE_SUMY,
        fie.F_FEATURE_M20,
        fie.F_FEATURE_SUMX2,
        fie.F_FEATURE_M02,
        fie.F_FEATURE_SUMY2,
        fie.F_FEATURE_M11,
        fie.F_FEATURE_SUMXY,
        fie.F_FEATURE_AREA,
        fie.F_FEATURE_RECT1AREA,
        fie.F_FEATURE_NS,
        fie.F_FEATURE_ST,
        fie.F_FEATURE_SC,
        fie.F_FEATURE_HOLES,
    ):
        # int features
        return "{:d}"
    elif feature_type in (
        fie.F_FEATURE_CENTERX,
        fie.F_FEATURE_CENTERY,
        fie.F_FEATURE_LSIZE,
        fie.F_FEATURE_WSIZE,
        fie.F_FEATURE_RECT2AREA,
        fie.F_FEATURE_MAJORAXIS,
        fie.F_FEATURE_MINORAXIS,
        fie.F_FEATURE_DIAMETER_EQUIDISK,
        fie.F_FEATURE_DIAMETER_EQUICIRCLE,
        fie.F_FEATURE_CONVEX_AREA,
        fie.F_FEATURE_CONVEX_PERIM,
        fie.F_FEATURE_FERET_MAX,
        fie.F_FEATURE_FERET_MIN,
        fie.F_FEATURE_DPMIN,
        fie.F_FEATURE_DPMAX,
        fie.F_FEATURE_DPAVE,
        fie.F_FEATURE_DPSIGMA,
        fie.F_FEATURE_DCMAX,
        fie.F_FEATURE_DCMIN,
        fie.F_FEATURE_DCAVE,
        fie.F_FEATURE_DSMAX,
        fie.F_FEATURE_DSMIN,
        fie.F_FEATURE_DSAVE,
        fie.F_FEATURE_PERIM,
        fie.F_FEATURE_PPS,
    ):
        # floats in medium value range
        return "{:.2f}"
    elif feature_type in (
        fie.F_FEATURE_RECT1LRATIO,
        fie.F_FEATURE_RECT1SRATIO,
        fie.F_FEATURE_RECT2LRATIO,
        fie.F_FEATURE_RECT2SRATIO,
        fie.F_FEATURE_AXISTHETA,
        fie.F_FEATURE_AXISRATIO,
        fie.F_FEATURE_CIRCULARITY1,
        fie.F_FEATURE_CIRCULARITY2,
        fie.F_FEATURE_CIRCULARITY3,
        fie.F_FEATURE_CONVEX_AREARATIO,
        fie.F_FEATURE_CONVEX_PERIMRATIO,
        fie.F_FEATURE_FMAX_THETA,
        fie.F_FEATURE_FMIN_THETA,
        fie.F_FEATURE_HRATIO,
        fie.F_FEATURE_AXISTHETA_CYCLIC,
        fie.F_FEATURE_FMAX_THETA_CYCLIC,
        fie.F_FEATURE_FMIN_THETA_CYCLIC,
    ):
        # floats in small value range
        return "{:.3f}"
    elif feature_type in (
        fie.F_FEATURE_M30,
        fie.F_FEATURE_M03,
        fie.F_FEATURE_M21,
        fie.F_FEATURE_M12,
        fie.F_FEATURE_MG20,
        fie.F_FEATURE_MG02,
        fie.F_FEATURE_MG11,
        fie.F_FEATURE_MG30,
        fie.F_FEATURE_MG03,
        fie.F_FEATURE_MG21,
        fie.F_FEATURE_MG12,
        fie.F_FEATURE_HU_MOMENT0,
        fie.F_FEATURE_HU_MOMENT1,
        fie.F_FEATURE_HU_MOMENT2,
        fie.F_FEATURE_HU_MOMENT3,
        fie.F_FEATURE_HU_MOMENT4,
        fie.F_FEATURE_HU_MOMENT5,
        fie.F_FEATURE_HU_MOMENT6,
    ):
        # floats in very large or very small value range
        return "{:.4g}"
    raise ValueError("Unknown feature type: " + feature_type)

def _get_abbreviated_measure_feature_name(feature_id):
    feature_name = str(fie.f_measure_feature_type(feature_id))
    prefix = "F_FEATURE_"
    if feature_name.startswith(prefix):
        feature_name = feature_name[len(prefix):]
    
    alias_tuples = [
        (fie.F_FEATURE_M10, fie.F_FEATURE_SUMX, "SUMX"),
        (fie.F_FEATURE_M01, fie.F_FEATURE_SUMY, "SUMY"),
        (fie.F_FEATURE_M20, fie.F_FEATURE_SUMX2, "SUMX2"),
        (fie.F_FEATURE_M02, fie.F_FEATURE_SUMY2, "SUMY2"),
        (fie.F_FEATURE_M11, fie.F_FEATURE_SUMXY, "SUMXY"),
    ]
    for base_id, alias_id, alias_name in alias_tuples:
        assert base_id == alias_id
        if feature_id == alias_id:
            feature_name += f" ({alias_name})"
    return feature_name.lower()

def plot_measure_results(
    hmeasure, bloblist, nblobs, plot_obj=None, show_no=True, show_features=True,
    features=[],
    font_size=None,
    no_props=None, feature_props=None, bbox_props=None):
    """2値ブローブ解析結果のプロットを行います。

    パラメータ **hmeasure** にブローブ解析結果オブジェクトを、 **bloblist** にブローブ番号配列を指定します。
    パラメータ **nblobs** にはブローブ数を指定します。
    
    パラメータ **show_no**, **show_features** により、
    それぞれブローブ番号、ブローブ特徴量の表示可否を指定できます。
    True を設定すると各項目を表示し、 False を設定すると非表示となります。

    パラメータ **features** に表示するブローブ特徴量の配列を指定します。
    配列の各要素は ``f_measure_feature_type`` 列挙型の整数値でなければなりません。

    パラメータ **font_size** にはプロットで使用するポイント単位のフォントサイズを指定します。
    None を指定した場合は自動的にフォントサイズが決定されます。

    :param hmeasure:       ブローブ解析結果オブジェクトを指定します。
    :param bloblist:       ブローブ番号配列を指定します。
    :param nblobs:         ブローブ数を指定します。
    :param plot_obj:       プロットを行う |figure| もしくは |axes| を指定します。
                            None を指定した場合はカレント |axes| が使用されます。
    :param show_no:        ブローブ番号を表示する場合は True を、表示しない場合は False を指定します。
    :param show_features:  ブローブ特徴量を表示する場合は True を、表示しない場合は False を指定します。
    :param features:       表示したいブローブ特徴量の配列を指定します。
                            配列の各要素は ``f_measure_feature_type`` 列挙型の整数値でなければなりません。
    :param font_size:      プロットで使用するポイント単位のフォントサイズを指定します。
                            None を指定した場合は自動的にフォントサイズが決定されます。
    :param no_props:       ブローブ番号を表示する際に |pyplot| のプロット関数に渡すキーワード引数を指定します。
    :param feature_props:  ブローブ特徴量を表示する際に |pyplot| のプロット関数に渡すキーワード引数を指定します。
    :param bbox_props:     バウンディングボックスを表示する際に |pyplot| のプロット関数に渡すキーワード引数を指定します。

    :return: プロットが行われた |axes| を返します。"""

    if not hasattr(hmeasure, "objtag") or hmeasure.objtag != fie.F_OBJID_MEASURE_RESULT:
        raise ValueError("hmeasure ({}) is not a Measure Result object".format(hmeasure.objtag))

    if no_props is None:
        no_props = {}
    if feature_props is None:
        feature_props = {}
    if bbox_props is None:
        bbox_props = {}

    plot_obj = fie._pyplot_util.get_figure(plot_obj)
    axes = fie._pyplot_util.get_axes(plot_obj)
    
    if abs(axes.get_ylim()[0] - axes.get_ylim()[1]) <= 1.0:
        # looks like ylim is broken.
        # set decent ylim to avoid "ValueError: Image size of ... pixels is too large..."
        # 見栄えのため、xlimも同様に設定する
        ymax_all = 0
        xmax_all = 0
        for i in range(nblobs):
            blobno = bloblist[i]
            xmin = fie.INT()
            ymin = fie.INT()
            xmax = fie.INT()
            ymax = fie.INT()
            fie.measure_get_xyrange(hmeasure, blobno, xmin, ymin, xmax, ymax)
            xmax_all = max(xmax_all, xmax)
            ymax_all = max(ymax_all, ymax)
        axes.set_xlim(0, xmax_all)
        axes.set_ylim(0, ymax_all)
    
    if not axes.yaxis_inverted():
        axes.invert_yaxis()
    axes.set_aspect('equal')
    
    plot_scale = _determine_plot_scale(axes)
    
    if font_size is None:
        font_size = _get_decent_font_size(axes)
    
    feature_path_effects = [matplotlib.patheffects.withStroke(linewidth=3.0, foreground="#ffffff")]
    
    colors_fg = [
        'b', 'g', 'r', '#007777', 'm', '#666600'
    ]
    
    for i in range(nblobs):
        blobno = bloblist[i]
        # print(bloblist[i])
        color_fg = colors_fg[i % len(colors_fg)]
        
        xmin = fie.INT()
        ymin = fie.INT()
        xmax = fie.INT()
        ymax = fie.INT()
        err = fie.fnFIE_measure_get_xyrange(hmeasure, blobno, xmin, ymin, xmax, ymax)
        if err != fie.F_ERR_NONE:
            raise RuntimeError("fnFIE_measure_get_xyrange")
        bbox_props_extended = dict(fill=False, edgecolor=color_fg, lw=1)
        bbox_props_extended.update(bbox_props)
        axes.add_patch(patches.Rectangle((xmin - 0.5, ymin - 0.5), xmax - xmin + 1, ymax - ymin + 1, **bbox_props_extended))

        pad_size = 2
        if show_no:
            shift = _point_to_inch(pad_size, axes.figure.dpi) / plot_scale
            no_props_extended = dict(
                size=font_size, ha="left", va="bottom", color="white", fontweight="bold",
                bbox={'pad': pad_size, 'facecolor': "darkred", 'linewidth': 0})
            no_props_extended.update(no_props)
            axes.text(
                xmin + shift, ymin - shift,
                str(blobno), **no_props_extended)

        if show_features:
            shift = _point_to_inch(pad_size + 2, axes.figure.dpi) / plot_scale + 1
            feature_strs = []
            for feature_id in features:
                feature_name = _get_abbreviated_measure_feature_name(feature_id)
                feature_val = _get_blob_prop(hmeasure, blobno, feature_id)
                feature_val_str = _get_blob_prop_format(feature_id).format(feature_val)
                feature_strs.append(f"{feature_name}: {feature_val_str}")
            feature_str = "\n".join(feature_strs)
            feature_props_extended = dict(
                size=font_size, ha="left", va="top", color=color_fg, path_effects=feature_path_effects)
            feature_props_extended.update(feature_props)
            axes.text(
                xmin + shift, ymin + shift,
                feature_str, **feature_props_extended)

    return axes

# 1Dバーコード認識

def plot_barcode1d_results(
    hbarcode, plot_obj=None, show_no=True, show_text=True, show_line=True, show_endpoints=True,
    text_encoding="utf-8",
    font_size=None,
    no_props=None, text_props=None, line_props=None, endpoints_props=None):
    """1Dバーコード認識の認識結果のプロットを行います。

    パラメータ **hbarcode** に1Dバーコードオブジェクトを指定します。
    指定する1Dバーコードオブジェクトは ``fnFIE_barcode_execute()`` が実行済みである必要があります。
    
    パラメータ **show_no**, **show_text**, **show_line**, **show_endpoints** により、
    それぞれバーコード番号、認識結果テキスト、バーコード位置を表す線分、バーコードの端点の表示可否を指定できます。
    True を設定すると各項目を表示し、 False を設定すると非表示となります。

    パラメータ **font_size** にはプロットで使用するポイント単位のフォントサイズを指定します。
    None を指定した場合は自動的にフォントサイズが決定されます。

    :param hbarcode:       1Dバーコードオブジェクトを指定します。
    :param plot_obj:       プロットを行う |figure| もしくは |axes| を指定します。
                            None を指定した場合はカレント |axes| が使用されます。
    :param show_no:        バーコード番号を表示する場合は True を、表示しない場合は False を指定します。
    :param show_text:      認識結果テキストを表示する場合は True を、表示しない場合は False を指定します。
    :param show_line:      バーコード位置を表す線分を表示する場合は True を、表示しない場合は False を指定します。
    :param show_endpoints: バーコードの端点を表示する場合は True を、表示しない場合は False を指定します。
    :param text_encoding:  認識結果テキストのエンコーディングを指定します。
    :param font_size:      プロットで使用するポイント単位のフォントサイズを指定します。
                            None を指定した場合は自動的にフォントサイズが決定されます。
    :param no_props:       バーコード番号を表示する際に |pyplot| のプロット関数に渡すキーワード引数を指定します。
    :param text_props:     認識結果テキストを表示する際に |pyplot| のプロット関数に渡すキーワード引数を指定します。
    :param line_props:     バーコード位置を表示する際に |pyplot| のプロット関数に渡すキーワード引数を指定します。
    :param endpoints_props: バーコードの端点を表示する際に |pyplot| のプロット関数に渡すキーワード引数を指定します。

    :return: プロットが行われた |axes| を返します。"""

    if not hasattr(hbarcode, "objtag") or hbarcode.objtag != fie.F_OBJID_BARCODE1D:
        raise ValueError("hbarcode ({}) is not a Barcode 1D object".format(hbarcode.objtag))

    if no_props is None: 
        no_props = {}
    if text_props is None: 
        text_props = {}
    if line_props is None: 
        line_props = {}
    if endpoints_props is None: 
        endpoints_props = {}
    
    plot_obj = fie._pyplot_util.get_figure(plot_obj)
    axes = fie._pyplot_util.get_axes(plot_obj)
    
    if not axes.yaxis_inverted():
        axes.invert_yaxis()
    axes.set_aspect('equal')
    
    plot_scale = _determine_plot_scale(axes)
    
    if font_size is None:
        font_size = _get_decent_font_size(axes)

    num_decoded = fie.INT()

    err = fie.fnFIE_barcode_query_num(hbarcode, num_decoded)
    if err != fie.F_ERR_NONE:
        raise RuntimeError("fnFIE_barcode_query_num")
    
    for i in range(num_decoded):
        # デコードメッセージ取得
        message = fie.CHAR.PTR()
        err = fie.fnFIE_barcode_query_msg(hbarcode, i, message)
        if err != fie.F_ERR_NONE:
            raise RuntimeError("fnFIE_barcode_query_msg")
        message_str = message.value_as_bytes.decode(text_encoding)
        
        # barcode position
        st_x = fie.DOUBLE()
        st_y = fie.DOUBLE()
        ed_x = fie.DOUBLE()
        ed_y = fie.DOUBLE()
        err = fie.fnFIE_barcode_query_start_stop_pos(hbarcode, i, st_x, st_y, ed_x, ed_y)
        if err != fie.F_ERR_NONE:
            raise RuntimeError("fnFIE_barcode_query_start_stop_pos")
        angle = math.atan2(ed_y - st_y, ed_x - st_x)
    
        if show_line:
            line_props_extended = dict(color="blue", lw=3)
            line_props_extended.update(line_props)
            axes.plot([st_x, ed_x], [st_y, ed_y], **line_props_extended)
        
        if show_endpoints:
            endpoints_props_extended = dict(zorder=4, color="red", marker=(4, 2, -math.degrees(angle)))
            endpoints_props_extended.update(endpoints_props)
            fie._pyplot_util.draw_points([st_x, ed_x], [st_y, ed_y], plot_obj=plot_obj, **endpoints_props_extended)

        unitvec_l = (math.cos(angle), math.sin(angle))
        unitvec_b = (-unitvec_l[1], unitvec_l[0])
        
        if show_no:
            pad_size = 3
            shift = _point_to_inch(pad_size + font_size, axes.figure.dpi) / plot_scale
            no_props_extended = dict(
                size=font_size, ha="center", va="center", color="red", fontweight="bold", bbox={'pad': pad_size, 'facecolor': "black"},
                rotation_mode='anchor')
            no_props_extended.update(no_props)
            axes.text(
                st_x - shift * unitvec_b[0], st_y - shift * unitvec_b[1],
                str(i), **no_props_extended)

        if show_text and message_str is not None:
            # get type
            barcode_type = fie.INT()
            err = fie.fnFIE_barcode_query_type(hbarcode, i, barcode_type)
            if err != fie.F_ERR_NONE:
                raise RuntimeError("fnFIE_barcode_query_type")
            type_str = {
                fie.F_BARCODE_EAN13: "EAN-13",
                fie.F_BARCODE_CODE39: "CODE39",
                fie.F_BARCODE_CODE128: "CODE128",
                fie.F_BARCODE_ITF: "ITF",
                fie.F_BARCODE_NW7: "NW-7",
                fie.F_BARCODE_EAN8: "EAN-8",
            }[barcode_type.value]
            
            pad_size = 3
            text_props_extended = dict(
                size=font_size, ha="center", va="center", bbox={'fc': '0.9', 'pad': 4})
            text_props_extended.update(text_props)
            axes.text(
                (st_x + ed_x) / 2, (st_y + ed_y) / 2,
                type_str + ": " + message_str, **text_props_extended)

    return axes

# QRコード認識

def _rotate_corners_to_put_first_elm_tl(corners):
    """多角形の頂点配列を受け取り、最初の要素が最も左上に配置されるように配列を回転させる"""
    tl_vals = [sum(corner) for corner in corners]
    tl_idx = _np.argmin(tl_vals)
    if tl_idx != 0:
        corners = corners[tl_idx:] + corners[:tl_idx]
    return corners

def plot_qrcode_results(
    hqr, plot_obj=None, show_undecoded=False, show_no=True, show_text=True, show_bbox=True, show_cells=True,
    text_encoding="utf-8",
    font_size=None,
    no_props=None, text_props=None, bbox_props=None, cells_props=None, put_text_bottom=True):
    """QRコード認識の認識結果のプロットを行います。

    パラメータ **hqr** にQRコードオブジェクトを指定します。
    指定するQRコードオブジェクトは ``fnFIE_qr_execute()`` が実行済みである必要があります。
    
    パラメータ **show_no**, **show_text**, **show_bbox**, **show_cells** により、
    それぞれQRコードインデックス番号、認識結果テキスト、バウンディングボックス、セル位置情報の表示可否を指定できます。
    True を設定すると各項目を表示し、 False を設定すると非表示となります。

    パラメータ **font_size** にはプロットで使用するポイント単位のフォントサイズを指定します。
    None を指定した場合は自動的にフォントサイズが決定されます。

    :param hqr:            QRコードオブジェクトを指定します。
    :param plot_obj:       プロットを行う |figure| もしくは |axes| を指定します。
                            None を指定した場合はカレント |axes| が使用されます。
    :param show_undecoded: デコードに失敗したQRコードシンボルを表示する場合は True を、表示しない場合は False を指定します。
    :param show_no:        QRコードインデックス番号を表示する場合は True を、表示しない場合は False を指定します。
    :param show_text:      認識結果テキストを表示する場合は True を、表示しない場合は False を指定します。
    :param show_bbox:      バウンディングボックスを表示する場合は True を、表示しない場合は False を指定します。
    :param show_cells:     セル位置情報を表示する場合は True を、表示しない場合は False を指定します。
    :param text_encoding:  認識結果テキストのエンコーディングを指定します。ECIプロトコルによる文字セット設定は無視します。
    :param font_size:      プロットで使用するポイント単位のフォントサイズを指定します。
                            None を指定した場合は自動的にフォントサイズが決定されます。
    :param no_props:       QRコードインデックス番号を表示する際に |pyplot| のプロット関数に渡すキーワード引数を指定します。
    :param text_props:     認識結果テキストを表示する際に |pyplot| のプロット関数に渡すキーワード引数を指定します。
    :param bbox_props:     バウンディングボックスを表示する際に |pyplot| のプロット関数に渡すキーワード引数を指定します。
    :param cells_props:    セル位置情報を表示する際に |pyplot| のプロット関数に渡すキーワード引数を指定します。
    :param put_text_bottom: 認識結果テキストを常に下側に表示する場合は True を、シンボルの向きに合わせて表示する場合は False を指定します。

    :return: プロットが行われた |axes| を返します。
    """

    if not hasattr(hqr, "objtag") or hqr.objtag != fie.F_OBJID_QR2D:
        raise ValueError("hqr ({}) is not a QR code 2D object".format(hqr.objtag))

    if no_props is None: 
        no_props = {}
    if text_props is None: 
        text_props = {}
    if bbox_props is None: 
        bbox_props = {}
    if cells_props is None: 
        cells_props = {}
    
    plot_obj = fie._pyplot_util.get_figure(plot_obj)
    axes = fie._pyplot_util.get_axes(plot_obj)
    
    if not axes.yaxis_inverted():
        axes.invert_yaxis()
    axes.set_aspect('equal')
    
    plot_scale = _determine_plot_scale(axes)
    
    if font_size is None:
        font_size = _get_decent_font_size(axes)

    decoded_indexes_raw = fie.INT.PTR()
    num_decoded = fie.INT()
    undecoded_indexes_raw = fie.INT.PTR()
    num_undecoded = fie.INT()

    err = fie.fnFIE_qr_query_decoded(hqr, decoded_indexes_raw, num_decoded)
    if err != fie.F_ERR_NONE:
        raise RuntimeError("fnFIE_qr_query_decoded")
    err = fie.fnFIE_qr_query_undecoded(hqr, undecoded_indexes_raw, num_undecoded)
    if err != fie.F_ERR_NONE:
        raise RuntimeError("fnFIE_qr_query_undecoded")
    
    decoded_indexes = [di.value for di in decoded_indexes_raw[:num_decoded]]
    undecoded_indexes = [di.value for di in undecoded_indexes_raw[:num_undecoded]]
    
    if show_undecoded:
        ids = decoded_indexes + undecoded_indexes
    else:
        ids = decoded_indexes
    
    for id_ in ids:
        # デコードメッセージ取得
        message = fie.CHAR.PTR()
        if id_ in decoded_indexes:
            err = fie.fnFIE_qr_query_message(hqr, id_, message)
            if err != fie.F_ERR_NONE:
                raise RuntimeError("fnFIE_qr_query_message")
            message_str = message.value_as_bytes.decode(text_encoding)
        else:
            message_str = None
        
        corners_mat = fie.FMATRIX.PTR()
        err = fie.fnFIE_qr_query_delimitingpts(hqr, id_, corners_mat)
        if err != fie.F_ERR_NONE:
            raise RuntimeError("fnFIE_qr_query_delimitingpts")
        corner_step = corners_mat[0].col // 4
        corners = [(corners_mat[0].m[0][i * corner_step], corners_mat[0].m[1][i * corner_step]) for i in range(4)]
        
        if show_cells:
            cells_mat = fie.FMATRIX.PTR()
            fie.fnFIE_qr_query_cellones(hqr, id_, cells_mat)
            if err != fie.F_ERR_NONE:
                raise RuntimeError("fnFIE_qr_query_cellones")
            cell_centers = [(cells_mat[0].m[0][i], cells_mat[0].m[1][i]) for i in range(cells_mat[0].col)]
            cells_props_extended = dict(s=3)
            cells_props_extended.update(cells_props)
            axes.scatter(*zip(*cell_centers), **cells_props_extended)

        if show_bbox:
            bbox_props_extended = dict(fill=False, edgecolor="red")
            bbox_props_extended.update(bbox_props)
            axes.fill(*zip(*corners), **bbox_props_extended)

        if put_text_bottom:
            corners = _rotate_corners_to_put_first_elm_tl(corners)

        corner_top = corners[0]
        corner_bottom = corners[3]
        corner_bottom_right = corners[2]
        bottom_dir = math.atan2(corner_bottom[1] - corner_top[1], corner_bottom[0] - corner_top[0])
        right_dir = math.atan2(corner_bottom_right[1] - corner_bottom[1], corner_bottom_right[0] - corner_bottom[0])
        unitvec_b = (math.cos(bottom_dir), math.sin(bottom_dir))
        
        if show_no:
            pad_size = 3
            shift = _point_to_inch(pad_size + 1, axes.figure.dpi) / plot_scale
            no_props_extended = dict(
                size=font_size, ha="left", va="bottom", color="red", fontweight="bold", bbox={'pad': pad_size, 'facecolor': "black"},
                rotation_mode='anchor')
            no_props_extended.update(no_props)
            axes.text(
                corner_top[0] - shift * unitvec_b[0], corner_top[1] - shift * unitvec_b[1],
                str(id_), **no_props_extended)
        if show_text and message_str is not None:
            pad_size = 4
            shift = _point_to_inch(pad_size + 1, axes.figure.dpi) / plot_scale
            text_props_extended = dict(
                size=font_size, ha="left", va="top", bbox={'fc': '0.9', 'pad': pad_size},
                rotation=-math.degrees(right_dir), rotation_mode='anchor')
            text_props_extended.update(text_props)
            axes.text(
                corner_bottom[0] + shift * unitvec_b[0], corner_bottom[1] + shift * unitvec_b[1],
                message_str, **text_props_extended)

    return axes

# データマトリックス認識

def plot_datamatrix_results(
    hdm, plot_obj=None, show_undecoded=False, show_no=True, show_text=True, show_bbox=True, show_cells=True,
    text_encoding="utf-8",
    font_size=None,
    no_props=None, text_props=None, bbox_props=None, cells_props=None, put_text_bottom=True):
    """データマトリックス認識の認識結果のプロットを行います。

    パラメータ **hdm** にデータマトリックスオブジェクトを指定します。
    指定するデータマトリックスオブジェクトは ``fnFIE_dm_execute()`` が実行済みである必要があります。
    
    パラメータ **show_no**, **show_text**, **show_bbox**, **show_cells** により、
    それぞれデータマトリックスインデックス番号、認識結果テキスト、バウンディングボックス、セル位置情報の表示可否を指定できます。
    True を設定すると各項目を表示し、 False を設定すると非表示となります。

    パラメータ **font_size** にはプロットで使用するポイント単位のフォントサイズを指定します。
    None を指定した場合は自動的にフォントサイズが決定されます。

    :param hdm:            データマトリックスオブジェクトを指定します。
    :param plot_obj:       プロットを行う |figure| もしくは |axes| を指定します。
                            None を指定した場合はカレント |axes| が使用されます。
    :param show_undecoded: デコードに失敗したデータマトリックスシンボルを表示する場合は True を、表示しない場合は False を指定します。
    :param show_no:        データマトリックスインデックス番号を表示する場合は True を、表示しない場合は False を指定します。
    :param show_text:      認識結果テキストを表示する場合は True を、表示しない場合は False を指定します。
    :param show_bbox:      バウンディングボックスを表示する場合は True を、表示しない場合は False を指定します。
    :param show_cells:     セル位置情報を表示する場合は True を、表示しない場合は False を指定します。
    :param text_encoding:  認識結果テキストのエンコーディングを指定します。ECIプロトコルによる文字セット設定は無視します。
    :param font_size:      プロットで使用するポイント単位のフォントサイズを指定します。
                            None を指定した場合は自動的にフォントサイズが決定されます。
    :param no_props:       データマトリックスインデックス番号を表示する際に |pyplot| のプロット関数に渡すキーワード引数を指定します。
    :param text_props:     認識結果テキストを表示する際に |pyplot| のプロット関数に渡すキーワード引数を指定します。
    :param bbox_props:     バウンディングボックスを表示する際に |pyplot| のプロット関数に渡すキーワード引数を指定します。
    :param cells_props:    セル位置情報を表示する際に |pyplot| のプロット関数に渡すキーワード引数を指定します。
    :param put_text_bottom: 認識結果テキストを常に下側に表示する場合は True を、シンボルの向きに合わせて表示する場合は False を指定します。

    :return: プロットが行われた |axes| を返します。
    """

    if not hasattr(hdm, "objtag") or hdm.objtag != fie.F_OBJID_DATAMATRIX:
        raise ValueError("hdm ({}) is not a DataMatrix object".format(hdm.objtag))

    if no_props is None: 
        no_props = {}
    if text_props is None: 
        text_props = {}
    if bbox_props is None: 
        bbox_props = {}
    if cells_props is None: 
        cells_props = {}
    
    plot_obj = fie._pyplot_util.get_figure(plot_obj)
    axes = fie._pyplot_util.get_axes(plot_obj)
    
    if not axes.yaxis_inverted():
        axes.invert_yaxis()
    axes.set_aspect('equal')
    
    plot_scale = _determine_plot_scale(axes)
    
    if font_size is None:
        font_size = _get_decent_font_size(axes)

    decoded_indexes_raw = fie.INT.PTR()
    num_decoded = fie.INT()
    undecoded_indexes_raw = fie.INT.PTR()
    num_undecoded = fie.INT()

    err = fie.fnFIE_dm_query_decoded(hdm, decoded_indexes_raw, num_decoded)
    if err != fie.F_ERR_NONE:
        raise RuntimeError("fnFIE_dm_query_decoded")
    err = fie.fnFIE_dm_query_undecoded(hdm, undecoded_indexes_raw, num_undecoded)
    if err != fie.F_ERR_NONE:
        raise RuntimeError("fnFIE_dm_query_undecoded")
    
    decoded_indexes = [di.value for di in decoded_indexes_raw[:num_decoded]]
    undecoded_indexes = [di.value for di in undecoded_indexes_raw[:num_undecoded]]
    
    if show_undecoded:
        ids = decoded_indexes + undecoded_indexes
    else:
        ids = decoded_indexes
    
    for id_ in ids:
        # デコードメッセージ取得
        message = fie.CHAR.PTR()
        if id_ in decoded_indexes:
            err = fie.fnFIE_dm_query_message(hdm, id_, message, None)
            if err != fie.F_ERR_NONE:
                raise RuntimeError("fnFIE_dm_query_message")
            message_str = message.value_as_bytes.decode(text_encoding)
        else:
            message_str = None
        
        corners_mat = fie.FMATRIX.PTR()
        err = fie.fnFIE_dm_query_corner(hdm, id_, corners_mat)
        if err != fie.F_ERR_NONE:
            raise RuntimeError("fnFIE_dm_query_corner")
        corners = [(corners_mat[0].m[0][i], corners_mat[0].m[1][i]) for i in range(4)]
        
        if show_cells:
            cells_mat = fie.FMATRIX.PTR()
            fie.fnFIE_dm_query_cellones(hdm, id_, cells_mat)
            if err != fie.F_ERR_NONE:
                raise RuntimeError("fnFIE_dm_query_cellones")
            cell_centers = [(cells_mat[0].m[0][i], cells_mat[0].m[1][i]) for i in range(cells_mat[0].col)]
            cells_props_extended = dict(s=3)
            cells_props_extended.update(cells_props)
            axes.scatter(*zip(*cell_centers), **cells_props_extended)

        if show_bbox:
            bbox_props_extended = dict(fill=False, edgecolor="red")
            bbox_props_extended.update(bbox_props)
            axes.fill(*zip(*corners), **bbox_props_extended)

        if put_text_bottom:
            corners = _rotate_corners_to_put_first_elm_tl(corners)

        corner_top = corners[0]
        corner_bottom = corners[1]
        corner_bottom_right = corners[2]
        bottom_dir = math.atan2(corner_bottom[1] - corner_top[1], corner_bottom[0] - corner_top[0])
        right_dir = math.atan2(corner_bottom_right[1] - corner_bottom[1], corner_bottom_right[0] - corner_bottom[0])
        unitvec_b = (math.cos(bottom_dir), math.sin(bottom_dir))
        
        if show_no:
            pad_size = 3
            shift = _point_to_inch(pad_size + 1, axes.figure.dpi) / plot_scale
            no_props_extended = dict(
                size=font_size, ha="left", va="bottom", color="red", fontweight="bold", bbox={'pad': pad_size, 'facecolor': "black"},
                rotation_mode='anchor')
            no_props_extended.update(no_props)
            axes.text(
                corner_top[0] - shift * unitvec_b[0], corner_top[1] - shift * unitvec_b[1],
                str(id_), **no_props_extended)
        if show_text and message_str is not None:
            pad_size = 4
            shift = _point_to_inch(pad_size + 1, axes.figure.dpi) / plot_scale
            text_props_extended = dict(
                size=font_size, ha="left", va="top", bbox={'fc': '0.9', 'pad': 4},
                rotation=-math.degrees(right_dir), rotation_mode='anchor')
            text_props_extended.update(text_props)
            axes.text(
                corner_bottom[0] + shift * unitvec_b[0], corner_bottom[1] + shift * unitvec_b[1],
                message_str, **text_props_extended)

    return axes
