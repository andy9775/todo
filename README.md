# todo

A simple command line todo list written in python

###Setup
1. Place `todo.py` into your preferred directory.
2. Type `cd /usr/local/bin` and execute `ln -s /path/to/todo.py todo`
3. Execute `chmod +x todo`

###Usage
From the command line call:<br>
- **`todo list`** - to list the current items in the todo list.<br>
- **`todo add`** - to add items to your todo list.<br>
- **`todo del #`** - to delete the item defined by # in the todo list<br>
- **`todo -l <listName> <action>`** - to perform the above actions on the 
list defined by `listName`. `todo -l otherList add "foo bar"` will add the 
todo item "foo bar" to the list "otherList".<br>
- **`todo del-list <listName>`** - to delete the list defined by 
"listName"<br><br>

Each time an action is called a hook is executed. These hooks are 

---
***MIT Licensed***
