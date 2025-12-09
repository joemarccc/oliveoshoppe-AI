# Supabase PostgreSQL Setup for Django

## Step 1: Get Supabase PostgreSQL Connection Details

1. Go to: https://app.supabase.com/project/ritaoxbzgiooejjxucwl/settings/database
2. You'll see the **Connection String** section
3. Look for the **Connection pooler** or **Direct connection** option
   - Use **Connection pooler** for Django (better for web apps): `postgresql://[user]:[password]@[host]:[port]/postgres?sslmode=require`
   - Or **Direct connection** if you prefer

4. Copy the connection string, it will look like:
   ```
   postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres
   ```

5. Extract these details:
   - **Host**: `aws-0-[region].pooler.supabase.com` (or direct connection host)
   - **Port**: `6543` (for pooler) or `5432` (for direct)
   - **Database**: `postgres`
   - **User**: `postgres.[project-ref]`
   - **Password**: Your Supabase database password (shown on the same page)

## Step 2: Add Supabase PostgreSQL to Render Environment Variables

Go to your Render service settings:
1. Dashboard → oliveoshoppe service → Environment
2. Add these variables:

```
DATABASE_URL=postgresql://[user]:[password]@[host]:[port]/postgres?sslmode=require
```

Or add individual variables:
```
DB_ENGINE=django.db.backends.postgresql
DB_HOST=aws-0-[region].pooler.supabase.com
DB_PORT=6543
DB_NAME=postgres
DB_USER=postgres.[project-ref]
DB_PASSWORD=[your-supabase-password]
```

## Step 3: Configure Django settings.py

Django code has been updated to check for PostgreSQL environment variables and use them if available, falling back to SQLite for local development.

## Step 4: Run Migrations on Render

After updating environment variables:
1. Go to Render dashboard
2. Click your service → Manual Deploy or wait for auto-deploy
3. The build command will run: `python manage.py migrate --noinput`
4. All tables will be created in Supabase PostgreSQL

## Step 5: Verify Connection

Once deployed:
1. Visit https://oliveoshoppe.onrender.com
2. Products should load (empty list initially)
3. Check Supabase SQL Editor to verify tables were created:
   - `auth_user`
   - `api_plant`
   - `api_order`
   - `api_cart`
   - etc.

## Troubleshooting

### Connection Refused
- Verify password is correct in Supabase
- Check host/port are correct
- Ensure firewall allows connection

### Migration Errors
- Check Render logs for error messages
- Try connecting with `psql` command line to test

### Database Already Exists
- No action needed - it will migrate existing schema

## Local Development

To test locally with Supabase PostgreSQL:
1. Copy the CONNECTION_POOLER string from Supabase
2. Add to `.env`:
   ```
   DATABASE_URL=postgresql://...
   ```
3. Run: `python manage.py migrate`
4. Run: `python manage.py runserver`

Or keep using local SQLite and only switch to PostgreSQL on Render.

## Security Notes

⚠️ **Never commit your password to git**
- Use Render environment variables (not in code)
- Use `.env` locally (in `.gitignore`)
- The code automatically picks up from environment variables

## Next Steps

1. Get connection details from Supabase
2. Add to Render environment variables
3. Redeploy on Render
4. Verify connection works
