#! /usr/bin/env bash

# 让 bash 在遇到错误时退出
set -e

# 添加当前目录到 PYTHONPATH
export PYTHONPATH=$PYTHONPATH:.

# 运行初始化脚本 (以模块方式运行)
echo "Running initialization script..."
python -m app.initial_data
echo "Initialization finished."

# 启动应用
echo "Starting Uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
