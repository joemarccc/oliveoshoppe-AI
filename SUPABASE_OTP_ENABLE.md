# Supabase OTP Configuration - Direct Setup

## Your Code Now Uses Supabase Directly ✅

Your Django app is now configured to use Supabase's native OTP functionality WITHOUT any external email services (Resend, Gmail SMTP, etc).

## How It Works

```
User Registration Flow:
1. User enters email → send_otp(email)
2. Supabase generates 6-digit OTP code
3. Supabase sends OTP via EMAIL (you must configure SMTP in Supabase)
4. User receives email with code
5. User enters code → verify_otp(email, code)
6. Supabase verifies code and creates user
7. Account created ✅
```

## Required Setup in Supabase Dashboard

### Step 1: Configure SMTP for Email Delivery

**Problem**: Supabase needs SMTP to send OTP emails. Without SMTP configured, emails won't be sent.

**Solution**: Configure your email provider's SMTP in Supabase.

1. Go to: https://app.supabase.com
2. Select your **oliveoshoppe** project
3. Go to: **Authentication → Email Templates** OR **Settings → Email Providers**
4. Look for **SMTP Configuration** or **Email Provider Settings**
5. Configure ONE of these options:

#### Option A: Use Gmail SMTP (Recommended for Testing)
```
SMTP Host: smtp.gmail.com
SMTP Port: 587
SMTP Username: your-email@gmail.com
SMTP Password: your-app-specific-password (not regular password)
Sender Email: noreply@oliveoshoppe.com (or your email)
```

**How to get Gmail App Password**:
1. Go to: https://myaccount.google.com/apppasswords
2. Select "Mail" and "Windows Computer"
3. Copy the 16-character password
4. Use that in SMTP Password field

#### Option B: Use Resend (Better for Production)
```
SMTP Host: smtp.resend.com
SMTP Port: 587
SMTP Username: resend
SMTP Password: re_bEehbKJR_JhwbkhzpzyLP5tU8kXpgVxX1 (your RESEND_API_KEY)
Sender Email: noreply@oliveoshoppe.com
```

#### Option C: Use SendGrid
```
SMTP Host: smtp.sendgrid.net
SMTP Port: 587
SMTP Username: apikey
SMTP Password: SG.xxxxxxxxxxxxx (your SendGrid API key)
Sender Email: noreply@oliveoshoppe.com
```

### Step 2: Enable OTP in Authentication Settings

1. Go to: **Authentication → Providers**
2. Click on **Email**
3. Scroll down to **OTP Settings** or **Enable Email OTP**
4. Make sure toggle is **ON**
5. Verify settings:
   - OTP Length: 6 digits
   - OTP Expiry: 3600 seconds (1 hour)
   - Auto-confirm users: OFF (if you want manual verification)

### Step 3: Verify Email Template (Optional)

1. Go to: **Authentication → Email Templates**
2. Look for **OTP** or **Verification Code** template
3. This is what users will receive in their email
4. Default template should work, or customize if needed

## Testing the OTP Flow

Once SMTP is configured in Supabase:

### Test 1: Send OTP
1. Go to: `http://localhost:8000/accounts/register/step1/`
2. Enter email: `test@example.com`
3. Click "Send Verification Code"
4. Expected result:
   - ✅ Message: "Verification code sent to test@example.com"
   - ✅ Email arrives in inbox with 6-digit code (within 5 seconds)

### Test 2: Verify OTP
1. Copy the 6-digit code from email
2. Enter code on Step 2 page
3. Click "Verify Code"
4. Expected result:
   - ✅ Message: "Email verified successfully!"
   - ✅ Redirected to Step 3 (Create Account)

### Test 3: Create Account
1. Enter username, password, phone
2. Accept Terms & Conditions
3. Click "Create Account"
4. Expected result:
   - ✅ Account created
   - ✅ Redirected to login page

## Troubleshooting

### Problem: "Error sending code" or Email Not Arriving

**Solution Checklist**:
1. ✅ SMTP is configured in Supabase dashboard
2. ✅ SMTP credentials are correct
3. ✅ OTP is enabled in Email provider settings
4. ✅ Check Supabase **Auth → Logs** for error messages
5. ✅ Wait 5-10 minutes (sometimes takes time to activate)
6. ✅ Try different email address
7. ✅ Check spam/junk folder

**If still not working**:
- Go to Supabase Auth Logs
- Look for error message
- Common errors:
  - "Invalid SMTP credentials" → Check SMTP password
  - "SMTP connection timeout" → Check SMTP host/port
  - "Email service disabled" → Enable OTP in providers

### Problem: "Invalid verification code"

**Solution**:
1. Copy code carefully (no spaces)
2. Wait 2-3 seconds after receiving email (Supabase needs time to sync)
3. Don't wait too long - OTP expires in 1 hour
4. Try resending code if expired

### Problem: "Email delivery failed" in Supabase Logs

**Solution**:
1. Check sender email is valid
2. Check recipient email is valid
3. Try a different email address to test
4. Verify SMTP credentials again

## Environment Variables (Already Configured)

Your `.env` file already has:
```bash
SUPABASE_URL=https://ritaoxbzgiooejjxucwl.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

No additional configuration needed in Django. Everything is handled by Supabase!

## Code Changes Made

### File: `oliveoshoppe/accounts/supabase_auth.py`

**Function: `send_otp(email)`**
- Calls `supabase.auth.sign_in_with_otp()`
- Supabase generates and sends OTP
- Returns success/error status

**Function: `verify_otp(email, token)`**
- Calls `supabase.auth.verify_otp()`
- Verifies 6-digit code
- Returns user object if valid
- User-friendly error messages

## Important Notes

✅ **Supabase handles everything**:
- OTP generation (random 6 digits)
- OTP storage (secure)
- OTP expiration (1 hour default)
- Email delivery (via SMTP)
- OTP validation

✅ **Your Django app**:
- Shows user the form
- Gets user input
- Calls Supabase functions
- Redirects on success/error

✅ **No external dependencies**:
- No Resend needed (removed)
- No Gmail SMTP hacks needed
- Pure Supabase OTP

## Next Steps

1. **Configure SMTP in Supabase** (choose Gmail, Resend, or SendGrid)
2. **Test sending OTP** from registration page
3. **Verify code receives** in your email
4. **Complete full registration flow** (Step 1 → Step 2 → Step 3)
5. **Test login** with newly created account

## Production Checklist

Before deploying to production:
- [ ] Test OTP with real email addresses
- [ ] Monitor Supabase Auth Logs for errors
- [ ] Verify SMTP is working reliably
- [ ] Set up email alerts for high error rates
- [ ] Document SMTP credentials (keep secure)
- [ ] Test resend functionality
- [ ] Test expired OTP handling
- [ ] Test too many attempts handling

## Support

If you need help:
1. Check Supabase docs: https://supabase.com/docs/guides/auth/otp
2. Check Supabase Auth Logs for error details
3. Try a test email with logging enabled
4. Verify all SMTP settings are correct

---

**Status**: ✅ Django code ready for Supabase OTP
**Pending**: Configure SMTP in Supabase dashboard
