"""
Bible Keyring 3D Model Generator for Blender
=============================================
Creates a mini bible book keyring with:
- Book body with rounded spine
- "I AM WHO I AM" embossed text on front cover
- Carabiner loop on spine for attachment
- Page-like detail lines on top/bottom edges

Usage: Open in Blender's Scripting tab and run, or paste into the Python console.
Target file: nfc-bible.blend
"""

import bpy
import bmesh
import math
from mathutils import Vector

# ============================================================
# CONFIGURATION - Adjust these values as needed
# ============================================================
BOOK_WIDTH = 30.0    # mm (X) - front to back
BOOK_HEIGHT = 38.0   # mm (Z) - top to bottom
BOOK_DEPTH = 10.0    # mm (Y) - spine thickness
COVER_THICKNESS = 1.5  # mm
SPINE_RADIUS = 5.0   # mm - radius of the rounded spine

# Carabiner loop
LOOP_OUTER_RADIUS = 4.0   # mm
LOOP_INNER_RADIUS = 2.5   # mm (hole for carabiner)
LOOP_THICKNESS = 3.0       # mm
LOOP_OFFSET_Z = 0.0        # centered on spine top

# Text
TEXT_CONTENT = "I AM\nWHO\nI AM"
TEXT_SIZE = 5.0       # mm
TEXT_EXTRUDE = 0.8    # mm - emboss depth (negative = engraved)
TEXT_FONT = None      # Uses Blender default font

# Page lines
PAGE_LINE_COUNT = 12
PAGE_LINE_DEPTH = 0.3  # mm

COLLECTION_NAME = "BibleKeyring"


def cleanup_existing():
    """Remove existing BibleKeyring collection if present."""
    if COLLECTION_NAME in bpy.data.collections:
        col = bpy.data.collections[COLLECTION_NAME]
        for obj in list(col.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(col)


def create_collection():
    """Create a new collection for the keyring."""
    col = bpy.data.collections.new(COLLECTION_NAME)
    bpy.context.scene.collection.children.link(col)
    return col


def set_active(obj):
    """Set object as active and selected."""
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def create_book_body(collection):
    """
    Create the main book body:
    - Rectangular body for the covers and pages
    - Rounded spine on the left side (negative X)
    """
    # Create main rectangular body
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(BOOK_WIDTH / 2, 0, 0)
    )
    body = bpy.context.active_object
    body.name = "BookBody"
    body.scale = (BOOK_WIDTH, BOOK_DEPTH, BOOK_HEIGHT)
    bpy.ops.object.transform_apply(scale=True)

    # Move to collection
    for c in body.users_collection:
        c.objects.unlink(body)
    collection.objects.link(body)

    return body


def create_spine(collection):
    """
    Create a rounded spine cylinder on the left side of the book.
    """
    # Create a cylinder for the spine
    bpy.ops.mesh.primitive_cylinder_add(
        radius=BOOK_DEPTH / 2,
        depth=BOOK_HEIGHT,
        vertices=32,
        location=(0, 0, 0),
        rotation=(0, 0, 0)
    )
    spine = bpy.context.active_object
    spine.name = "BookSpine"
    spine.rotation_euler = (math.radians(90), 0, 0)

    # Rotate so it's vertical (along Z)
    # Actually cylinder default is along Z, we want it along Z too
    spine.rotation_euler = (0, 0, 0)

    bpy.ops.object.transform_apply(rotation=True)

    # Move to collection
    for c in spine.users_collection:
        c.objects.unlink(spine)
    collection.objects.link(spine)

    return spine


