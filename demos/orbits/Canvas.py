import tkinter as tk, math

class Canvas:
    window = None
    drawing = None
    view = None

    @staticmethod
    def init(canvas_width, canvas_height, title='CIS 211 Canvas'):
        """Initialize (or re-initialize) the canvas to the specified width and height."""
        padding = 10
        if Canvas.window == None:
            Canvas.window = tk.Tk()
            Canvas.window['background'] = 'gray'
            Canvas.window.columnconfigure(0, weight=1)
            Canvas.window.rowconfigure(0, weight=1)
            Canvas.drawing = tk.Canvas(Canvas.window, height=canvas_height, width=canvas_width, background='white', highlightthickness=0)
            Canvas.drawing.columnconfigure(0, weight=1)
            Canvas.drawing.rowconfigure(0, weight=1)
            Canvas.drawing.grid(row=0, column=0, padx=padding, pady=padding, sticky='nsew')
            Canvas.window.protocol('WM_DELETE_WINDOW', Canvas.close)
        else:
            Canvas.drawing.delete('all')
            Canvas.drawing['width'] = canvas_width
            Canvas.drawing['height'] = canvas_height
        Canvas.window.title(title)
        Canvas.window.geometry('%dx%d+50+50' % (canvas_width + 2 * padding, canvas_height + 2 * padding))

    @staticmethod
    def close():
        """Close the canvas window (call Canvas.init again to reopen it)."""
        Canvas.window.destroy()
        Canvas.window = None
        Canvas.drawing = None

    @staticmethod
    def update():
        """Update the canvas"""
        Canvas.drawing.update()

    class Shape:
        """
        Shape is the base class for Text, Circle, and other objects placed on the canvas.
        """

        def move(self, dx, dy, track=False):
            """
            Move this shape by dx pixels horizontally and dy pixels vertically.  If track is
            True draw a line from the old position to the new postion (provided the
            object's penpoint attribute has been set).
            """
            if track and self._penpoint != None:
                a = Canvas.drawing.coords(self._id)
                x0 = a[0] + self._penpoint[0]
                y0 = a[1] + self._penpoint[1]
                Canvas.drawing.create_line(x0, y0, x0 + dx, y0 + dy, width=1, fill='#777777')
            Canvas.drawing.move(self._id, dx, dy)
            Canvas.drawing.lift(self._id)

        def coords(self):
            """
            Return this shape's current coordinates.
            """
            return Canvas.drawing.coords(self._id)

        def erase(self):
            """
            Remove this object from the canvas.  The object still exists, so set its ID
            to None to record the fact that it's not on the canvas (calling move or coords
            after this will raise an exception).
            """
            Canvas.drawing.delete(self._id)
            self._id = None

    class Text(Shape):
        """Place string s on the canvas at location (x,y)"""

        def __init__(self, s, x, y, **options):
            if Canvas.window == None:
                raise CanvasError('call Canvas.init to create the canvas window')
            params = {'text': s, 'font': ('Helvectica', 12), 'anchor': 'nw'}
            params.update(options)
            self._penpoint = None
            self._text = s
            self._font = ('Helvetica', 11)
            self._id = Canvas.drawing.create_text(x, y, **params)

    class Line(Shape):
        """Draw a line on the canvas from p1 to p2"""

        def __init__(self, p1, p2, **options):
            if Canvas.window == None:
                raise CanvasError('call Canvas.init to create the canvas window')
            params = {}
            params.update(options)
            self._penpoint = None
            self._id = Canvas.drawing.create_line(p1[0], p2[0], p1[1], p2[1], **params)

    class Rectangle(Shape):
        """Create a rectangle with upper left vertex at ul and lower right vertex at lr"""

        def __init__(self, ul, lr, **options):
            if Canvas.window == None:
                raise CanvasError('call Canvas.init to create the canvas window')
            params = {}
            params.update(options)
            x0, y0 = ul
            x1, y1 = lr
            self._penpoint = ((x1 - x0) // 2, (y1 - y0) // 2)
            self._id = Canvas.drawing.create_rectangle(x0, y0, x1, y1, **params)

    class Circle(Shape):
        """Create a circle with radius r at the specified (x,y) coordinates"""

        def __init__(self, r, loc, **options):
            if Canvas.window == None:
                raise CanvasError('call Canvas.init to create the canvas window')
            params = {}
            params.update(options)
            x, y = loc
            self._penpoint = (r, r)
            self._id = Canvas.drawing.create_oval((x - r), (y - r), (x + r), (y + r), **params)

    class Polygon(Shape):
        """Create a polygon given a sequence a of vertices"""

        def __init__(self, a, **options):
            if Canvas.window == None:
                raise CanvasError('call Canvas.init to create the canvas window')
            params = {}
            params.update(options)
            self._penpoint = (0, 0)
            self._id = Canvas.drawing.create_polygon(a, **params)

        def rotate(self, theta):
            """
            Rotate the polygon by an angle theta (expressed in degrees).  The object is
            rotated about the point defined by the first pair of (x,y) coordinates.
            """
            theta = math.radians(theta)
            a = Canvas.drawing.coords(self._id)
            x0 = a[0]
            y0 = a[1]
            for i in range(0, len(a), 2):
                x = a[i] - x0
                y = a[i + 1] - y0
                a[i] = x0 + x * math.cos(theta) - y * math.sin(theta)
                a[i + 1] = y0 + x * math.sin(theta) + y * math.cos(theta)

            Canvas.drawing.coords(self._id, *a)


class CanvasError(Exception):
    pass
