# tempe-graffiti

aws s3 cp s3://sagemaker-graffiti-images/ sagemaker-graffiti-images/ --recursive

# Clear and copy test directory
rm -rf sagemaker-graffiti-images/split/test/*
aws s3 cp --only-show-errors s3://sagemaker-graffiti-images/image-classification-transfer-learning/test sagemaker-graffiti-images/split/test --recursive
