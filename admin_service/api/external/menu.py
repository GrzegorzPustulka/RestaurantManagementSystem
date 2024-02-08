from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from admin_service.crud.menu import menu as crud_menu
from admin_service.schemas.external.menu import MenuCreate, MenuRead, MenuUpdate

from admin_service.api.deps import get_db

router = APIRouter(prefix="/menu", tags=["menu"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=MenuRead)
async def create_menu(menu_in: MenuCreate, db: Session = Depends(get_db)):
    return crud_menu.create(db=db, obj_in=menu_in)


@router.get("/{menu_id}", status_code=status.HTTP_200_OK, response_model=MenuRead)
async def read_menu(menu_id: str, db: Session = Depends(get_db)):
    menu = crud_menu.get(db=db, id=menu_id)
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found"
        )
    return menu


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[MenuRead])
def read_menu_all(db: Session = Depends(get_db)):
    menu = crud_menu.get_all(db=db)
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found"
        )
    return menu


@router.patch("/{menu_id}", status_code=status.HTTP_200_OK, response_model=MenuRead)
async def update_menu(menu_id: str, menu_in: MenuUpdate, db: Session = Depends(get_db)):
    menu = crud_menu.update(db=db, id=menu_id, obj_in=menu_in)
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found"
        )
    return menu


@router.delete("/{menu_id}", status_code=status.HTTP_200_OK, response_model=MenuRead)
async def delete_menu(menu_id: str, db: Session = Depends(get_db)):
    menu = crud_menu.remove(db=db, id=menu_id)
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found"
        )
    return menu
