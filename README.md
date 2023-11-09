# bilibili-live-recorder
B站直播间录屏，录制完成后自动打包上传到 OSS



## Config 配置

- OSSAccessKey 为阿里云 OSS 的 RAM 用户的 AccessKey
- OSSAccessToken 为阿里云 OSS 的 RAM 用户的 AccessToken
- OSSAccessPoint 填入阿里云 OSS 的 Endpoint
- OSSBucketName 填入阿里云 OSS 的 Bucket 名称
- OSSUploadSize 为录屏文件分片上传每片的大小
- roomId 为 B 站录制的直播间的 ID
