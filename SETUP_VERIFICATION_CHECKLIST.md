# Supabase + Resend OTP Integration - Verification Checklist

## Pre-Setup Verification ✅

### Your Current Setup
- ✅ Django application: Ready
- ✅ OTP functions: Updated (use Supabase directly)
- ✅ Registration views: 3-step flow ready
- ✅ Resend API Key: `re_bEehbKJR_JhwbkhzpzyLP5tU8kXpgVxX1`
- ✅ Supabase account: Connected

### What Needs To Happen Now
- ⏳ SMTP configuration in Supabase (YOU need to do this)
- ⏳ Test email delivery
- ⏳ Full registration flow test

---

## Supabase Dashboard Configuration

### Location: Settings → Email Provider

```
┌─ Supabase Dashboard
│
└─ Settings (bottom left)
   │
   └─ Email / SMTP Settings
      │
      └─ SMTP Configuration
```

### Configuration Values

| Field | Value |
|-------|-------|
| SMTP Host | `smtp.resend.com` |
| SMTP Port | `587` |
| SMTP Username | `resend` |
| SMTP Password | `re_bEehbKJR_JhwbkhzpzyLP5tU8kXpgVxX1` |
| Sender Email | `noreply@oliveoshoppe.com` |
| Use TLS | ✅ Yes/On |
| Use SSL | ❌ No/Off |

### Important Notes

⚠️ **Username is NOT your API key**
- Username must be exactly: `resend`
- Password IS your API key

⚠️ **Port must be 587**
- TLS port (not 25 or 465)
- Resend requires TLS

⚠️ **Sender email format**
- Format: `noreply@oliveoshoppe.com`
- Or: `OliveOshoppe <noreply@oliveoshoppe.com>`
- Must be valid email format

---

## Step-by-Step Configuration

### 1. Open Supabase Dashboard
```
https://app.supabase.com
→ Click your oliveoshoppe project
```

### 2. Go to Settings
```
Left sidebar → Settings (at bottom)
```

### 3. Find Email Configuration
```
Look for one of these sections:
- Email Provider
- SMTP Settings
- Email Configuration
- Auth Email Settings

(Different versions may have different names)
```

### 4. Enter Resend SMTP Details
```
SMTP Host:     smtp.resend.com
SMTP Port:     587
Username:      resend
Password:      re_bEehbKJR_JhwbkhzpzyLP5tU8kXpgVxX1
From Email:    noreply@oliveoshoppe.com
TLS:           Enable/On
```

### 5. Save Configuration
```
Click "Save" or "Apply"
Wait for confirmation message
```

### 6. Test Connection
```
Some dashboards have "Test SMTP" button
If available, click it to verify configuration
```

---

## Verification Tests

### Test 1: SMTP Connection ✓
**Goal**: Verify Supabase can connect to Resend

**Where**: Supabase Dashboard → Auth Logs
**What to look for**: 
- No connection errors
- No timeout errors
- No "Invalid credentials" errors

**If error**: Check username/password/host/port

---

### Test 2: Test Email Send ✓
**Goal**: Verify Resend can send emails

**Where**: Supabase Dashboard (if test button available)
**Steps**:
1. Enter test email address
2. Click "Send Test Email"
3. Check inbox within 30 seconds

**Expected**: Email arrives with test content

**If not arrived**: 
1. Check spam folder
2. Check Resend dashboard logs
3. Verify sender email is correct

---

### Test 3: OTP Send ✓
**Goal**: Verify OTP emails actually arrive to users

**Steps**:
1. Open app: `http://localhost:8000/accounts/register/step1/`
2. Enter your email
3. Click "Send Verification Code"
4. Check email inbox

**Expected**: 
- ✅ Page shows success message
- ✅ Email arrives within 5 seconds
- ✅ Email contains 6-digit OTP code
- ✅ Code is properly formatted

**If not working**:
1. Check browser console for errors
2. Check Django logs for error messages
3. Check Supabase Auth Logs for OTP errors
4. Check Resend dashboard for delivery issues

---

### Test 4: OTP Verification ✓
**Goal**: Verify OTP verification works end-to-end

**Steps**:
1. Copy 6-digit code from email
2. Go to Step 2 form (should be automatic)
3. Enter OTP code
4. Click "Verify Code"

