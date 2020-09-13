import bpy
import sys
sys.path.append("/usr/lib/python3/dist-packages")
from PIL import Image


SIZE = 2.0

def delete_all_duplicates(context, tokeep):
    bpy.ops.object.select_all(action='DESELECT')
    to_remove = tokeep.name + '.'
    for obj in context.scene.objects:
        if obj.name.startswith(to_remove):
            obj.select_set(True)
    bpy.ops.object.delete(confirm=False)


def merge_horizontally(fnames, output):
    images = [Image.open(x) for x in fnames]
    widths, heights = zip(*(i.size for i in images))
    
    total_width = sum(widths)
    max_height = max(heights)
    
    new_image = Image.new('RGBA', (total_width, total_height))
    
    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]
    
    new_im.save(output)
    

def main(context):
    scene = context.scene
    die = scene.objects['die']
    index = 0
    filenames = []
    for x in range(0, 2):
        for z in range(0, 4):
            bpy.ops.object.select_all(action='DESELECT')
            die.select_set(True)
            bpy.ops.object.duplicate_move(
                OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'},
                TRANSFORM_OT_translate={"value":(SIZE*x, 0, SIZE*z)})
            index += 1
            scene.render.filepath = '/tmp/{}-dice.png'.format(index)
            filenames.append(scene.render.filepath)
            bpy.ops.render.render(write_still = 1)
            
    delete_all_duplicates(context, die)
    print('Rendered, look in /tmp/?-dice.png')
    merge_horizontally(filenames, "/tmp/alldice.png")


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
