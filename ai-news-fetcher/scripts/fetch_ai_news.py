#!/usr/bin/env python3
"""
AI 资讯获取与分类脚本（优化版）
从微信公众号 RSS 源获取资讯，使用 AI 进行智能分类
"""
import requests
import json
import subprocess
import os
from datetime import datetime, timedelta

# 需要过滤的公众号ID列表
EXCLUDED_BIZ_IDS = {
    "3092970861",
    "3975307385",
    "3870521375",
    "3573172279",
    "3087180557",
    "3271657808",
    "2397888542",
    "2390216734"
}

# RSS API 配置
RSS_API_KEY = os.getenv("AI_NEWS_API_KEY", "5O5H1c1NsT")
RSS_API_BASE = os.getenv("AI_NEWS_API_BASE", "https://wexinrss.zeabur.app")

# 分类图标映射
CATEGORY_ICONS = {
    "AI编程工具及实践": "💻",
    "AI模型与技术": "🧠",
    "AI产品与应用": "🚀",
    "AI行业动态及观察": "📈",
    "其他": "📂"
}


def classify_news_with_ai(news_list):
    """使用阿里云百炼进行智能分类（优化版）"""
    
    if not news_list:
        return {}
    
    # 将新闻标题拼接成提示
    titles = "\n".join([f"{i+1}. {item['title']}" for i, item in enumerate(news_list)])
    
    prompt = f"""请对以下 {len(news_list)} 条资讯进行智能分类，只保留AI相关内容，过滤掉非AI内容。

资讯列表：
{titles}

分类规则：
1. 只保留与AI、人工智能、机器学习、大模型、AI工具、AI应用相关的资讯
2. 分类选项（严格使用以下分类名称）：
   - AI编程工具及实践：AI编程工具（Cursor、Claude、Claude Code、GitHub Copilot、OpenClaw、IDE等）、编程助手、使用技巧、实战教程、代码生成、IDE插件、开发者工具、编程实践
   - AI模型与技术：大模型发布、版本更新（GPT-5、Claude新版等）、模型架构、训练技术、算法创新、性能优化、模型能力提升、推理优化、微调、量化、蒸馏等纯技术内容
   - AI产品与应用：AI应用产品、功能更新、工具发布、Agent、智能体、SaaS产品、应用场景、产品集成、面向用户的AI服务
   - AI行业动态及观察：融资投资、人事变动、上市IPO、行业政策、市场趋势、公司财报、竞争格局、合作并购等商业层面内容，以及行业观察、观点评论、趋势分析
   - 其他：AI相关但跨多个分类的内容、观点评论、行业观察、不确定归属的内容
3. 每条资讯只分到一个最相关的分类
4. 严格过滤非AI内容（重要）：
   - **非AI内容不要分类**：招聘、活动通知、时政、普通科技新闻、汽车、房产、游戏、娱乐、音乐、体育等
   - 非AI关键词列表：招聘、求职、简历、岗位、征集、活动、论坛、大会、峰会、工作坊、申报、时政、两会、政府工作报告、习近平、人大、政协、汽车、房产、房贷、公积金、社保、医保、教育、学校、大学、考试、毕业、就业、股市、股票、基金、理财、保险、银行、信用卡、电商、购物、旅游、美食、健康、医疗、疫苗、疫情、体育、足球、篮球、网球、奥运会、世界杯、娱乐、明星、八卦、音乐、演唱会、歌手、彩铃、游戏、电竞、动漫、漫画、小说、文学、电影、电视剧、综艺、直播、网红、抖音、快手、小红书、美妆、化妆、护肤、服装、时尚、奢侈品、母婴、育儿、宠物
5. 分类判断要点（重要）：
   - **AI编程工具及实践判断**：
     - 关键词：Claude编程、Cursor、Copilot、OpenClaw、IDE、编程助手、技巧、实战、教程、代码生成
     - 示例："Claude编程的42个实战技巧"、"Cursor使用指南"、"VSCode AI插件" → 编程工具及实践
   - **AI模型与技术判断**：
     - 关键词：GPT、Claude、Qwen、Llama、模型发布、版本更新、架构、算法、训练、推理、能力提升
     - 示例："GPT-5.4 将发布"、"Claude 4.0 发布"、"模型架构创新" → 模型与技术
   - **AI产品与应用判断**：
     - 关键词：AI产品、功能更新、工具发布、Agent、SaaS、应用场景、产品集成
     - 示例："OpenAI发布新产品"、"AI工具集成" → 产品与应用
   - **AI行业动态及观察判断**：
     - 关键词：融资、投资、离职、入职、上市、IPO、公司战略、竞争、观察、观点、趋势
     - 示例："OpenAI融资100亿"、"CEO离职"、"行业观察" → 行业动态及观察
   - **其他判断**：
     - AI相关但跨分类、观点评论、行业观察
     - 注意：如果与AI完全无关，不要分类
6. 特别注意：
   - 包含"招聘"、"求职"、"征集"、"活动"等关键词 → 不分类（非AI）
   - 包含"汽车"、"房产"、"股市"、"旅游"等关键词 → 不分类（非AI）
   - 包含"两会"、"政府工作报告"、"习近平"等政治关键词 → 不分类（非AI）
   - 包含"观察"、"观点"、"分析"等词（如果讲的是AI行业）→ AI行业动态及观察
   - 包含"Claude编程"、"编程技巧"、"实战"等词 → AI编程工具及实践
   - 包含"发布"、"版本"、"能力提升"等词（如果讲的是大模型本身）→ AI模型与技术
7. 如果某分类没有资讯，则不显示该分类

请以 JSON 格式输出分类结果，格式如下：
{{
  "分类名称": [资讯索引列表],
  ...
}}

例如：
{{
  "AI编程工具及实践": [1, 5, 8],
  "AI模型与技术": [2, 9],
  "AI产品与应用": [3, 10],
  "AI行业动态及观察": [4, 6, 7],
  "其他": []
}}

只输出 JSON，不要输出其他内容。"""

    try:
        # 使用 openclaw 命令行工具调用阿里云百炼
        cmd = [
            "openclaw",
            "agent",
            "--message", prompt,
            "--model", "bailian/glm-5"  # 使用阿里云百炼 GLM-5 模型
        ]
        
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
        
        if result.returncode == 0:
            # 尝试解析 JSON
            response_text = result.stdout.decode('utf-8').strip()
            # 尝试提取 JSON 部分
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_text = response_text[start_idx:end_idx]
                categories = json.loads(json_text)
                return categories
        
    except Exception as e:
        print(f"AI 分类失败: {str(e)}")
    
    # 如果 AI 分类失败，使用简单关键词分类作为后备
    return classify_by_keywords(news_list)


