import tkinter as tk
from tkinter import ttk, messagebox


class Contact:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email
        self.next = None


class ContactBook:
    def __init__(self):
        self.head = None
        self.contact_count = 0

    def create_contact(self, name, phone, email):
        new_contact = Contact(name, phone, email)
        self.contact_count += 1

        if self.head is None or self.head.name >= name:
            new_contact.next = self.head
            self.head = new_contact
            return True

        current = self.head
        while current.next and current.next.name < name:
            current = current.next

        new_contact.next = current.next
        current.next = new_contact
        return True

    def search_contact(self, name):
        current = self.head
        while current and current.name <= name:
            if current.name == name:
                return current
            current = current.next
        return None

    def update_contact(self, name, new_phone=None, new_email=None):
        contact = self.search_contact(name)
        if contact:
            if new_phone:
                contact.phone = new_phone
            if new_email:
                contact.email = new_email
            return True
        return False

    def delete_contact(self, name):
        prev, current = None, self.head
        while current and current.name <= name:
            if current.name == name:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                self.contact_count -= 1
                return True
            prev, current = current, current.next
        return False


class ContactBookGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.contact_book = ContactBook()

        self.root.geometry("600x400")
        self.root.configure(padx=20, pady=20)

        self.create_input_frame()
        self.create_button_frame()
        self.create_display_frame()

    def create_input_frame(self):
        input_frame = ttk.LabelFrame(self.root, text="Contact Information", padding="10")
        input_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        ttk.Label(input_frame, text="Name:").grid(row=0, column=0, sticky="w")
        self.name_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.name_var).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(input_frame, text="Phone:").grid(row=1, column=0, sticky="w")
        self.phone_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.phone_var).grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(input_frame, text="Email:").grid(row=2, column=0, sticky="w")
        self.email_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.email_var).grid(row=2, column=1, padx=5, pady=2)

    def create_button_frame(self):
        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=1, column=0, sticky="ew", pady=10)

        ttk.Button(button_frame, text="Add Contact", command=self.add_contact).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Update Contact", command=self.update_contact).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Delete Contact", command=self.delete_contact).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Search Contact", command=self.search_contact).grid(row=0, column=3, padx=5)

    def create_display_frame(self):
        display_frame = ttk.LabelFrame(self.root, text="Contacts", padding="10")
        display_frame.grid(row=2, column=0, sticky="nsew", pady=5)

        self.tree = ttk.Treeview(display_frame, columns=("Name", "Phone", "Email"), show="headings", height=8)
        self.tree.heading("Name", text="Name")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Email", text="Email")

        scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

    def add_contact(self):
        name, phone, email = self.name_var.get(), self.phone_var.get(), self.email_var.get()
        if not all([name, phone, email]):
            messagebox.showerror("Error", "All fields are required!")
            return

        if self.contact_book.create_contact(name, phone, email):
            messagebox.showinfo("Success", f"Contact '{name}' added successfully!")
            self.clear_entries()
            self.refresh_contacts()

    def update_contact(self):
        name, phone, email = self.name_var.get(), self.phone_var.get(), self.email_var.get()
        if not name:
            messagebox.showerror("Error", "Name is required for updating a contact!")
            return

        if self.contact_book.update_contact(name, new_phone=phone, new_email=email):
            messagebox.showinfo("Success", f"Contact '{name}' updated successfully!")
            self.clear_entries()
            self.refresh_contacts()
        else:
            messagebox.showerror("Error", f"Contact '{name}' not found!")

    def delete_contact(self):
        name = self.name_var.get()
        if not name:
            messagebox.showerror("Error", "Name is required for deleting a contact!")
            return

        if self.contact_book.delete_contact(name):
            messagebox.showinfo("Success", f"Contact '{name}' deleted successfully!")
            self.clear_entries()
            self.refresh_contacts()
        else:
            messagebox.showerror("Error", f"Contact '{name}' not found!")

    def search_contact(self):
        name = self.name_var.get()
        if not name:
            messagebox.showerror("Error", "Please enter a name to search!")
            return

        contact = self.contact_book.search_contact(name)
        if contact:
            self.name_var.set(contact.name)
            self.phone_var.set(contact.phone)
            self.email_var.set(contact.email)
            messagebox.showinfo("Contact Found", f"Name: {contact.name}\nPhone: {contact.phone}\nEmail: {contact.email}")
        else:
            messagebox.showerror("Error", f"Contact '{name}' not found!")

    def refresh_contacts(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        current = self.contact_book.head
        while current:
            self.tree.insert("", "end", values=(current.name, current.phone, current.email))
            current = current.next

    def clear_entries(self):
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")


if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBookGUI(root)
    root.mainloop()
