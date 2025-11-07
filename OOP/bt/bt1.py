class Rectangle:
    def __init__(self, w, h):
        self.w = w
        self.h = h
    def area(self):
        return self.w * self.h
    def perimeter(self):
        return (self.w + self.h) * 2

class Square(Rectangle):
    def __init__(self, w):
        super().__init__(w, w)

rec = Rectangle(3, 4)
print("Dien tich hinh chu nhat la: ", rec.area())
print("Chu vi hinh chu nhat la: ", rec.perimeter())

sqal = Square(3)
print("Dien tich hinh chu vuong la: ", sqal.area())
print("Chu vi hinh chu vuong la: ", sqal.perimeter())
