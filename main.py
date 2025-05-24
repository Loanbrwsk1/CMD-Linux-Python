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
        self.output = ""
        
    def get_prompt(self):
        return cli.prompt

    def execute_command(self, command):
        parts = command.split()
        print(parts)
        cmd = parts[0]
        args = parts[1] if len(parts) > 1 else ""
        cli.entry.delete(0, len(command))

        if cmd == "ls":
            self.ls_cmd(command, args)
        if cmd == "pwd":
            self.pwd_cmd(cmd)
        if cmd == "clear":
            self.clear_cmd()
        if cmd == "cd":
            self.cd_cmd(command, args)
        if cmd == "help":
            self.help_cmd(command)
                
    def ls_cmd(self, command, args):
        path = self.fs.current_dir
        if args:
            path = self.fs.get_absolute_path(args)
        if not self.fs.path_exists(path):
            cli.display_output_cmd(f"ls: cannot access '{args if args else path}': No such file or directory", command)
            return
        if not self.fs.is_directory(path):
            cli.display_output_cmd(f"ls: {args if args else path}: Not a directory", command)
            return
        self.output = self.fs.filesystem[path]["content"]
        cli.display_output_ls(self.output, path)

    def pwd_cmd(self, command):
        cli.display_output_pwd(self.fs.current_dir, command)

    def clear_cmd(self):
        cli.clear()

    def cd_cmd(self, command, args):
        if not args:
                self.fs.current_dir = "/home/user"
        elif args in self.fs.filesystem[self.fs.current_dir]["content"] and self.fs.filesystem[self.fs.current_dir]["type"] == "directory":
            self.fs.current_dir += f"/{args}"
        elif args == "..":
            self.fs.current_dir = self.fs.get_absolute_path(args)
        else:
            cli.display_output_cmd(f"bash: cd: {args}: No such file or directory", command)
            return
        cli.display_output_cmd(self.fs.current_dir, command)

    def help_cmd(self, command):
        help_text = """Available commands:
ls [path]     - List directory contents
pwd           - Print working directory
cd [path]     - Change directory
cat [file]    - Display file contents
clear         - Clear terminal
help          - Show this help message"""
        cli.display_output_cmd(help_text, command)


class CLI:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        self.terminal = Terminal()
        self.window = ctk.CTk()
        self.window.title("CMD")
        self.window.configure(background="#000000")
        self.window.geometry("800x420+240+80")
        self.window.resizable(width=False, height=False)
        self.prompt = f"(user@linux-device)-[{self.terminal.fs.current_dir}] $"
        self.entry = ctk.CTkEntry(self.window, font=("Trebuchet MS", 15), width=780)
        self.entry.place(x=10, y=10)
        self.output_display = ctk.CTkTextbox(self.window, width=780, height=370, fg_color="#000000", font=("Trebuchet MS", 15))
        self.output_display.insert("end", f"{self.prompt} ")
        self.output_display.place(x=10, y=45)
        self.window.bind("<Return>", self.execute_command)

    def execute_command(self, event):
        command = self.entry.get()
        self.terminal.execute_command(command)
        self.display_output(f"{self.get_prompt()} ")

    def get_prompt(self):
        return f"(user@linux-device)-[{self.terminal.fs.current_dir}] $"

    def display_output(self, content):
        self.output_display.insert("end", content)

    def display_output_ls(self, content, path):
        self.output_display.insert("end", "ls\n")
        for i in range(len(content)):
            if self.terminal.fs.filesystem[f"{path}/{content[i]}"]["type"] == "directory":
                self.output_display.insert("end", f"[d]{content[i]}    ")
            else:
                self.output_display.insert("end", f"[f]{content[i]}    ")
        self.output_display.insert("end", "\n\n")

    def display_output_cmd(self, content, command):
        self.output_display.insert("end", f" {command}\n{content}\n\n")

    def clear(self):
        self.output_display.delete("0.0", "end")

    def run(self):
        self.window.mainloop()


#? Main
if __name__ == "__main__":
    cli = CLI()
    cli.run()