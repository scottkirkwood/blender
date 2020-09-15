import bpy

import asyncio
import os
import sys

def render(scene):
    bpy.ops.render.render(animation=True)
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
    render(scene)
    asyncio.run(merge_images('/tmp/dice/dice-?.png', '/tmp/dice/dice-map.png'))
    print('Rendered, look in /tmp/die/dice-map.png')

class AnimMergeOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.anim_merge_operator"
    bl_label = "Anim Merge Operator"

    def execute(self, context):
        main(context)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(AnimMergeOperator)


def unregister():
    bpy.utils.unregister_class(AnimMergeOperator)


if __name__ == "__main__":
    register()
    bpy.ops.object.anim_merge_operator()
