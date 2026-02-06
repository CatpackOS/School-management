import tkinter as tk
from tkinter import PhotoImage, ttk, messagebox


#---Global window references to prevent multiple windows---

window_add = None
window_remove = None
window_search_name = None
window_search_id = None
window_update = None

#------Buttons configuration / Functions-------

def update_counter():
    #Count the number of students in the table
    count = len(Table.get_children())
    label_counter.config(text=f"Number of students in the system: {count}")

def student_addition():
    global window_add
    #Prevent opening multiple add windows
    if window_add is not None and tk.Toplevel.winfo_exists(window_add):
        window_add.focus()
        return

    #Local Variables
    window_add = tk.Toplevel(window)
    window_add.geometry("300x200")
    window_add.title("Add the information of the student")

    # eset reference when closed
    def on_close():
        global window_add
        window_add.destroy()
        window_add = None
    window_add.protocol("WM_DELETE_WINDOW", on_close)

    label_add = ["Academic ID", "First name", "Last name"]
    entries_add = {}

    #Creates labels and entries
    for i, text in enumerate(label_add):
        tk.Label(window_add, text=text).grid(row=i, column=0, padx=5, pady=5, sticky="e")
        e = tk.Entry(window_add)
        e.grid(row=i, column=1, padx=5, pady=5)
        entries_add[text] = e

    #Function That runs when the button save is pressed
    def save_information():
        # Saving the information on variables
        academic_id_save = entries_add["Academic ID"].get().strip()
        first_name_save = entries_add["First name"].get().strip()
        last_name_save = entries_add["Last name"].get().strip()

        #Validation check
        if not academic_id_save or not first_name_save or not last_name_save:
            messagebox.showwarning("Missing Data", "Please fill in all fields")
            return

        #-----Duplicate check (by Academic ID)-----
        try:
            with open("Student's.csv", "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    parts = line.strip().split(",")
                    if parts[0] == academic_id_save:  #ID is first field
                        messagebox.showerror("Duplicate ID", "A student with this Academic ID already exists.")
                        return
        except FileNotFoundError:
            #File doesn't exist yet -> no duplicates
            pass

        #Opening a file and saving the data with an exception
        try:
            with open("Student's.csv", "a", encoding="utf-8") as f:
                f.write(f"{academic_id_save},{first_name_save},{last_name_save},\n")
        except Exception as e:
            messagebox.showerror("Error", f"Couldn't save data \n{e}")
            return

        #Updating main table immediately
        Table.insert("", "end", values=(academic_id_save, first_name_save, last_name_save))
        update_counter()
        messagebox.showinfo("Saved", "Student saved successfully!")

        #Clearing fields after saving
        for entry in entries_add.values():
            entry.delete(0, tk.END)

    #Save button
    button_save = tk.Button(window_add, text="Save", width=15, command=save_information)
    button_save.grid(row=len(label_add), column=0, columnspan=2, pady=20)

def student_remove():
    global window_remove
    #Prevent opening multiple remove windows
    if window_remove is not None and tk.Toplevel.winfo_exists(window_remove):
        window_remove.focus()
        return

    #Local Variables
    window_remove = tk.Toplevel(window)
    window_remove.geometry("300x200")
    window_remove.title("Remove a student")

    #Reset reference when closed
    def on_close():
        global window_remove
        window_remove.destroy()
        window_remove = None
    window_remove.protocol("WM_DELETE_WINDOW", on_close)

    tk.Label(window_remove, text="Academic ID to remove").pack(pady=10)
    entry_id = tk.Entry(window_remove)
    entry_id.pack(pady=5)

    def student_deletion():
        target_id = entry_id.get().strip()

        if not target_id:
            messagebox.showwarning("Missing ID", "Please enter academic ID.")
            return

        removed = False

        #---- Remove from CSV file ----
        try:
            new_lines = []
            with open("Student's.csv", "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    if line.startswith(target_id + ","):
                        removed = True
                    else:
                        new_lines.append(line)

            # Rewriting the CSV with the student removed
            with open("Student's.csv", "w", encoding="utf-8") as f:
                f.writelines(new_lines)

        except FileNotFoundError:
            messagebox.showerror("Error", "Student's.csv not found.")
            return

        #---- Remove from Treeview ----
        for row in Table.get_children():
            values = Table.item(row)["values"]
            if values and str(values[0]) == target_id:
                Table.delete(row)
                removed = True

        if removed:
            messagebox.showinfo("Removed", "Student removed successfully.")
            update_counter()
        else:
            messagebox.showwarning("Not found", "No student found with that ID.")

    #Remove button
    button_remove = tk.Button(window_remove, text="Remove", width=15, command=student_deletion)
    button_remove.pack(pady=15)

def search_name():
    global window_search_name
    # Prevent opening multiple search name windows
    if window_search_name is not None and tk.Toplevel.winfo_exists(window_search_name):
        window_search_name.focus()
        return

    window_search_name = tk.Toplevel(window)
    window_search_name.geometry("300x200")
    window_search_name.title("Search a name")

    def on_close():
        global window_search_name
        window_search_name.destroy()
        window_search_name = None
    window_search_name.protocol("WM_DELETE_WINDOW", on_close)

    tk.Label(window_search_name, text="Search a student by their name").pack(pady=10)
    entry_name = tk.Entry(window_search_name)
    entry_name.pack(pady=5)

    def find_name():
        search_text = entry_name.get().strip().lower()
        if not search_text:
            messagebox.showwarning("Missing data", "Please enter a name.")
            return

        found_students = []
        try:
            with open("Student's.csv", "r", encoding="utf-8") as file:
                for line in file:
                    if not line.strip():
                        continue
                    academic_id, first_name, last_name = line.strip().split(",")[:3]
                    if search_text == first_name.lower() or search_text in last_name.lower():
                        found_students.append(f"ID: {academic_id} | {first_name} {last_name}")
        except FileNotFoundError:
            messagebox.showerror("Error", "Student file not found.")
            return

        if found_students:
            messagebox.showinfo("Student found", "\n".join(found_students))
        else:
            messagebox.showinfo("Not found", "No student with that name was found.")

    tk.Button(window_search_name, text="Search with name", width=15, command=find_name).pack(pady=15)

def search_id():
    global window_search_id
    #Prevent opening multiple search ID windows
    if window_search_id is not None and tk.Toplevel.winfo_exists(window_search_id):
        window_search_id.focus()
        return

    window_search_id = tk.Toplevel(window)
    window_search_id.geometry("300x200")
    window_search_id.title("Search an ID")

    def on_close():
        global window_search_id
        window_search_id.destroy()
        window_search_id = None
    window_search_id.protocol("WM_DELETE_WINDOW", on_close)

    tk.Label(window_search_id, text="Search a student by their academic ID").pack(pady=10)
    entry_id = tk.Entry(window_search_id)
    entry_id.pack(pady=5)

    def find_id():
        search_text = entry_id.get().strip().lower()
        if not search_text:
            messagebox.showwarning("Missing data", "Please enter an id")
            return

        student_found = None
        try:
            with open("Student's.csv", "r", encoding="utf-8") as file:
                for line in file:
                    if not line.strip():
                        continue
                    academic_id, first_name, last_name = line.strip().split(",")[:3]
                    if search_text in academic_id.lower():
                        student_found = f"ID: {academic_id} | {first_name} {last_name}"
                        break
        except FileNotFoundError:
            messagebox.showerror("Error", "Student not found")
            return

        if student_found:
            messagebox.showinfo("Student found", student_found)
        else:
            messagebox.showinfo("Not found", "No student with that academic id")

    tk.Button(window_search_id, text="Search with ID", width=15, command=find_id).pack(pady=15)

def update():
    global window_update
    #Prevent opening multiple update windows
    if window_update is not None and tk.Toplevel.winfo_exists(window_update):
        window_update.focus()
        return

    #Create a new window for updating
    window_update = tk.Toplevel(window)
    window_update.geometry("350x250")
    window_update.title("Update Student")

    def on_close():
        global window_update
        window_update.destroy()
        window_update = None
    window_update.protocol("WM_DELETE_WINDOW", on_close)

    tk.Label(window_update, text="Enter Academic ID to update:").pack(pady=5)
    entry_current_id = tk.Entry(window_update)
    entry_current_id.pack(pady=5)

    label_add = ["Academic ID", "First name", "Last name"]
    entries_update = {}

    #Create labels and entries for new data
    for text in label_add:
        frame = tk.Frame(window_update)
        frame.pack(pady=5)
        tk.Label(frame, text=text, width=12, anchor="w").pack(side="left")
        e = tk.Entry(frame)
        e.pack(side="left")
        entries_update[text] = e

    def load_student():
        current_id = entry_current_id.get().strip()
        if not current_id:
            messagebox.showwarning("Missing Data", "Please enter the Academic ID.")
            return

        found = False
        try:
            with open("Student's.csv", "r", encoding="utf-8") as file:
                for line in file:
                    if not line.strip():
                        continue
                    parts = line.strip().split(",")
                    if parts[0] == current_id:
                        entries_update["Academic ID"].delete(0, tk.END)
                        entries_update["Academic ID"].insert(0, parts[0])
                        entries_update["First name"].delete(0, tk.END)
                        entries_update["First name"].insert(0, parts[1])
                        entries_update["Last name"].delete(0, tk.END)
                        entries_update["Last name"].insert(0, parts[2])
                        found = True
                        break
        except FileNotFoundError:
            messagebox.showerror("Error", "Student not found.")
            return

        if not found:
            messagebox.showwarning("Not found", "No student found with that Academic ID.")

    def save_update():
        old_id = entry_current_id.get().strip()
        new_id = entries_update["Academic ID"].get().strip()
        first_name = entries_update["First name"].get().strip()
        last_name = entries_update["Last name"].get().strip()

        if not old_id or not new_id or not first_name or not last_name:
            messagebox.showwarning("Missing Data", "Please fill in all fields")
            return

        updated = False
        new_lines = []

        try:
            with open("Student's.csv", "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    parts = line.strip().split(",")
                    if parts[0] == old_id:
                        new_lines.append(f"{new_id},{first_name},{last_name},\n")
                        updated = True
                    else:
                        # Prevent duplicate new ID
                        if parts[0] == new_id and new_id != old_id:
                            messagebox.showerror("Duplicate ID", "Another student with this Academic ID already exists.")
                            return
                        new_lines.append(line)
        except FileNotFoundError:
            messagebox.showerror("Error", "file not found.")
            return

        if updated:
            #Save the updated CSV
            with open("Student's.csv", "w", encoding="utf-8") as f:
                f.writelines(new_lines)

            #Update Treeview
            for row in Table.get_children():
                values = Table.item(row)["values"]
                if values and str(values[0]) == old_id:
                    Table.item(row, values=(new_id, first_name, last_name))
                    break

            messagebox.showinfo("Success", "Student updated successfully!")
            entry_current_id.delete(0, tk.END)
            for entry in entries_update.values():
                entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Not found", "No student found with that Academic ID.")

    tk.Button(window_update, text="Load Student", width=20, command=load_student).pack(pady=5)
    tk.Button(window_update, text="Save Update", width=20, command=save_update).pack(pady=10)

#------Function to load students into the table at startup------
def load_students_into_table():
    try:
        with open("Student's.csv", "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                parts = line.strip().split(",")
                if len(parts) >= 3:
                    academic_id, first_name, last_name = parts[:3]
                    Table.insert("", "end", values=(academic_id, first_name, last_name))
    except FileNotFoundError:
        pass



#------Main window------
window = tk.Tk()
window.geometry("1200x800") #resolution of the window
window.title("School System") #name if the window
icon = PhotoImage(file = "School picture.png") #icon for the window
window.iconphoto(True,icon)




#--------Labels of the window--------
label_main = tk.Label(window, text = "School Management System", font=("sans-serif",24,"bold"))
label_counter = tk.Label(window,font = "sans-serif" , relief = "solid" , bd = 3 , pady = 12)

label_main.place(x = 380 , y = 30) #Position of the label
label_counter.place(x = 720 , y = 190) #Position of the label_counter


#--------Buttons for the main window-------

#button for adding a new student in the system
button_add = tk.Button(window, text = "Add a student", width = 25, height = 2, font = ("sans-serif",11) , command = student_addition)
button_add.place(x = 240 , y = 120)

#button for removing a student from the system
button_remove = tk.Button(window, text = "Remove a student", width = 25 , height = 2 , font = ("sans-serif",11) , command = student_remove)
button_remove.place(x = 240 , y = 190)

#searching a student in the system by using their name
button_search = tk.Button(window, text = "Find a student by their name", width = 25 , height = 2 , font = ("sans-serif",11), command = search_name)
button_search.place(x = 480 , y = 120)

#searching a student in the system by using their academic id
button_search_id = tk.Button(window, text = "Find a student by their academic ID", width=25 , height = 2 , font = ("sans-serif",11), command = search_id)
button_search_id.place(x = 480 , y = 190)

#for updating student's data
button_update = tk.Button(window, text = "Update a student's data", width = 25 , height= 2 , font = ("sans-serif",11), command = update)
button_update.place(x = 720 , y = 120)



#-----Tables-----
Table = ttk.Treeview(window,columns= ("ID","First","Last"), height = 20)


#-----Table headings------
Table.heading("ID", text = "Academic ID", anchor = "center")
Table.heading("First", text = "First Name", anchor = "center")
Table.heading("Last", text = "Last name", anchor = "center")

# center the text in columns
Table.column("ID", anchor="center")
Table.column("First", anchor="center")
Table.column("Last", anchor="center")


#hide the 4th column
Table.column("#0",width = 0 , stretch=tk.NO)
Table.heading("#0", text = "")
Table.place(x = 100 , y = 300 , width = 1000) #Tables position

#load student's into the tables
load_students_into_table()

#update student's counter
update_counter()

window.mainloop()




