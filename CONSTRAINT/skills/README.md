# CONSTRAINT/skills 技能索引

## 已安装的 Skills
（暂无，按需从仓库下载或自建）

## 推荐自建的 Skill

### ecg-processing（ECG 信号处理技能）
- 状态：未创建
- 覆盖能力：MIT-BIH 数据读取、小波去噪、R 峰检测、心拍分类、AIF360 公平性
- 创建方式：使用元技能 `skills-skills` 生成

### 元技能获取方式
```powershell
$url = "https://raw.githubusercontent.com/chenranfeng8-ops/vibe-coding-constraint/develop/assets/skills/skills-skills/SKILL.md"
Invoke-WebRequest -Uri $url -OutFile "CONSTRAINT/skills/skills-skills-SKILL.md"
```

## 从仓库获取其他 Skill

所有可用 Skills 列表：
https://github.com/chenranfeng8-ops/vibe-coding-constraint/tree/develop/assets/skills

按需下载单个 Skill：
```powershell
$skill = "skill-name"  # 替换为实际技能名
$url = "https://raw.githubusercontent.com/chenranfeng8-ops/vibe-coding-constraint/develop/assets/skills/$skill/SKILL.md"
Invoke-WebRequest -Uri $url -OutFile "CONSTRAINT/skills/$skill-SKILL.md"
```
