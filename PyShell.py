import os
import time
from xml.dom import minidom


class ErrorInProgram(Exception):
    def __int__(self, error_message: str):
        super().__init__(error_message)


def __path_exist(__path: str):
    return os.path.exists(__path)


def __get_files_of_a_path(__path: str):
    if not __path_exist(__path):
        __print_error(__strings["path_does_not_exist"])
    __all_files = []
    for __all in os.listdir(__path):
        if not os.path.isdir(os.path.join(__path, __all)):
            __all_files.append(__all)
    return __all_files


def __get_folders_of_a_path(__path: str):
    if not __path_exist(__path):
        __print_error(__strings["path_does_not_exist"])
    __all_folders = []
    for __all in os.listdir(__path):
        if os.path.isdir(os.path.join(__path, __all)):
            __all_folders.append(__all)
    return __all_folders


def __change_language(__new_language: str):
    global __language
    if __new_language not in __infos['available_languages']:
        __print_error(__strings['not_a_valid_language_1']+__new_language+__strings['not_a_valid_language_2'])
    __language = __new_language
    __load_language()


def __load_language():
    __path = os.path.dirname(__file__)+"\\"+__language+"_strings.xml"
    __load_xml_file(__path)


def __load_xml_file(__file_path: str):
    if not __path_exist(__file_path):
        __print_error(__strings["file_path_does_not_exist_1"]+__file_path+__strings["file_path_does_not_exist_2"])
    __file = minidom.parse(__file_path)
    __all_infos = __file.getElementsByTagName('info')
    __all_strings = __file.getElementsByTagName('string')
    for __info in __all_infos:
        __infos[__info.attributes['id'].value] = __info.firstChild.data
    for __string in __all_strings:
        __strings[__string.attributes['id'].value] = __string.firstChild.data
    __infos['available_languages'] = __infos['available_languages'].split(',')


def __print_error(error_message: str):
    raise ErrorInProgram(__strings["error_message"]+" "+error_message)


def __change_directory(__new_path: str):
    global __current_folder, __files_in_directory, __folders_in_directory, ___prompt
    if not __path_exist(__new_path):
        __print_error(__strings['path_does_not_exist_1'] + __new_path + __strings['path_does_not_exist_2'])
    __files_in_directory = __get_files_of_a_path(__new_path)
    __folders_in_directory = __get_folders_of_a_path(__new_path)
    if ___prompt == __current_folder:
        ___prompt = __new_path
    __current_folder = __new_path
    os.chdir(__new_path)


def __previous_folder(__path: str):
    return os.path.dirname(__path)


def __cd(__path: str):
    global __current_folder
    try:
        if __path == '..':
            __change_directory(__previous_folder(__current_folder))
        elif __path == '/':
            __change_directory(__current_folder[:2])
        elif __path == '':
            print(__current_folder)
        elif __path[:2] in ('-h', '/?', '-?'):
            __help_commands('cd')
        elif __path_exist(__current_folder+'\\'+__path):
            __change_directory(__current_folder+'\\'+__path)
        elif not __path_exist(__path):
            __print_error(__strings['path_does_not_exist_1'] + __path + __strings['path_does_not_exist_2'])
        else:
            __change_directory(__path)
    except PermissionError:
        __print_error(__strings['you_dont_have_permissions_to_this_path']+__path)


def __rmdir(__path: str):
    if __path == '' or (__path[:2] in ('-h', '/?', '-?')):
        __help_commands('rmdir')
    elif len(__path) >= 2:
        if __path[1] != ':':
            if __path[0] not in '\\/':
                __path = '\\'+__path
            __path = __current_folder + __path
    else:
        __path = __current_folder + '\\' + __path
    if os.path.isdir(__path):
        import shutil
        shutil.rmtree(__path)
        if __path == __current_folder:
            __change_directory(__previous_folder(__current_folder))
        else:
            __change_directory(__current_folder)
    elif os.path.isfile(__path):
        __print_error(__strings['path_is_a_file_not_a_dir'])
    elif not __path_exist(__path):
        __print_error(__strings['path_does_not_exist_1'] + __path + __strings['path_does_not_exist_2'])


