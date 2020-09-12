import bpy


SIZE = 2.0

def delete_all_duplicates(context, tokeep):
    bpy.ops.object.select_all(action='DESELECT')
    to_remove = tokeep.name + '.'
    for obj in context.scene.objects:
        if obj.name.startswith(to_remove):
            obj.select_set(True)
    bpy.ops.object.delete(confirm=False)


def main(context):
    scene = context.scene
    die = scene.objects['die']
    index = 0
    for x in range(0, 2):
        for z in range(0, 4):
            die.select_set(True)
            bpy.ops.object.duplicate_move(
                OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'},
                TRANSFORM_OT_translate={"value":(SIZE*x, 0, SIZE*z)})
            bpy.ops.object.select_all(action='DESELECT')
            index += 1
            scene.render.filepath = '/tmp/{}-dice.png'.format(index)
            bpy.ops.render.render(write_still = 1)
            
    delete_all_duplicates(context, die)
    print('Rendered, look in /tmp/?-dice.png')


class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    def execute(self, context):
        main(context)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(SimpleOperator)


def unregister():
    bpy.utils.unregister_class(SimpleOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.simple_operator()
