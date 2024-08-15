from time import sleep
from utils.brick import (
    EV3UltrasonicSensor,
    wait_ready_sensors,
    EV3ColorSensor,
    reset_brick,
    Motor,
    EV3GyroSensor,

)

left_motor = Motor("D")
right_motor = Motor("B")
catapult = Motor("A")
loader = Motor("C")
US_SENSOR_FRONT = EV3UltrasonicSensor(1)
COLOR_SENSOR = EV3ColorSensor(2)
GYRO = EV3GyroSensor(4)
print("Program start.\nWaiting for sensors to turn on...")

wait_ready_sensors(True)  # Wait until all sensors are ready to be used
print("Done waiting.")

#left tunnel(left wheel 15, right wheel 15)
#right tunnel(bearings and wheels centered)
def main():
    try:
        # section_A()
        # print("A Done")
        # left_tunnel = section_B()
        # print("B Done")
        # section_C()
        # print("C Done")
        # section_D()
        # print("D Done")
        # section_E(left_tunnel)
        # print("E Done")
        # section_F(left_tunnel)
        # print("F Done")
        launch()

    except Exception as e:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        print(e)
    finally:
        print("finally")
        left_motor.set_dps(0)
        right_motor.set_dps(0)
        catapult.set_dps(0)
        loader.set_dps(0)
        reset_brick()  # Turn off everything on the brick's hardware, and reset it
        exit()


def section_A():
    left_motor.set_dps(-60)
    right_motor.set_dps(-200)
    sleep(2.8)
    left_motor.set_dps(-200)
    right_motor.set_dps(-206)
    sleep(1)
    rotate_to_n_degrees_right(89)
    # now in centered, facing tunnel, position lane closest to wall
    sleep(0.5)
    advance_n_blocks_gyro(3, 30, 5)


def section_B():  # complete
    left_tunnel = False
    left_motor.set_dps(250)
    right_motor.set_dps(250)
    sleep(1.75)
    left_motor.set_dps(0)
    right_motor.set_dps(0)
    print("Starting Section B")
    us_front_data = US_SENSOR_FRONT.get_value()
    while US_SENSOR_FRONT.get_value() is None or us_front_data == 0 or us_front_data > 50:
        print(us_front_data)
        us_front_data = US_SENSOR_FRONT.get_value()
    print(us_front_data)
    sleep(1)
    if us_front_data < 30:
        print("go into left tunnel")
        left_tunnel = True
        left_motor.set_dps(-250)
        right_motor.set_dps(-250)
        sleep(2)
        left_motor.set_dps(0)
        right_motor.set_dps(0)
        rotate_to_n_degrees_left(0)
        left_motor.set_dps(250)
        right_motor.set_dps(250)
        sleep(3.3)
        left_motor.set_dps(0)
        right_motor.set_dps(0)
        rotate_to_n_degrees_right(90)
        advance_in_tunnel(90)
        sleep(1)
        left_motor.set_dps(-200)
        right_motor.set_dps(-200)
        sleep(1)
        rotate_to_n_degrees_right(181)
        sleep(1)
    else:
        print("go into right tunnel")
        advance_in_tunnel(89)
        sleep(1)
        catapult.set_dps(300)
        catapult.set_position_relative(-90)
        sleep(0.5)
        left_motor.set_dps(-150)
        right_motor.set_dps(-300)
        sleep(2.3)
        rotate_to_n_degrees_right(182)
        catapult.set_dps(90)
        catapult.set_position_relative(90)
    return left_tunnel


def section_C():  # Complete
    reverse_to_red(182)
    sleep(1)
    catapult.set_dps(500)
    catapult.set_position_relative(-20)
    sleep(0.3)
    catapult.set_position_relative(20)
    sleep(0.3)


def section_D():  # Requires adjustment of advance_n_blocks then try running from inside loading zone
    while True:
        us_front_data = US_SENSOR_FRONT.get_value()
        if us_front_data is not None:
            if us_front_data < 5:
                print("Done loading")
                break
    sleep(1)
    rotate_to_n_degrees_left(178)
    advance_till_wall(178)


def section_E(left_tunnel):  # 2nd pass through tunnel
    rotate_to_n_degrees_right(360)
    if left_tunnel:
        left_motor.set_dps(250)
        right_motor.set_dps(257)
        sleep(1.9)
        rotate_to_n_degrees_left(265)
    else:
        left_motor.set_dps(-250)
        right_motor.set_dps(-257)
        sleep(1.3)
        rotate_to_n_degrees_left(268)


