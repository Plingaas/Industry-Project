import asyncio
import techmanpy

async def moveToTable():
   async with techmanpy.connect_sct(robot_ip='10.0.12.102') as conn:
      await conn.move_to_joint_angles_ptp([0, 15, -135, 30, -90, 0], 1.0, 200)

async def moveToHome():
   async with techmanpy.connect_sct(robot_ip='10.0.12.102') as conn:
      await conn.move_to_joint_angles_ptp([0, 0, 0, 0, 0, 0], 1.0, 200)

async def openGripper():
    async with techmanpy.connect_sct(robot_ip='10.0.12.102') as conn:
        await conn.queue_command('ToolCmd(1,1,100)')

async def setBase(x, y, z):
    async with techmanpy.connect_sct(robot_ip='10.0.12.102') as conn:
        await conn.set_base([x, y, z, 0, 0, 0])

async def moveTo(x, y, z):
    async with techmanpy.connect_sct(robot_ip='10.0.12.102') as conn:
        await conn.move_to_point_ptp([x, y, z, 0, 0, 0], 1.0, 200)

async def exitListen():
   async with techmanpy.connect_sct(robot_ip='10.0.12.102') as conn:
        await conn.exit_listen()
 
asyncio.run(moveToHome())
#asyncio.run(moveToTable())
asyncio.run(exitListen())
#asyncio.run(moveTo(100, 100, 800))
#asyncio.run(openGripper())