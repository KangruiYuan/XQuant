@echo off
if "%1" == "h" goto begin
mshta vbscript:createobject("wscript.shell").run("""%~0"" h",0)(window.close)&&exit
:begin
set path=D:\anaconda3;D:\anaconda3\Scripts
python D:\anaconda3\Lib\site-packages\XQuant\XQuant\Scripts\RunWeb.py
pause
