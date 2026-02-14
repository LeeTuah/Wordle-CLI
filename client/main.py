import wordle
from common import clear, write, detect_keypress, flush_input
from colorama import Fore, Back, Style

def main():
    running = True
    while running:
        clear()
        write('', resetcursor=True)

        text = f"""



                          {Back.GREEN + Fore.BLACK}┌───┐┌───┐{Back.YELLOW}┌───┐┌───┐{Back.WHITE}┌───┐┌───┐{Style.RESET_ALL}
                          {Back.GREEN + Fore.BLACK}| W || O |{Back.YELLOW}| R || D |{Back.WHITE}| L || E |{Style.RESET_ALL}
                          {Back.GREEN + Fore.BLACK}└───┘└───┘{Back.YELLOW}└───┘└───┘{Back.WHITE}└───┘└───┘{Style.RESET_ALL}

                          

1. Singleplayer
2. Multiplayer
3. Controls
4. Instructions
5. Exit
>> 
"""
        write(text)
        key = detect_keypress()

        match key:
            case '\'1\'':
                clear()
                w = wordle.Wordle()
                w.run()

            case '\'2\'':
                pass

            case '\'3\'':
                pass

            case '\'4\'':
                pass

            case '\'5\'':
                running = False

    flush_input()

main()