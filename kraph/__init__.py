from .kraph import Kraph


try:
    from .arkitekt import KraphService
except ImportError as e:
    try:
        import arkitekt
    except ImportError:
        pass
    else:
        raise e
try:
    from .rekuest import structure_reg
except ImportError as e:
    try:
        import rekuest
    except ImportError:
        pass
    else:
        raise e

__all__ = ["Kraph", "structure_reg", "KraphService"]
