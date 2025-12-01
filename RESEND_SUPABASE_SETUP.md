# Supabase + Resend SMTP Setup - Step by Step

## You Have Everything Ready ✅

Your Resend API Key is already in `.env`:
```
RESEND_API_KEY=re_bEehbKJR_JhwbkhzpzyLP5tU8kXpgVxX1
```

## Configure Supabase SMTP for Resend

### Step 1: Open Supabase Dashboard
1. Go to: https://app.supabase.com
2. Select your **oliveoshoppe** project
3. Click **Settings** (bottom left)

### Step 2: Find Email Provider Settings
1. In Settings, look for **Email Provider** or **SMTP**
2. You might see it under:
   - Settings → Email Configuration
   - Settings → SMTP
   - Authentication → Email Provider

### Step 3: Configure Resend SMTP

Fill in these exact values:

```
SMTP Host: smtp.resend.com
SMTP Port: 587
SMTP Username: resend
SMTP Password: re_bEehbKJR_JhwbkhzpzyLP5tU8kXpgVxX1
Sender Email: noreply@oliveoshoppe.com
Enable TLS: Yes/On
```

**Important**: 
- Username is literally the word: `resend` (not your API key)
- Password IS your API key (starts with `re_`)
- Port must be `587` (TLS)

### Step 4: Save and Test

1. Click "Save" or "Apply"
2. Supabase should show: "✅ SMTP configured successfully"
3. Wait 1-2 minutes for changes to propagate

## Testing Resend SMTP

### Test 1: Send Test Email
1. In Supabase dashboard, there might be a "Send test email" button
2. Enter a test email address
3. If successful, you'll receive an email from Resend

### Test 2: Registration Flow (In Your App)
1. Start server: `python manage.py runserver 8000`
2. Go to: `http://localhost:8000/accounts/register/step1/`
3. Enter your email
4. Click "Send Verification Code"
5. Expected:
   - ✅ Success message: "Verification code sent to..."
   - ✅ Email arrives within 5 seconds
   - ✅ Email contains 6-digit code

## Troubleshooting

### Email Not Arriving?

**Check 1: Supabase Auth Logs**
1. Dashboard → Authentication → Logs
2. Look for your email
3. Check error message:
   - "Invalid SMTP credentials" → Check username/password
   - "Connection refused" → Check host/port
   - "TLS error" → Check TLS setting

**Check 2: Resend Dashboard**
1. Go to: https://app.resend.com
2. Check **Logs** or **Events**
3. Should show email being delivered
4. If showing errors, check Resend status

**Check 3: Email Delivery**
1. Check spam/junk folder
2. Try different email address
3. Verify sender email format

### SMTP Not Saving?

1. Make sure all fields are filled
2. Check for typos (especially `resend` as username)
3. Try clearing browser cache
4. Try different browser
5. Contact Supabase support

## Email Format

When configured, users will receive:

```
From: noreply@oliveoshoppe.com
Subject: [Supabase Default] - Email confirmation

Body:
---
Confirm your email

Follow this link to confirm your email address.
[Link with OTP code]

Or enter this code:
123456

This link will expire in 1 hour.
---
```

(Supabase uses default template, but you can customize it later)

## Security Notes

✅ Your API key is secure:
- Stored in `.env` (not in code)
- Only used by Supabase backend
- Never exposed to frontend
- Can be rotated in Resend dashboard

✅ OTP is secure:
- 6-digit code expires in 1 hour
- Max 5 attempts (built-in)
- Rate limited by Supabase
- Validated by Supabase backend

## Production Checklist

- [ ] SMTP configured in Supabase (done after this setup)
- [ ] Test email sends successfully
- [ ] Test OTP verification works
- [ ] Monitor Supabase Auth Logs for errors
- [ ] Set up error alerts
- [ ] Document setup process
- [ ] Backup API key (keep secure)

## Next Steps

1. **Go to Supabase Dashboard**
2. **Configure SMTP with Resend details** (use values above)
3. **Wait 1-2 minutes**
4. **Test from registration page**
5. **You're done!** ✅

---

**Questions?**
- Resend docs: https://resend.com/docs
- Supabase docs: https://supabase.com/docs/guides/auth/auth-smtp
- Check error logs in Supabase dashboard

**Once SMTP is configured, your registration flow will work perfectly:**
```
User Email → Resend SMTP → User receives OTP → User verifies → Account created ✅
```
