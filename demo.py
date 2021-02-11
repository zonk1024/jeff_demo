#!/usr/bin/env python3

import redis

blah = None  # in scope to whole program

# overriding builtin print in global scope of this module
print = lambda x: print("\n{}".format(x))
def print(x):
    print("\n{}".format(x))

class InstanceCreationException(Exception):
    def __init__(self, description="Not allowed to create instance via direct instantiation"):

        original_blah = blah  # blah exists outside the scope, but is still usable

        blah = True  # not the same blah as above

        # global blah  # NOOOOOOO!  Never!

        still_original_blah = globals()["blah"]  # we can still get blah from the outter scope
        still_this_scope_blah = locals()["blah"]  # we can still get the blah from this scope too, fancily

        super(InstanceCreationException).__init__(self, description)


class Singleton(object):

    INSTANCE_OBJECT = None

    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        if "SINGLETON" not in self._kwargs and self._kwargs["SINGLETON"]:
            raise InstanceCreationException()

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if cls.INSTANCE_OBJECT is None:
            kwargs["SINGLETON"] = True
            cls.INSTANCE_OBJECT = cls(*args, **kwargs)
        return cls.INSTANCE_OBJECT

def x(a, b, c=0, d=0):
    pass

def wrap_x(*args, **kwargs):
    # args = (1, 2, 3)
    # kwargs = {"d": 5}
    # x(1, 2, 3, d=5)
    return x(*args, **kwargs)

# python2 way where print is a statement vs function
# print wrap_x(1, 2, 3, d=5)
print(wrap_x(1, 2, 3, d=5))


for _ in range(2):
    try:
        s = Singleton.get_instance()
    except KeyboardInterrupt:
        exit(0)
    except InstanceCreationException as e:
        raise e
    except ValueError as e:
        exit(2)
    except Exception as e:
        print("WTF?")
        exit(1)


class RedisTimeValueDatabase(object):

    CLIENT_CLASS = redis.Redis

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self._r = None

    def keys(self, search_string="*"):
        return self.r.keys(search_string)

    @property
    def r(self):
        if self._r is None:
            self._r = self.CLIENT_CLASS(self.host, self.port)
        return self._r

    @r.setter
    def r(self, new_r):
        self._r = new_r

    @staticmethod
    def get_triangle_area(base, height):
        return base * height * .5

    @classmethod
    def change_client_class(cls, new_client_class):
        cls.CLIENT_CLASS = new_client_class


# use python convention to tell if we are being run or imported
if __name__ == "__main__":
    # calls staticmethod get_triangle_area on class RedisTimeValueDatabase
    print(RedisTimeValueDatabase.get_triangle_area(5, 4))

    # imports elasiticache module/lib
    import elasiticache
    # sets class RedisTimeValueDatabase's client to use client Elasticache from module elasiticache
    # this would break it but there could be a redis2 library that would work
    RedisTimeValueDatabase.change_client_class(elasiticache.Elasticache)

    # creates instance of RedisTimeValueDatabase and assigns it to variable rtvdb
    rtvdb = RedisTimeValueDatabase("localhost", 6379)

    # prints return value of getter for r (instance method
    # RedisTimeValueDatabase.r wrapped with @property to make function a
    # "getter"
    print(rtvdb.r)

    # create new instance of Redis client from redis module
    new_r = redis.Redis("localhost", 6379)

    # assign new_r as rtvdb.r via "setter" RedisTimeValueDatabase.r (wrapped
    # with @r.setter)
    # Fixes calling change_client_class for this instance of
    # RedisTimeValueDatabase ONLY
    rtvdb.r = new_r

    # print return value of instance method RedisTimeValueDatabase.keys
    print(rtvdb.keys())

    # pretty basic types
    some_bool = True  # immutable
    some_int = 5  # immutable
    some_float = 5.5  # immutable
    some_float_infinity = float("inf")  # immutable
    some_str = "blah"  # immutable
    some_bytes = bytes(some_str)  # immutable

    # somewhat more complicated, not bad though
    some_tuple = (, )  # immutable collection of immutables
    some_list = []  # mutable collection of mutables or immutables
    some_set = set()  # unique collection of immutables
    some_dict = {}  # mapping of immutables to mutables or immutables
