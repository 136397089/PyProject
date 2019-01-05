# -*- coding: utf-8 -*-
import os

from qcloud_image import Client
from qcloud_image import CIUrl, CIFile, CIBuffer, CIUrls, CIFiles, CIBuffers

appid = 'APPID'
secret_id = 'SECRETID'
secret_key = 'SECRETKEY'
bucket = 'BUCKET'

client = Client(appid, secret_id, secret_key, bucket)
client.use_http()
client.set_timeout(30)