def classify_by_keywords(news_list):
    """关键词分类后备方案（谨慎过滤非AI内容）"""
    categories = {
        "AI编程工具及实践": [],
        "AI模型与技术": [],
        "AI产品与应用": [],
        "AI行业动态及观察": [],
        "其他": [],
        "非AI": []  # 用于标记非AI内容
    }

    # AI编程工具及实践关键词（开发者工具）
    coding_tool_keywords = ["Claude编程", "Cursor", "Claude Code", "Copilot", "IDE", "编辑器", "CLI", "命令行",
                            "代码生成", "IDE插件", "调试", "重构", "Git", "GitHub", "GitLab",
                            "VSCode", "IntelliJ", "PyCharm", "开发者工具", "Code Review",
                            "智能编程", "代码补全", "代码审查", "编程助手", "Vibe Coding",
                            "编程技巧", "实战技巧", "教程", "指南", "编程实践", "使用技巧"]

    # AI模型与技术关键词（技术本身）
    model_tech_keywords = ["模型架构", "Transformer", "MoE", "强化学习", "RL", "微调", "Fine-tuning",
                           "蒸馏", "量化", "部署", "算法", "训练", "推理", "参数",
                           "神经网络", "深度学习", "多模态", "Token", "上下文", "幻觉", "对齐",
                           "评测", "Benchmark", "技术突破", "研究", "论文", "学术",
                           "GPT-", "Claude", "Qwen", "Llama", "Gemini", "模型发布", "版本更新",
                           "能力提升", "性能优化", "模型能力", "推理优化"]

    # AI产品与应用关键词（面向用户的产品）
    product_app_keywords = ["AI产品", "AI应用", "功能更新", "产品发布", "新功能", "升级", "版本",
                            "内测", "公测", "Demo", "SaaS", "平台", "Agent", "智能体",
                            "Chatbot", "聊天机器人", "语音助手", "AI助手", "Assistant", "Bot",
                            "集成", "插件", "扩展", "工具", "应用场景", "解决方案"]

    # AI行业动态关键词（商业层面）
    industry_keywords = ["融资", "投资", "收购", "并购", "上市", "IPO", "财报", "估值",
                         "裁员", "入职", "离职", "人事", "任命", "辞职", "团队", "公司",
                         "合作", "战略", "布局", "政策", "法规", "监管", "法案", "禁令",
                         "许可", "合规", "市场", "行业", "赛道", "生态", "趋势", "报告",
                         "预测", "创业", "独角兽", "巨头", "竞争", "市场份额"]

    # 明确的非AI关键词（谨慎过滤）
    non_ai_keywords = [
        # 招聘类
        "招聘", "求职", "简历", "岗位", "工作", "诚聘", "HC", "职位",
        # 活动类
        "征集", "活动", "论坛", "大会", "峰会", "工作坊", "申报", "报名",
        # 时政类
        "两会", "政府工作报告", "习近平", "人大", "政协", "时政",
        # 汽车房产类
        "汽车", "新能源车", "蔚来", "小鹏", "理想汽车", "比亚迪", "特斯拉",
        "房产", "房贷", "公积金", "社保", "医保", "住房", "买房",
        # 教育类
        "教育", "学校", "大学", "考试", "毕业", "就业", "考研", "高考",
        # 金融理财类
        "股市", "股票", "基金", "理财", "保险", "银行", "信用卡", "投资",
        # 电商购物类
        "电商", "购物", "优惠", "折扣", "促销", "双十一", "618", "淘宝", "京东", "拼多多",
        # 旅游美食类
        "旅游", "美食", "餐厅", "酒店", "机票", "火车票",
        # 娱乐音乐类
        "娱乐", "明星", "八卦", "音乐", "演唱会", "歌手", "彩铃", "粉丝", "打榜",
        # 游戏电竞类
        "游戏", "电竞", "手游", "端游", "游戏本", "显卡",
        # 体育类
        "体育", "足球", "篮球", "网球", "奥运会", "世界杯", "NBA", "CBA",
        # 影视类
        "电影", "电视剧", "综艺", "直播", "网红", "抖音", "快手", "小红书",
        # 生活类
        "美妆", "化妆", "护肤", "服装", "时尚", "奢侈品", "母婴", "育儿", "宠物"
    ]

    for i, news in enumerate(news_list):
        title = news["title"]
        classified = False

        # 先检查是否明确非AI内容
        for keyword in non_ai_keywords:
            if keyword in title:
                categories["非AI"].append(i)
                classified = True
                break

        if not classified:
            # 优先检查AI编程工具及实践
            for keyword in coding_tool_keywords:
                if keyword in title:
                    categories["AI编程工具及实践"].append(i)
                    classified = True
                    break

        if not classified:
            for keyword in model_tech_keywords:
                if keyword in title:
                    categories["AI模型与技术"].append(i)
                    classified = True
                    break

        if not classified:
            for keyword in product_app_keywords:
                if keyword in title:
                    categories["AI产品与应用"].append(i)
                    classified = True
                    break

        if not classified:
            for keyword in industry_keywords:
                if keyword in title:
                    categories["AI行业动态及观察"].append(i)
                    classified = True
                    break

        if not classified:
            # 检查是否包含AI相关关键词（GPT、Claude、Qwen等）
            ai_keywords = ["GPT", "Claude", "Qwen", "Llama", "Gemini", "ChatGPT", "AI", "人工智能",
                         "大模型", "LLM", "机器学习", "深度学习", "智能体", "Agent"]
            for keyword in ai_keywords:
                if keyword in title:
                    categories["其他"].append(i)
                    classified = True
                    break

        if not classified:
            # 不包含AI关键词的，标记为非AI
            categories["非AI"].append(i)

    # 过滤掉非AI内容
    if "非AI" in categories and categories["非AI"]:
        excluded_indices = set(categories["非AI"])
        # 过滤掉非AI内容
        filtered_categories = {}
        for cat_name, indices in categories.items():
            if cat_name != "非AI":
                filtered_indices = [idx for idx in indices if idx not in excluded_indices]
                if filtered_indices:
                    filtered_categories[cat_name] = filtered_indices
        return filtered_categories

    return {k: v for k, v in categories.items() if k != "非AI"}


