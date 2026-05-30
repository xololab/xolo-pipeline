bl_info = {
    "name": "Ateru Helper (ACEScg & Cycles)",
    "author": "Ronny Ascencio",
    "version": (2, 0, 6),
    "blender": (5, 0, 0),
    "location": "View3D > Sidebar > Pipeline",
    "description": "Collection configuration, View Layers and compositing with ACEScg y Cycles.",
    "category": "Pipeline",
}

import bpy
import os
import re
from bpy.app.handlers import persistent

LIGHT_GROUPS = ["HDR", "sun", "lgtA", "lgtB", "lgtC", "lgtD", "lgtE", "lgtF", "lgtG"]
ATERU_HANDLER_NAME = "ateru_update_paths_on_save"
_ATERU_RESAVING = False

# =============================================================================
# AUTO-PATH PIPELINE RESOLVER
# =============================================================================


def get_ateru_render_path():
    filepath = bpy.data.filepath
    if not filepath:
        print("Ateru Warning: Archivo no guardado. Usando ruta temporal.")
        return "//render_outputs/", "untitled"

    file_dir, filename = os.path.split(filepath)
    name_clean, _ = os.path.splitext(filename)  # Remueve el .blend

    version_match = re.search(r"(v\d+)", filename, re.IGNORECASE)
    version = version_match.group(1).lower() if version_match else "v001"

    norm_dir = os.path.normpath(file_dir)
    parts = norm_dir.split(os.sep)

    try:
        proj_idx = parts.index("projects")
        project_path = os.sep.join(parts[: proj_idx + 2])
        entity_type = parts[proj_idx + 2]
        entity_name = parts[proj_idx + 3]

        if entity_type == "shots":
            render_dir = os.path.join(
                project_path, "renders", "cg", entity_name, version
            )
        elif entity_type == "assets":
            render_dir = os.path.join(
                project_path, "renders", "assets", entity_name, version
            )
        else:
            render_dir = os.path.join(
                project_path, "renders", entity_type, entity_name, version
            )

        return render_dir + os.sep, name_clean

    except (ValueError, IndexError):
        return "//render_outputs/", name_clean


def build_render_filename(base_name, pass_name):
    version_match = re.search(r"(.+?)([_-]?v\d+)$", base_name, re.IGNORECASE)
    if version_match:
        prefix, version = version_match.groups()
        return f"{prefix}_{pass_name}{version}."
    return f"{base_name}_{pass_name}."


def set_if_different(owner, attr_name, value):
    if getattr(owner, attr_name, None) != value:
        setattr(owner, attr_name, value)
        return True
    return False


# =============================================================================
# CONFIGURACIÓN GLOBAL
# =============================================================================


def setup_render_engine():
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"

    # El output global de RenderSettings no soporta multilayer; el EXR
    # multilayer se configura en el nodo CompositorNodeOutputFile.
    scene.render.image_settings.file_format = "OPEN_EXR"
    scene.render.image_settings.color_depth = "16"
    scene.render.image_settings.color_mode = "RGBA"

    prefs = bpy.context.preferences.addons["cycles"].preferences
    if prefs.compute_device_type == "NONE":
        for compute_type in ["OPTIX", "CUDA", "METAL", "HIP", "ONEAPI"]:
            try:
                prefs.compute_device_type = compute_type
                break
            except:
                pass

    prefs.get_devices()
    for device in prefs.devices:
        device.use = True

    scene.cycles.device = "GPU"

    try:
        scene.display_settings.display_device = "sRGB"
        view_transforms = [
            t.name
            for t in scene.view_settings.bl_rna.properties["view_transform"].enum_items
        ]
        if "ACES 1.0 SDR-video" in view_transforms:
            scene.view_settings.view_transform = "ACES 1.0 SDR-video"
        elif "AgX" in view_transforms:
            scene.view_settings.view_transform = "AgX"
        scene.sequencer_colorspace_settings.name = "ACEScg"
    except:
        pass


# =============================================================================
# ACTIVACIÓN MASIVA DE PASES (VFX READY)
# =============================================================================


def create_collection(name, parent=None):
    if name not in bpy.data.collections:
        new_col = bpy.data.collections.new(name)
        if parent:
            parent.children.link(new_col)
        else:
            bpy.context.scene.collection.children.link(new_col)
    return bpy.data.collections[name]


