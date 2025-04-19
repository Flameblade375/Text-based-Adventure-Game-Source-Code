from . import utils as u

global commands

def show_commands(commands_to_show=0):
    global commands
    try:
        if type(commands_to_show) == list:
            commands_to_show = commands_to_show[0]
        if type(commands_to_show) == str:
            commands_to_show = int(commands_to_show)
    except ValueError:
        print('invalid number of commands to show!')
        commands_to_show = 0
    # Print a list of the commands
    print(
        """
        Commands:
        """
    )
    if commands_to_show == 0:
        commands_to_show = len(commands)
    shown_commands = 0
    for key, value in commands.items():
        print(f'        {key} - {value["description"]} - {value["args"]}')
        shown_commands += 1
        if shown_commands >= commands_to_show:
            return


# A function to split an innput str into a list, with the first entry being
# the command, which may be multiple words
def parse_command(command: str) -> list:
    global commands
    for key in commands.keys():
        u.DEBUG('Checking command "' + command + '" with key "' + key + '"')
        if command.startswith(key):
            if len(command) == len(key):
                return [key.strip()]
            return [key.strip()] + command[len(key):].strip().split()
    return False

