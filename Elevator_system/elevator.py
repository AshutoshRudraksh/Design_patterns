from os import stat_result
# Implementation

from collections import deque
import heapq
import time
from enum import Enum

# our elevator have 3 states: going_up. going_down, Idle 
# for this we use enum states
class State(Enum):
  IDLE = 1
  UP = 2
  DOWN = 3
  EMERGENCY = 4

# We have two types of elevator 
class ElevatorType(Enum):
  PASSENGER = 1
  EMERGENCY = 2

# IT IS IMPORTANT  to distinguish whether the request is made from the inside
# or outside of the elevator 

class RequestOrigin(Enum):
  INSIDE = 1
  OUTSIDE = 2

# the elevator door can have two states:  OPEN, CLOSED
class DoorState(Enum):
  OPEN = 1
  CLOSED = 2

# now let's say I need to request for elevator the user need to press button 
# either from inside or outside of the elevator

class Request:

  def __init__(self, origin, origin_floor, destination_floor=None):
    self.origin = origin
    self.direction = State.IDLE
    self.origin_floor = origin_floor
    self.destination_floor = destination_floor
    self.elevator_type = ElevatorType.PASSENGER

  # how to determine whether to go down or up
    if destination_floor is not None:
      if origin_floor < destination_floor:
        self.direction = State.UP
      elif origin_floor > destination_floor:
        self.direction = State.DOWN

  def get_origin_floor(self):
    return self.origin_floor

  def get_destination_floor(self):
    return self.destination_floor

  def get_origin(self):
    return self.origin

  def get_direction(self):
    return self.direction

  # to determine order within the heap
  def __lt__(self, other):
    return self.origin_floor < other.origin_floor


# given that service elevator should act differently then the passenger elevator 
# in that it is made to move heavy items. we can extend request class to ServiceRequest

class ServiceRequest(Request):
  def __init__(self, origin, current_floor=None, destination_floor=None):
    if current_floor is not None and destination_floor is not None:
      super().__init__(origin,current_floor, destination_floor)
    else:
      super().__init__(origin, destination_floor)
    self.elevator_type = ElevatorType.SERVICE


# LET'S create abstract elevator class which is be handling the request for both type of elevators

class Elevator:
  def __init__(self, current_floor, emergency_status):
    self.current_floor = current_floor
    self.state = State.IDLE
    self.emergency_status = emergency_status
    self.door_state = DoorState.CLOSED

  def open_door(self):
    self.door_state = DoorState.OPEN
    print(f"Door is OPEN on the floor {self.current_floor}")

  def close_door(self):
    self.door_state = DoorState.CLOSED
    print("Doors are closed")

  def wait_for_seconds(self, seconds):
    time.sleep(seconds)
  
  def operate(self):
    pass

  def process_emergency(self):
    pass

  def get_current_floor(self):
    return self.current_floor

  def get_state(self):
    return self.state

  def set_state(self, state):
    self.state = state


  def get_current_floor(self, floor):
    self.current_floor = floor

  def get_door_state(self):
    return self.door_state

  def get_emergency_status(self, status):
    self.emergency_status = status

class PassengerElevator(Elevator):
  def __init__(self, current_floor, emergency_status):
    super().__init__(current_floor, emergency_status)
    self.passenger_up_queue = []
    self.passenger_down_queue = []

  def operate(self):
    while self.passenger_up_queue or self.passenger_down_queue:
      self.process_requet()

    self.set_state(State.IDLE)
    print("All requests have been fulfilled, elevator is now", self.get_state())

  
  def process_emergency(self):
    self.passenger_up_queue.clear()
    self.passenger_down_queue.clear()
    self.set_current_floor(1)
    self.set_state(State.IDLE)
    self.open_doors()
    self.set_emergency_status(True)
    print("Queues cleared, current floor is", self.get_current_floor(),
          ". Doors are ", self.get_door_state())
    self.set_state(State.IDLE)

  def add_up_request(self, request):
    if request.get_origin() == RequestOrigin.OUTSIDE:
      pick_up_request = Request(request.get_origin(), request.get_origin_floor())
      heapq.heappush(self.passenger_up_queue, pick_up_request)
    heapq.heappush(self.passenger_up_queue, request)

  def add_down_request(self, request):
    if request.get_origin() == RequestOrigin.OUTSIDE:
      pick_up_request = Request(request.get_origin(), request.get_origin_floor(),
                                request.get_origin_floor())
      heapq.heappush(self.passenger_down_queue, request)

  def process_up_requests(self):
    while self.passenger_up_queue:
      up_request = heapq.heappop(self.passenger_up_queue)

      if self.get_current_floor() == up_request.get_destination_floor():
        print("Currently on floor", self.get_current_floor(), 
              ". No movement as destination is the same as current floor")
        continue
      print("The current floor is", self.get_current_floor(), 
            ". Next stop: ", up_request.get_destination_floor())
      
      try:
        print("Moving ", end="")
        for _ in range(3):
          print(".", end="", flush=True)
          time.sleep(0.5) #pause for half a second between dots
        time.sleep(1) # 1 second to move between floors
        print()
      except KeyboardInterrupt:
        pass
      except Exception as e:
        print("Error: ", e)      
      
      self.set_current_floor(up_request.get_destination_floor())
      print("Arrived at", self.get_current_floor())

      self.open_doors()
      # simulating 3 seconds for people to enter/exit
      self.wait_for_seconds(3)
      self.close_doors()

    print("Finished processing up requests.")

  def process_down_requests(self):
    while self.passenger_down_queue:
      down_request = heapq.heappop(self.passenger_down_queue)

      if self.get_current_floor() == down_request.get_destination_floor():
        print("Currently on floor", self.get_current_floor(), 
              ". No movement as destination is the same as current floor")
        continue
      print("The current floor is", self.get_current_floor(), ". Next stop:", down_request.get_destination_floor())

    try: 
      print("Moving", end="")
      for _ in range(3):
        print(".", end="", flush=True)
        time.sleep(0.5)
      time.sleep(1)
      print()
    except KeyboardInterrupt:
      pass
    except Exception as e:
      print("Error: ", e)

    self.set_current_floor(down_request.get_destination_floor())
    print("Arrived at", self.get_current_floor())

    self.open_doors()
    #simulating 3 seconds for people to enter/exist.

    self.wait_for_seconds(3)
    self.close_doors()

    print("Finished processing all the down requests.")


  def process_request(self):
    if self.get_state() == State.UP or self.get_state() == State.IDLE:
      self.process_up_requests()
      if self.passenger_down_queue:
        print("Now processing down requests...")

        self.process_down_requests()
    else:
      self.process_down_requests()
      if self.passenger_up_queue:
        print(f"Now processing up requests...")
        self.process_up_requests()


