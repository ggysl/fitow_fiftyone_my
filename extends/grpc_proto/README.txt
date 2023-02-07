编译命令:
cd {此文件夹}
python -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. ./FFRPC.proto

推荐版本:
grpcio==1.49.1
grpcio-tools==1.49.1
protobuf==4.21.7 # protobuf是很多库的依赖, 安装前注意是否已经存在, 存在的话建议保持原版本