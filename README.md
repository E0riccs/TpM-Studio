# TpM-Studio
Created.

# INSTALL 
## MiniO

可能需要解决网络问题
```bash
docker pull minio/minio
```

Windows上推荐Docker Desktop，并运行在WSL2后端模式中
```bash 
docker run -p 9000:9000 -p 9090:9090 --name minio -d --restart=always \
    -v YOUR_DATA_PATH:/data -v YOUR_CONFIG_PATH:/root/.minio \
    minio/minio \
    server /data --console-address ":9090"
```

Check [localhost:9090](http://localhost:9090/login) with default ID: minioadmin, Password: minioadmin.
## 
