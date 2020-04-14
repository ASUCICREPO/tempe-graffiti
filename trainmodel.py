import os
import shutil
import random
import subprocess
import glob
train_ratio = 0.8
batch_size = 32
max_batch = 300
proj_dir = os.path.dirname(os.path.abspath(__file__))
s3_dir = os.path.join(proj_dir,'sagemaker-graffiti-images')
dataset_dir = os.path.join(s3_dir ,'classified')
classes = os.listdir(dataset_dir)
split_dir = os.path.join(s3_dir,'split')
train_dir = os.path.join(split_dir, 'train')
validation_dir = os.path.join(split_dir, 'validation')
test_dir = os.path.join(split_dir, 'test')


def findNum(N, K): 
       
    rem = N % K 
    if(rem == 0): 
        return N 
    else: 
        return N - rem 
def split_data():
    for _class in classes:
        shutil.rmtree(os.path.join(train_dir,_class), ignore_errors=True)
        shutil.rmtree(os.path.join(validation_dir,_class), ignore_errors=True)
        shutil.rmtree(os.path.join(test_dir,_class), ignore_errors=True)
        print("\nCleaned all directories for %s" %_class)
        os.makedirs(os.path.join(train_dir,_class))
        os.makedirs(os.path.join(validation_dir,_class))
        os.makedirs(os.path.join(test_dir,_class))

        image_dir = os.path.join(dataset_dir, _class)
        # Only found jpg images in given set 
        image_set = set(glob.glob(os.path.join(image_dir, "*.jpg")))
        # print("\nImage Set",len(image_set))
        train_set = set(random.sample(image_set, min(findNum(len(image_set),batch_size),max_batch*batch_size//2)))
        # print(len(train_set))
        # train_set = random.sample(image_set, int(train_ratio*len(image_set)))
        # train_set = set(train_set[: ((len(train_set) - (len(train_set) % batch_size) )+1)])
        remaining_set = image_set - train_set
        validation_set = set(random.sample(remaining_set, int(findNum(0.5 * len(remaining_set),batch_size))))
        test_set = remaining_set - validation_set

        print ("\n",_class, "total images: ", len(image_set), "train images: ", len(train_set), "validation images: ", len(validation_set), "test images: ", len(test_set))
        print("\nImages " , _class, "before split", len(image_set), "after split", (len(train_set)+len(validation_set)+len(test_set)))

        for file in train_set:
            shutil.copy(os.path.join(image_dir, file), os.path.join(train_dir,_class))
        for file in validation_set:
            shutil.copy(os.path.join(image_dir, file), os.path.join(validation_dir,_class))
        for file in test_set:
            shutil.copy(os.path.join(image_dir, file), os.path.join(test_dir,_class))
    print("\nSuccessfully split to train, val, test in %s" %split_dir)

def create_rec_file():
    for rec_type in ['train','validation']:
        rec_dir = os.path.join(proj_dir,"rec")
        rec_file = os.path.abspath("im2rec.py")
        lst_file = os.path.join(rec_dir,"tempe-graffiti-"+rec_type)
        print("\nRunning cmd for %s lst file"%rec_type)
        command = r"python {0} {1} {2} --recursive --list --num-thread 8".format(rec_file, lst_file,  train_dir if rec_type=='train' else validation_dir)
        print(command)
        proc = subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)
        out,err = proc.communicate()
        print("\nOutput",out)
        print("\nError",err)
        print("\nRunning cmd for %s rec file"%rec_type)
        command = r"python {0} {1} {2} --recursive --pass-through --pack-label --num-thread 8".format(rec_file, lst_file, train_dir if rec_type=='train' else validation_dir)
        print(command)
        proc = subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)
        out,err = proc.communicate()
        print("\nOutput",out)
        print("\nError",err)

def upload_rec_to_s3():
    print("\n\nExecute pwershell script to upload rec files")
    subprocess.run(["powershell.exe", "C:\\cic\\tempe-graffiti\\upload_rec.ps1"])
    print("\nExecuted pwershell script to upload rec files")
        
split_data()
create_rec_file()
upload_rec_to_s3()