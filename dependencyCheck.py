from importlib.util import find_spec
import os

def depCheck(file: str, debug=False, promptBeforeInstall=True, consoleMessage="Some modules are missing. Do you want to install them? [Y/n]: "):
    """
    depCheck() should be called before your imports, so that it can install if they are not present at runtime

    'file' should be the path to the file that you want to check
    dependencies\n
    'debug' prints extra messages to the console
    """
    if file is None:
        raise Exception("File not defined")
        
    if not os.path.exists(file):
        raise Exception(f"'{file}' not found") 

    print(file)
    missingPackages = []

    with open(file, 'r') as f:
        lines = f.readlines()

        for line in lines:
            line:str
            line.strip()
            if line.startswith('from') or line.startswith('import'):
                line = line.split(' ')
                pkg = line[1]
                pkg = pkg.replace('\n', '')
                pkg:str
                if pkg.find('.') != -1:
                    pkg = pkg.split('.')
                    spec = find_spec(pkg[0])
                    if spec is None:
                        missingPackages.append(pkg[0])
                else:
                    spec = find_spec(pkg)
                    if spec is None:
                        missingPackages.append(pkg)
                
    if os.name=="posix":
        inst="sudo pip install {}"
    elif os.name == "nt":
        inst = "pip install {}"
    else:
        raise Exception("OS not recognized")
    
    res = None
    if len(missingPackages)!=0:
        res = input(consoleMessage)
        if res.lower() != 'y':
            return
    
    for package in missingPackages:
        if debug:
            print("Installing {}".format(package))
        os.system(inst.format(package))