def get_news_summary(days: int = 1, classify: bool = True, platform: str = "feishu") -> str:
    """
    获取并分类汇总 AI 资讯（仅保留AI相关）
    
    Args:
        days: 获取最近几天的资讯（默认1天，即昨天到今天）
        classify: 是否进行 AI 分类（默认True）
        platform: 目标平台，影响格式（feishu/wechat/discord）
    
    Returns:
        格式化后的资讯汇总字符串（Markdown 格式）
    """

    # 计算日期范围
    today = datetime.now()
    yesterday = today - timedelta(days=days)

    # 格式化日期 YYYYMMDD
    after = yesterday.strftime("%Y%m%d")
    before = today.strftime("%Y%m%d")

    # API URL
    url = f"{RSS_API_BASE}/api/query?k={RSS_API_KEY}&content=0&before={before}&after={after}"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()

        # 提取 title 和 link，过滤指定公众号
        news_list = []
        excluded_count = 0
        if isinstance(data, dict) and 'data' in data and isinstance(data['data'], list):
            for item in data['data']:
                if isinstance(item, dict):
                    # 获取公众号ID并检查是否需要过滤
                    biz_id = str(item.get("biz_id", ""))
                    if biz_id in EXCLUDED_BIZ_IDS:
                        excluded_count += 1
                        continue

                    title = item.get("title", "")
                    link = item.get("link", "")
                    if title and link:
                        news_list.append({"title": title, "link": link})

        if not news_list:
            return f"""## 📰 AI 资讯汇总

> 📅 `{yesterday.strftime('%Y-%m-%d')}` - `{today.strftime('%Y-%m-%d')}`

😊 暂无AI相关资讯，请稍后再来查看～
"""

        # 分类
        if classify:
            categories = classify_news_with_ai(news_list)
        else:
            # 不进行 AI 分类，全部归入"最新资讯"
            categories = {"AI相关": list(range(len(news_list)))}

        # 构建汇总消息（优化后的 Markdown 格式）
        return format_news_markdown(news_list, categories, yesterday, today, platform)

    except Exception as e:
        return f"""## ❌ 获取 AI 资讯失败

> 错误信息：`{str(e)}`

请检查网络连接或 API 配置后重试。
"""


