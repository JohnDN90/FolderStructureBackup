"""
FolderStructureBackup create a backup of a directory's folder structure.

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
"""


__author__ = "David John Neiferd"
__copyright__ = "Copyright (C) 2019 David John Neiferd"
__version__ = "0.1"
__license__ = "GNU GPL v3"
__license_folderStructureBackup__ = ("----------------------------------------------------------\n"
"FolderStructureBackup create a backup of a directory's folder structure.\n"
"\n"
"Copyright (C) 2019  David John Neiferd\n"
"\n"
"This program is free software: you can redistribute it and/or modify\n"
"it under the terms of the GNU General Public License as published by\n"
"the Free Software Foundation, either version 3 of the License, or\n"
"(at your option) any later version.\n"
"\n"
"This program is distributed in the hope that it will be useful,\n"
"but WITHOUT ANY WARRANTY; without even the implied warranty of\n"
"MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n"
"GNU General Public License for more details.\n"
"\n"
"You should have received a copy of the GNU General Public License\n"
"along with this program.  If not, see <https://www.gnu.org/licenses/>.\n"
"----------------------------------------------------------\n")

__license_xxHash__ = ("----------------------------------------------------------\n"
'\nxxHash Library\n'
'Copyright (c) 2012-2014, Yann Collet\n'
'All rights reserved.\n'
'\n'
'Redistribution and use in source and binary forms, with or without modification,\n'
'are permitted provided that the following conditions are met:\n'
'\n'
'* Redistributions of source code must retain the above copyright notice, this\n'
'  list of conditions and the following disclaimer.\n'
'\n'
'* Redistributions in binary form must reproduce the above copyright notice, this\n'
'  list of conditions and the following disclaimer in the documentation and/or\n'
'  other materials provided with the distribution.\n'
'\n'
'THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND\n'
'ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED\n'
'WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE\n'
'DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR\n'
'ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES\n'
'(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;\n'
'LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON\n'
'ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT\n'
'(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS\n'
'SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n'
"----------------------------------------------------------\n\n")

print(__license_xxHash__)
print(__license_folderStructureBackup__)

import os
import zipfile
import datetime
import time
import sys
import psutil
from subprocess import check_output, Popen, PIPE


def getVolumeInfo(path):
    val = check_output(['df', '-h', path]).split("\n")[1].split(" ")
    val = [v for v in val if v != '']
    filesystem = val[0]
    fstype = val[1]
    fssize = val[2]
    fsused = val[3]
    fsavail = val[4]
    fsmount = val[6]

    cmd1 = ['system_profiler', 'SPSerialATADataType']\

    cmd2 = ['grep',
           '"BSD Name: %s"' % (filesystem.split("/")[-1]), '-B26', '-A3']

    ps = Popen(cmd1, stdout=PIPE)
    val = check_output(cmd2, stdin=ps.stdout).split("\n")
    ps.wait()

    val = [v.strip() for v in val]
    val = [v for v in val if v != '']

    hddserial = [v.split(':')[-1] for v in val if "Serial Number:" in v][0]
    # fstype2 = [v.split(':')[-1] for v in val if "ID_FS_TYPE=" in v][0]
    # fsuuid = [v.split(':')[-1] for v in val if "ID_FS_UUID=" in v][0]

    raise NotImplementedError("Not yet finished.")


    # try:
    #     fslabel = [v.split('=')[-1] for v in val if "ID_FS_LABEL=" in v][0]
    # except:
    #     fslabel = "N/A"
    # return fslabel, fstype, fssize, fsused, fsavail, fsmount, hddserial, fstype2, fsuuid, val


# Specify the path of the backup and the rootPath of the folder structure that will be backed up
if len(sys.argv)==1:
    rootPath = raw_input("Specify the path to be backed up:  ")
    backupPath = raw_input("Specify location to create the backup: ")
    hashType = raw_input("Specifiy the hash type (leave blank for None):  ") or None
    if hashType is None:
        storeHash = False
    else:
        storeHash = True
else:
    rootPath = sys.argv[1]
    backupPath = sys.argv[2]
    if len(sys.argv)>3:
        hashType = sys.argv[3]
        storeHash = True
    else:
        hashType = None
        storeHash = False

if not backupPath.endswith("/"):
    backupPath = backupPath + "/"

if not rootPath.endswith("/"):
    rootPath = rootPath + "/"

# Get the current date and time
currentDT = datetime.datetime.now()
strDT = currentDT.strftime("%Y%m%d_%H%M%S")

# Create a backup file with current date and time in it
outputPath = backupPath + "folderStructureBackup_" + strDT + ".txt"

print("\nSummary\n----------\nBacking Up: %s\nTo: %s\nHash Type: %s\n------------------------------------"%(rootPath, outputPath[:-4]+".zip", hashType))
ans = raw_input("Ensure above information is correct. Start backup? (yes/no):  \n\n")

if ans.lower() != "yes":
    raise RuntimeError("User canceled operation.")

if hashType is None:
    pass
elif hashType.lower() == "xxhash":
    import xxhash
elif hashType.lower() == "crc32":
    import zlib
elif hashType.lower() == "md5":
    import hashlib
else:
    raise ValueError("Uknonwn hash type, %s, specified by user."%hashType)

