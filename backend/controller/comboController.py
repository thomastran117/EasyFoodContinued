from typing import Optional
from fastapi import APIRouter, Query, Depends
from utilities.errorRaiser import raise_error, BadRequestException
from resources.database_client import SessionLocal
from service.tokenService import require_auth_token, get_current_user


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
