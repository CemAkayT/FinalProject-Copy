from db import app, mysql


def update_product(product_id, title, description, price, section, image_path):
    try:
        with app.app_context():
            cur = mysql.connection.cursor()
            cur.execute("SET NAMES utf8mb4;")
            cur.execute("SET CHARACTER SET utf8mb4;")

            # Update the product data
            query = """
                UPDATE products
                SET title = %s, description = %s, price = %s, section = %s, image_path = %s
                WHERE product_id = %s
            """
            values = (title, description, price, section, image_path, product_id)
            cur.execute(query, values)

            mysql.connection.commit()
            cur.close()

            return True
    except Exception as e:
        print(f"Error updating product: {str(e)}")
        return False


if __name__ == "__main__":
    product_id = 2
    new_title = "Coca Cola 0.33 L"
    new_description = "Iskold Cola"
    new_price = 14
    new_section = "Drikkevarer"
    new_image_path = "/static/images/cola.jpeg"

    if update_product(
        product_id, new_title, new_description, new_price, new_section, new_image_path
    ):
        print("Product updated successfully")
    else:
        print("Failed to update product")
