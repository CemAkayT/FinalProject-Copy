from db import app, mysql

def update_product(product_id):
    try:
        with app.app_context():
            cur = mysql.connection.cursor()
            cur.execute("SET NAMES utf8mb4;")
            cur.execute("SET CHARACTER SET utf8mb4;")

            query = """
                DELETE FROM products
                WHERE product_id = %s
            """
            cur.execute(query, (product_id,)) # This is a tuple containing a single element, which is the

            mysql.connection.commit()
            cur.close()
            
            return True
    except Exception as e:
        print(f"Error updating product: {str(e)}")
        return False

if __name__ == "__main__":
    product_id = 2 # just type a product_id to delete from the database

    if update_product(product_id):
        print("Product deleted successfully")
    else:
        print("Failed to delete product")
