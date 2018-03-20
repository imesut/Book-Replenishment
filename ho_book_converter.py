import ftplib
import os

from secrets import ftp_host, user, password, linklist, urlDomain

list = open(linklist, "r")

liste = []

for i in list.readlines():
    liste.append(i)

localFolder = os.getcwd() + "/"

ftp = ftplib.FTP(ftp_host)
ftp.login(user, password)

exts = ["wav", "mp3"]

queTotal = 0
for i in liste:
    if i.find(" is a broken link") > 0:
        queTotal += 1

print("There is " + str(queTotal) + " broken files")
queItem = 1

for link in liste:
    if link.find(" is a broken link") > 0:
        url = link.split(" ")[0]
        path = "/hayalortagim/" + url.replace(urlDomain, "")
        fileName = path.split("/")[-1]
        path = path.replace(fileName, "")
        fileNameParts = fileName.split(".")
        convertedFileName = fileName
        fileName = fileNameParts[0] + "." + exts[1 - exts.index(fileNameParts[-1])]
        ftp.cwd(path)
        print(str(queItem) + "/" + str(queTotal) + " file (" + fileName + ") is downloading")
        downloadingFile = open(fileName, mode="wb")
        ftp.retrbinary("RETR " + fileName, downloadingFile.write)
        downloadingFile.close()
        print(str(queItem) + "/" + str(queTotal) + " file (" + fileName + ") is converting")
        os.system("ffmpeg -i " + localFolder + fileName + " " + localFolder + convertedFileName)
        print(str(queItem) + "/" + str(queTotal) + " file (" + convertedFileName + ") is uploading")
        fileToUpload = open(convertedFileName, mode="rb")
        ftp.storbinary("STOR " + convertedFileName, fileToUpload)
        fileToUpload.close()
        print(str(queItem) + "/" + str(queTotal) + " file (" + convertedFileName + ") is uploaded")
        print(str(float(queItem/queTotal)) + "is done...")

list.close()
ftp.quit()
