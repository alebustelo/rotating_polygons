from numpy import *
from tkinter import *


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle


class Polygon(object):
    def prepare_points(self, poly_points):
        print("prepare_points")
        i = 0
        list_x = []
        list_y = []
        for point in poly_points:
            if i % 2 == 0:
                list_x.append(point)
            else:
                list_y.append(point)
            i += 1
        self.points.append(list_x)
        self.points.append(list_y)
        for i in self.points:
            print(*i)

    def calc_signed_area(self):
        print("calc_signed_area")
        wrap_around = 0
        for i in range(int(self.point_count)):
            if i + 1 == self.point_count:
                wrap_around = 0
            else:
                wrap_around = i + 1
            self.a += self.points[0][i]*self.points[1][wrap_around] - self.points[0][wrap_around]*self.points[1][i]
            print(str(i) + ": " + str(self.a) + ", (x_i, y_i): (" + str(self.points[0][i]) + ", " + str(self.points[1][i]) + "), (x_i+1, y_i+1): (" + str(self.points[0][wrap_around]) + ", " + str(self.points[1][wrap_around]) + ")")

        self.a = self.a * 0.5
        print("A = " + str(self.a))

    def calc_centroid(self):
        print("calc_centroid")
        self.calc_signed_area()
        print("calc_centroid")

        wrap_around = 0
        for i in range(int(self.point_count)):
            if i + 1 == self.point_count:
                wrap_around = 0
            else:
                wrap_around = i + 1
            self.centroid[0] += (self.points[0][i] + self.points[0][wrap_around]) * (self.points[0][i]*self.points[1][wrap_around] - self.points[0][wrap_around]*self.points[1][i]) #x
            self.centroid[1] += (self.points[1][i] + self.points[1][wrap_around]) * (self.points[0][i]*self.points[1][wrap_around] - self.points[0][wrap_around]*self.points[1][i]) #y
            print(str(i) + ": (x, y): (" + str(self.centroid[0]) + ", " + str(self.centroid[1]) + ")")
        self.centroid[0] = self.centroid[0] * (1 / (6 * self.a))
        self.centroid[1] = self.centroid[1] * (1 / (6 * self.a))

        temp_x = []
        temp_y = []

        for i in range(int(self.point_count)):
            temp_x.append(self.centroid[0])
            temp_y.append(self.centroid[1])

        self.centroid_2xn.append(temp_x)
        self.centroid_2xn.append(temp_y)

        print("(x, y): (" + str(self.centroid[0]) + ", " + str(self.centroid[1]) + ")")
        print("centroid 2xn: " + str(self.centroid_2xn))

    def apply_rotate(self, new_points):
        print("apply_rotate")
        apply_points = []
        j = 0
        for i in range(int(self.point_count)):
            apply_points.append(new_points[j % 2][i])
            j += 1
            apply_points.append(new_points[j % 2][i])
            j += 1

        print(tuple(apply_points))
        self.canvas.coords(self.polygon, tuple(apply_points))

    def calculate_rotate(self, degree):
        print("calculate_rotate")
        degree = deg2rad(degree)
        R = []
        r1 = [cos(degree), -sin(degree)]
        r2 = [sin(degree), cos(degree)]
        R.append(r1)
        R.append(r2)

        print("R: " + str(R))

        sub_x = []
        sub_y = []
        sub = []

        for i in range(int(self.point_count)):
            sub_x.append(self.points[0][i] - self.centroid_2xn[0][i])
            sub_y.append(self.points[1][i] - self.centroid_2xn[1][i])
        sub.append(sub_x)
        sub.append(sub_y)

        print("sub: " + str(sub))

        P = (matmul(R, sub))

        print("P: " + str(P))

        add_x = []
        add_y = []

        for i in range(int(self.point_count)):
            add_x.append(P[0][i] + self.centroid_2xn[0][i])
            add_y.append(P[1][i] + self.centroid_2xn[1][i])
        self.rotP.insert(0, add_x)
        self.rotP.insert(1, add_y)

        print("rotP:")
        for i in range(int(self.point_count)):
            print("x " + str(i) + ": " + str(self.rotP[0][i]))
            print("y " + str(i) + ": " + str(self.rotP[1][i]))
        return self.rotP

    def rotate(self, degree, canvas_obj=None, poly_obj=None):
        print("rotate")
        if canvas_obj != None and poly_obj != None:
            self.canvas = canvas_obj
            self.polygon = poly_obj
            self.poly_points = self.canvas.coords(self.polygon)
            self.point_count = len(self.poly_points) / 2
            self.prepare_points(self.poly_points)
            self.calc_centroid()
        self.apply_rotate(self.calculate_rotate(degree))

    def __init__(self, canvas_obj=None, poly_obj=None):
        self.a = 0                             #polygon's signed area
        self.centroid = [0, 0]                 #polygon's centroid x and y
        self.centroid_2xn = []                 #centroid 2xn matrix for dot product
        self.points = []                       #polygon's points in 2xn matrix
        self.point_count = 0                   #number of points in polygon
        self.rotP = []                         #polygon's new rotated points in 2xn matrix
        self.polygon = None                    #polygon object
        self.canvas = None                     #canvas object
        if canvas_obj != None and poly_obj != None:
            self.canvas = canvas_obj
            self.polygon = poly_obj
            self.poly_points = self.canvas.coords(self.polygon)
            self.point_count = len(self.poly_points) / 2
            self.prepare_points(self.poly_points)
            self.calc_centroid()


