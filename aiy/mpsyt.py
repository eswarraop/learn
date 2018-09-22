


import subprocess

import os
import code
import time


class player():

    def __init__(self):

        log_file = "mpsyt.log"
        self.log = open(log_file, 'w')
        err_file = "mpsyt.err"
        self.err = open(err_file, 'w')

        self.mpsyt = subprocess.Popen(["/usr/local/bin/mpsyt",""],stdin=subprocess.PIPE,
                                                                  stdout=self.log,
                                                                  stderr=self.err,
                                                                  shell=True)

        time.sleep(1)
        self.send_command('set playerargs --volume=30')

    
    def send_command( self, line):
        line = line + os.linesep
        self.mpsyt.stdin.write(bytes(line, 'utf-8'))
        self.mpsyt.stdin.flush()

        #code.interact( local  = locals() )

    def play_song(self, line):
        command = "/{0}".format( line ) 
        self.send_command(command)
        time.sleep(1)
        self.send_command("1")

    def play_list(self, line):
        command = "//{0}".format( line )
        self.send_command(command)
        time.sleep(1)
        self.send_command("1")
        time.sleep(1)
        self.send_command("1")


    def kill(self):
        self.mpsyt.kill()


    def stop(self):
        self.send_command("\n")


    def pause(self):
        self.send_command(" ")

    def set_volume(self, number):

        number = int(number)
        self.send_command("set playerargs --volume={0}".format( number ))

    def increase_volume(self ):
        self.send_command("9".format( number ))

    def decrease_volume(self ):
        self.send_command("0".format( number ))





if __name__ == '__main__':

    obj = player()
    obj.play_song("geeta govindam")

    code.interact( local = locals() )


