import os
import shutil
import logging

# Constants
EV_DIR = 'ev'
CURR_PUSH_PATH = f'{EV_DIR}/.curr_push'
CARRIED_OVER_PATH = f'{EV_DIR}/.carried_over'
CARRIED_OVER_FILE = f'{EV_DIR}/.carried_over.txt'

logging.basicConfig(level=logging.INFO)

def push(tag):
    # Create new push with tag
    if not os.path.exists(EV_DIR):
        os.makedirs(EV_DIR)
    if not os.path.exists(CARRIED_OVER_PATH):
        shutil.copytree(f'{EV_DIR}/', CARRIED_OVER_PATH)
    if os.path.exists(CARRIED_OVER_FILE):
        with open(CARRIED_OVER_FILE, 'r') as f:
            carried_over_content = f.read()
            logging.info('Carrying over from previous push: %s', carried_over_content)

    # Create new push
    push_dir = f'{EV_DIR}/{tag}'
    if not os.path.exists(push_dir):
        os.makedirs(push_dir)
    with open(f'{push_dir}/.first', 'w') as f:
        f.write('true')
    
    # Update .ev and CARRIED_OVER_PATH files
    if len(sys.argv) > 2:
        new_tag = sys.argv[1]
    else:
        new_tag = tag
    with open(f'{push_dir}/.ev', 'w') as f:
        f.write(new_tag)
    shutil.move(CARRIED_OVER_PATH, push_dir)

def pull(tag):
    # Reroll to specific push
    if not os.path.exists(EV_DIR):
        os.makedirs(EV_DIR)
    with open(f'{EV_DIR}/.ev', 'r') as f:
        current_push = f.read()
    if len(sys.argv) > 2:
        new_tag = sys.argv[1]
    else:
        new_tag = tag
    shutil.move(f'{EV_DIR}/{new_tag}', EV_DIR)
    
    # Update CARRIED_OVER_PATH file
    with open(CARRIED_OVER_PATH, 'w') as f:
        with open(f'{EV_DIR}/.carried_over', 'r') as g:
            carried_over_content = g.read()
            if not os.path.exists(f'{EV_DIR}/.first'):
                f.write('false')
    
    # Update .ev file
    with open(CARRIED_OVER_PATH, 'a') as f:
        f.write('\n' + new_tag)
        
def status():
    # Show push user is on atm
    if not os.path.exists(EV_DIR):
        logging.info('No pushes found!')
    else:
        with open(f'{EV_DIR}/.ev', 'r') as f:
            current_push = f.read()
        logging.info('You are currently on push %s', current_push)

def list_pushes():
    # List all pushes
    if not os.path.exists(EV_DIR):
        logging.info('No pushes found!')
    else:
        pushes_dir = EV_DIR
        for dir_name in os.listdir(pushes_dir):
            if os.path.isfile(f'{pushes_dir}/{dir_name}'):
                continue
            push_file = f'{pushes_dir}/{dir_name}/.ev'
            if not os.path.exists(push_file):
                continue
            with open(push_file, 'r') as f:
                tag = f.read()
                logging.info('%s', tag)

def latest():
    # Pull the latest push
    if not os.path.exists(EV_DIR):
        logging.info('No pushes found!')
    else:
        pushes_dir = EV_DIR
        for dir_name in os.listdir(pushes_dir):
            if not os.path.isdir(f'{pushes_dir}/{dir_name}'):
                continue
            push_file = f'{pushes_dir}/{dir_name}/.ev'
            if os.path.exists(push_file):
                with open(push_file, 'r') as f:
                    tag = f.read()
                    logging.info('Tag: %s', tag)

def main():
    if len(sys.argv) > 1 and sys.argv[1] in ['push', 'pull']:
        action = sys.argv[1]
        if action == 'push':
            push(sys.argv[2])
        else:
            pull(sys.argv[2])
    else:
        status()

if __name__ == '__main__':
    main()