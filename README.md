# 老板 Skills

原来的单体“老板 Skill”已经拆成两个职责单一的 Skill：一个只负责把内容写好，一个只负责把内容审严。这样可以避免改稿时夹带长篇审核，也能避免审稿时擅自重写全文。

## 1. lao-ban-script-writer

负责内容生产与表达：

- 写稿、改稿、洗稿和口语化
- 模仿“老板”的直接、具体、高标准语气
- 设计短视频标题、钩子和开头
- 保留原意，清理转写错误、重复和机械套话
- 用确定性检测拦截重复的“不是……而是……”及常见 AI 套话

不负责专业事实审核。遇到可疑数据、医学结论或政策表述时，只标记为“待审核”。

## 2. lao-ban-content-reviewer

负责发布前审核：

- 检查专业错误和事实风险
- 检查前提、因果、结论和例外条件
- 判断标题是否夸大、是否能被正文兑现
- 找出适用人群、风险、边界、数据来源等信息缺口
- 给出“可发 / 修改后可发 / 不能发”的明确结论

默认不重写全文，只给问题、理由和修改方向。

## 推荐工作流

先调用 `$lao-ban-script-writer` 完成稿件，再调用 `$lao-ban-content-reviewer` 做发布前审核。审核退回后，只把明确的问题交回写稿 Skill 修改。

## 安装

Windows PowerShell：

```powershell
git clone https://github.com/Cheer12936/colleague-lao-ban-skill.git "$env:USERPROFILE\.codex\skills\lao-ban-skills"
```

重新载入 Codex 后，可以分别使用：

- `$lao-ban-script-writer`
- `$lao-ban-content-reviewer`

如果安装过旧版 `colleague-lao-ban`，请先停用旧版，避免多个 Skill 同时响应。

## 仓库结构

```text
lao-ban-script-writer/
  SKILL.md
  agents/openai.yaml
  scripts/style_lint.py
lao-ban-content-reviewer/
  SKILL.md
  agents/openai.yaml
```

## 许可

当前仓库未附开源许可证。如需允许复制、修改或再发布，请由仓库所有者补充明确的 `LICENSE`。