def section_F(left_tunnel):  # Requires adjustment of reverse_n_blocks
    # Try running from tunnel --> launch zone
    if left_tunnel:
        advance_to_red(265)
        # left_motor.set_dps(-100)
        # right_motor.set_dps(-200)
        # sleep(3)
        # left_motor.set_dps(0)
        # right_motor.set_dps(0)
        # rotate_to_n_degrees_left(260)
        # advance_to_red(260)

    else:
        advance_to_red(270)
        left_motor.set_dps(-200)
        right_motor.set_dps(-180)
        sleep(5)
        left_motor.set_dps(0)
        right_motor.set_dps(0)
        rotate_to_n_degrees_right(290)
        advance_to_red(290)

def reverse_to_red(target_angle):
    while target_angle is None:
        target_angle = GYRO.get_abs_measure()
    COLOR_SENSOR.set_mode("id")
    while True:
        gyro_data = GYRO.get_abs_measure()
        cs_data = COLOR_SENSOR.get_value()
        print(target_angle, gyro_data, cs_data)
        if gyro_data < target_angle - 5:
            print("hard turn left")
            rotate_to_n_degrees_left(target_angle)
        elif gyro_data > target_angle + 5:
            print("hard turn right")
            rotate_to_n_degrees_right(target_angle)
        elif gyro_data < target_angle:
            print("turn right")
            left_motor.set_dps(-475)
            right_motor.set_dps(-500)
        elif gyro_data > target_angle:
            print("turn left")
            left_motor.set_dps(-500)
            right_motor.set_dps(-475)
        else:
            print("straight")
            left_motor.set_dps(-500)
            right_motor.set_dps(-507)
        if cs_data == 5:
            break
    print("Done")
    sleep(0.1)
    left_motor.set_dps(0)
    right_motor.set_dps(0)


def advance_to_red(target_angle):
    while target_angle is None:
        target_angle = GYRO.get_abs_measure()
    COLOR_SENSOR.set_mode("id")
    while True:
        gyro_data = GYRO.get_abs_measure()
        cs_data = COLOR_SENSOR.get_value()
        print(target_angle, gyro_data, cs_data)
        if gyro_data < target_angle - 5:
            print("hard turn right")
            rotate_to_n_degrees_right(target_angle)
        elif gyro_data > target_angle + 5:
            print("hard turn left")
            rotate_to_n_degrees_left(target_angle)
        elif gyro_data < target_angle:
            print("turn left")
            left_motor.set_dps(450)
            right_motor.set_dps(425)
        elif gyro_data > target_angle:
            print("turn right")
            left_motor.set_dps(425)
            right_motor.set_dps(450)
        else:
            print("straight")
            left_motor.set_dps(450)
            right_motor.set_dps(457)
        if cs_data == 5:
            break
    print("Done")
    left_motor.set_dps(0)
    right_motor.set_dps(0)


def advance_in_tunnel(initial):  # NEED to fix (how robot behaves inside the tunnel)
    while True:  # movement for tunnel
        gyro_data = GYRO.get_abs_measure()
        cs_data = COLOR_SENSOR.get_red()
        us_data = US_SENSOR_FRONT.get_value()
        print(gyro_data)
        if gyro_data < initial - 3:
            print("hard turn right")
            rotate_to_n_degrees_right(initial)
        elif gyro_data > initial + 3:
            print("hard turn left")
            rotate_to_n_degrees_left(initial)
        elif gyro_data < initial:
            print("turn left")
            left_motor.set_dps(450)
            right_motor.set_dps(425)
        elif gyro_data > initial:
            print("turn right")
            left_motor.set_dps(425)
            right_motor.set_dps(450)
        else:
            print("straight")
            left_motor.set_dps(450)
            right_motor.set_dps(458)
        if us_data is not None and us_data > 0:
            print(us_data)
            if us_data < 20:
                if cs_data is not None and cs_data > 5:
                    print(cs_data)
                    if cs_data < 30:
                        print("Stop")
                        left_motor.set_dps(0)
                        right_motor.set_dps(0)
                        sleep(1)
                        break


def advance_n_blocks_gyro(n, line_color, min_color):  # Complete
    blocks_moved = 0
    target_angle = GYRO.get_abs_measure()
    left_motor.set_dps(100)
    right_motor.set_dps(100)
    sleep(0.1)
    while True:
        gyro_data = GYRO.get_abs_measure()
        us_front_data = US_SENSOR_FRONT.get_value()
        cs_data = COLOR_SENSOR.get_red()
        if blocks_moved < n:
            print(target_angle, gyro_data, cs_data)
            if cs_data is not None:
                if cs_data > min_color and cs_data < line_color:
                    blocks_moved += 1
                    sleep(0.1)
            if gyro_data < target_angle - 3:
                print("hard turn right")
                rotate_to_n_degrees_right(target_angle)
            elif gyro_data > target_angle + 3:
                print("hard turn left")
                rotate_to_n_degrees_left(target_angle)
            elif gyro_data < target_angle:
                print("turn left")
                left_motor.set_dps(350)
                right_motor.set_dps(325)
            elif gyro_data > target_angle:
                print("turn right")
                left_motor.set_dps(325)
                right_motor.set_dps(350)
            else:
                print("straight")
                left_motor.set_dps(350)
                right_motor.set_dps(350)
            if 0 < us_front_data < 15:
                print("Obstacle detected")
                left_motor.set_dps(0)
                right_motor.set_dps(0)
                break
        else:
            print(f"stop, moved {blocks_moved} blocks.")
            sleep(0.05)
            left_motor.set_dps(0)
            right_motor.set_dps(0)
            break


