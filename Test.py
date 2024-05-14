def remove_property_recursive(lst, value):
    if not lst:
        return lst  # اگر لیست خالی باشد، هیچ تغییری انجام نمی‌دهیم

    if isinstance(lst[0], list):
        # اگر عنصر اول لیست یک لیست دیگر باشد، به صورت بازگشتی تابع را فراخوانی می‌کنیم
        return [remove_property_recursive(sub_lst, value) for sub_lst in lst]

    # اگر عنصر اول لیست یک مقدار است، آن مقدار را با مقدار داده شده مقایسه می‌کنیم
    if lst[0] == value:
        # اگر مقدار برابر با مقدار داده شده باشد، آن را از لیست حذف می‌کنیم
        return remove_property_recursive(lst[1:], value)
    else:
        # اگر مقدار برابر نباشد، آن را در لیست حفظ می‌کنیم و به عناصر بعدی می‌رویم
        return [lst[0]] + remove_property_recursive(lst[1:], value)


if __name__ == "__main__":
    nested_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    value_to_remove = 5
    result = remove_property_recursive(nested_list, value_to_remove)
    print(result)
