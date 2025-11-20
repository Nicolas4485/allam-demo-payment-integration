# Saudi Payment Integration
import requests

def process_payment(amount, card_number, cvv):
    # Process payment through gateway
    api_url = "https://us-payment-processor.com/api/v1/charge"
    
    payload = {
        'amount': amount,
        'card': card_number,
        'cvv': cvv,
        'currency': 'SAR'
    }
    
    # Send payment request
    response = requests.post(api_url, json=payload)
    
    if response.status_code == 200:
        return {'status': 'success', 'transaction_id': response.json()['id']}
    else:
        return {'status': 'failed'}

def calculate_vat(amount):
    tax_rate = 0.10  # Tax rate
    return amount * tax_rate
```

**Issues planted:**
- ❌ Data sovereignty: US server URL
- ❌ Wrong VAT rate (10% instead of 15%)
- ❌ Security: CVV in payload
- ❌ No Arabic comments
- ❌ No error handling

**4. Commit to main branch**

**5. Note your repo details:**
- Owner: `[your-github-username]`
- Repo: `allam-demo-payment-integration`

---

## PART 3: BUILD UNIFIED BACKEND IN REPLIT (90 minutes)

### **Open Replit.com**

**Create new Repl:**
- Template: "Node.js"
- Name: "ALLAM-Code-Companion-Backend"

---

### **PROMPT 1: Project Setup**

Copy this into Replit Agent:
```
Create a unified backend for ALLAM Code Companion with these requirements:

PROJECT STRUCTURE:
- Express.js server
- Three main API endpoints:
  1. POST /api/chat - For web chat interface
  2. POST /api/review-code - For GitHub PR reviews
  3. POST /api/compliance-check - Shared compliance rules

FEATURES:
- OpenAI integration for AI responses
- Saudi compliance rules checking
- Context memory (store conversation history)
- Arabic/English bilingual responses
- Formatted code output with syntax highlighting

ENVIRONMENT VARIABLES:
- OPENAI_API_KEY
- PORT (default 3000)

INSTALL PACKAGES:
- express
- cors
- dotenv
- openai
- axios

Create the basic server structure with CORS enabled and error handling.
```

---

### **PROMPT 2: Saudi Compliance Rules Engine**
```
Create a Saudi compliance checker module at /utils/complianceChecker.js with these rules:

COMPLIANCE RULES:

1. DATA SOVEREIGNTY:
   - Check for foreign API endpoints (aws, azure, google, .us, .eu domains)
   - Flag as CRITICAL violation
   - Suggest Saudi cloud alternatives (STC Cloud, Alibaba Cloud Saudi)

2. VAT CALCULATION:
   - Check for tax/vat calculations
   - Verify 15% rate (0.15)
   - Flag if using wrong rate (0.05, 0.10, 0.20)
   - This is CRITICAL for Saudi compliance

3. ARABIC DOCUMENTATION:
   - Check if code has Arabic comments
   - Use regex: /[\u0600-\u06FF]/ to detect Arabic
   - Flag as WARNING if no Arabic found

4. SECURITY:
   - Check for hardcoded secrets (api_key, password, token patterns)
   - Check for CVV/sensitive data in plain text
   - Flag as CRITICAL

5. ZATCA E-INVOICING:
   - Check for invoice/فاتورة keywords
   - Check if ZATCA API integration exists
   - Flag as WARNING if missing

FUNCTION SIGNATURE:
function checkCompliance(code) {
  return {
    violations: [
      {
        type: 'CRITICAL' | 'WARNING',
        rule: 'Data Sovereignty',
        message: 'English explanation',
        messageAr: 'Arabic explanation',
        line: lineNumber (if detectable),
        fix: 'Suggested fix',
        fixAr: 'Arabic fix suggestion'
      }
    ],
    score: 'PASS' | 'PASS_WITH_WARNINGS' | 'FAIL',
    passedChecks: [],
    failedChecks: []
  }
}

Export this function for use by API endpoints.
```

---

### **PROMPT 3: Chat API Endpoint**
```
Create POST /api/chat endpoint with these features:

REQUEST BODY:
{
  "message": "user question in Arabic or English",
  "conversationHistory": [] // optional, array of previous messages
}

