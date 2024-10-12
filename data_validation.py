from datetime import datetime

Categories = {"C": "Credit", "D" : "Debit"}

def get_date(prompt, default = True):
    date_str = input(prompt)
    if(not default and not date_str):
        date_str = datetime.today().strftime('%d-%m-%Y')
        return date_str
    try:
        valid_date = datetime.strptime(date_str, '%d-%m-%Y')
        return valid_date.strftime('%d-%m-%Y')
    except ValueError:
        print("Please Enter a valid date of format dd-mm-yyyy")
        return get_date(prompt, default = True)
    
def get_amount():
    try:
        amt = float(input("Enter the amount: "))
        if amt < 0:
            print("Please Enter a positive amount")
            get_amount()
        return amt
    except ValueError:
        print(ValueError)
        get_amount

def get_category():
    cat = input("Enter the Category you want ('C' for credit, 'D' for debit): ")
    if cat in Categories:
        return Categories[cat]
    print("Please Enter a Valid Category")
    get_category()

def get_desciption():
    return input("Enter Description: ")