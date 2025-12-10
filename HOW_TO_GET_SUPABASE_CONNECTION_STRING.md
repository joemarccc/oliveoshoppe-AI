# How to Get Your Supabase PostgreSQL Connection String

## Step-by-Step Guide

### Option 1: Via Supabase Dashboard (Easiest)

1. **Go to Supabase Dashboard**
   - Visit: https://app.supabase.com
   - Login with your account

2. **Select Your Project**
   - Click on your **oliveoshoppe** project
   - (If you haven't created a project yet, you'll need to create one first)

3. **Navigate to Database Settings**
   - Click the **Settings** icon (⚙️) in the left sidebar
   - Click **Database** under Settings

4. **Find Connection String**
   - Scroll down to the **Connection string** section
   - You'll see multiple formats:
     - **URI** ← Use this one for Django
     - Postgres
     - JDBC
     - .NET
     - Nodejs

5. **Copy the URI Format**
   - Click on **URI** tab
   - Copy the full connection string that looks like:
   ```
   postgresql://postgres.[PROJECT-REF]:[YOUR-PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
   ```

6. **Replace [YOUR-PASSWORD]**
   - The connection string will have `[YOUR-PASSWORD]` placeholder
   - Replace it with your actual database password
   - **If you forgot your password**, click "Reset Database Password" on the same page

---

## What Your Connection String Should Look Like

### Example Format:
```
postgresql://postgres.abcdefghijklmnop:MySecretPassword123@aws-0-us-west-1.pooler.supabase.com:6543/postgres
```

### Breaking it down:
- `postgresql://` - Protocol
- `postgres.abcdefghijklmnop` - Username (with project reference)
- `MySecretPassword123` - Your database password
- `aws-0-us-west-1.pooler.supabase.com` - Host (Supabase server)
- `6543` - Port (connection pooler)
- `/postgres` - Database name

---

## Alternative: Connection Pooler vs Direct Connection

Supabase provides two connection types:

### 1. **Connection Pooler** (RECOMMENDED for Render)
- Port: `6543`
- Better for serverless/hosted platforms
- Format:
  ```
  postgresql://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres
  ```

### 2. **Direct Connection**
- Port: `5432`
- For local development or long-lived connections
- Format:
  ```
  postgresql://postgres:[password]@db.[ref].supabase.co:5432/postgres
  ```

**For Render deployment, use the Connection Pooler (port 6543)**

---

## If You Don't Have a Supabase Project Yet

### Create a New Project:

1. Go to https://app.supabase.com
2. Click **New Project**
3. Fill in:
   - **Name**: `oliveoshoppe` or any name
   - **Database Password**: Create a strong password (SAVE THIS!)
   - **Region**: Choose closest to your users
   - **Pricing Plan**: Free tier is fine

4. Wait 2-3 minutes for project to initialize

5. Once ready, follow steps above to get connection string

---

## Add Connection String to Your Project

### For Local Development (.env file):

Add to your `.env` file:
```
DATABASE_URL=postgresql://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres
```

### For Render Deployment:

1. Go to Render Dashboard: https://dashboard.render.com
2. Select your `oliveoshoppe` service
3. Go to **Environment** tab
4. Click **Add Environment Variable**
5. Add:
   - **Key**: `DATABASE_URL`
   - **Value**: Paste your Supabase PostgreSQL connection string
6. Click **Save**

Render will automatically redeploy with the new database connection.

---

## Verify Your Connection String

You can test the connection string locally:

```bash
# Install psql (PostgreSQL client)
# On Windows with Chocolatey:
choco install postgresql

# Test connection:
psql "postgresql://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres"
```

If successful, you'll see:
```
postgres=>
```

---

## Update Your .env File

Once you have the real connection string, update your `.env` file:

```dotenv
SECRET_KEY=your-actual-django-secret-key
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,oliveoshoppe.onrender.com,testserver
DATABASE_URL=postgresql://postgres.[YOUR-REF]:[YOUR-PASSWORD]@aws-0-[region].pooler.supabase.com:6543/postgres
SUPABASE_URL=https://[YOUR-REF].supabase.co
SUPABASE_ANON_KEY=your-actual-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-actual-service-role-key
```

---

## Finding Your Supabase Keys

While you're in the Supabase Dashboard:

1. Click **Settings** (⚙️) → **API**
2. Find:
   - **Project URL**: Your `SUPABASE_URL`
   - **anon public**: Your `SUPABASE_ANON_KEY`
   - **service_role secret**: Your `SUPABASE_SERVICE_ROLE_KEY`

Copy these to your `.env` file as well.

---

## Common Issues

### ❌ "Connection refused"
- Check if you copied the full connection string
- Verify password is correct (no brackets)
- Try resetting database password in Supabase

### ❌ "SSL required"
If you get SSL errors, add `?sslmode=require` to the end:
```
postgresql://...postgres?sslmode=require
```

### ❌ "Password authentication failed"
- Reset your database password in Supabase Dashboard
- Make sure you replaced `[YOUR-PASSWORD]` with actual password

---

## Quick Checklist

- [ ] Created/logged into Supabase account
- [ ] Created a project (if new)
- [ ] Found connection string in Settings → Database
- [ ] Copied URI format connection string
- [ ] Replaced `[YOUR-PASSWORD]` with actual password
- [ ] Added to `.env` as `DATABASE_URL`
- [ ] Added to Render environment variables
- [ ] Updated SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY

---

## Need Help?

If you're still stuck, check:
1. Supabase Dashboard → Settings → Database → Connection string section
2. Look for the **URI** tab specifically
3. Click "Reset Database Password" if you forgot it

The connection string is essential for Django to connect to your PostgreSQL database on Render!
