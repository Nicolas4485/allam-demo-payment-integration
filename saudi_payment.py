# Saudi Payment Integration | تكامل الدفع السعودي
import requests
import os

def process_payment(amount, transaction_id):
    """
    معالجة الدفع من خلال بوابة SADAD السعودية
    Process payment through SADAD Saudi gateway
    """
    # استخدام خادم سعودي - Saudi server
    api_url = "https://api.stc.com.sa/payment/v1/charge"
    
    payload = {
        'amount': amount,
        'transaction_id': transaction_id,
        'currency': 'SAR'
    }
    
    # إرسال طلب الدفع - Send payment request
    try:
        response = requests.post(
            api_url, 
            json=payload,
            headers={'Authorization': f'Bearer {os.getenv("PAYMENT_API_KEY")}'},
            timeout=10
        )
        
        if response.status_code == 200:
            return {
                'status': 'success', 
                'transaction_id': response.json()['id']
            }
        else:
            return {
                'status': 'failed',
                'error': response.json().get('message', 'Unknown error')
            }
    except requests.exceptions.RequestException as e:
        return {'status': 'failed', 'error': str(e)}

def calculate_saudi_vat(amount):
    """
    حساب ضريبة القيمة المضافة السعودية ١٥٪
    Calculate Saudi VAT at 15%
    """
    vat_rate = 0.15  # نسبة الضريبة السعودية - Saudi VAT rate
    vat_amount = amount * vat_rate
    
    return {
        'original_amount': amount,  # المبلغ الأصلي
        'vat_amount': vat_amount,   # قيمة الضريبة
        'total_amount': amount + vat_amount  # المبلغ الإجمالي
    }
```

**3. Commit changes**

Message: "Fix data sovereignty and VAT compliance issues"

**4. Create Pull Request:**

- Base: main
- Compare: feature/fix-compliance
- Title: "Fix Saudi compliance violations"
- Description: "Fixed data sovereignty (using STC), correct VAT (15%), added Arabic comments, improved security"

**5. Click "Create pull request"**

**6. Watch for ALLAM review:**

Within 10-30 seconds, ALLAM should comment on your PR with a review!

---

## PART 7: DEMO PREPARATION (15 minutes)

### **Prepare demo scenarios:**

---

### **Scenario 1: Chat Demo**

**Open chat interface:** `https://your-replit-url.repl.co`

**Test questions to prepare:**

1. **English:** "How do I integrate SADAD payment in Python?"
2. **Arabic:** "أريد كود لحساب ضريبة القيمة المضافة السعودية"
3. **Mixed:** "Create Saudi ID validation function with Arabic comments"

**Practice the flow:**
- Ask question → Get response with code → Show Arabic comments → Explain Saudi-specific features

---

### **Scenario 2: PR Review Demo**

**Prepare two PRs:**

**PR 1: Bad Code (Already created)**
- File: saudi_payment.py (original with violations)
- ALLAM should flag: Data sovereignty, wrong VAT, security issues

**PR 2: Fixed Code (Just created)**
- File: saudi_payment.py (fixed version)
- ALLAM should approve: Compliance passed

**Demo flow:**
- Show PR #1 with violations → Explain ALLAM caught issues
- Show PR #2 with fixes → Show ALLAM approved
- Explain continuous assistance loop

---

### **Scenario 3: Architecture Explanation**

**Prepare diagram/slides showing:**
```
Developer Workflow with ALLAM

Step 1: Ask ALLAM (Chat)
   "How do I build X?"
        ↓
   [ALLAM generates code with Arabic comments]
        ↓
   Developer copies to editor

Step 2: Write Code
   Developer adapts code to project
        ↓
   Commits to GitHub

Step 3: Auto Review (PR)
   ALLAM reviews automatically
        ↓
   Checks compliance (data sovereignty, VAT, security)
        ↓
   ✅ Approves OR ❌ Requests changes

Step 4: Continuous Learning
   ALLAM learns from approved code
        ↓
   Future suggestions improve
```

