import sys
def main():
    #选择跑哪个function
    #菜单
    print("Welcome!")
    print("This is Cpts415 group 2 project")
    print("Main Menu")
    print("----------")
    print("1: AAA")
    print("2: BBB")
    print("3: CCC")
    print("4: AAA")
    print("5: Exit")
    print("----------")

    user_option = input("What do you want to do?")
    if user_option == '1':
        print("Hi")                 # function 1
    if user_option == '2':
        print("Hello")              # function 2
    if user_option == '3':
        print("Whats up")           # function 3
    if user_option == '4':
        print("Sup")                # function 4
    if user_option == '5':
        print("Okay bye")
        sys.exit()                  # exit





if __name__ == '__main__':
    main()