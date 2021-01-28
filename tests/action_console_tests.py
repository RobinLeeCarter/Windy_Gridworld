from environment.action import Action
import common
from common import XY
a = Action(common.XY(2, 3))
b = Action(common.XY(4, 5))
dic = {a: 0, b: 1}
c = Action(common.XY(2, 3))
dic[c]
d = Action(common.XY(4, 5))
dic[d]


import common
import action_explore
a = action_explore.Action(common.XY(0, -1))
a.index
