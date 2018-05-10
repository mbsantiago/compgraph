class Namespace(object):
    pass


def make_namespace_from_dict(dictionary):
    namespace = Namespace()
    for key in dictionary:
        value = dictionary[key]
        if isinstance(value, dict):
            value = make_namespace_from_dict(value)
        setattr(namespace, key, value)
    return namespace
