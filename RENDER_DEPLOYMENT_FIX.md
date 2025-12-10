# Render Deployment Configuration

## ✅ Changes Made

Fixed the server 500 error caused by:
1. **Duplicate URL names** - Removed conflicting `name='home'` in api/urls.py
2. **Missing PostgreSQL support** - Added dj-database-url for database configuration
3. **No error handling** - Added try/except to shop_view
4. **Missing DATABASE_URL** - Added to render.yaml

---

## 🔧 Required: Configure DATABASE_URL on Render

### Step 1: Get Your Supabase PostgreSQL URL

1. Go to your Supabase Dashboard: https://app.supabase.com/project/ritaoxbzgiooejjxucwl/settings/database
2. Find **Connection String** section
3. Copy the **URI** format (not the psql command)
4. It should look like:
   ```
   postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres
   ```

### Step 2: Add DATABASE_URL to Render

1. Go to Render Dashboard: https://dashboard.render.com/
2. Click on your **oliveoshoppe** service
3. Go to **Environment** tab
4. Click **Add Environment Variable**
5. Add:
   - **Key**: `DATABASE_URL`
   - **Value**: `your-supabase-postgresql-url-here`
6. Click **Save Changes**

### Step 3: Verify Other Environment Variables

Make sure these are also set:
- ✅ `SECRET_KEY` - Your Django secret key
- ✅ `DEBUG` - Set to `False`
- ✅ `ALLOWED_HOSTS` - `oliveoshoppe.onrender.com`
- ✅ `SUPABASE_URL` - `https://ritaoxbzgiooejjxucwl.supabase.co`
- ✅ `SUPABASE_ANON_KEY` - Your Supabase anon key
- ✅ `SUPABASE_SERVICE_ROLE_KEY` - Your Supabase service role key

### Step 4: Redeploy

After adding DATABASE_URL:
1. Render will **auto-deploy** from the latest GitHub push
2. Or manually: Click **Manual Deploy** → **Deploy latest commit**
3. Wait for build to complete (migrations will run automatically)

---

## 🧪 Testing After Deployment

1. Visit: `https://oliveoshoppe.onrender.com/`
2. You should see:
   - ✅ Shop page loads (even if empty)
   - ✅ No more 500 error
   - ✅ Navbar shows Login/Register buttons
   - ✅ Can browse products (if any exist in DB)

---

## 📝 What Changed

### Database Configuration (`oliveoshoppe/settings.py`)
```python
# Now automatically detects DATABASE_URL
if DATABASE_URL:
    # Production: PostgreSQL from Supabase
    DATABASES = {'default': dj_database_url.parse(DATABASE_URL)}
else:
    # Development: SQLite
    DATABASES = {'default': {'ENGINE': 'sqlite3', 'NAME': 'db.sqlite3'}}
```

### Build Command (`render.yaml`)
```yaml
buildCommand: pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
```
- Now runs **migrations** automatically on each deploy

### Shop View Error Handling (`api/views.py`)
```python
try:
    # Shop logic...
except Exception as e:
    logger.error(f"Shop view error: {str(e)}")
    # Return empty shop with error message
```
- Won't crash the entire site if database query fails

---

## 🚨 Common Issues

### Issue 1: Still getting 500 error
- **Check Render logs**: Dashboard → Logs tab
- **Verify DATABASE_URL** is set correctly
- **Check Supabase URL** has no typos

### Issue 2: Empty shop page
- **Normal!** No plants in database yet
- Go to `/admin/` to add plants
- Or use Django shell to create sample plants

### Issue 3: Static files not loading
- Already handled by WhiteNoise
- Run `python manage.py collectstatic` locally to test

---

## 📊 Next Steps

After site is working:

1. **Add Products**: Login to `/admin/` and create plant products
2. **Create Superuser**: Run in Render shell or locally and sync to DB
3. **Test Registration**: Try the full email confirmation flow
4. **Test Shopping**: Add products to cart, checkout

---

## 💡 Pro Tips

### Creating Superuser on Render
1. Go to Render Dashboard → Shell tab
2. Run:
   ```bash
   python manage.py createsuperuser
   ```
3. Follow prompts to create admin account
4. Login at `/admin/`

### Adding Sample Plants via Shell
```python
from api.models import Plant
Plant.objects.create(
    name="Aloe Vera",
    description="Easy-care succulent plant",
    price=15.99,
    stock=10
)
```

---

## 🆘 Still Not Working?

Share the **Render deployment logs** (last 50 lines) to diagnose:
1. Go to Render Dashboard
2. Click Logs tab
3. Copy last 50-100 lines
4. Look for Python errors or tracebacks
