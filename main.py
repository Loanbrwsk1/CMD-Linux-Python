"""
@author: Loan Borowski
"""

#? Imports
import customtkinter as ctk
import subprocess
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

    def execute_command(self, command:str):
        parts = command.split()
        if len(parts) == 0:
            cli.display_output("\n")
            return
        cmd = parts[0]
        args = parts[1:] if len(parts) > 1 else ""
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
        elif cmd == "cp":
            self.cp(command, args)
        elif cmd == "mv":
            self.mv(command, args)
        elif cmd == "ps":
            self.ps(command)
        elif cmd == "loan&leo":
            self.mystere(command)
        elif cmd == "maya":
            self.maya(command)
        elif cmd == "miam":
            self.crumble(command)
        elif cmd == "<3":
            self.heart(command)
        elif cmd == "quit" or cmd == "exit":
            self.quit()
        else:
            cli.display_output("Command not found", command)
            
    def ls(self, command:str, args:list[str]):
        path = self.fs.current_dir
        if args:
            path = self.fs.get_absolute_path(args[0])
        if not self.fs.path_exists(path):
            cli.display_output(f"ls: cannot access '{args[0] if args[0] else path}': No such file or directory", command)
            return
        if not self.fs.is_directory(path):
            cli.display_output(f"ls: {args[0] if args[0] else path}: Not a directory", command)
            return
        self.output = self.fs.filesystem[path]["content"]
        cli.display_output_ls(self.output, path, command)

    def pwd(self, command:str):
        cli.display_output_pwd(self.fs.current_dir, command)

    def clear(self):
        cli.clear()

    def cd(self, command:str, args:list[str]):
        if not args:
                self.fs.current_dir = "/home/user"
                cli.display_output(self.fs.current_dir, command)
                return
        path = self.fs.get_absolute_path(args[0])
        if args[0] in self.fs.filesystem[self.fs.current_dir]["content"] and self.fs.is_directory(path):
            self.fs.current_dir += f"/{args[0]}"
        elif args[0] == "..":
            self.fs.current_dir = self.fs.get_absolute_path(args[0])
        else:
            cli.display_output(f"bash: cd: '{args[0]}': No such directory", command)
            return
        cli.display_output(self.fs.current_dir, command)

    def help(self, command:str):
        help_text = """Available commands:
ls [path]                 - List directory contents
pwd                       - Print working directory
cd [path]                 - Change directory
cat [file]                - Display file contents
touch [file]              - Create a file
rm [file]                 - Delete a file
mkdir [dir]               - Create a directory
rmdir [dir]               - Delete a directory
nano [file]               - Edit a file. [Alt] to quit
cp [source] [destination] - Copy source into destination
mv [source] [destination] - Cut source into destination
clear                     - Clear terminal
help                      - Show this help message"""
        cli.display_output(help_text, command)

    def cat(self, command:str, args:list[str]):
        if not args:
            cli.display_output("cat: missing file operand", command)
            return
        path = self.fs.get_absolute_path(args[0])
        if not self.fs.path_exists(path):
            cli.display_output(f"cat: '{args[0]}': No such file or directory", command)
            return
        if not self.fs.is_file(path):
            cli.display_output(f"cat: '{args[0]}': Is a directory", command)
            return
        cli.display_output(self.fs.filesystem[path]["content"], command)

    def touch(self, command:str, args:list[str], from_other_command:bool=False):
        if not args:
            cli.display_output("touch: missing file operand", command)
            return
        if "/" in args[0]:
            cli.display_output(f"bash: touch: '{args[0]}': Cannot user '/' in name", command)
            return
        path = f"{self.fs.current_dir}/{args[0]}"
        if not path in self.fs.filesystem:
            self.fs.filesystem[f"{self.fs.current_dir}/{args[0]}"] = {"type" : "file", "content" : ""}
            self.fs.filesystem[f"{self.fs.current_dir}"]["content"].append(args[0])
        if not from_other_command:
            cli.display_output("", command)

    def rm(self, command:str, args:list[str], from_other_command:bool=False):
        if not args:
            cli.display_output("rm: missing file operand", command)
            return
        path = self.fs.get_absolute_path(args[0])
        if not self.fs.path_exists(path):
            cli.display_output(f"rm: '{args[0]}': No such file", command)
            return
        if not self.fs.is_file(path):
            cli.display_output(f"rm: '{args[0]}': Is a directory", command)
            return
        self.fs.filesystem.pop(path)
        for v in self.fs.filesystem.values():
            if args[0] in v["content"]:
                v["content"].remove(args[0])
                if not from_other_command:
                    cli.display_output("", command)
                return
        if not from_other_command:
            cli.display_output("", command)
        
    def mkdir(self, command:str, args:list[str], from_other_command:bool=False):
        if not args:
            cli.display_output("mkdir: missing directory operand", command)
            return
        if "/" in args[0]:
            cli.display_output(f"bash: mkdir: '{args[0]}': Cannot user '/' in name", command)
            return
        path = f"{self.fs.current_dir}/{args[0]}"
        if path not in self.fs.filesystem:
            self.fs.filesystem[path] = {"type" : "directory", "content" : []}
            self.fs.filesystem[f"{self.fs.current_dir}"]["content"].append(str(args[0]))
        if not from_other_command:
            cli.display_output("", command)

    def rmdir(self, command:str, args:list[str], from_other_command:bool=False):
        if not args:
            cli.display_output("rmdir: missing directory operand", command)
            return
        path = self.fs.get_absolute_path(args[0])
        if not self.fs.path_exists(path):
            cli.display_output(f"rmdir: {args[0]}: No such directory", command)
            return
        if self.fs.is_file(path):
            cli.display_output(f"rmdir: {args[0]}: Is a file", command)
            return
        self.fs.filesystem.pop(path)
        for v in self.fs.filesystem.values():
            if args[0] in v["content"]:
                v["content"].remove(args[0])
                if not from_other_command:
                    cli.display_output("", command)
                return
        if not from_other_command:
            cli.display_output("", command)
        
    def quit(self):
        cli.running = False
        cli.window.destroy()

    def nano(self, command:str, args:list[str]):
        if not args:
            cli.display_output("nano: missing file operand", command)
            return
        if "/" in args[0]:
            cli.display_output(f"nano: {args[0]}: Don't use '/'", command)
            return
        if not self.fs.path_exists(f"{self.fs.current_dir}/{args[0]}"):
            self.touch(command, [args[0]], True)
        path = self.fs.get_absolute_path(args[0])
        if self.fs.is_directory(path):
            cli.display_output(f"nano: {args[0]}: No such file")
            return
        self.nano_top_level = ctk.CTkToplevel(fg_color="#000000")
        self.nano_top_level.geometry("800x420+640+80")
        self.nano_top_level.resizable(False, False)
        self.nano_top_level.title(f"nano: {args[0]}")
        if os.name == "nt":
            self.nano_top_level.iconbitmap("icons/nano-icon.ico")
        self.nano_textbox = ctk.CTkTextbox(self.nano_top_level, width=806, height=426, font=("Trebuchet MS", 15), fg_color="#000000")
        self.nano_top_level.bind("<Alt_L>", lambda _:self.save_file(path))
        self.nano_textbox.insert("end", self.fs.filesystem[path]["content"])
        self.nano_textbox.place(x=-3, y=-3)
        cli.display_output("", command)
    
    def save_file(self, path:str):
        text = self.nano_textbox.get("0.0", "end")
        self.fs.filesystem[path]["content"] = text
        self.nano_top_level.destroy()

    def cp(self, command:str, args:list[str]):
        if not args:
            cli.display_output("cp: missing file operand", command)
            return
        if len(args) < 2:
            cli.display_output(f"cp: missing destination file operand after {args[0]}", command)
            return
        path1 = self.fs.get_absolute_path(args[0])
        path2 = self.fs.get_absolute_path(args[1])
        if not self.fs.path_exists(path1):
            cli.display_output(f"cp: {args[0]}: Not such file or directory", command)
            return
        if not self.fs.path_exists(path2):
            cli.display_output(f"cp: {args[1]}: Not such file or directory", command)
            return
        if self.fs.is_file(path1) and self.fs.is_directory(path2):
            self.fs.filesystem[f"{path2}/{args[0]}"] = self.fs.filesystem[path1]
            self.fs.filesystem[path2]["content"].append(args[0])
        elif self.fs.is_file(path1) and self.fs.is_file(path2):
            self.fs.filesystem[path2] = self.fs.filesystem[path1]
        elif self.fs.is_directory(path1) and self.fs.is_directory(path2):
            self.fs.filesystem[f"{path2}/{args[0]}"] = self.fs.filesystem[path1]
            self.fs.filesystem[path2]["content"].append(args[0])
            for i in self.fs.filesystem[path1]["content"]:
                self.fs.filesystem[f"{path2}/{args[0]}/{i}"] = self.fs.filesystem[f"{self.fs.get_absolute_path(f"{path1}/{i}")}"]
        else:
            cli.display_output(f"cp: cannot overwrite non-directory {args[0]} with directory {args[1]}", command)
        cli.display_output("", command)

    def mv(self, command:str, args:list[str]):
        if not args:
            cli.display_output("mv: missing file operand", command)
            return
        if len(args) < 2:
            cli.display_output(f"mv: missing destination file operand after {args[0]}", command)
            return
        path1 = self.fs.get_absolute_path(args[0])
        path2 = self.fs.get_absolute_path(args[1])
        if not self.fs.path_exists(path1):
            cli.display_output(f"mv: {args[0]}: Not such file or directory", command)
            return
        if not self.fs.path_exists(path2):
            if self.fs.is_file(path1):
                self.touch(command, [args[1]], True)
            else:
                self.mkdir(command, [args[1]], True)
        if self.fs.is_file(path1) and self.fs.is_directory(path2):
            self.fs.filesystem[f"{path2}/{args[0]}"] = self.fs.filesystem[path1]
            self.fs.filesystem[path2]["content"].append(args[0])
            self.rm(command, [args[0]], True)
        elif self.fs.is_file(path1) and self.fs.is_file(path2):
            self.fs.filesystem[path2] = self.fs.filesystem[path1]
            self.rm(command, [args[0]], True)
        elif self.fs.is_directory(path1) and self.fs.is_directory(path2):
            self.fs.filesystem[f"{path2}/{args[0]}"] = self.fs.filesystem[path1]
            self.fs.filesystem[path2]["content"].append(args[0])
            for i in self.fs.filesystem[path1]["content"]:
                self.fs.filesystem[f"{path2}/{args[0]}/{i}"] = self.fs.filesystem[f"{self.fs.get_absolute_path(f"{path1}/{i}")}"]
            self.rmdir(command, [args[0]], True)
        else:
            cli.display_output(f"mv: cannot overwrite non-directory {args[0]} with directory {args[1]}", command)
        cli.display_output("", command)
        
    def ps(self, command:str):
        if os.name == "posix":
            cli.display_output(f"{subprocess.run(["ps"], capture_output=True, text=True).stdout}", command)
        elif os.name == "nt":
            cli.display_output(f"{os.popen('tasklist').read()}", command)

    def mystere(self, command:str):
        cli.display_output("""         _nnnn_                      
        dGGGGMMb     ,''''''''''''''''''''''''''''''''''''''''''''.
       @p~qp~~qMb    | Hello, this app was made by Loan and Leo ! |
       M|@||@) M|   _;............................................'
       @,----.JM| -'
      JS^\\__/  qKL
     dZP        qKRb
    dZP          qKKb
   fZP            SMMb
   HZM            MMMM
   FqM            MMMM
 __| ".        |\\dS"qML
 |    `.       | `' \\Zq
_)      \\.___.,|     .'
\\____   )MMMMMM|   .'
     `-'       `--' hjm""", command)
        
    def maya(self, command:str):
        cli.display_output("""
   \\\\\\|||///
 .  ======= 
/ \\| O   O |
\\ / \\`___'/ 
 #   _| |_
(#) (     )  
 #\\//|* *|\\\\ 
 #\\/(  *  )/   
 #   =====  
 #   ( U ) 
 #   || ||
.#---'| |`----.
`#----' `-----'""", command)

    def crumble(self, command:str):
        cli.display_output(""" Le crumble salé aux deux patates de Mr Galand
                               
                   .
                  / `.
                .'... `-.
              .'.. .   ..\\
             /. . . .   ..`.
            /...  ... .    .\\
           /.. . ........   .\\
         .'.   ...   ......  .|
       .' ... . ..... . ..--'.|
     .' ...  ...   ._.--'    .|
   .'... . ...  _.-'O   OO O .|
  /... .___.---'O OO .O. OO O.|
 /__.--' OO O  .OO O  OO O ...|
 | OO OO O OO . .O. OO O  ..O.|
 (O. OO. .O O O O  OO  ..OO O.|
 ( OO .O. O  O  OO............|
 (OOO........O_______.-------'
 |_____.-----'""", command)

    def heart(self, command:str):
        cli.display_output("""      _____           _____
  ,ad8PPPP88b,     ,d88PPPP8ba,
 d8P"      "Y8b, ,d8P"      "Y8b
dP'           "8a8"           `Yd
8(              "              )8
I8                             8I
 Yb,                         ,dP
  "8a,                     ,a8"
    "8a,                 ,a8"
      "Yba             adP"
        `Y8a         a8P'
          `88,     ,88'
            "8b   d8"
             "8b d8"
              `888'
                """, command)


