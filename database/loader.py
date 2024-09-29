from environs import Env
from motor.motor_tornado import MotorClient

env = Env()
env.read_env()

client = MotorClient(env.str("MONGO_URL"))
db = client["RowdySsh"]
