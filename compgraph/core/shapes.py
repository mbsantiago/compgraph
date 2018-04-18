from __future__ import division


class InvalidShapeError(Exception):
    pass


def validate_shape(shape):
    if not isinstance(shape, (list, tuple)):
        try:
            shape = list(shape)
        except Exception as exp:
            msg = 'Shape is not of the right type [list/tuple]'
            msg += '{}'.format(exp)
            raise InvalidShapeError(msg)
    for dim in shape:
        if (not isinstance(dim, (int, float))) or (dim is None):
            msg = '{} is no a valid shape.'.format(shape)
            raise InvalidShapeError(msg)


class Shape(object):
    def __init__(self, shape):
        validate_shape(shape)
        self._shape = shape

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, new_shape):
        validate_shape(shape)
        self._shape = new_shape

    def __add__(self, other):
        if isinstance(other, Shape):
            return Shape([x+y for x, y in zip(self.shape, other.shape)])
        if isinstance(other, int):
            return Shape([x + other for x in self.shape])

    def __mul__(self, other):
        if isinstance(other, Shape):
            return Shape([x * y for x, y in zip(self.shape, other.shape)])
        if isinstance(other, int):
            return Shape([x * other for x in self.shape])

    def __div__(self, other):
        if isinstance(other, Shape):
            return Shape([x / y for x, y in zip(self.shape, other.shape)])
        if isinstance(other, int):
            return Shape([x / other for x in self.shape])

    def __truediv__(self, other):
        if isinstance(other, Shape):
            return Shape([x / y for x, y in zip(self.shape, other.shape)])
        if isinstance(other, int):
            return Shape([x / other for x in self.shape])

    def __sub__(self, other):
        if isinstance(other, Shape):
            return Shape([x - y for x, y in zip(self.shape, other.shape)])
        if isinstance(other, int):
            return Shape([x - other for x in self.shape])

    def __mod__(self, other):
        if isinstance(other, Shape):
            return Shape([x % y for x, y in zip(self.shape, other.shape)])
        if isinstance(other, int):
            return Shape([x % other for x in self.shape])

    def __repr__(self):
        return str(self._shape)

    def __getitem__(self, key):
        return self._shape[key]

    def __iter__(self):
        return iter(self._shape)

    def __eq__(self, other):
        if isinstance(other, Shape):
            other = other.shape
        for x, y in zip(self.shape, other):
            if x != y:
                return False
        return True

    @staticmethod
    def concat(shape1, shape2):
        return Shape(shape1.shape + shape2.shape)