# Credit: quantumSoup and awiebe on Stackoverflow.com
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def crc32(fname):
    with open(fname, "rb") as f:
        value = 0
        for chunk in iter(lambda: f.read(4096), b""):
            value = zlib.crc32(chunk, value) & 0xfffffff
    return value


def xxHash(fname):
    # pip install xxhash if necessary
    hash_xxhash = xxhash.xxh64()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_xxhash.update(chunk)
    return hash_xxhash.hexdigest()

if hashType is None:
    pass
elif hashType.lower() == "xxhash":
    getHash = xxHash
elif hashType.lower() == "crc32":
    getHash = crc32
elif hashType.lower() == "md5":
    getHash = md5

# obj_Disk = psutil.disk_usage(rootPath)
# totalSize = float(obj_Disk.used)
totalSize = float(check_output(['du', '-s', rootPath]).split("\t")[0])*1000.0

start = time.time()
sumSize = 0
# Windows Code
if (os.name == "posix") and (storeHash):
    with open(outputPath, 'w') as f:
        # Walk through all the directories and files in the rootPath specified above and write them to the backup file
        f.write("#%s\n" % (rootPath))
        f.write("#OS: %s\n" % (os.name))
        f.write("#Date: %s\n"%(currentDT.strftime("%Y%m%d")))
        f.write("#Time: %s\n"%(currentDT.strftime("%H%M%S")))
        fslabel, fstype, fssize, fsused, fsavail, fsmount, hddserial, fstype2, fsuuid, val = getVolumeInfo(rootPath)
        f.write("#Volume Name: %s\n" % (fslabel))
        f.write("#Volume Serial No.: %s\n" % (hddserial))
        f.write("#Volume UUID: %s\n"%(fsuuid))
        f.write("#File System Type: %s, %s\n" % (fstype, fstype2))
        f.write("#Extra HDD Info Below\n")
        for v in val:   f.write("#%s\n"%v)
        f.write("#File List Format: file_path, file_size, file_mtime, %s_hash\n" % (hashType))
        for root, dirs, files in os.walk(rootPath, topdown=True):
            f.write("#Files\n")
            for name in files:
                val = os.path.join(root, name)
                try:
                    size = os.path.getsize(val)
                except:
                    size = "N/A"
                try:
                    mtime = time.strftime('%Y%m%d_%H%M%S', time.gmtime(os.path.getmtime(val)))
                except:
                    size = 0
                try:
                    md5hash = getHash(val)
                except:
                    md5hash = "N/A"
                f.write("%s, %s, %s, %s\n" % (val, size, mtime, md5hash))
                sumSize += size
                duration = time.time() - start
                avgSpeed = (sumSize/duration)/1000000.0
                progress = sumSize / float(totalSize) * 100.0
                print("Progress: %.2f%%  Average Speed: %.3f MB/s"%(progress, avgSpeed))

            for name in dirs:
                val = os.path.join(root, name)
                f.write("%s\n" % (val))

elif (os.name == "posix") and not (storeHash):
    with open(outputPath, 'w') as f:
        # Walk through all the directories and files in the rootPath specified above and write them to the backup file
        f.write("#%s\n" % (rootPath))
        f.write("#OS: %s\n" % (os.name))
        f.write("#Date: %s\n" % (currentDT.strftime("%Y%m%d")))
        f.write("#Time: %s\n" % (currentDT.strftime("%H%M%S")))
        fslabel, fstype, fssize, fsused, fsavail, fsmount, hddserial, fstype2, fsuuid, val = getVolumeInfo(rootPath)
        f.write("#Volume Name: %s\n" % (fslabel))
        f.write("#Volume Serial No.: %s\n" % (hddserial))
        f.write("#Volume UUID: %s\n" % (fsuuid))
        f.write("#File System Type: %s, %s\n" % (fstype, fstype2))
        f.write("#Extra HDD Info Below\n")
        for v in val:   f.write("#%s\n" % v)
        f.write("#File List Format: file_path, file_size, file_mtime\n")
        for root, dirs, files in os.walk(rootPath, topdown=True):
            f.write("#Files\n")
            for name in files:
                val = os.path.join(root, name)
                try:
                    size = os.path.getsize(val)
                except:
                    size = 0
                try:
                    mtime = time.strftime('%Y%m%d_%H%M%S', time.gmtime(os.path.getmtime(val)))
                except:
                    mtime = "N/A"
                f.write("%s, %s, %s\n" % (val, size, mtime))
                sumSize += size
                duration = time.time() - start
                avgSpeed = (sumSize / duration) / 1000000.0
                progress = sumSize / float(totalSize) * 100.0
                print("Progress: %.2f%%  Average Speed: %.3f MB/s" % (progress, avgSpeed))
            f.write("#Directories\n")
            for name in dirs:
                val = os.path.join(root, name)
                f.write("%s\n" % (val))
else:
    raise NotImplementedError("Code for operating system of type %s is not implemented."%(os.name))

end = time.time()
print("\nTook %.3f seconds.\n"%(end-start))

# Compress the backup file to save space
zipped = zipfile.ZipFile(outputPath[:-4]+".zip", 'w')
zipped.write(outputPath, compress_type=zipfile.ZIP_DEFLATED)
zipped.close()

# Remove the original uncompressed backup file
os.remove(outputPath)


time.sleep(5)