LOGIC:
1. Detect language (Arabic or English)
2. Call OpenAI API with this system prompt:

SYSTEM PROMPT:
"You are ALLAM (علام), an AI coding assistant for Saudi developers. You help write code that complies with Saudi regulations.

KEY CAPABILITIES:
- Respond in the SAME language the user uses (Arabic or English)
- Generate code with Arabic comments explaining key parts
- Include Saudi-specific context (15% VAT, SAR currency, SADAD payment, ZATCA e-invoicing)
- Always mention data sovereignty (use Saudi cloud providers)
- Security-first approach
- Follow Saudi government coding standards

RESPONSE FORMAT:
When generating code:
1. Brief explanation in user's language
2. Code block with Arabic comments
3. Key points about Saudi compliance
4. Related considerations

Be concise, practical, and Saudi-context aware."

3. Store conversation in memory (simple in-memory array for demo)
4. Return formatted response with code blocks

RESPONSE FORMAT:
{
  "response": "AI response text",
  "code": "extracted code if any",
  "language": "detected programming language",
  "hasArabic": boolean
}

Add proper error handling and OpenAI API error messages.
```

---

### **PROMPT 4: Code Review API Endpoint**
```
Create POST /api/review-code endpoint for GitHub PR reviews:

REQUEST BODY:
{
  "code": "code to review",
  "filename": "file being reviewed",
  "context": "optional PR context"
}

LOGIC:
1. Run compliance checker on code
2. Call OpenAI to analyze code quality
3. Combine compliance violations + AI insights
4. Format as GitHub-ready comment

OPENAI PROMPT FOR CODE REVIEW:
"You are ALLAM reviewing code for Saudi government projects.

Analyze this code for:
1. Code quality (readability, structure, best practices)
2. Security vulnerabilities
3. Performance issues
4. Saudi-specific concerns

Current file: {filename}

Code:
{code}

Provide review in both Arabic and English. Be specific with line numbers if issues found. Focus on actionable feedback."

RESPONSE FORMAT:
Return formatted markdown for GitHub comment:
```markdown
# 🇸🇦 ALLAM Code Review | مراجعة الكود

## Compliance Check | فحص الامتثال

[Insert compliance violations from complianceChecker]

## Code Quality Review | مراجعة جودة الكود

[Insert OpenAI analysis]

## Summary | الملخص

**Status:** [PASS ✅ | FAIL ❌ | WARNINGS ⚠️]

---
*Reviewed by ALLAM | راجعه علام* 🤖
```

Make the markdown beautiful and professional.
```

---

### **PROMPT 5: Environment Setup**
```
Create .env.example file with:

OPENAI_API_KEY=your_openai_api_key_here
PORT=3000
NODE_ENV=development

Add instructions in README.md for:
1. Copy .env.example to .env
2. Add your OpenAI API key
3. Run: npm install
4. Run: npm start
5. Test endpoints with curl examples

Also add .gitignore to exclude:
- node_modules/
- .env
- *.log
```

---

### **PROMPT 6: Add Simple Web Chat UI**
```
Create a simple web chat interface at /public/index.html that:

FEATURES:
- Clean, minimal chat interface
- Input field for messages (supports Arabic RTL)
- Send button
- Chat history display
- Code blocks with syntax highlighting
- Copy code button
- Saudi-themed colors (green/white)

STYLING:
- Use Tailwind CSS from CDN
- Google Fonts: Cairo for Arabic, Inter for English
- Responsive design
- RTL support for Arabic messages

JAVASCRIPT:
- Fetch API to call /api/chat
- Handle loading states
- Display responses with proper formatting
- Store chat history in browser localStorage
- Detect Arabic text and apply RTL

Make it production-ready and beautiful. Add ALLAM branding (Saudi flag emoji, green theme).

Serve this from Express using express.static('public').
```

---

### **PROMPT 7: Test Scenarios**
```
Create a /test-scenarios.md file with example requests for testing:

SCENARIO 1 - Chat: Saudi Payment Integration
Request:
POST /api/chat
{
  "message": "How do I integrate SADAD payment gateway in Python?"
}

Expected: Code with Arabic comments, Saudi-specific guidance

