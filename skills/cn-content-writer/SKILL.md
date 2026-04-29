---
name: cn-content-writer
description: 中文社交媒体内容创作 — 公众号文章写作 (wechat-writer) + 小红书文案转换 (xhs-writer)。覆盖从选题、标题优化、文章结构到跨平台适配的完整内容工作流。
---

# CN Content Writer — 中文社交媒体内容创作

Umbrella skill for Chinese social media content creation: from writing WeChat Official Account (公众号) articles to adapting them for Xiaohongshu (小红书).

## Pipeline

```
Topic/URL → WeChat Article (wechat-writer) → XHS Adaptation (xhs-writer)
```

## Skill References

| Reference | Purpose | Content Type | Key Features |
|-----------|---------|-------------|--------------|
| [wechat-writer.md](references/wechat-writer.md) | 技术公众号文章写作 | Tech wechat articles | Title formulas, article structures, hook techniques, CTA templates |
| [xhs-writer.md](references/xhs-writer.md) | 公众号文章转小红书文案 | Xiaohongshu style copy | Cross-platform adaptation, cover design specs, emoji styling |

---

## Workflow Selection

| User Request | Use |
|-------------|-----|
| "Write an article about [topic]" → wechat-writer — generates titles, outline, full article |
| "Optimize this title" → wechat-writer — applies title formulas |
| "Generate an article outline" → wechat-writer — picks structure template |
| "Convert this article to 小红书 style" → xhs-writer — adapts content |
| "Polish this tech article" → wechat-writer — refines expression/structure |

## WeChat Writer — Quick Summary

**Title formulas**: 数字型 (`5个技巧让你…`), 痛点型 (`还在手写SQL？`), 悬念型, 权威型

**Structure templates**: 入门教程, 避坑指南, 对比评测, 深度解析, 实战复盘, 观点输出

**Writing specs**: 段落3-5行, 每800字配图, 代码可运行且≤20行

## XHS Writer — Quick Summary

**Conversion process**: URL/本地文件 → 抓取/读取 → 分析结构 → 转换小红书写法 → 生成封面图文案 → 保存

**Style requirements**: 精简核心信息, 情绪化表达 (宝子们/家人们), Emoji 点缀, 3-5个hook开头句

**Output files** per article: `{date}_{title}_xhs.md` (文案), `{date}_{title}_cover-points.md` (封面设计)

## References

- `references/wechat-writer.md` — Full wechat article writing guide with templates
- `references/xhs-writer.md` — Full xiaohongshu adaptation workflow
