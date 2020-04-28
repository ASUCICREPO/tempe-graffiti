# tempe-graffiti

aws s3 cp s3://sagemaker-graffiti-images/ sagemaker-graffiti-images/ --recursive

# Clear and copy test directory
rm -rf sagemaker-graffiti-images/split/test/*
aws s3 cp --only-show-errors s3://sagemaker-graffiti-images/image-classification-transfer-learning/test sagemaker-graffiti-images/split/test --recursive

-# Download latest model and unzip to root dir of repo, replace <>
-aws s3 cp --only-show-errors s3://sagemaker-graffiti-images/DEMO-imageclassification/output/DEMO-imageclassification-2020-<>/output/model.tar.gz .
-tar -xvzf model.tar.gz -C ./
-cp image-classification-symbol.json model-shapes.json image-classification-<>.params model/model-<>/
-
-# Copy model to model archive dir
-mkdir model/model-<>^C
-cp image-classification-<>.params image-classification-symbol.json model-shapes.json model/model-<>/^C
-vi model/model-<>/ReadMe.txt ^C
-
-#Results
-4/26 :: 4-24 model looks best
-4/27 :: 4-24 still best