def create_carabiner_loop(collection):
    """
    Create a loop/ring on top of the spine for carabiner attachment.
    """
    # Create torus-like loop using a cylinder with hole
    # Outer ring
    bpy.ops.mesh.primitive_cylinder_add(
        radius=LOOP_OUTER_RADIUS,
        depth=LOOP_THICKNESS,
        vertices=32,
        location=(0, 0, BOOK_HEIGHT / 2 + LOOP_OUTER_RADIUS - 1.0)
    )
    loop_outer = bpy.context.active_object
    loop_outer.name = "LoopOuter"
    bpy.ops.object.transform_apply(location=True)

    # Move to collection
    for c in loop_outer.users_collection:
        c.objects.unlink(loop_outer)
    collection.objects.link(loop_outer)

    # Inner hole (to be subtracted)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=LOOP_INNER_RADIUS,
        depth=LOOP_THICKNESS + 2,
        vertices=32,
        location=(0, 0, BOOK_HEIGHT / 2 + LOOP_OUTER_RADIUS - 1.0)
    )
    loop_inner = bpy.context.active_object
    loop_inner.name = "LoopInner"
    bpy.ops.object.transform_apply(location=True)

    # Move to collection
    for c in loop_inner.users_collection:
        c.objects.unlink(loop_inner)
    collection.objects.link(loop_inner)

    # Boolean difference to create the hole
    set_active(loop_outer)
    bool_mod = loop_outer.modifiers.new(name="LoopHole", type='BOOLEAN')
    bool_mod.operation = 'DIFFERENCE'
    bool_mod.object = loop_inner
    bool_mod.solver = 'FAST'
    bpy.ops.object.modifier_apply(modifier="LoopHole")

    # Remove the inner cylinder
    bpy.data.objects.remove(loop_inner, do_unlink=True)

    return loop_outer


def create_embossed_text(collection):
    """
    Create the 'I AM WHO I AM' text on the front cover.
    Uses separate text lines for proper layout.
    """
    lines = ["I AM", "WHO", "I AM"]
    line_spacing = TEXT_SIZE * 1.6
    total_height = (len(lines) - 1) * line_spacing
    start_z = total_height / 2

    text_objects = []

    for i, line in enumerate(lines):
        bpy.ops.object.text_add(
            location=(
                BOOK_WIDTH / 2,       # Center on front cover X
                -BOOK_DEPTH / 2 - TEXT_EXTRUDE / 2 + 0.01,  # On front face
                start_z - i * line_spacing  # Vertical position
            )
        )
        txt = bpy.context.active_object
        txt.name = f"Text_{line.replace(' ', '_')}"
        txt.data.body = line
        txt.data.size = TEXT_SIZE
        txt.data.extrude = TEXT_EXTRUDE
        txt.data.align_x = 'CENTER'
        txt.data.align_y = 'CENTER'

        # Rotate to face front (negative Y)
        txt.rotation_euler = (math.radians(90), 0, 0)

        # Use a bold font if available
        txt.data.font = bpy.data.fonts.get("Bfont Regular") or bpy.data.fonts[0]

        # Convert to mesh for boolean operations
        set_active(txt)
        bpy.ops.object.convert(target='MESH')

        # Move to collection
        for c in txt.users_collection:
            c.objects.unlink(txt)
        collection.objects.link(txt)

        text_objects.append(txt)

    # Join all text objects
    if len(text_objects) > 1:
        set_active(text_objects[0])
        for t in text_objects[1:]:
            t.select_set(True)
        bpy.ops.object.join()

    text_combined = bpy.context.active_object
    text_combined.name = "EmbossedText"
    return text_combined


def create_page_lines(collection):
    """
    Create horizontal lines on the page edges (top and bottom)
    to simulate stacked pages.
    """
    page_objects = []

    # Pages are visible on the right side (positive X) between covers
    # and on top/bottom edges
    inner_depth = BOOK_DEPTH - 2 * COVER_THICKNESS
    line_spacing = inner_depth / (PAGE_LINE_COUNT + 1)

    for i in range(PAGE_LINE_COUNT):
        y_pos = -BOOK_DEPTH / 2 + COVER_THICKNESS + (i + 1) * line_spacing

        # Create a thin box for each page line on the right edge (open side)
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(BOOK_WIDTH + 0.01, y_pos, 0)
        )
        line = bpy.context.active_object
        line.name = f"PageLine_{i}"
        line.scale = (PAGE_LINE_DEPTH, 0.15, BOOK_HEIGHT * 0.9)
        bpy.ops.object.transform_apply(scale=True)

        for c in line.users_collection:
            c.objects.unlink(line)
        collection.objects.link(line)
        page_objects.append(line)

    # Join all page lines
    if page_objects:
        set_active(page_objects[0])
        for p in page_objects[1:]:
            p.select_set(True)
        bpy.ops.object.join()

        result = bpy.context.active_object
        result.name = "PageLines"
        return result
    return None


