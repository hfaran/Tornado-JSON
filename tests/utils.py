from traceback import print_exc


def handle_import_error(err):
    print_exc()
    print("Please run `py.test` from the root project directory")
    exit(1)