# Service elevator which operates on first come first serve basis
class ServiceElevator(Elevator):
  def __init__(self, current_floor, emergency_status):
    super().__init__(current_floor, emergency_status)
    self.service_queue = deque()

  def operate(self):
    while self.service_queue:
      curr_request = self.service_queue.popleft()

      print() # Move to the next line after the dots
      print("Currently at", self.get_current_floor())
      try:
        time.sleep(1)
        print("Currently at", self.get_current_floor(), end="")
        for _ in range(3):
          print(".", end="", flush=True)
          time.sleep(0.5)
      except KeyboardInterrupt:
        pass
      except Exception as e:
        print("Error:", e)

      self.set_current_floor(curr_request.get_destination_floor())
      self.set_state(curr_request.fet_direction())
      print("Arrived at", self.get_current_floor())

      self.open_doors()
      self.wait_for_seconds(3)
      self.close_doors()
    self.set_state(State.IDLE)
    print("All requests have been fulfilled, elevator is now", self.get_state())

  def add_request_to_queue(self, request):
    self.service_queue.append(request)

  def process_emergency(self):
    self.service_queue.clear()
    self.set_current_floor(1)
    self.set_state(State.IDLE)
    self.open_doors()
    self.set_emergency_status(True)
    print("Queues cleared, current floor is", self.get_current_floor(),
          ". Doors are ", self.get_door_state())


#The user does not need to know all of the above business logic. 
#To abstract the instantiation, we can use the Factory pattern in our ElevatorFactory class.

class ElevatorFactory:
  @staticmethod
  def create_elevator(elevator_type: ElevatorType):
    if elevator_type == ElevatorType.PASSENGER:
      return PassengerElevator(1, False)
    elif elevator_type == ElevatorType.SERVICE:
      return ServiceElevator(1, False)
    else:
      return None

# Now that we have everything in place let's create the contoller class 
# the class that user will interact with

class Controller:

  def __init__(self, factory):
    self.factory = factory
    self.passenger_elevator = factory.create_elevator(ElevatorType.PASSENGER)
    self.service_elevator = factory.create_elevator(ElevatorType.SERVICE)
  
  def send_passenger_up_requests(self, requests):
    self.passenger_elevator.add_up_request(requests)

  def send_passenger_down_requests(self, requests):
    self.passenger_elevator.add_down_request(requests)

  def send_service_request(self, request):
    self.service_elevator.add_request_to_queue(request)

  def handle_passenger_requests(self):
    self.passenger_elevator.operate()

  def handle_service_requests(self):
    self.service_elevator.operate()

  def handle_emergency(self):
    self.passenger_elevator.process_emergency()
    self.service_elevator.process_emergency()


# Main class

class Main:
  
  @staticmethod
  def main():
    factory = ElevatorFactory()
    controller = Controller(factory)

    controller.send_passenger_up_requests(Request(RequestOrigin.OUTSIDE, 1, 5))
    controller.send_passenger_down_requests(Request(RequestOrigin.OUTSIDE, 4, 2))
    controller.send_passenger_up_requests(Request(RequestOrigin.INSIDE, 3, 6))
    controller.handle_passenger_requests()

    controller.send_passenger_up_requests(Request(RequestOrigin.OUTSIDE, 1, 5))
    controller.send_passenger_down_requests(Request(RequestOrigin.INSIDE, 5))
    controller.send_passenger_up_requests(Request(RequestOrigin.OUTSIDE, 4, 12))
    controller.handle_passenger_requests()

    print("Now processing service requests...")

    controller.send_service_request(ServiceRequest(RequestOrigin.INSIDE, 13))
    controller.send_service_request(ServiceRequest(RequestOrigin.INSIDE, 13, 2))
    controller.send_service_request(ServiceRequest(RequestOrigin.INSIDE, 13, 15))

    controller.handle_service_requests()

if __name__ == "__main__":
  Main.main()



