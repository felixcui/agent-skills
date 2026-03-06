---
name: ai-news-fetcher
description: 获取 AI 领域最新资讯并进行智能分类。用于从微信公众号 RSS 源获取 AI 相关文章，使用 AI 自动分类为「AI编程工具及实践」「AI模型与技术」「AI产品与应用」「AI行业动态」等类别，支持发送到飞书和发布到微信公众号。使用场景：每日 AI 资讯汇总、AI 新闻监控、自动资讯推送。
---

# AI 资讯获取器

从微信公众号 RSS 源获取最新的 AI 资讯，进行智能分类，并支持发送到飞书和发布到微信公众号。

## 功能特点

- **自动获取**：从配置的 RSS API 获取昨日到今日的 AI 资讯
- **智能分类**：使用 AI 模型自动将资讯分类到不同类别
- **分类类别**：
  - AI编程工具及实践（Cursor、Claude Code、Copilot 等）
  - AI模型与技术（大模型发布、算法创新、多模态等）
  - AI产品与应用（AI 应用产品、Agent、智能体等）
  - AI行业动态（融资并购、行业政策、市场趋势等）
- **过滤机制**：自动过滤指定公众号的内容和非AI相关内容
- **多格式输出**：支持纯文本、Markdown 等格式
- **公众号发布**：支持创建草稿和发布到微信公众号

## 使用方法

### 1. 获取资讯（仅输出）

```bash
python3 scripts/fetch_ai_news.py
```

### 2. 获取并发送到飞书

```bash
bash scripts/send_ai_news.sh
```

### 3. 发布资讯到微信公众号（新增）

#### 方式一：创建草稿（推荐先测试）

```bash
python3 scripts/publish_to_wechat.py --create-draft
```

#### 方式二：创建草稿并发布

```bash
python3 scripts/publish_to_wechat.py --publish
```

#### 方式三：指定天数和封面图

```bash
# 获取最近 3 天的资讯并发布
python3 scripts/publish_to_wechat.py --days 3 --publish

# 使用自定义封面图
python3 scripts/publish_to_wechat.py --cover-image /path/to/cover.jpg --publish

# 使用后台已有的封面图 media_id
python3 scripts/publish_to_wechat.py --thumb-media-id YOUR_MEDIA_ID --publish
```

#### 方式四：保存 Markdown 到本地

```bash
python3 scripts/publish_to_wechat.py --days 1 --save-md /path/to/ai_news.md
```

## 配置说明

### 修改 RSS API 密钥

编辑 `scripts/fetch_ai_news.py` 中的 API URL：

```python
url = f"https://wexinrss.zeabur.app/api/query?k=YOUR_API_KEY&content=0&before={before}&after={after}"
```

### 修改过滤的公众号

编辑 `scripts/fetch_ai_news.py` 中的 `EXCLUDED_BIZ_IDS` 集合：

```python
EXCLUDED_BIZ_IDS = {
    "3092970861",  # 公众号ID
    # 添加更多...
}
```

### 修改发送目标（飞书）

编辑 `scripts/send_ai_news.sh` 中的 `--target` 参数：

```bash
--target "ou_xxxxx"  # 飞书用户 open_id 或群聊 chat_id
```

### 配置微信公众号凭证

在 `aicoding-news-weekly/.env` 文件中配置（已在 skill 目录下）：

```bash
WECHAT_APPID=wx0f68874c718318bf
WECHAT_APPSECRET=4719e11ebae2e75231484b7a5eb79802
```

## 定时任务配置

### 飞书推送（已配置）

添加到 crontab 实现每日自动推送：

```bash
# 每天早上 7:10 执行
10 7 * * * cd ~/.openclaw/workspace-fs_news_claw && bash skills/ai-news-fetcher/scripts/send_ai_news.sh >> /var/log/ai_news.log 2>&1
```

### 微信公众号发布（可选）

如果需要自动发布到公众号，可以添加到 crontab：

```bash
# 每天早上 7:30 创建草稿
30 7 * * * cd ~/.openclaw/workspace-fs_news_claw && python3 skills/ai-news-fetcher/scripts/publish_to_wechat.py --create-draft >> /var/log/wechat_publish.log 2>&1

# 每天早上 8:00 发布文章
0 8 * * * cd ~/.openclaw/workspace-fs_news_claw && python3 skills/ai-news-fetcher/scripts/publish_to_wechat.py --publish >> /var/log/wechat_publish.log 2>&1
```

## 依赖

- Python 3.6+
- requests 库
- markdown 库
- pygments 库（代码高亮）
- openclaw CLI（用于发送消息）

## 输出示例

### 飞书格式

```
📰 AI 资讯汇总

> 📅 `2026-03-04` - `2026-03-05`
> 📊 共 **69** 条资讯（已过滤 9 条）

📌 AI编程工具及实践（5 条）
• [Cursor 0.45 发布，新增 Agent 模式](https://...)
• [Claude Code 使用技巧分享](https://...)

📌 AI模型与技术（4 条）
• [GPT-5 即将发布，参数规模突破](https://...)

📌 AI产品与应用（3 条）
• [OpenAI 推出新功能](https://...)

📌 AI行业动态（3 条）
• [某 AI 公司完成 B 轮融资](https://...)
```

### 微信公众号格式

标题：📰 AI 资讯汇总 - 2026年03月05日
摘要：本期汇总了最新的 AI 相关资讯，涵盖编程工具、模型技术、产品应用和行业动态等内容。
内容：HTML 格式的公众号文章

## 技术细节

### AI 资讯获取和分类

- 使用 `fetch_ai_news.py` 从 RSS API 获取资讯
- 使用阿里云百炼进行智能分类（通过 OpenClaw 调用）
- 关键词分类作为后备方案
- 自动过滤非AI相关内容（音乐、游戏、娱乐等）

### 微信公众号发布

- 使用 `publish_to_wechat.py` 统一发布流程
- 依赖 `aicoding-news-weekly/skills/md_to_html.py` 转换 Markdown 为 HTML
- 依赖 `aicoding-news-weekly/skills/wechat_api_client.py` 调用微信 API
- 支持创建草稿和发布文章两种模式

### 优化说明

- ✅ 移除非AI相关资讯（音乐、游戏、娱乐等）
- ✅ 只保留AI相关内容（编程工具、模型技术、产品应用、行业动态）
- ✅ 使用 aicoding-news-weekly skill 下的成熟工具
- ✅ 统一配置管理（.env 文件）
