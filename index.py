import os
from app import start

def main():
    while True:
        try:
            start()   
        except Exception as e:
            print(e)
        print('> Waiting 5 minutes')
        os.system('sleep 300')


if __name__ == "__main__":
    print('> Start loop!')
    main()
