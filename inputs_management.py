def get_user_input(): 
    #validate user input 
    print("Select your category:")
    print("1. English")
    print("2. Others")
    while True:
        try:
            option = int(input("Enter the number corresponding to your choice: "))
            if option == 1 or option == 2:
                break
            else:
                print("Enter a valid option (1 or 2).")
        except ValueError:
            print("Enter a valid number.")
    return option
        