class CLI:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        self.terminal = Terminal()
        self.window = ctk.CTk()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        self.window.title("CMD")
        if os.name == "nt":
            self.window.iconbitmap("icons/terminal-icon.ico")
        self.window.configure(fg_color="#000000")
        self.window.geometry(f"{screen_width // 2}x{screen_height // 2}")
        self.window.resizable(width=False, height=False)
        self.prompt = f"(user@linux-device)-[{self.terminal.fs.current_dir}] $"
        self.entry = ctk.CTkEntry(self.window, font=("Terminal", 15), width=screen_width // 2 - 20, border_color="#FFFFFF", fg_color="#000000", border_width=1, placeholder_text="Enter your commands here", placeholder_text_color="#ECECEC", corner_radius=0)
        self.entry.place(x=10, y=10)
        self.output_display = ctk.CTkTextbox(self.window, width=screen_width // 2 - 20, height=screen_height // 2 - 60, fg_color="#000000", font=("Terminal", 15), border_color="#FFFFFF", border_width=1, text_color="#FFFFFF", corner_radius=0)
        self.output_display.insert("end", f"{self.prompt} ")
        self.output_display.configure(state="disabled")
        self.output_display.place(x=10, y=45)
        self.window.bind("<Return>", self.execute_command)
        self.running = True

    def execute_command(self, event):
        command = self.entry.get()
        self.output_display.configure(state="normal")
        self.terminal.execute_command(command)
        self.window.title(command)
        if self.running:
            self.output_display.insert("end", f"{self.get_prompt()} ")
        self.output_display.configure(state="disabled")

    def get_prompt(self):
        return f"(user@linux-device)-[{self.terminal.fs.current_dir}] $"

    def display_output_ls(self, content:str, path:str, command:str):
        self.output_display.insert("end", f"{command}\n")
        for i in range(len(content)):
            if self.terminal.fs.filesystem[f"{path}/{content[i]}"]["type"] == "directory":
                self.output_display.insert("end", f"[d]{content[i]}    ")
            else:
                self.output_display.insert("end", f"[f]{content[i]}    ")
        self.output_display.insert("end", "\n\n")

    def display_output(self, content:str, command:str=""):
        if len(command) > 0:
            self.output_display.insert("end", f"{command}\n{content}\n\n")
        else:
            self.output_display.insert("end", f"{content}\n")

    def clear(self):
        self.output_display.delete("0.0", "end")

    def run(self):
        self.window.mainloop()


#? Main
if __name__ == "__main__":
    cli = CLI()
    cli.run()
