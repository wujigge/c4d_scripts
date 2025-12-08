import c4d

def main():
    doc = c4d.documents.GetActiveDocument()
    if not doc:
        return

    selected_objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)
    if not selected_objects:
        return

    DEFORMER_TYPES = [
        c4d.Obend, c4d.Obulge, c4d.Oshear, c4d.Otaper, c4d.Otwist, c4d.Offd,
        1024476, c4d.Ocacorrection, c4d.Ocamesh, c4d.Oexplosion, c4d.Oexplosionfx,
        c4d.Omelt, c4d.Oshatter, c4d.Ocajiggle, c4d.Ocasquash, c4d.Ocacollision,
        c4d.Oshrinkwrap, c4d.Ospherify, 1035447, c4d.Ocasmooth, c4d.Ocasurface,
        c4d.Owrap, 1060422, 1008982, c4d.Osplinerail, c4d.Omgsplinewrap,
        c4d.Odisplacer, c4d.Oformula, c4d.Ocamorph, 1021318, 5149, c4d.Obevel
    ]

    def collect_deformers(start_obj):
        """递归收集当前对象及其所有子级中的变形器"""
        deformers = []
        def traverse(obj):
            if not obj:
                return
            if obj.GetType() in DEFORMER_TYPES:
                deformers.append(obj)
            # 遍历子对象
            child = obj.GetDown()
            while child:
                traverse(child)
                child = child.GetNext()
        traverse(start_obj)
        return deformers

    all_deformers = []
    for obj in selected_objects:
        all_deformers.extend(collect_deformers(obj))

    if not all_deformers:
        return

    for deformer in all_deformers:
        current_vis = deformer[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR]
        if current_vis == 1:  # 如果当前可见性是 OFF，则切换为 DEFAULT
            deformer[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 2
        else:  # 否则，切换为 OFF
            deformer[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 1

    c4d.EventAdd()

if __name__ == '__main__':
    main()
    