def __mkdir(__path: str):
    if __path == '' or (__path[:2] in ('-h', '/?', '-?')):
        __help_commands('mkdir')
    elif len(__path) >= 2:
        if (__path[1] != ':') and (__path[0].lower() not in 'abcdefghijklmnopqrstuvwxyz'):
            if __path[0] not in '\\/':
                __path = '\\'+__path
            __path = __current_folder + __path
    else:
        __path = __current_folder + '\\' + __path
    if __path_exist(__path):
        __print_error(__strings['path_already_exist'])
    else:
        os.mkdir(__path)
        __change_directory(__current_folder)


def __delete(__path: str):
    if __path == '' or (__path[:2] in ('-h', '/?', '-?')):
        __help_commands('delete')
    elif len(__path) >= 2:
        if __path[1] != ':':
            if __path[0] not in '\\/':
                __path = '\\'+__path
            __path = __current_folder + __path
    else:
        __path = __current_folder + '\\' + __path
    if os.path.isdir(__path):
        __print_error(__strings['path_is_a_dir_not_a_file'])
    elif os.path.isfile(__path):
        os.remove(__path)
    elif not __path_exist(__path):
        __print_error(__strings['path_does_not_exist_1'] + __path + __strings['path_does_not_exist_2'])


def __dir(__path: str):
    if __path[:2] in ('-h', '/?', '-?'):
        __help_commands('dir')
    elif __path == '':
        __path = __current_folder
    elif len(__path) >= 2:
        if __path[1] != ':':
            if __path[0] not in '\\/':
                __path = '\\'+__path
            __path = __current_folder + __path
    else:
        __path = __current_folder + '\\' + __path
    if os.path.isfile(__path):
        __print_error(__strings['path_is_a_file_not_a_dir'])
    elif not __path_exist(__path):
        __print_error(__strings['path_does_not_exist_1']+__path+__strings['path_does_not_exist_2'])
    else:
        __taille_totale_fichier = 0
        __folders = __get_folders_of_a_path(__path)
        __files = __get_files_of_a_path(__path)
        if len(__folders) == 0 and len(__files) == 0:
            __print_error(__strings['no_file_or_folder_in_the_path'])
        from datetime import datetime
        ft = datetime.fromtimestamp
        print(__strings['file_and_dir_creation_date'], ';', __strings['file_and_dir_creation_hour'], ';',
              __strings['file_and_dir_last_modified_date'], ';', __strings['file_and_dir_last_modified_hour'], ';',
              __strings['file_or_dir'], ';', __strings['file_and_dir_size'], ';', __strings['file_and_dir_name'])
        for __folder in __folders:
            __folder_infos = os.stat(__path+'\\'+__folder)
            print(ft(__folder_infos.st_ctime).strftime("%Y-%m-%d ; %H:%M"), ';',
                  ft(__folder_infos.st_mtime).strftime("%Y-%m-%d ; %H:%M"), ';', __strings['folder'], ';',
                  str(__folder_infos.st_size/1000)+'kb', ';', __folder)
        for __file in __files:
            __file_infos = os.stat(__path+'\\'+__file)
            print(ft(__file_infos.st_ctime).strftime("%Y-%m-%d ; %H:%M"), ';',
                  ft(__file_infos.st_mtime).strftime("%Y-%m-%d ; %H:%M"), ';', __strings['file'], ';',
                  str(__file_infos.st_size/1000)+'kb', ';', __file)


def __start(__command: str):
    import os
    import platform
    if platform.system() == "Windows":
        os.system("start "+__command)
    elif platform.system() == "Linux":
        __print_error(__strings['this_command_is_not_available_for_linux'])


def __execute(__command: str):
    import os
    import platform
    if platform.system() == "Windows":
        os.system(__command)
    elif platform.system() == "Linux":
        os.system("xdg-open "+__command)


