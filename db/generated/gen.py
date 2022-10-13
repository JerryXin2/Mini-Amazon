from werkzeug.security import generate_password_hash
import csv
from faker import Faker

num_users = 100
num_sellers = 20
num_products = 2000
num_carts = 100
num_orders = 2500
num_product_reviews  = 500
num_seller_reviews = 100

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


def gen_users(num_users):
    available_uids = []
    with open('Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            available_uids.append(uid)
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            balance = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            email = profile['mail']
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            fullname = profile['name']
            cart_id = uid
            address = profile['address']
            writer.writerow([uid, email, fullname, address, password, balance, cart_id])
        print(f'{num_users} generated')
    return available_uids

def gen_sellers(num_sellers, available_uids):
    available_sids = []
    with open('Sellers.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Sellers...', end=' ', flush=True)
        for i in range(num_sellers):
            if i % 10 == 0:
                print(f'{i}', end=' ', flush=True)
            profile = fake.profile()
            uid = fake.random_element(elements = available_uids)
            available_sids.append(uid)
            seller = profile['company']
            writer.writerow([uid, seller])
        print(f'{num_sellers} generated')
    return available_sids

def gen_products(num_products, available_sids):
    available_pids = []
    with open('Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for product_id in range(num_products):
            if product_id % 100 == 0:
                print(f'{product_id}', end=' ', flush=True)
            seller_id = fake.random_element(elements = available_sids)
            product_name = fake.sentence(nb_words=4)[:-1]
            category = fake.word()
            description = fake.sentence(nb_words = 20) [:-1]
            image = fake.dga()
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            available = fake.random_element(elements=('true', 'false'))
            if available == 'true':
                available_pids.append(product_id)
            writer.writerow([product_id, seller_id, product_name, category, description, image, price, available])
        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids

def gen_carts(num_carts):
    with open('Carts.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Carts...', end=' ', flush=True)
        for i in range(num_carts):
            if i % 10 == 0:
                print(f'{i}', end=' ', flush=True)
            cart_id = fake.random_element(elements = available_uids) #cid not checked b/c for this example they match uid, will either change this or remove cart_id as a separate id in the future
            product_id = fake.random_element(elements = available_pids) 
            quantity = fake.random_int(min = 1, max = 9)
            writer.writerow([cart_id, product_id, quantity])
        print(f'{num_users} generated')
    return
    
def gen_orders(num_orders, available_uids, available_pids, available_sids):
    with open('Orders.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Orders...', end=' ', flush = True)
        for id in range(num_orders):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            product_id = fake.random_element(elements = available_pids)
            seller_id = fake.random_element(elements = available_sids)
            uid = fake.random_element(elements = available_uids)
            address = fake.address()
            order_time = fake.date_time()    
            quantity = fake.random_int(min = 1, max = 9)
            fulfillment = fake.random_element(elements=('true', 'false'))
            writer.writerow([product_id, seller_id, uid, address, order_time, quantity, fulfillment])
        print(f'{num_orders} generated')
    return
    
def gen_inventory(available_pids):
    with open('Inventory.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Inventory...', end=' ', flush = True)
        for p in (available_pids):
            product_id = p   
            quantity = fake.random_int(min = 1, max = 9999)
            writer.writerow([product_id, quantity])
        print(f'inventory generated')
    return
    
def gen_product_reviews(num_product_reviews, available_pids, available_uids):
    with open ('Product_Reviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Product Reviews...', end=' ', flush = True)
        for id in range(num_product_reviews):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            product_id = fake.random_element(elements = available_pids)
            uid = fake.random_element(elements = available_uids)
            review = fake.sentence(nb_words = 20) [:-1]
            writer.writerow([product_id, uid, review])
        print(f'{num_product_reviews} generated')
    return
    
def gen_seller_reviews(num_seller_reviews, available_sids, available_uids):
    with open ('Seller_Reviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Seller Reviews...', end=' ', flush = True)
        for id in range(num_seller_reviews):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            seller_id = fake.random_element(elements = available_sids)
            reviewer_id = fake.random_element(elements = available_uids)
            review = fake.sentence(nb_words = 20) [:-1]
            writer.writerow([seller_id, reviewer_id, review])
        print(f'{num_product_reviews} generated')
    return



available_uids = gen_users(num_users)
available_sids = gen_sellers(num_sellers, available_uids)
available_pids = gen_products(num_products, available_sids)
gen_carts(num_carts)
gen_orders(num_orders, available_uids, available_pids, available_sids)
gen_inventory(available_pids)
gen_product_reviews(num_product_reviews, available_pids, available_uids)
gen_seller_reviews(num_seller_reviews, available_sids, available_uids)
