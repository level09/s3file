import boto
from boto.s3.key import Key
import requests, os, tempfile, ntpath, hashlib


class S3File():
    s3_access_key = None
    s3_secret_token = None
    bucket = None
    conn = None
    temp_dir = None

    def __init__(self, S3_ACCESS_KEY, S3_SECRET_TOKEN, BUCKET_NAME):
        self.s3_access_key = S3_ACCESS_KEY
        self.s3_secret_token = S3_SECRET_TOKEN
        self.conn = boto.connect_s3(self.s3_access_key, self.s3_secret_token)
        self.bucket = self.conn.get_bucket(BUCKET_NAME)
        self.temp_dir = tempfile.mkdtemp()

    def push_from_url(self, url, remote_path=None):
        try:

            f, ext = os.path.splitext(url)
            new_file_name = '%s%s' % (hashlib.md5(url).hexdigest(), ext)
            file = self.__download_file(url, self.temp_dir, new_file_name)
            return self.__push_to_s3(file)
        except Exception, e:
            print e
            return None


    def push_from_path(self, path,generate_name=False, remote_path=None):
        try:
            path = os.path.abspath(path)

            f, ext = os.path.splitext(path)
            new_file_name = '%s%s' % (hashlib.md5(path).hexdigest(), ext)
            if generate_name:
                return self.__push_to_s3(path,change_name=new_file_name)
            else:
                return self.__push_to_s3(path)
        except Exception, e:
            print e
            return None


    def __push_to_s3(self,file,change_name=None):
        key = Key(self.bucket)
        if change_name:
            key.key = change_name
        else:
            key.key = ntpath.basename(file)

        key.set_contents_from_filename(file)
        key.make_public()
        url = key.generate_url(0, query_auth=False, force_http=True)
        try:
            os.remove(file)
        except Exception,e:
            print e
        return url

    def __download_file(self,url, path, filename=''):
        try:
            if filename == '':
                filename = url.split('/')[-1]
            r = requests.get(url, stream=True)
            with open(path + '/' + filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
                        f.flush()
            return os.path.join(path, filename)
        except Exception, e:
            print e