def __move(__paths: list):
    if len(__paths) == 1:
        if __paths[0] == '':
            __help_commands('move')
        else:
            __print_error(__strings['bad_syntax_for_the_command'])
    else:
        __paths = __paths[1:]
    if len(__paths) == 2:
        if not __path_exist(__paths[0]):
            __print_error(__strings['file_or_folder_path_does_not_exist_1'] + __paths[0] + 
                          __strings['file_or_folder_path_does_not_exist_2'])
        if not __path_exist(__previous_folder(__paths[1])):
            __print_error(__strings['path_for_the_new_file_or_folder_does_not_exist'])
        import os
        import platform
        if platform.system() == "Windows":
            __command = 'move ' + '"' + __paths[0] + '" "' + __paths[1] + '"'
            os.system(__command)
        elif platform.system() == "Linux":
            __command = 'mv ' + '"' + __paths[0] + '" "' + __paths[1] + '"'
            os.system(__command)
    elif len(__paths) > 2:
        __print_error(__strings['you_enter_too_much_arguments'] + ' ' + 
                      __strings['in_fact_this_command_take_a_number_of_arguments_1'] + '2' + 
                      __strings['in_fact_this_command_take_a_number_of_arguments_2'])


def __type(__path: str):
    import os
    import platform
    if __path == '':
        __help_commands('type')
    elif not __path_exist(__path):
        __print_error(__strings['file_path_does_not_exist_1']+__path+__strings['file_path_does_not_exist_2'])
    elif not os.path.isfile(__path):
        __print_error(__strings['path_is_a_dir_not_a_file'])
    else:
        if platform.system() == "Windows":
            os.system("type '"+__path+"'")
        elif platform.system() == "Linux":
            os.system("cat '"+__path+"'")


def __cls():
    import os
    import platform
    if platform.system() == "Windows":
        os.system("cls")
    elif platform.system() == "Linux":
        os.system("clear")


def __systeminfo():
    import os
    import platform
    if platform.system() == "Windows":
        os.system("systeminfo")
    elif platform.system() == "Linux":
        os.system("cat /etc/os-release* \\n uname -a")


def __title(__title_name: str):
    if __title_name == '':
        __help_commands('title')
    else:
        import os
        import platform
        if platform.system() == "Windows":
            os.system("title "+__title_name)
        elif platform.system() == "Linux":
            __print_error(__strings['this_command_is_not_available_for_linux'])


def __prompt(__new_prompt: str):
    global ___prompt
    if __new_prompt == '':
        ___prompt = __current_folder
    else:
        ___prompt = __new_prompt


def __regedit():
    import os
    import platform
    if platform.system() == "Windows":
        os.system("regedit")
    elif platform.system() == "Linux":
        __print_error(__strings['this_command_is_not_available_for_linux'])


def __color(__color: str):
    if __color == '':
        __help_commands('color')
    elif len(__color) != 2:
        __print_error(__strings['bad_syntax_for_the_command'])
    elif (__color[0] not in '0123456789abcdef') or (__color[1] not in '0123456789abcdef'):
        __print_error(__strings['bad_syntax_for_the_command'])
    else:
        import os
        import platform
        if platform.system() == "Windows":
            os.system("color "+__color)
        elif platform.system() == "Linux":
            __print_error(__strings['this_command_is_not_available_for_linux'])


def __sfc(__arg: str):
    if __arg == '':
        __help_commands('sfc')
    elif __arg.lower() not in ('/scannow', '/verifyonly%', '/scanfile%', '/verifyfile%', '/offbootdir%',
                               '/offwindir%', '/offlogfile'):
        __print_error(__strings['not_a_valid_argument_1']+__arg+__strings['not_a_valid_argument_2'])
    else:
        import os
        import platform
        if platform.system() == "Windows":
            os.system("sfc "+__arg)
        elif platform.system() == "Linux":
            __print_error(__strings['this_command_is_not_available_for_linux'])


