import c4d
from c4d import documents

PLUGIN_TAG_NAME = "SquareSegementsForPlane"

def main():
    # 获取当前活动对象
    obj = doc.GetActiveObject()
    if obj is None:
        return

    # 检测是否为源生Plane对象
    if obj.GetType() != c4d.Oplane:
        return

    # 检测是否已有名为 "SquareSegementsForPlane" 的 Python Tag
    tags = obj.GetTags()
    for tag in tags:
        if tag.GetType() == c4d.Tpython and tag.GetName() == PLUGIN_TAG_NAME:
            return  # 如果已有该 Tag，则终止代码

    # 如果没有该 Tag，则添加一个
    python_tag = c4d.BaseTag(c4d.Tpython)
    python_tag.SetName(PLUGIN_TAG_NAME)
    obj.InsertTag(python_tag)

    # 填充 Python Tag 的代码
    code = """
import c4d

def main():
    obj = op.GetObject()
    if obj is None or obj.GetType() != c4d.Oplane:
        return

    # 获取 Plane 的参数
    width = obj[c4d.PRIM_PLANE_WIDTH]
    height = obj[c4d.PRIM_PLANE_HEIGHT]
    width_segments = obj[c4d.PRIM_PLANE_SUBW]
    height_segments = obj[c4d.PRIM_PLANE_SUBH]

    # 计算宽高比
    ws_hs = (width / width_segments) / (height / height_segments)

    # 获取自定义数据
    data = op.GetDataInstance()
    initialized = data.GetBool(1000)  # 自定义 ID 1000 用于存储是否初始化
    prev_width = data.GetReal(1003)  # 自定义 ID 1003 用于存储上次的 Width
    prev_height = data.GetReal(1004)  # 自定义 ID 1004 用于存储上次的 Height
    prev_width_segments = data.GetInt32(1001)  # 自定义 ID 1001 用于存储上次的 Width Segments
    prev_height_segments = data.GetInt32(1002)  # 自定义 ID 1002 用于存储上次的 Height Segments

    # 首次运行时调整 Height Segments
    if not initialized:
        target_height_segments = max(1, int(round((height / width) * width_segments)))
        obj[c4d.PRIM_PLANE_SUBH] = target_height_segments
        data.SetBool(1000, True)  # 标记为已初始化
        data.SetReal(1003, width)
        data.SetReal(1004, height)
        data.SetInt32(1001, width_segments)
        data.SetInt32(1002, target_height_segments)
        return

    # 检测参数变化
    if width != prev_width or height != prev_height:
        # 如果 Width 或 Height 改变，调整 Height Segments
        target_height_segments = max(1, int(round((height / width) * width_segments)))
        obj[c4d.PRIM_PLANE_SUBH] = target_height_segments
        data.SetReal(1003, width)
        data.SetReal(1004, height)
        data.SetInt32(1002, target_height_segments)
    elif width_segments != prev_width_segments:
        # 如果 Width Segments 改变，调整 Height Segments
        target_height_segments = max(1, int(round((height / width) * width_segments)))
        obj[c4d.PRIM_PLANE_SUBH] = target_height_segments
        data.SetInt32(1002, target_height_segments)
    elif height_segments != prev_height_segments:
        # 如果 Height Segments 改变，调整 Width Segments
        target_width_segments = max(1, int(round((width / height) * height_segments)))
        obj[c4d.PRIM_PLANE_SUBW] = target_width_segments
        data.SetInt32(1001, target_width_segments)

    # 更新存储的分段数和尺寸
    data.SetReal(1003, obj[c4d.PRIM_PLANE_WIDTH])
    data.SetReal(1004, obj[c4d.PRIM_PLANE_HEIGHT])
    data.SetInt32(1001, obj[c4d.PRIM_PLANE_SUBW])
    data.SetInt32(1002, obj[c4d.PRIM_PLANE_SUBH])
"""
    python_tag[c4d.TPYTHON_CODE] = code
    c4d.EventAdd()

if __name__ == "__main__":
    main()