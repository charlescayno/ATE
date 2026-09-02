import traceback
with open(r'C:\Users\ccayno\Downloads\pi_ate-PI_ATE_Marketing_Release-MR1.0.5@4f59a860b74\psu_tests\test_efficiency.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('print(traceback.format_exc())', 'print(traceback.format_exc())\n            with open(\'error_log.txt\', \'a\') as f: f.write(traceback.format_exc() + \'\\n\')')

with open(r'C:\Users\ccayno\Downloads\pi_ate-PI_ATE_Marketing_Release-MR1.0.5@4f59a860b74\psu_tests\test_efficiency.py', 'w', encoding='utf-8') as f:
    f.write(text)
