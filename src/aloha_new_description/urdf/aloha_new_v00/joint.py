# Isaac Sim Script Editor 直接运行
# 键位：
#   Joint1: Q/A
#   Joint2: W/S
#   Joint3: E/D
#   Joint4: R/F
#   Joint5: T/G
#   Joint6: Y/H
#   Gripper(7&8): O/L  (O开, L关)
#   Shift：加速
#   ESC：退出/停止控制（取消订阅）

import omni
import omni.appwindow
import carb
import carb.input
from omni.isaac.dynamic_control import _dynamic_control

# ====== 你只需要改这里（如果路径不同）======
ART_PATH = "/aloha_description/aloha_description/root_joint"
JOINT_NAMES = [f"fl_joint{i}" for i in range(1, 9)]
# ========================================

BASE_VEL = 0.6          # 基础速度（你嫌慢就调大）
FAST_MULT = 2.5         # Shift 加速倍数

# --- Dynamic Control ---
dc = _dynamic_control.acquire_dynamic_control_interface()
art = dc.get_articulation(ART_PATH)
if not art:
    raise RuntimeError(f"[Teleop] articulation not found: {ART_PATH}")

dc.wake_up_articulation(art)

dofs = []
for jn in JOINT_NAMES:
    dof = dc.find_articulation_dof(art, jn)
    if dof == _dynamic_control.INVALID_HANDLE:
        raise RuntimeError(f"[Teleop] DOF not found: {jn} under {ART_PATH}")
    dofs.append(dof)

print("[Teleop] OK. Found DOFs:", JOINT_NAMES)
print("[Teleop] Controls: Q/A W/S E/D R/F T/G Y/H   Gripper O/L   Shift=fast   ESC=stop")

# --- Keyboard events ---
app_window = omni.appwindow.get_default_app_window()
keyboard = app_window.get_keyboard()

pressed = set()
shift_down = False
running = True

def _key_name(key):
    # carb.input 的 key 是枚举；这里用 int 直接比对更稳
    return key

# 订阅键盘事件（必须保存句柄，不然会被 GC）
_keyboard_sub = None
_update_sub = None

def on_keyboard_event(event, *args):
    global shift_down, running, _keyboard_sub, _update_sub
    et = event.type
    key = event.input

    if et == carb.input.KeyboardEventType.KEY_PRESS:
        pressed.add(key)
        if key in (carb.input.KeyboardInput.LEFT_SHIFT, carb.input.KeyboardInput.RIGHT_SHIFT):
            shift_down = True
        if key == carb.input.KeyboardInput.ESCAPE:
            running = False

    elif et == carb.input.KeyboardEventType.KEY_RELEASE:
        if key in pressed:
            pressed.remove(key)
        if key in (carb.input.KeyboardInput.LEFT_SHIFT, carb.input.KeyboardInput.RIGHT_SHIFT):
            shift_down = False

_keyboard_sub = keyboard.subscribe_to_keyboard_events(on_keyboard_event)

# --- 每帧更新：按键->关节速度目标 ---
# 映射：每个关节一对按键（正/反）
K = carb.input.KeyboardInput
keymap = {
    0: (K.Q, K.A),
    1: (K.W, K.S),
    2: (K.E, K.D),
    3: (K.R, K.F),
    4: (K.T, K.G),
    5: (K.Y, K.H),
    6: (K.O, K.L),  # gripper joint7
    7: (K.O, K.L),  # gripper joint8
}

def on_update(e):
    global running, _keyboard_sub, _update_sub

    if not running:
        # 停止时把所有速度清零，并取消订阅
        for dof in dofs:
            dc.set_dof_velocity_target(dof, 0.0)
        print("[Teleop] Stopped.")
        if _keyboard_sub is not None:
            _keyboard_sub.unsubscribe()
        if _update_sub is not None:
            _update_sub.unsubscribe()
        return

    v = BASE_VEL * (FAST_MULT if shift_down else 1.0)

    for i, dof in enumerate(dofs):
        k_pos, k_neg = keymap[i]
        cmd = 0.0
        if k_pos in pressed: cmd += v
        if k_neg in pressed: cmd -= v
        dc.set_dof_velocity_target(dof, cmd)

# 每帧回调订阅（必须保存句柄）
_update_sub = omni.kit.app.get_app().get_update_event_stream().create_subscription_to_pop(on_update)
