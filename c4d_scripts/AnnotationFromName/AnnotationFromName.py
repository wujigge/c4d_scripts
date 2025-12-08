import c4d
def main():
    # 1. 检查是否有选中对象，无选中则静默终止
    selected_objs = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    if not selected_objs:
        print("未选择任何对象，终止脚本")
        return

    # 定义标签名称常量
    PYTHON_TAG_NAME = "ForAnnotation"
    ANNOTATION_TAG_NAME = "ForName"

    for selected_obj in selected_objs:
        # 2. 检查并添加Python标签（ForAnnotation）
        python_tag = None
        # 遍历对象标签，查找指定名称的Python标签
        for tag in selected_obj.GetTags():
            if tag.GetType() == c4d.Tpython and tag.GetName() == PYTHON_TAG_NAME:
                python_tag = tag
                break

        # 不存在则创建新Python标签
        if not python_tag:
            python_tag = c4d.BaseTag(c4d.Tpython)
            python_tag.SetName(PYTHON_TAG_NAME)
            selected_obj.InsertTag(python_tag)
            print(f"已为 {selected_obj.GetName()} 添加Python标签：{PYTHON_TAG_NAME}")
        else:
            print(f"{selected_obj.GetName()} 已存在Python标签：{PYTHON_TAG_NAME}，跳过创建")

        # 3. 检查并添加Annotation标签（ForName）
        annotation_tag = None
        # 遍历对象标签，查找指定名称的Annotation标签（Tannotation类型）
        for tag in selected_obj.GetTags():
            if tag.GetType() == c4d.Tannotation and tag.GetName() == ANNOTATION_TAG_NAME:
                annotation_tag = tag
                break

        # 不存在则创建新Annotation标签
        if not annotation_tag:
            annotation_tag = c4d.BaseTag(c4d.Tannotation)
            annotation_tag.SetName(ANNOTATION_TAG_NAME)
            selected_obj.InsertTag(annotation_tag)
            print(f"已为 {selected_obj.GetName()} 添加Annotation标签：{ANNOTATION_TAG_NAME}")
        else:
            print(f"{selected_obj.GetName()} 已存在Annotation标签：{ANNOTATION_TAG_NAME}，跳过创建")

        # 4. 写入Python标签代码（实现对象名称与Annotation标签同步）
        sync_code = f"""import c4d

def main():
    # 获取标签所属对象
    obj = op.GetObject()
    if not obj:
        return

    # 目标Annotation标签名称
    ANNOTATION_TAG_NAME = "{ANNOTATION_TAG_NAME}"

    # 查找对象上的Annotation标签
    annotation_tag = None
    for tag in obj.GetTags():
        if tag.GetType() == c4d.Tannotation and tag.GetName() == ANNOTATION_TAG_NAME:
            annotation_tag = tag
            break

    if not annotation_tag:
        return

    # 获取对象当前名称并同步到Annotation标签
    current_name = obj.GetName()
    # 仅当名称不同时更新（避免重复触发）
    if annotation_tag[c4d.ANNOTATIONTAG_TEXT] != current_name:
        annotation_tag[c4d.ANNOTATIONTAG_TEXT] = current_name
        c4d.EventAdd()  # 刷新视图
"""

        # 将同步代码写入Python标签
        python_tag[c4d.TPYTHON_CODE] = sync_code
        print(f"已更新 {selected_obj.GetName()} 的Python标签同步代码")

        # 立即执行一次同步，刷新当前名称
        c4d.CallButton(python_tag, c4d.TPYTHON_CODE)
        print(f"已同步 {selected_obj.GetName()} 的名称到Annotation标签")

    # 刷新C4D界面
    c4d.EventAdd()

if __name__ == "__main__":
    main()