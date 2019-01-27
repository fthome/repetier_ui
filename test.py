import sys
import getopt
try:
    opts, args = getopt.getopt(sys.argv[1:],"h:p:t:m:",["host=","port=","topic=","message="])
    print(opts)
    print(args)
except getopt.GetoptError:
    print"Error... usage"
