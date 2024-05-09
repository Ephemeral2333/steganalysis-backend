import zipfile


def unzip_file(zip_src, dst_dir):
    """
    :param zip_src: zip文件的全路径
    :param dst_dir: 要解压到的目的地文件夹
    """
    r = zipfile.is_zipfile(zip_src)
    if r:
        fz = zipfile.ZipFile(zip_src, 'r')
        for file in fz.namelist():
            fz.extract(file, dst_dir)
    else:
        print('This is not a zip file')
