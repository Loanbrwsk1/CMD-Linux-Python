"""
@author: Loan Borowski
"""

"""
TODO: ls cd mkdir cat touch rmdir pwd 
"""

#? Imports
import customtkinter as ctk
import json
import os

#? Classes
class Filesysteme:
    def __init__(self):
        self.current_dir = "/home/user"
        self.filesystem = {
            "/" : {
                "type" : "direcotry",
                "content" : ["home", "etc"]
            },
            "/home" : {
                "type" : "directory",
                "content" : ["user"]
            },
            "/home/user" : {
                "type" : "directory",
                "content" : ["text.txt", "Documents"]
            }, 
            "/home/user/text.txt" : {
                "type" : 'file',
                "content" : "Ceci est un test"
            },
            "/home/user/Documents" : {
                "type" : "directory",
                "content" : []
            }
        }

    def get_absolute_path(self, path):
        if path.startswith("/"):
            return path
        elif path == "..":
            if self.current_dir == "/":
                return "/"
            return "/".join(self.current_dir.split("/")[:-1]) or "/"
        elif path == ".":
            return self.current_dir
        else:
            if self.current_dir == "/":
                return "/" + path
            return self.current_dir + "/" + path
    
    def path_exists(self, path):
        return path in self.filesystem
    
    def is_directory(self, path):
        return self.filesystem[path]["type"] == "directory"
    
    def is_file(self, path):
        return self.filesystem[path]["type"] == "file"


class Terminal:
    def __init__(self):
        self.fs = Filesysteme()
        self.history = []
        self.output = ""
        
    def get_prompt(self):
        return cli.prompt

    def execute_command(self, command):
        self.history.append(f"{cli.prompt} {command}")

        parts = command.split()
        print(parts)
        cmd = parts[0]
        args = parts[1] if len(parts) > 1 else ""
        cli.entry.delete(0, len(command))

        if cmd == "ls":
            self.output = self.fs.filesystem[self.fs.current_dir]["content"]
            cli.display_output_ls(self.output)
        if cmd == "pwd":
            cli.display_output_pwd(self.fs.current_dir, cmd)
        if cmd == "clear":
            self.history = []
            self.output = ""
            cli.clear()



        

class CLI:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        self.terminal = Terminal()
        self.window = ctk.CTk()
        self.window.title("CMD")
        self.window.configure(background="#000000")
        self.window.geometry("800x450+240+80")
        self.window.resizable(width=False, height=False)
        self.prompt = f"(user@linux-device)-[{self.terminal.fs.current_dir}] $"
        self.label_prompt = ctk.CTkLabel(self.window, text=self.prompt, font=("Trebuchet MS", 15))
        self.label_prompt.place(x=10, y=2)
        self.entry = ctk.CTkEntry(self.window, font=("Trebuchet MS", 15), width=780)
        self.entry.place(x=10, y=30)
        self.output_display = ctk.CTkTextbox(self.window, width=780, height=370, fg_color="#000000", font=("Trebuchet MS", 15))
        self.output_display.place(x=10, y=65)
        self.window.bind("<Return>", self.execute_command)

    def execute_command(self, event):
        command = self.entry.get()
        self.terminal.execute_command(command)

    def display_output_ls(self, content):
        self.output_display.insert("end", f"{self.prompt} ls\n")
        for i in range(len(content)):
            if self.terminal.fs.filesystem[f"{self.terminal.fs.current_dir}/{content[i]}"]["type"] == "directory":
                self.output_display.insert("end", f"[d]{content[i]}    ")
            else:
                self.output_display.insert("end", f"[f]{content[i]}    ")
        self.output_display.insert("end", "\n\n")

    def display_output_pwd(self, content, command):
        self.output_display.insert("end", f"{self.prompt} {command}\n{content}\n\n")

    def clear(self):
        self.output_display.delete("0.0", "end")

    def run(self):
        self.window.mainloop()


#? Main
if __name__ == "__main__":
    cli = CLI()
    cli.run()