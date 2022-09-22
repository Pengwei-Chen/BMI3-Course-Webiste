import inspect
from functools import wraps
from typing import Optional, Union
import types

def typed(func): 
    @wraps(func)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        bound_types = sig.bind_partial(**func.__annotations__).arguments
        bound_values = sig.bind(*args, **kwargs)
        # Enforce type assertions across supplied arguments 
        for name, value in bound_values.arguments.items():
            if name in bound_types:
                if hasattr(bound_types[name], "__origin__"):
                    if bound_types[name].__origin__ is Union:
                        if not type(value) in bound_types[name].__args__:
                             raise TypeError('Argument {} must be one of {}'.format(name, bound_types[name]))
                    elif bound_types[name].__origin__ is Generic:
                        if not isinstance(value, bound_types[name].__args__[0]):
                            raise TypeError('Argument {} must be {} or None'.format(name, bound_types[name]))
                    else: 
                        raise TypeError("Types for type hint is not supported")
                else:
                    if not isinstance(value, bound_types[name]):
                        raise TypeError('Argument {} must be {}'.format(name, bound_types[name]))
        return func(*args, **kwargs) 
    return wrapper

def typeassert(*ty_args, **ty_kwargs): 
    def decorate(func):
        sig = inspect.signature(func)
        bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments
        print(bound_types)
        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            # Enforce type assertions across supplied arguments for name, value in bound_values.arguments.items():
            if name in bound_types:
                if not isinstance(value, bound_types[name]):
                    raise TypeError('Argument {} must be {}'.format(name, bound_types[name]))
            return func(*args, **kwargs) 
        return wrapper
    return decorate

class MultiMethod:
    def __init__(self, name):
        self.register_dict = {}
        self.__name__ = name
        
    def _register(self,key,value):
        # key for argument type; value for method
        self.register_dict[key] = value
    
    def register(self,method):
        sig = inspect.signature(method)
        types = []
        for name, parm in sig.parameters.items():
            if name == 'self':
                continue
            if parm.annotation is inspect.Parameter.empty:
                raise TypeError(
                    'Argument {} must be annotated with a type'.format(name)
                )
            if not isinstance(parm.annotation, type):
                raise TypeError(
                    'Argument {} annotation must be a type'.format(name)
                )
            if parm.default is not inspect.Parameter.empty:
                self._register(tuple(types),method)
            types.append(parm.annotation)

        self._register(tuple(types),method)
    
    def __call__(self, *args):
        types = tuple(type(arg) for arg in args[1:])
        meth = self.register_dict.get(types)
        if meth:
            return meth(*args)
        else:
            raise TypeError(
                '...'.format(name)
            )
   
    def __get__(self, instance, cls):
        # Descriptor method needed to make calls work in a class
        if instance is not None:
            return types.MethodType(self, instance) 
        else:
            return self

    
class MultiDict(dict):
    def __setitem__(self, key, value):
        if key in self:
            current_value = self[key]
            if isinstance(current_value, MultiMethod):
                current_value.register(value)
            else:
                mvalue = MultiMethod(key)
                mvalue.register(current_value)
                mvalue.register(value)
                super().__setitem__(key, mvalue)
        else:
            super().__setitem__(key, value)

class MultipleTypeCheckedMeta(type):
    def __new__(cls,clsname,bases,clsdict):
        return type.__new__(cls,clsname,bases,dict(clsdict))
    @classmethod
    def __prepare__(cls,clsname,bases):
        return MultiDict()