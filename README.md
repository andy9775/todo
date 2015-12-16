# todo

A simple command line todo script written in python with multiple todo lists

###Setup
1. Place `todo.py` into your preferred directory.
2. Type `cd /usr/local/bin` and execute `ln -s /path/to/todo.py todo`
3. Execute `chmod +x todo`

###Usage
From the command line call:<br>
- **`todo list`** - to list the current items in the todo list.<br>
- **`todo add`** - to add items to your todo list.<br>
- **`todo del #`** - to delete the item defined by # in the todo list<br>
- **`todo -to <listName> <action>`** - to perform the above actions on the 
list defined by `listName`. `todo -to otherList add "foo bar"` will add the 
todo item "foo bar" to the list "otherList".<br>
- **`todo del-list <listName>`** - to delete the list defined by 
"listName"<br>
- **`todo list-all`** - to print out the items in each todo list<br>
- **`todo show`** - to print out all the current todo list's

Each time an action is called a hook is executed. See the hooks readme file 
to learn more.

---
***MIT Licensed***
