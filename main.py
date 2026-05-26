import updater

VERSION = "1.1.0"

def main():
    print(f"Verificando atualizações...")
    updater.check_and_update(VERSION)

    print(f"============================")
    print(f"  teste_autoupdate v{VERSION}")
    print(f"============================")

if __name__ == "__main__":
    main()