class Rotate:
    degrees = 0

    def main(self):
        root = Tk()
        root.geometry("500x400+300+300")

        w = Canvas(root, width=500, height=400)
        w.pack()

        print("Entry")

        #square
        print("poly0")
        poly0 = w.create_polygon((75, 275, 75, 375, 175, 375, 175, 275), fill="blue")

        # print("circle1")
        # circle1 = w.create_circle(325, 325, 50, outline="#DDD", width=4)
        #
        #large magic circle
        # print("poly1")
        # poly1 = w.create_polygon((175, 216, 375, 216, 275, 38), fill="dark slate blue")
        #
        # print("poly2")
        # poly2 = w.create_polygon((175, 95, 375, 95, 275, 273), fill="medium slate blue")
        #
        # poly3 = w.create_polygon((175, 216, 375, 216, 275, 38), fill="dark slate blue")
        # poly4 = w.create_polygon((175, 216, 375, 216, 275, 38), fill="dark slate blue")
        # poly5 = w.create_polygon((175, 216, 375, 216, 275, 38), fill="dark slate blue")
        # poly6 = w.create_polygon((175, 216, 375, 216, 275, 38), fill="dark slate blue")
        poly7 = w.create_polygon((175, 216, 375, 216, 275, 38), fill="dark slate blue")
        poly7P = Polygon(w, poly7)

        #prototype
        #print("poly0")
        #poly0 = w.create_polygon((0, 0, 60, 0, 30, 26), fill="green")

        #small magic circle
        #print("poly1")
        #poly1 = w.create_polygon((40, 40, 100, 40, 70, 66), fill="green")

        #print("poly2")
        #poly2 = w.create_polygon((40, 56, 100, 56, 70, 30), fill="green")

        #square
        print("poly3")
        poly3 = w.create_polygon((275, 275, 375, 275, 375, 375, 275, 375), fill="purple")
        poly3P = Polygon(w, poly3)

        print("circle1")
        w.create_circle(325, 325, 50, outline="#DDD", width=4)

        #large magic circle
        print("poly4")
        poly4 = w.create_polygon((175, 216, 375, 216, 275, 38), fill="dark slate blue")
        poly4P = Polygon(w, poly4)

        print("poly5")
        poly5 = w.create_polygon((175, 95, 375, 95, 275, 273), fill="medium slate blue")
        poly5P = Polygon(w, poly5)

        print("circle2")
        w.create_circle((poly5P.centroid[0]+poly4P.centroid[0])/2, (poly5P.centroid[1]+poly4P.centroid[1])/2, (375-175)/2, outline="blue", width=4)

        w.create_circle(poly5P.centroid[0], poly5P.centroid[1], 119, outline="firebrick", width=4)

        w.create_circle(poly5P.centroid[0], poly5P.centroid[1], 119/3, outline="#DDD", width=4)

        #pentagram
        #print("poly6")
        #poly6 = w.create_polygon((175, 273, 275, 35, 375, 273, 175, 95, 375, 95), fill="goldenrod")


        root.title("Rotating Polygon Demo")
        w.pack(fill=BOTH,expand=1)

        rot1 = Polygon()

        def update():
            print("update")
            self.degrees += 1
            Polygon().rotate(1, w, poly0) #degree should be constant for constant rotation
            # Polygon().rotate(self.degrees, w, poly1)
            # Polygon().rotate(self.degrees, w, poly2)
            # Polygon().rotate(self.degrees, w, poly3)
            # Polygon().rotate(self.degrees, w, poly4)
            # Polygon().rotate(self.degrees, w, poly5)
            # Polygon().rotate(self.degrees, w, poly6)
            poly7P.rotate(self.degrees)
            # poly0.rotate(self.degrees)
            # poly1.rotate(self.degrees)
            # poly2.rotate(self.degrees)
            poly3P.rotate(self.degrees)
            poly4P.rotate(self.degrees)
            poly5P.rotate(self.degrees)
            root.after(10, update)

        root.after(0, update)
        root.mainloop()

        print("Exit")

if __name__ == "__main__":
    rotateObj = Rotate()
    rotateObj.main()
