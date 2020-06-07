from abc import abstractmethod


class SingletonMeta(type):
    def __init__(cls, *args, **kwargs):
        cls.instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__call__(*args, **kwargs)
        return cls.instance


class BaseServiceMixin:
    @property
    @abstractmethod
    def service_name(self):
        pass

    @property
    @abstractmethod
    def service_type(self):
        pass
