#! /usr/bin/env bash

# 让 bash 在遇到错误时退出
set -e

# 运行初始化脚本
python app/initial_data.py

# 启动应用
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
