import pybullet as p
import time
import pybullet_data

# Connect to PyBullet
physicsClient = p.connect(p.GUI)  # or p.DIRECT for non-graphical version

# Set the search path for URDF files
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# Set gravity
p.setGravity(0, 0, -10)


# Define the initial position and orientation for the R2D2 model
startPos = [0, 0, 1]
startOrientation = p.getQuaternionFromEuler([0, 0, 0])

# Load the R2D2 URDF at the specified position and orientation
boxId = p.loadURDF("random_urdfs/001/001.urdf", startPos, startOrientation)

# Run the simulation for 10,000 steps
for i in range(10000):
    p.stepSimulation()
    time.sleep(1.0 / 240.0)

# Get and print the position and orientation of the R2D2 model
cubePos, cubeOrn = p.getBasePositionAndOrientation(boxId)
print(cubePos, cubeOrn)

# Disconnect from PyBullet
p.disconnect()
