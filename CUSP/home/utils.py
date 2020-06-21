
def profile_strength(num):
    if num <= 5:
        rem = "Poor!"
    elif num <=10:
        rem =  "OK!"
    elif num <15:
        rem =  "Great!"
    elif num <= 19:
        rem =  "Awesome!"
    percent = float((num/19)*100)
    return rem, percent