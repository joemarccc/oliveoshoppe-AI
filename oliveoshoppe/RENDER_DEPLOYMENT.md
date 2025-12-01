# Deploy Django/Supabase App to Render (Free)

## Step 1: Prepare Your GitHub Repository

1. Make sure your code is pushed to GitHub (public or private repo)
2. Verify these files are in the root directory:
   - `Procfile` ✓ (created)
   - `render.yaml` ✓ (created)
   - `requirements.txt` ✓ (updated with gunicorn + whitenoise)
   - `.env.example` ✓ (created)
   - `.gitignore` (should exclude `.env`)

3. Commit changes:
   ```bash
   git add .
   git commit -m "Setup Render deployment configuration"
   git push
   ```

---

## Step 2: Create Render Account

1. Go to https://render.com
2. Sign up with GitHub (easier for integration)
3. Authorize Render to access your GitHub repos

---

## Step 3: Create a New Web Service

1. Click **"New +"** → **"Web Service"**
2. Select your `oliveoshoppe-AI` repository
3. Configure:
   - **Name**: `oliveoshoppe` (or whatever you want)
   - **Environment**: `Python 3`
   - **Build Command**: 
     ```
     pip install -r requirements.txt
     ```
   - **Start Command**: 
     ```
     gunicorn oliveoshoppe.wsgi:application
     ```
   - **Plan**: `Free` (should be selected by default)

---

## Step 4: Set Environment Variables

In Render dashboard, go to **Environment** and add these variables:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | Generate a strong key: https://djecrety.ir/ |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `your-app-name.onrender.com` (you'll get this URL after deploy) |
| `SUPABASE_URL` | Your Supabase project URL |
| `SUPABASE_ANON_KEY` | Your Supabase anon key |
| `SUPABASE_SERVICE_ROLE_KEY` | Your Supabase service role key |

**Optional (for email):**
| Key | Value |
|-----|-------|
| `EMAIL_HOST_USER` | Your Gmail address |
| `EMAIL_HOST_PASSWORD` | Your Gmail app password |

---

## Step 5: Deploy!

1. Click **"Create Web Service"**
2. Render will build and deploy your app
3. Wait for the build to complete (5-10 minutes)
4. Once live, you'll get a URL like: `https://oliveoshoppe.onrender.com`

---

## Step 6: Update ALLOWED_HOSTS

1. After your app URL is generated, update Render environment:
   - Set `ALLOWED_HOSTS` to your actual URL (e.g., `oliveoshoppe.onrender.com`)
2. Render will auto-redeploy with updated settings

---

## Step 7: Run Database Migrations (if needed)

If you're using PostgreSQL or need to migrate data:

1. Go to your Render service dashboard
2. Click **"Shell"** tab
3. Run:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

---

## Common Issues & Fixes

### Issue: "Static files not found"
**Solution**: WhiteNoise should handle this. Ensure `STATICFILES_STORAGE` is set in settings.py ✓

### Issue: "Module not found" errors
**Solution**: Update `requirements.txt` with all dependencies ✓

### Issue: "Email not working"
**Solution**: Either enable Supabase email confirmations OR configure SMTP in Render env vars

### Issue: "Database not found"
**Solution**: For free tier, SQLite works fine. For PostgreSQL, Render offers free databases via add-ons

---

## Redeploy on Code Changes

Whenever you push to GitHub, Render automatically redeploys (if auto-deploy is enabled). You can also manually trigger redeploy from the Render dashboard.

---

## Next Steps

1. Test your app at `https://your-app-name.onrender.com`
2. Try the registration flow
3. Check logs in Render dashboard if issues occur
4. Configure email (Supabase or SMTP) for production
5. Add custom domain (optional)

---

## Support

- Render Docs: https://render.com/docs/deploy-django
- Django Deployment: https://docs.djangoproject.com/en/5.0/howto/deployment/