def __tree():
    import os
    import platform
    if platform.system() == "Windows":
        os.system("tree")
    elif platform.system() == "Linux":
        __print_error("tree")


def __ipconfig(__args: list[str]):
    import os
    import platform
    if platform.system() == "Windows":
        __command = 'ipconfig'
        if len(__args) >= 1:
            if __args[0] == '/all':
                if len(__args) != 1:
                    __print_error(__strings['bad_syntax_for_the_command'])
                __command += ' /all'
            elif __args[0] == '/flushdns':
                if len(__args) != 1:
                    __print_error(__strings['bad_syntax_for_the_command'])
                __command += ' /flushdns'
            elif __args[0] == '/displaydns':
                if len(__args) != 1:
                    __print_error(__strings['bad_syntax_for_the_command'])
                __command += ' /displaydns'
            elif __args[0] == '/registerdns':
                if len(__args) != 1:
                    __print_error(__strings['bad_syntax_for_the_command'])
                __command += ' /registerdns'
            elif __args[0] == '/release':
                if len(__args) not in (1, 2):
                    __print_error(__strings['bad_syntax_for_the_command'])
                __command += ' /release'
                if len(__args) == 2:
                    __command += ' ' + __args[1]
            elif __args[0] == '/release6':
                if len(__args) not in (1, 2):
                    __print_error(__strings['bad_syntax_for_the_command'])
                __command += ' /release6'
                if len(__args) == 2:
                    __command += ' ' + __args[1]
            elif __args[0] == '/renew':
                if len(__args) not in (1, 2):
                    __print_error(__strings['bad_syntax_for_the_command'])
                __command += ' /renew'
                if len(__args) == 2:
                    __command += ' ' + __args[1]
            elif __args[0] == '/renew6':
                if len(__args) not in (1, 2):
                    __print_error(__strings['bad_syntax_for_the_command'])
                __command += ' /renew6'
                if len(__args) == 2:
                    __command += ' ' + __args[1]
            elif __args[0] == '/showclassid':
                if len(__args) != 2:
                    __print_error(__strings['bad_syntax_for_the_command'])
                __command += ' /showclassid ' + __args[1]
            elif __args[0] == '/showclassid6':
                if len(__args) != 2:
                    __print_error(__strings['bad_syntax_for_the_command'])
                __command += ' /showclassid6 ' + __args[1]
            elif __args[0] == '/setclassid':
                if len(__args) not in (2, 3):
                    __print_error(__strings['bad_syntax_for_the_command'])
                __command += ' /setclassid ' + __args[1]
                if len(__args) == 3:
                    __command += ' ' + __args[2]
            elif __args[0] == '/setclassid6':
                if len(__args) not in (2, 3):
                    __print_error(__strings['bad_syntax_for_the_command'])
                __command += ' /setclassid6 ' + __args[1]
                if len(__args) == 3:
                    __command += ' ' + __args[2]
            elif __args[0] == '/allcompartments':
                if len(__args) not in (1, 2):
                    __print_error(__strings['bad_syntax_for_the_command'])
                __command += ' /allcompartments'
                if len(__args) == 2:
                    if __args[1] != '/all':
                        __print_error(
                            __strings['not_a_valid_argument_1'] + __args[1] + __strings['not_a_valid_argument_2'])
                    __command += ' /all'
            else:
                __print_error(__strings['not_a_valid_argument_1'] + __args[0] + __strings['not_a_valid_argument_2'])
    else:
        __command = 'ifconfig'
        if len(__args) >= 1:
            if __args[0] == '/all':
                if len(__args) != 1:
                    __print_error(__strings['bad_syntax_for_the_command'])
                __command += ' /all'
    os.system(__command)


def __nslookup(__arg: str):
    import os
    import platform
    if platform.system() == "Windows":
        os.system("nslookup "+__arg)
    elif platform.system() == "Linux":
        os.system("nslookup "+__arg)


