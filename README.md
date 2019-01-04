# FolderStructureBackup
A program to backup folder structure information and file information (size, mtime, checksum) which can be useful in restoring folder structure after recovering deleted files.

Copyright (C) 2019  David John Neiferd

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Other Software
--------------
Uses Python modules: os, zipfile, datetime, time, sys, psutil, win32api, xxhash, zlib, hashlib.

Uses xxHash via the xxhash 1.3.0 pypi package. See LICNESE_xxHash for the Copyright and License of xxHash.


Intended Usage
--------------
The program creates a text file which stores the full path of all files in a specified directory and all of its subdirectories. For each of these files, it stores the fize size, modification time, and optionally a file checksum.  It also stores the full path of all subdirectories in a specified directory. The text file is then compressed (.zip) to save space.

This information can be useful in situations when recovering deleted files. For example, Recuva and PhotoRec will recovery many files but does not recover the folder structure.  The information backed up with this program can be used to help sort the recovered files back into their original folder structures.

NEVER SAVE THE BACKUP TO THE SAME LOCATION THAT YOU ARE BACKING UP!
If you are backing up your C: drive's folder structure, do not store the backup.zip file to the C: drive. Otherwise if the C: drive becomes corrupted, you will lose your backup.zip file.


Instructions
------------
1) Double click folderStructureBackup.exe to run it
2) Enter the path you want to backup
3) Enter the path where you want to create the backup file
4) Specify the hash type for file checksums: md5, crc32, xxhash, or leave blank for None
5) Read the summary, ensure the information is correct, type yes to start backup or no to cancel