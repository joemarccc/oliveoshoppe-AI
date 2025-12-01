# UI Testing Guide - OliveOshoppe

## 🚀 Quick Access URLs

Start the server first:
```powershell
C:\Users\Joemarc\env\env\Scripts\Activate.ps1
cd oliveoshoppe
python manage.py runserver
```

Server runs at: **http://127.0.0.1:8000/**

### Authentication Pages

| Page | URL | Features |
|------|-----|----------|
| Login | `http://127.0.0.1:8000/accounts/login/` | Two-column layout, Google OAuth, password reset |
| Register | `http://127.0.0.1:8000/accounts/register/` | Phone field, password requirements, Google OAuth |
| Logout | `/accounts/logout/` | Redirects to login page |

### Admin Interface

| Page | URL | Features |
|------|-----|----------|
| Admin Home | `http://127.0.0.1:8000/admin/` | Dashboard with app access |
| Plants | `http://127.0.0.1:8000/admin/api/plant/` | Plant management with image previews |
| Products | `http://127.0.0.1:8000/admin/api/product/` | Product management |

## 📋 Visual Testing Checklist

### Login Page (`/accounts/login/`)

**Desktop View (> 768px)**
- [ ] Sidebar image visible on left
- [ ] Green gradient background
- [ ] Two-column layout displayed
- [ ] Login form on right side
- [ ] Logo box (60px × 60px) with leaf icon
- [ ] Form inputs have 2px borders
- [ ] Input focus shows olive border
- [ ] "Forgot password?" link right-aligned
- [ ] Login button shows gradient
- [ ] Login button elevates on hover
- [ ] Google button visible (if configured)
- [ ] Divider line with "OR" text
- [ ] Register link at bottom

**Mobile View (< 768px)**
- [ ] Sidebar image hidden
- [ ] Single column layout
- [ ] Form centered
- [ ] All elements properly sized
- [ ] Touch targets >= 48px
- [ ] No horizontal scroll

**Interaction Tests**
- [ ] Username field accepts input
- [ ] Password field masks input
- [ ] Focus states show blue glow
- [ ] Buttons have hover effects
- [ ] Links change color on hover
- [ ] Enter key submits form

### Register Page (`/accounts/register/`)

**Visual Elements**
- [ ] White container with shadow
- [ ] Rounded corners (15px)
- [ ] Logo box at top center
- [ ] Green gradient background
- [ ] All form fields visible
- [ ] Phone number field marked optional
- [ ] Password requirements box visible
- [ ] Requirements box has left border
- [ ] Google button below form

**Form Fields**
- [ ] Username: Text input with placeholder
- [ ] Email: Email-type input
- [ ] Phone: Tel-type input with format hint
- [ ] Password1: Password-type input
- [ ] Password2: Password-type input (confirm)

**Password Requirements Box**
- [ ] Light gray background
- [ ] Left border accent (olive green)
- [ ] Lists 3 requirements
- [ ] Clear typography

**Error Handling**
- [ ] Try submitting empty form
- [ ] Error box appears (yellow background)
- [ ] Error icon displays
- [ ] Error messages specific to field
- [ ] Multiple errors all shown
- [ ] Error text in readable color

**Mobile Responsive**
- [ ] Container fits screen
- [ ] Padding adjusted for small screens
- [ ] Form fields stack properly
- [ ] Buttons are touchable

### Admin Interface (`/admin/`)

**Header Styling**
- [ ] Green gradient background (left to right)
- [ ] White text
- [ ] Leaf icon visible
- [ ] "OliveOshoppe Admin" text visible
- [ ] Header text is clickable
- [ ] Click navigates to admin home

**Sidebar Navigation**
- [ ] White/light background
- [ ] Section headers in olive green
- [ ] App names listed
- [ ] Links have proper spacing
- [ ] Links underline on hover
- [ ] Hover shows green accent border
- [ ] Selected item is bold
- [ ] Smooth transitions on hover

**Tables**
- [ ] Header row has gradient background
- [ ] Text in header is white
- [ ] Rows alternate colors (light gray/white)
- [ ] Rows have subtle bottom borders
- [ ] Hover on row shows light background
- [ ] Borders are rounded
- [ ] Shadow effect visible

**Forms**
- [ ] Input borders are 2px (not 1px)
- [ ] Input borders are gray
- [ ] Input padding is 12px
- [ ] Focus shows olive border
- [ ] Focus shows blue glow
- [ ] Labels are uppercase
- [ ] Labels are bold
- [ ] Labels are olive-green colored

**Buttons**
- [ ] Background gradient (olive medium to light)
- [ ] White text
- [ ] Rounded corners (6px)
- [ ] Shadow effect visible
- [ ] Hover: darker gradient
- [ ] Hover: elevated (2px up)
- [ ] Hover: stronger shadow
- [ ] Click: returns to normal

**Images**
- [ ] Product images have rounded corners
- [ ] Images have box shadow
- [ ] Hover on image: scales to 1.15x
- [ ] Zoom smooth transition
- [ ] Max width respected

**Messages**
- [ ] Success: Green background
- [ ] Error: Red background
- [ ] Warning: Yellow background
- [ ] Info: Blue background
- [ ] Left border visible
- [ ] Icons show before text

## 🎨 Color Verification

### Olive Green Palette
- [ ] Dark Olive: #2c5530 (used for headers, text)
- [ ] Medium Olive: #3d7a44 (used for buttons, links)
- [ ] Light Olive: #4e9f50 (used for accents, backgrounds)
- [ ] Lighter Olive: #7fb069 (used for highlights)

## 🔍 Cross-Browser Testing

Test in these browsers:
- [ ] Chrome/Chromium (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile Chrome
- [ ] Mobile Safari

## ⚡ Performance Check

- [ ] Pages load quickly
- [ ] No console errors
- [ ] No broken images
- [ ] CSS loads properly
- [ ] Animations are smooth
- [ ] No layout shift

## 📸 Visual Comparison

### Before (Old UI)
- Basic gradient background
- Simple white container
- Minimal styling
- Limited visual hierarchy

### After (New UI)
- Professional two-column layout (login)
- Modern shadow effects
- Smooth transitions
- Clear visual hierarchy
- Better error messaging
- Enhanced admin styling

## 🐛 Bug Reports Format

If you find an issue, report it as:

```
**Title**: [Brief description]
**Page**: [URL or page name]
**Browser**: [Chrome/Firefox/Safari/etc + version]
**Device**: [Desktop/Mobile + size]
**Screenshot**: [If possible]

**Steps to Reproduce**:
1. ...
2. ...
3. ...

**Expected**: [What should happen]
**Actual**: [What actually happens]
```

## 📱 Responsive Breakpoints

- **Mobile**: < 768px (single column, optimized)
- **Tablet**: 768px - 1024px (transitional)
- **Desktop**: > 1024px (full layout)

Test at these widths:
- [ ] 320px (iPhone SE)
- [ ] 375px (iPhone 12)
- [ ] 430px (Pixel 6)
- [ ] 768px (iPad)
- [ ] 1024px (iPad Pro)
- [ ] 1920px (Desktop)

## ✅ Sign-Off Checklist

Before considering UI complete:
- [ ] All pages load without errors
- [ ] Responsive design works on all breakpoints
- [ ] All colors match brand palette
- [ ] All buttons are clickable
- [ ] All forms work correctly
- [ ] Error messages display properly
- [ ] Admin interface is functional
- [ ] No console errors
- [ ] Performance is acceptable
- [ ] Cross-browser compatibility verified

---

**Last Updated**: November 20, 2025
**Version**: 1.0
