from windows.main.main_window import MainWindow

if __name__ == "__main__":
    window = MainWindow()

    try:
        window.mainloop()
    except KeyboardInterrupt:
        window.destroy()
