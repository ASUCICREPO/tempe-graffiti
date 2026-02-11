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

## Disclaimers
Customers are responsible for making their own independent assessment of the information in this document.

This document:

(a) is for informational purposes only,

(b) references AWS product offerings and practices, which are subject to change without notice,

(c) does not create any commitments or assurances from AWS and its affiliates, suppliers or licensors. AWS products or services are provided "as is" without warranties, representations, or conditions of any kind, whether express or implied. The responsibilities and liabilities of AWS to its customers are controlled by AWS agreements, and this document is not part of, nor does it modify, any agreement between AWS and its customers, and

(d) is not to be considered a recommendation or viewpoint of AWS.

Additionally, you are solely responsible for testing, security and optimizing all code and assets on GitHub repo, and all such code and assets should be considered:

(a) as-is and without warranties or representations of any kind,

(b) not suitable for production environments, or on production or other critical data, and

(c) to include shortcuts in order to support rapid prototyping such as, but not limited to, relaxed authentication and authorization and a lack of strict adherence to security best practices.

All work produced is open source. More information can be found in the GitHub repo.
