# Supabase Email Confirmation Fix - Complete Guide

## ✅ Current Status
- ✅ Code is correct and ready
- ✅ Registration flow: Step 1 → Email sent → Click link → Step 3
- ❌ Supabase dashboard not configured (sending localhost links)

---

## 🔧 Required Supabase Dashboard Changes

### 1. Fix Site URL (CRITICAL)
**This controls the base URL in confirmation emails**

1. Go to: https://app.supabase.com/project/ritaoxbzgiooejjxucwl/settings/auth
2. Find: **Site URL**
3. Change from: `http://localhost:3000`
4. Change to: `https://oliveoshoppe.onrender.com`
5. Click **Save**

---

### 2. Fix Redirect URLs (CRITICAL)
**This controls where emails redirect after clicking**

1. In same page: **Redirect URLs** section
2. **Remove** these:
   - `http://localhost:3000/**`
   - `http://127.0.0.1:3000/**`
   - Any other localhost URLs

3. **Add** these:
   - `https://oliveoshoppe.onrender.com/**`
   - `https://oliveoshoppe.onrender.com/auth/confirm/`
   - `https://oliveoshoppe.onrender.com/accounts/**`

4. Click **Save**

---

### 3. Fix Email Template (CRITICAL)
**This is the HTML users receive**

1. Go to: **Authentication** → **Email Templates**
2. Click: **Confirm signup**
3. **Replace the entire template** with this:

```html
<h2>Welcome to Olive Oshoppe! 🌿</h2>

<p>Hi there!</p>

<p>Thank you for signing up. Please click the button below to confirm your email address and complete your registration:</p>

<p style="text-align: center; margin: 30px 0;">
  <a href="{{ .ConfirmationURL }}" 
     style="background-color: #2c5530; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold;">
    Confirm Your Email
  </a>
</p>

<p>Or copy and paste this link into your browser:</p>
<p style="word-break: break-all; color: #666;">{{ .ConfirmationURL }}</p>

<p style="margin-top: 30px; color: #999; font-size: 12px;">
  If you didn't sign up for Olive Oshoppe, you can safely ignore this email.
</p>

<p style="color: #999;">
  Thanks,<br>
  The Olive Oshoppe Team
</p>
```

4. Click **Save**

**IMPORTANT**: Do NOT modify `{{ .ConfirmationURL }}` - Supabase automatically generates the correct URL with tokens.

---

### 4. Verify Email Provider Settings

1. Go to: **Settings** → **Authentication**
2. Scroll to: **Email Provider** or **SMTP Settings**
3. Choose ONE option:

#### Option A: Use Supabase's Built-in Email (EASIEST)
- Make sure **"Use Supabase SMTP"** is selected
- No configuration needed
- Works immediately

#### Option B: Use Custom SMTP (e.g., Resend)
If you want branded emails:
```
SMTP Host: smtp.resend.com
SMTP Port: 587
Username: resend
Password: re_bEehbKJR_JhwbkhzpzyLP5tU8kXpgVxX1
Sender Email: noreply@oliveoshoppe.com
Enable TLS: Yes
```

5. Click **Save**

---

## 🧪 Testing the Fix

### Test 1: Send New Confirmation Email
1. Go to: https://oliveoshoppe.onrender.com/accounts/register/step1/
2. Enter email: `joemarcpagdilao@gmail.com`
3. Click: **Send Confirmation Link**
4. Check logs for: `Confirmation email sent to...`

### Test 2: Check Email
1. Open inbox (check spam/junk too)
2. Look for email from Supabase or `noreply@oliveoshoppe.com`
3. Verify the link shows: `https://oliveoshoppe.onrender.com/auth/confirm/...`
4. **NOT**: `http://localhost:3000/...`

### Test 3: Click Confirmation Link
1. Click the button/link in email
2. Should see: Loading spinner → "Email Confirmed!" message
3. Auto-redirects to: Step 3 (Complete Registration)
4. URL should be: `https://oliveoshoppe.onrender.com/accounts/register/step3/`

### Test 4: Complete Registration
1. Enter username
2. Enter password (twice)
3. Enter phone number
4. Click: **Complete Registration**
5. Should redirect to home page
6. User created successfully ✅

