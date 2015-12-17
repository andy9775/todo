#Hooks
Hooks are called after `todo <cmd>` is called. The possibilities include:
<br>
    - **`on_add`** - This hook is called after `todo add "new todo"` is 
    called. <br>
    - **`on_del`** - This hook is called after `todo del <#>` is called.<br>
    - **`on_list`** - This hook is called after `todo list`  and `todo 
    list-all` is called.<br>
    - **`on-del-list`** - This hook is called every time a user deletes alist
    
Each script is passed:<br>
1. The action being performed: to_add, to_del, to_list, rm_list, show_lists,
list_all<br>
2. The current items in the todo list (including any updates)<br>
3. Items being added to the list<br>
4. The name of the list that is being called
5. Additional arguments as specified by the `-s` command line argument<br>
 
###Setup
1. if `~/.todo/` does not exists, create it
2. create `~/.todo/hooks` directory
3. create the preferred hooks. These include: `on_list`, `on_add` and `on_del`

###Usage
Hooks can be used to trigger a web call and insert certain data into firebase which can then be synchronized with mobile devices.
