#!/usr/bin/env python
# this is the script to run from the command line
import argparse
import os
from subprocess import call
import sys
import re

# regular expression used to capture numbers with decimal separator at the
# start of a line
# eg captures '13.', '1.' etc.
REG_EX = r'^\d+\.'

# define constants:
#===============================================
ADD = 'to_add'
DEL = 'to_del'
LIST = 'to_list'
DEL_LIST = 'rm_list'
SHOW = 'show_lists'
LIST_ALL = 'list_all'

HOME_DIR = os.path.expanduser('~')
TODO_DIR = '.todo/'
HOOKS_DIR = 'hooks/'
#===============================================

# command functions

def todo_dir_exists():
    """
    Checks to see if the .todo directory exists in the users home directory
    :return: if directory exists return true else create it and return
        whether it exists
    :rtype: bool
    """
    if not os.path.exists(os.path.join(HOME_DIR, TODO_DIR)):
        os.makedirs(os.path.join(HOME_DIR, TODO_DIR))
    return os.path.exists(os.path.join(HOME_DIR, TODO_DIR))

def get_todo_file(fileName, mode = 'r'):
    """
    :param fileName: the todo list to return
    :type fileName:  str
    :param mode: open mode eg r, a, w
    :type mode: str
    :return: the todo file
    :rtype: file
    """
    fileName = os.path.join(HOME_DIR, TODO_DIR, fileName + '.txt')
    if not os.path.exists(fileName):
        open(fileName, 'w').close() # don't return a writeable file
    return open(fileName, mode)

def get_todo_list(listName):
    """
    Functions reads the todo list and returns the items in an array
    :param listName: The name of the todo list
    :type listName: str
    :return: a list of strings that are included in the todo list
    :rtype: list of strings
    """
    with get_todo_file(listName, 'r') as f:
        return f.readlines()

def write_to_todo_list(todo_name ,todos):
    """
    Writes the array of items to the todo list
    :param todos: todo's to write to the file
    :type todos: list of str
    :param todo_name: the todo list to append to
    :type todo_name: str
    """
    if type(todos) is str:
        todos = [todos]
    todos = [i.replace('\n','') for i in todos]
    item_num = len(get_todo_list(todo_name)) + 1

    with get_todo_file(todo_name, 'a') as f:
        for todo in todos:
            f.write(str(item_num) + '. ' + todo + '\n')
            item_num += 1

def delete_todo(item_num, todo_name):
    """
    Function will delete an item from the todo list
    :param item_num: the number of the item to delete
    :type item_num: int
    :param todo_name: the todo list name
    :type todo_name: str
    """
    todo_list = get_todo_list(todo_name)
    to_remove = []
    try:
        for num in item_num:
             to_remove.append(todo_list[num - 1])
    except IndexError:
        print('Wrong deletion numbers were entered. The list has ' + str(len(
            todo_list)) + ' item(s)')
        sys.exit(1)

    for item in to_remove:
        todo_list.remove(item)
    counter = 0
    for item in todo_list:
        item = re.sub(REG_EX, str(counter + 1) + '.', item)
        todo_list[counter] = item
        counter +=1
    with get_todo_file(todo_name, 'w') as f:
        f.write(''.join(todo_list))

def print_todos(todo_list):
    """
    Function will print the items in the todo list
    :param todo_list: the list to print
    :type todo_list: str
    """
    counter = 1
    for todo in get_todo_list(todo_list):
        todo = todo.replace('\n', '')
        print(todo)
        counter += 1
    if counter >1:
        print('-----------------')

def print_lists():
    """
    Function prints the available lists that the user can use.
    """
    print('Lists:')
    for item in get_current_todo_lists():
        if not item == '':
            print('\t' +item)
    print('-----------------')

def print_all_todos():
    todo_lists = get_current_todo_lists()
    for list in todo_lists:
        print('======= ' + list + ' =======')
        print_todos(list)

def delete_lists(list):
    """
    Function deletes the list specified by the argument
    :param list: The list to delete
    :type list: str
    """
    if len(list) == 0:
        print('No list provided. To delete a list call \n\ttodo del-list '
              '<list>')
    for item in list:
        if not os.path.exists(os.path.join(HOME_DIR, TODO_DIR, item + '.txt')):
            print(item + ' does not exist. Current options are: \n'+
              '\n'.join(get_current_todo_lists()))
            continue
        print('Deleting list ' + item + '...')
        os.remove(os.path.join(HOME_DIR, TODO_DIR, item + '.txt'))
        if not os.path.exists(os.path.join(HOME_DIR, TODO_DIR, item + '.txt')):
            print(item + ' deleted successfully')
        else:
            print(item + ' did not delete. Try running del-list again or '
                         'remove the list item manually')

