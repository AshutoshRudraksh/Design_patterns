package java;

import java.util.ArrayList;
import java.util.List;

public class Prototype {
   interface Shape {
    Shape clone();
}

class Rectangle implements Shape {
    private int width;
    private int height;

    public Rectangle(int width, int height) {
        this.width = width;
        this.height = height;
    }

    public int getWidth() {
        return this.width;
    }

    public int getHeight() {
        return this.height;
    }

    @Override
    public Shape clone() {
        // if we do return this; now this is shallow copy we need deep copy
        return new Rectangle(this.width, this.height); // this will return deep copy
    }
}

class Square implements Shape {
    private int length;

    public Square(int length) {
        this.length = length;
    }

    public int getLength() {
        return this.length;
    }

    @Override
    public Shape clone() {
        return new Square(this.length);
    }
}

class Test {
    public List<Shape> cloneShapes(List<Shape> shapes) {
        List<Shape> clonedShapes = new ArrayList<>();
        for(Shape shape: shapes ){
            // navie way to do this is just return clonedShape.add(shapes); this will return shallow copy
            clonedShapes.add(shape.clone());
        }
        return clonedShapes;
    }
}
 
}