---

### **Talking Points:**

**Opening:**
"ALLAM Code Companion is one AI assistant that works everywhere Saudi developers work: in chat for learning, in PRs for compliance, throughout the entire development lifecycle."

**Key Differentiators:**
1. **Arabic-first:** Understands Arabic context, not just translation
2. **Saudi compliance:** Built-in rules for data sovereignty, VAT, ZATCA
3. **Continuous assistance:** Not one-time help, but ongoing throughout development
4. **Automated enforcement:** Compliance isn't optional, it's automatic

**Vision:**
"This becomes critical infrastructure for Vision 2030 digital projects. Every government agency, every contractor building for Saudi government, uses ALLAM to ensure code meets national standards."

**Roadmap:**
- Phase 1: Chat + GitHub (what I built today)
- Phase 2: VS Code extension + real-time linting
- Phase 3: Learning from agency codebases
- Phase 4: Platform for government-wide compliance

---

## TROUBLESHOOTING

### **If chat doesn't work:**

**Check:**
1. OpenAI API key is set in Replit Secrets
2. Replit app is running (green dot)
3. Console for errors
4. Test with curl: `curl -X POST https://your-url/api/chat -H "Content-Type: application/json" -d '{"message":"test"}'`

**Common fixes:**
- Restart Replit
- Check OpenAI account has credits
- Verify API key is correct

---

### **If GitHub webhook doesn't trigger:**

**Check:**
1. n8n workflow is active (toggle at top)
2. Webhook URL is correct in GitHub settings
3. GitHub webhook shows recent deliveries (Settings → Webhooks → Edit → Recent Deliveries)
4. Click "Redeliver" on a delivery to test

**Common fixes:**
- n8n might be sleeping (free tier) - execute workflow manually to wake it
- Check webhook secret matches if you set one
- Verify GitHub token has repo permissions

---

### **If ALLAM review is empty:**

**Check:**
1. Replit API is responding: test `/api/review-code` with Postman
2. OpenAI API call succeeded (check Replit logs)
3. n8n extracted code correctly (check execution data)

**Common fixes:**
- Add console.log in Replit code to debug
- Check n8n execution log for each node
- Verify code was actually passed to ALLAM endpoint

---

## TESTING CHECKLIST

Before demo:

**✅ Chat Interface:**
- [ ] Loads without errors
- [ ] Sends message successfully
- [ ] Receives response with code
- [ ] Copy button works
- [ ] Arabic input works (RTL displays correctly)
- [ ] Code blocks have syntax highlighting

**✅ PR Review:**
- [ ] Create PR triggers webhook
- [ ] n8n receives webhook
- [ ] Workflow executes all nodes
- [ ] ALLAM posts comment on PR
- [ ] Comment is formatted correctly (Arabic + English)
- [ ] Compliance violations detected correctly

**✅ End-to-End:**
- [ ] Ask chat for code
- [ ] Copy code to GitHub file
- [ ] Commit triggers review
- [ ] Review references similar patterns from chat

**✅ Presentation:**
- [ ] Can access chat from phone (mobile backup)
- [ ] GitHub PR is visible (not private repo)
- [ ] You can articulate the vision clearly
- [ ] You have talking points memorized

---

## DEMO DAY SETUP

### **30 minutes before:**

1. ✅ Test chat interface (ask 2-3 questions)
2. ✅ Verify PRs are visible
3. ✅ Check n8n workflow is active
4. ✅ Open all tabs you'll need
5. ✅ Have backup: record screen in case live demo fails

### **Tab setup:**
```
Tab 1: Chat interface (your main demo)
Tab 2: GitHub PR #1 (bad code with violations)
Tab 3: GitHub PR #2 (fixed code, approved)
Tab 4: n8n workflow (show architecture)
Tab 5: Replit code (if they ask technical questions)
Tab 6: Architecture diagram/slides
