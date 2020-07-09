import os
import sys
import math
import random
import string
from PIL import Image

train="train_test"
test="test_test"
pic_path0="C:/Users/Lenovo/Desktop/covid0609/tensorflow-yolov3-master/COVID-CT-master/Images-processed/CT_NonCOVID/CT_NonCOVID/"
pic_path1="C:/Users/Lenovo/Desktop/covid0609/tensorflow-yolov3-master/COVID-CT-master/Images-processed/CT_COVID/CT_COVID/"
text_path="C:/Users/Lenovo/Desktop/covid0609/tensorflow-yolov3-master/COVID-CT-master/Images-processed/"
#C:\Users\Lenovo\Desktop\covid0609\tensorflow-yolov3-master\COVID-CT-master\Images-processed\CT_COVID\CT_COVID
#验证集数量
_NUM_TEST = 600
_NUM_TEST1 = 300
#随机种子
_RANDOM_SEED = 1
photo_filenames = []
def get_filenames(pic_path,sign):
    for filename in os.listdir(pic_path):
        # 获取文件路径
        path = os.path.join(pic_path, filename)
        img = Image.open(pic_path+filename)
        #photo_filenames.append(path+' 1,1,'+str(img.width-1)+','+str(img.height-1)+','+str(sign))
        photo_filenames.append(path+','+str(sign))
    return photo_filenames

def text_create(filenames,text_path,name):
    full_path = text_path + name + '.txt'
    file = open(full_path, 'w+')
    for i,filename in enumerate(filenames):
        file.write(filename+'\n')
        sys.stdout.write('\r>> Write %s %d/%d' % (name,i + 1, len(filenames)))
        sys.stdout.flush()
    file.close()
    sys.stdout.write('\n')
    sys.stdout.flush()

if __name__ == '__main__':
    # 获得所有图片
    pic_filenames = get_filenames(pic_path1,1)
    pic_filenames = get_filenames(pic_path0,0)
    random.seed(_RANDOM_SEED)
    random.shuffle(pic_filenames)
    training_filenames = pic_filenames[:_NUM_TEST]
    testing_filenames = pic_filenames[_NUM_TEST:]
    text_create(training_filenames,text_path,train)
    text_create(testing_filenames,text_path,test)

    print('生成文件')