def setup_view_layer_passes(vl):
    vl.use_pass_z = True
    vl.use_pass_normal = True
    vl.use_pass_vector = True
    vl.use_pass_uv = True
    vl.use_pass_position = True
    if hasattr(vl, "use_pass_mist"):
        vl.use_pass_mist = True

    vl.use_pass_diffuse_direct = True
    vl.use_pass_diffuse_indirect = True
    vl.use_pass_diffuse_color = True
    vl.use_pass_glossy_direct = True
    vl.use_pass_glossy_indirect = True
    vl.use_pass_glossy_color = True
    vl.use_pass_transmission_direct = True
    vl.use_pass_transmission_indirect = True
    vl.use_pass_transmission_color = True
    vl.use_pass_emit = True
    vl.use_pass_environment = True
    vl.use_pass_ambient_occlusion = True

    vl.use_pass_cryptomatte_object = True
    vl.use_pass_cryptomatte_material = True
    vl.use_pass_cryptomatte_asset = True

    if hasattr(vl, "cycles"):
        vl.cycles.denoising_store_passes = True

    if hasattr(vl, "lightgroups"):
        for lg_name in LIGHT_GROUPS:
            if lg_name not in vl.lightgroups:
                try:
                    bpy.ops.scene.view_layer_add_lightgroup(name=lg_name)
                except Exception as e:
                    print(f"Ateru Error - Light Group {lg_name}: {e}")


def setup_view_layer(vl_name, active_col_name, all_pass_names):
    scene = bpy.context.scene
    vl = scene.view_layers.get(vl_name) or scene.view_layers.new(vl_name)

    old_vl = bpy.context.window.view_layer
    bpy.context.window.view_layer = vl

    setup_view_layer_passes(vl)

    def set_layer_col_state(layer_col):
        if layer_col.collection.name == active_col_name:
            layer_col.exclude = False
            layer_col.indirect_only = False
            layer_col.holdout = False
        elif layer_col.collection.name in all_pass_names:
            layer_col.exclude = False
            layer_col.indirect_only = True
        for child in layer_col.children:
            set_layer_col_state(child)

    set_layer_col_state(vl.layer_collection)

    bpy.context.window.view_layer = old_vl
    return vl


# =============================================================================
# AUTO-WIRING EN COMPOSITOR
# =============================================================================


def add_file_slot(file_output, name, socket_type="RGBA"):
    """
    Blender 5 reemplazo file_slots por file_output_items. En esa API el nombre
    del item crea el socket y la capa EXR; en 4.x se mantiene file_slots.path.
    """
    if hasattr(file_output, "file_output_items"):
        item = file_output.file_output_items.new(socket_type, name)
        item.name = name
    else:
        item = file_output.file_slots.new(name)
        item.path = name
    return item


def get_light_group_socket(outputs, light_group_name):
    """Blender 5 exposes light group outputs as Combined_<group name>."""
    return outputs.get(f"Combined_{light_group_name}") or outputs.get(light_group_name)


def configure_output_path(file_output, render_out_path, file_name):
    changed = False

    if hasattr(file_output, "directory"):
        changed |= set_if_different(file_output, "directory", render_out_path)
        changed |= set_if_different(file_output, "file_name", file_name)
    else:
        changed |= set_if_different(
            file_output, "base_path", os.path.join(render_out_path, file_name)
        )

    return changed


def create_multilayer_output(tree, render_out_path, file_name, location, output_role):
    file_output = tree.nodes.new("CompositorNodeOutputFile")
    file_output.name = f"Ateru {output_role.title()} Output"
    file_output.label = f"Ateru {output_role.title()} EXR"
    file_output.location = location
    file_output.format.file_format = "OPEN_EXR_MULTILAYER"
    file_output.format.color_depth = "16"

    configure_output_path(file_output, render_out_path, file_name)

    if hasattr(file_output, "file_output_items"):
        file_output.file_output_items.clear()
    else:
        file_output.file_slots.clear()
        file_output.file_slots.new(file_name)

    return file_output


def is_utility_view_layer(view_layer_name):
    return view_layer_name.lower() == "utilitypass"


def get_compositor_tree(scene):
    if hasattr(scene, "compositing_node_group") and scene.compositing_node_group:
        return scene.compositing_node_group
    return getattr(scene, "node_tree", None) if scene.use_nodes else None


