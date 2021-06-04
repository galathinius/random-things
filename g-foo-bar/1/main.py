def circular_shift(s, num):
    return s[num:] + s[:num]

def var2(s):
    to_return = 0
    
    for i in range(len(s)):
        if s == circular_shift(s, i):
            to_return +=1
    
    return to_return if to_return else 1
