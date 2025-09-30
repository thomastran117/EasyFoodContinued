from typing import Optional
from fastapi import APIRouter, Query, Depends
from utilities.errorRaiser import raise_error, BadRequestException
from resources.alchemy import SessionLocal
from service.tokenService import oauth2_scheme, get_current_user


async def createCombo(token: str = Depends(oauth2_scheme)):
    db = SessionLocal()
    try:
        pass
    except Exception as e:
        raise_error(e)
    finally:
        db.close()


async def getCombo(id: int, token: str = Depends(oauth2_scheme)):
    db = SessionLocal()
    try:
        pass
    except Exception as e:
        raise_error(e)
    finally:
        db.close()


async def getCombos():
    pass


async def updateCombo(id: int, token: str = Depends(oauth2_scheme)):
    db = SessionLocal()
    try:
        pass
    except Exception as e:
        raise_error(e)
    finally:
        db.close()


async def deleteCombo(id: int, token: str = Depends(oauth2_scheme)):
    db = SessionLocal()
    try:
        pass
    except Exception as e:
        raise_error(e)
    finally:
        db.close()