def get_output_role(file_output):
    text = " ".join(
        str(value)
        for value in (
            getattr(file_output, "name", ""),
            getattr(file_output, "label", ""),
            getattr(file_output, "file_name", ""),
            getattr(file_output, "base_path", ""),
        )
    ).lower()

    if "beauty" in text:
        return "beauty"
    if "utility" in text:
        return "utility"
    return None


def update_ateru_output_paths():
    render_out_path, blend_filename = get_ateru_render_path()
    changed = False

    for scene in bpy.data.scenes:
        changed |= set_if_different(
            scene.render,
            "filepath",
            os.path.join(render_out_path, "_main_render_preview", blend_filename + "."),
        )

        tree = get_compositor_tree(scene)
        if not tree:
            continue

        for node in tree.nodes:
            if node.bl_idname != "CompositorNodeOutputFile":
                continue

            output_role = get_output_role(node)
            if output_role not in {"beauty", "utility"}:
                continue

            changed |= configure_output_path(
                node,
                render_out_path,
                build_render_filename(blend_filename, output_role),
            )

    return changed


@persistent
def ateru_update_paths_on_save_pre(_dummy):
    update_ateru_output_paths()


@persistent
def ateru_update_paths_on_save_post(_dummy):
    global _ATERU_RESAVING

    if _ATERU_RESAVING:
        return

    changed = update_ateru_output_paths()
    if not changed or not bpy.data.filepath:
        return

    _ATERU_RESAVING = True
    try:
        bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
    finally:
        _ATERU_RESAVING = False


def remove_ateru_handlers():
    for handler_list in (bpy.app.handlers.save_pre, bpy.app.handlers.save_post):
        for handler in list(handler_list):
            if getattr(handler, "__name__", "") in {
                "ateru_update_paths_on_save_pre",
                "ateru_update_paths_on_save_post",
            }:
                handler_list.remove(handler)


def register_ateru_handlers():
    remove_ateru_handlers()
    bpy.app.handlers.save_pre.append(ateru_update_paths_on_save_pre)
    bpy.app.handlers.save_post.append(ateru_update_paths_on_save_post)


