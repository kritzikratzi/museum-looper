import inotify.adapters
import os
import time
import shutil
import subprocess
import configparser

config_parser = configparser.ConfigParser()
config_parser.read("/boot/looper.txt")
config = config_parser['DEFAULT']
ip = config['ip']
fullscreen = config['fullscreen']=='true'
master = config['master']=='true'

print("Config: ")
print("  ip:         " + ip)
print("  fullscreen: " + str(fullscreen))
print("  master:     " + str(master))
print("")
print("Starting in 10 seconds...")
time.sleep(10)

def copy_from(dir):
	found=False
	for file in os.listdir(dir):
		print("found " + file)
		if (file.endswith(".mp4") or file.endswith(".MP4")) and not file.startswith("."):
			print("    copy " + file + "/home/pi/Videos/main_video.mp4")
			#shutil.copyfile(dir+"/"+file, "/home/pi/Videos/main_video.mp4")
			subprocess.run(["rsync", "--size-only", "--progress", dir+"/"+file,"/home/pi/Videos/main_video.mp4"])
			print("    copy complete!")
			found=True
			break
		else:
			print("    ignore")
	if not found:
		print("no mp4 file found :(")
	os.system('drive="$(findmnt -n -M "' + dir + '" -o SOURCE)"; udisksctl unmount -b "$drive"; udisksctl power-off -b "$drive";')
	time.sleep(2)
	os.system("xdotool mousemove 320 300")
	os.system("xdotool click 1")
	time.sleep(2)


def start_video():
	kill_video()

	if fullscreen:
		os.system("blocker/blocker &")
	time.sleep(2)
	#os.system("mplayer -framedrop -vo gl:swapinterval=1 -autosync 0 -lavdopts threads=4:skiploopfilter=all -loop 0 -pp 0 -xineramascreen -2 -geometry 3840x1080+0+0 /home/pi/Videos/main_video.mp4 &")
	cmd = "sudo ./omxplayer-sync/omxplayer-sync -o alsa"
	if master:
		cmd = cmd + " -muv"
	else:
		cmd = cmd + " -luv"
	cmd = cmd + " --tiny /home/pi/Videos/main_video.mp4 &"
	print("running " + cmd)
	os.system(cmd)
	#os.system("mplayer -framedrop -pp 0 -loop 0 -xineramascreen -2 -geometry 3840x1080+0+0 /home/pi/Videos/main_video.mp4 &")
	time.sleep(1)
	os.system("xdotool mousemove 220 200")
	os.system("xdotool click 1")
	os.system("unclutter -idle 0.01 -root &")




def kill_video():
	#os.system("killall -9 play_video.sh")
	os.system("killall -9 blocker 2>/dev/null")
	os.system("killall -9 mplayer 2>/dev/null")
	os.system("sudo killall -9 omxplayer 2>/dev/null")
	os.system("sudo killall -9 omxplayer-sync 2>/dev/null")
	os.system("sudo killall -9 omxplayer.bin 2>/dev/null")
	os.system("killall unclutter 2>/dev/null")

print("update network config")
os.system("sudo ifconfig eth0 " + ip + " netmask 255.255.255.0 up")

print("Checking already mounted volumes...")
for file in os.listdir("/media/pi"):
	if os.path.isdir("/media/pi/" + file):
		copy_from("/media/pi/" + file)
		break;


start_video()

i = inotify.adapters.Inotify()
i.add_watch("/media/pi")

for event in i.event_gen(yield_nones=False):
	(_,type_names,path,filename)=event
	print("PATH={} filename={} types={}".format(path,filename,type_names))

	if 'IN_CREATE' in type_names and 'IN_ISDIR' in type_names:
		kill_video()
		time.sleep(2)
		print("copy from {}/{}".format(path,filename))
		copy_from(path + "/" + filename)
		time.sleep(2)
		start_video()
		time.sleep(2)

