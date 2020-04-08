import os
import shutil
import random
import subprocess

train_ratio,val_ratio,test_ratio = 0.8,0.1,0.1
batch_size = 32

cic_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dataset_dir = os.path.join(cic_dir,'classified')
classes = os.listdir(dataset_dir)
split_dir = os.path.join(cic_dir,'split')
train_dir = os.path.join(split_dir, 'train')
validation_dir = os.path.join(split_dir, 'validation')
test_dir = os.path.join(split_dir, 'test')


# if not os.path.exists(split_dir):

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
        image_set = set(os.listdir(image_dir))
        train_set = random.sample(image_set, int(train_ratio*len(image_set)))
        train_set = set(train_set[: (len(train_set) - (len(train_set) % batch_size) )])
        remaining_set = image_set - train_set
        validation_set = set(random.sample(remaining_set, int( (1/(val_ratio+test_ratio))*val_ratio * len(remaining_set))))
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
        rec_dir = os.path.join(cic_dir,"rec")
        rec_file = os.path.join(rec_dir,"im2rec.py")
        lst_file = os.path.join(rec_dir,"tempe-graffiti-"+rec_type)
        print("\nRun cmd for lst file")
        command = '\npython {0} {1} {2} --recursive --list --num-thread 8'.format(rec_file, lst_file,  train_dir if rec_type=='train' else validation_dir)
        print(command)
        print("\nRun cmd for rec file")
        command = '\npython {0} {1} {2} --recursive --pass-through --pack-label --num-thread 8'.format(rec_file, lst_file, train_dir if rec_type=='train' else validation_dir)
        print(command)

split_data()
create_rec_file()
