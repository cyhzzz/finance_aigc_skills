# CDP 操作命令参考

## 热点采集命令

```bash
# 财联社深度
curl -s "http://localhost:3456/new?url=https://www.cls.cn/depth?id=1000"

# 新浪财经7×24
curl -s "http://localhost:3456/new?url=https://finance.sina.com.cn/7x24/"

# 东方财富操盘必读
curl -s "http://localhost:3456/new?url=https://finance.eastmoney.com/a/cdfsd_2.html"
```

## 小红书搜索命令

```bash
# 搜索话题（type=51获取笔记）
curl -s "http://localhost:3456/new?url=https://www.xiaohongshu.com/search_result?keyword={关键词}&type=51"

# 获取笔记列表（标题+时间）
curl -s -X POST "http://localhost:3456/eval?target={targetId}" \
  -d 'JSON.stringify({
    notes: Array.from(document.querySelectorAll(".note-item")).slice(0,12).map(el => ({
      title: el.querySelector(".title span")?.textContent?.trim() || el.textContent?.trim()?.slice(0,50),
      time: el.textContent?.match(/(\d+分钟前|\d+小时前|\d+天前)/)?.[0] || "未知"
    }))
  })'

# 点击具体笔记获取完整互动数据
curl -s "http://localhost:3456/new?url=https://www.xiaohongshu.com/explore/{笔记ID}"

# 获取笔记详情
curl -s -X POST "http://localhost:3456/eval?target={targetId}" \
  -d 'JSON.stringify({
    title: document.querySelector("h1")?.textContent?.trim() || document.title,
    liked: document.querySelectorAll(".count")[0]?.textContent?.trim() || "",
    collected: document.querySelectorAll(".count")[1]?.textContent?.trim() || "",
    commented: document.querySelectorAll(".count")[2]?.textContent?.trim() || "",
    content: document.querySelector(".note-content")?.textContent?.trim()?.slice(0,500) || ""
  })'
```

## 健康检查

```bash
# 检查CDP连接
curl -s http://localhost:3456/health
```
