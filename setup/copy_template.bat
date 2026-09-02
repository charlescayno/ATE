::Copy excel template
set appdata_path=C:\Users\%USERNAME%\AppData\Local\PI_ATE
echo %appdata_path%
if not exist %appdata_path% (
mkdir %appdata_path%
copy data_process\ATE_Charts_Template.xlsx "%appdata_path%"
)