**Expected**:
- ✅ Code accepted
- ✅ Success message shown
- ✅ Redirected to Step 3
- ✅ Email displayed as verified

**If fails**:
- Invalid code? → Try copying again (remove spaces)
- Expired? → Request new code (button at bottom)
- Still failing? → Check Supabase Auth Logs

---

### Test 5: Complete Registration ✓
**Goal**: Full end-to-end registration test

**Steps**:
1. Step 1: Enter email → Send code
2. Step 2: Receive code → Verify code
3. Step 3: Enter username/password → Create account
4. Login: Use new credentials

**Expected**:
- ✅ All 3 steps complete successfully
- ✅ Account created in Supabase
- ✅ Can login with credentials
- ✅ User appears in Django admin

**If fails at any step**: See specific test above

---

## Troubleshooting Guide

### Scenario 1: "Error sending code"

**Possible causes**:
1. SMTP not configured → Configure now
2. SMTP credentials wrong → Verify each field
3. SMTP connection failed → Check port/host
4. Email service down → Check Resend status

**Solution**:
- [ ] Check all SMTP fields are correct
- [ ] Verify port is 587 (not 25)
- [ ] Verify TLS is enabled
- [ ] Check Supabase Auth Logs
- [ ] Try again after 1 minute

---

### Scenario 2: Email Not Arriving

**Possible causes**:
1. Email sent but delivery failed
2. In spam folder
3. Email address invalid
4. Rate limited (too many requests)

**Solution**:
- [ ] Check spam/junk folder
- [ ] Try different email address
- [ ] Check Supabase Auth Logs
- [ ] Check Resend dashboard logs
- [ ] Wait 5 minutes and try again

---

### Scenario 3: "Invalid verification code"

**Possible causes**:
1. Code typed wrong
2. Code expired (>1 hour old)
3. Too many attempts (>5)
4. Code already used

**Solution**:
- [ ] Copy code carefully (no spaces)
- [ ] Use code within 1 hour
- [ ] Request new code if expired
- [ ] Check you didn't exceed 5 attempts

---

### Scenario 4: SMTP Configuration Won't Save

**Possible causes**:
1. Invalid values entered
2. Typo in credentials
3. Browser cache issue
4. Form validation error

**Solution**:
- [ ] Double-check all values
- [ ] Special attention to username: `resend` (not API key)
- [ ] Clear browser cache: Ctrl+Shift+Delete
- [ ] Try different browser
- [ ] Try incognito/private window

---

## Dashboard Locations by Supabase Version

### Supabase v2.0+
```
Settings (left sidebar)
→ Email Provider
→ SMTP Configuration
```

### Supabase v1.x
```
Settings (left sidebar)
→ Email
→ SMTP Settings
```

### If You Can't Find It
1. Go to: https://app.supabase.com
2. Select project
3. In top search, type: "SMTP" or "Email"
4. Should jump to correct section

---

## Quick Reference Card

**Copy these values exactly:**

```
Host:      smtp.resend.com
Port:      587
User:      resend
Pass:      re_bEehbKJR_JhwbkhzpzyLP5tU8kXpgVxX1
From:      noreply@oliveoshoppe.com
TLS:       On
SSL:       Off
```

---

## Success Indicators

✅ You'll know it's working when:

1. **SMTP Configuration Saved**
   - Green checkmark or success message
   - Settings persist after refresh

2. **OTP Emails Arrive**
   - Email in inbox within 5 seconds
   - From: `noreply@oliveoshoppe.com`
   - Contains 6-digit code

3. **Registration Complete**
   - All 3 steps work
   - Account created
   - Can login immediately

4. **No Errors**
   - Django console: No error messages
   - Supabase Logs: No "OTP send" errors
   - Resend dashboard: Email delivered

---

## Next: What to Do Now

1. **Open Supabase Dashboard**: https://app.supabase.com
2. **Find Settings → Email Provider**
3. **Enter SMTP values** (copy from table above)
4. **Save configuration**
5. **Wait 1-2 minutes** (propagation time)
6. **Test from app** (Step 3 test above)
7. **Complete registration** (Step 5 test above)

---

**You're almost there!** Just need to configure SMTP in Supabase dashboard. 🎉

Once done, the entire OTP registration flow will work automatically.
