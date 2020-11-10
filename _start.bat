echo off
chcp 65001



cd %~dp0
cd "scripts"
check_mat_tsession.py


pause
exit