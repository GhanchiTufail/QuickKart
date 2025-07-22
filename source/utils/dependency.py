    return product

def get_all_products(
    db: Session = Depends(get_db)
):
    product = db.query(Product).all()   
    return product    return product

def get_all_products(
    db: Session = Depends(get_db)
):
    product = db.query(Product).all()   
    return product    return product

def get_all_products(
    db: Session = Depends(get_db)
):
    product = db.query(Product).all()   
    return product    return product

def get_all_products(
    db: Session = Depends(get_db)
):
    product = db.query(Product).all()   
    return product
):
    product = db.query(Product).filter(Product.seller_id == seller.id).all()   
    return product

def get_all_products(
    db: Session = Depends(get_db)
):
    product = db.query(Product).all()   
    return product