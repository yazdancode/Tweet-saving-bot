import random

# تولید یک عدد تصادفی بین 0 و 255
random_number = random.randint(0, 255)

# تبدیل عدد تصادفی به فرمت هگزادسیمال
hexadecimal_number = hex(random_number)

print("عدد تصادفی در فرمت هگزادسیمال:", hexadecimal_number)
