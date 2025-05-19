# E-commerce Admin API

A FastAPI-based backend API for e-commerce admin dashboard that provides detailed insights into sales, revenue, and inventory management.

## Features

- Sales Status and Analysis
  - Retrieve and filter sales data
  - Revenue analysis (daily, weekly, monthly, annual)
  - Period and category comparison
  - Sales data by date range, product, and category

- Inventory Management
  - Current inventory status
  - Low stock alerts
  - Inventory level updates
  - Change tracking

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd e-commerce-admin-api
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/ecommerce_db
SECRET_KEY=your-secret-key
```

5. Initialize the database:
```bash
python scripts/init_db.py
```

6. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Interactive API documentation: `http://localhost:8000/docs`
- Alternative API documentation: `http://localhost:8000/redoc`

### Main Endpoints

#### Sales Endpoints
- `GET /api/sales/` - Get all sales data
- `GET /api/sales/revenue/` - Get revenue analysis
- `GET /api/sales/compare/` - Compare revenue across periods
- `GET /api/sales/by-date/` - Get sales by date range
- `GET /api/sales/by-product/` - Get sales by product
- `GET /api/sales/by-category/` - Get sales by category

#### Inventory Endpoints
- `GET /api/inventory/` - Get current inventory status
- `GET /api/inventory/alerts/` - Get low stock alerts
- `PUT /api/inventory/{product_id}` - Update inventory levels
- `GET /api/inventory/history/{product_id}` - Get inventory change history

#### Product Endpoints
- `POST /api/products/` - Register new product
- `GET /api/products/` - Get all products
- `GET /api/products/{product_id}` - Get product details
- `PUT /api/products/{product_id}` - Update product
- `DELETE /api/products/{product_id}` - Delete product

## Database Schema

The database consists of the following main tables:

1. `products`
   - id (Primary Key)
   - name
   - description
   - price
   - category_id (Foreign Key)
   - created_at
   - updated_at

2. `categories`
   - id (Primary Key)
   - name
   - description

3. `inventory`
   - id (Primary Key)
   - product_id (Foreign Key)
   - quantity
   - low_stock_threshold
   - last_updated

4. `inventory_history`
   - id (Primary Key)
   - inventory_id (Foreign Key)
   - previous_quantity
   - new_quantity
   - change_type
   - timestamp

5. `sales`
   - id (Primary Key)
   - product_id (Foreign Key)
   - quantity
   - unit_price
   - total_amount
   - sale_date
   - created_at

## Demo Data

The project includes a script to populate the database with sample data. Run:
```bash
python scripts/seed_data.py
```

This will create sample products, categories, inventory records, and sales data for testing purposes. 