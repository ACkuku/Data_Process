import json
import cv2, os
from xml.dom.minidom import Document


def generate_xml(name, split_lines, img_size, class_ind):
    doc = Document()

    annotation = doc.createElement('annotation')
    doc.appendChild(annotation)

    title = doc.createElement('folder')
    title_text = doc.createTextNode('BDD100k')
    title.appendChild(title_text)
    annotation.appendChild(title)

    title = doc.createElement('filename')
    title_text = doc.createTextNode(img_name)
    title.appendChild(title_text)
    annotation.appendChild(title)

    source = doc.createElement('source')
    annotation.appendChild(source)

    title = doc.createElement('database')
    title_text = doc.createTextNode("The BDD100k Database")
    title.appendChild(title_text)
    annotation.appendChild(title)

    title = doc.createElement('annotation')
    title_text = doc.createTextNode('BDD100k')
    title.appendChild(title_text)
    source.appendChild(title)

    size = doc.createElement('size')
    annotation.appendChild(size)

    title = doc.createElement('width')
    title_text = doc.createTextNode(str(img_size[1]))
    title.appendChild(title_text)
    size.appendChild(title)

    title = doc.createElement('height')
    title_text = doc.createTextNode(str(img_size[0]))
    title.appendChild(title_text)
    size.appendChild(title)

    title = doc.createElement('depth')
    title_text = doc.createTextNode(str(img_size[2]))
    title.appendChild(title_text)
    size.appendChild(title)

    for label in split_lines:
        cls_name = label['category']
        if cls_name in class_ind:
            bbox = label['box2d']
            if bbox['x1'] == -1:
                continue
            object = doc.createElement('object')
            annotation.appendChild(object)

            title = doc.createElement('name')
            title_text = doc.createTextNode(cls_name)
            title.appendChild(title_text)
            object.appendChild(title)

            title = doc.createElement('difficult')
            title_text = doc.createTextNode('0')
            title.appendChild(title_text)
            object.appendChild(title)

            bndbox = doc.createElement('bndbox')
            object.appendChild(bndbox)
            title = doc.createElement('xmin')
            title_text = doc.createTextNode(str(bbox['x1']))
            title.appendChild(title_text)
            bndbox.appendChild(title)
            title = doc.createElement('ymin')
            title_text = doc.createTextNode(str(bbox['y1']))
            title.appendChild(title_text)
            bndbox.appendChild(title)
            title = doc.createElement('xmax')
            title_text = doc.createTextNode(str(bbox['x2']))
            title.appendChild(title_text)
            bndbox.appendChild(title)
            title = doc.createElement('ymax')
            title_text = doc.createTextNode(str(bbox['y2']))
            title.appendChild(title_text)
            bndbox.appendChild(title)

    # with open('./VOC2012/Annotations/' + name[:-4] + '.xml', 'w') as f:
        # f.write(doc.toprettyxml(indent=''))
     #    f.write(doc.toprettyxml())


if __name__ == '__main__':
    img_sets = ['train', 'val']
    root_path = "/home/disk/data/bdd100k/bdd100k"
    class_ind = ["bus", "traffic light", "traffic sign", "person", "bike", "truck", "motor", "car", "train", "rider"]
    for img_set in img_sets:
        with open('../../VOC2012/ImageSets/Main/{}.txt'.format(img_set), 'w') as f:
            label_path = os.path.join(root_path, 'labels', 'bdd100k_labels_images_{}.json'.format(img_set))
            img_path = os.path.join(root_path, 'images', '100k', '{}'.format(img_set))
            frames = json.load(open(label_path, 'r'))
            for frame in frames:
                img_name = frame['name']
                f.write(img_name[:-4])
                f.write('\n')
                img_size = cv2.imread(os.path.join(img_path, img_name)).shape
                labels = frame['labels']

                for label in labels:
                    cls_name = label['category']
                    if cls_name in class_ind:
                        xy = label['box2d']
                        if int(round(xy['x1'])) >= int(round(xy['x2'])) or int(round(xy['y1'])) >= int(round(xy['y2'])):
                            xy['x1'] = -1
                            continue
                        # if int(round(xy['x1'])) < 0:
                        #     xy['x1'] = 0
                        #     xy['x1'] += 1
                        # if int(round(xy['y1'])) < 0:
                        #     xy['y1'] = 0
                        #     xy['y1'] += 1
                        # if int(round(xy['x2'])) > img_size[1]:
                        #     xy['x2'] = img_size[1]
                        #     xy['x2'] -= 1
                        # if int(round(xy['y2'])) > img_size[0]:
                        #     xy['y2'] = img_size[0]
                        #     xy['y2'] -= 1

                generate_xml(img_name, labels, img_size, class_ind)
