# -*- coding: utf-8 -*-

import hashlib
import shutil
import requests
import time
from caoliu import settings


class ImagePipeline(object):
    def process_item(self, item, spider):
        response = requests.get(item['image_src'], stream=True)
        with open('%ssrc.txt' % settings.SRC_PATH, 'a+') as f:
            hash_key = hashlib.sha1(str(time.time())).hexdigest()
            hash_image = hash_key + '.' + item['image_src'].split('.')[-1]
            f.write(item['url'].encode('utf-8')+'\t' + item['title'].encode('utf-8')+'\t'+item['image_src'].encode('utf-8') + '\t' + hash_image.encode('utf-8'))
        with open('%s%s' % (settings.IMAGE_PATH, hash_image), 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
