# CodeXRay｜把你的反馈，变成 AI 下一次写代码的依据。

CodeXRay 会记录你对代码讲解、实现、调试和审查的明确反馈，并在你提出要求时将反馈合成为个性化代码 prompt。

让有用的反馈持续积累，让相同的纠正少说一次。

[English](README.md)

## 快速开始

需要 Git、Python 3，以及支持 `codex plugin` 命令的 Codex 版本。

在终端执行：

```sh
git clone https://github.com/qiuchenmeng/CodeXRay.git
cd CodeXRay
codex plugin marketplace add .
codex plugin add codexray@codexray
```

最后两条命令完成市场注册和插件安装。请在与你实际使用的 Codex 应用相同的环境、配置目录中执行。仅克隆仓库不会注册插件。

在终端检查安装结果：

```sh
codex plugin list --marketplace codexray --json
```

插件应处于已安装且启用状态。还可以让 CodeXRay 在已安装的技能目录中运行其自带的 `scripts/append_feedback.py --paths`；该命令只报告路径，不创建反馈。

## 直接从 GitHub 安装

将本次插件结构发布到仓库后，其他用户可以不单独克隆，直接执行：

```sh
codex plugin marketplace add https://github.com/qiuchenmeng/CodeXRay.git
codex plugin add codexray@codexray
```


新建 Codex 对话，打开你要处理的代码项目，然后发送：

```text
@codexray 请解释这个项目的代码结构。
```

如果客户端用 `$` 选择 skill，也可以在该选择器中选择 `codexray`。确认可用技能列表出现 `codexray:codexray`；安装后仍未出现时，重启 Codex。

使用这个codexray之后，我希望我给出反馈如：给每个新加的代码后面都增加注释 # +++ , 这样此后都会增加对应的注释，如果我说，不需要增加了，那么直接删掉这个部分的偏好。