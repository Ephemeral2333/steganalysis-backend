import random
import string

# 获取验证码
def getCaptcha():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))