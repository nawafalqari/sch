class Commands:
    def __init__(self):
        self.commands: dict[str, Command] = {}
    
    def register(self, command: "Command"):
        self.commands[command.name] = command

    def list_commands(self) -> list["Command"]:
        return list(self.commands.values())

    def find_command(self, content: str) -> "Command":
        name = content.strip().lower().split(" ")[0]

        for command in self.list_commands():
            if command.name == name or name in command.aliases:
                return command

class Command:
    def __init__(self, name: str, aliases: list[str], callback):
        self.name = name
        self.aliases = aliases
        self.callback = callback

def command(name: str, aliases: list[str] = []):
    def decorator(callback):
        cmd = Command(name, aliases, callback)
        commands.register(cmd)

        return callback
    
    return decorator

commands = Commands()