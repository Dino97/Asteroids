
class Input:
    keys = {}

    @classmethod
    def is_key_down(cls, key):
        if key in cls.keys:
            if cls.keys[key] is True:
                return True

        return False
