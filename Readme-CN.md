# CodeXRay｜把你的反馈，变成 AI 下一次写代码的依据。

CodeXRay 会记录你对代码讲解、实现、调试和审查的明确反馈。

让有用的反馈持续积累，让相同的纠正少说一次。

[English](README.md)

## 在 Codex 中快速开始

把仓库克隆到任意目录，只完成了下载。需要先安装到 skill 目录，再调用。反馈存储脚本需要 Python 3。

### 通过 Codex 安装

在 Codex 对话框中发送以下内容，不是在终端执行：

```text
$skill-installer 从 https://github.com/qiuchenmeng/CodeXRay 安装 skill。SKILL.md 位于仓库根目录，skill 路径是 .，安装名称使用 codexray。
```

安装完成后，在下一轮消息中尝试调用。如果技能选择器仍未显示它，重启 Codex。

打开你要处理的代码项目，然后发送：

```text
$codexray 请解释这个项目的代码结构。
```

### 手动安装，供自己的所有项目使用

在终端中执行下面对应系统的命令。命令使用每位用户自己的主目录，不依赖作者的用户名或仓库位置。需要先安装 Git。

Windows PowerShell：

```powershell
New-Item -ItemType Directory -Force "$HOME/.agents/skills" | Out-Null
git clone https://github.com/qiuchenmeng/CodeXRay.git "$HOME/.agents/skills/codexray"
```

macOS / Linux / WSL（Bash）：

```bash
mkdir -p "$HOME/.agents/skills"
git clone https://github.com/qiuchenmeng/CodeXRay.git "$HOME/.agents/skills/codexray"
```

安装后应存在以下文件：

```text
~/.agents/skills/codexray/
  SKILL.md
  scripts/append_feedback.py
  references/derive-preferences.md
```

如果目标目录已存在，先检查已有安装，不要重复克隆覆盖。使用 WSL 或远程环境时，应安装到 Codex 实际运行的环境中。

### 只安装到某个项目

在你准备使用 CodeXRay 的代码项目根目录中执行：

```bash
git clone https://github.com/qiuchenmeng/CodeXRay.git .agents/skills/codexray
```

随后在 Codex 中打开这个项目并调用已安装的 skill。skill 目录应位于目标代码项目内部；与项目并列的仓库目录不等于项目级安装。

## 调用与识别检查

- Codex CLI / IDE：使用 `/skills` 或输入 `$`，选择已安装的 `codexray`，再发送代码问题。这些内容应输入对话框，不是终端命令。
- ChatGPT：输入 `@`，选择已安装的 skill。仅输入纯文本 `@codexray` 不会把本地 Git 仓库安装到 ChatGPT；需要先完成对应宿主的安装流程。
- 如果选择器里没有 `codexray`，先检查安装路径，再重启 Codex。模型在回复中重复技能名称，不能证明宿主已发现该 skill。
- 选择器显示技能后，可让它运行自身的 `scripts/append_feedback.py --paths`，进行最小检查。该命令只报告存储路径，不创建反馈文件；需要 Python 3。

反馈数据与安装目录分开保存，默认位于 `~/.codexray`，也可以用 `CODEXRAY_HOME` 指定。CodeXRay 只从明确反馈中积累偏好，并在你提出要求时合成个性化 prompt；普通代码问题不会自动成为反馈。

安装发现规则和调用语法见 [OpenAI Docs：Build skills](https://learn.chatgpt.com/docs/build-skills)。若要通过共享插件目录分发，应按官方插件流程将 skill 打包为插件；本文的克隆方式用于本地安装。
