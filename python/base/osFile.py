# coding=utf-8

import os

src_dir = u"G:\wegoimg\批量下载"
dst_dir = r"C:\Users\Administrator\Nox_share\ImageShare"
for root, dirs, files in os.walk(src_dir):
    dst_root = root.replace(src_dir, dst_dir, 1)
    if not os.path.exists(dst_root):
        os.makedirs(dst_root)
    for file in files:
        src_file = os.path.join(root, file)
        dst_file = os.path.join(dst_root, file)
        with open(src_file, 'rb') as fsrc, open(dst_file, 'wb') as fdst:
            fdst.write(fsrc.read())