#this program will add your accounts into a json
#you can search the document by the name of the website,pwd or email address

"""
Nu o sa l termin in seara asta asa ca asta e ideea programului:
o lista de dictionare, feicare dictionar avand ca si key:
-website
-email address
-nickname
-password

A se adauga o functie de a cauta in document si a arata toate jsoanele care se potrivesc unui criteriu de cautare( probabil key respectiva idk)

OPTIONAL: cripteaza parolele
"""

import json
from cryptography.fernet import Fernet


FILENAME = "accounts.json"

def create_account():
    account = {}
    account['website'] = input("The name of the website: ")
    account['email'] = input("Email address: ")
    account['nickname'] = input("Nickname: ")
    account['password'] = input("Password: ")

    return account
# se creaza un dictionar cu datele contului

def encrypting():
    #this generates a key and opens a file 'key.key' and writes the key there
    key = Fernet.generate_key()
    with open('key.key','wb') as file:
        file.write(key)

    #this just opens your 'key.key' and assings the key stored there as 'key'
    with open('key.key','rb') as file:
        key = file.read()

    #this opens your json and reads its data into a new variable called 'data'
    with open(FILENAME,'rb') as f:
        data = f.read()

    #this encrypts the data read from your json and stores it in 'encrypted'
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    #this writes your new, encrypted data into a new JSON file
    with open(FILENAME,'wb') as f:
        f.write(encrypted)

    return encrypted

def decrypting(encrypted):
    with open('key.key','rb') as file:
        key = file.read()
    
    fernet = Fernet(key)
    fernet.decrypt(encrypted)

def creating_a_list_with_all_the_accounts():
    with open(FILENAME,'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        acc_lis = file_data["accounts"]
    
    return acc_lis
# function to add to JSON


def write_json(new_data):
    with open(FILENAME,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside "accounts"
        file_data["accounts"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)
        
        
def account_searching(acc_lis,search_option_value, value = 'website'):
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
    print("")
    print("Do you want to: ")
    print("1. Add an account.")
    print("2. Search for an account.")
    print("3. Remove an accouunt.")
    print("0. Quit")
    choice = int(input())

    return choice



def add_or_remove(choice,acc_lis):
    
    
    if choice == 1:
        write_json(create_account())
    
    
    
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
        
        with open(FILENAME,'r+') as file:
        # First we load existing data into a dict.
            file_data = json.load(file)
            
        for i in range(len(file_data["accounts"])-1):
            if acc == file_data["accounts"][i]["website"]:
                del file_data["accounts"][i]
        
        with open(FILENAME, "w") as file:
            json.dump(file_data, file, indent = 4)

# trebuia deschisa fila de 2 ori, o data cu r pentru a incarca datele si inca o data cu w pentru a muta cursorul la inceput si a rescrie tot cacatul :(
def start():
    
    
    choice = 1
    while choice != 0:
        
        acc_lis = creating_a_list_with_all_the_accounts()
        choice = add_or_remove_menu()
        add_or_remove(choice,acc_lis)
        
        # for encoding check crypting test.py
        #still not finished :(
            #should i store encrypted info 
            #then decrypt, use and then encrypt again and store it back?
            #idfk

start()