---

## 🔍 Verification Checklist

Before testing:
- [ ] Site URL = `https://oliveoshoppe.onrender.com`
- [ ] Redirect URLs include production domain
- [ ] No localhost URLs in Redirect URLs
- [ ] Email template uses `{{ .ConfirmationURL }}` only
- [ ] Email provider configured (Supabase SMTP or custom)
- [ ] All settings saved (check for unsaved changes indicator)

---

## 🚨 Common Issues & Solutions

### Issue 1: Email still shows localhost
**Cause**: Site URL not updated in Supabase
**Fix**: Update Site URL to `https://oliveoshoppe.onrender.com` and save

### Issue 2: No email received
**Cause**: SMTP not configured
**Fix**: Enable Supabase's built-in SMTP or configure Resend

### Issue 3: Email arrives but link broken
**Cause**: Redirect URLs don't include production domain
**Fix**: Add `https://oliveoshoppe.onrender.com/**` to Redirect URLs

### Issue 4: "Invalid token" error
**Cause**: Token expired (valid for 1 hour) or wrong Site URL
**Fix**: Request new confirmation email after fixing Site URL

### Issue 5: Redirects to localhost after clicking
**Cause**: Old email with old link
**Fix**: Request NEW email after updating Supabase settings

---

## 📊 Expected Flow

```
User Flow:
┌─────────────────────────────────────────────────────┐
│ 1. User enters email on Step 1                      │
│    https://oliveoshoppe.onrender.com/register/step1 │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│ 2. Django calls Supabase sign_up()                  │
│    - Generates confirmation token                   │
│    - Sends email via SMTP                          │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│ 3. User receives email with link:                   │
│    https://oliveoshoppe.onrender.com/auth/confirm/  │
│    #access_token=xyz&refresh_token=abc              │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│ 4. User clicks link → auth_confirm.html loads       │
│    - JavaScript extracts tokens from URL hash       │
│    - Calls /auth/confirm/verify/ API               │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│ 5. Backend verifies token with Supabase             │
│    - Stores email in session                        │
│    - Sets email_verified = True                     │
│    - Returns success JSON                           │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│ 6. JavaScript auto-redirects to Step 3              │
│    https://oliveoshoppe.onrender.com/register/step3 │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│ 7. User completes profile (username/password/phone) │
│    - Creates user in Supabase                       │
│    - Creates user in Django                         │
│    - Redirects to home                              │
└─────────────────────────────────────────────────────┘
```

---

## 📝 After Configuring Supabase

### Test the complete flow:
1. Clear browser cookies/session
2. Go to registration step 1
3. Enter email
4. Check email inbox
5. Click confirmation link (should show production URL)
6. Verify auto-redirect to step 3
7. Complete registration
8. Login successfully ✅

---

## 🎯 Key Points

1. **Site URL** controls the base domain in emails
2. **Redirect URLs** control where links can redirect to
3. **Email Template** must use `{{ .ConfirmationURL }}` (Supabase variable)
4. **SMTP** must be configured to actually send emails
5. **Old emails won't work** - request new email after fixing settings

---

## 💡 Production Best Practices

Once working:
- ✅ Remove all localhost URLs from Supabase
- ✅ Set token expiry to reasonable time (default 1 hour)
- ✅ Monitor email delivery in Supabase logs
- ✅ Test with multiple email providers (Gmail, Outlook, Yahoo)
- ✅ Check spam folder handling
- ✅ Add custom domain email later (e.g., noreply@oliveoshoppe.com)

---

## 🆘 Still Not Working?

### Debug Steps:
1. Check Render logs: `https://dashboard.render.com/`
2. Check Supabase logs: **Authentication** → **Logs**
3. Verify environment variables in Render:
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`
   - `SUPABASE_SERVICE_ROLE_KEY`
4. Test locally first with ngrok or similar
5. Contact Supabase support if emails still not sending

---

## 📞 Support

If issues persist:
- Supabase Discord: https://discord.supabase.com
- Supabase Support: https://supabase.com/support
- Check Supabase Status: https://status.supabase.com
