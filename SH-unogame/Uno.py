import UnoGame as uno
from time import sleep
1
options = ['시작', '나가기']

while True:
    print(uno.thick_borders+"""\n\n|| ||   ||\ ||    // \\\\\n|| ||   ||\\\||   ((   ))\n\\\ //   || \||    \\\ //\n\n"""+uno.thin_borders+"\n")
    for i, option in enumerate(options):
        print(("{}| {}\n").format(i+1, option))
    print(uno.thick_borders)

    menu_choice = input("Select option: ").upper()
    if menu_choice == options[0] or menu_choice == '1':
        sleep(1)
        print("\n"+uno.thin_borders+"STARTING GAME"+uno.thin_borders)
        sleep(1)
        uno.Game().start_game()
    elif menu_choice == options[1] or menu_choice == '2':
        raise SystemExit