# 使用教程
## 步骤 1：安装依赖项
- 确保您的系统上已经安装了所需的Python库。您可以使用以下命令来安装它们：
```
pip install Flask requests

```
## 步骤 2：配置
- 在开始使用之前，您需要编辑 config.json 文件并配置一些参数，如recording，room_id等。示例配置文件如下：
```
{
  "recording": true,
  "room_id": null,
  "check_mode": "all",
  "area_name": ["Area1", "Area2"],
  "keywords": ["Keyword1", "Keyword2"],
  "parent_area_name": ["ParentArea1", "ParentArea2"]
}


```

-   recording: 录制状态，true 表示启用录制，false 表示禁用录制。（不需要修改）
-   room_id: 要监控的直播间ID，建议保持为空。
-   check_mode: 录制条件检查模式，可选值为 "area"（直播子分区）, "keywords"（关键词）, "parent_area"（直播主分区）, "all"（直播子分区和包含关键词）。
-   其他根据 check_mode 的不同，配置相应的检查条件。

## 步骤 3：运行应用
- 通过以下命令运行Flask应用：

```
python RCWM.py --log-level=INFO
```

## 此脚本使用ChatGPT3.5 生成的代码
