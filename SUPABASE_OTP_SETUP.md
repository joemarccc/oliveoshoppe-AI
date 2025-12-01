# Supabase OTP Configuration Guide

## Problem
You're getting a 404 error on `/auth/verify-otp/` because:
1. Your registration sends OTP codes ✅ (code is correct)
2. But Supabase is sending **confirmation links instead of OTP codes** ❌
3. This means OTP is NOT enabled in your Supabase project

## Solution: Enable OTP in Supabase

### Step 1: Go to Supabase Dashboard
1. Open [https://app.supabase.com](https://app.supabase.com)
2. Select your **oliveoshoppe** project
3. Go to **Authentication → Providers**

### Step 2: Enable Email OTP
1. Click on **Email** provider
2. Scroll down to **Email OTP Settings**
3. Make sure the toggle is **ON** (enabled)
4. Settings should look like:
   - ✅ Enable Email OTP
   - OTP Length: 6 digits
   - OTP Expiry: 3600 seconds (1 hour)

### Step 3: Disable Email Confirmations (Optional)
If you ONLY want OTP (not confirmation links), disable auto-confirm:

1. Still in **Authentication → Providers → Email**
2. Scroll to **Disable Email Confirmations**
3. Toggle this OFF if you want manual confirmation only
4. Keep it ON if you want users confirmed automatically after OTP

**Recommended Settings:**
- ✅ Email OTP Enabled
- ✅ Disable Email Confirmations (toggle OFF) - so users must verify OTP
- Auto-confirm: OFF

### Step 4: Verify URL Redirect Settings
1. Go to **Authentication → URL Configuration**
2. Add your site URLs:
   - Redirect URL: `http://localhost:8000/accounts/register/step2/`
   - Or: `http://localhost:8000` (for general)
3. Make sure no `/auth/verify-otp/` is configured

### Step 5: Set Environment Variables
Ensure your `.env` file has:
```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
SITE_URL=http://localhost:8000
```

## Testing OTP Flow

### Test 1: Send OTP
1. Go to registration: `http://localhost:8000/accounts/register/step1/`
2. Enter your email: `test@example.com`
3. Click "Send Verification Code"
4. Expected: You should receive an email with a **6-digit OTP code**
   - Example: `123456`
   - NOT a confirmation link

### Test 2: Verify OTP
1. Copy the OTP code from email
2. Enter it on Step 2 form
3. Click "Verify Code"
4. Expected: You proceed to Step 3 (Create Account)

### Test 3: Create Account
1. Enter username, password, phone
2. Accept Terms & Conditions
3. Click "Create Account"
4. Expected: Account created, redirected to login

---

## Troubleshooting

### Problem: Still Getting Confirmation Links Instead of OTP Codes

**Solution:**
1. Check if OTP is really enabled in Supabase dashboard
2. Try logging out of Supabase dashboard and logging back in
3. Try refreshing your browser cache
4. The change can take 5-10 minutes to take effect

### Problem: Email Not Arriving

**Solution:**
1. Check spam/junk folder
2. Verify email is typed correctly
3. In Supabase dashboard, check **Auth Logs** for errors:
   - Go to Authentication → Logs
   - Look for your test email
   - Check error messages

### Problem: "Invalid or Expired OTP" Error

**Solution:**
1. Make sure you're copying the code correctly
2. Wait at least 5 seconds after email arrives (Supabase needs time to sync)
3. OTP expires after 3600 seconds (1 hour) - so use it quickly
4. Try the Resend button to get a new code

### Problem: "Page not found (404)" on Email Link

**Solution:**
This means Supabase is still sending confirmation links. 
1. Go back to **Authentication → Providers → Email**
2. Scroll down carefully
3. Look for "Email OTP" or "OTP Settings"
4. Make sure it's toggled ON
5. Wait 5-10 minutes and try again

---

## How OTP Works in Your App

```
User Flow:
┌─────────────────┐
│  Step 1: Email  │  User enters email → Triggers send_otp()
└────────┬────────┘
         │
         ↓ Supabase sends OTP via email
┌─────────────────────────────────────────┐
│ User receives email with 6-digit code   │
│ Example: "Your code is: 123456"         │
└─────────────┬───────────────────────────┘
              │
              ↓ User copies code
┌──────────────────────┐
│ Step 2: Verify OTP   │ User enters code → Triggers verify_otp()
└──────────┬───────────┘
           │
           ↓ Supabase validates
        ✅ Valid? Continue
           │
           ↓
┌───────────────────────────┐
│ Step 3: Create Account    │ User enters username/password
└───────────┬───────────────┘
            │
            ↓
         ✅ Account Created
            │
            ↓
┌─────────────────┐
│ Redirect Login  │
└─────────────────┘
```

---

## Code Flow

### File: `oliveoshoppe/accounts/supabase_auth.py`

**Function: `send_otp(email)`**
```python
# This function:
# 1. Calls supabase.auth.sign_in_with_otp()
# 2. Supabase automatically sends OTP via email
# 3. Returns success/error status

# Email should contain something like:
# "Your OTP code is: 123456
#  This code expires in 1 hour."
```

**Function: `verify_otp(email, token)`**
```python
# This function:
# 1. Takes the 6-digit code user entered
# 2. Calls supabase.auth.verify_otp()
# 3. Validates against Supabase OTP
# 4. Returns user object if valid

# This marks email as verified in Supabase
```

### File: `oliveoshoppe/accounts/views.py`

**View: `register_step1_email()`**
```python
# GET: Shows email input form
# POST: 
#   - Gets email from form
#   - Calls send_otp(email)
#   - Stores email in session
#   - Redirects to Step 2
```

**View: `register_step2_otp()`**
```python
# GET: Shows OTP input form (expects 6 digits)
# POST:
#   - Gets OTP code from form
#   - Calls verify_otp(email, otp_code)
#   - If valid, marks otp_verified=True in session
#   - Redirects to Step 3
```

**View: `register_step3_details()`**
```python
# GET: Shows account details form
# POST:
#   - Validates OTP was verified (checks session)
#   - Gets username/password/phone from form
#   - Creates user in Supabase
#   - Creates user in Django
#   - Clears session
#   - Redirects to login
```

---

## Key Points

✅ **OTP is NOT the same as confirmation link**
- Confirmation link: User clicks link in email (auto-verifies)
- OTP: User receives code in email, manually enters code (requires user action)

✅ **Your Django code is correct**
- It expects OTP codes, not links
- It handles the 3-step flow properly

✅ **Supabase needs to be configured**
- Enable Email OTP in provider settings
- Make sure OTP is the delivery method (not links)

✅ **After OTP is enabled, everything works automatically**
- Supabase handles email delivery
- Your code handles verification flow
- Django creates user locally for app

---

## Next Steps

1. **Go to Supabase Dashboard** and enable OTP
2. **Test the full registration flow** using the test cases above
3. **Check email spam folder** for test emails
4. **Monitor Supabase Auth Logs** for any errors

---

## Need Help?

If OTP still isn't working after enabling:
1. Check Supabase **Auth → Logs** for error messages
2. Verify email settings in Supabase (SMTP configuration)
3. Try resetting browser cache
4. Try a different test email address

**Important**: Supabase free tier includes OTP - no additional cost!

---

## Production Notes

- For production, use your actual domain (not localhost)
- Update `SITE_URL` environment variable
- Ensure email is delivered from a trusted sender
- Monitor OTP send/verify success rates
- Set up error alerts for failed OTP attempts
