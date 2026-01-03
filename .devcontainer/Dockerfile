# ---------------------------------------------------------
# ROS1 Noetic Dev Container - v2.1 (PyYAML Fixed)
# ---------------------------------------------------------

FROM osrf/ros:noetic-desktop-full

# 避免交互式前端干扰
ENV DEBIAN_FRONTEND=noninteractive

# ==============================
# 1. 安装系统工具、VS Code 依赖、编译工具
# ==============================
RUN apt-get update && apt-get install -y \
    git curl wget vim zsh \
    net-tools iputils-ping \
    sudo locales \
    fonts-powerline \
    # VS Code Server 依赖
    libx11-6 libxkbfile1 libsecret-1-0 libkrb5-3 libgl1-mesa-glx \
    # 编译工具 & Python 包管理
    python3-catkin-tools \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# ==============================
# 2. 【关键修复】升级 PyYAML
# ==============================
# Ubuntu 20.04 自带的 PyYAML 版本过低，导致 rosdep update 报错
# 这里强制升级到最新版
RUN pip3 install --upgrade PyYAML

# ==============================
# 3. 系统配置 (Locale & Root 密码)
# ==============================
RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

# 设置 root 密码 (可选，方便 su root)
RUN echo 'root:root' | chpasswd

# ==============================
# 4. 创建开发用户 'rosdev'
# ==============================
ENV USERNAME=rosdev
RUN groupadd --gid 1000 $USERNAME \
    && useradd --uid 1000 --gid 1000 -m $USERNAME -s /bin/zsh \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# 切换到开发用户
USER $USERNAME
WORKDIR /home/$USERNAME

# ==============================
# 5. Zsh 美化 & Pixi 安装
# ==============================
ENV DEFAULT_USER=$USERNAME

# 安装 Oh-My-Zsh 及插件
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended \
    && git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions \
    && git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

# 配置 .zshrc
RUN sed -i 's/ZSH_THEME="robbyrussell"/ZSH_THEME="agnoster"/g' ~/.zshrc \
    && sed -i 's/plugins=(git)/plugins=(git zsh-autosuggestions zsh-syntax-highlighting)/g' ~/.zshrc \
    && echo "source /opt/ros/noetic/setup.zsh" >> ~/.zshrc \
    && echo "export TERM=xterm-256color" >> ~/.zshrc

# 安装 pixi 并配置路径
RUN curl -fsSL https://pixi.sh/install.sh | bash \
    && echo 'export PATH="$HOME/.pixi/bin:$PATH"' >> ~/.zshrc \
    && echo 'eval "$(pixi completion --shell zsh)"' >> ~/.zshrc

# 容器启动命令
CMD ["/bin/zsh"]