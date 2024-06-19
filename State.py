# traffic example
from abc import ABC, abstractmethod

class TrafficLightState(ABC):
  @abstractmethod
  def change_state(self, traffic_light):
    pass
  
class GreenState(TrafficLightState):
  def change_state(self, traffic_light):
    print("Green - go!")
    traffic_light.set_state(YellowState())

class YellowState(TrafficLightState):
  def change_state(self, traffic_light):
    if isinstance(traffic_light.get_prev_state(), RedState):
      print("Yellow (from Red to Green) - caution!")
      traffic_light.set_state(GreenState())
    else:
      print("Yellow (from Green to Red) - caution!")
      traffic_light.set_state(RedState())

class RedState(TrafficLightState):
  def change_state(self, traffic_light):
    print("Red - Stop!")
    traffic_light.set_state(YellowState())

class TrafficLight:
  def __init__(self):
    self.state = RedState()
    self.prev_state = None

  def set_state(self, state):
    self.prev_state = self.state
    self.state = state

  def get_prev_state(self):
    return self.prev_state
  
  def change(self):
    self.state.change_state(self)

light_system = TrafficLight()

light_system.change() # Red -Stop!
light_system.change() # yellow (from red to Green) - caution!
light_system.change() # Green - Go!
light_system.change() # yellow (from Green to Red) - caution!
light_system.change() # Red - Stop!
