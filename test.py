t = """
یک درخواست جدید دریافت شد
اطلاعات کاربر به شرح زیر است:
محتوای درخواست: m
تاریخ ارسال: 1403/03/01
نام: Mr.
نام خانوادگی: Python
یوزرنیم: @Y_Shabanei
شماره کاربری: 5105508285
دریافت شد."""

import re

pattern = r"شماره کاربری: \d+"
x = re.findall(pattern=pattern, string=t)[0].split()[2]
print(x)