def __tasklist(__arg: str):
    import os
    import platform
    if platform.system() == "Windows":
        os.system("tasklist " + __arg)
    elif platform.system() == "Linux":
        __print_error("ps -aux")


def __control(__arg: str):
    if __arg.lower() not in ('', 'admintools', 'desktop', 'folders', 'fonts', 'keyboard', 'mouse', 'printers',
                             'schedtasks', 'color'):
        __print_error(__strings['not_a_valid_argument_1'] + __arg + __strings['not_a_valid_argument_2'])
    else:
        import os
        import platform
        if platform.system() == "Windows":
            os.system("control " + __arg)
        elif platform.system() == "Linux":
            __print_error(__strings['this_command_is_not_available_for_linux'])


def __help_commands(__command: str):
    if __command in ('', 'help'):
        print(__strings['help_help'])
    elif __command == 'cd':
        print(__strings['help_cd'])
    elif __command == 'rmdir':
        print(__strings['help_rmdir'])
    elif __command == 'mkdir':
        print(__strings['help_mkdir'])
    elif __command == 'delete':
        print(__strings['help_delete'])
    elif __command == 'dir':
        print(__strings['help_dir'])
    elif __command == 'start':
        print(__strings['help_start'])
    elif __command == 'execute':
        print(__strings['help_execute'])
    elif __command == 'move':
        print(__strings['help_move'])
    elif __command == 'type':
        print(__strings['help_type'])
    elif __command == 'cls':
        print(__strings['help_cls'])
    elif __command == 'systeminfo':
        print(__strings['help_systeminfo'])
    elif __command == 'title':
        print(__strings['help_title'])
    elif __command == 'prompt':
        print(__strings['help_prompt'])
    elif __command == 'regedit':
        print(__strings['help_regedit'])
    elif __command == 'color':
        print(__strings['help_color'])
    elif __command == 'sfc':
        print(__strings['help_sfc'])
    elif __command == 'tree':
        print(__strings['help_tree'])
    elif __command == 'nslookup':
        print(__strings['help_nslookup'])
    elif __command == 'tasklist':
        print(__strings['help_tasklist'])
    else:
        __print_error(__strings['this_command_does_not_exist_1'] + __command + 
                      __strings['this_command_does_not_exist_2'])


