import os


def create_directory(directory_name):
    if not os.path.exists(directory_name):
        os.mkdir(directory_name)
        print(f"'{directory_name}' created")
    else:
        print(f"'{directory_name}' already exists")


current_directory = os.path.dirname(os.path.abspath(__file__))
create_directory(os.path.join(current_directory, "../test"))
