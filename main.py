import env
import time
from threading import Thread

agent = env.Agent()

t = Thread(target=agent._test)
t.daemon = True
t.start()
agent.show()
#agent._test()
#agent.show()