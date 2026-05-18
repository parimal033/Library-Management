import streamlit as st
import json
import random
import string
from pathlib import Path
from datetime import datetime

# ---------------------------
# Data Handling
# ---------------------------

DATABASE = "library.json"

def load_data():
    if Path(DATABASE).exists():
        with open(DATABASE, "r") as f:
            content = f.read().strip()
            if content:
                return json.loads(content)
    return {"books": [], "members": []}

def save_data(data):
    with open(DATABASE, "w") as f:
        json.dump(data, f, indent=4, default=str)

def generate_id(prefix="B"):
    return prefix + "-" + ''.join(random.choices(string.ascii_letters + string.digits, k=5))

data = load_data()

# ---------------------------
# UI Title
# ---------------------------

st.title("📚 Library Management System")

menu = st.sidebar.selectbox("Select Option", [
    "Add Book",
    "List Books",
    "Add Member",
    "List Members",
    "Borrow Book",
    "Return Book"
])

# ---------------------------
# Add Book
# ---------------------------

if menu == "Add Book":
    st.subheader("➕ Add New Book")

    title = st.text_input("Book Title")
    author = st.text_input("Author")
    copies = st.number_input("Number of Copies", min_value=1, step=1)

    if st.button("Add Book"):
        book = {
            "id": generate_id(),
            "title": title,
            "author": author,
            "total_copies": copies,
            "available_copies": copies,
            "added_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        data["books"].append(book)
        save_data(data)
        st.success("✅ Book added successfully!")

# ---------------------------
# List Books
# ---------------------------

elif menu == "List Books":
    st.subheader("📖 All Books")

    if not data["books"]:
        st.warning("No books available.")
    else:
        st.table(data["books"])

# ---------------------------
# Add Member
# ---------------------------

elif menu == "Add Member":
    st.subheader("👤 Add Member")

    name = st.text_input("Member Name")
    email = st.text_input("Email")

    if st.button("Add Member"):
        member = {
            "id": generate_id("M"),
            "name": name,
            "email": email,
            "borrowed": []
        }
        data["members"].append(member)
        save_data(data)
        st.success("✅ Member added successfully!")

# ---------------------------
# List Members
# ---------------------------

elif menu == "List Members":
    st.subheader("👥 All Members")

    if not data["members"]:
        st.warning("No members found.")
    else:
        display_members = []
        for m in data["members"]:
            display_members.append({
                "ID": m["id"],
                "Name": m["name"],
                "Email": m["email"],
                "Borrowed Books": len(m["borrowed"])
            })
        st.table(display_members)

# ---------------------------
# Borrow Book
# ---------------------------

elif menu == "Borrow Book":
    st.subheader("📚 Borrow Book")

    member_ids = [m["id"] for m in data["members"]]
    book_ids = [b["id"] for b in data["books"] if b["available_copies"] > 0]

    if not member_ids or not book_ids:
        st.warning("Members or books not available.")
    else:
        member_id = st.selectbox("Select Member", member_ids)
        book_id = st.selectbox("Select Book", book_ids)

        if st.button("Borrow"):
            member = next(m for m in data["members"] if m["id"] == member_id)
            book = next(b for b in data["books"] if b["id"] == book_id)

            borrow_entry = {
                "book_id": book["id"],
                "title": book["title"],
                "borrowed_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            member["borrowed"].append(borrow_entry)
            book["available_copies"] -= 1

            save_data(data)
            st.success("✅ Book borrowed successfully!")

# ---------------------------
# Return Book
# ---------------------------

elif menu == "Return Book":
    st.subheader("🔄 Return Book")

    member_ids = [m["id"] for m in data["members"] if m["borrowed"]]

    if not member_ids:
        st.warning("No borrowed books found.")
    else:
        member_id = st.selectbox("Select Member", member_ids)
        member = next(m for m in data["members"] if m["id"] == member_id)

        borrowed_books = member["borrowed"]
        book_titles = [f"{b['book_id']} - {b['title']}" for b in borrowed_books]

        selected_book = st.selectbox("Select Book to Return", book_titles)

        if st.button("Return Book"):
            index = book_titles.index(selected_book)
            returned_book = member["borrowed"].pop(index)

            # increase available copies
            for book in data["books"]:
                if book["id"] == returned_book["book_id"]:
                    book["available_copies"] += 1
                    break

            save_data(data)
            st.success("✅ Book returned successfully!")