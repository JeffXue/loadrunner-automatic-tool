@echo off
rem 项目名称默认使用ydh
set project_name=test

rem 测试版本+轮次
set project_version=V1.0.0Round1

rem 测试场景名称，不需带后缀
set scenario_name=api

rem loadrunner脚本类型，0 ：C语言编写  1 ：调Jar包实现
set lr_type=0

rem 设置loadrunner bin路径
set lr_path="C:\Program Files (x86)\HP\LoadRunner\bin"

rem 设置工作目录，结尾不需要带上\
set workspace="D:\LoadRunnerWorkStation"

rem 根据配置生成运行LoadRunner批处理文件
python generate_lr_bat.py %project_name% %scenario_name% %project_version% %lr_type% %lr_path% %workspace%

rem 运行批处理文件
run_lr.bat

pause

