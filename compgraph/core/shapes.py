
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
        if (not isinstance(dim, int)) or (dim is None):
            msg = '{} is no a valid shape.'.format(shape)
            raise InvalidShapeError('{} is not a valid shape')


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



EXAMPLES = '''

    floor($output1[:-1] )


'''
