# s3file

Very simplified Library for s3 file uploads. 

###Usage 

```
from s3file import S3File
file = S3File('your s3 access key', 'your s3 secret token', 'your bucket name')
print file.push_from_url("https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png")

print file.push_from_path('path to your file')

```