def __commands(__main: str, args: [str]):
    import os
    import platform
    if __main == 'cd':
        if len(args) == 0:
            __cd('')
        else:
            __args = ''
            for __i in range(len(args)):
                __args += args[__i]
                if __i != (len(args)-1):
                    __args += ' '
            __cd(__args)
    elif __main == 'mkdir':
        if len(args) == 0:
            __mkdir('')
        else:
            __args = ''
            for __i in range(len(args)):
                __args += args[__i]
                if __i != (len(args)-1):
                    __args += ' '
            __mkdir(__args)
    elif __main == 'rmdir':
        if len(args) == 0:
            __rmdir('')
        else:
            __args = ''
            for __i in range(len(args)):
                __args += args[__i]
                if __i != (len(args)-1):
                    __args += ' '
            __rmdir(__args)
    elif __main == 'delete':
        if len(args) == 0:
            __delete('')
        else:
            __args = ''
            for __i in range(len(args)):
                __args += args[__i]
                if __i != (len(args)-1):
                    __args += ' '
            __delete(__args)
    elif __main == 'dir':
        if len(args) == 0:
            __dir('')
        else:
            __args = ''
            for __i in range(len(args)):
                __args += args[__i]
                if __i != (len(args)-1):
                    __args += ' '
            __dir(__args)
    elif __main == 'help':
        if len(args) == 0:
            __help_commands('')
        else:
            __help_commands(args[0])
    elif __main == 'start':
        __command = ''
        for arg in args:
            __command += arg+' '
        __start(__command)
    elif __main == 'execute':
        __command = ''
        for arg in args:
            __command += arg + ' '
        __execute(__command)
    elif __main == 'move':
        __paths = ''
        for arg in args:
            __paths += arg + ' '
        __paths = __paths.split('"')
        while ' ' in __paths:
            __paths.remove(' ')
        __move(__paths)
    elif __main == 'type':
        if len(args) == 0:
            __type('')
        else:
            __args = ''
            for __i in range(len(args)):
                __args += args[__i]
                if __i != (len(args) - 1):
                    __args += ' '
            __type(__args)
    elif __main == 'cls':
        if len(args) != 0:
            if args[0] in ('/?', '-?', '-h', '-help', '/help', '/h'):
                __help_commands('cls')
                return
        __cls()
    elif __main == 'systeminfo':
        if len(__main) != 0:
            if args[0] in ('/?', '-?', '-h', '-help', '/help', '/h'):
                __help_commands('systeminfo')
                return
        __systeminfo()
    elif __main == 'title':
        if len(args) == 0:
            __title('')
        else:
            __title(args[0])
    elif __main == 'prompt':
        if len(args) == 0:
            __prompt('')
        else:
            __args = ''
            for __i in range(len(args)):
                __args += args[__i]
                if __i != (len(args) - 1):
                    __args += ' '
            __prompt(__args)
    elif __main == 'regedit':
        if len(args) != 0:
            if args[0] in ('/?', '-?', '-h', '-help', '/help', '/h'):
                __help_commands('regedit')
                return
        __regedit()
    elif __main == 'color':
        if len(args) == 0:
            __color('')
        else:
            _color = ''
            for __i in range(len(args)):
                _color += args[__i]
                if __i != (len(args) - 1):
                    _color += ' '
            __color(_color)
    elif __main == 'sfc':
        if len(args) == 0:
            __sfc('')
        else:
            __arg = ''
            for __i in range(len(args)):
                __arg += args[__i]
                if __i != (len(args) - 1):
                    __arg += ' '
            __sfc(__arg)
    elif __main == 'tree':
        if len(args) != 0:
            if args[0] in ('/?', '-?', '-h', '-help', '/help', '/h'):
                __help_commands('tree')
                return
        __tree()
    elif __main == 'ipconfig':
        if len(args) != 0:
            if args[0] in ('/?', '-?', '-h', '-help', '/help', '/h'):
                __help_commands('ipconfig')
                return
        __ipconfig(args)
    elif __main == 'control':
        if len(args) == 0:
            __sfc('')
        else:
            __arg = ''
            for __i in range(len(args)):
                __arg += args[__i]
                if __i != (len(args) - 1):
                    __arg += ' '
            __sfc(__arg)
    elif __main == 'nslookup':
        __args = ''
        if len(args) != 0:
            for __i in range(len(args)):
                __args += args[__i]
                if __i != (len(args) - 1):
                    __args += ' '
            if args[0] in ('/?', '-?', '-h', '-help', '/help', '/h'):
                __help_commands('nslookup')
                return
        __nslookup(__args)
    elif __main == 'tasklist':
        __args = ''
        if len(args) != 0:
            for __i in range(len(args)):
                __args += args[__i]
                if __i != (len(args) - 1):
                    __args += ' '
            if args[0] in ('/?', '-?', '-h', '-help', '/help', '/h'):
                __help_commands('tasklist')
                return
        __tasklist(__args)
    elif __main in __control_panel_commands:
        __args = ''
        for __i in range(len(args)):
            __args += args[__i]
            if __i != (len(args) - 1):
                __args += ' '
        if platform.system() == "Windows":
            os.system('control '+__main + ' ' + __args)
        elif platform.system() == "Linux":
            __print_error(__strings['this_command_is_not_available_for_linux'])
    elif (__main in __windows_tools) or (__main in __windows_utilies) or (__main in __other_windows_commands):
        __args = ''
        for __i in range(len(args)):
            __args += args[__i]
            if __i != (len(args) - 1):
                __args += ' '
        if platform.system() == "Windows":
            os.system(__main+' '+__args)
        elif platform.system() == "Linux":
            __print_error(__strings['this_command_is_not_available_for_linux'])
    elif __main in __files_in_directory:
        __command = __current_folder+'\\'+__main
        for arg in args:
            __command += ' '+arg
        os.system(__command)
    elif len(__main) == 2 and __main[1] == ':' and __main[0].lower() in 'abcdefghijklmnopqrstuvwxyz':
        __change_directory(__main.upper())
    else:
        __print_error(__strings['this_command_does_not_exist_1']+__main+__strings['this_command_does_not_exist_2'])


