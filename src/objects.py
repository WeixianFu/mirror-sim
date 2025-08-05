import bpy
import mathutils

class Vehicle:
    def __init__(self, model_path:str, location=(0, 0, 0), attach_point=(-3.5, 0, 0.5)):
        """
        Initializes the Vehicle object with a model path and location and trailer/caravan attach point.
        """
        self.obj = self._import_model(model_path)
        self.set_location(location)
        self.attach_point = mathutils.Vector(attach_point)
        # Set the vehicle's orientation vectors
        # Forward direction is assumed to be along the negative X-axis, Right direction is along the negative Y-axis, and Up direction is along the Z-axis
        # These can be adjusted based on the model's orientation.
        self.forward_dir = mathutils.Vector((-1, 0, 0))
        self.right_dir   = mathutils.Vector((0, -1, 0))
        self.up_dir      = mathutils.Vector((0, 0, 1))
        # Set the vehicle's location. The location is set to the specified location parameter
        bpy.context.view_layer.update()

    def _import_model(self, model_path:str):
        """
        Imports the vehicle model from the specified path.
        """
        if model_path.lower().endswith('.obj'):
            bpy.ops.wm.obj_import(filepath=model_path)
        elif model_path.lower().endswith('.fbx'):
            bpy.ops.import_scene.fbx(filepath=model_path)
        else:
            raise ValueError("Unsupported model format for {model_path}. Please use .obj or .fbx files.")
        # Get the imported object
        imported_objs = [obj for obj in bpy.context.selected_objects]
        vehicle_obj = imported_objs[0] if imported_objs else None
        if vehicle_obj:
            vehicle_obj.name = "Vehicle"
            return vehicle_obj
    
    def set_location(self, location:tuple):
        """
        Sets the location of the vehicle.
        """
        if isinstance(location, (tuple, list)) and len(location) == 3:
            self.obj.location = location
        else:
            raise ValueError("Location must be a tuple or list with three elements (x, y, z).")

    def get_world_location(self, local_point:mathutils.Vector) -> mathutils.Vector:
        """
        Returns the world location of the vehicle.
        """
        vehicle_obj = bpy.data.objects.get("Vehicle")
        if vehicle_obj:
            return vehicle_obj.matrix_world.translation
        return None
if __name__ == "__main__":
    # Example usage
    import sys, os
    # Ensure the script can find the utils module
    this_dir = os.path.dirname(__file__)
    if this_dir not in sys.path:
        sys.path.append(this_dir)

    from untils import clear_scene    
    clear_scene()   

    vehicle = Vehicle(model_path="C:\Datas\\trailer_mirror\mirror_sim\models\\vehicles\GLS580\GLS580.obj", location=(0, 0, 0), attach_point=(-3.5, 0, 0.5))
    print("Vehicle world location:", vehicle.get_world_location(mathutils.Vector((0, 0, 0))))