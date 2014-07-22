from ctypes import cdll, c_char_p, c_int, byref, pointer
import sys

print sys.argv

lib = cdll.LoadLibrary('libshairport.so')
argc = c_int(len(sys.argv))
argv = (c_char_p * len(sys.argv))(*sys.argv)

lib.shairport_main(argc, argv)
lib.shairport_loop()
