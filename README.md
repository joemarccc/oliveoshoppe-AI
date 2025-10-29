# Olive O'Shoppe - Plant Store

A Django-based e-commerce platform for selling plants with separate user and admin interfaces.

## Features

### Authentication & Role Separation

- User registration with role selection (normal user/staff)
- Role-based login and dashboard routing
- Staff/admin users get access to admin dashboard
- Normal users are directed to user dashboard

### Product Management

#### Product Model Fields:
- Name (CharField)
- Description (TextField)
- Price (DecimalField)
- Stock (IntegerField)
- Image (ImageField, optional)

#### Admin Features:
- Full CRUD operations for products
- Stock management
- Image upload with validation (2MB limit)
- Custom admin dashboard

#### User Features:
- View available products (stock > 0)
- Search and filter products
- Sort by name and price
- Pagination (12 items per page)

### Cart and Checkout

#### Cart Features:
- Add products to cart
- Update quantities
- Remove items
- View cart total
- Stock validation

#### Checkout Process:
- Review order summary
- Enter shipping information
- Stock verification
- Order confirmation
- Stock reduction on successful checkout

### Views & Templates

#### Admin Views:
- Admin dashboard
- Product management
- Order management
- User management
- Inventory control

#### User Views:
- User dashboard
- Product catalog
- Cart management
- Checkout process
- Order history

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd oliveoshoppe
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Usage

### Admin/Staff Access

1. Register as staff/admin or use superuser account
2. Access admin features at `/admin/`
3. Manage products, orders, and users
4. Monitor inventory and sales

### Normal User Access

1. Register as a normal user
2. Browse available products
3. Add items to cart
4. Complete checkout process
5. View order history

## Security Features

- Role-based access control
- Image upload validation
- Stock validation
- CSRF protection
- Password hashing
- Session management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 