"""
坐标角度友好
功能：根据按键状态处理坐标或角度
- 无按键：坐标取整（四舍五入到整数）
- 按住Alt：角度精确到1位小数（四舍五入）
- 按住Shift：同时处理坐标和角度
- 版本: 版本v20250601.1
"""

import c4d
from c4d import gui
import math

def round_position(pos):
    """将位置向量四舍五入为整数"""
    return c4d.Vector(
        round((pos.x),0),
        round((pos.y),0),
        round((pos.z),0)
    )

def round_rotation(hpb):
    """将HPB角度向量四舍五入到1位小数（角度制）"""
    # 将弧度转换为角度，四舍五入后再转回弧度
    return c4d.Vector(
        math.radians(round(math.degrees(hpb.x), 1)),
        math.radians(round(math.degrees(hpb.y), 1)),
        math.radians(round(math.degrees(hpb.z), 1))
    )

def main():
    # 获取当前选择的对象
    selected_objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    if not selected_objects:
        return

    # 检测按键状态
    bc = c4d.BaseContainer()
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.BFM_INPUT_CHANNEL, bc):
        qualifier = bc[c4d.BFM_INPUT_QUALIFIER]
        alt_pressed = qualifier & c4d.QALT
        shift_pressed = qualifier & c4d.QSHIFT

    doc.StartUndo()

    for obj in selected_objects:
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)

        if shift_pressed:
            # 同时处理坐标和角度
            pos = obj.GetAbsPos()
            obj.SetAbsPos(round_position(pos))

            hpb = obj.GetAbsRot()
            obj.SetAbsRot(round_rotation(hpb))
        elif alt_pressed:
            # 仅处理角度
            hpb = obj.GetAbsRot()
            obj.SetAbsRot(round_rotation(hpb))
        else:
            # 仅处理坐标
            pos = obj.GetAbsPos()
            obj.SetAbsPos(round_position(pos))

    doc.EndUndo()
    c4d.EventAdd()

if __name__ == '__main__':
    main()