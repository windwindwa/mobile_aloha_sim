import omni
from pxr import Usd, UsdPhysics, PhysxSchema
from omni.isaac.dynamic_control import _dynamic_control

dc = _dynamic_control.acquire_dynamic_control_interface()
stage = omni.usd.get_context().get_stage()

candidates = []
for prim in stage.Traverse():
    if not prim.IsValid():
        continue

    # 兼容不同版本：两种常见 articulation root 标记
    is_art_root = UsdPhysics.ArticulationRootAPI(prim).GetPrim().IsValid()
    is_physx_art = PhysxSchema.PhysxArticulationAPI(prim).GetPrim().IsValid()

    if is_art_root or is_physx_art:
        path = prim.GetPath().pathString
        candidates.append(path)

print("=== Candidates (has ArticulationRootAPI / PhysxArticulationAPI) ===")
for p in candidates:
    ok = bool(dc.get_articulation(p))
    print(("OK  " if ok else "NO  "), p)

if not candidates:
    print("没找到任何 articulation root 标记。可能：机器人不是按 articulation 搭的，或还没启用物理/没被转换为 articulation。")
