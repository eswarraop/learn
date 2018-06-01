
import subprocess
import code


track = 'ninnu kori audio jukebox'

p = subprocess.Popen(["/usr/local/bin/mpsyt",""],stdin=subprocess.PIPE,stdout=subprocess.PIPE)

#code.interact( local = locals() )

p.stdin.write(bytes('/' + track + '\n1\n', 'utf-8'))
p.stdin.flush()

value = input("Press a key\n")

pkill = subprocess.Popen(["/usr/bin/pkill","omxplayer"],stdin=subprocess.PIPE)
p.kill()



