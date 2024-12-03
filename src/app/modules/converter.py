"""
ModelConverter Class

This class is responsible for converting 3D model files (OBJ format) and their corresponding texture files into other formats (such as GLB or FBX). It processes the models by importing them into Blender, applying textures, and exporting them to the desired format.

Key Features:
- Clears the Blender scene before processing models.
- Imports OBJ files into Blender.
- Applies textures to models using Blender's material system.
- Converts the models to GLB or FBX formats.
- Handles missing files with logging.

Usage:
    converter = ModelConverter(input_downloader_dir="path/to/downloaded/files", input_cleaner_file="path/to/cleaner/data.json", output_converter_dir="path/to/output")
    converter.process()

Dependencies:
- bpy (Blender Python API)
- os
- json
- loguru
"""

import bpy
import os
import json
from loguru import logger


class ModelConverter:
    """
    A class for converting 3D models (OBJ) with textures into GLB or FBX formats using Blender.

    Attributes:
        input_downloader_dir (str): Directory where the downloaded 3D model and texture files are located.
        input_cleaner_file (str): Path to the cleaned JSON data containing model and texture information.
        output_converter_dir (str): Directory where the converted model files (GLB/FBX) will be saved.
        cleaner_file (file object): File object for the input cleaner file.
        cleaner_data (list): List of cleaned data containing model and texture details.
    """

    def __init__(
        self, input_downloader_dir: str, input_cleaner_file: str, output_converter_dir: str
    ):
        """
        Initializes the ModelConverter with input and output directories for models and textures and a cleaner file.

        Args:
            input_downloader_dir (str): Path to the directory containing downloaded model and texture files.
            input_cleaner_file (str): Path to the cleaned data file.
            output_converter_dir (str): Directory to save converted model files.
        """
        self.input_downloader_dir = input_downloader_dir
        self.input_cleaner_file = input_cleaner_file
        self.output_converter_dir = output_converter_dir

        self.cleaner_file = open(self.input_cleaner_file, "r", encoding="utf-8")
        self.cleaner_data = json.load(self.cleaner_file)

    def clear_scene(self):
        """
        Clears the Blender scene by selecting and deleting all mesh objects, and resetting the scene to its factory settings.
        """
        bpy.ops.object.select_by_type(type="MESH")
        bpy.ops.object.select_all(action="SELECT")
        bpy.ops.object.delete(use_global=False)
        bpy.ops.wm.read_factory_settings(use_empty=True)

    def import_obj(self, input_obj: str):
        """
        Imports the given OBJ file into the Blender scene.

        Args:
            input_obj (str): The file path to the OBJ file to be imported.
        """
        active_object = bpy.context.active_object
        bpy.ops.wm.obj_import(filepath=input_obj)
        bpy.context.view_layer.objects.active = active_object

    def apply_texture(self, obj: bpy.types.Object, texture_path: str):
        """
        Applies a texture to the given object in Blender.

        Args:
            obj (bpy.types.Object): The object to which the texture will be applied.
            texture_path (str): The file path to the texture image.
        """
        mat = bpy.data.materials.new(name="Material")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]

        tex_image = mat.node_tree.nodes.new("ShaderNodeTexImage")
        tex_image.image = bpy.data.images.load(filepath=texture_path)
        mat.node_tree.links.new(bsdf.inputs["Base Color"], tex_image.outputs["Color"])

        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)

    def convert_model(self, input_obj: str, input_texture: str, output_path: str):
        """
        Converts the 3D model by importing it, applying the texture, and exporting it in the desired format (GLB or FBX).

        Args:
            input_obj (str): The path to the OBJ file to be converted.
            input_texture (str): The path to the texture file to be applied to the model.
            output_path (str): The path where the converted model will be saved.
        """
        try:
            self.clear_scene()
            self.import_obj(input_obj)

            for obj in bpy.context.scene.objects:
                if obj.type == "MESH":
                    self.apply_texture(obj, input_texture)

            if output_path.endswith(".glb"):
                bpy.ops.export_scene.gltf(
                    filepath=output_path, use_selection=True, export_format="GLB"
                )
            elif output_path.endswith(".fbx"):
                bpy.ops.export_scene.fbx(
                    filepath=output_path, use_selection=True, embed_textures=True
                )

            logger.success(f"File exported to {output_path}")
        except Exception as e:
            logger.error(f"Failed to export {output_path}; Exception: {e}")

    def process(self):
        """
        Processes each row of the cleaned data to convert the associated model and texture files.

        It checks if the required files exist, and then converts the model from OBJ to GLB/FBX format.
        """
        for row in self.cleaner_data:
            model = row["model"]
            input_obj = os.path.join(self.input_downloader_dir, "obj", model["objName"])
            input_texture = os.path.join(self.input_downloader_dir, "texture", model["textureName"])
            model_name = model["objName"].replace(".obj", ".glb")
            output_path = os.path.join(self.output_converter_dir, model_name)

            if not os.path.exists(input_obj):
                logger.warning(f"Missing OBJ file: {input_obj}")
                continue
            if not os.path.exists(input_texture):
                logger.warning(f"Missing Texture file: {input_texture}")
                continue

            self.convert_model(input_obj, input_texture, output_path)


if __name__ == "__main__":
    downloader_dir = "D:/Tools/ots-crawl-3d/data/output/downloader"
    converter_dir = "D:/Tools/ots-crawl-3d/data/output/converter"
    cleaner_json_file = "D:/Tools/ots-crawl-3d/data/output/cleaner/data.json"
    os.makedirs(converter_dir, exist_ok=True)

    converter = ModelConverter(
        input_downloader_dir=downloader_dir,
        input_cleaner_file=cleaner_json_file,
        output_converter_dir=converter_dir,
    )
    converter.process()
