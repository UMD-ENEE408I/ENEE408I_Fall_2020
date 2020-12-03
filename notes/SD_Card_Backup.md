# Introduction

The Windows program "ImageUSB" allows making up a raw (byte for byte) copy of the micro-SD card used in the Jetson Xavier NX's. If your SD card becomes corrupted, or your Jetson cannot boot for whatever reason, you can restore a previous image made onto your SD card and everything will be back to the way it was.

This is non-trivial on Windows because of the numerous partitions created on Jetson SD cards and the way Windows handles low-level access to drives. This can cause the typically recommended tools to not work.

Since the classes SD Cards are 32GB's, this will make a 32GB file on your computer that is the byte-for-byte backup of the SD card (e.g. make sure you have enough space).

Link to Software: https://www.techspot.com/downloads/7113-imageusb.html (Links to an external site.)

# Usage

Run the program and set the checkboxes for your use case. You likely do not need to check "Post Image Verification", this will make the process take longer.

# Testing

I tested this program using the images for my Jetson Nano (both backup and restore), due to the low level nature of the tool, and the non-dependence on drive letters, I expect it to work for everyone.

# Other programs I tried

Many traditional Windows tools that claim to work for this purpose will not due to the partitioning scheme used for the Xavier NX's. In particular I tried:

* Win32DiskImager (this is a famous program, while this worked for me, however it needs a drive letter that represents the entire drive regardless of partitioning, this was not assignable for at least one student)
* Rufus (no save icon, despite obviously working for other people on the internet)
* EaseUS Backup (could back up but not restore due to partition errors)
* Balena Etcher (what NVIDIA recommends for writing, does not support image backups)
