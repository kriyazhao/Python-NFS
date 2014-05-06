set file=testData.txt
set md5=735779d21596c407963518e17c35d65c
set sha1=4b661664f2cbdae20550b54f780f990606b48651

python infochunk.py --host 198.46.132.117  --port 8080 checkchunk
python putchunk.py --host 198.46.132.117 --port 8080 %file%
python getchunk.py --host 198.46.132.117 --port 8080 %md5% %sha1%
python postchunk.py --host 198.46.132.117 --port 8080 %md5% %sha1%
