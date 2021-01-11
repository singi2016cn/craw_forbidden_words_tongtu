# 安装

本项目使用 `python3`

## 1 创建 `venv` 环境

```
python -m venv venv

pip install --upgrade pip # 升级pip,如果已经是最新请跳过, pip -V 查看版本
```


## 2 安装项目依赖

> `data/` 目录下需要读写权限

> `linux` 系统需要安装 `chrome` ；例如 `centos` 可以执行 `yum install google-chrome-stable`

> `linux` 系统需要赋予 `chromedriver/linux/chromedriver` 可执行权限

```
pip install -r requirements.txt
```

## 3 配置下面文件

```
config.py
```

## 4 运行

```
python main.py
```