# -*- coding:utf-8 -*-
__author__ = 'xuekj'
import sys
import time
from report.util import get_parameter_lists

parameter_list = get_parameter_lists(sys.argv)
project_name = parameter_list[0]
scenario_name = parameter_list[1] + '.lrs'
result_name = parameter_list[1]
project_version = parameter_list[2]
project_type = parameter_list[1]
lr_type = parameter_list[3]
lr_path = parameter_list[4]
workspace = parameter_list[5]
start_time = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))


template = """
@echo off

taskkill /f /im Wlrun.exe

rem 设置LoadRunner运行配置参数
set lr_scenario="%(workspace)s\\%(scenario_name)s"
set lr_res="%(workspace)s\\res\\%(result_name)s"
set lr_res_lrr="%(workspace)s\\res\\%(result_name)s\\%(result_name)s.lrr"
set lr_res_template=spms_lr_report_template

rem 移动到report目录中以运行后续脚本
cd report

rem 运行LoadRunner
echo running scenario
"%(lr_path)s\\Wlrun.exe" -TestPath %%lr_scenario%%  -ResultName %%lr_res%%  -Run

rem 运行LoadRunner结果分析
echo analyse lr result
"%(lr_path)s\\AnalysisUI.exe" -RESULTPATH %%lr_res_lrr%% -TEMPLATENAME %%lr_res_template%% -CLOSE

rem 运行二次结果分析
python start.py %%lr_res%% %(project_name)s-%(project_version)s-%(project_type)s %(start_time)s %(lr_type)s

"""
value = {'project_name': project_name, 'scenario_name': scenario_name,
         'result_name': result_name, 'project_version': project_version,
         'project_type': project_type, 'start_time': start_time,
         'lr_type': lr_type, 'workspace': workspace, 'lr_path': lr_path}

with open('run_lr.bat', 'w') as f:
    f.write(template % value)