def join_all_parts(collection):
    """
    Join all parts into a single mesh for 3D printing.
    Uses boolean union to merge body, spine, loop, and text.
    """
    # Get all mesh objects in the collection
    mesh_objects = [obj for obj in collection.objects if obj.type == 'MESH']

    if len(mesh_objects) < 2:
        return mesh_objects[0] if mesh_objects else None

    # Find the main body
    main = None
    others = []
    for obj in mesh_objects:
        if obj.name == "BookBody":
            main = obj
        else:
            others.append(obj)

    if main is None:
        main = mesh_objects[0]
        others = mesh_objects[1:]

    set_active(main)

    for other in others:
        bool_mod = main.modifiers.new(name=f"Union_{other.name}", type='BOOLEAN')
        bool_mod.operation = 'UNION'
        bool_mod.object = other
        bool_mod.solver = 'FAST'

        try:
            bpy.ops.object.modifier_apply(modifier=bool_mod.name)
        except Exception as e:
            print(f"Warning: Boolean union failed for {other.name}: {e}")
            # Try removing the modifier if it failed
            if bool_mod.name in [m.name for m in main.modifiers]:
                main.modifiers.remove(bool_mod)

    # Remove the other objects after joining
    for other in others:
        try:
            bpy.data.objects.remove(other, do_unlink=True)
        except:
            pass

    main.name = "BibleKeyring"
    return main


def add_material(obj):
    """Add a dark navy blue material like in the reference image."""
    mat = bpy.data.materials.new(name="BibleNavy")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        # Dark navy blue color
        bsdf.inputs["Base Color"].default_value = (0.05, 0.08, 0.18, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.7
        bsdf.inputs["Specular IOR Level"].default_value = 0.3

    obj.data.materials.append(mat)


def main():
    """Main function to create the bible keyring."""
    print("=" * 50)
    print("Creating Bible Keyring 3D Model...")
    print("=" * 50)

    # Cleanup
    cleanup_existing()

    # Create collection
    col = create_collection()

    # Step 1: Book body
    print("[1/6] Creating book body...")
    body = create_book_body(col)

    # Step 2: Rounded spine
    print("[2/6] Creating spine...")
    spine = create_spine(col)

    # Step 3: Carabiner loop
    print("[3/6] Creating carabiner loop...")
    loop = create_carabiner_loop(col)

    # Step 4: Embossed text
    print("[4/6] Creating embossed text...")
    text = create_embossed_text(col)

    # Step 5: Page lines
    print("[5/6] Creating page detail lines...")
    pages = create_page_lines(col)

    # Step 6: Join all parts
    print("[6/6] Joining all parts...")
    final = join_all_parts(col)

    if final:
        # Add material
        add_material(final)

        # Set origin to center of mass
        set_active(final)
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')

        # Scale to mm (Blender default is meters, ensure scene unit is mm)
        # If scene is in meters, scale down
        if bpy.context.scene.unit_settings.length_unit == 'METERS':
            final.scale = (0.001, 0.001, 0.001)
            bpy.ops.object.transform_apply(scale=True)

        print(f"\n✅ Bible Keyring created successfully!")
        print(f"   Object: {final.name}")
        print(f"   Dimensions: {BOOK_WIDTH}x{BOOK_DEPTH}x{BOOK_HEIGHT} mm")
        print(f"   Carabiner hole: {LOOP_INNER_RADIUS * 2}mm diameter")
        print(f"   Location: Collection '{COLLECTION_NAME}'")
    else:
        print("❌ Error: Failed to create the keyring.")

    return final


# ============================================================
# RUN
# ============================================================
if __name__ == "__main__":
    main()
