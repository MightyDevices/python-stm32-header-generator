

# header element is basically a dictionary with a element
# type specified during creation
class HeaderElement(dict):
    # constructor
    def __init__(self, type_name, *args):
        # call underlying class constructor
        super(HeaderElement, self).__init__(*args)
        # do not allow 'type' key to be messed around
        if 'type' in self:
            raise KeyError("'type' key is reserved for element type "
                           "description")
        # store the element name
        self['type'] = type_name

    # set the key-value
    def __setitem__(self, key, value):
        # second check must be provided since constructor sets the
        # field value ;-)
        if key is 'type' and 'type' in self:
            raise KeyError("Don't mess with the type field!")
        # call the normal method
        super(HeaderElement, self).__setitem__(key, value)

    # delete the key
    def __delitem__(self, key):
        if key is 'type':
            raise KeyError("Don't delete the type field!")
        # call the normal method
        super(HeaderElement, self).__delitem__(key)

    # pop logic
    def pop(self, k):
        if k is 'type':
            raise KeyError("Don't delete the type field!")
        # call the normal method
        super(HeaderElement, self).pop(k)

    # convert to string
    def __str__(self):
        raise NotImplementedError("String redering for element not implemented")


# define directive element
class HeaderElementDefine(HeaderElement):
    # constructor
    def __init__(self, label: str, value: str=""):
        # call underlying class constructor
        super(HeaderElementDefine, self).__init__("define", {
            'label': label,
            'value': value
        })

    # convert to string
    def __str__(self):
        return "#define " + self['label'] + " " + self['value']
