def create_object(obj_module: str, obj_class: str, obj_args: dict):
    mod   = __import__(obj_module, fromlist=[obj_class])
    klass = getattr(mod, obj_class)

    return klass(**obj_args)