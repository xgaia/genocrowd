import git
import sys
import traceback

from genocrowd.libgenocrowd.LocalAuth import LocalAuth
from genocrowd.libgenocrowd.Start import Start

from flask import (Blueprint, current_app, jsonify, session)

from pkg_resources import get_distribution


start_bp = Blueprint('start', __name__, url_prefix='/')


@start_bp.route('/api/hello', methods=['GET'])
def hello():
    """Dummy routes

    Returns
    -------
    json
        error: True if error, else False
        errorMessage: the error message of error, else an empty string
        message: a welcome message
    """
    try:
        message = "Welcome to Genocrowd" if 'user' not in session else "Hello {} {}, Welcome to Genocrowd!".format(
            session["user"]["fname"], session["user"]["lname"])

    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        return jsonify({
            'error': True,
            'errorMessage': str(e),
            'message': ''
        }), 500

    return jsonify({
        'error': False,
        'errorMessage': '',
        'message': message
    })


@start_bp.route('/api/start', methods=['GET'])
def start():
    """Starting route

    Returns
    -------
    json
        Information about a eventualy logged user, and the Genocrowd version
        and a footer message
    """
    try:
        starter = Start(current_app, session)
        starter.start()

        # Get commmit hash
        sha = None
        if current_app.iniconfig.getboolean('genocrowd', 'display_commit_hash'):
            try:
                repo = git.Repo(search_parent_directories=True)
                sha = repo.head.object.hexsha[:10]
            except Exception:
                pass

        # get proxy path
        proxy_path = "/"
        try:
            proxy_path = current_app.iniconfig.get("genocrowd", "reverse_proxy_path")
        except Exception:
            pass

        config = {
            "footerMessage": current_app.iniconfig.get('genocrowd', 'footer_message'),
            "version": get_distribution('genocrowd').version,
            "commit": sha,
            "gitUrl": current_app.iniconfig.get('genocrowd', 'github'),
            "disableIntegration": current_app.iniconfig.getboolean('genocrowd', 'disable_integration'),
            "prefix": current_app.iniconfig.get('triplestore', 'prefix'),
            "namespace": current_app.iniconfig.get('triplestore', 'namespace'),
            "proxyPath": proxy_path,
            "user": {},
            "logged": False
        }

        json = {
            "error": False,
            "errorMessage": '',
            "config": config
        }

        if 'user' in session:
            current_app.logger.debug(session["user"]["username"])
            local_auth = LocalAuth(current_app, session)
            user = local_auth.get_user(session['user']['username'])
            session['user'] = user
            json['config']['user'] = user
            json['config']['logged'] = True

        return jsonify(json)

    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        return jsonify({
            "error": True,
            "errorMessage": str(e),
            "config": {}
        }), 500
