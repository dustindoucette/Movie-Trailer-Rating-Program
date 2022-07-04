import sys, os

os.system('ffmpeg -i ./Movie-Trailers/' + sys.argv[1] +'.avi -r 2 -start_number 0 ./Movie-Trailers/' + sys.argv[1] + '/image%01d.jpg -hide_banner -loglevel error')