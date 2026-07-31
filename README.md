# Maimemo Daily

每天 23:50（Asia/Taipei）调用墨墨开放 API，保存当天已经完成的单词及首次作答结果。

## 一、上传文件

把本压缩包中的全部文件上传到仓库根目录，须保留：

- `.github/workflows/collect.yml`
- `scripts/collect.py`
- `data/.gitkeep`

## 二、设置 Token

进入仓库：

`Settings → Secrets and variables → Actions → New repository secret`

创建：

- Name：`MAIMEMO_TOKEN`
- Secret：你重新生成的墨墨开放 API Token

不要把 Token 写入代码、README 或普通仓库文件。

## 三、允许 GitHub Actions 写入

进入：

`Settings → Actions → General → Workflow permissions`

选择：

`Read and write permissions`

然后保存。

## 四、测试

进入仓库的 `Actions` 页面，选择：

`Collect Maimemo Daily Words`

点击：

`Run workflow`

运行成功后，仓库中会出现：

- `data/YYYY-MM-DD.json`
- `data/latest.json`

## 五、供 ChatGPT 定时读取

要让 ChatGPT 的定时任务无需 GitHub 私有连接即可读取，需要把仓库设为 Public。

固定读取地址：

`https://raw.githubusercontent.com/oyqd0818-sketch/maimemo-daily/main/data/latest.json`

注意：公开仓库会使每日单词和“认识／模糊／忘记”状态可被持有链接的人看到，但不会暴露 `MAIMEMO_TOKEN`。

## 数据字段

- `FAMILIAR`：认识
- `VAGUE`：模糊
- `FORGET`：忘记
- `WELL_FAMILIAR`：熟知
- `CANCEL_WELL_FAMILIAR`：取消熟知

## 墨墨侧要求

墨墨开放学习 API 目前为公测功能。请在墨墨 App 中开启自动同步，并在当天至少打开一次 App，否则当天数据可能不完整。
