import subprocess
def run_in_terminal(cmd:str)->tuple:
    "a method that run cmd in terminal and returns the output"
    output=None
    error_occured=False
    try:
        lst=cmd.split(" ")
        output=subprocess.run(lst,capture_output=True,shell=True)
        if output and output.stderr.decode()!="": 
            error_occured=True
            raise Exception("")
        return (error_occured,output.stdout.decode())
    except Exception as e:
        if output:
            return (error_occured,output.stderr.decode())
        return (error_occured,None)

