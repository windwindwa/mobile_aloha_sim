# 新版aloha的sim

执行`display_aloha.launch`

![aloha_v2](image.png)

## 注意URDF版本(以零点区分)

若您的机械臂,上电后使用上位机使能回零,j2、j3关节非触碰到限位位置,则为旧版零点

旧版本零点以j2、j3的限位位置偏移2度得到,参

`aloha_new_v00.urdf`

执行`display_aloha_v00.launch`


# 这是一个为你定制的 `README.md` 文档。它不仅仅是一个使用说明，还包含了**环境复现的核心提示词（Prompt）**，正如你所强调的——“生产过程更加重要”。

你可以将此内容直接保存为项目根目录下的 `README.md`。

---

# 🤖 ROS1 Hybrid Development Environment (Docker + Pixi)

> **核心理念**：使用 Docker 隔离系统级 ROS 环境，使用 Pixi 灵活管理 Python 算法环境。
> **适用场景**：VS Code (Mac) -> Remote SSH -> Ubuntu Host -> Docker Container。

## 📋 目录

1. [环境架构](https://www.google.com/search?q=%23-%E7%8E%AF%E5%A2%83%E6%9E%B6%E6%9E%84)
2. [宿主机准备 (Ubuntu Host)](https://www.google.com/search?q=%23-%E5%AE%BF%E4%B8%BB%E6%9C%BA%E5%87%86%E5%A4%87)
3. [快速启动](https://www.google.com/search?q=%23-%E5%BF%AB%E9%80%9F%E5%90%AF%E5%8A%A8)
4. [日常开发工作流](https://www.google.com/search?q=%23-%E6%97%A5%E5%B8%B8%E5%BC%80%E5%8F%91%E5%B7%A5%E4%BD%9C%E6%B5%81)
5. [故障排查 (Troubleshooting)](https://www.google.com/search?q=%23-%E6%95%85%E9%9A%9C%E6%8E%92%E6%9F%A5-troubleshooting)
6. [环境复现 (AI Prompt)](https://www.google.com/search?q=%23-%E7%8E%AF%E5%A2%83%E5%A4%8D%E7%8E%B0-ai-prompt-%E6%A0%B8%E5%BF%83%E8%B5%84%E4%BA%A7)

---

## 🏗 环境架构

该环境采用 **Hybrid（混合）** 架构，解决了 ROS1 系统依赖僵化与 Python 现代算法库（如 Torch/Numpy）版本冲突的问题。

* **OS 层 (Docker)**: `ros:noetic` (Ubuntu 20.04)，负责 `roscore`、`catkin build`、以及硬件驱动。
* **Shell 层**: `Zsh` + `Oh-My-Zsh` + 语法高亮/自动补全，非 Root 用户 (`rosdev`)，UID 自动同步。
* **Python 层 (Pixi)**: 独立于系统 Python，通过 `pixi.toml` 管理两个隔离环境：
* `ros1-python-env`: 用于运行深度学习、强化学习算法。
* `backup-env`: 备用调试环境。


* **编辑器**: VS Code Dev Container (自动注入插件、配置、挂载工作区)。

---

## 🖥 宿主机准备

在远程 **Ubuntu 宿主机** 上，必须配置图形显示权限，以便容器内的 Gazebo/Rviz 能显示在屏幕上。

1. **开放 X11 访问权限**:
```bash
# 在宿主机终端执行
xhost +local:docker

```


2. **检查 Display ID**:
```bash
echo $DISPLAY
# 通常输出 :0 或 :1

```


*DevContainer 已配置自动继承此变量，若显示有问题，请手动在容器内 `export DISPLAY=:0`。*

---

## 🚀 快速启动

1. **VS Code 连接**: 使用 Remote-SSH 连接到远程 Ubuntu 主机。
2. **打开项目**: 打开包含 `.devcontainer` 的文件夹。
3. **构建容器**:
* 点击左下角绿色图标 `><`。
* 选择 **Reopen in Container**。
* *首次构建需要几分钟，会自动安装 ROS、Pixi、Zsh 等。*



---

## 🛠 日常开发工作流

### 1. 编译 (Build)

容器启动后，或者代码有 C++ 变动/新增包时：

```bash
# 1. 确保在工作空间根目录
cd /home/rosdev/mobile_aloha_ws

# 2. 使用 catkin build (比 catkin_make 更强)
catkin build

```

### 2. 加载环境 (Source)

**这一步至关重要**，否则系统找不到你的包。

```bash
source devel/setup.zsh

```

*注：编译一次之后，第二次重建容器不用再编译，因为 `devel` 文件夹是通过挂载同步的。*

### 3. Python 环境 (Pixi)

不要直接用 `python`，请使用 Pixi 托管的环境：

```bash
# 进入 ROS1 专用 Python 环境
pixi shell -e ros1-python-env

```

*(此时终端提示符左侧会出现环境名称)*

### 4. 启动仿真 (Launch)

```bash
# 语法: roslaunch <包名> <launch文件名>
roslaunch aloha_new_description display_aloha.launch

```

---

## 🔍 故障排查 (Troubleshooting)

### 🔴 问题：找不到 Launch 文件 / Package Not Found

**现象**：
`RLException: [xxx.launch] is neither a launch file in package [xxx]...`

**像侦探一样排查 (3步法)**：

1. **确认物理位置**：
文件到底在哪？是不是名字打错了？
```bash
# 递归查找
find src/aloha_new_description -name "*.launch"

```


* *情况 A*: 没输出 -> 文件名错或不存在。
* *情况 B*: 在子文件夹 -> 引用时需要加路径，如 `subfolder/display.launch`。


2. **确认注册状态**：
ROS 看到这个包了吗？
```bash
rospack find aloha_new_description

```


* *报错*：说明没 Source 或者没编译。
* *解决*：`rospack profile` 刷新索引，然后再次 `source devel/setup.zsh`。


3. **终极修复连招 (标准重启流程)**：
如果上述都没用，按顺序执行：
```bash
cd /home/rosdev/mobile_aloha_ws  # 回家
catkin build                     # 重新编译
source devel/setup.zsh           # 重新加载
rospack list | grep aloha        # 验证确认

```



### 🔴 问题：Docker 权限报错 (Permission Denied)

如果在 `catkin build` 或 `pixi` 时遇到权限错误：

```bash
# 在容器内执行，夺回所有权
sudo chown -R $(id -u):$(id -g) .

```



