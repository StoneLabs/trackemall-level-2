# Clear frames bucket
import subprocess
for _id in range(0, 1000):
    cmd = ['wget', "127.0.0.1:2438/getFrame?id=" + str(_id), "-O", "/tmp/next_frame.dat", "wb+"]
    prc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, input="")