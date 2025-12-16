# Supabase Storage Setup for Product Images

## Step 1: Create a Storage Bucket in Supabase

1. Go to **Supabase Dashboard**: https://app.supabase.com
2. Select your project: **ritaoxbzgiooejjxucwl**
3. Click **Storage** in the left sidebar
4. Click **Create a new bucket**
5. Name it: `plants`
6. Make it **Public** (check the "Public bucket" checkbox)
7. Click **Create bucket**

## Step 2: Upload Product Images to Supabase Storage

1. In the Supabase Storage panel, click on the `plants` bucket
2. Click **Upload file** or drag and drop images
3. Upload all images from your `assets/products/` folder:
   - moon_cactus.jpg
   - pintado.jpg
   - donya_aurora.jpg
   - citronella.jpg
   - pinwheel.jpg
   - sineguelas.jpg
   - bermudagrass.jpg
   - buxus.jpg
   - bougainvillea.jpg
   - miagos.jpg
   - fukientea.jpg
   - pinkrose.jpg
   - mum1.jpg
   - longgan.jpg
   - americanlemon.jpg
   - atsuet.jpg
   - avocado.jpg
   - sagingsaba.jpg
   - calamansi.jpg
   - coffee.jpg
   - mangosteen.jpg
   - sunflower.jpg

## Step 3: Get Public Image URLs

Each uploaded image gets a public URL in this format:
```
https://ritaoxbzgiooejjxucwl.supabase.co/storage/v1/object/public/plants/moon_cactus.jpg
```

**Base URL**: `https://ritaoxbzgiooejjxucwl.supabase.co/storage/v1/object/public/plants/`

**Example**: 
- File: `moon_cactus.jpg`
- Full URL: `https://ritaoxbzgiooejjxucwl.supabase.co/storage/v1/object/public/plants/moon_cactus.jpg`

## Step 4: Update Product Images in Django Admin

1. Go to **Django Admin**: https://oliveoshoppe.onrender.com/admin/
2. Login with admin credentials:
   - Username: `admin`
   - Password: `Admin@2025`
3. Click **Plants** in the left sidebar
4. For each product, edit and update the image field:

### Example Products & Image URLs:

| Product | Image Field Value |
|---------|------------------|
| Moon Cactus | `https://ritaoxbzgiooejjxucwl.supabase.co/storage/v1/object/public/plants/moon_cactus.jpg` |
| Poinsettia (Christmas Flower) | `https://ritaoxbzgiooejjxucwl.supabase.co/storage/v1/object/public/plants/pintado.jpg` |
| Doña Aurora | `https://ritaoxbzgiooejjxucwl.supabase.co/storage/v1/object/public/plants/donya_aurora.jpg` |
| Citronella | `https://ritaoxbzgiooejjxucwl.supabase.co/storage/v1/object/public/plants/citronella.jpg` |
| Crepe Jasmine | `https://ritaoxbzgiooejjxucwl.supabase.co/storage/v1/object/public/plants/pinwheel.jpg` |
| Sineguelas | `https://ritaoxbzgiooejjxucwl.supabase.co/storage/v1/object/public/plants/sineguelas.jpg` |
| Bermuda Grass | `https://ritaoxbzgiooejjxucwl.supabase.co/storage/v1/object/public/plants/bermudagrass.jpg` |
| Boxwood | `https://ritaoxbzgiooejjxucwl.supabase.co/storage/v1/object/public/plants/buxus.jpg` |
| Bougainvillea | `https://ritaoxbzgiooejjxucwl.supabase.co/storage/v1/object/public/plants/bougainvillea.jpg` |
| Golden Miagos | `https://ritaoxbzgiooejjxucwl.supabase.co/storage/v1/object/public/plants/miagos.jpg` |
| Fukien Tea Tree | `https://ritaoxbzgiooejjxucwl.supabase.co/storage/v1/object/public/plants/fukientea.jpg` |
| Pink Rose | `https://ritaoxbzgiooejjxucwl.supabase.co/storage/v1/object/public/plants/pinkrose.jpg` |
| Chrysanthemum | `https://ritaoxbzgiooejjxucwl.supabase.co/storage/v1/object/public/plants/mum1.jpg` |
| Longan Tree | `https://ritaoxbzgiooejjxucwl.supabase.co/storage/v1/object/public/plants/longgan.jpg` |
| American Lemon | `https://ritaoxbzgiooejjxucwl.supabase.co/storage/v1/object/public/plants/americanlemon.jpg` |
| Atsuet | `https://ritaoxbzgiooejjxucwl.supabase.co/storage/v1/object/public/plants/atsuet.jpg` |
| Avocado | `https://ritaoxbzgiooejjxucwl.supabase.co/storage/v1/object/public/plants/avocado.jpg` |
| Banana (Saba) | `https://ritaoxbzgiooejjxucwl.supabase.co/storage/v1/object/public/plants/sagingsaba.jpg` |
| Calamansi | `https://ritaoxbzgiooejjxucwl.supabase.co/storage/v1/object/public/plants/calamansi.jpg` |
| Coffee | `https://ritaoxbzgiooejjxucwl.supabase.co/storage/v1/object/public/plants/coffee.jpg` |
| Mangosteen | `https://ritaoxbzgiooejjxucwl.supabase.co/storage/v1/object/public/plants/mangosteen.jpg` |
| Sunflower | `https://ritaoxbzgiooejjxucwl.supabase.co/storage/v1/object/public/plants/sunflower.jpg` |

## Steps to Update Each Product:

1. Click on a product name
2. In the **Image** field, paste the full Supabase URL (from the table above)
3. Click **Save**
4. Repeat for all 22 products

## Alternative: Update via Admin Dashboard

If you prefer the custom admin dashboard:

1. Go to https://oliveoshoppe.onrender.com/api/admin-dashboard/
2. Click **Manage Products**
3. Edit each product and add the image URL
4. Save changes

## How Images Display on the Shop

Once you update the image URLs in Django admin:

1. The shop page will display product images from Supabase Storage
2. Images load automatically when users browse products
3. Images are cached by CDN for fast loading
4. No image files stored on Render (which can't persist files)

## Advantages of Supabase Storage

✅ **Persistent**: Images survive app redeployments  
✅ **Fast**: CDN-backed delivery  
✅ **Scalable**: Can handle unlimited images  
✅ **Public URLs**: No authentication needed for public images  
✅ **Easy management**: Upload/delete via Supabase dashboard  

## Adding New Products with Images

In the future, when adding new products:

1. Upload image to Supabase Storage `plants` bucket
2. Get the public URL
3. Create product in Django admin with image URL

## Troubleshooting

**Images not showing?**
- Check the URL is correct in Supabase dashboard
- Verify the bucket is set to **Public**
- Clear browser cache (Ctrl+Shift+Delete)
- Check browser console for 404 errors

**URL format wrong?**
- Base: `https://ritaoxbzgiooejjxucwl.supabase.co/storage/v1/object/public/plants/`
- Add image filename: `https://ritaoxbzgiooejjxucwl.supabase.co/storage/v1/object/public/plants/moon_cactus.jpg`

**Can't upload to Supabase?**
- Make sure bucket is **Public**
- Check you have permission to the `plants` bucket
- Try a small test image first
