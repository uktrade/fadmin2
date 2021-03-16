from core.utils.command_helpers import (
    CheckUserCommand,
)



class Command(CheckUserCommand):
    help = "test the way it works"
    command_name  = __name__

    def add_arguments(self, parser):
        parser.add_argument("period", type=int)


    def handle_user(self, *args, **options):
            print(f"Hello, My name is: {__name__}")