def advance_till_wall(target_angle):
    right_motor.set_dps(100)
    left_motor.set_dps(100)
    sleep(1)
    while True:
        gyro_data = GYRO.get_abs_measure()
        us_front_data = US_SENSOR_FRONT.get_value()
        print(target_angle, gyro_data, us_front_data)
        if gyro_data < target_angle:
            print("turn left")
            left_motor.set_dps(500)
            right_motor.set_dps(450)
        elif gyro_data > target_angle:
            print("turn right")
            left_motor.set_dps(450)
            right_motor.set_dps(500)
        else:
            print("straight")
            left_motor.set_dps(500)
            right_motor.set_dps(507)
        if 0 < us_front_data < 20:
            print("Obstacle detected")
            left_motor.set_dps(0)
            right_motor.set_dps(0)
            break
    left_motor.set_dps(0)
    right_motor.set_dps(0)


def rotate_to_n_degrees_left(n):  # complete
    current = GYRO.get_abs_measure()
    left_motor.set_dps(-200)
    right_motor.set_dps(200)
    while current != n:
        if abs(n - current) < 10:
            left_motor.set_dps(-30)
            right_motor.set_dps(30)
        elif current < n + 2:
            print("fixing right")
            rotate_to_n_degrees_right(n)
        print(current)
        current = GYRO.get_abs_measure()
    left_motor.set_dps(0)
    right_motor.set_dps(0)
    current = GYRO.get_abs_measure()

    print(current)


def rotate_to_n_degrees_right(n):  # complete
    current = GYRO.get_abs_measure()
    left_motor.set_dps(200)
    right_motor.set_dps(-200)
    while current != n:
        if abs(n - current) < 10:
            left_motor.set_dps(30)
            right_motor.set_dps(-30)
        elif current > n + 2:
            print("fixing left")
            rotate_to_n_degrees_left(n)
        print(current)
        current = GYRO.get_abs_measure()
    left_motor.set_dps(0)
    right_motor.set_dps(0)
    current = GYRO.get_abs_measure()
    print(current, "complete")

def launch():
    left_motor.set_dps(-100)
    right_motor.set_dps(-100)
    sleep(1.5)
    left_motor.set_dps(0)
    right_motor.set_dps(0)
    rotate_to_n_degrees_left(181)

    # adjust wall distance
    wall_distance = 35.7

    # for 3: 1000dps 130angle
    # for 2: 400dps 100angle
    # for 1: 200 110angle


    for i in range(15):
        if i>0 and i%3:
            left_motor.set_dps(100)
            right_motor.set_dps(100)
            sleep(1)
            left_motor.set_dps(0)
            right_motor.set_dps(0)
        current_distance = US_SENSOR_FRONT.get_value()
        while not(wall_distance-0.5<current_distance < wall_distance+0.5):
            current_distance = US_SENSOR_FRONT.get_value()
            print("current distance:", current_distance)
            if 0<(current_distance-wall_distance)<4:
                left_motor.set_dps(-50)
                right_motor.set_dps(-50)
                print("minor front")
            elif 0<(current_distance-wall_distance)<-4:
                left_motor.set_dps(50)
                right_motor.set_dps(50)
                print("minor backward")
            elif current_distance<wall_distance:
                left_motor.set_dps(-200)
                right_motor.set_dps(-200)
            elif current_distance>wall_distance:
                left_motor.set_dps(200)
                right_motor.set_dps(200)
        left_motor.set_dps(0)
        right_motor.set_dps(0)
        sleep(1)
        print(i)
        loader.set_dps(1000)
        loader.set_position_relative(-45)
        sleep(0.30)
        loader.set_position_relative(45)
        sleep(1)
        if i == 0:
            dpsValue = 200
            angleValue = 110
        elif i == 1:
            dpsValue = 400
            angleValue = 100
        else:
            dpsValue = 500
            angleValue = 130
        if i > 0 and i % 2:
            rotate_to_n_degrees_right(GYRO.get_abs_measure() + 1)
        catapult.set_dps(dpsValue)
        catapult.set_position_relative(-angleValue)
        sleep(1)
        catapult.set_dps(25)
        catapult.set_limits(25)
        catapult.set_position_relative(angleValue)
        sleep(1.5)



if __name__ == "__main__":
    main()