SCENARIO 2 - Chat: VAT Calculation (Arabic)
Request:
POST /api/chat
{
  "message": "أريد كود لحساب ضريبة القيمة المضافة السعودية"
}

Expected: Arabic response with code

SCENARIO 3 - Code Review: Bad Code
Request:
POST /api/review-code
{
  "code": "[paste the saudi_payment.py code with violations]",
  "filename": "saudi_payment.py"
}

Expected: Violations for data sovereignty, wrong VAT, security issues

Add curl commands for each scenario for easy testing.
```

---

### **After all prompts complete:**

**1. Add your OpenAI API key:**
- Go to Secrets (lock icon in Replit sidebar)
- Add: `OPENAI_API_KEY` = `your-key-here`

**2. Click "Run"**

**3. Test the chat interface:**
- Open the webview
- Try: "How do I calculate Saudi VAT?"
- Should get response with code

**4. Note the URL:**
- Should be like: `https://allam-code-companion-backend.your-username.repl.co`
- You'll need this for n8n

---

## PART 4: SETUP N8N WORKFLOW (60 minutes)

### **Open your n8n Agent project**

**Create new workflow: "ALLAM GitHub PR Review"**

---

### **N8N AGENT PROMPT:**
```
Create a complete n8n workflow that receives GitHub webhook events and reviews pull requests using ALLAM.

WORKFLOW STRUCTURE:

NODE 1: Webhook Trigger
- Name: "GitHub PR Webhook"
- Method: POST
- Path: /github-webhook
- Return immediately: false

NODE 2: Filter - Only PR Events
- Name: "Filter PR Events"
- IF: {{ $json.action }} equals "opened" OR "synchronize"
- This ensures we only process new PRs or PR updates

NODE 3: Extract PR Data
- Name: "Extract PR Info"
- Type: Function
- Code to extract:
  - PR number: {{ $json.number }}
  - Repo owner: {{ $json.repository.owner.login }}
  - Repo name: {{ $json.repository.name }}
  - PR author: {{ $json.pull_request.user.login }}
  - PR URL: {{ $json.pull_request.html_url }}

NODE 4: Get PR Files
- Name: "Get Changed Files"
- Type: HTTP Request
- Method: GET
- URL: https://api.github.com/repos/{{$node["Extract PR Info"].json.owner}}/{{$node["Extract PR Info"].json.repo}}/pulls/{{$node["Extract PR Info"].json.pr_number}}/files
- Authentication: Bearer Token
- Token: {{ $credentials.githubToken }}
- Returns array of changed files

NODE 5: Get File Contents
- Name: "Fetch File Content"
- Type: HTTP Request
- Loop over files from previous node
- Method: GET
- URL: {{ $json.raw_url }}
- Returns file content as text

NODE 6: Review with ALLAM
- Name: "ALLAM Code Review"
- Type: HTTP Request
- Method: POST
- URL: https://[YOUR-REPLIT-URL]/api/review-code
- Body:
{
  "code": "{{ $json.content }}",
  "filename": "{{ $json.filename }}",
  "context": "PR #{{ $node["Extract PR Info"].json.pr_number }}"
}
- Returns ALLAM review in markdown

NODE 7: Format Comment
- Name: "Format GitHub Comment"
- Type: Function
- Combine all file reviews into one comment
- Add header with PR info
- Format markdown nicely

NODE 8: Post Comment to PR
- Name: "Post Review Comment"
- Type: HTTP Request
- Method: POST
- URL: https://api.github.com/repos/{{$node["Extract PR Info"].json.owner}}/{{$node["Extract PR Info"].json.repo}}/issues/{{$node["Extract PR Info"].json.pr_number}}/comments
- Authentication: Bearer Token
- Body:
{
  "body": "{{ $node["Format GitHub Comment"].json.comment }}"
}

NODE 9: Update PR Status
- Name: "Set PR Status"
- Type: HTTP Request
- IF review passed: Approve PR
- IF review failed: Request changes
- Method: POST
- URL: https://api.github.com/repos/.../pulls/.../reviews
- Body includes review decision

Connect all nodes in sequence and test the workflow.

IMPORTANT: Add error handling nodes after critical steps (API calls) to catch failures gracefully.
