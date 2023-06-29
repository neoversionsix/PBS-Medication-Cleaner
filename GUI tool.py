import pandas as pd
from tkinter import Tk, Button, Label, filedialog

class Application:
    def __init__(self, window):
        self.window = window
        self.file_loc_name = ""

        self.load_button = Button(window, text="Load Text File", command=self.load_file)
        self.load_button.pack()

        self.save_button = Button(window, text="Save as Excel File", command=self.save_as_excel, state="disabled")
        self.save_button.pack()

        self.status_label = Label(window, text="", bg="white")
        self.status_label.pack()

        self.close_button = Button(window, text="Close", command=self.close_app)
        self.close_button.pack()

    def load_file(self):
        self.file_loc_name = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if self.file_loc_name:
            self.status_label["text"] = f"Loaded file: {self.file_loc_name}"
            self.save_button["state"] = "normal"
        else:
            self.status_label["text"] = "No file loaded"
            self.save_button["state"] = "disabled"

    def save_as_excel(self):
        df_file_out = self.process_file(self.file_loc_name)
        file_save_name = filedialog.asksaveasfilename(defaultextension=".xlsx")
        df_file_out.to_excel(file_save_name, index = False)
        self.status_label["text"] = f"File has been saved as {file_save_name}"

    def close_app(self):
        self.window.destroy()

    @staticmethod
    def process_file(file_loc_name):
        column_names = ['desc', 'ID', 'role']
        df_file = pd.read_csv(file_loc_name, sep = '\t', header=0, names = column_names)
        df_file_out = df_file.drop_duplicates(subset='ID', keep=False)
        unique_IDs = df_file_out['ID'].tolist()

        for id in set(df_file['ID']):
            if id not in unique_IDs:
                df_temp = df_file[df_file['ID'] == id]
                roles = " ".join(df_temp.role.tolist())
                df_temp_role_merged = df_temp.iloc[[0]].copy()
                df_temp_role_merged['role'] = roles
                df_file_out = pd.concat([df_file_out, df_temp_role_merged])
                unique_IDs.append(id)
        return df_file_out

def main():
    root = Tk()
    app = Application(root)
    root.mainloop()

if __name__ == "__main__":
    main()
