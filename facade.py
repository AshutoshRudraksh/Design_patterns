# prompt: I am learning facade pattern curretly so I am going to write code just need important notes and link to specific articles in facade in commects

# Facade pattern
# The Facade pattern provides a simplified interface to a complex subsystem.
# It hides the underlying complexity of the subsystem from the client code.

# For example, a facade for a banking system might provide methods for opening accounts,
# depositing money, and withdrawing money. These methods would hide the details of how these
# operations are actually performed by the underlying banking system.


# Links to specific articles on the Facade pattern:
# https://www.tutorialspoint.com/design_pattern/facade_pattern.htm
# https://sourcemaking.com/design_patterns/facade
# https://refactoring.guru/design-patterns/facade

from enum import Enum

class Brightness(Enum):
  UNKNOWN = 0
  BRIGHT = 1
  DIM = 2
  

class Service(Enum):
  UNKNOWN = 0
  HULU = 1
  NETFLIX = 2
  AMAZON_PRIME = 3


class SmartHomeSubSystem:

  def __init__(self):
    self._brightness = Brightness.UNKNOWN
    self.temperature = 19
    self.is_security_armed = False
    self.streaming_service = Service.UNKNOWN
  
  def set_brightness(self, brightness):
    self._brightness = brightness

  def set_temperature(self, temperature):
    self.temperature = temperature

  def set_is_security_armed(self, is_security_armed):
    self.is_security_armed = is_security_armed

  def set_streaming_service(self, streaming_service):
    self.streaming_service = streaming_service

  def _enable_motion_sensors(self):
    pass
  
  def _update_firmware(self):
    pass


class SmartHomeFacade:

  def __init__(self, smart_home):
    self.smart_home = smart_home

  def set_movie_mode(self):
    self.smart_home.set_brightness(Brightness.DIM)
    self.smart_home.set_temperature(34)
    self.smart_home.set_is_security_armed(False)
    self.smart_home.set_streaming_service(Service.NETFLIX)

  def set_focus_mode(self):
    self.smart_home.set_brightness(Brightness.BRIGHT)
    self.smart_home.set_temperature(35)
    self.smart_home.set_is_security_armed(False)
    self.smart_home.set_streaming_service(Service.UNKNOWN)

f = SmartHomeFacade(SmartHomeSubSystem())
f.set_movie_mode()
print(f.smart_home.temperature)
print(f.smart_home.streaming_service)
print(f'\n after changing the mode to focus: \n')
f.set_focus_mode()
print(f.smart_home.temperature)
print(f.smart_home.streaming_service)
