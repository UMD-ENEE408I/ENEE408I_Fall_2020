# Introduction

Your Jetson comes with OpenCV 4.1.1 pre-installed. However, if you need a newer version you can do so by building from source.

For now the easiest method is to install OpenCV from source using the official [OpenCV-Python in Ubuntu instructions](https://docs.opencv.org/master/d2/de6/tutorial_py_setup_in_ubuntu.html)
**Note:** Use `'make -j6` instead of `make` to speed up your build significantly by using parallel compilation.

## TODO
Update these instructions to build OpenCV CUDA acceleration functions for the Jetson Xavier's CUDA compute capability. Test ways to speed up build. See if anything from the old wiki [here](https://github.com/Pitt-RAS/iarc7_common/wiki/Installation-on-TX2#opencv) is still relevant
