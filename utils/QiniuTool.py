from flask import current_app
from qiniu import Auth, put_data


class QiniuTool:
    def __init__(self):
        ak = current_app.config.get("QINIU_AK")
        sk = current_app.config.get("QINIU_SK")
        self.q = Auth(ak, sk)
        self.bucket_name = current_app.config.get("QINIU_BUCKET_NAME")

    def upload(self, image, newfilename):
        token = self.q.upload_token(self.bucket_name, newfilename, 3600)
        res = put_data(up_token=token, key=newfilename, data=image)
        print(res)
        if res[0]["key"] == newfilename:
            return newfilename
        else:
            return False
