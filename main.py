"""
@author: Loan Borowski
"""

#? Imports
import customtkinter as ctk

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
        if len(parts) == 0:
            cli.display_output("\n")
            return
        cmd = parts[0]
        args = parts[1] if len(parts) > 1 else ""
        cli.entry.delete(0, len(command))

        if cmd == "ls":
            self.ls(command, args)
        elif cmd == "pwd":
            self.pwd(cmd)
        elif cmd == "clear":
            self.clear()
        elif cmd == "cd":
            self.cd(command, args)
        elif cmd == "help":
            self.help(command)
        elif cmd == "cat":
            self.cat(command, args)
        elif cmd == "touch":
            self.touch(command, args)
        elif cmd == "rm":
            self.rm(command, args)
        elif cmd == "mkdir":
            self.mkdir(command, args)
        elif cmd == "rmdir":
            self.rmdir(command, args)
        elif cmd == "nano":
            self.nano(command, args)
        elif cmd == "quit" or cmd == "exit":
            self.quit()
        else:
            cli.display_output_cmd("Command not found", command)
             
    def ls(self, command, args):
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
        cli.display_output_ls(self.output, path, command)

    def pwd(self, command):
        cli.display_output_pwd(self.fs.current_dir, command)

    def clear(self):
        cli.clear()

    def cd(self, command, args):
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

    def help(self, command):
        help_text = """Available commands:
ls [path]     - List directory contents
pwd           - Print working directory
cd [path]     - Change directory
cat [file]    - Display file contents
touch [file]  - Create a file
rm [file]     - Delete a file
mkdir [dir]   - Create a directory
rmdir [dir]   - Delete a directory
nano [file]   - Edit a file
clear         - Clear terminal
help          - Show this help message"""
        cli.display_output_cmd(help_text, command)

    def cat(self, command, args):
        if not args:
            cli.display_output_cmd("cat: missing file operand", command)
            return
        path = self.fs.get_absolute_path(args)
        if not self.fs.path_exists(path):
            cli.display_output_cmd(f"cat: {args}: No such file or directory", command)
            return
        if not self.fs.is_file(path):
            cli.display_output_cmd(f"cat: {args}: Is a directory", command)
            return
        cli.display_output_cmd(self.fs.filesystem[path]["content"], command)

    def touch(self, command, args):
        if not args:
            cli.display_output_cmd("touch: missing file operand", command)
            return
        path = f"{self.fs.current_dir}/{args}"
        if not path in self.fs.filesystem:
            self.fs.filesystem[f"{self.fs.current_dir}/{args}"] = {"type" : "file", "content" : ""}
            self.fs.filesystem[f"{self.fs.current_dir}"]["content"].append(args)
        cli.display_output_cmd("", command)

    def rm(self, command, args):
        if not args:
            cli.display_output_cmd("rm: missing file operand", command)
            return
        path = self.fs.get_absolute_path(args)
        if not self.fs.path_exists(path):
            cli.display_output_cmd(f"rm: {args}: No such file", command)
            return
        if not self.fs.is_file(path):
            cli.display_output_cmd(f"rm: {args}: Is a directory", command)
            return
        self.fs.filesystem.pop(path)
        for v in self.fs.filesystem.values():
            if args in v["content"]:
                v["content"].remove(args)
                cli.display_output_cmd("", command)
                return
        
    def mkdir(self, command, args):
        if not args:
            cli.display_output_cmd("mkdir: missing directory operand", command)
            return
        path = f"{self.fs.current_dir}/{args}"
        if not path in self.fs.filesystem:
            self.fs.filesystem[f"{self.fs.current_dir}/{args}"] = {"type" : "directory", "content" : []}
            self.fs.filesystem[f"{self.fs.current_dir}"]["content"].append(args)
        cli.display_output_cmd("", command)

    def rmdir(self, command, args):
        if not args:
            cli.display_output_cmd("rmdir: missing directory operand", command)
            return
        path = self.fs.get_absolute_path(args)
        if not self.fs.path_exists(path):
            cli.display_output_cmd(f"rmdir: {args}: No such directory", command)
            return
        if self.fs.is_file(path):
            cli.display_output_cmd(f"rmdir: {args}: Is a file", command)
            return
        self.fs.filesystem.pop(path)
        for v in self.fs.filesystem.values():
            if args in v["content"]:
                v["content"].remove(args)
                cli.display_output_cmd("", command)
                return
        
    def quit(self):
        cli.running = False
        cli.window.destroy()

    def nano(self, command, args):
        if "/" in args:
            cli.display_output_cmd(f"nano: {args}: Don't use '/'", command)
            return
        if not args:
            cli.display_output_cmd("nano: missing file operand", command)
            return
        path = self.fs.get_absolute_path(args)
        if self.fs.is_directory(path):
            cli.display_output_cmd(f"nano: {args}: No such file")
            return
        if not self.fs.path_exists(path):
            cli.display_output_cmd(f"nano: {args}: No such directory")
            return
        self.nano_top_level = ctk.CTkToplevel(cli.window, fg_color="#000000")
        self.nano_top_level.geometry("800x420+640+80")
        self.nano_top_level.title(f"nano: {args}")
        self.nano_textbox = ctk.CTkTextbox(self.nano_top_level, width=806, height=426, font=("Trebuchet MS", 15), fg_color="#000000")
        cli.display_output_cmd("", command)
        self.nano_top_level.bind("<Alt_L>", lambda _:self.save_file(path))
        self.nano_textbox.insert("end", self.fs.filesystem[path]["content"])
        self.nano_textbox.place(x=-3, y=-3)
    
    def save_file(self, path):
        text = self.nano_textbox.get("0.0", "end")
        self.fs.filesystem[path]["content"] = text
        self.nano_top_level.destroy()

        
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
        self.running = True

    def execute_command(self, event):
        command = self.entry.get()
        self.terminal.execute_command(command)
        if self.running:
            self.display_output(f"{self.get_prompt()} ")

    def get_prompt(self):
        return f"(user@linux-device)-[{self.terminal.fs.current_dir}] $"

    def display_output(self, content):
        self.output_display.insert("end", content)

    def display_output_ls(self, content, path, command):
        self.output_display.insert("end", f"{command}\n")
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