try:
    __infos = {}
    __strings = {}
    __current_folder = os.getcwd()
    print(__current_folder)
    __default_strings_file = os.path.dirname(__file__)+"\\fr_strings.xml"
    ___prompt = __current_folder
    __load_xml_file(__default_strings_file)
    __files_in_directory = __get_files_of_a_path(__current_folder)
    __folders_in_directory = __get_folders_of_a_path(__current_folder)
    __language = __infos['available_languages'][0]
    __load_language()
    __windows_tools = ['explorer', 'regedit', 'services.msc', 'taskmgr', 'msconfig', 'mstsc', 'logoff', 'shutdown',
                       'cmd', 'notepad', 'osk']
    __windows_utilies = ['calc', 'chkdsk', 'charmap', 'cleanmgr', 'comp', 'colorcpl', 'cttune', 'dxdiag', 'eudcedit',
                         'fonts', 'fsquirt', 'ftp', 'joy.cpl', 'label', 'magnify', 'mrt', 'msiexec', 'msinfo32',
                         'mspaint', 'narrator', 'powershell', 'shrpubw', 'sigverif', 'sndvol', 'snippingtool',
                         'utilman', 'verifier', 'wf.msc', 'wfs', 'wiaacmgr', 'winver', 'write', 'winword']
    __control_panel_commands = ['appwiz.cpl', 'control', '	access.cpl', 'hdwwiz.cpl', 'wuaucpl.cpl', 'fsquirt',
                                'timedate.cpl', 'directx.cpl', 'desk.cpl', 'inetcpl.cpl', 'jpicpl32.cpl', 'main.cpl',
                                'ncpa.cpl', 'netsetup.cpl', 'nvtuicpl.cpl', 'odbccp32.cpl', 'ac3filter.cpl',
                                'password.cpl', 'telephon.cpl', 'powercfg.cpl', 'intl.cpl', 'sticpl.cpl', 'wscui.cpl',
                                'mmsys.cpl', 'sysdm.cpl', 'nusrmgr.cpl', 'firewall.cpl', 'findfast.cpl']
    __other_windows_commands = ['dcomcnfg', 'certmgr.msc', 'compmgmt.msc', 'ddeshare', 'devmgmt.msc', 'dfrg.msc',
                                'diskmgmt.msc', 'diskpart', 'drwtsn32', 'eventvwr.msc', 'fonts', 'freecell',
                                'gpedit.msc', 'iexpress', 'ciadv.msc', 'secpol.msc', 'lusrmgr.msc', 'packager',
                                'perfmon', 'ntmsmgr.msc', 'ntmsoprq.msc', 'rsop.msc', 'fsmgmt.msc', 'cliconfg',
                                'msconfig', 'wmimgmt.msc']
    if __name__ == '__main__':
        __title('PyShell')
        __cls()
        print("PyShell [version 1.0.0]")
        while 1:
            try:
                print()
                print(___prompt+'>', end='')
                __command_to_execute = input().split()
                __params = []
                for i in range(1, len(__command_to_execute)):
                    __params.append(__command_to_execute[i])
                try:
                    __command_to_execute = str(__command_to_execute[0])
                except IndexError:
                    continue
                if __command_to_execute == 'exit':
                    exit(0)
                try:
                    __commands(__command_to_execute, __params)
                except ErrorInProgram as e:
                    print(e)
                except KeyboardInterrupt:
                    pass
                time.sleep(0.1)
            except KeyboardInterrupt:
                print()
except ErrorInProgram as e:
    print(e)
