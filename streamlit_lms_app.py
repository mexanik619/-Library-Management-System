import streamlit as st
from LMS import Library, Librarian, BookStatus

# Initialize library and librarian
if 'library' not in st.session_state:
    st.session_state.library = Library("City Central Library", "123 Main St, Cityville")
    st.session_state.librarian = Librarian("John Smith", "EMP001", "john@library.com")
    st.session_state.library.add_librarian(st.session_state.librarian)

library = st.session_state.library
librarian = st.session_state.librarian

st.title("📚 Library Management System")

menu = st.sidebar.radio("Navigation", [
    "Add Book", "Register Member", "Issue Book", "Return Book",
    "Search Books", "Overdue Report", "Library Overview"
])

if menu == "Add Book":
    st.header("➕ Add a New Book")
    with st.form("add_book_form"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        isbn = st.text_input("ISBN")
        pub_year = st.number_input("Publication Year", min_value=1900, max_value=2100, step=1)
        category = st.text_input("Category")
        submitted = st.form_submit_button("Add Book")
        if submitted:
            book_id = librarian.add_book(library, title, author, isbn, pub_year, category)
            st.success(f"Book added with ID: {book_id}")

elif menu == "Register Member":
    st.header("👤 Register a New Member")
    with st.form("register_member_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        address = st.text_input("Address")
        phone = st.text_input("Phone")
        submitted = st.form_submit_button("Register Member")
        if submitted:
            member_id = librarian.register_member(library, name, email, address, phone)
            st.success(f"Member registered with ID: {member_id}")

elif menu == "Issue Book":
    st.header("📗 Issue a Book")
    book_id = st.text_input("Book ID")
    member_id = st.text_input("Member ID")
    if st.button("Issue"):
        success = librarian.issue_book_to_member(library, book_id, member_id)
        if success:
            st.success("Book issued successfully.")
        else:
            st.error("Could not issue book. Check IDs and availability.")

elif menu == "Return Book":
    st.header("📘 Return a Book")
    book_id = st.text_input("Book ID to return")
    member_id = st.text_input("Member ID")
    if st.button("Return"):
        fine = librarian.return_book_from_member(library, book_id, member_id)
        if fine is not None:
            st.success(f"Book returned. Fine: ${fine}")
        else:
            st.error("Invalid return. Check IDs.")

elif menu == "Search Books":
    st.header("🔍 Search Books")
    keyword = st.text_input("Search keyword")
    if keyword:
        results = library.search_books(keyword)
        if results:
            for book in results:
                st.write(f"{book}")
        else:
            st.warning("No books found.")

elif menu == "Overdue Report":
    st.header("📄 Overdue Books Report")
    overdue = library.generate_report_overdue_books()
    if overdue:
        for entry in overdue:
            st.write(f"**{entry['book'].title}** - {entry['member'].name} | {entry['days_late']} days late | Fine: ${entry['fine']}")
    else:
        st.info("No overdue books.")

elif menu == "Library Overview":
    st.header("🏛️ Library Overview")
    st.write(str(library))
    st.subheader("Books:")
    for book in library.books.values():
        st.text(str(book))
    st.subheader("Members:")
    for member in library.members.values():
        st.text(str(member))
