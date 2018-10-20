from pycocotools.coco import COCO
import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt
import pylab
pylab.rcParams['figure.figsize'] = (8.0, 10.0)
import os

annFile = "/home/disk/data/bdd100k/bdd100k/labels/coco_val.json"
coco = COCO(annFile)
cats = coco.loadCats(coco.getCatIds())
nms = [cat['name'] for cat in cats]

catIds = coco.getCatIds(catNms=nms)
imgIds = coco.getImgIds(catIds=catIds)
imgIds = coco.getImgIds(imgIds=imgIds)
img = coco.loadImgs(imgIds[np.random.randint(0, len(imgIds))])[0]

I = io.imread("/home/disk/data/bdd100k/bdd100k/images/100k/val/"+img['file_name'])
plt.imshow(I)
plt.show()

plt.imshow(I);
plt.axis('off')
annIds = coco.getAnnIds(imgIds=img['id'], catIds=catIds, iscrowd=None)
anns = coco.loadAnns(annIds)
coco.showAnns(anns)
plt.show()

