from sqlalchemy import (create_engine, Column, Integer,
                        String, Date, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

import datetime
import csv


engine = create_engine('sqlite:///inventory.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Brands(Base):
    __tablename__ = 'brands'

    brand_id = Column(Integer, primary_key=True)
    brand_name = Column('Brand Name', String)
    brand_rel_1 = relationship('Product', back_populates='brand_rel_2',
                               cascade='all, delete, delete-orphan')

    def __repr__(self):
        return f'''
    \nBrand {self.brand_id}    
    \rBrand Name: {self.brand_name}
    '''


class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True)
    product_name = Column('Product Name', String)
    product_quantity = Column('Product Quantity', Integer)
    product_price = Column('Product Price', Integer)
    date_updated = Column('Date Updated', Date)
    brand_id = Column('Brand ID', Integer, ForeignKey('brands.brand_id'))
    brand_rel_2 = relationship('Brands', back_populates='brand_rel_1')

    def __repr__(self):
        return f'''
        \nProduct: {self.product_id}
        \rProduct Name: {self.product_name} 
        \rProduct Quantity: {self.product_quantity} 
        \rProduct Price: {self.product_price} 
        \rDate Updated: {self.date_updated}
        \rBrand ID: {self.brand_id}
        '''


def menu():
    while True:
        print('''
              \nSTORE PRODUCT INVENTORY
              \rV) View Details of a Single Product
              \rN) Add New Product to Store Inventory
              \rA) View Product Analysis
              \rB) Make a backup of the entire Store Inventory
              \rE) Exit
              ''')
        choice = input('Please select an option: [V, N, A, B, E] ')
        if choice.lower() in ['v', 'n', 'a', 'b', 'e']:
            return choice
        else:
            input('''
                  \rThat is not a valid value. 
                  \rPlease choose from one of the following options: [V, N, A, B, E]
                  \rPress enter to try again.''')


# Add products to the database
# Edit Products
# Delete Products
# Search Products
# Data Cleaning
def clean_product_quantity(quantity_str):
    int_quantity = int(quantity_str)
    return int_quantity


def clean_date(date_str):
    split_date = date_str.split('/')
    month = int(split_date[0])
    day = int(split_date[1])
    year = int(split_date[2])
    return datetime.date(year, month, day)


def clean_price(price_str):
    split_price = price_str.split('$')
    price_float = float(split_price[1])
    return int(price_float * 100)


def add_brands_csv():
    with open('store-inventory/brands.csv') as csvfile:
        data = csv.reader(csvfile)
        next(data)
        for row in data:
            brand_name = row[0]
            new_brand = Brands(brand_name=brand_name)
            session.add(new_brand)
        session.commit()


def add_inventory_csv():
    with open('store-inventory/inventory.csv') as csvfile:
        data = csv.reader(csvfile)
        next(data)
        for row in data:
            product_name = row[0]
            product_quantity = clean_product_quantity(row[2])
            product_price = clean_price(row[1])
            date = clean_date(row[3])
            # brand_name = row[4]
            brand_id = session.query(Brands.brand_id)
            new_product = Product(product_name=product_name, product_quantity=product_quantity,  
                                  product_price=product_price, date_updated=date, brand_id=brand_id)
            session.add(new_product)
        session.commit()


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice.lower() == 'v':
            # View Details of single product
            pass
        elif choice.lower() == 'n':
            # Add New Product
            pass
        elif choice.lower() == 'a':
            # View Product Analysis
            pass
        elif choice.lower() == 'b':
            # Backup entire store inventory
            pass
        else:
            print('Goodbye!')
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    # app()
    add_brands_csv()
    add_inventory_csv()

    for product in session.query(Product):
        print(product)