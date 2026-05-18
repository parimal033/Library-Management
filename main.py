import json
import random
import string 
from pathlib import Path
from datetime import datetime


class Library:
    database = "library.json"
    data = {
        "books" : [],
        "members" : []
    }
    
    # Load existing data to Json or create your json
    if Path(database).exists():
        with open(database,"r") as f:
            content = f.read().strip()
            if content:
                data = json.loads(content)
    else:
        with open(database,'w') as f:
            json.dump(data,f,indent=4)
            
    @classmethod
    def save_data(cls):
        with open(cls.database,'w') as f:
            json.dump(cls.data,f,indent=4,default=str)

        
    
    
    
    
    def genrate_id(prefix = "B"):
        random_id = ""
        for i in range(5):
            random_id += random.choice(string.ascii_letters + string.digits)
        
        return prefix + "-" + random_id
    
    
    
    def add_book(self):
        title = input("Enter book title :- ")
        author = input("Enter book Author :- ")
        copies = int(input("How many copies :- "))
    
        book = {
            "id" : Library.genrate_id(),
            "title" : title,
            "author" : author,
            "total_copies": copies,
            "available_copies" : copies,
            "added_on" : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        Library.data["books"].append(book)
        Library.save_data()


    def list_books(self):
        if not Library.data["books"]:
            print("Sorry No books found")
            return
        
        # Header line
        print(f"{'ID':<10} | {'Title':<20} | {'Author':<15} | {'Available':<10}")
        print("-" * 65)

        # Book rows
        for b in Library.data["books"]:
            print(f"{b['id']:<10} | {b['title']:<20} | {b['author']:<15} | {b['available_copies']}/{b['total_copies']}")


    def add_member(self):
        name = input("Enter your name :- ")
        email = input("Enter your email :- ")    

        member = {
            "id" : Library.genrate_id("M"),
            "name" : name,
            "email" : email,
            "borrowed": []
        }
        
        Library.data['members'].append(member)
        Library.save_data()
        print("Member is created sucessfully")
        
    
    def list_members(self):
        if not Library.data["members"]:
            print("Sorry No members")
            return
        
        # Header line
        print(f"{'Member ID':<12} | {'Name':<20} | {'Email':<30} | {'Borrowed Count':<15}")
        print("-" * 85)

        # Member rows
        for m in Library.data['members']:
            borrowed_count = len(m['borrowed'])
            print(f"{m['id']:<12} | {m['name']:<20} | {m['email']:<30} | {borrowed_count} book(s)")

    
    def borrow_book(self):
        member_id = input("Enter your id :- ").strip()
        members = [m for m in Library.data['members'] if m["id"] == member_id]
        
        if not members:
            print("User is not found")
            return 
        member = members[0]
        
        book_id = input("Enter the book id :- ").strip()
        books = [b for b in Library.data['books'] if b["id"] == book_id]
        
        if not books:
            print("Books is not found")
            return
        book = books[0]
    
        if book['available_copies'] <= 0:
            print("Sorry no books exist")
            return
        
        borrow_entery = {
            "book_id" : book["id"],
            "title" : book['title'],
            "Borrow_on" :  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        member["borrowed"].append(borrow_entery)
        book['available_copies'] -= 1
        Library.save_data()
    
    
    def return_book(self):
        member_id = input("Enter your id :- ").strip()
        members = [m for m in Library.data['members'] if m["id"] ==member_id]
       
        if not members:
            print("User is not found")
            return 
        
        member = members[0]
        
        if not member['borrowed']:
            print("No borrowes books")
            return
        
        for m in Library.data['members']:
            print(f"\n=== Member: {m['name']} ===")
            print(f"ID         : {m['id']}")
            print(f"Email      : {m['email']}")
            print("Borrowed Books:")
    
            if m['borrowed']:
                for book in m['borrowed']:
                    print(f"  - [{book['book_id']}] '{book['title']}' (Borrowed: {book['Borrow_on']})")
            
            try:
                choice = int(input("Enter number to return :- "))
                selected = member['borrowed'].pop(choice - 1)
                
                books = [bk for bk in Library.data['books'] if bk['id'] == selected['book_id']]
                if books:
                    books[0]['available_copies'] += 1
            
                Library.save_data()
            except Exception as err:
                print("Invalid value")
            
            
    
obj = Library()

while True:
    print("="*50)
    print("\t\tLibrary Management System")
    print("="*50)

    print("1. Add Book")
    print("2. List Book")
    print("3. Add Member")
    print("4. List Member")
    print("5. Borrow Book")
    print("6. Retuen Book")
    print("0. Exit the portal")

    print("-"*50)

    choice = int(input("What task you want to do :- "))


    if choice == 1:
        obj.add_book()
    elif choice == 2:
        obj.list_books()
    elif choice == 3:
        obj.add_member()
    elif choice == 4:
        obj.list_members()
    elif choice == 5:
        obj.borrow_book()
    elif choice == 6:
        obj.return_book()
    elif choice == 7:
        exit(0)