# 基于深度学习的影像隐写分析系统（Flask 后端）

## 一、项目概述
本项目是我的毕业设计--基于深度学习的影像隐写分析系统的后端部分，使用 Flask 框架搭建，依托于 SRNet_CBAM 模型，旨在为用户提供高效、准确的影像隐写分析服务，能够判断影像中是否存在隐藏信息，助力保障数字影像的安全性。

## 二、功能特点
- **精准分析**：利用 SRNet_CBAM 强大的特征提取和分析能力，对上传的影像进行深度检测，准确判断其是否被隐写以及隐写的可能性程度，为用户提供可靠的分析结果。
- **高效响应**：基于 Flask 框架的轻量级和异步处理特性，能够快速响应用户的分析请求，在短时间内完成影像的隐写分析并返回结果，提升用户体验。
- **易于集成**：提供简洁清晰的 API 接口，方便与前端界面或其他相关系统进行集成，可轻松嵌入到更大型的数字媒体安全检测平台中，增强整体系统的功能完整性。

## 三、技术架构
- **后端框架**：Flask
    - Flask 作为一个轻量级的 Web 框架，为项目提供了简单易用的路由系统、请求处理机制和响应生成功能，使得我们能够快速搭建起稳定的后端服务，专注于核心的影像隐写分析逻辑开发，而无需过多关注底层网络编程的复杂细节。
- **深度学习模型**：SRNet_CBAM
    - SRNet_CBAM 模型在隐写分析领域展现出卓越的性能。其独特的 CBAM 注意力机制能够使模型在处理影像时，更加精准地聚焦于关键特征区域，有效提升对隐写信息的检测准确率。通过在大量的影像数据集上进行训练，模型具备了良好的泛化能力，能够应对各种不同类型和场景下的影像隐写分析任务。
- **依赖库**
    - NumPy：用于数值计算，为模型的训练和推理过程中的数据处理提供高效的数组操作功能，加速矩阵运算等关键计算步骤，确保系统的运行效率。
    - PyTorch：作为深度学习的核心框架，负责模型的构建、训练和加载。它提供了丰富的神经网络层、优化器和工具函数，方便我们实现和优化 SRNet_CBAM 模型，使其能够准确地执行影像隐写分析任务。

## 四、安装与运行
1. **克隆项目**
```bash
git clone https://github.com/Ephemeral2333/steganalysis-backend
```
2. **创建虚拟环境（可选但推荐）**
```bash
conda create -n steganalysis python==3.9 
conda activate steganalysis
```
3. **安装依赖**
安装 https://github.com/Ephemeral2333/SRNet_CBAM 中的依赖
4. **下载预训练模型**
将 SRNet_CBAM 的预训练模型权重文件放置在项目指定的模型目录下（如 `models/` ），确保模型能够正确加载并进行推理。
5. **启动应用**
```bash
python app.py
```
应用启动后，将在本地监听指定端口（默认为 `5000` ），你可以通过访问 `http://localhost:5000` 来测试后端服务是否正常运行。
