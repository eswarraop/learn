


import subprocess
import os


class mpsyt_runner( ):

    def __init__(self):
        self.mpsyt = subprocess.Popen(["/usr/local/bin/mpsyt",""],stdin=subprocess.PIPE,
                                                                  stdout=subprocess.PIPE,
                                                                  shell=True)
        self.mpsyt.stdin.write(bytes('set playerargs --volume=30\n', 'utf-8'))
        self.mpsyt.stdin.flush()

    
    def send_command( self, line):
        self.mpsyt.stdin.write(bytes(line, 'utf-8'))
        self.mpsyt.stdin.flush()

        #code.interact( local  = locals() )


    def kill(self):
        self.mpsyt.kill()


    def stop(self):
        self.send_command("\n")


    def pause(self):
        self.send_command(" ")

    def set_volume(self, number):

        number = int(number)
        self.send_command("set playerargs --volume={0}".format( number ))




if __name__ == '__main__':

    obj = mpsyt_runner()

