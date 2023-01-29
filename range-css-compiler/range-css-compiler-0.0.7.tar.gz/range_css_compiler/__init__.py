
# RangeCSS-Compiler [range_css_compiler]

import os
import sys
import fies
from sout import sout
# 形式変換 (yaml -> equid) [yaml_style_to_equid]
from .parts import yaml_style_to_equid as y2e
# 2次計画問題の行列を定義するjsコードに変換 [to_qp_mat_js.py]
from .parts import to_qp_mat_js as tqmj
# クライアント側jsを生成 (2次計画法でHTMLの動的な割り付けを実施) [gen_compiled_rcss.py]
from .parts import gen_compiled_rcss as gcr

# ファイル名拡張子の変更
def ext_rep(org_filename, new_ext):
	if "." not in org_filename:
		without_ext = org_filename
	else:
		without_ext = ".".join(org_filename.split(".")[:-1])
	ret_filename = without_ext + new_ext
	return ret_filename

# RangeCSSのyaml帳票をjsに変換 [range_css_compiler]
def compile(
	org_yaml_filename,
	output_js_filename = None,
):
	# output_js_filename の自動生成
	if output_js_filename is None:
		output_js_filename = ext_rep(org_yaml_filename, ".js")	# ファイル名拡張子の変更
	# yaml読み込み
	rcss_style = fies[org_yaml_filename, "yaml"]
	# yaml形式のRangeCSS_Styleをequid形式のcond, lossに変換 [yaml_style_to_equid]
	cond, loss, css_id_ls = y2e.yaml_style_to_equid(rcss_style)
	# 2次計画問題の行列を定義するjsコードに変換 [to_qp_mat_js.py]
	js_code = tqmj.to_qp_mat_js(cond, loss)
	# クライアント側jsを生成 (2次計画法でHTMLの動的な割り付けを実施) [gen_compiled_rcss.py]
	ret_js_code = gcr.gen_compiled_rcss(
		js_code,
		css_id_ls
	)
	# 保存
	# デフォルト動作を上書きにしたくない場合は下記を使用
	# if os.path.exists(output_js_filename): raise Exception("[RangeCSS-Compiler error] output filename already exists.")
	fies[output_js_filename, "text"] = ret_js_code

# コンソールから利用
def console_command():
	# コンソール引数
	arg_ls = sys.argv[1:]
	# 第一引数で分岐
	arg_len = len(arg_ls)
	if arg_len == 0:
		print("[RangeCSS-Compiler error] Please specify an argument for the command. (Example: rcss compile [filename])")
		return None
	if arg_ls[0] == "compile":
		if arg_len < 2:
			print("info: Please specify a file name (a yaml file containing the styles) as the second argument.")
			return None
		org_yaml_filename = arg_ls[1]
		output_js_filename = (arg_ls[2] if arg_len >= 3 else None)
		# RangeCSSのyaml帳票をjsに変換 [range_css_compiler]
		compile(
			org_yaml_filename = org_yaml_filename,
			output_js_filename = output_js_filename,
		)
	else:
		print("[RangeCSS-Compiler error] unknown command.")
