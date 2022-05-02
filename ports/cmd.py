import argparse
from controller.highlight_controller import HighlightController

def start():
    msg = "Sync highlights from kindle to a json file and get random quotes"
    
    # Initialize parser
    parser = argparse.ArgumentParser(description = msg) 

    # Adding optional argument
    parser.add_argument("-e", "--email", help = "email to connect to kindle")
    parser.add_argument("-p", "--password", help = "password to connect to kindle")
    parser.add_argument("-u", "--username", help = "unique name to distinguish one user from the other")
    parser.add_argument("-s", "--sync", help = "set to True if want to synchronize")
    parser.add_argument("-g", "--get", help = "get random highlights")
    
    # Read arguments from command line
    args = parser.parse_args()
    if args.sync:
        email = args.email
        password = args.password
        username = args.username

        controller = HighlightController(is_local=True)
        controller.sync_highlights(email, password, username)