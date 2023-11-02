from db import app, mysql

def insert_product(title, description, price, category, image_path):
    try:
        with app.app_context():
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO products (title, description, price, category, image_path) VALUES (%s, %s, %s, %s, %s)",
                (title, description, price, category, image_path),
            )
            mysql.connection.commit()
            cur.close()
            return True
    except Exception as e:
        print(f"Error inserting product: {str(e)}")
        return False


if __name__ == "__main__":
    title = "Fanta"
    description = "Mexicansk inspireret med jalapeno og guacamole"
    price = 9.99
    category = "Drikkevarer"
    image_path = "/static/images/fanta.jpeg"

    if insert_product(title, description, price, category, image_path):
        print("Product inserted successfully")
    else:
        print("Failed to insert product")
