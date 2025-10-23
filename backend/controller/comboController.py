from typing import Optional

from fastapi import APIRouter, Depends, Query

from resources.database_client import SessionLocal
from service.tokenService import get_current_user, require_auth_token
from utilities.errorRaiser import BadRequestException, raise_error


async def createCombo(token: str = Depends(require_auth_token)):
    db = SessionLocal()
    try:
        pass
    except Exception as e:
        raise_error(e)
    finally:
        db.close()


async def getCombo(id: int, token: str = Depends(require_auth_token)):
    db = SessionLocal()
    try:
        pass
    except Exception as e:
        raise_error(e)
    finally:
        db.close()


async def getCombos():
    pass


async def updateCombo(id: int, token: str = Depends(require_auth_token)):
    db = SessionLocal()
    try:
        pass
    except Exception as e:
        raise_error(e)
    finally:
        db.close()


async def deleteCombo(id: int, token: str = Depends(require_auth_token)):
    db = SessionLocal()
    try:
        pass
    except Exception as e:
        raise_error(e)
    finally:
        db.close()
