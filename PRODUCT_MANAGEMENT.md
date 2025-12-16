# Product Images & Database Management

## Admin Credentials

You have 3 admin accounts:

1. **Main Admin**
   - Email: `admin@oliveoshoppe.com`
   - Username: `admin`
   - Password: `Admin@2025`

2. **Gordon College Admin**
   - Email: `202210491@gordoncollege.edu.ph`
   - Username: `gordon_admin`
   - Password: `pagdilaoOO10491`

3. **Testing Admin**
   - Email: `oliveoshoppe.testing@gmail.com`
   - Username: `testing_admin`
   - Password: `pagdilaoOO10491`

## Product Images Storage

### Where images are stored:

1. **Local Development**: `media/plants/` folder
2. **Production (Render)**: Images should be uploaded to **Supabase Storage**

### How to manage product images:

#### Option 1: Upload to Supabase Storage (RECOMMENDED for production)

1. Go to Supabase Dashboard → Storage
2. Create a bucket called `plants`
3. Make it public
4. Upload images from `assets/products/` folder
5. Update product image URLs in admin panel to point to Supabase URLs
   - Format: `https://ritaoxbzgiooejjxucwl.supabase.co/storage/v1/object/public/plants/moon_cactus.jpg`

#### Option 2: Use Django Media Files (for development)

- Images are stored in `media/plants/`
- Django serves them at `/media/plants/moon_cactus.jpg`
- **Note**: Render's free tier doesn't persist uploaded files (they get deleted on redeploy)

## Managing Products in Real-Time

### Via Django Admin Panel:

1. Login at: `https://oliveoshoppe.onrender.com/admin/`
2. Go to **Plants** section
3. You can:
   - Add new products
   - Edit existing products (name, price, stock, images)
   - Delete products
   - Update stock quantities

### Via Custom Admin Dashboard:

1. Login at: `https://oliveoshoppe.onrender.com/api/admin-dashboard/`
2. Manage:
   - Products/plants
   - Orders
   - Inventory levels
   - Sales statistics

### Database Updates:

- All changes are saved **immediately** to Supabase PostgreSQL
- Stock updates happen in real-time when:
  - Customers purchase products
  - Admin updates inventory
- Products are stored in the `api_plant` table

## Initial Product Setup

All 23 products from `oliveoshoppe products.txt` are automatically loaded on deployment:

- Moon Cactus, Poinsettia, Doña Aurora, Citronella, etc.
- Each has: name, price, stock, care instructions, images
- Default stock quantities are set
- Images reference `plants/` folder

## Updating Product Quantities

### Method 1: Django Admin

1. Go to `/admin/api/plant/`
2. Click on a product
3. Update the `Stock` field
4. Click Save

### Method 2: Custom Admin Dashboard

1. Go to `/api/manage/products/`
2. Edit any product
3. Change quantity
4. Submit

### Method 3: Management Command (bulk update)

```bash
python manage.py load_products
```

This re-syncs all products from the hardcoded list.

## Recommended Setup for Production

1. **Upload all images to Supabase Storage**
   - Create `plants` bucket
   - Upload from `assets/products/`
   - Get public URLs

2. **Update image paths in database**
   - Use Django admin to update each product's image field
   - Change from `plants/moon_cactus.jpg` to full Supabase URL

3. **Manage stock via admin panel**
   - Real-time updates
   - Persists in Supabase PostgreSQL
   - Survives redeployments

## Notes

- Supabase PostgreSQL stores all product data (name, price, stock, etc.)
- Images can be in Supabase Storage (recommended) or local media folder (dev only)
- Stock quantities update automatically when orders are placed
- Low stock alerts appear in admin dashboard when stock ≤ 10