def call_hooks(action, todo_list, add_todo, script_args, list_name):
    """
    Calls the hooks based on a certain user action. E.g. if a user calls
    `todo add "foo bar"
    the on_add script will be called and be passed the todo list name and the
    list of items added to the todo list.
    :param action: what is being performed
    :type action: const
    """
    directory = os.path.join(HOME_DIR, TODO_DIR, HOOKS_DIR)
    if action == ADD:
        directory += 'on_add'
    elif action == DEL:
        directory += 'on_del'
    elif action == LIST:
        directory += 'on_list'
    elif action == LIST_ALL:
        directory += 'on_list'
    elif action == DEL_LIST:
        directory += 'on_del_list'
    try:
        if os.path.exists(directory):
            call([directory, action, ''.join(todo_list), add_todo,
                  list_name, script_args])
            return True
        return False
    except OSError as e:
        print(action + ' hook could not be called. Make sure it exists ' \
                            'and '
                       'that you have permission to call it.')

# argparse functions:
def add_subparsers(parse):
    """
    Helper function to add the sub-parsers to the argparse instance
    :param parse: argparse instance
    :type parse: argparse
    """
    sub_parser = parse.add_subparsers()
    sub = sub_parser.add_parser('del')
    sub.add_argument(DEL, type=int, help='The item number to delete in the '
                                         'specified list. To select a list '
                                         'use -l', nargs='*')
    sub = sub_parser.add_parser('add')
    sub.add_argument(ADD, type=str, help='What you want to add to the todo '
                                         'list. To specify the list use -l',
                                         nargs='*')
    sub = sub_parser.add_parser('list')
    sub.add_argument(LIST, action='store_true', help='Shows a list of the '
                                                     'current todo\'s. To '
                                                     'specify the list use -l')
    sub = sub_parser.add_parser('del-list')
    sub.add_argument(DEL_LIST, help='Specify which list to remove.', nargs='*')

    sub = sub_parser.add_parser('show')
    sub.add_argument(SHOW, action='store_true', help='Show all the available '
                                                     'lists.')

    sub = sub_parser.add_parser('list-all')
    sub.add_argument(LIST_ALL, action='store_true', help='List the items in '
                                                         'all todo list\'s')

def get_action(args):
    """
    Function returns the action that is being performed.
    Includes:

    add
    del
    list
    del-list

    :param args:
    :type args:
    :return:
    :rtype:
    """
    args = args.__dict__
    if args.has_key(ADD):
        return ADD
    elif args.has_key(DEL):
        return DEL
    elif args.has_key(LIST):
        return LIST
    elif args.has_key(DEL_LIST):
        return DEL_LIST
    elif args.has_key(SHOW):
        return SHOW
    elif args.has_key(LIST_ALL):
        return LIST_ALL

def get_current_todo_lists():
    """
    :return: a list of the current todo lists
    :rtype: list of str
    """
    list = os.listdir(os.path.join(HOME_DIR, TODO_DIR))
    def filter(item):
        if item == '\n':
            return ''
        if item.endswith('.txt'):
            return item.replace('.txt','')
        return ''
    list =  map(filter, list)
    while list.count('') > 0:
        list.remove('')
    return list

if __name__ == '__main__':
    todo_dir_exists()

    parse = argparse.ArgumentParser(description='An easy to use todo list\n'
                                                '\tadd\t\tAdd items to a list\n'
                                                '\tlist\t\tList items in a '
                                                'list\n'
                                                '\tdel\t\tDelete an item from a '
                                                    'list\n'
                                                '\tdel-list\tDelete a list\n'
                                                '\tshow\t\tShow all the lists\n'
                                                '\tlist-all\tList all '
                                                'todo\'s\n',
                                    formatter_class=argparse.RawTextHelpFormatter)
    lists = get_current_todo_lists()

    parse.add_argument('-to', '-list','--list', type=str, default='todo',
                       help='Specify the list to add to. The current options '
                            'are:\n' + '\n  '.join(lists))
    parse.add_argument('-s', '--script', type=str, help='A string argument '
                                                        'passed to the script '
                                                        'called on the '
                                                        'action', default='')
    add_subparsers(parse)

    args = parse.parse_args()
    action = get_action(args)

    if action == ADD:
        write_to_todo_list( args.list, args.to_add,)
        print_todos(args.list)
    elif action == DEL:
        delete_todo(args.to_del, args.list)
        print_todos(args.list)
    elif action == LIST:
        print_todos(args.list)
    elif action == DEL_LIST:
        delete_lists(args.rm_list)
    elif action == SHOW:
        print_lists()
        sys.exit(0)
    elif action == LIST_ALL:
        print_all_todos()

    if not hasattr(args, 'to_add'):
        call_hooks(action, get_todo_list(args.list), '', args.script, args.list)
    else:
        call_hooks(action, get_todo_list(args.list), args.to_add,
                   args.script, args.list)
