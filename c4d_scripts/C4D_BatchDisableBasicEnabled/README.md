# 全场景关闭 Enabled（C4D_BatchDisableBasicEnabled）

遍历全场景层级，将开启的 Basic Enabled 设为关闭。

## 使用

1. 打开目标文档；不要求选择对象。
2. 在 C4D 脚本管理器运行同目录的 `C4D_BatchDisableBasicEnabled.py`。
3. 检查结果；首次使用请在场景副本中操作。

## 范围与恢复

有撤销代码，未在本轮验收；作用范围是整个场景，不是选中对象。

## 验证记录

2026-09-23：根据现有源码补齐说明，未修改脚本，未执行 C4D 宿主验证。目标整理基线为 C4D 2025，具体小版本兼容性待逐项登记。

[返回脚本总表](../../docs/script-catalog.md)
