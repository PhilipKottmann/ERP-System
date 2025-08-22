from .controller.controller import Controller

def main():
    app = Controller()
    app.view.mainloop()

if __name__ == "__main__":
    main()