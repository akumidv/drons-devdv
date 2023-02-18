from mavsdk import System
import asyncio
import random

# https://mavsdk.mavlink.io/main/en/python/quickstart.html
# https://docs.px4.io/main/en/simulation/jmavsim.html

async def fly_dron():
    drone = System()
    await drone.connect(system_address="udp://:14540")
    #
    # await drone.action.arm()
    # await drone.action.takeoff()

    status_text_task = asyncio.ensure_future(print_status_text(drone))

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position estimate OK")
            break

    print("Fetching amsl altitude at home location....")
    async for terrain_info in drone.telemetry.home():
        absolute_altitude = terrain_info.absolute_altitude_m
        break
        
    print("-- Arming")
    await drone.action.arm()
    await asyncio.sleep(5)
    print("-- Taking off")
    await drone.action.takeoff()

    await asyncio.sleep(10)

    print('-- Random moving')
    manual_inputs = [
        [0, 0, 0.5, 0],  # no movement
        [-0.25, 0, 0.5, 0],  # minimum roll
        [0.25, 0, 0.5, 0],  # maximum roll
        [0, -0.25, 0.5, 0],  # minimum pitch
        [0, 0.25, 0.5, 0],  # maximum pitch
        [0, 0, 0.5, -0.25],  # minimum yaw
        [0, 0, 0.5, 0.25],  # maximum yaw
        [0, 0, 0.6, 0],  # max throttle
        [0, 0, 0.4, 0],  # minimum throttle
    ]

    for _ in range(3):
        # grabs a random input from the test list
        # WARNING - your simulation vehicle may crash if its unlucky enough
        input_index = random.randint(0, len(manual_inputs) - 1)
        input_list = manual_inputs[input_index]
        print(f'  #{input_index} values:', input_list)
        # get current state of roll axis (between -1 and 1)
        roll = float(input_list[0])
        # get current state of pitch axis (between -1 and 1)
        pitch = float(input_list[1])
        # get current state of throttle axis (between -1 and 1, but between 0 and 1 is expected)
        throttle = float(input_list[2])
        # get current state of yaw axis (between -1 and 1)
        yaw = float(input_list[3])

        await drone.manual_control.set_manual_control_input(roll, pitch, throttle, yaw)
        await asyncio.sleep(0.1)
        await drone.manual_control.set_manual_control_input(0, 0, 0.5, 0)
        await asyncio.sleep(2)

    flying_alt = absolute_altitude + 20.0
    # goto_location() takes Absolute MSL altitude
    await drone.action.goto_location(47.397606, 8.543060, flying_alt, 0)

    await asyncio.sleep(20)


    print("-- Landing")
    await drone.action.land()

    status_text_task.cancel()

async def print_status_text(drone):
    try:
        async for status_text in drone.telemetry.status_text():
            print(f"Status: {status_text.type}: {status_text.text}")
    except asyncio.CancelledError:
        return

if __name__ == '__main__':
    asyncio.run(fly_dron())

