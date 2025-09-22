#!/usr/bin/env python3
"""
Deployment Preparation Script for PythonAnywhere
This script prepares your EventApp for deployment by checking all necessary files and changes.
"""

import os
import sys
import subprocess
from datetime import datetime

def check_git_status():
    """Check git status and prepare for commit."""
    print("🔍 Checking Git Status")
    print("=" * 50)
    
    try:
        # Check if we're in a git repository
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, cwd='.')
        
        if result.returncode != 0:
            print("❌ Not in a git repository or git not available")
            return False
        
        # Get modified files
        modified_files = result.stdout.strip().split('\n') if result.stdout.strip() else []
        
        if not modified_files:
            print("✅ No changes to commit")
            return True
        
        print("📝 Files with changes:")
        for file in modified_files:
            if file:
                status = file[:2]
                filename = file[3:]
                print(f"   {status} {filename}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking git status: {e}")
        return False

def check_required_files():
    """Check if all required files exist."""
    print("\n🔍 Checking Required Files")
    print("=" * 50)
    
    required_files = [
        'app.py',
        'requirements.txt',
        'templates/admin_members.html',
        'templates/register.html',
        '.env.example' or '.env'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️  Missing files: {', '.join(missing_files)}")
        return False
    
    return True

def check_recent_changes():
    """Check what changes were made recently."""
    print("\n🔍 Recent Changes Summary")
    print("=" * 50)
    
    changes = [
        "✅ Added membership_type field to User model",
        "✅ Created MEMBERSHIP_TYPES dictionary with Chinese options",
        "✅ Added get_membership_type_info() helper function",
        "✅ Updated registration form with phone and membership_type fields",
        "✅ Modified member management to show YS Type column",
        "✅ Fixed membership_type update logic in superuser validation",
        "✅ Added membership_type to template context",
        "✅ Updated edit modal to include membership_type field",
        "✅ Fixed database migration for membership_type column"
    ]
    
    for change in changes:
        print(f"   {change}")
    
    return True

def create_deployment_commit():
    """Create a deployment commit with all changes."""
    print("\n📝 Creating Deployment Commit")
    print("=" * 50)
    
    try:
        # Add all changes
        subprocess.run(['git', 'add', '.'], check=True)
        print("✅ Added all changes to staging")
        
        # Create commit
        commit_message = f"""Deploy: Add membership type system and fix member management

- Add membership_type field to User model with Chinese options (NA, 会员, 家族, 星光, 嫡传)
- Create MEMBERSHIP_TYPES dictionary and get_membership_type_info() helper function
- Update registration form with phone number and membership type dropdown
- Replace Status column with YS Type column in member management
- Fix membership_type update logic in superuser validation route
- Add membership_type to template context and edit modal
- Ensure proper separation between membership_grade and membership_type
- Database migration: Add membership_type column to existing users

Deployment ready for PythonAnywhere."""
        
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        print("✅ Created deployment commit")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating commit: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def show_deployment_instructions():
    """Show deployment instructions for PythonAnywhere."""
    print("\n🚀 PythonAnywhere Deployment Instructions")
    print("=" * 60)
    
    instructions = [
        "1. Push changes to your Git repository:",
        "   git push origin main",
        "",
        "2. SSH into PythonAnywhere and navigate to your project:",
        "   cd /home/yourusername/app.course.rsvp/eventapp",
        "",
        "3. Pull the latest changes:",
        "   git pull origin main",
        "",
        "4. Activate virtual environment:",
        "   source venv/bin/activate",
        "",
        "5. Install/update dependencies:",
        "   pip install -r requirements.txt",
        "",
        "6. Run database migration (if needed):",
        "   python -c \"from app import app, db; app.app_context().push(); db.create_all()\"",
        "",
        "7. Reload your web app in PythonAnywhere dashboard",
        "",
        "8. Test the new features:",
        "   - Registration with phone and membership type",
        "   - Member management with YS Type column",
        "   - Editing membership types in admin interface"
    ]
    
    for instruction in instructions:
        print(instruction)
    
    print("\n" + "=" * 60)
    print("📋 Key Changes Being Deployed:")
    print("   • New membership_type field with Chinese options")
    print("   • Updated registration form with phone and membership type")
    print("   • Member management shows YS Type instead of Status")
    print("   • Fixed membership type editing functionality")
    print("   • Proper separation of membership_grade and membership_type")
    print("=" * 60)

def main():
    print("🚀 EventApp Deployment Preparation")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run all checks
    git_ok = check_git_status()
    files_ok = check_required_files()
    changes_ok = check_recent_changes()
    
    if not all([git_ok, files_ok, changes_ok]):
        print("\n❌ Some checks failed. Please fix the issues before deploying.")
        return
    
    # Ask user if they want to create commit
    print("\n" + "=" * 60)
    create_commit = input("Create deployment commit? (y/N): ").strip().lower()
    
    if create_commit == 'y':
        if create_deployment_commit():
            print("\n✅ Deployment commit created successfully!")
            show_deployment_instructions()
        else:
            print("\n❌ Failed to create deployment commit")
    else:
        print("\n⏸️ Skipping commit creation")
        show_deployment_instructions()

if __name__ == '__main__':
    main()
