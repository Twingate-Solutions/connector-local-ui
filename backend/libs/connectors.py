import sys,os,re
import io
import shutil
import subprocess
from subprocess import check_output

sys.path.insert(1, './libs')
sys.path.insert(1, '../resources')
import errors

dirname = os.path.dirname(__file__)
INSTALL_STUB = os.path.join(dirname, '../resources/stub_install_script.sh')
INSTALL_INSTANCE = os.path.join(dirname, '../resources/install_connector.sh')


def check_for_running_connector():
    status = os.system('systemctl is-active twingate-connector')
    print(status)
    if status == 0:
        return True
    else:
        return False

def provision_install_script(accessToken,refreshToken,tenant):
    shutil.copyfile(INSTALL_STUB, INSTALL_INSTANCE)
    # Read in the file
    with open(INSTALL_STUB, 'r') as file :
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace('<ACCESSTOKEN>', accessToken).replace('<REFRESHTOKEN>',refreshToken).replace('<TENANT>',tenant)

    # Write the file out again
    with open(INSTALL_INSTANCE, 'w') as file:
        file.write(filedata)
    return True
    
def run_install_script(filepath):
    try:
        output = check_output(["sudo","sh",filepath], text=True)
        #print(output)
        return False,output
    except subprocess.CalledProcessError as e:
        return True,errors.rconnector_install_error(e.returncode)

def delete_install_script():
    os.remove(INSTALL_INSTANCE)
    return True

def install_connector():
    hasError,res = run_install_script(INSTALL_INSTANCE)
    return hasError,res
