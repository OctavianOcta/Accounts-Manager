import json
from cryptography.fernet import Fernet
import ast

FILENAME = "accounts.csv"

def create_account():
    # a dictionary is created with date for the account
    account = {}
    account['website'] = input("The name of the website: ")
    account['email'] = input("Email address: ")
    account['nickname'] = input("Nickname: ")
    account['password'] = input("Password: ")

    return account

def key_generation():
        #this generates a key and opens a file 'key.key' and writes the key there
        #used once to get the file and key and commented
    key = Fernet.generate_key()
    with open('key.key','wb') as file:
        file.write(key)


def getting_key():
    #this just opens your 'key.key' and assings the key stored there as 'key'
    with open('test_key.key','rb') as file:
        key = file.read()       
    
    return key


def encrypting(key,data):

    #this encrypts the data and stores it in 'encrypted'
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    #this writes your new, encrypted data into the file
    with open(FILENAME,'wb') as f:
        f.write(encrypted)

    
def bytes_to_dict(decrypted_data):
    # transforms the data that comes as class:bytes into class:dict
    decrypted_data2 = decrypted_data.decode("UTF-8")
    decrypted_data3 = ast.literal_eval(decrypted_data2)
    
    return decrypted_data3

def dict_to_bytes(data):
    #transforms the data that you worked with from class:dict to class:bytes
    user_encode_data = json.dumps(data).encode('utf-8')
    return user_encode_data


def decrypting(key):
    
    #decrypts the data from the file
    with open(FILENAME, "rb") as encrypted_file:
        encrypted = encrypted_file.read()
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted)

    return decrypted_data


def creating_a_list_with_all_the_accounts(decrypted_data3):
    #gets a list of dictionaries from the data that you got from the file
    acc_lis = decrypted_data3["accounts"]
    
    return acc_lis


def append_data(acc_lis,new_data):
    #appends the new dict to the existing list of dicts
    acc_lis.append(new_data)
    
    return acc_lis
    
        
        
def account_searching(acc_lis,search_option_value, value = 'website'):
    #searches into your list of accounts for the account by either the value of "website" or "email"
    counter = 0
        
    for acc in acc_lis:
        if acc[value].lower().strip() == search_option_value.lower().strip():
            print("")
            print("The account that you are searching for is:")
            print("Website: " + acc['website'])
            print("Email: " + acc['email'])
            print('Nickname: ' + acc['nickname'])
            print("Password: " + acc['password'])
            break
                    
        else:
            counter += 1
            
    if counter == len(acc_lis):
        print("")
        print("We couldn't find your account.")
        print("Check if you wrote it corectly or add it to the account.")   
        
        
def add_or_remove_menu():
    #The menu
    print("")
    print("Do you want to: ")
    print("1. Add an account.")
    print("2. Search for an account.")
    print("3. Remove an accouunt.")
    print("0. Quit")
    choice = int(input())

    return choice



def add_or_remove(choice,acc_lis,file_data):
    # 1- adds an account
    # 2 - searches for an account
    # 3 - removes an account
    # basically the main body of the app
    
    if choice == 1:
        acc_lis = append_data(acc_lis,create_account())
    
    
    
    if choice == 2:
        print("")
        print("What do you want to search for?")
        print("1.Website")
        print("2.Email Address")
        search_option = int(input())
        
        if search_option == 1:
            
            search_option_value = input("Enter the website: ")
            account_searching(acc_lis, search_option_value)
        
        if search_option == 2:
            search_option_value = input("Enter the email address: ")
            account_searching(acc_lis,search_option_value,"email")
            
    if choice == 3:
        print("Search for the account you want to be deleted.")
        search_option_value = input("Enter the website: ")
        account_searching(acc_lis,search_option_value)
        print("")
        print("If you are sure you want to delte the account, re-enter the name of the website.")
        acc = input("")
        
        
        for i in range(len(acc_lis)):
            if acc == acc_lis[i]["website"]:
                del acc_lis[i]
                break
        
    return acc_lis


def start(decrypted_data3):
    # a loop to do your stuff untill you want to stop
    acc_lis = creating_a_list_with_all_the_accounts(decrypted_data3)
    
    choice = 1
    while choice != 0:
        
        choice = add_or_remove_menu()
        file_data_list = add_or_remove(choice,acc_lis,decrypted_data3)
        
    
    return file_data_list

def setup():
    # the body for the encrypting and decrypting the info
    key = getting_key()
    decrypted_data = decrypting(key)
    decrypted_data3 = bytes_to_dict(decrypted_data)

    file_data_list = start(decrypted_data3)
    file_data = {"accounts":file_data_list}
    print(file_data)
    file_data_as_bytes = dict_to_bytes(file_data)
    print(file_data_as_bytes)
    encrypting(key,file_data_as_bytes)

setup()
#key_generation()
