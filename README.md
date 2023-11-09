# bilibili-live-recorder

B站直播间录屏，录制完成后自动打包上传到阿里云 OSS 储存。

## 使用方法

1. 先下载 [BililiveRecorder](https://github.com/BililiveRecorder/BililiveRecorder) 中 Release 的命令行版本
2. 在项目目录中创建 `BililiveRecorder` 文件夹并将 BililiveRecorder 压缩包解压到里面
3. 将本项目下载并且导入 `requirements.txt`
4. 运行 `python3 -u main.py` 即可运行

## Config 配置

- OSSAccessKey 为阿里云 OSS 的 RAM 用户的 AccessKey
- OSSAccessToken 为阿里云 OSS 的 RAM 用户的 AccessToken
- OSSAccessPoint 填入阿里云 OSS 的 Endpoint
- OSSBucketName 填入阿里云 OSS 的 Bucket 名称
- OSSUploadSize 为录屏文件分片上传每片的大小
- roomId 为 B 站录制的直播间的 ID

## 鸣谢

本项目大量参考了 [valkjsaaa/auto-bilibili-recorder](https://github.com/valkjsaaa/auto-bilibili-recorder) 的代码，该项目拥有更多的功能，能够同时录制多个直播间！同时，感谢 [BililiveRecorder/BililiveRecorder](https://github.com/BililiveRecorder/BililiveRecorder) 的项目提供了录制方面的支持！
