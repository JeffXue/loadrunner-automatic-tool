@echo off
rem ��Ŀ����Ĭ��ʹ��ydh
set project_name=test

rem ���԰汾+�ִ�
set project_version=V1.0.0Round1

rem ���Գ������ƣ��������׺
set scenario_name=api

rem loadrunner�ű����ͣ�0 ��C���Ա�д  1 ����Jar��ʵ��
set lr_type=0

rem ����loadrunner bin·��
set lr_path="C:\Program Files (x86)\HP\LoadRunner\bin"

rem ���ù���Ŀ¼����β����Ҫ����\
set workspace="D:\LoadRunnerWorkStation"

rem ����������������LoadRunner�������ļ�
python generate_lr_bat.py %project_name% %scenario_name% %project_version% %lr_type% %lr_path% %workspace%

rem �����������ļ�
run_lr.bat

pause

