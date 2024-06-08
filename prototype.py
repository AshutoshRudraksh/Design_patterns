from abc import ABC, abstractmethod
from copy import deepcopy


class DocumentPrototype(ABC):
  @abstractmethod
  def clone_document(self):
    pass

  @abstractmethod
  def display(self):
    pass

class Document(DocumentPrototype):
  def __init__(self, content, images, formatting, annotations):
    self.content = content
    self.images = deepcopy(images)
    self.formatting = formatting
    self.annotations = deepcopy(annotations)

  def clone_document(self):
    return Document(self.content, 
                    self.images,
                    self.formatting,
                    self.annotations)
    
  def display(self):
    print("Content:", self.content)
    print("Images:", self.images)
    print("Formatting:", self.formatting)
    print("Annotations:", self.annotations)

  def add_images(self, images):
    self.images.extend(images)
  
  def add_annotations(self,annotations):
    self.annotations.append(annotations)

images =["Image1.png"]
annotations = ["Annotations1"]
original_doc = Document("Hello, world!",images, "Basic", annotations)      

# cloning the document using the prototype pattern
copied_doc = original_doc.clone_document()

# Making changes to the original document
original_doc.add_images("Image2.png")
original_doc.add_annotations("Annotation2")

# Displaying the contents of both documents
print("Original Document:")
original_doc.display()
print("\nCopied Document:")
copied_doc.display()

# In the code above, the client interacts with the DocumentPrototype interface, which is implemented by Document. 
# Both the originalDoc and copiedDoc are instances of Document that conforms to the DocumentPrototype interface. Notice how flexible this design is; it enables the client to work with various types of documents without being tied to a specific implementation. 
# As a result, modifications to originalDoc or copiedDoc do not impact one another, which goes to show the independence of clones generate through the Prototype pattern.