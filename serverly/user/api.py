import serverly
import serverly.utils
from serverly import Request, Response, error_response
from serverly.user import err

_RES_406 = Response(
    406, body="Unable to parse required parameters. Expected username, password.")


def register(method: str, path: str):
    serverly._sitemap.register_site(method, _api_register, path)


def use(function: str, method: str, path: str):
    """Serverly comes with builtin API-functions for the following serverly.user functions:
    - authenticate
    - change
    - delete
    - get
    - register
    `function`accepts on of the above. The API-endpoint will be registered for `method`on `path`.
    """
    supported_funcs = {"authenticate": _api_authenticate, "change": _api_change,
                       "delete": _api_delete, "get": _api_get, "register": _api_register}
    if not function.lower() in supported_funcs.keys():
        raise ValueError(
            "function not supported. Supported are authenticate, change, delete, get, get_all, register")
    serverly._sitemap.register_site(
        method, supported_funcs[function.lower()], path)


def _api_authenticate(req: Request):
    try:
        serverly.user.authenticate(req.user_cred[0], req.user_cred[1])
        response = Response()
    except TypeError:
        try:
            serverly.user.authenticate(
                req.obj["username"], req.obj["password"])
            response = Response()
        except (AttributeError, KeyError):
            response = _RES_406
            response.body += " Preferably put credentials in the header."
    # not merging these two caus a duplicate registration *needs* to tell that a certain username is already taken
    except err.UserNotFoundError as e:
        response = Response(404, body=str(e))
    except err.NotAuthenticatedError:
        response = Response(401, body="Not authorized.")
    except Exception as e:
        response = Response(500, body=str(e))
    return response


def _api_change(req: Request):
    try:
        serverly.user.authenticate(req.user_cred[0], req.user_cred[1])
        serverly.user.change(req.user_cred[0], **req.obj)
        response = Response()
    except TypeError:
        response = Response(401, {"WWW-Authenticate": "Basic"})
    except err.UserNotFoundError as e:
        response = Response(404, body=str(e))
    except err.NotAuthenticatedError:
        response = Response(401, body="Not authorized")
    return response


def _api_delete(req: Request):
    try:
        serverly.user.authenticate(req.user_cred[0], req.user_cred[1])
        serverly.user.delete(req.user_cred[0])
        response = Response()
    except TypeError:
        try:
            serverly.user.authenticate(
                req.obj["username"], req.obj["password"])
            response = Response()
        except (AttributeError, KeyError):
            response = _RES_406
            response.body += " Preferably put credentials in the header."
    except err.UserNotFoundError as e:
        response = Response(404, body=str(e))
    except err.NotAuthenticatedError:
        response = Response(401)
    except Exception as e:
        response = Response(500, body=str(e))


def _api_get(req: Request):
    try:
        serverly.user.authenticate(req.user_cred[0], req.user_cred[1])
        user = serverly.user.get(req.user_cred[0])
        response = Response(body=serverly.utils.clean_user_object(user))
    except TypeError:
        try:
            serverly.user.authenticate(
                req.obj["username"], req.obj["password"])
            response = Response()
        except (AttributeError, KeyError):
            response = _RES_406
            response.body += " Preferably put credentials in the header."
    except err.UserNotFoundError as e:
        response = Response(404, body=str(e))
    except err.NotAuthenticatedError:
        response = Response(401)
    except Exception as e:
        response = Response(500, body=str(e))


def _api_register(req: Request):
    try:
        serverly.user.register(**req.obj)
        response = Response()
    except (KeyError, AttributeError) as e:
        response = _RES_406
    except Exception as e:
        response = Response(500, body=str(e))
    return response