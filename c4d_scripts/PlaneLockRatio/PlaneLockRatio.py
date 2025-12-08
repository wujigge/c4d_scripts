# 脚本功能:
# 为当前选中的平面对象添加一个 Python Tag，以锁定其宽高比。
# 作者: wujigge 邮箱: wujigge@outlook.com

import c4d
from c4d import documents, plugins

def main():
    # 获取当前对象
    obj = doc.GetActiveObject()

    # 检测当前对象是否是平面（Plane）
    if obj is None or obj.GetType() != c4d.Oplane:
        return

    # 检测当前对象是否有一个名为 PlaneLockRatio 的 Python Tag
    tags = obj.GetTags()
    for tag in tags:
        if tag.GetName() == "PlaneLockRatio" and tag.GetType() == c4d.Tpython:
            return  # 已经有 PlaneLockRatio 的 Python Tag，不执行任何操作

    # 创建一个新的 Python Tag
    python_tag = obj.MakeTag(c4d.Tpython)
    if python_tag is None:
        return

    # 设置 Python Tag 的名称
    python_tag.SetName("PlaneLockRatio")

    # 获取 Python Tag 的代码容器
    code = """
import c4d

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

# 保存初始的宽度和高度
initial_width = None
initial_height = None

def main():
    global initial_width, initial_height

    # 获取当前对象
    obj = op.GetObject()

    # 检测当前对象是否是平面（Plane）
    if obj.GetType() != c4d.Oplane:
        return

    # 获取当前对象的宽度和高度
    width = obj[c4d.PRIM_PLANE_WIDTH]
    height = obj[c4d.PRIM_PLANE_HEIGHT]

    # 如果初始宽度和高度未设置，则设置它们
    if initial_width is None or initial_height is None:
        initial_width = width
        initial_height = height

    # 计算宽高比例
    if initial_width == 0:
        return
    ratio = initial_height / initial_width

    # 根据比例调整尺寸
    if width != initial_width and width != 0:
        obj[c4d.PRIM_PLANE_HEIGHT] = width * ratio
        initial_width = width
        initial_height = width * ratio
    elif height != initial_height and height != 0:
        obj[c4d.PRIM_PLANE_WIDTH] = height / ratio
        initial_height = height
        initial_width = height / ratio

# Cinema 4D 会自动调用 main 函数
"""
    
    # 将代码写入 Python Tag
    python_tag[c4d.TPYTHON_CODE] = code

    # 更新 Cinema 4D 界面
    c4d.EventAdd()

if __name__ == '__main__':
    main()