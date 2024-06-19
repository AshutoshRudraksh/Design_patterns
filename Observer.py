# Book store implementation

class Store(ABC):
  @abstractmethod
  def add_customer(self, customer):
    pass

  @abstractmethod
  def remove_customer(self, customer):
    pass
  
  @abstractmethod
  def notify_customers(self):
    pass

  @abstractmethod
  def update_quantity(self, quantity):
    pass

class BookStore(Store):
  def __init__(self):
    self._customers = []
    self._stock_quantity = 0

  def add_customer(self, customer):
    self._customer.append(customer)

  def remove_customer(self, customer):
    self._customers.remove(customer)

  def notify_customers(self):
    for customer in self._customers:
      customer.update(self._stock_quantity)

  def update_quantity(self, quantity):
    self._stock_quantity = quantity
    self.notify_customers()

class Customer(ABC):
  @abstractmethod
  def update(self, stock_quantity):
    pass

class BookCustomer(Customer):
  def __init__(self, store):
    self._store = store
    self._observed_stock_quantity = 0
    self._store.add_customer(self)

  def update(self, stock_quantity):
    self._observed_stock_quantity = stock_quantity
    if stock_quantity>0:
      print(f'Hello, A book you are interested in is back in stock')


store = BookStore()
customer1 = BookCustomer(store)
customer2 = BookCustomer(store)

#initially, the book is out of stock
print("Setting stock to 0.")
store.update_quantity(0)

# the book comes back in stock
print("Setting stock to 10.")
store.update_quatity(10)

# remove customer1 from the notification list
store.remove_customer(customer1)

#simulate the situation where the stock changes again
print("\nSetting stock to 4")
store.update_quantity(4)