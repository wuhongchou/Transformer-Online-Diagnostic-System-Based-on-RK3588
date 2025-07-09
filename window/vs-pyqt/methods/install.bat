@echo off
if /i "%1"=="-s" ( 
for /f %%i in ('dir *.exe /b') do %%i -s -noconfirm -n -b
) else (
if /i "%1"=="/s" ( 
for /f %%i in ('dir *.exe /b') do %%i -s -noconfirm -n -b
) else (
for /f %%i in ('dir *.exe /b') do %%i
)
)
@echo on 