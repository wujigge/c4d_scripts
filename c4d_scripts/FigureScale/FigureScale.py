import c4d

def get_object_size(obj):
    """
    获取物体的实际尺寸（X, Y, Z），保留4位小数。
    :param obj: 选择的物体
    :return: 尺寸元组 (size_x, size_y, size_z)
    """
    # 获取物体的边界框半径
    rad = obj.GetRad()

    # 计算实际尺寸（半径需乘以2），保留4位小数
    size_x = round(rad.x * 2, 4)
    size_y = round(rad.y * 2, 4)
    size_z = round(rad.z * 2, 4)

    return size_x, size_y, size_z

class FigureScaleDialog(c4d.gui.GeDialog):
    IDC_SOURCE_X = 1000
    IDC_SOURCE_Y = 1001
    IDC_SOURCE_Z = 1002

    def __init__(self, size_x, size_y, size_z):
        self.size_x = size_x
        self.size_y = size_y
        self.size_z = size_z
        self.last_input_value = None
        self.last_input_id = None

    def CreateLayout(self):
        self.SetTitle("FigureScale")

        # 第一行：SourceX 和输入框
        self.AddStaticText(0, c4d.BFH_LEFT, name="SourceX")
        self.AddEditNumberArrows(self.IDC_SOURCE_X, c4d.BFH_RIGHT)
        self.SetFloat(self.IDC_SOURCE_X, self.size_x, min=0, step=0.1)

        # 第二行：SourceY 和输入框
        self.AddStaticText(0, c4d.BFH_LEFT, name="SourceY")
        self.AddEditNumberArrows(self.IDC_SOURCE_Y, c4d.BFH_RIGHT)
        self.SetFloat(self.IDC_SOURCE_Y, self.size_y, min=0, step=0.1)

        # 第三行：SourceZ 和输入框
        self.AddStaticText(0, c4d.BFH_LEFT, name="SourceZ")
        self.AddEditNumberArrows(self.IDC_SOURCE_Z, c4d.BFH_RIGHT)
        self.SetFloat(self.IDC_SOURCE_Z, self.size_z, min=0, step=0.1)

        # 第四行：OK 和 Cancel 按钮
        self.AddDlgGroup(c4d.DLG_OK | c4d.DLG_CANCEL)

        return True

    def Command(self, id, msg):
        if id == c4d.DLG_OK:
            if self.last_input_id == self.IDC_SOURCE_X:
                self.last_input_value = self.GetFloat(self.IDC_SOURCE_X)
            elif self.last_input_id == self.IDC_SOURCE_Y:
                self.last_input_value = self.GetFloat(self.IDC_SOURCE_Y)
            elif self.last_input_id == self.IDC_SOURCE_Z:
                self.last_input_value = self.GetFloat(self.IDC_SOURCE_Z)
            else:
                # 如果没有明确的最后输入框，按顺序检查
                if self.IsEnabled(self.IDC_SOURCE_X):
                    self.last_input_value = self.GetFloat(self.IDC_SOURCE_X)
                elif self.IsEnabled(self.IDC_SOURCE_Y):
                    self.last_input_value = self.GetFloat(self.IDC_SOURCE_Y)
                elif self.IsEnabled(self.IDC_SOURCE_Z):
                    self.last_input_value = self.GetFloat(self.IDC_SOURCE_Z)

            self.Close()
        elif id == c4d.DLG_CANCEL:
            self.last_input_value = None
            self.Close()
        elif id in [self.IDC_SOURCE_X, self.IDC_SOURCE_Y, self.IDC_SOURCE_Z]:
            self.last_input_id = id
        return True

def main():
    # 获取当前活动文档
    doc = c4d.documents.GetActiveDocument()

    # 获取当前选择的物体列表
    selected_objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0)

    # 如果没有选择物体，则不执行任何操作
    if not selected_objects:
        return

    # 如果选择了多个物体，提示用户只选择一个物体
    if len(selected_objects) > 1:
        c4d.gui.MessageDialog("请确保只选择一个物体。")
        return

    # 获取选择的物体
    obj = selected_objects[0]

    # 获取物体当前的尺寸
    x, y, z = get_object_size(obj)

    # 创建并打开对话框
    dlg = FigureScaleDialog(x, y, z)
    dlg.Open(c4d.DLG_TYPE_MODAL, defaultw=200, defaulth=150)

    # 获取最后输入的值
    new_value = dlg.last_input_value

    if new_value is None:
        # 用户没有任何输入，直接返回
        return

    # 判断最后输入的值是否和原来的值相同
    original_value = None
    if dlg.last_input_id == FigureScaleDialog.IDC_SOURCE_X:
        original_value = x
    elif dlg.last_input_id == FigureScaleDialog.IDC_SOURCE_Y:
        original_value = y
    elif dlg.last_input_id == FigureScaleDialog.IDC_SOURCE_Z:
        original_value = z

    if original_value is None or new_value == original_value:
        # 没有有效输入或者最后输入的值和原来的值相同，不做操作
        return

    # 得到了新的值，进行计算
    ratio = new_value / original_value
    if dlg.last_input_id == FigureScaleDialog.IDC_SOURCE_X:
        finalX = new_value
        finalY = y * ratio
        finalZ = z * ratio
    elif dlg.last_input_id == FigureScaleDialog.IDC_SOURCE_Y:
        finalX = x * ratio
        finalY = new_value
        finalZ = z * ratio
    elif dlg.last_input_id == FigureScaleDialog.IDC_SOURCE_Z:
        finalX = x * ratio
        finalY = y * ratio
        finalZ = new_value

    # 保留四位小数
    finalX = round(finalX, 4)
    finalY = round(finalY, 4)
    finalZ = round(finalZ, 4)

    print(f"finalX: {finalX}, finalY: {finalY}, finalZ: {finalZ}")

    # 计算缩放比例
    scale_x = finalX / x
    scale_y = finalY / y
    scale_z = finalZ / z

    # 获取物体的当前缩放值
    current_scale = obj.GetRelScale()
    # 应用新的缩放比例
    new_scale = c4d.Vector(current_scale.x * scale_x, current_scale.y * scale_y, current_scale.z * scale_z)
    obj.SetRelScale(new_scale)

    # 更新场景
    c4d.EventAdd()

if __name__ == "__main__":
    main()