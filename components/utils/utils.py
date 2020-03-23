def create_object(obj_module: str, obj_class: str, obj_args: dict):
    mod   = __import__(obj_module, fromlist=[obj_class])
    klass = getattr(mod, obj_class)

    return klass(**obj_args)

def get_fitted_image_dimensions(
    original_width: int,
    original_height: int,
    fit_to_width: int,
    fit_to_height: int
) -> tuple:
    fit_ratio      = fit_to_width / fit_to_height
    original_ratio = original_width / original_height

    if fit_ratio > original_ratio:
        return (int(original_width * (fit_to_height / original_height)), fit_to_height)
    else:
        return (fit_to_width, int(original_height * (fit_to_width / original_width)))