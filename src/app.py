import ai.mikamakilite as mkl
import telethon as tl


def main():
    mkl.client.start()
    mkl.client.run_until_disconnected()

if __name__ == "__main__":
    main()