def format_news_markdown(news_list, categories, start_date, end_date, platform="feishu"):
    """
    将资讯格式化为美观的 Markdown
    
    Args:
        news_list: 资讯列表
        categories: 分类字典
        start_date: 开始日期
        end_date: 结束日期
        platform: 目标平台
    """
    lines = []
    
    # 标题
    lines.append("## 📰 AI 资讯汇总")
    lines.append("")
    
    # 日期和统计信息（使用引用块）
    lines.append(f"> 📅 `{start_date.strftime('%Y-%m-%d')}` - `{end_date.strftime('%Y-%m-%d')}`")
    lines.append(f"> 📊 共 **{len(news_list)}** 条资讯")
    lines.append("")
    
    # 计算AI相关资讯数量
    ai_news_count = sum(len(indices) for indices in categories.values())
    
    if ai_news_count == 0:
        lines.append("😊 暂无AI相关资讯～")
        lines.append("")
        return "\n".join(lines)
    
    # 按顺序输出分类
    category_order = [
        "AI编程工具及实践",
        "AI模型与技术", 
        "AI产品与应用",
        "AI行业动态及观察",
        "其他"
    ]
    
    category_number = 0
    for category in category_order:
        if category not in categories or not categories[category]:
            continue
            
        category_number += 1
        indices = categories[category]
        icon = CATEGORY_ICONS.get(category, "🤖")
        
        # 分类标题（使用 ### 层级）
        lines.append(f"### {icon} {category}（{len(indices)} 条）")
        lines.append("")
        
        # 资讯列表（带编号）
        for i, idx in enumerate(indices, 1):
            news = news_list[idx]
            title = news["title"]
            link = news["link"]
            lines.append(f"{i}. [{title}]({link})")
        
        lines.append("")
    
    
    return "\n".join(lines)


def get_raw_news(days: int = 1) -> list:
    """
    获取原始资讯列表（不含分类）
    
    Args:
        days: 获取最近几天的资讯
    
    Returns:
        资讯列表，每项包含 title 和 link
    """
    today = datetime.now()
    yesterday = today - timedelta(days=days)
    after = yesterday.strftime("%Y%m%d")
    before = today.strftime("%Y%m%d")
    url = f"{RSS_API_BASE}/api/query?k={RSS_API_KEY}&content=0&before={before}&after={after}"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()

        news_list = []
        if isinstance(data, dict) and 'data' in data and isinstance(data['data'], list):
            for item in data['data']:
                if isinstance(item, dict):
                    biz_id = str(item.get("biz_id", ""))
                    if biz_id in EXCLUDED_BIZ_IDS:
                        continue
                    title = item.get("title", "")
                    link = item.get("link", "")
                    if title and link:
                        news_list.append({"title": title, "link": link})
        return news_list
    except Exception as e:
        print(f"获取资讯失败: {str(e)}")
        return []


if __name__ == "__main__":
    print(get_news_summary())
