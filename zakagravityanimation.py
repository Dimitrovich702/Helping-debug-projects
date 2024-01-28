import dearpygui.dearpygui as dpg
import dearpygui
import time, math, random, threading
from itertools import chain


dpg.create_context()
dpg.create_viewport(title="Satisfying circles")
dpg.setup_dearpygui()

class Circle:
    def __init__(self, radius: float, speed: float, x: float, y: float):
        self.radius = radius
        self.add_speed = speed
        self.x = x
        self.y = y
        self.x_acceleration = 0 + self.add_speed
        self.y_acceleration = 0


def start_anim(num):
    print("Start animation button pressed.")

    outradius = dpg.get_value(outside_circle_radius)
    outdiameter = outradius*2

    default_in_radius = dpg.get_value(start_circle_radius)
    in_add_speed = dpg.get_value(additional_circle_speed)
    gravity_speed = dpg.get_value(gravity)
    object_start_x = dpg.get_value(start_x)
    object_start_y = dpg.get_value(start_y)
    cillide_timeout = dpg.get_value(collide_check_timeout)

    trail_rainbow = dpg.get_value(trail_and_rainbow)
    rainbow_color_codes: list[tuple] = []
    rainbow_iteration = 0

    animation_num = num

    if trail_rainbow == 1:
        for r, g, b in zip(
                chain(reversed(range(256)), [0] * 256),
                chain(range(256), reversed(range(256))),
                chain([0] * 256, range(256))):
                    rainbow_color_codes.append((r, g, b, 255))

    with dpg.window(label=f"Animation {num}", width=outdiameter+30, height=outdiameter+30):
        #dpg.add_text(f"Circle radius = {dpg.get_value(start_circle_radius)}")
        dpg.draw_circle(center=(outradius, outradius), radius=outradius, fill=(255, 255, 255, 255), color=(255, 0, 0, 255), thickness=5)

        # Physics simulator
        pr_circle: Circle = None
        pr_drawing: dearpygui.dearpygui.get_item_slot = None
        iter_collide_check = 0
        while True:
            sleep = 0.1
            time.sleep(0.01)
            if pr_circle is not None:
                cur_circle = pr_circle
            else:
                cur_circle = Circle(default_in_radius, in_add_speed, object_start_x, object_start_y)

            if cur_circle.x_acceleration > 25:
                cur_circle.x_acceleration = 25
            elif cur_circle.x_acceleration < -25:
                cur_circle.x_acceleration = -23
            if cur_circle.y_acceleration > 25:
                cur_circle.y_acceleration = 23
            elif cur_circle.y_acceleration < -25:
                cur_circle.y_acceleration = -23

            cur_circle.y += cur_circle.y_acceleration * sleep
            cur_circle.x += cur_circle.x_acceleration * sleep
            if trail_rainbow == 1:
                if rainbow_iteration == 512: rainbow_iteration = 0
                pr_drawing = dpg.draw_circle(center=(cur_circle.x, cur_circle.y), radius=cur_circle.radius,
                                             fill=(0, 0, 0, 255), color=rainbow_color_codes[rainbow_iteration])
                rainbow_iteration += 1
            else:
                if pr_drawing is not None:
                    dpg.delete_item(pr_drawing, children_only=False, slot=dpg.get_item_slot(pr_drawing))
                pr_drawing = dpg.draw_circle(center=(cur_circle.x, cur_circle.y), radius=cur_circle.radius,
                                                fill=(0, 0, 0, 255), color=[255, 0, 0, 255])

            print(
                f"DEBUG: x: {cur_circle.x}, y: {cur_circle.y}, x_ac: {cur_circle.x_acceleration}, y_ac: {cur_circle.y_acceleration}")

            distence_beetween_centeres: float = math.sqrt((cur_circle.x - outradius)**2 + (cur_circle.y - outradius)**2)

            if distence_beetween_centeres < outradius - cur_circle.radius:
                cur_circle.y_acceleration += gravity_speed * sleep
            if iter_collide_check == 0:
                if distence_beetween_centeres >= outradius - cur_circle.radius:
                    cur_circle.x_acceleration = -cur_circle.x_acceleration
                    cur_circle.y_acceleration = -cur_circle.y_acceleration
                    cur_circle.x_acceleration = cur_circle.x_acceleration + cur_circle.add_speed if cur_circle.x_acceleration > 0 else cur_circle.x_acceleration - cur_circle.add_speed
                    cur_circle.y_acceleration = cur_circle.y_acceleration + cur_circle.add_speed if cur_circle.y_acceleration > 0 else cur_circle.y_acceleration - cur_circle.add_speed
                    iter_collide_check = cillide_timeout
            else:
                iter_collide_check -= 1
            pr_circle = cur_circle


def start_animation():
    anim_num = random.randrange(0, 999999999999)
    anim = threading.Thread(target=start_anim, args=(anim_num,))
    anim.start()

def upd_object():
    dpg.configure_item(start_x, default_value=dpg.get_value(outside_circle_radius), max_value=dpg.get_value(outside_circle_radius) * 2)
    dpg.configure_item(start_y, default_value=dpg.get_value(outside_circle_radius), max_value=dpg.get_value(outside_circle_radius) * 2)

with dpg.window(label="Satisfying options"):
    dpg.add_text("Scene settings")
    outside_circle_radius = dpg.add_slider_float(label="Scene radius", default_value=100, max_value=1000, callback=upd_object)
    dpg.add_text("Object settings")
    start_circle_radius = dpg.add_slider_float(label="Circle radius", default_value=10)
    start_x = dpg.add_slider_float(label="Start x", default_value=100, max_value=200)
    start_y = dpg.add_slider_float(label="Start y", default_value=100, max_value=200)
    trail_and_rainbow = dpg.add_checkbox(label="Leave trail & rainbow outline")
    dpg.add_text("Physics configuration")
    gravity = dpg.add_slider_float(label="gravity/s", default_value=3, max_value=23)
    additional_circle_speed = dpg.add_slider_float(label="Additional circle speed with each colliding", default_value=3, max_value=23)
    collide_check_timeout = dpg.add_slider_int(label="Colide check timeout (ticks)", default_value=3, max_value=10)
    dpg.add_button(label="Start", callback=start_animation)

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
