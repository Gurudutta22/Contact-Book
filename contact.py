class Contact:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email
        self.next = None  # for linked list implementation

class ContactBook:
    def __init__(self):
        self.head = None
        self.contact_count = 0  # Variable to keep track of total contacts
        
    def create_contact(self, name, phone, email):
        """
        Create a new contact and add it to the contact book
        Using sorted linked list implementation - O(n)
        """
        new_contact = Contact(name, phone, email)
        self.contact_count += 1
        
        # If list is empty or new contact should be at start
        if self.head is None or self.head.name >= name:
            new_contact.next = self.head
            self.head = new_contact
            print(f"\nContact created successfully: {name}")
            return
            
        # Find the correct position to insert
        current = self.head
        while current.next and current.next.name < name:
            current = current.next
            
        new_contact.next = current.next
        current.next = new_contact
        print(f"\nContact created successfully: {name}")
        
    def display_contacts(self):
        """
        Display all contacts in sorted order - O(n)
        """
        if not self.head:
            print("\nContact book is empty!")
            return
            
        print("\nContact List:")
        print("-" * 50)
        current = self.head
        while current:
            print(f"Name: {current.name}")
            print(f"Phone: {current.phone}")
            print(f"Email: {current.email}")
            print("-" * 50)
            current = current.next
            
    def search_contact(self, name):
        """
        Search for a contact using binary search concept - O(n)
        Returns the contact and its previous node if found
        """
        if not self.head:
            return None, None
            
        current = self.head
        prev = None
        
        while current and current.name <= name:
            if current.name == name:
                return prev, current
            prev = current
            current = current.next
            
        return None, None
        
    def update_contact(self, name, new_phone=None, new_email=None):
        """
        Update contact information - O(n)
        """
        _, contact = self.search_contact(name)
        
        if contact:
            if new_phone:
                contact.phone = new_phone
            if new_email:
                contact.email = new_email
            print(f"\nContact updated successfully: {name}")
        else:
            print(f"\nContact not found: {name}")
            
    def delete_contact(self, name):
        """
        Delete a contact from the book - O(n)
        """
        prev, contact = self.search_contact(name)
        
        if not contact:
            print(f"\nContact not found: {name}")
            return
            
        if prev:
            prev.next = contact.next
        else:
            self.head = contact.next
            
        self.contact_count -= 1
        print(f"\nContact deleted successfully: {name}")
        
    def get_contact_count(self):
        """
        Return total number of contacts - O(1)
        """
        return self.contact_count

def main():
    contact_book = ContactBook()
    
    while True:
        print("\nContact Book Menu:")
        print("1. Create Contact")
        print("2. Display All Contacts")
        print("3. Search Contact")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Get Contact Count")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ")
        
        if choice == '1':
            name = input("Enter name: ")
            phone = input("Enter phone number: ")
            email = input("Enter email: ")
            contact_book.create_contact(name, phone, email)
            
        elif choice == '2':
            contact_book.display_contacts()
            
        elif choice == '3':
            name = input("Enter name to search: ")
            _, contact = contact_book.search_contact(name)
            if contact:
                print("\nContact found:")
                print("-" * 50)
                print(f"Name: {contact.name}")
                print(f"Phone: {contact.phone}")
                print(f"Email: {contact.email}")
                print("-" * 50)
            else:
                print(f"\nContact not found: {name}")
                
        elif choice == '4':
            name = input("Enter name to update: ")
            new_phone = input("Enter new phone number (press enter to skip): ")
            new_email = input("Enter new email (press enter to skip): ")
            contact_book.update_contact(name, new_phone if new_phone else None, 
                                     new_email if new_email else None)
                                     
        elif choice == '5':
            name = input("Enter name to delete: ")
            contact_book.delete_contact(name)
            
        elif choice == '6':
            count = contact_book.get_contact_count()
            print(f"\nTotal contacts: {count}")
            
        elif choice == '7':
            print("\nThank you for using Contact Book!")
            break
            
        else:
            print("\nInvalid choice! Please try again.")

if __name__ == "__main__":
    main()