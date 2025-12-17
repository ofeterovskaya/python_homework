# extend-point-to-vector.py
import math

class Point:
    """Represents a point in 2D space with x and y coordinates."""
    
    def __init__(self, x, y):
        """Initialize a point with x and y coordinates."""
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        """Check equality with another Point."""
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y
    
    def __str__(self):
        """String representation of the Point."""
        return f"Point({self.x}, {self.y})"
    
    def distance(self, other):
        """Calculate Euclidean distance to another point."""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


class Vector(Point):
    """Vector class that inherits from Point."""
    
    def __str__(self):
        """Override string representation for Vector."""
        return f"Vector({self.x}, {self.y})"
    
    def __add__(self, other):
        """Override + operator for vector addition."""
        if not isinstance(other, Vector):
            raise TypeError("Can only add Vector to Vector")
        return Vector(self.x + other.x, self.y + other.y)


if __name__ == "__main__":
    # Demonstrate Point class functionality
    print("=== Point Class Demo ===")
    p1 = Point(3, 4)
    p2 = Point(0, 0)
    p3 = Point(3, 4)
    
    print(f"p1: {p1}")
    print(f"p2: {p2}")
    print(f"p3: {p3}")
    
    # Test equality
    print(f"p1 == p2: {p1 == p2}")
    print(f"p1 == p3: {p1 == p3}")
    
    # Test distance
    print(f"Distance from p1 to p2: {p1.distance(p2)}")
    print(f"Distance from p1 to p3: {p1.distance(p3)}")
    
    print("\n=== Vector Class Demo ===")
    v1 = Vector(2, 3)
    v2 = Vector(1, -1)
    
    print(f"v1: {v1}")
    print(f"v2: {v2}")
    
    # Test vector addition
    v3 = v1 + v2
    print(f"v1 + v2 = {v3}")
    
    # Test inherited methods
    print(f"v1 == v2: {v1 == v2}")
    print(f"Distance from v1 to v2: {v1.distance(v2)}")
    
    # Show that Vector inherits from Point
    print(f"v1 is instance of Point: {isinstance(v1, Point)}")
    print(f"v1 is instance of Vector: {isinstance(v1, Vector)}")
