import subprocess
from opp.models import Command
from opp.repository import CommandRepository

class CommandService:
    def __init__(self):
        self.repo = CommandRepository()

    def register(self, alias: str, name: str, path: str):
        if not alias or not name or not path:
            raise ValueError("Alias, name, and path must be provided.")

        cmd = Command(id=None, alias=alias, name=name, path=path)
        cmd_id = self.repo.add_command(cmd)
        return cmd_id
    
    def find(self, alias: str) -> Command | None:
        return self.repo.get_by_alias(alias)
    
    def list(self):
        commands = self.repo.get_all()
        return commands
    
    def find_by_id(self, id: int) -> Command | None:
        return self.repo.get_by_id(id)
        
    
    def remove(self, alias: str) -> bool:
        return self.repo.delete_by_alias(alias)
    
    def update(self, alias: str, name: str, path: str) -> bool:
        command = self.find(alias)
        if command:
            command.name = name
            command.path = path
            return self.repo.update_command(command)
        return False
    
    def execute(self, alias: str) -> bool:
        command = self.find(alias)
        if not command:
            return False

        try:
            subprocess.Popen(command.path, shell=True)
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to execute '{alias}': {e}")

        