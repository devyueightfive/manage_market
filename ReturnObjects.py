class Return:
    """Object for informing of function returns.\n
     Object consists of 3 attributes:
        v = (0,-1)\n
        t = ('OK', 'Warning', 'Error')\n
        text = any_text
    """

    def __init__(self, v, t='OK', text=''):
        self.Value = v
        self.type = t
        self.text = text

    def __str__(self):
        return f"Value:\t{self.Value}\nType:\t{self.type}\nText:\t{self.text}"
