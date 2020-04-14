echo ""
echo "Started upload of rec files"

#aws s3 cp .\rec\tempe-graffiti-train.idx s3://sagemaker-graffiti-images/image-classification-transfer-learning/train/tempe-graffiti-train.idx
#aws s3 cp .\rec\123 s3://sagemaker-graffiti-images/image-classification-transfer-learning/train/123 --recursive
#read-host "Check script file and press enter to continue upload"


echo 'clean local log dir'
rm ./sagemaker-graffiti-images/logs/* -r -fo

echo 'clean s3 log dir'
aws s3 rm s3://sagemaker-graffiti-images/logs/ --recursive --include '*'

echo "Attempting upload train rec"
echo $(Get-Date)
aws s3 cp .\rec\tempe-graffiti-train.rec s3://sagemaker-graffiti-images/image-classification-transfer-learning/train/tempe-graffiti-train.rec
echo $(Get-Date)
echo "Uploaded 1"
echo "Attempting upload val rec"
echo $(Get-Date)
aws s3 cp .\rec\tempe-graffiti-validation.rec s3://sagemaker-graffiti-images/image-classification-transfer-learning/validation/tempe-graffiti-validation.rec
echo $(Get-Date)
echo "Uploaded 2"

echo 'download logs'
aws s3 cp --recursive s3://sagemaker-graffiti-images/logs/ ./sagemaker-graffiti-images/logs/

#aws s3 cp .\split\test s3://sagemaker-graffiti-images/image-classification-transfer-learning/test --recursive
#read-host "press enter to exit"

#shutdown /h

#shutdown /s	