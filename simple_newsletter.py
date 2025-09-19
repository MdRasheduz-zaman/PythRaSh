#!/usr/bin/env python3
"""
WORKING NEWSLETTER SOLUTION
Creates QMD that embeds your HTML newsletter content directly
"""

import os
import sys
import re
from datetime import datetime
import argparse

def create_perfect_newsletter_qmd(html_filename, date, title, description):
    """
    Create a QMD file that directly embeds your newsletter content
    """
    
    # Parse date
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%B %d, %Y")
    except ValueError:
        print(f"❌ Error: Invalid date format. Use YYYY-MM-DD")
        return False
    
    # Get just the filename without path
    html_basename = os.path.basename(html_filename)
    
    # Read the HTML newsletter content
    try:
        with open(html_filename, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Extract the body content (everything between <body> and </body>)
        body_match = re.search(r'<body[^>]*>(.*?)</body>', html_content, re.DOTALL | re.IGNORECASE)
        if body_match:
            newsletter_body = body_match.group(1)
        else:
            print(f"❌ Could not find <body> tags in HTML file")
            return False
            
        print(f"✅ Successfully extracted newsletter content ({len(newsletter_body)} characters)")
        
    except Exception as e:
        print(f"❌ Error reading HTML file: {e}")
        return False
    
    # Create QMD filename
    qmd_filename = html_filename.replace('.html', '.qmd')
    
    print(f"📄 Creating: {os.path.basename(qmd_filename)}")
    
    # Working QMD that embeds the content properly
    qmd_content = f'''---
title: "{title}"
subtitle: "Weekly AI Newsletter"
author: "Md Rasheduzzaman"
date: "{date}"
description: "{description}"
categories: [newsletter, AI, biology, healthcare]
format:
  html:
    toc: false
    page-layout: full
    css: newsletter.css
---

::: {{.callout-tip}}
## 📧 Newsletter Format

This is PythRaSh's AI Newsletter for {formatted_date}. You can [view the original newsletter]({html_basename}){{target="_blank"}} or [subscribe to receive it directly](https://forms.gle/ueS3aqeJsujHA48L9).
:::

```{{=html}}
<div style="width: 100%; margin: 2rem 0;">
  <div style="text-align: center; margin-bottom: 1rem;">
    <p><strong>Original Format:</strong> 
    <a href="{html_basename}" target="_blank" style="color: #667eea; text-decoration: none; font-weight: 600; padding: 8px 16px; border: 1px solid #667eea; border-radius: 4px;">📧 View Email Version</a></p>
  </div>
  
  <!-- Newsletter content -->
  <div style="width: 100%; background: white; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); overflow: hidden;">
{newsletter_body}
  </div>
</div>
```

---

## 🔗 Quick Actions

::: columns
::: {{.column width="50%"}}
### 📧 Subscribe
[Get weekly AI newsletters](https://forms.gle/ueS3aqeJsujHA48L9){{.btn .btn-primary}}

### 🔗 Share
- [Share on Twitter](https://twitter.com/intent/tweet?text=Check%20out%20PythRaSh%27s%20AI%20Newsletter&url=https://mdrasheduz-zaman.github.io/PythRaSh/ch/newsletter/)
- [Share on LinkedIn](https://www.linkedin.com/sharing/share-offsite/?url=https://mdrasheduz-zaman.github.io/PythRaSh/ch/newsletter/)
:::

::: {{.column width="50%"}}
### 📱 Connect
- [Website](https://mdrasheduz-zaman.github.io/PythRaSh/)
- [LinkedIn](https://www.linkedin.com/in/md-rashed-uz-zaman)
- [GitHub](https://github.com/mdrasheduz-zaman)

### 📋 Archive
[View all newsletters](index.qmd)
:::
:::

---

*Published on {formatted_date} | [Subscribe for weekly updates](https://forms.gle/ueS3aqeJsujHA48L9)*
'''

    # Write QMD file
    try:
        with open(qmd_filename, 'w', encoding='utf-8') as f:
            f.write(qmd_content)
        print(f"✅ Created: {os.path.basename(qmd_filename)}")
        return True
    except Exception as e:
        print(f"❌ Error writing QMD file: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='Create newsletter QMD with embedded content',
        epilog='''
WORKING NEWSLETTER WORKFLOW:
1. Save your HTML newsletter in ch/newsletter/
2. Run: python simple_newsletter.py your_newsletter.html --date "2025-09-15" --title "Your Title" --description "Description"
3. Run: quarto render
4. Newsletter content displays in archive!

Examples:
  python simple_newsletter.py ch/newsletter/AI_Newsletter_2025_09_15.html -d "2025-09-15" -t "AI Newsletter - Sept 15, 2025" --desc "Weekly update"
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('html_file', help='Your HTML newsletter file (path + filename)')
    parser.add_argument('--date', '-d', required=True, help='Newsletter date (YYYY-MM-DD)')
    parser.add_argument('--title', '-t', required=True, help='Newsletter title')
    parser.add_argument('--description', '--desc', required=True, help='Newsletter description')
    
    args = parser.parse_args()
    
    # Check if HTML file exists
    if not os.path.exists(args.html_file):
        print(f"❌ HTML file not found: {args.html_file}")
        print(f"📁 Current directory: {os.getcwd()}")
        return 1
    
    # Create QMD with embedded content
    success = create_perfect_newsletter_qmd(
        args.html_file,
        args.date,
        args.title, 
        args.description
    )
    
    if success:
        print(f"\n🎉 SUCCESS! Newsletter content embedded.")
        print(f"📝 What happened:")
        print(f"   ✅ Extracted newsletter body content")
        print(f"   ✅ Created QMD with direct embedding")
        print(f"   ✅ Newsletter content will display in archive")
        print(f"\n🚀 Next steps:")
        print(f"   1. Run: quarto render")
        print(f"   2. Your newsletter content will be visible!")
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())
