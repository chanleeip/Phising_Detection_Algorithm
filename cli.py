import main
import typer
import os
app=typer.Typer()

@app.command(help="This cli is used for analyzing batch of emails/email.")
def run_file(path:str='',dir:bool=False,file:bool=False):
    if path:
        print(main.run_script(path))
    if dir:
        if os.path.isdir(path):
            print("Sucess, analyzing")
        else:
            print("not a directory")

    if file:
        if os.path.exists(path):
            print("Sucess, analyzing")
        else:
            print("not a file")


if __name__ == "__main__":
    app()



