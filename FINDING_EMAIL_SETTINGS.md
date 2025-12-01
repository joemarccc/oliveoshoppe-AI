# Finding Email Settings in Supabase - Multiple Methods

## Method 1: Direct Link (Fastest)

Go directly to your project's settings:
```
https://app.supabase.com/project/[PROJECT_ID]/settings/email
```

Or try:
```
https://app.supabase.com/project/[PROJECT_ID]/settings/auth
```

---

## Method 2: Navigation from Dashboard

### Step A: Open Project
1. Go to: https://app.supabase.com
2. Click: `oliveoshoppe` project
3. You're now in project dashboard

### Step B: Find Settings
- **Option 1**: Left sidebar bottom → ⚙️ Settings
- **Option 2**: Top right menu → Settings
- **Option 3**: Look for gear icon

### Step C: Find Email
Inside Settings, look for:
- "Email Provider"
- "SMTP"
- "Email Configuration" 
- "Email Templates"
- "Authentication" → "Email"

---

## Method 3: Through Authentication Menu

1. In left sidebar, find: **Authentication**
2. Click: **Authentication**
3. Look for submenu items:
   - Providers
   - Email
   - SMTP
   - Settings
4. Click on "Email" or "SMTP"

---

## Method 4: Search Function

Some Supabase versions have search:
1. Top of page, look for search box
2. Type: "SMTP" or "Email Provider"
3. Should show matching sections
4. Click on result

---

## What You're Looking For

The SMTP configuration form should have these fields:

```
☐ SMTP Host
☐ SMTP Port  
☐ SMTP Username
☐ SMTP Password
☐ Sender Email Address
☐ TLS/SSL Options
```

If you see these fields, you're in the right place!

---

## Common Dashboard Layouts

### Layout A: Settings Tab-Based
```
Settings
├─ General
├─ Account
├─ Email          ← Click here
├─ Database
└─ API
```

### Layout B: Settings Nested
```
Settings
├─ Email Configuration
│  ├─ SMTP Settings    ← Click here
│  ├─ Templates
│  └─ Sender
```

### Layout C: Under Authentication
```
Authentication
├─ Providers
├─ Email            ← Click here
├─ Users
└─ Policies
```

---

## Verification: You Found the Right Place

You're in the right settings when you see:
- ✅ Form fields for SMTP (Host, Port, User, Pass)
- ✅ Option to enter sender email
- ✅ "Save" or "Apply" button
- ✅ Maybe a "Test Connection" button

You're in the WRONG place if you see:
- ❌ Only email templates
- ❌ User email list
- ❌ Confirmation email settings
- ❌ Password reset settings

---

## After Finding Settings

1. Fill in values (copy from below)
2. Click Save
3. Wait for confirmation
4. See green checkmark or success message
5. Settings should persist after page refresh

---

## Copy-Paste Values

Once you find the form, enter these:

**SMTP Host:**
```
smtp.resend.com
```

**SMTP Port:**
```
587
```

**SMTP Username:**
```
resend
```

**SMTP Password:**
```
re_bEehbKJR_JhwbkhzpzyLP5tU8kXpgVxX1
```

**Sender Email:**
```
noreply@oliveoshoppe.com
```

**TLS:** ✅ Enable/On
**SSL:** ❌ Disable/Off

---

## If You Still Can't Find It

### Troubleshooting Steps

1. **Check Supabase version**
   - Dashboard may vary by version
   - Try logging out and back in
   - Try different browser

2. **Check project is correct**
   - Make sure you're in "oliveoshoppe" project
   - Check project ID matches your Supabase URL

3. **Check permissions**
   - Make sure you're project owner
   - Admin users might have access
   - Check with your team lead

4. **Try direct link**
   - Replace [ID] with your actual project ID
   - ID is in URL or project settings
   - Example: 
     ```
     https://app.supabase.com/project/ritaoxbzgiooejjxucwl/settings/email
     ```

5. **Contact Supabase Support**
   - In-app chat on dashboard
   - Email: support@supabase.com
   - Include your project name and what you're looking for

---

## Pro Tips

💡 **Bookmark the settings page** once you find it
```
https://app.supabase.com/project/[PROJECT_ID]/settings/email
```

💡 **Test configuration immediately** after saving
- Use Test button if available
- Or try registration flow

💡 **Keep this document** for future reference
- Same setup for production
- Same SMTP values
- Only update sender email if different

---

## After Configuration

Next steps:
1. Settings saved ✅
2. Wait 1-2 minutes (propagation)
3. Test OTP send
4. Test OTP verify  
5. Test registration
6. Done! 🎉

---

**Any issues?**
- Check SETUP_VERIFICATION_CHECKLIST.md for tests
- Check RESEND_SUPABASE_SETUP.md for detailed guide
- Check Django logs for error messages
