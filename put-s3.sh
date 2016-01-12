#! /bin/bash                                                                   
# Upload files to S3 using curl
                                                  
orig=$1
hostname=$(hostname)
date=$(date +"%m-%d-%Y")
file="$hostname--$date.tgz"
 
# Access key for se-tmp user
s3Key="<ACCESS_KEY>"
s3Secret="<SECRET_KEY>"

# S3 bucket
bucket="<YOUR_BUCKET_NAME>"
resource="/${bucket}/${file}"
 
contentType="application/x-compressed-tar"
dateValue=$(date -R)
stringToSign="PUT\n\n${contentType}\n${dateValue}\n${resource}"
 
# compress file
tar -cvzf "$file" "$orig"
 
# S3 request
signature=$(echo -en "${stringToSign}" | openssl sha1 -hmac ${s3Secret} -binary | base64)
curl -v -X PUT -T "${file}" \
  -H "Host: ${bucket}.s3.amazonaws.com" \
  -H "Date: ${dateValue}" \
  -H "Content-Type: ${contentType}" \
  -H "Authorization: AWS ${s3Key}:${signature}" \
  https://${bucket}.s3.amazonaws.com/"${file}"
 
rm "$file"
