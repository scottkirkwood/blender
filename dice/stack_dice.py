import bpy

import asyncio
import os
import sys


SIZE = 2.0

def delete_all_duplicates(context, tokeep):
    bpy.ops.object.select_all(action='DESELECT')
    to_remove = tokeep.name + '.'
    for obj in context.scene.objects:
        if obj.name.startswith(to_remove):
            obj.select_set(True)
    bpy.ops.object.delete(confirm=False)


def render(scene, index):
    scene.render.filepath = '/tmp/{}-dice.png'.format(index)
    bpy.ops.render.render(write_still = 1)
    return scene.render.filepath


async def merge_images(glob, output):
    abspath = bpy.path.abspath("//")
    proc = await asyncio.create_subprocess_exec(
        os.path.join(abspath, 'mergeimages'),
        '-o', output,
        glob,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    if proc.returncode != 0:
        if stdout:
            print(f'[stdout]\n{stdout.decode()}')
        if stderr:
            print(f'[stderr]\n{stderr.decode()}')

    
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
            filenames.append(render(scene, index))
            
    delete_all_duplicates(context, die)
    asyncio.run(merge_images('/tmp/?-dice.png', '/tmp/output-dice.png'))
    print('Rendered, look in /tmp/output-dice.png')


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