def setup_compositing_tree(view_layer_names):
    scene = bpy.context.scene
    scene.use_nodes = True

    bpy.context.view_layer.update()

    # Retorna la ruta del directorio y el nombre limpio del archivo actual
    render_out_path, blend_filename = get_ateru_render_path()
    scene.render.filepath = os.path.join(
        render_out_path, "_main_render_preview", blend_filename + "."
    )

    if hasattr(scene, "compositing_node_group"):
        scene.render.use_compositing = True
        if scene.compositing_node_group is None:
            scene.compositing_node_group = bpy.data.node_groups.new(
                name="Pipeline Nodetree", type="CompositorNodeTree"
            )
        tree = scene.compositing_node_group
    else:
        tree = scene.node_tree

    tree.nodes.clear()

    utility_passes = {
        "Depth": ("Depth", "FLOAT"),
        "Mist": ("Mist", "FLOAT"),
        "Vector": ("Vector", "VECTOR"),
        "UV": ("UV", "VECTOR"),
        "Position": ("Position", "VECTOR"),
        "Normal": ("Normal", "VECTOR"),
        "Diffuse Direct": ("Diff_Dir", "RGBA"),
        "Diffuse Indirect": ("Diff_Ind", "RGBA"),
        "Diffuse Color": ("Diff_Color", "RGBA"),
        "Glossy Direct": ("Gloss_Dir", "RGBA"),
        "Glossy Indirect": ("Gloss_Ind", "RGBA"),
        "Glossy Color": ("Gloss_Color", "RGBA"),
        "Transmission Direct": ("Trans_Dir", "RGBA"),
        "Transmission Indirect": ("Trans_Ind", "RGBA"),
        "Transmission Color": ("Trans_Color", "RGBA"),
        "Emission": ("Emission", "RGBA"),
        "Environment": ("Environment", "RGBA"),
        "Ambient Occlusion": ("AO", "FLOAT"),
        "Denoising Albedo": ("Denoising_Albedo", "RGBA"),
        "Denoising Normal": ("Denoising_Normal", "VECTOR"),
        "Denoising Depth": ("Denoising_Depth", "FLOAT"),
    }

    beauty_output = create_multilayer_output(
        tree,
        render_out_path,
        build_render_filename(blend_filename, "beauty"),
        (1500, 300),
        "beauty",
    )
    utility_output = create_multilayer_output(
        tree,
        render_out_path,
        build_render_filename(blend_filename, "utility"),
        (1500, -650),
        "utility",
    )

    y_offset = 0

    for vl_name in view_layer_names:
        rl_node = tree.nodes.new("CompositorNodeRLayers")
        rl_node.layer = vl_name
        rl_node.location = (0, y_offset)

        rl_node.update()

        main_denoise = tree.nodes.new("CompositorNodeDenoise")
        main_denoise.location = (400, y_offset)

        if "Image" in rl_node.outputs:
            tree.links.new(rl_node.outputs["Image"], main_denoise.inputs["Image"])
        if "Denoising Normal" in rl_node.outputs:
            tree.links.new(
                rl_node.outputs["Denoising Normal"], main_denoise.inputs["Normal"]
            )
        if "Denoising Albedo" in rl_node.outputs:
            tree.links.new(
                rl_node.outputs["Denoising Albedo"], main_denoise.inputs["Albedo"]
            )

        if is_utility_view_layer(vl_name):
            # 1. Utility: pases técnicos y componentes.
            for pass_socket, (suffix, s_type) in utility_passes.items():
                if pass_socket in rl_node.outputs:
                    slot_name = f"{vl_name}_{suffix}"
                    add_file_slot(utility_output, slot_name, s_type)

                    target_socket = utility_output.inputs.get(slot_name)
                    if target_socket:
                        tree.links.new(rl_node.outputs[pass_socket], target_socket)

            # 2. Utility: Cryptomattes.
            for out in rl_node.outputs:
                if out.name.startswith("Crypto"):
                    slot_name = f"{vl_name}_{out.name}"
                    add_file_slot(utility_output, slot_name, "RGBA")
                    target_socket = utility_output.inputs.get(slot_name)
                    if target_socket:
                        tree.links.new(out, target_socket)
        else:
            # 1. Beauty: imagen final, alpha y Light Groups.
            if "Image" in rl_node.outputs:
                slot_name = f"{vl_name}_Beauty_Denoised"
                add_file_slot(beauty_output, slot_name, "RGBA")
                target_socket = beauty_output.inputs.get(slot_name)
                if target_socket:
                    tree.links.new(main_denoise.outputs["Image"], target_socket)

            if "Alpha" in rl_node.outputs:
                slot_name = f"{vl_name}_Alpha"
                add_file_slot(beauty_output, slot_name, "FLOAT")
                target_socket = beauty_output.inputs.get(slot_name)
                if target_socket:
                    tree.links.new(rl_node.outputs["Alpha"], target_socket)

            lg_y_offset = y_offset - 300
            for lg_name in LIGHT_GROUPS:
                src_socket = get_light_group_socket(rl_node.outputs, lg_name)

                if src_socket:
                    slot_name = f"{vl_name}_Lgt_{lg_name}"
                    add_file_slot(beauty_output, slot_name, "RGBA")

                    target_socket = beauty_output.inputs.get(slot_name)

                    if target_socket:
                        lg_denoise = tree.nodes.new("CompositorNodeDenoise")
                        lg_denoise.location = (400, lg_y_offset)
                        lg_denoise.label = f"Denoise {lg_name}"

                        tree.links.new(src_socket, lg_denoise.inputs["Image"])

                        if "Denoising Normal" in rl_node.outputs:
                            tree.links.new(
                                rl_node.outputs["Denoising Normal"],
                                lg_denoise.inputs["Normal"],
                            )
                        if "Denoising Albedo" in rl_node.outputs:
                            tree.links.new(
                                rl_node.outputs["Denoising Albedo"],
                                lg_denoise.inputs["Albedo"],
                            )

                        tree.links.new(lg_denoise.outputs["Image"], target_socket)
                        lg_y_offset -= 160

        y_offset -= 2500


# =============================================================================
# OPERADORES Y UI
# =============================================================================


