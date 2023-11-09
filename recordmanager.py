import subprocess
import sys
import os
import time
import tarfile

from oss2 import SizedFileAdapter, determine_part_size
from oss2.models import PartInfo
import oss2

from config import OSSAccessKeyId, OSSAccessKeySecret, OSSAccessPoint, OSSBucketName, OSSUploadSize

BINARY_PATH = str(os.getcwd()) + "/"

def pushFile(source, filename):
    if os.path.exists(os.path.join(source, filename)) and os.path.isfile(os.path.join(source, filename)):
        auth = oss2.Auth(OSSAccessKeyId, OSSAccessKeySecret)
        bucket = oss2.Bucket(auth, OSSAccessPoint, OSSBucketName)
        key = "blive-record/" + filename
        filename = os.path.join(source, filename)
        total_size = os.path.getsize(filename)
        part_size = determine_part_size(total_size, preferred_size=OSSUploadSize)
        print("正在上传", filename, part_size)


        headers = dict()
        headers['Cache-Control'] = 'no-cache'
        headers['Content-Encoding'] = 'utf-8'
        upload_id = bucket.init_multipart_upload(key, headers=headers).upload_id # 这里可以根据阿里云官方的 SDK 文档自行修改
        parts = []

        with open(filename, 'rb') as fileobj:
            part_number = 1
            offset = 0
            try:
                while offset < total_size:
                    print("正在上传：", part_number)
                    num_to_upload = min(part_size, total_size - offset)
                    # 调用SizedFileAdapter(fileobj, size)方法会生成一个新的文件对象，重新计算起始追加位置。
                    result = bucket.upload_part(key, upload_id, part_number,
                                                SizedFileAdapter(fileobj, num_to_upload))
                    parts.append(PartInfo(part_number, result.etag))
                    offset += num_to_upload
                    part_number += 1
            except:
                print("上传", filename, "时 OSS 发生错误，请重试")
                return False
        
        headers = dict()
        bucket.complete_multipart_upload(key, upload_id, parts, headers=headers)
        os.unlink(filename)
        return True
    return False

class RecordManager:

    def __init__(self, roomId: int):
        self.room = roomId
        self.pushingList = []
        self.startRecord()

    def startRecord(self):
        spawn_command = \
        f"{BINARY_PATH}BililiveRecorder/BililiveRecorder.Cli " \
        f"portable " \
        f"-d 63 " \
        f"--webhook-url " \
        f'"http://127.0.0.1:13589/process_handle" ' \
        f'--filename ' \
        '"{{ roomId }}/{{ \\"now\\" | time_zone: \\"Asia/Shanghai\\" | format_date: \\"yyyyMMdd\\" }}/'\
        '{{ roomId }}-{{ \\"now\\" | time_zone: \\"Asia/Shanghai\\" | format_date: \\"yyyyMMdd-HHmmss-fff\\" }}.flv" ' \
        f'{os.path.join(os.getcwd(), "storage")}/ ' \
        f'{self.room} '
        print(f"Spawn recorder for {self.room}: {spawn_command}")
        self.recorder = subprocess.Popen(spawn_command, shell=True)
    
    def handle_hook(self, data: dict):
        if data['EventType'] not in ['SessionStarted', 'SessionEnded', 'FileOpening', 'FileClosed'] :
            return None
        roomId = data['EventData']['RoomId']
        if roomId == self.room:
            print("直播间 ID 不一致！")
            return None
        if data['EventType'] == 'FileClosed':
            if data['EventData']['RelativePath'] not in self.pushingList:
                self.pushRecord(data['EventData']['RelativePath'])
                self.pushingList.append(data['EventData']['RelativePath'])
        
        return None

    def pushRecord(self, recordFile, retry = 0):
        if retry >= 5:
            print("文件重试上传超过 5 次，自动停止重试...")
            return 
        if not pushFile(os.path.join(os.getcwd(), "storage/"), recordFile):
            retry = retry + 1
            print("文件上传失败，正在重试重新上传，重试次数：", retry)
            self.pushRecord(recordFile, retry)
        else:
            self.pushingList.remove(recordFile)
        return 
