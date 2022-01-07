from flask import Response, request
from __main__ import app, g, users, dns
from controllers.users import OperationError
from controllers.dns import DNSError

@app.route("/domains/<path:domain>", methods=['POST'])
def applyDomain(domain):
    if not g.user:
        return {"message": "Unauth."}, 401

    user = users.getUser(g.user['uid'])
    domain = domain.strip('/').split('/')
    domainName = '.'.join(reversed(domain))

    try:
        if not users.authorize(user, "APPLY", domain):
            return {"errorType": "PermissionDenied", "msg": ""}, 403
        dns.applyDomain(user['uid'], domainName)
    except OperationError as e:
        return {"errorType": e.typ, "msg": e.msg}, 403

    return {"msg": "ok"}

@app.route("/domains/<path:domain>", methods=['DELETE'])
def releaseDomain(domain):
    if not g.user:
        return {"message": "Unauth."}, 401

    user = users.getUser(g.user['uid'])
    domain = domain.strip('/').split('/')
    domainName = '.'.join(reversed(domain))

    try:
        if not users.authorize(user, "REPLEASE", domain):
            return {"errorType": "PermissionDenied", "msg": ""}, 403
        dns.releaseDomain(user['uid'], domainName)
    except OperationError as e:
        return {"errorType": e.typ, "msg": e.msg}, 403

    return {"msg": "ok"}