class PIPELINE_OT_SetupFullCG(bpy.types.Operator):
    bl_idname = "pipeline.setup_full_cg"
    bl_label = "Setup Full CG Scene"

    def execute(self, context):
        setup_render_engine()
        passes = [
            "fgPass",
            "bgPass",
            "envPass",
            "characterPass",
            "propPass",
            "effectPass",
            "utilityPass",
        ]
        for p in passes:
            create_collection(p)
            setup_view_layer(p, p, passes)

        if "fgPass" in context.scene.view_layers:
            context.window.view_layer = context.scene.view_layers["fgPass"]

        setup_compositing_tree(passes)
        return {"FINISHED"}


class PIPELINE_OT_SetupBeautyUtility(bpy.types.Operator):
    bl_idname = "pipeline.setup_beauty_utility"
    bl_label = "Setup Beauty + Utility"

    def execute(self, context):
        setup_render_engine()
        passes = ["beautyPass", "utilityPass"]
        for p in passes:
            create_collection(p)
            setup_view_layer(p, p, passes)

        if "beautyPass" in context.scene.view_layers:
            context.window.view_layer = context.scene.view_layers["beautyPass"]

        setup_compositing_tree(passes)
        return {"FINISHED"}


class PIPELINE_OT_SetupEnvironment(bpy.types.Operator):
    bl_idname = "pipeline.setup_environment"
    bl_label = "Setup Environment Only"

    def execute(self, context):
        setup_render_engine()
        passes = ["envPass", "utilityPass"]
        for p in passes:
            create_collection(p)
            setup_view_layer(p, p, passes)

        if "envPass" in context.scene.view_layers:
            context.window.view_layer = context.scene.view_layers["envPass"]

        setup_compositing_tree(passes)
        return {"FINISHED"}


class PIPELINE_OT_SetupCharacter(bpy.types.Operator):
    bl_idname = "pipeline.setup_character"
    bl_label = "Setup Character Only"

    def execute(self, context):
        setup_render_engine()
        passes = ["characterPass", "utilityPass"]
        for p in passes:
            create_collection(p)
            setup_view_layer(p, p, passes)

        if "characterPass" in context.scene.view_layers:
            context.window.view_layer = context.scene.view_layers["characterPass"]

        setup_compositing_tree(passes)
        return {"FINISHED"}


class PIPELINE_OT_SetupLookDev(bpy.types.Operator):
    bl_idname = "pipeline.setup_lookdev"
    bl_label = "Setup LookDev Asset"

    def execute(self, context):
        setup_render_engine()
        ld_col = create_collection("LookDev_Environment")
        create_collection("lookdevAsset")
        create_collection("macbethChart", ld_col)
        create_collection("lightRig", ld_col)
        passes = ["lookdevAsset", "LookDev_Environment"]
        setup_view_layer("lookdevPass", "lookdevAsset", passes)

        if "lookdevPass" in context.scene.view_layers:
            context.window.view_layer = context.scene.view_layers["lookdevPass"]

        setup_compositing_tree(["lookdevPass"])
        return {"FINISHED"}


class PIPELINE_PT_Panel(bpy.types.Panel):
    bl_label = "Ateru Pipeline Tools"
    bl_idname = "PIPELINE_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Ateru"

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label(text="Automated Passes & Lgt Groups", icon="LIGHT")
        box.label(text="Auto-Paths (EXR Multilayer)", icon="FILE_FOLDER")

        col = layout.column(align=True)
        col.operator("pipeline.setup_full_cg", text="Full CG Scene", icon="SCENE_DATA")
        col.operator(
            "pipeline.setup_beauty_utility",
            text="Beauty + Utility",
            icon="RENDER_RESULT",
        )
        col.operator(
            "pipeline.setup_environment", text="Environment", icon="WORLD_DATA"
        )
        col.operator(
            "pipeline.setup_character", text="Character", icon="OUTLINER_OB_ARMATURE"
        )
        col.operator("pipeline.setup_lookdev", text="LookDev", icon="SHADING_RENDERED")


classes = (
    PIPELINE_OT_SetupFullCG,
    PIPELINE_OT_SetupBeautyUtility,
    PIPELINE_OT_SetupEnvironment,
    PIPELINE_OT_SetupCharacter,
    PIPELINE_OT_SetupLookDev,
    PIPELINE_PT_Panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    register_ateru_handlers()


def unregister():
    remove_ateru_handlers()
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
