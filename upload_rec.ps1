echo ""
echo "Started upload of rec files"

#aws s3 cp ..\rec\tempe-graffiti-train.idx s3://sagemaker-graffiti-images/image-classification-transfer-learning/train/tempe-graffiti-train.idx
#aws s3 cp ..\rec\123 s3://sagemaker-graffiti-images/image-classification-transfer-learning/train/123 --recursive
read-host "Check powershell file and press enter to continue upload"

aws s3 cp ..\rec\tempe-graffiti-train.rec s3://sagemaker-graffiti-images/image-classification-transfer-learning/train/tempe-graffiti-train.rec
echo "Uploaded 1"
aws s3 cp ..\rec\tempe-graffiti-validation.rec s3://sagemaker-graffiti-images/image-classification-transfer-learning/validation/tempe-graffiti-validation.rec
echo "Uploaded 2"
aws s3 cp ..\split\test s3://sagemaker-graffiti-images/image-classification-transfer-learning/test --recursive

#shutdown /h

shutdown /s