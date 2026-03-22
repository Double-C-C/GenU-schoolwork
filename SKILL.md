---
name: GenU-schoolwork
description: 学校作业生成工作流。自动执行命令、记录日志、生成终端截图、编写Markdown实验报告，最终打包交付。关键词：学校作业、实验报告、作业截图、作业生成、生成作业、打包作业。
read_when:
  - 用户提到学校作业、实验报告
  - 用户要生成作业文档
  - 用户要打包作业
  - 用户说"生成作业"、"作业截图"、"实验截图"
metadata:
  emoji: "📚"
---

# 学校作业生成工作流 Skill

## 用途

自动完成以下流程：
1. 执行实验命令，输出记录到日志文件
2. 用render.py将日志渲染为终端截图
3. 编写 Markdown 实验报告，嵌入截图
4. 打包为 `.tar.gz` 发给用户

## 目录结构

```
/tmp/homework<N>/
├── <作业标题>.md       # 实验报告
└── images/
    └── *.png           # 各步骤截图
```

最终打包为 `/tmp/homework<N>.tar.gz` 发送。

## 标准工作流

### Step 0 - 准备基础信息

用户学号 / 其他认证文字: <学号> = `未填写` (请询问用户获取认证文字/学号)

用户操作环境 = <操作系统> = `未填写`  (请自行获取当前操作系统)



### Step 1 - 执行命令并记录日志

```bash
LOG=/tmp/cmd_log.txt
{
  echo '<学号>@ubuntu:~$ <命令>'
  <实际执行命令> 2>&1
  echo '<学号>@ubuntu:~$ '
} > $LOG
```

> 用户名固定为学号，主机名 请读取当前操作系统运行环境。

### Step 2 - 生成截图

```bash
python3 /root/.openclaw/workspace/skills/homework-workflow/render.py \
  --user <学号> --host <操作系统> \
  --file /tmp/cmd_log.txt \
  --output /tmp/homework<N>/images/<step_name>.png
```

### Step 3 - 编写 Markdown 报告

```markdown
# <作业标题>

**姓名：** <学号> 
**日期：** YYYY-MM-DD  
**课程：** <课程名>  

---

## 步骤一：<步骤描述>

<操作说明>

![截图说明](images/<step_name>.png)

<结果说明>
```

### Step 4 - 打包与交付（仅在整个作业全部完成后）

所有步骤完成后，询问用户是否需要打包，或判断作业已全部完成时再打包：

```bash
cd /tmp && tar -czvf homework<N>.tar.gz homework<N>/
```

然后用 `<qqfile>/tmp/homework<N>.tar.gz</qqfile>` 发送给用户。

> ⚠️ 每完成一个步骤只需发截图预览，**不要每步都打包**。等用户确认作业全部完成，或用户主动要求打包时，再执行打包发送。

## 依赖

- Python3 + Pillow（`pip install Pillow`）
- tar
- render.py 已内置于本 skill 目录，无需安装 terminal-screenshot skill

## 注意事项

- 每次新作业用新目录 `/tmp/homework<N>/`，避免覆盖
- 学号默认 <学号>，如用户指定其他学号则替换<学号>
- MD 文档中截图路径用相对路径 `images/xxx.png`
- MD 文档的操作说明和结果说明中请不要出现类似AI生成的语言, 也不要出现"你可以"之类的字眼
- 每个步骤单独一张截图，命名清晰（如 `snort_096.png`、`install_gcc.png`）
- 作业完成后同步更新 MD，追加新步骤，重新打包
