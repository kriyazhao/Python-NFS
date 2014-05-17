set file1=testData1.txt
set file2=testData2.txt
set md5=735779d21596c407963518e17c35d65c
set sha1=4b661664f2cbdae20550b54f780f990606b48651

python getInfo.py --host 198.46.132.117  --port 8080 validateFiles
python putfile.py --host 198.46.132.117 --port 8080 %file1%
python deletefile.py --host 198.46.132.117 --port 8080 %md5% %sha1%

python putfile.py --host 198.46.132.117 --port 8080 %file2%
python postfile.py --host 198.46.132.117 --port 8080 %md5% %sha1%
