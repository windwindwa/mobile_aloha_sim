FROM nvcr.io/nvidia/isaac-sim:5.1.0

# 切换到 root 用户以安装系统包
USER root

# 环境变量设置
ENV DEBIAN_FRONTEND=noninteractive

# 注入自定义包路径到 PYTHONPATH
# 使用 ${PYTHONPATH} 追加到现有路径
ENV PYTHONPATH="/work/IsaacLab/source:/opt/isaac_pkgs:${PYTHONPATH}"

# 设置工作目录
WORKDIR /work

# 安装系统依赖
# 【修复点】：将 libgl1-mesa-glx 替换为 libgl1
RUN apt-get update && apt-get install -y \
    git curl wget vim zsh \
    net-tools iputils-ping \
    sudo locales \
    fonts-powerline \
    libx11-6 libxkbfile1 libsecret-1-0 libkrb5-3 libgl1 \
    && rm -rf /var/lib/apt/lists/*

# 生成语言包
RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8